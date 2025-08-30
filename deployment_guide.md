# 🚀 Study Time Prediction API - Deployment Guide

This guide provides multiple deployment options for your Study Time Prediction API to use in your AI Study Planner project.

## 📋 **Prerequisites**

- Python 3.8+
- Your trained model: `study_time_model.pkl`
- All project files from this repository

## 🎯 **Deployment Options**

### 1. **Local Deployment (Recommended for Development)**

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
python deploy.py
# Select option 1 for local deployment
```

**Manual Start:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Access:**
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

### 2. **Docker Deployment (Recommended for Production)**

**Using Docker:**
```bash
# Build and run with Docker
docker build -t study-api .
docker run -d --name study-api-container -p 8000:8000 study-api
```

**Using Docker Compose:**
```bash
# Start with Docker Compose
docker-compose up -d

# Stop
docker-compose down
```

### 3. **Cloud Deployment Options**

#### **A. Heroku**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-study-api
git add .
git commit -m "Deploy API"
git push heroku main
```

#### **B. Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

#### **C. Render**
```bash
# Connect your GitHub repo to Render
# Set build command: pip install -r requirements.txt
# Set start command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### **D. DigitalOcean App Platform**
```bash
# Use the provided Dockerfile
# Deploy through DigitalOcean dashboard
```

## 🔧 **Integration with AI Study Planner**

### **Python Integration**
```python
import requests

class StudyPlannerAPI:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
    
    def get_study_prediction(self, student_data):
        """Get study time prediction for a student"""
        response = requests.post(
            f"{self.api_url}/predict",
            json=student_data
        )
        return response.json()
    
    def check_api_health(self):
        """Check if API is running"""
        try:
            response = requests.get(f"{self.api_url}/health")
            return response.status_code == 200
        except:
            return False

# Usage in your Study Planner
api = StudyPlannerAPI("http://your-api-url.com")
prediction = api.get_study_prediction({
    "failures": 0, "higher": 1, "absences": 3,
    "freetime": 2, "goout": 3, "famrel": 4,
    "famsup": 1, "schoolsup": 0, "paid": 1,
    "traveltime": 2, "health": 5, "internet": 1, "age": 17
})
```

### **JavaScript/Node.js Integration**
```javascript
class StudyPlannerAPI {
    constructor(apiUrl = "http://localhost:8000") {
        this.apiUrl = apiUrl;
    }
    
    async getStudyPrediction(studentData) {
        const response = await fetch(`${this.apiUrl}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async checkHealth() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
}

// Usage
const api = new StudyPlannerAPI("http://your-api-url.com");
api.getStudyPrediction({
    failures: 0, higher: 1, absences: 3,
    freetime: 2, goout: 3, famrel: 4,
    famsup: 1, schoolsup: 0, paid: 1,
    traveltime: 2, health: 5, internet: 1, age: 17
}).then(result => console.log(result));
```

### **React/Frontend Integration**
```jsx
import React, { useState, useEffect } from 'react';

const StudyPredictionComponent = () => {
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const getPrediction = async (studentData) => {
        setLoading(true);
        try {
            const response = await fetch('http://your-api-url.com/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(studentData)
            });
            
            const result = await response.json();
            setPrediction(result);
        } catch (error) {
            console.error('Prediction failed:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div>
            {loading && <p>Loading prediction...</p>}
            {prediction && (
                <div>
                    <h3>Study Time Prediction</h3>
                    <p>Recommended: {prediction.predicted_study_time}</p>
                    <p>Confidence: {prediction.confidence_level}</p>
                    <p>Recommendation: {prediction.recommendation}</p>
                </div>
            )}
        </div>
    );
};
```

## 🔒 **Security & Production Considerations**

### **Environment Variables**
```bash
# Create .env file
ENVIRONMENT=production
LOG_LEVEL=info
API_KEY=your-secret-key
CORS_ORIGINS=https://yourdomain.com
```

### **CORS Configuration**
```python
# Add to main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Rate Limiting**
```python
# Add rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("10/minute")
def predict_studytime(request: Request, data: StudyTimeInput):
    # Your prediction logic
```

## 📊 **Monitoring & Health Checks**

### **Health Check Endpoint**
```bash
curl http://your-api-url.com/health
```

### **Logging**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/predict")
def predict_studytime(data: StudyTimeInput):
    logger.info(f"Prediction request received for student age: {data.age}")
    # Your logic here
```

## 🚀 **Quick Deployment Commands**

### **Generate Client Code**
```bash
python deploy.py
# Select option 4
# Enter your API URL
```

### **Test Deployment**
```bash
python deploy.py
# Select option 5
# Enter your API URL
```

### **Full Deployment with Docker**
```bash
# Build and deploy
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📞 **Support**

If you encounter issues:
1. Check the API health endpoint
2. Review logs for errors
3. Ensure your model file is accessible
4. Verify all dependencies are installed

Your API is now ready to be integrated into your AI Study Planner! 🎉
