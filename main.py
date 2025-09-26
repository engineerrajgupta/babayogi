import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import the business logic
from logic import DietGenerationLogic


# Load environment variables from a .env file
load_dotenv()

# --- Server Startup Check ---
if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY not found in environment variables or .env file.")
if not os.getenv("PINECONE_API_KEY"):
    raise RuntimeError("PINECONE_API_KEY not found in environment variables or .env file.")

# --- Pydantic Models for Request Validation ---
class DoshaScores(BaseModel):
    vata: int = Field(..., example=7, description="Vata dosha score")
    pitta: int = Field(..., example=3, description="Pitta dosha score")
    kapha: int = Field(..., example=2, description="Kapha dosha score")

class Profile(BaseModel):
    prakriti: DoshaScores = Field(...)
    vikriti: DoshaScores = Field(...)

class Health(BaseModel):
    agni: str = Field(..., example="weak")
    ama: str = Field(..., example="moderate")

class DietPreferences(BaseModel):
    dietType: str = Field(..., example="vegetarian")
    allergies: List[str] = Field(default=[], example=["Dairy"])
    cuisine: List[str] = Field(..., example=["North Indian"])

class Environment(BaseModel):
    season: str = Field(..., example="winter")

class Goals(BaseModel):
    primaryGoal: str = Field(..., example="Improve digestion and reduce bloating")

class DietRequest(BaseModel):
    profile: Profile
    health: Health
    dietPreferences: DietPreferences
    environment: Environment
    goals: Goals

# --- FastAPI Application Setup ---
app = FastAPI(
    title="Aayur.AI - Personalized Wellness Guide",
    version="3.0.0"
)
origins = ["*"] # Be specific with your front-end domain in a real app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
diet_logic = DietGenerationLogic()

# --- Root and Favicon Endpoints ---
@app.get("/")
async def read_root():
    return {"message": "API is running. Use the /generate-diet-plan endpoint with a POST request."}

@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse("favicon.ico")

# --- Main API Endpoint ---
@app.post("/generate-diet-plan", tags=["Diet Generation"])
async def generate_diet_plan(request: DietRequest):
    try:
        user_payload = request.model_dump()
        diet_plan = diet_logic.get_diet_plan(user_payload)
        
        if "error" in diet_plan:
             raise HTTPException(status_code=422, detail=diet_plan)
        
        return diet_plan
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"An unexpected error occurred in the main endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )
