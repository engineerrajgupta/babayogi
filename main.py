import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

# Import the business logic
from logic import DietGenerationLogic

# Load environment variables from a .env file
load_dotenv()

# --- Server Startup Check ---
# Ensure the necessary API keys are available before starting.
if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY not found in environment variables or .env file.")
if not os.getenv("PINECONE_API_KEY"):
    raise RuntimeError("PINECONE_API_KEY not found in environment variables or .env file.")


# --- Pydantic Models for Request Validation ---

class DoshaScores(BaseModel):
    vata: int = Field(..., example=7, description="Vata dosha score, typically 1-10")
    pitta: int = Field(..., example=3, description="Pitta dosha score, typically 1-10")
    kapha: int = Field(..., example=2, description="Kapha dosha score, typically 1-10")

class Profile(BaseModel):
    prakriti: DoshaScores = Field(..., description="The user's core, unchanging constitution")
    vikriti: DoshaScores = Field(..., description="The user's current state of imbalance")

class Health(BaseModel):
    agni: str = Field(..., example="weak", description="Digestive fire strength (e.g., 'strong', 'weak', 'variable')")
    ama: str = Field(..., example="moderate", description="Level of toxins in the body (e.g., 'low', 'moderate')")

class DietPreferences(BaseModel):
    dietType: str = Field(..., example="vegetarian", description="User's dietary choice (e.g., 'vegetarian', 'vegan')")
    allergies: List[str] = Field(default=[], example=["Dairy", "Gluten"], description="List of known allergens")
    # --- UPDATED: Added cuisine for Satmaya ---
    cuisine: List[str] = Field(..., example=["North Indian", "South Indian"], description="List of cuisines the user is accustomed to (Satmaya)")

class Environment(BaseModel):
    season: str = Field(..., example="winter", description="Current season (e.g., 'winter', 'summer', 'autumn')")

class Goals(BaseModel):
    primaryGoal: str = Field(..., example="Improve digestion and reduce bloating", description="The user's main health objective")

class DietRequest(BaseModel):
    """The main request body model that nests all other models."""
    profile: Profile
    health: Health
    dietPreferences: DietPreferences
    environment: Environment
    goals: Goals

# --- FastAPI Application Setup ---

app = FastAPI(
    title="Aayur.AI - Personalized Wellness Guide",
    description="An AI-powered API that generates a personalized Ayurvedic diet plan using a RAG pipeline with Pinecone and Gemini.",
    version="3.0.0"
)

# Create a single, reusable instance of our logic class.
# This will initialize models and connect to Pinecone on startup.
diet_logic = DietGenerationLogic()

@app.post("/generate-diet-plan", tags=["Diet Generation"])
async def generate_diet_plan(request: DietRequest):
    """
    Accepts a user's detailed profile and returns a personalized wellness guide.
    """
    try:
        user_payload = request.model_dump()
        diet_plan = diet_logic.get_diet_plan(user_payload)
        
        if "error" in diet_plan:
             raise HTTPException(status_code=422, detail=diet_plan)
        
        return diet_plan
        
    except HTTPException as http_exc:
        # Re-raise HTTPException to ensure FastAPI handles it correctly
        raise http_exc
    except Exception as e:
        # Generic error handler for any unexpected issues
        print(f"An unexpected error occurred in the main endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )
# To run this server:
# 1. Create a .env file and add your GEMINI_API_KEY.
# 2. Open your terminal in the same directory.
# 3. Run: pip install -r requirements.txt
# 4. Run: uvicorn main:app --reload
# 5. Access the interactive API docs at http://127.0.0.1:8000/docs
