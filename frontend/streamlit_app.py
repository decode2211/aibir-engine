import streamlit as st
import requests
import json
from typing import Optional
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="🚀 AIBIR - AI Internship Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8001"

# ==================== FUTURISTIC AI-THEMED CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Main container - Dark futuristic theme */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
        font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(100, 200, 255, 0.5);
    }
    
    /* Glassmorphism Card with 3D effect */
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
    }
    
    .premium-card:hover {
        transform: translateY(-10px) rotateX(5deg);
        box-shadow: 0 20px 60px 0 rgba(100, 200, 255, 0.4);
        border: 1px solid rgba(100, 200, 255, 0.5);
    }
    
    /* Job Card - Futuristic 3D */
    .job-card {
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.1) 0%, rgba(150, 100, 255, 0.1) 100%);
        backdrop-filter: blur(10px);
        color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(100, 200, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
        position: relative;
        overflow: hidden;
    }
    
    .job-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .job-card:hover::before {
        left: 100%;
    }
    
    .job-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 48px rgba(100, 200, 255, 0.4);
        border: 1px solid rgba(100, 200, 255, 0.6);
    }
    
    /* Animated Header */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 50px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        animation: gradientShift 8s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-title {
        font-size: 3.2em;
        font-weight: 800;
        margin-bottom: 12px;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.8);
        letter-spacing: -1px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 30px rgba(100, 200, 255, 0.6); }
        to { text-shadow: 0 0 30px rgba(255, 255, 255, 1), 0 0 40px rgba(100, 200, 255, 0.9); }
    }
    
    .hero-subtitle {
        font-size: 1.3em;
        font-weight: 400;
        margin-bottom: 10px;
        opacity: 0.95;
    }
    
    .hero-tagline {
        font-size: 1em;
        opacity: 0.9;
        margin-top: 10px;
    }
    
    /* Tab styling - Futuristic */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 0, 0, 0.2);
        padding: 8px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        font-weight: 600;
        padding: 14px 22px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(100, 200, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.3), rgba(150, 100, 255, 0.3));
        color: white;
        border: 1px solid rgba(100, 200, 255, 0.5);
        box-shadow: 0 4px 20px rgba(100, 200, 255, 0.4);
    }
    
    /* Input styling - Glassmorphism */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 12px 16px;
        font-size: 1em;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border: 1px solid rgba(100, 200, 255, 0.6);
        box-shadow: 0 0 20px rgba(100, 200, 255, 0.3);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Buttons - 3D Animated */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 700;
        font-size: 1em;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Messages - Neon style */
    .stSuccess {
        background: rgba(39, 174, 96, 0.2);
        border: 1px solid rgba(39, 174, 96, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(39, 174, 96, 0.3);
    }
    
    .stError {
        background: rgba(231, 76, 60, 0.2);
        border: 1px solid rgba(231, 76, 60, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(231, 76, 60, 0.3);
    }
    
    .stWarning {
        background: rgba(243, 156, 18, 0.2);
        border: 1px solid rgba(243, 156, 18, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(243, 156, 18, 0.3);
    }
    
    .stInfo {
        background: rgba(52, 152, 219, 0.2);
        border: 1px solid rgba(52, 152, 219, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(52, 152, 219, 0.3);
    }
    
    /* Recommendation card - Holographic */
    .recommendation-card {
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.1) 0%, rgba(150, 100, 255, 0.1) 100%);
        border: 1px solid rgba(100, 200, 255, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.4s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .recommendation-card:hover {
        transform: scale(1.02);
        border-color: rgba(100, 200, 255, 0.6);
        box-shadow: 0 12px 40px rgba(100, 200, 255, 0.3);
    }
    
    /* Metric styling - 3D Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
        color: white;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform-style: preserve-3d;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) rotateY(5deg);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.6);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 800;
        margin-bottom: 8px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    }
    
    .metric-label {
        font-size: 1em;
        opacity: 0.95;
        font-weight: 600;
    }
    
    /* Footer - Futuristic */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 60px;
        padding: 40px 20px;
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(100, 200, 255, 0.3);
        backdrop-filter: blur(10px);
        font-size: 0.95em;
    }
    
    .footer-highlight {
        color: #64c8ff;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(100, 200, 255, 0.5);
    }
    
    p {
        font-size: 1em;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.85);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
</style>
""", unsafe_allow_html=True)

# ==================== HERO HEADER ====================
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🚀 AIBIR</div>
    <div class="hero-subtitle">AI-Based Internship Recommendation System</div>
    <div class="hero-tagline">Find Your Perfect Internship • Generate Applications • Get Hired</div>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if "student_id" not in st.session_state:
    st.session_state.student_id = "student_" + datetime.now().strftime("%Y%m%d%H%M%S")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

# Refresh button in sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if st.button("🔄 Refresh Cache", key="refresh_sidebar"):
        st.cache_data.clear()
        st.rerun()
    st.divider()

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Resume", 
    "💼 Jobs", 
    "🤖 Advisor", 
    "📊 Stats", 
    "✉️ Email", 
    "📝 Cover Letter"
])

# ==================== TAB 1: RESUME UPLOAD ====================
with tab1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### 📄 Upload Your Resume")
        st.write("Let us analyze your skills and find matching internships")
        
        with st.form("resume_form"):
            student_name = st.text_input("👤 Full Name", placeholder="John Doe")
            student_email = st.text_input("📧 Email", placeholder="john@example.com")
            student_phone = st.text_input("📱 Phone", placeholder="+91-1234567890")
            resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
            
            submitted = st.form_submit_button("🚀 Upload & Analyze", use_container_width=True)
            
            if submitted:
                if student_name and student_email and resume_file:
                    st.success("✅ Resume uploaded successfully!")
                    st.session_state.resume_uploaded = True
                else:
                    st.error("❌ Please fill all fields")
    
    with col2:
        st.markdown("### 💡 What We Do")
        st.markdown("""
        ✨ **AI-Powered Analysis**
        - Extract skills from your resume
        - Identify strengths and gaps
        - Recommend tailored opportunities
        
        🎯 **Smart Matching**
        - Match with 15+ live job listings
        - From top companies & startups
        - Updated in real-time
        
        📈 **Career Growth**
        - Get personalized recommendations
        - AI-powered cover letters
        - Custom cold emails to recruiters
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: JOB SCRAPER ====================
with tab2:
    st.markdown("### 💼 Live Internship Opportunities")
    
    # Check if resume is uploaded
    if not st.session_state.get("resume_uploaded"):
        st.warning("📄 Please upload your resume in the 'Resume' tab to see personalized job recommendations")
        st.info("✨ Upload your resume to unlock:\n- 15+ live internship opportunities\n- AI-matched recommendations\n- One-click applications")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("🔍 Search jobs", placeholder="Python, React, etc.")
        with col2:
            sort_by = st.selectbox("📊 Sort by", ["Recent", "Company", "Salary"])
        with col3:
            if st.button("🔄 Refresh Jobs", use_container_width=True):
                st.cache_data.clear()
        
        try:
            response = requests.get(f"{BACKEND_URL}/recommend/jobs/all")
            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                total_jobs = len(jobs)
                
                # Filter if search query
                if search_query:
                    jobs = [j for j in jobs if search_query.lower() in j.get("title", "").lower() or 
                           search_query.lower() in j.get("description", "").lower()]
                
                st.markdown(f"### 🎯 Found {len(jobs)} of {total_jobs} opportunities")
                
                for idx, job in enumerate(jobs, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="job-card">
                            <h3 style="margin-top:0; color: #ffffff;">{idx}. {job.get('title', 'N/A')}</h3>
                            <p style="color: #64c8ff; font-weight: 600; margin: 8px 0;">
                                {job.get('company', 'Unknown Company')} • {job.get('location', 'India')}
                            </p>
                            <p style="margin: 8px 0; color: rgba(255,255,255,0.85);">{job.get('description', '')[:150]}...</p>
                            <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
                                <span style="background: rgba(100, 200, 255, 0.2); color: #64c8ff; padding: 6px 14px; border-radius: 8px; font-size: 0.85em; border: 1px solid rgba(100, 200, 255, 0.3);">
                                    📍 {job.get('source', 'Web')}
                                </span>
                                <span style="font-weight: 700; font-size: 1.1em; color: #5ff5a0; text-shadow: 0 0 10px rgba(95, 245, 160, 0.5);">
                                    💰 {job.get('salary', 'Competitive')}
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("🔗 View", key=f"view_{idx}", use_container_width=True):
                            st.info(f"Opening: {job.get('link', '#')}")
                    with col2:
                        if st.button("💌 Email", key=f"email_{idx}", use_container_width=True):
                            st.success("✉️ Go to Email tab to generate")
                    with col3:
                        if st.button("📄 Cover Letter", key=f"cl_{idx}", use_container_width=True):
                            st.success("📝 Go to Cover Letter tab to generate")
                    
                    st.divider()
            else:
                st.error("Failed to fetch jobs")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ==================== TAB 3: CAREER ADVISOR ====================
with tab3:
    st.markdown("### 🤖 AI Career Advisor")
    st.write("Get personalized career advice powered by AI")
    
    advisor_prompt = st.text_area(
        "Ask your career question",
        placeholder="E.g., How can I improve my skills for internships? What should I focus on?",
        height=120
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Get Advice", key="advisor_btn", use_container_width=True):
            if advisor_prompt:
                try:
                    with st.spinner("🤔 Thinking..."):
                        response = requests.post(
                            f"{BACKEND_URL}/chat",
                            json={"message": advisor_prompt}
                        )
                        if response.status_code == 200:
                            advice = response.json().get("response", "")
                            st.success("✅ Advice generated!")
                            st.markdown(f"""
                            <div class="recommendation-card">
                            {advice}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question")

# ==================== TAB 4: STATISTICS ====================
with tab4:
    st.markdown("### 📊 Job Market Analytics")
    
    try:
        response = requests.get(f"{BACKEND_URL}/recommend/jobs/all")
        if response.status_code == 200:
            data = response.json()
            jobs_by_source = data.get("by_source", {})
            total_jobs = data.get("total_jobs", 0)
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_jobs}</div>
                    <div class="metric-label">Total Jobs</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(jobs_by_source)}</div>
                    <div class="metric-label">Active Sources</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_per_source = round(total_jobs / len(jobs_by_source)) if jobs_by_source else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_per_source}</div>
                    <div class="metric-label">Avg. Per Source</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">⚡</div>
                    <div class="metric-label">Live & Fresh</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Source breakdown
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🕷️ Jobs by Source")
                if jobs_by_source:
                    df = pd.DataFrame(list(jobs_by_source.items()), columns=["Source", "Count"])
                    st.bar_chart(df.set_index("Source"))
            
            with col2:
                st.markdown("### 📈 Source Details")
                for source, count in jobs_by_source.items():
                    st.markdown(f"**{source}**: {count} 📍")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ==================== TAB 5: COLD EMAIL GENERATOR ====================
with tab5:
    st.markdown("### ✉️ AI-Powered Cold Email Generator")
    st.write("Generate personalized emails to impress recruiters")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Email Details")
        email_job_title = st.text_input("Job Title", placeholder="Software Engineer Intern", key="email_job")
        email_company = st.text_input("Company Name", placeholder="Google", key="email_company")
        email_recruiter = st.text_input("Recruiter Name (Optional)", placeholder="Sarah Smith", key="email_recruiter")
        email_your_name = st.text_input("Your Name", placeholder="John Doe", key="email_name")
    
    with col2:
        st.markdown("#### 📝 Job Information")
        email_job_desc = st.text_area(
            "Job Description",
            placeholder="Paste job description here...",
            height=160,
            key="email_job_desc"
        )
    
    email_resume_text = st.text_area(
        "Your Skills & Experience",
        placeholder="Describe your background, skills, and experience...",
        height=120,
        key="email_resume"
    )
    
    if st.button("✨ Generate Cold Email", key="gen_email", use_container_width=True):
        if email_job_title and email_company and email_job_desc and email_resume_text:
            try:
                with st.spinner("🔨 Crafting your email..."):
                    response = requests.post(
                        f"{BACKEND_URL}/api/generate/email",
                        json={
                            "job_title": email_job_title,
                            "company_name": email_company,
                            "recruiter_name": email_recruiter or None,
                            "resume_text": email_resume_text,
                            "job_description": email_job_desc,
                            "user_name": email_your_name,
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()["data"]
                        
                        st.success("✅ Email generated successfully!")
                        
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, rgba(100, 200, 255, 0.3), rgba(150, 100, 255, 0.3)); backdrop-filter: blur(10px); color: white; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid rgba(100, 200, 255, 0.5); box-shadow: 0 8px 32px rgba(100, 200, 255, 0.3);">
                            <h3 style="color: white; margin: 0; font-size: 1.2em; text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);">📧 Email Subject</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(data["subject"], language="text")
                        
                        st.markdown("#### 📝 Email Body")
                        st.text_area(
                            "Email Content",
                            value=data["body"],
                            height=350,
                            disabled=True,
                            key="email_body"
                        )
                        
                        # Alternative subjects
                        st.markdown("#### 💡 Alternative Subject Lines")
                        try:
                            subjects_response = requests.get(
                                f"{BACKEND_URL}/api/generate/email-subjects",
                                params={
                                    "job_title": email_job_title,
                                    "company_name": email_company,
                                    "count": 3
                                }
                            )
                            if subjects_response.status_code == 200:
                                subjects = subjects_response.json()["data"]["subjects"]
                                for i, subject in enumerate(subjects, 1):
                                    st.markdown(f"**{i}.** {subject}")
                        except:
                            pass
                    else:
                        st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")

# ==================== TAB 6: COVER LETTER GENERATOR ====================
with tab6:
    st.markdown("### 📝 AI Cover Letter Generator")
    st.write("Create professional cover letters tailored to each job")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 👤 Your Information")
        cl_your_name = st.text_input("Full Name", placeholder="John Doe", key="cl_name")
        cl_email = st.text_input("Email Address", placeholder="john@example.com", key="cl_email")
        cl_phone = st.text_input("Phone Number", placeholder="+91-XXXX-XXXX-XX", key="cl_phone")
    
    with col2:
        st.markdown("#### 💼 Position Details")
        cl_job_title = st.text_input("Job Title", placeholder="Software Engineer Intern", key="cl_job")
        cl_company = st.text_input("Company Name", placeholder="Google", key="cl_company")
    
    cl_job_desc = st.text_area(
        "Job Description",
        placeholder="Paste job description here...",
        height=120,
        key="cl_job_desc"
    )
    
    cl_resume_text = st.text_area(
        "Your Background",
        placeholder="Describe your experience, skills, and achievements...",
        height=120,
        key="cl_resume"
    )
    
    if st.button("📄 Generate Cover Letter", key="gen_cl", use_container_width=True):
        if cl_job_title and cl_company and cl_job_desc and cl_resume_text:
            try:
                with st.spinner("📝 Writing your cover letter..."):
                    response = requests.post(
                        f"{BACKEND_URL}/api/generate/cover-letter",
                        json={
                            "job_title": cl_job_title,
                            "company_name": cl_company,
                            "resume_text": cl_resume_text,
                            "job_description": cl_job_desc,
                            "user_name": cl_your_name,
                            "user_email": cl_email,
                            "user_phone": cl_phone,
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()["data"]
                        
                        st.success("✅ Cover letter generated successfully!")
                        
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(100, 200, 255, 0.3), rgba(150, 100, 255, 0.3)); backdrop-filter: blur(10px); color: white; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid rgba(100, 200, 255, 0.5); box-shadow: 0 8px 32px rgba(100, 200, 255, 0.3);">
                            <h3 style="color: white; margin: 0; font-size: 1.2em; text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);">📋 Cover Letter ({data.get('word_count', 0)} words)</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.text_area(
                            "Cover Letter",
                            value=data["cover_letter"],
                            height=400,
                            disabled=True,
                            key="cover_letter_text"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"📊 Word count: {data.get('word_count', 0)} (Recommended: 250-400)")
                        with col2:
                            if data.get('word_count', 0) < 250:
                                st.warning("⚠️ Consider expanding your letter")
                            elif data.get('word_count', 0) > 400:
                                st.warning("⚠️ Consider shortening your letter")
                            else:
                                st.success("✅ Perfect length!")
                    else:
                        st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 24px;">
        <h3 style="color: #64c8ff; margin-bottom: 16px; text-shadow: 0 0 20px rgba(100, 200, 255, 0.5);">🚀 AI-Powered Job Discovery</h3>
        <p style="color: rgba(255, 255, 255, 0.8);">✨ Real-time scraping • 🤖 AI recommendations • 📧 Smart applications</p>
    </div>
    <hr style="border: 1px solid rgba(100, 200, 255, 0.2); margin: 24px 0;">
    <div>
        <p style="margin-bottom: 8px; font-weight: 600;">
            <span class="footer-highlight">AIBIR</span> - AI Based Internship Finder
        </p>
        <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9em;">
            Powered by SerpAPI • FastAPI • Streamlit • ML
        </p>
        <p style="color: rgba(255, 255, 255, 0.4); font-size: 0.85em; margin-top: 12px;">
            © 2026 AIBIR. All rights reserved.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
