import os
import httpx
from groq import AsyncGroq
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Chatbot Backend")

# CORS Setup - Allow frontend to communicate with backend
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",  # React default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allowing all for easier local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_API_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Initialize Groq Client
# It handles its own session and base URL
groq_client = AsyncGroq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Request Model
class ChatRequest(BaseModel):
    message: str
    model: str = "llama3-8b-8192" # Default to Groq Llama 3
    use_openai: bool = False

@app.get("/")
async def root():
    return {"message": "AI Chatbot Backend is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify backend status"""
    return {"status": "ok", "service": "AI Chatbot Backend"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint.
    By default connects to local Ollama instance.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Optional OpenAI Fallback (Retained for legacy structure)
    if request.use_openai:
        return {"response": "OpenAI mode selected but not fully configured in this demo. Please use Groq or Ollama."}
    
    # Live Groq API Integration
    if groq_client and "llama" in request.model.lower() or "mixtral" in request.model.lower():
        try:
            chat_completion = await groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ],
                model=request.model,
            )
            return {"response": chat_completion.choices[0].message.content}
        except Exception as e:
            print(f"Groq API Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")

    # Local Ollama Fallback (if Groq key missing or standard ollama model requested)
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": request.model,
                "messages": [{"role": "user", "content": request.message}],
                "stream": False
            }
            
            response = await client.post(f"{OLLAMA_API_URL}/api/chat", json=payload, timeout=60.0)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Ollama Error: {response.text}")
            
            data = response.json()
            return {"response": data.get("message", {}).get("content", "")}

    except httpx.RequestError:
        raise HTTPException(status_code=503, detail=f"Unable to connect to model API. Check Groq Keys or ensure Ollama is running.")
    except Exception as e:
        print(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the server with reload enabled for development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
