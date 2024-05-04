# agents.py
import os 
from crewai import Agent
from crewai_tools import FileReadTool, DirectoryReadTool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from tools.tavily_research_tool import TavilyTool
from tools.google_search_tool import GoogleSearchTool
from tools.eleven_labs_tool import ElevenLabsTool


# Initialize tools
file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool()
tavily_tool = TavilyTool()
google_search_tool = GoogleSearchTool ()
eleven_labs_tool = ElevenLabsTool()

# Setup LLM with Groq
llm_groq = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192",
    temperature=0.1,
    max_tokens=8000
)

llm_groq2 = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY2"),
    model="mixtral-8x7b-32768",
    temperature=0.1,
    max_tokens=30000
)

llm_groq3 = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY3"),
    model="mixtral-8x7b-32768",
    temperature=0.1,
    max_tokens=30000
)

llm_openrouter1 = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.1,
    max_tokens=8000
)

llm_openrouter2 = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="meta-llama/llama-3-70b-instruct",
    temperature=0.2,
    max_tokens=8000
)

llm_openrouter3 = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="mistralai/mixtral-8x7b-instruct",
    temperature=0.1,
    max_tokens=32000
)

llm_openrouter4 = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="anthropic/claude-3-opus",
    temperature=0.1,
    max_tokens=200000
)

# Define Planner Agent
planner = Agent(
    role='Research Coordinator',
    goal='Devise comprehensive research questions based on initial topic and initial web search.',
    backstory='A veteran academician known for meticulous research methodologies, able to intuit the best questions for research that will lead to an information-rich answer.',
    tools=[tavily_tool, google_search_tool],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15, 
    allow_delegation=False, 
    llm=llm_groq2
    # llm_config={
    #     'model': 'llama3-70b-8192',
    #     'temperature': 0.1,
    #     'max_tokens': 8000
    # }
)

# Define Initial Researcher Agent
initial_researcher = Agent(
    role='Research Analyst',
    goal='Perform initial data collection and analysis, careful to gather only the most relevant information.',
    backstory='Skilled in rapid data gathering and analysis, often laying the groundwork for breakthrough insights.',
    tools=[tavily_tool],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15, 
    allow_delegation=False,  # Can delegate specific data retrieval tasks
    llm=llm_openrouter1
    # llm_config={
    #     'model': 'llama3-70b-8192',
    #     'temperature': 0.1,
    #     'max_tokens': 8000
    # }
)

# Define Sub-topic Generator Agent
sub_topic_generator = Agent(
    role='Topic Specialist',
    goal='Identify and delineate specific sub-topics from initial research findings to enable focused in-depth studies. These are critical as they will be the basis for the main topics of the report.',
    backstory='An expert in pattern recognition and thematic analysis, pivotal in drilling down complex data into actionable insights.',
    tools=[tavily_tool, google_search_tool],
    verbose=True,
    memory=True,
    max_rpm=20,
    max_iter=15, 
    allow_delegation=False,  # Can delegate the task of exploring specific sub-topics
    llm=llm_groq3
    # llm_config={
    #     'model': 'llama3-70b-8192',
    #     'temperature': 0.1,
    #     'max_tokens': 8000
    # }
)

# Define Detailed Researcher Agent
detailed_researcher = Agent(
    role='Deep Dive Analyst',
    goal='Conduct detailed research on identified sub-topics, employing advanced analytical methods to uncover nuanced information, revealing in-depth insights and avoiding reporting on generic or vague topics.',
    backstory='Renowned for their depth of knowledge and ability to uncover hidden layers within complex subjects.',
    tools=[tavily_tool, google_search_tool],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15, 
    allow_delegation=False,  # Performs in-depth analysis personally
    llm=llm_openrouter1
    # llm_config={
    #     'model': 'llama3-70b-8192',
    #     'temperature': 0.1,
    #     'max_tokens': 8000
    # }
)

# Define Aggregator Agent
aggregator = Agent(
    role='Senior Researcher and Expert Report Writer',
    goal='Synthesize all research findings into a cohesive, comprehensive, and exhaustive final report, ensuring clarity and actionable insights.',
    backstory='A seasoned synthesizer of information, known for transforming extensive research data into digestible, impactful reports.',
    tools=[],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15, 
    allow_delegation=False,  # Directly handles the compilation of the report
    llm=llm_openrouter2
    # llm_config={
    #     'model': 'llama3-70b-8192',
    #     'temperature': 0.1,
    #     'max_tokens': 8000
    # }
)

# Define script intake Agent
script_intake = Agent(
    role='In charge of obtaining txt script for audio and video generation',
    goal='Get, store and make available the txt file of the script for other agents to use',
    backstory='A master at file retrieval and storage',
    tools=[],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15, 
    allow_delegation=False,  # Directly handles the compilation of the report
    llm=llm_openrouter4
)
# Define asset organizer Agent
asset_organizer = Agent(
    role='Organize the assets for the video and make sure other agents are aware of the location of the assets.  You are master python programmer and use code to organize assets',
    goal='read the script contents and then create folder based on script contents and store the script in the folder. place all other assets generated in same folder',
    backstory='With a proven track record in digital asset management and organizational systems, this agent excels at structuring complex datasets and ensuring all team members have seamless access to necessary resources. You do this by using python code to manipulate files on local computer. Known for its meticulous attention to detail and robust methodological approach, it ensures that every asset is correctly categorized and readily accessible.',
    tools=[file_read_tool],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15, 
    allow_delegation=False, 
    llm=llm_openrouter4
)

# Define voice generator Agent
voice_generator = Agent(
    role='Voice Generator',
    goal='Generate an MP3 file from a text script using ElevenLabs API.',
    backstory='Expert in text-to-speech conversion and API interactions.',
    tools=[eleven_labs_tool],
    verbose=True,
    memory=True,
    max_rpm=28,
    max_iter=15,
    allow_delegation=False,
    llm=llm_openrouter3
)

# Export agents
__all__ = ['planner', 'initial_researcher', 'sub_topic_generator', 'detailed_researcher', 'aggregator', 'script_intake', 'asset_organizer', 'voice_generator']
