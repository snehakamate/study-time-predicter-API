#!/usr/bin/env python3
"""
Render Deployment Setup Script
Prepares your project for Render deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def check_render_requirements():
    """Check if all files are ready for Render deployment"""
    print("🎨 Render Deployment Requirements Check")
    print("=" * 50)
    
    required_files = [
        'main.py',
        'requirements.txt',
        'Dockerfile',
        'render.yaml',
        'study_time_model.pkl',
        '.gitignore'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            all_good = False
    
    print()
    return all_good

def check_git_status():
    """Check if this is a git repository"""
    print("🔍 Git Repository Status")
    print("=" * 30)
    
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
            
            # Check if remote is set
            remote_result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'origin' in remote_result.stdout:
                print("✅ Remote repository configured")
                return True
            else:
                print("⚠️  No remote repository configured")
                return False
        else:
            print("❌ Not a git repository")
            return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False

def create_git_commands():
    """Generate git commands for setup"""
    print("\n📝 Git Setup Commands")
    print("=" * 30)
    
    commands = [
        "# Initialize git repository (if not already done)",
        "git init",
        "",
        "# Add all files",
        "git add .",
        "",
        "# Commit changes",
        'git commit -m "Initial commit - Study Time Prediction API"',
        "",
        "# Set main branch",
        "git branch -M main",
        "",
        "# Add remote (replace YOUR_USERNAME with your GitHub username)",
        "git remote add origin https://github.com/YOUR_USERNAME/study-time-prediction-api.git",
        "",
        "# Push to GitHub",
        "git push -u origin main"
    ]
    
    for cmd in commands:
        print(cmd)

def show_render_steps():
    """Show Render deployment steps"""
    print("\n🚀 Render Deployment Steps")
    print("=" * 35)
    
    steps = [
        "1. Go to https://render.com/",
        "2. Sign up with GitHub account",
        "3. Click 'New' → 'Web Service'",
        "4. Connect your GitHub repository",
        "5. Configure:",
        "   - Name: study-time-api",
        "   - Environment: Docker",
        "   - Branch: main",
        "   - Build Command: (leave empty)",
        "   - Start Command: (leave empty)",
        "6. Click 'Create Web Service'",
        "7. Wait for deployment (5-10 minutes)",
        "8. Test your API at: https://your-app-name.onrender.com"
    ]
    
    for step in steps:
        print(step)

def test_local_api():
    """Test if local API is working"""
    print("\n🧪 Local API Test")
    print("=" * 20)
    
    try:
        import requests
        import time
        import subprocess
        import sys
        
        print("Starting local API...")
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 
            'main:app', '--host', '127.0.0.1', '--port', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for API to start
        time.sleep(3)
        
        try:
            # Test health endpoint
            response = requests.get('http://127.0.0.1:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
                
                # Test prediction endpoint
                test_data = {
                    'failures': 0, 'higher': 1, 'absences': 3,
                    'freetime': 2, 'goout': 3, 'famrel': 4,
                    'famsup': 1, 'schoolsup': 0, 'paid': 1,
                    'traveltime': 2, 'health': 5, 'internet': 1, 'age': 17
                }
                
                response = requests.post(
                    'http://127.0.0.1:8000/predict', 
                    json=test_data, 
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Prediction endpoint working")
                    print(f"   Sample prediction: {result['predicted_study_time']}")
                else:
                    print(f"❌ Prediction endpoint failed: {response.status_code}")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API test failed: {e}")
        
        finally:
            process.terminate()
            
    except ImportError:
        print("❌ Requests library not installed")
        print("   Run: pip install requests")

def main():
    print("🎨 Study Time Prediction API - Render Deployment Setup")
    print("=" * 60)
    
    # Check requirements
    if not check_render_requirements():
        print("\n❌ Missing required files. Please ensure all files are present.")
        sys.exit(1)
    
    # Check git status
    git_ready = check_git_status()
    
    # Test local API
    test_local_api()
    
    print("\n" + "=" * 60)
    
    if git_ready:
        print("🎉 Your project is ready for Render deployment!")
        show_render_steps()
    else:
        print("📝 Setup required:")
        create_git_commands()
        print("\nAfter setting up git:")
        show_render_steps()
    
    print("\n📖 For detailed instructions, see: RENDER_DEPLOYMENT_GUIDE.md")
    print("🚀 Happy deploying!")

if __name__ == "__main__":
    main()
