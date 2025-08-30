#!/usr/bin/env python3
"""
Cloud Deployment Preparation Script
Prepares your Study Time Prediction API for cloud deployment
"""

import os
import sys
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required files exist for cloud deployment"""
    print("🔍 Checking deployment requirements...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'study_time_model.pkl',
        '.gitignore'
    ]
    
    missing_files = []
    existing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(file)
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print(f"\n✅ All {len(existing_files)} required files found!")
    return True

def create_railway_config():
    """Create Railway-specific configuration"""
    print("\n🚂 Creating Railway configuration...")
    
    # Create railway.toml if it doesn't exist
    railway_config = '''[build]
builder = "dockerfile"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
'''
    
    with open('railway.toml', 'w') as f:
        f.write(railway_config)
    
    print("✅ Created railway.toml")

def create_render_config():
    """Create Render-specific configuration"""
    print("\n🎨 Creating Render configuration...")
    
    # Create render.yaml if it doesn't exist
    render_config = '''services:
  - type: web
    name: study-time-api
    env: docker
    plan: free
    buildCommand: ""
    startCommand: ""
    healthCheckPath: /health
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: LOG_LEVEL
        value: info
'''
    
    with open('render.yaml', 'w') as f:
        f.write(render_config)
    
    print("✅ Created render.yaml")

def create_github_workflow():
    """Create GitHub Actions workflow for automated testing"""
    print("\n🔄 Creating GitHub Actions workflow...")
    
    # Create .github/workflows directory
    os.makedirs('.github/workflows', exist_ok=True)
    
    workflow = '''name: Test API

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test API
      run: |
        python -c "
        import requests
        import time
        import subprocess
        import sys
        
        # Start the API
        process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'])
        
        # Wait for API to start
        time.sleep(5)
        
        try:
            # Test health endpoint
            response = requests.get('http://127.0.0.1:8000/health')
            assert response.status_code == 200
            print('✅ Health check passed')
            
            # Test prediction endpoint
            test_data = {
                'failures': 0, 'higher': 1, 'absences': 3,
                'freetime': 2, 'goout': 3, 'famrel': 4,
                'famsup': 1, 'schoolsup': 0, 'paid': 1,
                'traveltime': 2, 'health': 5, 'internet': 1, 'age': 17
            }
            
            response = requests.post('http://127.0.0.1:8000/predict', json=test_data)
            assert response.status_code == 200
            print('✅ Prediction endpoint working')
            
        finally:
            process.terminate()
        "
'''
    
    with open('.github/workflows/test.yml', 'w') as f:
        f.write(workflow)
    
    print("✅ Created GitHub Actions workflow")

def create_deployment_readme():
    """Create deployment-specific README"""
    print("\n📝 Creating deployment README...")
    
    deployment_readme = '''# 🚀 Study Time Prediction API - Cloud Deployment

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
'''
    
    with open('DEPLOYMENT.md', 'w') as f:
        f.write(deployment_readme)
    
    print("✅ Created DEPLOYMENT.md")

def main():
    print("🚀 Study Time Prediction API - Cloud Deployment Preparation")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please ensure all required files are present before deploying.")
        sys.exit(1)
    
    # Create platform-specific configurations
    create_railway_config()
    create_render_config()
    create_github_workflow()
    create_deployment_readme()
    
    print("\n🎉 Deployment preparation complete!")
    print("\n📋 Next Steps:")
    print("1. Push your code to GitHub")
    print("2. Choose a cloud platform (Railway recommended)")
    print("3. Connect your GitHub repository")
    print("4. Deploy! 🚀")
    
    print("\n📚 Available platforms:")
    print("   • Railway: https://railway.app/ (Easiest)")
    print("   • Render: https://render.com/ (Good free tier)")
    print("   • DigitalOcean: https://www.digitalocean.com/ (Professional)")
    print("   • Google Cloud: https://cloud.google.com/ (Enterprise)")
    
    print("\n📖 See cloud_deployment_guide.md for detailed instructions")

if __name__ == "__main__":
    main()
