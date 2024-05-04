import requests
import os
import random
from dotenv import load_dotenv
load_dotenv()

url = "https://cloud.leonardo.ai/api/rest/v1/prompt/improve"
prompt1 = "a successful young female digital marketer in a luxurious setting (home, yacht, cafe, beach, poolside, or similar), using high-tech devices for her work"
prompt2 = "a successful young female digital marketer in a luxurious setting enjoying her leisure time that success has afforded. Having a fun time with friends or family"

# Randomly choose between prompt1 and prompt2
chosen_prompt = random.choice([prompt1, prompt2])

payload = { "prompt": chosen_prompt }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {os.getenv('LEONARDO_API_KEY')}"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)