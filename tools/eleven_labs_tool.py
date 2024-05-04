from crewai_tools import BaseTool
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field

class ElevenLabsTool(BaseTool):
    name: str = "ElevenLabs Voice Generator"
    description: str = "Generates voice from text using the Eleven Labs API."
    xi_api_key: str = Field(default=None)
    voice_id: str = Field(default="4dyF1bD2mjNHsB76Wf9q")
    text_file_path: str = Field(default="script.txt")
    output_path: str = Field(default_factory=lambda: "output_{}.mp3".format(datetime.now().strftime("%Y%m%d%H%M%S")))

    def __init__(self, text_file_path=None):
        super().__init__()
        load_dotenv()
        self.xi_api_key = os.getenv('XI_API_KEY')
        self.text_file_path = text_file_path if text_file_path else self.text_file_path

    def _run(self):
        if not self.text_file_path:
            return "No text file path provided."

        try:
            with open(self.text_file_path, 'r') as file:
                text_to_speak = file.read()
        except FileNotFoundError:
            return f"File not found: {self.text_file_path}"

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        headers = {"Accept": "application/json", "xi-api-key": self.xi_api_key}
        data = {"text": text_to_speak, "model_id": "eleven_multilingual_v2"}

        response = requests.post(tts_url, headers=headers, json=data, stream=True)
        if response.ok:
            with open(self.output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            return f"Audio stream saved successfully as {self.output_path}."
        else:
            return "Failed to generate speech: " + response.text