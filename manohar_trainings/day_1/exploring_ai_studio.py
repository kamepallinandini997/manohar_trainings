import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
load_dotenv()

# Get the key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Initialize client with API key
client = genai.Client(api_key=api_key)
'''
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few lines" 

)

# Disables thinking
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) 
    ),
)

'''

'''
sending output like a stream

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=["Explain how AI works"]
)
for chunk in response:
    print(chunk.text, end="")
    


# Define the desired output structure using Pydantic
class Recipe(BaseModel):
    recipe_name: str
    description: str
    ingredients: list[str]
    steps: list[str]

# Request the model to populate the schema
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Provide a classic recipe for chocolate chip cookies.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Recipe,
    ),
)

# The response.text will be a valid JSON string matching the Recipe schema
print(response.text) '''

from google import genai
from PIL import Image
from io import BytesIO

client = genai.Client()

result = client.models.generate_images(
    model='imagen-4.0-fast-generate-001',
    prompt="Image of a cat",
    config=dict(
        number_of_images=1, # 1 to 4 (always 1 for the ultra model)
        output_mime_type="image/jpeg",
        person_generation="ALLOW_ADULT" ,# 'ALLOW_ALL' (but not in Europe/Mena), 'DONT_ALLOW' or 'ALLOW_ADULT'
        aspect_ratio="1:1" # "1:1", "3:4", "4:3", "9:16", or "16:9"
        )
        )

for generated_image in result.generated_images:
   image = Image.open(BytesIO(generated_image.image.image_bytes))