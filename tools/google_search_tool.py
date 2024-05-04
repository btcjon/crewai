from crewai_tools import BaseTool
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

class GoogleSearchTool(BaseTool):
    name: str = "Google Search Tool"
    description: str = "Performs web searches using Google's Custom Search JSON API."
    api_key: str = Field(default_factory=lambda: os.getenv('GOOGLE_API_KEY'))
    cx: str = Field(default_factory=lambda: os.getenv('GOOGLE_CX'))

    def _run(self, query: str) -> str:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query
        }
        response = requests.get(url, params=params)
        results = response.json()

        search_items = results.get('items', [])
        output = []
        for item in search_items:
            title = item.get('title')
            link = item.get('link')
            snippet = item.get('snippet')
            output.append(f"{title}\n{link}\n{snippet}\n")

        return "\n".join(output)
