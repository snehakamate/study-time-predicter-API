# 🎨 Render Deployment Guide - Study Time Prediction API

This guide will walk you through deploying your API to Render step by step.

## 📋 **Prerequisites**

✅ **Already Done:**
- Your API code is ready
- `Dockerfile` is configured
- `render.yaml` is set up
- All dependencies are included

## 🚀 **Step-by-Step Deployment**

### **Step 1: Create GitHub Repository**

1. **Go to GitHub**: https://github.com/
2. **Create New Repository**:
   - Click "New repository"
   - Name: `study-time-prediction-api`
   - Make it Public (Render free tier requirement)
   - Don't initialize with README (you already have files)
3. **Upload Your Code**:
   ```bash
   # In your project directory
   git init
   git add .
   git commit -m "Initial commit - Study Time Prediction API"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/study-time-prediction-api.git
   git push -u origin main
   ```

### **Step 2: Sign Up for Render**

1. **Go to Render**: https://render.com/
2. **Sign Up**:
   - Click "Get Started for Free"
   - Choose "Continue with GitHub" (recommended)
   - Authorize Render to access your GitHub account

### **Step 3: Deploy Your API**

1. **Create New Web Service**:
   - Click "New" → "Web Service"
   - Click "Connect" next to your GitHub repository

2. **Configure Your Service**:
   - **Name**: `study-time-api` (or any name you prefer)
   - **Environment**: `Docker` (this is important!)
   - **Branch**: `main`
   - **Build Command**: Leave empty (uses Dockerfile)
   - **Start Command**: Leave empty (uses Dockerfile)

3. **Advanced Settings** (Optional):
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: ✅ Enabled (recommended)

4. **Environment Variables** (Optional):
   - Click "Advanced" → "Environment Variables"
   - Add:
     - `ENVIRONMENT` = `production`
     - `LOG_LEVEL` = `info`

5. **Deploy**:
   - Click "Create Web Service"
   - Render will start building your Docker image

### **Step 4: Monitor Deployment**

1. **Watch the Build**:
   - You'll see build logs in real-time
   - This may take 5-10 minutes for the first build

2. **Check for Success**:
   - Green checkmark = Success
   - Red X = Error (check logs)

### **Step 5: Test Your API**

Once deployed, your API will be available at:
- **URL**: `https://your-app-name.onrender.com`
- **Health Check**: `https://your-app-name.onrender.com/health`
- **Documentation**: `https://your-app-name.onrender.com/docs`

**Test Commands**:
```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test prediction endpoint
curl -X POST https://your-app-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "failures": 0, "higher": 1, "absences": 3,
    "freetime": 2, "goout": 3, "famrel": 4,
    "famsup": 1, "schoolsup": 0, "paid": 1,
    "traveltime": 2, "health": 5, "internet": 1, "age": 17
  }'
```

## 🔧 **Integration with AI Study Planner**

### **Update Your Study Planner Code**

Replace your local API URL with the Render URL:

```python
# Before (local)
api_url = "http://localhost:8000"

# After (Render)
api_url = "https://your-app-name.onrender.com"

# Use the client library
from study_api_client import StudyTimeAPIClient

client = StudyTimeAPIClient(api_url)
prediction = client.predict_study_time(
    failures=0, higher=1, absences=3, freetime=2,
    goout=3, famrel=4, famsup=1, schoolsup=0,
    paid=1, traveltime=2, health=5, internet=1, age=17
)

print(f"Study Time: {prediction.predicted_study_time}")
print(f"Confidence: {prediction.confidence_level}")
print(f"Recommendation: {prediction.recommendation}")
```

## 📊 **Render Dashboard Features**

### **Monitoring**
- **Logs**: View real-time application logs
- **Metrics**: CPU, memory usage
- **Deployments**: History of all deployments

### **Auto-Deploy**
- Every push to `main` branch triggers a new deployment
- Automatic rollback on failure

### **Custom Domains**
- Add your own domain (paid feature)
- Automatic HTTPS

## 💰 **Pricing**

### **Free Tier**:
- ✅ 750 hours/month (enough for 24/7 usage)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Automatic HTTPS
- ✅ Custom domains (paid)

### **Paid Plans**:
- **Starter**: $7/month - 1 GB RAM, dedicated CPU
- **Standard**: $25/month - 2 GB RAM, better performance

## 🚨 **Common Issues & Solutions**

### **1. Build Fails**
**Symptoms**: Red X in deployment
**Solutions**:
- Check build logs for errors
- Ensure `Dockerfile` is in root directory
- Verify all files are committed to GitHub

### **2. API Not Responding**
**Symptoms**: 502/503 errors
**Solutions**:
- Check application logs
- Verify `/health` endpoint works
- Ensure model file is included

### **3. Slow Response Times**
**Symptoms**: Long loading times
**Solutions**:
- Free tier has cold starts (first request after inactivity)
- Consider upgrading to paid plan for better performance

### **4. Model Loading Issues**
**Symptoms**: 503 Service Unavailable
**Solutions**:
- Check if `study_time_model.pkl` is in repository
- Verify file permissions
- Check application logs for model loading errors

## 🔄 **Updating Your API**

### **Automatic Updates**:
1. Make changes to your code
2. Push to GitHub `main` branch
3. Render automatically deploys the new version

### **Manual Updates**:
1. Go to Render dashboard
2. Click on your service
3. Click "Manual Deploy"

## 📞 **Support**

### **Render Support**:
- **Documentation**: https://render.com/docs
- **Community**: https://community.render.com/
- **Status**: https://status.render.com/

### **Your API Health**:
- **Health Check**: `https://your-app-name.onrender.com/health`
- **Logs**: Available in Render dashboard

## 🎉 **Success Checklist**

- [ ] GitHub repository created and code pushed
- [ ] Render account created
- [ ] Web service deployed successfully
- [ ] Health endpoint responding
- [ ] Prediction endpoint working
- [ ] Integration with Study Planner tested
- [ ] Auto-deploy working

## 🚀 **Next Steps**

1. **Deploy to Render** (follow steps above)
2. **Test thoroughly** (health + prediction endpoints)
3. **Update your Study Planner** with the new API URL
4. **Monitor performance** in Render dashboard
5. **Scale up** if needed (upgrade to paid plan)

Your API will be live and ready to serve your AI Study Planner! 🎯
