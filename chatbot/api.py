from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chatbot import chat_with_ai

app = FastAPI(title="Chatbot API", version="1.0.0")

# Allow local React dev servers (Vite, CRA, Next) and same-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {
        "name": "Chatbot API",
        "status": "ok",
        "endpoints": {
            "health": "GET /health",
            "chat": "POST /chat",
            "docs": "GET /docs",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    try:
        reply = chat_with_ai(message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return ChatResponse(reply=str(reply))
