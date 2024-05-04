from crewai import Task, Crew, Process
from agents import asset_organizer, voice_generator
import logging
import os

print("Current working directory:", os.getcwd())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Task 1: Asset Folder Generation
task_asset_folder_generation = Task(
    description="1. read the content of the script txt file provided. 2. Create a folder/directory that is named based on the script contents. Keep the name short and concise. 3. save the script inside the folder you created. Do not proceed to the next task until you verify that the folder has been created and the script has been stored. share the new relative path to the script stored.",
    expected_output="Relative Path to the folder containing the script and assets.",
    agent=asset_organizer,
    async_execution=False,
    inputs={'script_path': None}  # Placeholder for dynamic input
)

# # Task 3: Voice Generation
# task_voice_generation = Task(
#     description="Generate an MP3 voiceover from the text script using the ElevenLabs API.",
#     expected_output="MP3 file path within the asset folder.",
#     agent=voice_generator,
#     async_execution=False,
#     inputs={'script': task_asset_folder_generation.output}
# )

# Forming the Crew
vid_maker_crew = Crew(
    agents=[asset_organizer, voice_generator],
    tasks=[
        task_asset_folder_generation,
        #task_voice_generation
    ],
    max_rpm=27,
    process=Process.sequential  # Sequential execution ensures each task is completed before the next starts
)

def kickoff(script_path):
    # Check if the script file exists
    if not os.path.exists(script_path):
        logger.error("The script file does not exist at the provided path: %s", script_path)
        return

    try:
        # Pass the script path directly to the kickoff method
        result = vid_maker_crew.kickoff(inputs={'script_path': script_path})
        print("Vid_Maker Output:", result)
        print(vid_maker_crew.usage_metrics)
        logger.info("Video maker crew process executed successfully.")
    except Exception as e:
        logger.exception("Failed to execute video maker crew process: %s", e)

# Example usage
if __name__ == "__main__":
    user_script_path = input("Please enter the path to the script txt file: ")
    kickoff(user_script_path)
