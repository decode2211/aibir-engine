"""
Real-time AI chatbot for student career guidance
Uses Groq API for fast, intelligent responses
"""

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = None
if GROQ_AVAILABLE and GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"Warning: Could not configure Groq: {e}")
        GROQ_AVAILABLE = False

def get_chatbot_response(user_message: str, chat_history: list = None) -> str:
    """
    Get real-time AI response for student queries using Groq
    
    Args:
        user_message: The student's question
        chat_history: Previous conversation context
        
    Returns:
        AI-generated response
    """
    
    if not GROQ_AVAILABLE:
        return "⚠️ Chatbot library not available. Please install: pip install groq"
    
    if not groq_client:
        return "⚠️ Chatbot is not configured. Please add GROQ_API_KEY to backend/.env file."
    
    try:
        # System prompt for career guidance context
        system_message = """You are an expert career counselor and internship advisor for students in India. 
Your role is to:
- Help students with career guidance and internship questions
- Provide advice on resume building, skill development, and job searching
- Answer questions about different tech roles, companies, and career paths
- Give practical, actionable advice for students starting their careers
- Be encouraging, supportive, and professional

Keep responses concise (2-4 paragraphs max) but helpful. Use emojis sparingly for a friendly tone."""

        # Build conversation messages for Groq API
        messages = [{"role": "system", "content": system_message}]
        
        # Add chat history (last 5 messages for context)
        if chat_history:
            for msg in chat_history[-5:]:
                messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Get response from Groq (using llama-3.3-70b-versatile - best free model)
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",  # Fast, smart, and free!
            temperature=0.7,
            max_tokens=500,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        if not response_text:
            return "⚠️ I couldn't generate a response. Please try rephrasing your question."
        
        return response_text
        
    except Exception as e:
        error_msg = str(e)
        print(f"Chatbot error: {error_msg}")
        
        # Handle specific errors
        if "api" in error_msg.lower() and "key" in error_msg.lower():
            return "⚠️ API key issue. Please check your GROQ_API_KEY in backend/.env"
        elif "rate" in error_msg.lower() or "limit" in error_msg.lower():
            return "⚠️ Rate limit reached. Please try again in a moment."
        elif "quota" in error_msg.lower():
            return "⚠️ API quota exceeded. Please try again later."
        elif "blocked" in error_msg.lower():
            return "⚠️ Content was blocked by safety filters. Please rephrase your question."
        else:
            return "⚠️ Sorry, I encountered an error. Please try again."
