import requests
import json

def test_study_time_prediction():
    """Test the study time prediction API endpoint"""
    
    # API endpoint
    url = "http://127.0.0.1:8000/predict"
    
    # Sample test data
    test_data = {
        "failures": 0,
        "higher": 1,
        "absences": 3,
        "freetime": 2,
        "goout": 3,
        "famrel": 4,
        "famsup": 1,
        "schoolsup": 0,
        "paid": 1,
        "traveltime": 2,
        "health": 5,
        "internet": 1,
        "age": 17
    }
    
    try:
        # Make POST request
        response = requests.post(url, json=test_data)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print("\n📊 Prediction Results:")
            print(f"   Study Time: {result['predicted_study_time']}")
            print(f"   Confidence: {result['confidence_level']}")
            print(f"   Key Factors: {', '.join(result['key_influencing_factors'])}")
            print(f"   Recommendation: {result['recommendation']}")
        else:
            print(f"❌ API Test Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running!")
        print("   Run: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_endpoint():
    """Test the health check endpoint"""
    
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print("✅ Health Check: API is running!")
            print(f"   Status: {response.json()}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Health Check: API server not running")

if __name__ == "__main__":
    print("🧪 Testing Study Time Prediction API")
    print("=" * 50)
    
    # Test health endpoint first
    test_health_endpoint()
    print()
    
    # Test prediction endpoint
    test_study_time_prediction()
