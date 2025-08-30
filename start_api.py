#!/usr/bin/env python3
"""
Study Time Prediction API Startup Script
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pandas
        import numpy
        import joblib
        import sklearn
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_model_file():
    """Check if the model file exists"""
    if os.path.exists("study_time_model.pkl"):
        print("✅ Model file found: study_time_model.pkl")
        return True
    else:
        print("⚠️  Model file not found: study_time_model.pkl")
        print("   Please ensure your trained model is in the project root directory.")
        print("   The API will still start but prediction endpoints will return errors.")
        return False

def main():
    print("🚀 Study Time Prediction API")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model file
    model_exists = check_model_file()
    
    print("\n📋 API Information:")
    print("   • Local URL: http://127.0.0.1:8000")
    print("   • Interactive Docs: http://127.0.0.1:8000/docs")
    print("   • Health Check: http://127.0.0.1:8000/health")
    
    if not model_exists:
        print("\n⚠️  Note: API will start but prediction endpoints will be unavailable")
        print("   until you add your studytime_model.pkl file.")
    
    print("\n🎯 To test the API:")
    print("   1. Open http://127.0.0.1:8000/docs in your browser")
    print("   2. Try the /predict endpoint with sample data")
    print("   3. Or run: python test_api.py")
    
    print("\n🔄 Starting API server...")
    print("   Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Start the uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 API server stopped.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
