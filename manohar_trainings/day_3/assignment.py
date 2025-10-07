from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import google.generativeai as genai  
from dotenv import load_dotenv 

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
app = FastAPI()


class TextRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str

class EntitiesResponse(BaseModel):
    entities: List[str]


@app.post("/v1/summarize", response_model=SummaryResponse)
async def summarize_text(request: TextRequest):
   
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"Summarize this text:\n{request.text}")
        return SummaryResponse(summary=response.text)
    except Exception as e:
        return SummaryResponse(summary=f"Error: {str(e)}")


@app.post("/v1/extract/entities", response_model=EntitiesResponse)
async def extract_entities(request: TextRequest):
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Extract named entities (medicine, disease, organization, date, product, etc.) "
            f"from this text. Return them as a comma-separated list:\n{request.text}"
        )

        entities_list = [ent.strip() for ent in response.text.split(",") if ent.strip()]
        return EntitiesResponse(entities=entities_list)
    except Exception as e:
        return EntitiesResponse(entities=[f"Error: {str(e)}"])
