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

# Scenes and actions for the image generation
scenes = [
    "home",
    "shopping",
    "yacht",
    "Private Jet Interior",
    "High-End Cafe",
    "Co-Working Space",
    "Beach"
]

actions = [
    "actively engaged in various digital marketing activities with elements like a sleek computer screen displaying a high-value digital product",
    "managing social media campaigns using a multi-screen setup",
    "crafting a digital marketing campaign, sketching out ideas on a digital tablet",
    "creating 'Live' video for social media with her mobile phone"
]

# Generate and save images
num_images = 2  # Define the number of images to generate
for i in range(num_images):
    selected_scene = random.choice(scenes)
    selected_action = random.choice(actions)
    prompt = f"Create a dynamic, very realistic image that captures the essence of a successful digital marketing lifestyle, tailored for women in a luxurious {selected_scene}, featuring a young female entrepreneur {selected_action}. The setting should be chic and high-tech with darker, moody lighting to enhance the atmosphere of exclusivity and success."

    # Payload for the POST request to generate images
    payload = {
        "height": 1024,
        "prompt": prompt,
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