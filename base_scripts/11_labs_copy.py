import os
import requests
import boto3
import logging
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
from mutagen.mp3 import MP3
from dotenv import load_dotenv

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Constants
XI_API_KEY = os.getenv('XI_API_KEY')
if not XI_API_KEY:
    logging.error("XI_API_KEY is not set in environment variables.")
    exit(1)  # Exit if critical environment variable is missing

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY is not set in environment variables.")
    exit(1)

BUCKET_NAME = "cashdaily1"
VOICE_ID = "4dyF1bD2mjNHsB76Wf9q"

# Step 1: Ask user for the relative path to the script.txt file and the step to start from
text_file_path = input("Enter the relative path to your script.txt file: ")
start_step = int(input("Enter the step number to start from (1-10): "))

if not os.path.isfile(text_file_path):
    logging.error(f"The file {text_file_path} does not exist.")
    exit(1)

text_file_dir = os.path.dirname(os.path.abspath(text_file_path))
assets_file_path = os.path.join(text_file_dir, "assets.txt")

# Step 2: Read text from file
if start_step <= 2:
    try:
        with open(text_file_path, 'r') as file:
            text_to_speak = file.read()
        logging.info("Text read successfully from script.txt")
    except Exception as e:
        logging.error(f"Failed to read text file: {str(e)}")
        exit(1)

# Step 3: Use OpenAI to generate a folder name using chat model
if start_step <= 3:
    try:
          # Set API key

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate a concise, descriptive name for a folder based on the following text: {text_to_speak}"}
        ])
        folder_name = response.choices[0].message.content.strip()
        logging.info(f"Generated folder name: {folder_name}")

        # Step 4: Create folder if it doesn't exist
        folder_path = os.path.join(text_file_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Folder created: {folder_path}")
    except Exception as e:
        logging.error(f"OpenAI API error or folder creation error: {str(e)}")
        exit(1)

# Steps 5-6: Ensure text_to_speak is defined if starting from these steps

# Step 6: Send text to elevenlabs for voice mp3 generation
if start_step <= 6:
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
        LOCAL_FILE_PATH = os.path.join(folder_path, "output.mp3")  # Define path dynamically
        with open(LOCAL_FILE_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        logging.info(f"Audio stream saved successfully as {LOCAL_FILE_PATH}")

        # Step 7: Find length of mp3 file
        try:
            audio = MP3(LOCAL_FILE_PATH)
            total_length = int(audio.info.length)
            logging.info(f"Audio length: {total_length} seconds")

            # Step 8: Calculate total scenes
            total_scenes = round(total_length / 5)
            logging.info(f"Total scenes calculated: {total_scenes}")

            # Step 9: Upload mp3 file to s3
            S3_KEY = os.path.basename(LOCAL_FILE_PATH)  # Define S3 key based on file name
            s3_client = boto3.client('s3')
            s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
            s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{S3_KEY}"
            logging.info(f"File uploaded to S3 at URL: {s3_url}")

            # Step 10: Save the URL, audio length, and total scenes to assets.txt
            with open(assets_file_path, "a") as file:
                file.write(f"{s3_url}\n")
                file.write(f"total_length:{total_length}\n")
                file.write(f"total_scenes:{total_scenes}\n")
            logging.info("URL, audio length, and total scenes saved to assets.txt in the script directory")
        except Exception as e:
            logging.error(f"Error during MP3 handling or S3 upload: {str(e)}")
    else:
        logging.error(f"Failed to generate speech: {response.text}")
