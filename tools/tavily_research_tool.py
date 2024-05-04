from crewai_tools import BaseTool
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

class TavilyTool(BaseTool):
    name: str = "Tavily Web Research Tool"
    description: str = "Tool to perform advanced web research using the Tavily API."
    api_key: str = Field(default_factory=lambda: os.getenv('TAVILY_API_KEY'))
    base_url: str = "https://api.tavily.com"

    def _run(self, query: str) -> str:
        # Including API key in the request body if required by the API
        payload = {
            'query': query,
            'api_key': self.api_key  # Ensure this aligns with API's expected parameter for API key
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.base_url}/search", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"

# Example of initializing and using the Tavily tool
tavily_tool = TavilyTool()
