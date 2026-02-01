from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.chatbot import get_chatbot_response

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    success: bool

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Real-time AI chatbot endpoint for student queries
    """
    try:
        # Convert history to format expected by chatbot
        chat_history = [
            {"role": msg.role, "content": msg.content} 
            for msg in request.history
        ]
        
        # Get AI response
        response_text = get_chatbot_response(
            user_message=request.message,
            chat_history=chat_history
        )
        
        return ChatResponse(
            response=response_text,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
