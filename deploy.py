#!/usr/bin/env python3
"""
Study Time Prediction API Deployment Script
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

class APIDeployer:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.api_url = None
        
    def check_dependencies(self):
        """Check if required files exist"""
        required_files = ['main.py', 'requirements.txt', 'study_time_model.pkl']
        missing_files = []
        
        for file in required_files:
            if not (self.project_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        print("✅ All required files found!")
        return True
    
    def deploy_local(self):
        """Deploy locally using uvicorn"""
        print("🚀 Deploying API locally...")
        try:
            subprocess.run([
                sys.executable, "-m", "uvicorn", 
                "main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--workers", "4"
            ], check=True)
        except KeyboardInterrupt:
            print("\n👋 Local deployment stopped.")
        except Exception as e:
            print(f"❌ Local deployment failed: {e}")
    
    def deploy_docker(self):
        """Deploy using Docker"""
        print("🐳 Deploying API with Docker...")
        try:
            # Build Docker image
            subprocess.run(["docker", "build", "-t", "study-api", "."], check=True)
            print("✅ Docker image built successfully!")
            
            # Run container
            subprocess.run([
                "docker", "run", "-d",
                "--name", "study-api-container",
                "-p", "8000:8000",
                "-v", f"{self.project_dir}/study_time_model.pkl:/app/study_time_model.pkl:ro",
                "study-api"
            ], check=True)
            print("✅ Docker container started!")
            print("🌐 API available at: http://localhost:8000")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker deployment failed: {e}")
        except FileNotFoundError:
            print("❌ Docker not found. Please install Docker first.")
    
    def deploy_docker_compose(self):
        """Deploy using Docker Compose"""
        print("🐳 Deploying API with Docker Compose...")
        try:
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print("✅ Docker Compose deployment successful!")
            print("🌐 API available at: http://localhost:8000")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker Compose deployment failed: {e}")
        except FileNotFoundError:
            print("❌ Docker Compose not found. Please install Docker Compose first.")
    
    def test_deployment(self, url="http://localhost:8000"):
        """Test the deployed API"""
        print(f"🧪 Testing deployment at {url}...")
        try:
            # Test health endpoint
            health_response = requests.get(f"{url}/health", timeout=10)
            if health_response.status_code == 200:
                print("✅ Health check passed!")
                
                # Test prediction endpoint
                test_data = {
                    "failures": 0, "higher": 1, "absences": 3,
                    "freetime": 2, "goout": 3, "famrel": 4,
                    "famsup": 1, "schoolsup": 0, "paid": 1,
                    "traveltime": 2, "health": 5, "internet": 1, "age": 17
                }
                
                pred_response = requests.post(
                    f"{url}/predict", 
                    json=test_data, 
                    timeout=10
                )
                
                if pred_response.status_code == 200:
                    result = pred_response.json()
                    print("✅ Prediction endpoint working!")
                    print(f"📊 Sample prediction: {result['predicted_study_time']}")
                    return True
                else:
                    print(f"❌ Prediction endpoint failed: {pred_response.status_code}")
                    return False
            else:
                print(f"❌ Health check failed: {health_response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Deployment test failed: {e}")
            return False
    
    def generate_client_code(self, base_url="http://localhost:8000"):
        """Generate client code for different languages"""
        print("📝 Generating client code...")
        
        # Python client
        python_client = f'''import requests

class StudyTimeAPI:
    def __init__(self, base_url="{base_url}"):
        self.base_url = base_url
    
    def predict_study_time(self, **features):
        """Predict study time based on student features"""
        response = requests.post(f"{{self.base_url}}/predict", json=features)
        response.raise_for_status()
        return response.json()
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{{self.base_url}}/health")
        response.raise_for_status()
        return response.json()

# Usage example
api = StudyTimeAPI()
result = api.predict_study_time(
    failures=0, higher=1, absences=3, freetime=2,
    goout=3, famrel=4, famsup=1, schoolsup=0,
    paid=1, traveltime=2, health=5, internet=1, age=17
)
print(result)
'''
        
        # JavaScript client
        js_client = f'''class StudyTimeAPI {{
    constructor(baseUrl = "{base_url}") {{
        this.baseUrl = baseUrl;
    }}
    
    async predictStudyTime(features) {{
        const response = await fetch(`${{this.baseUrl}}/predict`, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify(features)
        }});
        
        if (!response.ok) {{
            throw new Error(`HTTP error! status: ${{response.status}}`);
        }}
        
        return await response.json();
    }}
    
    async healthCheck() {{
        const response = await fetch(`${{this.baseUrl}}/health`);
        if (!response.ok) {{
            throw new Error(`HTTP error! status: ${{response.status}}`);
        }}
        return await response.json();
    }}
}}

// Usage example
const api = new StudyTimeAPI();
api.predictStudyTime({{
    failures: 0, higher: 1, absences: 3, freetime: 2,
    goout: 3, famrel: 4, famsup: 1, schoolsup: 0,
    paid: 1, traveltime: 2, health: 5, internet: 1, age: 17
}}).then(result => console.log(result));
'''
        
        # Save client code
        with open('client_python.py', 'w') as f:
            f.write(python_client)
        
        with open('client_javascript.js', 'w') as f:
            f.write(js_client)
        
        print("✅ Client code generated:")
        print("   - client_python.py")
        print("   - client_javascript.js")

def main():
    deployer = APIDeployer()
    
    print("🚀 Study Time Prediction API Deployment")
    print("=" * 50)
    
    if not deployer.check_dependencies():
        sys.exit(1)
    
    print("\n📋 Deployment Options:")
    print("1. Local deployment (uvicorn)")
    print("2. Docker deployment")
    print("3. Docker Compose deployment")
    print("4. Generate client code")
    print("5. Test existing deployment")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        deployer.deploy_local()
    elif choice == "2":
        deployer.deploy_docker()
    elif choice == "3":
        deployer.deploy_docker_compose()
    elif choice == "4":
        base_url = input("Enter API base URL (default: http://localhost:8000): ").strip()
        if not base_url:
            base_url = "http://localhost:8000"
        deployer.generate_client_code(base_url)
    elif choice == "5":
        url = input("Enter API URL to test (default: http://localhost:8000): ").strip()
        if not url:
            url = "http://localhost:8000"
        deployer.test_deployment(url)
    else:
        print("❌ Invalid option selected.")

if __name__ == "__main__":
    main()
