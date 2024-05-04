import os
import random
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv('LEONARDO_API_KEY')

# Check if the API key is loaded correctly
if API_KEY is None:
    print("Failed to load API KEY. Check your .env file.")
    exit(1)

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=API_KEY)

# Directory to save images
save_path = 'path_to_save_images'
os.makedirs(save_path, exist_ok=True)

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

num_images = 2  # Number of images to generate

def generate_image(prompt):
    try:
        # Set up the request body with the desired parameters
        body = {
            "prompt": prompt,
            "modelId": "b24e16ff-06e3-43eb-8d33-4416c2d75876",  # Ensure this is the correct model ID
            "photoReal": True,
            "photoRealVersion": "v2",
            "alchemy": True,
            "presetStyle": "CINEMATIC",
            "width": 576,  # Adjusted for 9:16 ratio
            "height": 1024,  # Adjusted for 9:16 ratio
            "num_images": 1
        }
        
        # Make the POST request to Leonardo's API
        response = requests.post(
            'https://cloud.leonardo.ai/api/rest/v1/generations',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json=body
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to generate image: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"Failed to generate image: {str(e)}")
        print("Error details:", e.args)
        return None


# Generate and save images
for i in range(num_images):
    selected_scene = random.choice(scenes)
    selected_action = random.choice(actions)
    prompt = f"Create a dynamic, very realistic image that captures the essence of a successful digital marketing lifestyle, tailored for women in a luxurious {selected_scene}, featuring a young female entrepreneur {selected_action}. The setting should be chic and high-tech with darker, moody lighting to enhance the atmosphere of exclusivity and success."
    
    image_data = generate_image(prompt)
    if image_data and 'data' in image_data and image_data['data']:
        image_url = image_data['data'][0]['url']
        image_response = requests.get(image_url)
        
        # Save the image
        with open(os.path.join(save_path, f'image_{i+1}.png'), 'wb') as file:
            file.write(image_response.content)
        print(f'Image {i+1} saved.')
    else:
        print("Image generation failed, skipping save.")
