"""
Study Time Prediction API Client Library
Easy integration for your AI Study Planner project
"""

import requests
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class StudyPrediction:
    """Study time prediction result"""
    predicted_study_time: str
    confidence_level: str
    key_influencing_factors: list
    recommendation: str

class StudyTimeAPIClient:
    """
    Client for the Study Time Prediction API
    
    Usage:
        client = StudyTimeAPIClient("http://localhost:8000")
        prediction = client.predict_study_time(
            failures=0, higher=1, absences=3, freetime=2,
            goout=3, famrel=4, famsup=1, schoolsup=0,
            paid=1, traveltime=2, health=5, internet=1, age=17
        )
        print(prediction.predicted_study_time)
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the API (e.g., "http://localhost:8000")
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API is healthy and running
        
        Returns:
            Health status information
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API health check failed: {e}")
    
    def predict_study_time(self, **features) -> StudyPrediction:
        """
        Predict study time based on student features
        
        Args:
            **features: Student features (failures, higher, absences, etc.)
        
        Returns:
            StudyPrediction object with prediction results
        
        Raises:
            ValueError: If required features are missing
            ConnectionError: If API request fails
        """
        # Validate required features
        required_features = {
            'failures', 'higher', 'absences', 'freetime', 'goout',
            'famrel', 'famsup', 'schoolsup', 'paid', 'traveltime',
            'health', 'internet', 'age'
        }
        
        missing_features = required_features - set(features.keys())
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=features,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return StudyPrediction(
                predicted_study_time=data['predicted_study_time'],
                confidence_level=data['confidence_level'],
                key_influencing_factors=data['key_influencing_factors'],
                recommendation=data['recommendation']
            )
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Prediction request failed: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid API response format: {e}")
    
    def predict_study_time_dict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict study time using a dictionary of features
        
        Args:
            features: Dictionary containing student features
        
        Returns:
            Dictionary with prediction results
        """
        prediction = self.predict_study_time(**features)
        return {
            'predicted_study_time': prediction.predicted_study_time,
            'confidence_level': prediction.confidence_level,
            'key_influencing_factors': prediction.key_influencing_factors,
            'recommendation': prediction.recommendation
        }
    
    def is_available(self) -> bool:
        """
        Check if the API is available
        
        Returns:
            True if API is available, False otherwise
        """
        try:
            self.health_check()
            return True
        except:
            return False
    
    def get_api_info(self) -> Dict[str, Any]:
        """
        Get API information and documentation URL
        
        Returns:
            Dictionary with API information
        """
        return {
            'base_url': self.base_url,
            'docs_url': f"{self.base_url}/docs",
            'health_url': f"{self.base_url}/health",
            'prediction_url': f"{self.base_url}/predict"
        }

# Convenience functions for quick usage
def quick_prediction(api_url: str, **features) -> StudyPrediction:
    """
    Quick prediction without creating a client instance
    
    Args:
        api_url: API base URL
        **features: Student features
    
    Returns:
        StudyPrediction object
    """
    client = StudyTimeAPIClient(api_url)
    return client.predict_study_time(**features)

def check_api_health(api_url: str) -> bool:
    """
    Quick health check without creating a client instance
    
    Args:
        api_url: API base URL
    
    Returns:
        True if API is healthy, False otherwise
    """
    client = StudyTimeAPIClient(api_url)
    return client.is_available()

# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage
    client = StudyTimeAPIClient("http://localhost:8000")
    
    if client.is_available():
        print("✅ API is available!")
        
        # Make a prediction
        prediction = client.predict_study_time(
            failures=0, higher=1, absences=3, freetime=2,
            goout=3, famrel=4, famsup=1, schoolsup=0,
            paid=1, traveltime=2, health=5, internet=1, age=17
        )
        
        print(f"📊 Study Time: {prediction.predicted_study_time}")
        print(f"🎯 Confidence: {prediction.confidence_level}")
        print(f"🔍 Key Factors: {', '.join(prediction.key_influencing_factors)}")
        print(f"💡 Recommendation: {prediction.recommendation}")
    else:
        print("❌ API is not available")
    
    # Example 2: Quick prediction
    try:
        result = quick_prediction("http://localhost:8000",
            failures=0, higher=1, absences=3, freetime=2,
            goout=3, famrel=4, famsup=1, schoolsup=0,
            paid=1, traveltime=2, health=5, internet=1, age=17
        )
        print(f"Quick prediction: {result.predicted_study_time}")
    except Exception as e:
        print(f"Quick prediction failed: {e}")
