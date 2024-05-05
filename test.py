from openai import OpenAI
import os

# Set the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Using the new client to create a chat completion
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": "what color is the sky?"}])

# Printing the content of the response
print(response.choices[0].message.content)
