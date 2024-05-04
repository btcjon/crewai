import os
import openai
import requests
import time
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_and_save_images(num_images, save_path):
    api_key = os.getenv('OPENAI_API_KEY')
    client = openai.OpenAI(api_key=api_key)
    
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
        "Actively engaged in various digital marketing activities. She should be interacting with elements like a sleek computer screen displaying a high-value digital product, and visible notifications of successful transactions.",
        "Managing Social Media: Showing her managing social media campaigns using a multi-screen setup, demonstrating her engagement with current trends and her influence in real-time.",
        "Creating Content: Illustrating her crafting a digital marketing campaign, perhaps sketching out ideas on a digital tablet or brainstorming with an interactive whiteboard, which emphasizes her creative process.",
        "Creating “Live” video for social media with her mobile phone"
    ]

    os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

    for i in range(num_images):
        selected_scene = random.choice(scenes)
        selected_action = random.choice(actions)
        
        prompt = f"Create a dynamic, very realistic image that captures the essence of a successful digital marketing lifestyle, tailored for women. The overall setting should be chic and high-tech, reflecting a sense of wealth and cutting-edge innovation. This vibrant and motivating atmosphere should ideally convey the lucrative potential of digital sales that guarantees significant earnings. Should depict a modern, luxurious {selected_scene}. Feels both elegant and sophisticated with darker, moody lighting to enhance the atmosphere of exclusivity and success. Feature a young female entrepreneur {selected_action}"

        response = client.images.generate(
            model="dall-e-3",  # Replace with the correct model name
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1792"  # Corrected image resolution for 9:16 aspect ratio
        )
        
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        
        timestamp = int(time.time())
        filename = f'image_{i}_{timestamp}.png'
        full_path = os.path.join(save_path, filename)
        
        with open(full_path, 'wb') as f:
            f.write(image_response.content)
        print(f"Image {i} saved as {full_path}.")

# Example usage
num_images = int(input("Enter the number of images to generate: "))
save_path = input("Enter the relative path where images should be saved: ")
generate_and_save_images(num_images, save_path)