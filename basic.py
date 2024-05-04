import os
from dotenv import load_dotenv
from openai import OpenAI
import traceback

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

if not API_KEY:
    print("Failed to load API KEY. Check your .env file.")
    exit(1)

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=API_KEY)

def generate_image(prompt):
    try:
        # Attempting to generate a single image with minimal parameters
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            quality="standard",
            n=1
        )
        print("Image generation successful!")
        return response
    except Exception as e:
        print(f"Failed to generate image: {str(e)}")
        traceback.print_exc()  # Print detailed traceback
        return None

# Generate a simple image
prompt = "A simple, beautiful landscape painting."
image_response = generate_image(prompt)

# If image generation was successful, print the image URL
if image_response and 'data' in image_response and image_response['data']:
    print("Image URL:", image_response['data'][0]['url'])
else:
    print("No image data received.")
