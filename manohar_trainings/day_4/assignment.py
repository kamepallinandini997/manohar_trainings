from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv 
from google import genai
from google.genai import types
import pathlib

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
app = FastAPI()
client = genai.Client()


class TextRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str


zero_shot_prompt ="""Summarize this text in plain few words :"""

few_shot_prompt = """
You are a professional summarizer. Below are examples:

Example 1:
Text: "The economy grew by 3% last quarter due to increased consumer spending."
Summary: "The economy grew 3% last quarter because of more consumer spending."

Example 2:
Text: "Scientists have developed a new AI system that predicts diseases before symptoms appear."
Summary: "AI can now predict diseases early, before symptoms show."

Now, summarize the following text in a similar concise and clear way:
"""

chain_of_thought_prompt = """
Let's think step-by-step to summarize the text effectively.
1. Identify the key ideas.
2. Ignore details or examples that don’t add meaning.
3. Condense the message into a clear summary.

Now, apply this reasoning to the following text:
"""

role_based_prompt = """
You are an Ai expert . Summarize the following text as a AI specialist, focusing on insights most relevant to that field. 
Use tone, vocabulary, and clarity appropriate for that professional audience.
Text:
"""

@app.post("/v1/summarize", response_model=SummaryResponse)
async def summarize(request: TextRequest):
   
    try:
        model_name = "gemini-2.5-flash"
        response = client.models.generate_content(
            model = model_name,
            contents =f"{chain_of_thought_prompt}{request.text}")
        return SummaryResponse(summary=response.text)
    except Exception as e:
        return SummaryResponse(summary=f"Error: {str(e)}")

@app.post("/v1/summarize-pdf", response_model=SummaryResponse)
async def summarize_pdf():
    try:
        filepath = pathlib.Path('NIPS-2017-attention-is-all-you-need-Paper.pdf')
        prompt = "Summarize this document into few lines:"
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type='application/pdf',
            ),
            prompt])
        return SummaryResponse(summary=response.text)
    except Exception as e:
        return SummaryResponse(summary=f"Error: {str(e)}")
