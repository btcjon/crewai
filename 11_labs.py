import os
import openai
import requests
import boto3
from mutagen.mp3 import MP3
from dotenv import load_dotenv

# Setup basic configuration for logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
XI_API_KEY = os.getenv('XI_API_KEY')
BUCKET_NAME = "cashdaily1"
VOICE_ID = "4dyF1bD2mjNHsB76Wf9q"

if not OPENAI_API_KEY or not XI_API_KEY:
    logging.error("API keys are not set in environment variables.")
    exit(1)

# Initialize OpenAI client with the new interface
openai.api_key = OPENAI_API_KEY

# Step 1. Ask user for the relative path to the script.txt file and the step to start from
text_file_path = input("Enter the relative path to your script.txt file: ")
start_step = 1

if not os.path.isfile(text_file_path):
    logging.error(f"The file {text_file_path} does not exist.")
    exit(1)

text_file_dir = os.path.dirname(os.path.abspath(text_file_path))

# Step 2. Read text from file
    try:
        with open(text_file_path, 'r') as file:
            text_to_speak = file.read()
        logging.info("Text read successfully from script.txt")
    except Exception as e:
        logging.error(f"Failed to read text file: {str(e)}")
        exit(1)

# Step 3. Generate a folder name using OpenAI
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Ensure to use a supported model
            prompt=f"Generate a concise, descriptive name for a folder based on the following text: {text_to_speak}",
            max_tokens=10,
            temperature=0.7
        )
        folder_name = response.choices[0].text.strip()
        folder_path = os.path.join(text_file_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        logging.info(f"Folder created: {folder_path}")
    except Exception as e:
        logging.error(f"OpenAI API error or folder creation error: {str(e)}")
        exit(1)



# Step 4: Send text to elevenlabs for voice mp3 generation
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    data = {
        "text": text_to_speak,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }
    response = requests.post(tts_url, headers=headers, json=data, stream=True)
    if response.ok:
        logging.info("Text-to-Speech API call successful")
        # Save the audio stream to a file
        LOCAL_FILE_PATH = os.path.join(folder_path, f"{folder_name}.mp3")
        with open(LOCAL_FILE_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        logging.info(f"Audio stream saved successfully as {LOCAL_FILE_PATH}")

        # Step 4: Find length of mp3 file
        try:
            audio = MP3(LOCAL_FILE_PATH)
            total_length = int(audio.info.length)
            logging.info(f"Audio length: {total_length} seconds")

            # Step 6: Calculate total scenes
            total_scenes = round(total_length / 5)
            logging.info(f"Total scenes calculated: {total_scenes}")

            # Step 7: Upload mp3 file to s3
            S3_KEY = f"{folder_name}/{os.path.basename(LOCAL_FILE_PATH)}"
            s3_client = boto3.client('s3')
            s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
            s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{S3_KEY}"
            logging.info(f"File uploaded to S3 at URL: {s3_url}")

            # Step 8: Save the URL, audio length, and total scenes to assets.txt
            with open(os.path.join(folder_path, 'assets.txt'), 'a') as file:
                file.write(f"MP3 URL: {s3_url}\n")
                file.write(f"Total Length: {total_length} seconds\n")
                file.write(f"Total Scenes: {total_scenes}\n")
            logging.info("URL, audio length, and total scenes saved to assets.txt in the script directory")
        except Exception as e:
            logging.error(f"Error during MP3 handling or S3 upload: {str(e)}")
    else:
        logging.error(f"Failed to generate speech: {response.text}")

# Begin Image generation process. 1 image per scene
# Define the API URL and headers
post_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
api_key = os.getenv('LEONARDO_API_KEY')
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

# Step 9: Improve prompts for images. Define prompt improvement URL
prompt_improve_url = "https://cloud.leonardo.ai/api/rest/v1/prompt/improve"

# Predefined prompts
prompts = [
    "a successful young female digital marketer in a luxurious setting (home, yacht, cafe, beach, poolside, or similar), using high-tech devices for her work",
    "a successful young female digital marketer in a luxurious setting enjoying her leisure time that success has afforded. Having a fun time with friends or family"
]

# Step 10: Read the total scenes from assets.txt to determine the number of images to generate
assets_file_path = os.path.join(folder_path, 'assets.txt')
try:
    with open(assets_file_path, 'r') as file:
        lines = file.readlines()
        total_scenes_line = next(line for line in lines if "Total Scenes" in line)
        num_images = int(total_scenes_line.split(': ')[1].strip())  # Extract the number of scenes
except Exception as e:
    logging.error(f"Failed to read or parse assets.txt: {str(e)}")
    exit(1)

# Now num_images is set dynamically based on the total scenes
print(f"Number of images to generate: {num_images}")


for i in range(num_images):
    # Randomly choose between the predefined prompts
    chosen_prompt = random.choice(prompts)
    print(f"Using original prompt: {chosen_prompt}")  # Debugging line to check which prompt is chosen

    # Improve the prompt using the API
    improve_payload = {"prompt": chosen_prompt}
    improve_response = requests.post(prompt_improve_url, json=improve_payload, headers=headers)
    
    # Wait for 5 seconds to ensure the prompt has been improved
    time.sleep(5)

    if improve_response.status_code == 200:
        response_json = improve_response.json()
        improved_prompt = response_json.get('promptGeneration', {}).get('prompt', None)
        
        # Debugging line to check the full response from the API
        print("API Improve Response:", json.dumps(response_json, indent=4))
        
        # Check if the prompt was actually improved
        if improved_prompt is None or improved_prompt == chosen_prompt:
            print("No improvement on the prompt. Stopping the process.")
            continue  # Skip this iteration or use `break` to stop the entire loop
        
        print(f"Improved prompt: {improved_prompt}")  # Debugging line to check the improved prompt
    else:
        print("Failed to improve prompt, using base prompt.")  # Debugging line for failure case
        print("HTTP Status:", improve_response.status_code, "Response:", improve_response.text)  # Additional debugging information
        continue  # Skip this iteration or use `break` to stop the entire loop

    # Payload for the POST request to generate images
    payload = {
        "height": 1024,
        "prompt": improved_prompt,  # Ensure this uses the improved prompt
        "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",
        "width": 576,
        "alchemy": True,
        "photoReal": True,
        "photoRealVersion": "v2",
        "presetStyle": "CINEMATIC",
        "num_images": 1
    }

    # Make the POST request to generate images
    post_response = requests.post(post_url, headers=headers, json=payload)
    if post_response.status_code == 200:
        post_data = post_response.json()
        print("API Response:", json.dumps(post_data, indent=4))
        generation_id = post_data['sdGenerationJob']['generationId']
        max_attempts = 20
        attempts = 0
        while attempts < max_attempts:
            get_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
            get_response = requests.get(get_url, headers=headers)
            if get_response.status_code == 200:
                get_data = get_response.json()
                if get_data['generations_by_pk']['status'] == 'COMPLETE':
                    if get_data['generations_by_pk']['generated_images']:
                        # Use the folder_path from earlier in the script
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        for img in get_data['generations_by_pk']['generated_images']:
                            image_url = img['url']
                            image_response = requests.get(image_url)
                            if image_response.status_code == 200:
                                image_filename = image_url.split("/")[-1]
                                with open(f'{folder_path}/{image_filename}', 'wb') as f:
                                    f.write(image_response.content)
                                print(f"Image downloaded successfully: {image_url}")
                        break
                    else:
                        print("No images generated yet, checking again...")
                elif get_data['generations_by_pk']['status'] == 'FAILED':
                    print("Generation failed.")
                    break
            else:
                print("Failed to retrieve generation details, HTTP Status:", get_response.status_code)
            time.sleep(15)
            attempts += 1
        if attempts == max_attempts:
            print("Maximum attempts reached, generation may still be processing.")
    else:
        print("Failed to generate images, HTTP Status:", post_response.status_code, "Response:", post_response.text)

    # Step 11: Upload all images to S3 once they are all downloaded
    for local_image_path in local_image_paths:
        image_filename = os.path.basename(local_image_path)
        s3_key = f"{folder_name}/{image_filename}"
        s3_client.upload_file(local_image_path, BUCKET_NAME, s3_key)
        s3_image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        print(f"Image uploaded to S3 at URL: {s3_image_url}")

        # Optionally save the S3 URL to assets.txt
        with open(os.path.join(folder_path, 'assets.txt'), 'a') as file:
            file.write(f"S3 Image URL: {s3_image_url}\n")
