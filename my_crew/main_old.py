import os
from dotenv import load_dotenv
from crewai import Crew
from config.settings import agents, tasks
from my_crew.tools.google_search_tool import GoogleSearchTool

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')

# Initialize the Google Search Tool with API credentials
google_search = GoogleSearchTool(api_key=GOOGLE_API_KEY, cx=GOOGLE_CX)

# Example setup for the crew
my_crew = Crew(agents=agents, tasks=tasks)

# Prompt the user to enter a topic
user_topic = input("Please enter the topic you want to research: ")

# Kickoff the crew with the user-provided topic
# Kickoff the crew with a specific query
results = my_crew.kickoff(inputs={'query': 'latest AI news'})
print(results)
