from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from langchain_community.chat_models import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from .config import settings
from .database import get_db, init_db, ChatMessage
from .models import Message, ChatRequest, MessageCreate

app = FastAPI(title=settings.APP_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
@app.on_event("startup")
def on_startup():
    init_db()

# Initialize Ollama
chat_model = ChatOllama(
    base_url=settings.OLLAMA_BASE_URL, 
    model=settings.OLLAMA_MODEL,
    callbacks=[StreamingStdOutCallbackHandler()]
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Local AI Chatbot Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/history", response_model=List[Message])
def get_history(db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).order_by(ChatMessage.timestamp).all()
    return messages

@app.post("/chat", response_model=Message)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user_message_content = request.message
    
    # Save user message to DB
    user_msg = ChatMessage(role="user", content=user_message_content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # Construct conversation history for context
    # Fetch recent history (e.g., last 10 messages) to keep context manageable
    recent_messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).limit(10).all()
    recent_messages.reverse() # Order by timestamp asc

    langchain_messages = []
    # Add a system message if needed, or just start with history
    langchain_messages.append(SystemMessage(content="You are a helpful AI assistant running locally."))
    
    for msg in recent_messages:
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        else:
            langchain_messages.append(AIMessage(content=msg.content))
    
    # Send to LLM
    try:
        response = chat_model.invoke(langchain_messages)
        response_content = response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LLM: {str(e)}")

    # Save assistant message to DB
    assistant_msg = ChatMessage(role="assistant", content=response_content)
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return assistant_msg
