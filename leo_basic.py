import requests
import json
import os
import random
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the API URL and headers
post_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
api_key = os.getenv('LEONARDO_API_KEY')
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

# Define prompt improvement URL
prompt_improve_url = "https://cloud.leonardo.ai/api/rest/v1/prompt/improve"

# Predefined prompts
prompts = [
    "a successful young female digital marketer in a luxurious setting (home, yacht, cafe, beach, poolside, or similar), using high-tech devices for her work",
    "a successful young female digital marketer in a luxurious setting enjoying her leisure time that success has afforded. Having a fun time with friends or family"
]

# Generate and save images
num_images = 3  # Define the number of images to generate
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
                        image_dir = './leo_images'
                        if not os.path.exists(image_dir):
                            os.makedirs(image_dir)
                        for img in get_data['generations_by_pk']['generated_images']:
                            image_url = img['url']
                            image_response = requests.get(image_url)
                            if image_response.status_code == 200:
                                image_filename = image_url.split("/")[-1]
                                with open(f'{image_dir}/{image_filename}', 'wb') as f:
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
