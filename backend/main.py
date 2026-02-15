import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from schema_generator import generate_master_dataset

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    query: str

@app.post("/api/nl-query")
async def nl_query(request: QueryRequest):
    # Fetch real-time processed data to give the LLM
    current_trial_state = generate_master_dataset()
    
    system_prompt = f"""
    You are TrialPulse AI. Current Live Data: {current_trial_state}
    
    TASK:
    - Analyze the data above to answer user queries.
    - Identify risks: High 'overdue_items' or low 'dqi'.
    - If a site has more than 10 overdue items, flag it as a priority.
    - Be precise with patient counts and site IDs.
    - Keep answers under 50 words.
    """
    
    try:
        response = model.generate_content(f"{system_prompt}\nUser: {request.query}")
        return {"response": response.text}
    except Exception:
        return {"response": "I am analyzing the dataset. Please specify a site ID."}

@app.get("/api/sites")
def get_all_sites():
    return generate_master_dataset()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)