# 🐳 Docker Cloud Deployment Guide

This guide will help you deploy your Study Time Prediction API to various cloud platforms using Docker.

## 📋 **Prerequisites**

1. **Install Docker Desktop** (if not already installed):
   - Download from: https://www.docker.com/products/docker-desktop/
   - Install and start Docker Desktop
   - Verify installation: `docker --version`

2. **GitHub Account** (for most platforms)
3. **Cloud Platform Account** (choose one below)

## 🎯 **Deployment Options**

### **Option 1: Railway (Recommended - Easiest)**

**Pros:**
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Built-in Docker support
- ✅ Easy setup
- ✅ Great for beginners

**Steps:**
1. **Sign up**: Go to https://railway.app/
2. **Connect GitHub**: Link your GitHub account
3. **Create Project**: Click "New Project" → "Deploy from GitHub repo"
4. **Select Repository**: Choose your API repository
5. **Deploy**: Railway will automatically detect Docker and deploy

**Configuration:**
- Railway automatically detects your `Dockerfile`
- No additional configuration needed
- Your API will be available at: `https://your-app-name.railway.app`

---

### **Option 2: Render**

**Pros:**
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy Docker deployment
- ✅ Good documentation

**Steps:**
1. **Sign up**: Go to https://render.com/
2. **Connect GitHub**: Link your GitHub account
3. **Create Web Service**: Click "New" → "Web Service"
4. **Select Repository**: Choose your API repository
5. **Configure**:
   - **Name**: `study-time-api`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Build Command**: Leave empty (uses Dockerfile)
   - **Start Command**: Leave empty (uses Dockerfile)
6. **Deploy**: Click "Create Web Service"

**Environment Variables** (optional):
```
ENVIRONMENT=production
LOG_LEVEL=info
```

---

### **Option 3: DigitalOcean App Platform**

**Pros:**
- ✅ Professional platform
- ✅ Excellent Docker support
- ✅ Reasonable pricing ($5/month)
- ✅ Great performance

**Steps:**
1. **Sign up**: Go to https://www.digitalocean.com/
2. **Create App**: Click "Create" → "Apps"
3. **Connect GitHub**: Link your GitHub account
4. **Select Repository**: Choose your API repository
5. **Configure**:
   - **Source**: GitHub
   - **Branch**: `main`
   - **Build Command**: Leave empty (uses Dockerfile)
   - **Run Command**: Leave empty (uses Dockerfile)
6. **Deploy**: Click "Create Resources"

---

### **Option 4: Google Cloud Run**

**Pros:**
- ✅ Serverless Docker
- ✅ Pay per use
- ✅ Auto-scaling
- ✅ Enterprise-grade

**Steps:**
1. **Install Google Cloud CLI**:
   ```bash
   # Download and install from: https://cloud.google.com/sdk/docs/install
   ```

2. **Initialize Project**:
   ```bash
   gcloud init
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable Cloud Run**:
   ```bash
   gcloud services enable run.googleapis.com
   ```

4. **Deploy**:
   ```bash
   gcloud run deploy study-time-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## 🔧 **Local Docker Testing**

Before deploying to cloud, test locally:

```bash
# Build the Docker image
docker build -t study-api .

# Run the container
docker run -p 8000:8000 study-api

# Test the API
curl http://localhost:8000/health
```

## 📝 **Required Files for Cloud Deployment**

Your repository should contain:
- ✅ `Dockerfile` (already created)
- ✅ `docker-compose.yml` (already created)
- ✅ `main.py` (API code)
- ✅ `requirements.txt` (dependencies)
- ✅ `study_time_model.pkl` (your model)
- ✅ `.gitignore` (exclude unnecessary files)

## 🌐 **Post-Deployment**

After successful deployment:

1. **Get your API URL** (e.g., `https://your-app.railway.app`)
2. **Test the API**:
   ```bash
   curl https://your-app.railway.app/health
   ```
3. **Update your AI Study Planner** to use the new URL
4. **Test integration** with your Study Planner

## 🔒 **Security Considerations**

### **Environment Variables**
Add these to your cloud platform:
```
ENVIRONMENT=production
LOG_LEVEL=info
```

### **CORS Configuration**
If your Study Planner is on a different domain, add CORS to `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-study-planner-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 **Monitoring**

### **Health Checks**
All platforms will automatically check:
- `GET /health` endpoint
- Container startup
- Application responsiveness

### **Logs**
Access logs through your cloud platform's dashboard:
- Railway: Project → Deployments → View Logs
- Render: Service → Logs
- DigitalOcean: App → Runtime Logs
- Google Cloud: Cloud Run → Logs

## 🚀 **Quick Deployment Commands**

### **Railway (CLI)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### **Render (CLI)**
```bash
# Install Render CLI
curl -sL https://render.com/download-cli/linux | bash

# Deploy
render deploy
```

## 💰 **Cost Comparison**

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Railway | ✅ Yes | $5/month | Beginners |
| Render | ✅ Yes | $7/month | Small projects |
| DigitalOcean | ❌ No | $5/month | Production |
| Google Cloud | ✅ Yes | Pay per use | Enterprise |

## 🎯 **Recommended Workflow**

1. **Start with Railway** (easiest)
2. **Test your API** thoroughly
3. **Integrate with Study Planner**
4. **Scale up** if needed (move to DigitalOcean/Google Cloud)

## 📞 **Troubleshooting**

### **Common Issues:**

1. **Build Fails**:
   - Check Dockerfile syntax
   - Verify all files are in repository
   - Check platform logs

2. **API Not Responding**:
   - Verify health endpoint works
   - Check environment variables
   - Review application logs

3. **Model Loading Issues**:
   - Ensure `study_time_model.pkl` is in repository
   - Check file permissions
   - Verify model compatibility

### **Support Resources:**
- Railway: https://docs.railway.app/
- Render: https://render.com/docs
- DigitalOcean: https://docs.digitalocean.com/
- Google Cloud: https://cloud.google.com/run/docs

Your API is ready for cloud deployment! 🚀
