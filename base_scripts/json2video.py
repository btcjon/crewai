import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Your API key from the .env file
api_key = os.getenv('JSON2VIDEO_API_KEY')

# JSON payload that describes the video
video_json = {
    "scenes": [
        {
            "elements": [
                {
                    "type": "text",
                    "text": "Hello, World!",
                    "start": 0,
                    "duration": 5
                }
            ]
        }
    ]
}

# API endpoint
url = 'https://api.json2video.com/v2/movies'

# Headers including the required API key
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

# Making the POST request to create the movie
response = requests.post(url, json=video_json, headers=headers)

# Checking the response
if response.status_code == 200:
    print("Movie creation started successfully.")
    print("Project ID:", response.json()['project'])
else:
    print("Failed to start movie creation:", response.text)