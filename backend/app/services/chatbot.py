"""
Real-time AI chatbot for student career guidance
Uses Google Gemini API for intelligent responses
"""

import google.generativeai as genai
from app.config import GEMINI_API_KEY

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_chatbot_response(user_message: str, chat_history: list = None) -> str:
    """
    Get real-time AI response for student queries
    
    Args:
        user_message: The student's question
        chat_history: Previous conversation context
        
    Returns:
        AI-generated response
    """
    
    if not GEMINI_API_KEY:
        return "⚠️ Chatbot is not configured. Please add GEMINI_API_KEY to backend/.env file."
    
    try:
        # System prompt for career guidance context
        system_context = """You are an expert career counselor and internship advisor for students in India. 
Your role is to:
- Help students with career guidance and internship questions
- Provide advice on resume building, skill development, and job searching
- Answer questions about different tech roles, companies, and career paths
- Give practical, actionable advice for students starting their careers
- Be encouraging, supportive, and professional

Keep responses concise (2-4 paragraphs max) but helpful. Use emojis sparingly for a friendly tone."""

        # Initialize model
        model = genai.GenerativeModel('gemini-pro')
        
        # Build conversation context
        conversation = []
        if chat_history:
            for msg in chat_history[-5:]:  # Keep last 5 messages for context
                conversation.append(msg)
        
        # Create full prompt
        full_prompt = f"{system_context}\n\nStudent Question: {user_message}\n\nYour Response:"
        
        # Get response
        response = model.generate_content(full_prompt)
        
        return response.text
        
    except Exception as e:
        print(f"Chatbot error: {e}")
        return f"⚠️ Sorry, I encountered an error. Please try again or rephrase your question."
