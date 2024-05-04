import os
import random
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

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
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            quality="standard",
            n=1
        )
        return response
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
