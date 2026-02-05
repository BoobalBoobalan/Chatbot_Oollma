import os
import httpx
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Request Model
class ChatRequest(BaseModel):
    message: str
    model: str = "tinyllama" # Default model, can be switched to 'mistral' or others
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

    # Optional OpenAI Fallback
    if request.use_openai:
        if not OPENAI_API_KEY:
             raise HTTPException(status_code=500, detail="OpenAI API Key not configured")
        # Note: robust OpenAI implementation omitted to focus on Ollama, 
        # but this is where you would allow switching logic.
        return {"response": "OpenAI mode selected but not fully configured in this demo. Please use Ollama."}
    
    # Ollama Integration
    try:
        async with httpx.AsyncClient() as client:
            # We use the /api/chat endpoint from Ollama
            # Docs: https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion
            payload = {
                "model": request.model,
                "messages": [{"role": "user", "content": request.message}],
                "stream": False
            }
            
            # Timeout set to 60s as LLMs can be slow
            response = await client.post(f"{OLLAMA_API_URL}/api/chat", json=payload, timeout=60.0)
            
            if response.status_code != 200:
                error_detail = response.text
                print(f"Ollama Error: {error_detail}")
                raise HTTPException(status_code=response.status_code, detail=f"Ollama Error: {error_detail}")
            
            data = response.json()
            # Extract the actual response content
            ai_message = data.get("message", {}).get("content", "")
            
            return {"response": ai_message}

    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Unable to connect to Ollama at {OLLAMA_API_URL}. Is it running? (Run 'ollama serve')")
    except Exception as e:
        print(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the server with reload enabled for development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
