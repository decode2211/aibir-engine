# 🚀 AIBIR Engine - Deployment Guide

## Quick Deploy Options

### Option 1: Render.com (Recommended - FREE Tier)

1. **Fork/Push to GitHub** ✅ (Already Done!)
   - Repository: `https://github.com/decode2211/aibir-engine`

2. **Deploy Backend**
   - Go to [render.com](https://render.com) → Sign up/Login
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - Name: `aibir-backend`
     - Root Directory: `backend`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - Environment Variables:
       - `GROQ_API_KEY` = your_groq_api_key
       - `SERP_API_KEY` = your_serp_api_key
   - Click "Create Web Service"
   - Copy the URL (e.g., `https://aibir-backend.onrender.com`)

3. **Deploy Frontend**
   - Click "New +" → "Web Service" again
   - Connect same repo
   - Settings:
     - Name: `aibir-frontend`
     - Root Directory: `frontend`
     - Build Command: `pip install -r requirements-streamlit.txt`
     - Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
     - Environment Variables:
       - `BACKEND_URL` = `https://aibir-backend.onrender.com` (from step 2)
   - Click "Create Web Service"

4. **Access Your App**
   - Frontend URL: `https://aibir-frontend.onrender.com`

---

### Option 2: Railway.app (FREE $5 Credit)

1. **Deploy Backend**
   - Go to [railway.app](https://railway.app) → Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `aibir-engine` repo
   - Settings:
     - Root Directory: `backend`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - Add Variables:
       - `GROQ_API_KEY`
       - `SERP_API_KEY`
   - Generate Domain → Copy URL

2. **Deploy Frontend**
   - Add new service from same repo
   - Settings:
     - Root Directory: `frontend`
     - Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
     - Add Variable:
       - `BACKEND_URL` = backend_url_from_step_1
   - Generate Domain

---

### Option 3: Streamlit Cloud (Frontend Only - FREE)

1. **Deploy Frontend**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub
   - Select repo: `aibir-engine`
   - Main file path: `frontend/streamlit_app.py`
   - Advanced settings:
     - Python version: 3.11
     - Add secrets:
       ```toml
       BACKEND_URL = "your_deployed_backend_url"
       ```

2. **Deploy Backend Separately** (Use Render or Railway for backend)

---

### Option 4: Docker Deployment (VPS/Cloud)

```bash
# 1. Clone repo
git clone https://github.com/decode2211/aibir-engine
cd aibir-engine

# 2. Create .env file
echo "GROQ_API_KEY=your_key" > backend/.env
echo "SERP_API_KEY=your_key" >> backend/.env

# 3. Run with Docker Compose
docker-compose up -d

# Access:
# Backend: http://your-server:8001
# Frontend: http://your-server:8507
```

---

### Option 5: Vercel (Frontend) + Render (Backend)

1. **Deploy Backend on Render** (See Option 1)

2. **Deploy Frontend on Vercel**
   - Install Vercel CLI: `npm i -g vercel`
   - Run: `cd frontend && vercel`
   - Follow prompts
   - Add environment variable:
     - `BACKEND_URL` = your_render_backend_url

---

## 🔑 Required API Keys

Before deploying, get these FREE API keys:

1. **Groq API Key**
   - Visit: https://console.groq.com
   - Sign up → Create API Key
   - Copy key

2. **SerpAPI Key**
   - Visit: https://serpapi.com
   - Sign up → Get API Key
   - Free tier: 100 searches/month

---

## 🎯 Recommended Setup for FREE Hosting

**Best Option:** Render.com for both services

- ✅ FREE tier available
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ✅ Easy environment variables
- ✅ Good uptime

**Total Cost:** $0/month (Free tier)

---

## 📊 Post-Deployment Checklist

- [ ] Both services are running
- [ ] Frontend can reach backend API
- [ ] Resume upload works
- [ ] Job recommendations load
- [ ] Chatbot responds
- [ ] Email generator works
- [ ] Cover letter generator works
- [ ] All 6 tabs functional

---

## 🐛 Troubleshooting

**Issue:** Frontend can't connect to backend
- **Fix:** Update `BACKEND_URL` in frontend environment variables

**Issue:** Jobs not loading
- **Fix:** Check SERP_API_KEY is set correctly in backend

**Issue:** Chatbot not responding
- **Fix:** Verify GROQ_API_KEY is valid and has quota

**Issue:** Cold start delay (Render free tier)
- **Fix:** First load takes 30-60s, subsequent loads are fast

---

## 🔗 Live URLs (After Deployment)

- **Frontend:** https://aibir-frontend.onrender.com
- **Backend API:** https://aibir-backend.onrender.com
- **GitHub Repo:** https://github.com/decode2211/aibir-engine

---

## 📧 Need Help?

If you encounter issues during deployment:
1. Check server logs in Render/Railway dashboard
2. Verify all environment variables are set
3. Ensure API keys are valid
4. Check backend is accessible at `/` endpoint

Good luck with your deployment! 🚀
