# Aayur.AI - Your Personalized Ayurvedic Wellness Guide

Aayur.AI is an intelligent API that generates comprehensive, personalized Ayurvedic wellness plans. It leverages a modern AI architecture known as Retrieval-Augmented Generation (RAG) to provide advice that is both deeply personalized and grounded in a curated knowledge base.



## ✨ Features

-   **Deep Personalization**: Generates plans based on individual Dosha scores (Prakriti & Vikriti), health goals, allergies, and cuisine preferences (Satmaya).
-   **RAG Architecture**: Uses Pinecone for intelligent, semantic retrieval of suitable foods and Google's Gemini Pro for generating coherent, expert-level wellness plans.
-   **Robust & Scalable**: Built with FastAPI for high performance and validated with Pydantic for data integrity.
-   **Cloud-Native**: Ready for deployment on modern serverless platforms like Vercel.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI
-   **AI Generation**: Google Gemini Pro
-   **Vector Database**: Pinecone
-   **Semantic Search**: `sentence-transformers`
-   **API Validation**: Pydantic
-   **Server**: Uvicorn

## 🏛️ Architecture

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1.  **User Request**: The API receives a detailed user profile via a `POST` request.
2.  **Semantic Query Generation**: The user's profile is transformed into a rich, contextual query (e.g., "A cooling, gluten-free South Indian food to pacify a Pitta imbalance...").
3.  **Intelligent Retrieval**: This query is converted into a 384-dimension vector embedding. Pinecone is then queried to find the most semantically similar food items from our curated database, applying metadata filters for allergies.
4.  **Prompt Augmentation**: The user's profile and the retrieved list of suitable foods are compiled into a detailed, structured prompt.
5.  **Expert Generation**: The augmented prompt is sent to the Gemini Pro model, which generates the final, structured JSON wellness plan.
6.  **API Response**: The generated JSON is sent back to the client.

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   A Google Gemini API Key
-   A Pinecone API Key and a pre-populated Pinecone index

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Create an Environment File

Create a file named `.env` in the root of the project and add your API keys:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
PINECONE_API_KEY="YOUR_PINECONE_API_KEY_HERE"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server Locally

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and the interactive documentation can be accessed at `http://127.0.0.1:8000/docs`.

## ⚙️ API Endpoint

### Generate Wellness Plan

-   **URL**: `/generate-diet-plan`
-   **Method**: `POST`
-   **Body**: A JSON object matching the Pydantic models in `main.py`.

#### Sample Payload:

```json
{
  "profile": {
    "prakriti": { "vata": 4, "pitta": 7, "kapha": 6 },
    "vikriti": { "vata": 8, "pitta": 4, "kapha": 3 }
  },
  "health": {
    "agni": "weak",
    "ama": "moderate"
  },
  "dietPreferences": {
    "dietType": "vegetarian",
    "allergies": [],
    "cuisine": ["North Indian"]
  },
  "environment": {
    "season": "winter"
  },
  "goals": {
    "primaryGoal": "Improve energy levels and reduce anxiety"
  }
}
```
