import streamlit as st
import requests
import json
from typing import Optional

# Configure page
st.set_page_config(
    page_title="LinkedIn Internship Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.2em;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .recommendation-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        background-color: #F5F5F5;
        margin-bottom: 15px;
    }
    .skill-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        background-color: #2E86AB;
        color: white;
        margin-right: 5px;
        margin-bottom: 5px;
        font-size: 0.85em;
    }
    .score-high {
        color: #27AE60;
        font-weight: bold;
    }
    .score-medium {
        color: #F39C12;
        font-weight: bold;
    }
    .score-low {
        color: #E74C3C;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">� AI Based Internship Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your resume and discover real-time LinkedIn internship opportunities</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload** your resume (PDF)
    2. **Enter** your details
    3. **Get** LinkedIn internship recommendations
    
    The AI will:
    - Extract your skills
    - Find matching LinkedIn internships
    - Provide direct apply links
    """)
    
    st.divider()
    st.info("💡 **Tip:** Ensure your resume includes your technical skills and experience for better recommendations.")

# Main content
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📄 Resume Upload")
    
    # Form for resume upload
    with st.form("resume_form"):
        student_name = st.text_input("Full Name", placeholder="John Doe")
        student_email = st.text_input("Email", placeholder="john@example.com")
        resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        
        submit_btn = st.form_submit_button("🚀 Analyze Resume", use_container_width=True)
    
    if submit_btn:
        if not student_name or not student_email:
            st.error("❌ Please fill in all fields")
        elif not resume_file:
            st.error("❌ Please upload a PDF resume")
        else:
            with st.spinner("⏳ Analyzing your resume..."):
                try:
                    # Prepare form data
                    files = {"resume": ("resume.pdf", resume_file, "application/pdf")}
                    data = {
                        "student_name": student_name,
                        "student_email": student_email
                    }
                    
                    # Call backend API
                    response = requests.post(
                        f"{BACKEND_URL}/upload-resume",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        student_id = result.get("student_id")
                        
                        # Store in session state
                        st.session_state.student_id = student_id
                        st.session_state.student_name = student_name
                        
                        st.success(f"✅ Resume uploaded successfully! (ID: {student_id})")
                        st.info(f"Hello **{student_name}**! Fetching your recommendations...")
                        
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Make sure the server is running on http://127.0.0.1:8000")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with col2:
    st.subheader("🎯 Your Recommendations")
    
    # Check if we have a student_id in session
    if "student_id" in st.session_state:
        student_id = st.session_state.student_id
        student_name = st.session_state.get("student_name", "")
        
        try:
            # Fetch recommendations from backend
            rec_response = requests.get(
                f"{BACKEND_URL}/recommend/{student_id}",
                timeout=30
            )
            
            if rec_response.status_code == 200:
                data = rec_response.json()
                
                # Display detected skills
                skills = data.get("skills", [])
                if skills:
                    st.markdown("### 🛠️ Detected Skills from Resume")
                    skills_html = ""
                    for skill in skills[:15]:
                        skills_html += f'<span class="skill-badge">{skill}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                    st.divider()
                
                # LinkedIn Internships
                internships = data.get("internships", [])
                total = data.get("total_count", 0)
                
                if internships:
                    st.markdown(f"### 💼 LinkedIn Internships ({total} Available)")
                    st.caption("Real-time opportunities from LinkedIn")
                    
                    for idx, internship in enumerate(internships, 1):
                        with st.container():
                            col_title, col_btn = st.columns([3, 1])
                            
                            with col_title:
                                st.markdown(f"**{idx}. {internship.get('title', 'Internship')}**")
                                st.caption(f"🏢 {internship.get('company', 'N/A')} • 📍 {internship.get('location', 'N/A')}")
                                
                                # Show skills
                                if internship.get("skills"):
                                    skills_str = ", ".join(internship["skills"][:4])
                                    st.caption(f"💡 Skills: {skills_str}")
                            
                            with col_btn:
                                if internship.get('url'):
                                    st.link_button(
                                        "Search LinkedIn",
                                        internship['url'],
                                        use_container_width=True
                                    )
                            
                            st.divider()
                else:
                    st.info("No LinkedIn internships available at the moment. Try again later.")
                
            elif rec_response.status_code == 404:
                st.warning("⏳ Student profile not found. Please upload your resume first.")
            else:
                st.error(f"❌ Error fetching recommendations: {rec_response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Make sure the server is running.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    else:
        st.info("📤 Upload your resume on the left to see personalized recommendations")

# AI Chatbot Section
st.divider()
st.header("💬 Career Advisor Chatbot")
st.caption("Ask anything about internships, careers, skills, or job search!")

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about careers, internships, or skills..."):
    # Add user message to chat
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": prompt,
                        "history": st.session_state.chat_messages[:-1]  # Exclude current message
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    bot_response = response.json()["response"]
                    st.markdown(bot_response)
                    
                    # Add bot response to chat history
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": bot_response
                    })
                else:
                    error_msg = "⚠️ Sorry, I couldn't process that. Please try again."
                    st.error(error_msg)
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    
            except requests.exceptions.ConnectionError:
                error_msg = "⚠️ Cannot connect to chatbot. Make sure the backend is running."
                st.error(error_msg)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Clear chat button
if st.session_state.chat_messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_messages = []
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; padding: 20px;'>
    <p><strong>LinkedIn Internship Finder</strong> - Find real-time LinkedIn opportunities | Powered by FastAPI & Gemini AI</p>
</div>
""", unsafe_allow_html=True)
