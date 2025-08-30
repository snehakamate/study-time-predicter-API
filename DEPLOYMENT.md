# 🚀 Study Time Prediction API - Cloud Deployment

This API is ready for cloud deployment using Docker.

## 🐳 Quick Deploy

### Railway (Recommended)
1. Go to https://railway.app/
2. Sign up and connect GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Deploy! 🎉

### Render
1. Go to https://render.com/
2. Sign up and connect GitHub
3. Click "New" → "Web Service"
4. Select this repository
5. Configure:
   - Name: `study-time-api`
   - Environment: `Docker`
6. Deploy! 🎉

### DigitalOcean
1. Go to https://www.digitalocean.com/
2. Create App Platform
3. Connect GitHub and select this repository
4. Deploy! 🎉

## 🔗 API Endpoints

After deployment, your API will be available at:
- **Health Check**: `https://your-app-url.com/health`
- **Prediction**: `https://your-app-url.com/predict`
- **Documentation**: `https://your-app-url.com/docs`

## 📊 Usage Example

```python
import requests

# Get prediction
response = requests.post('https://your-app-url.com/predict', json={
    'failures': 0, 'higher': 1, 'absences': 3,
    'freetime': 2, 'goout': 3, 'famrel': 4,
    'famsup': 1, 'schoolsup': 0, 'paid': 1,
    'traveltime': 2, 'health': 5, 'internet': 1, 'age': 17
})

result = response.json()
print(f"Study Time: {result['predicted_study_time']}")
```

## 🔧 Integration

Use the `study_api_client.py` file to easily integrate with your AI Study Planner:

```python
from study_api_client import StudyTimeAPIClient

client = StudyTimeAPIClient("https://your-app-url.com")
prediction = client.predict_study_time(
    failures=0, higher=1, absences=3, freetime=2,
    goout=3, famrel=4, famsup=1, schoolsup=0,
    paid=1, traveltime=2, health=5, internet=1, age=17
)
```

## 📞 Support

If you encounter issues:
1. Check the health endpoint
2. Review platform logs
3. Ensure all files are in the repository
4. Verify model file is included

Happy deploying! 🚀
