# Study Time Prediction API

A FastAPI-based machine learning API that predicts study time based on student characteristics and behaviors.

## Features

- **Study Time Prediction**: Predicts daily study time in hours based on 13 input features
- **Confidence Scoring**: Provides confidence levels for predictions
- **Key Influencing Factors**: Identifies important factors affecting study time
- **Personalized Recommendations**: Offers tailored study advice
- **Interactive Documentation**: Auto-generated API docs with Swagger UI

## Setup

### Prerequisites

- Python 3.8+
- Your trained model file: `studytime_model.pkl`

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your model file**:
   - Ensure `studytime_model.pkl` is in the project root directory

3. **Run the API**:
   ```bash
   uvicorn main:app --reload
   ```

## API Usage

### Base URL
- Local: `http://127.0.0.1:8000`
- Interactive Docs: `http://127.0.0.1:8000/docs`

### Endpoints

#### 1. Health Check
```bash
GET /
GET /health
```

#### 2. Study Time Prediction
```bash
POST /predict
```

**Request Body**:
```json
{
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
```

**Response**:
```json
{
  "predicted_study_time": "2.5 hours/day",
  "confidence_level": "87%",
  "key_influencing_factors": [
    "Low failures",
    "High motivation",
    "Good health"
  ],
  "recommendation": "Great! Keep up the good work, aim for balance between study and rest."
}
```

## Feature Descriptions

| Feature | Description | Range |
|---------|-------------|-------|
| `failures` | Number of past failures | 0-4 |
| `higher` | Wants to take higher education | 0-1 |
| `absences` | Number of school absences | 0-93 |
| `freetime` | Free time after school | 1-5 |
| `goout` | Going out with friends | 1-5 |
| `famrel` | Quality of family relationships | 1-5 |
| `famsup` | Family educational support | 0-1 |
| `schoolsup` | Extra educational support | 0-1 |
| `paid` | Extra paid classes | 0-1 |
| `traveltime` | Home to school travel time | 1-4 |
| `health` | Current health status | 1-5 |
| `internet` | Internet access at home | 0-1 |
| `age` | Student's age | 15-22 |

## Testing the API

### Using curl
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

### Using Python requests
```python
import requests

url = "http://127.0.0.1:8000/predict"
data = {
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

response = requests.post(url, json=data)
print(response.json())
```

## Development

### Project Structure
```
std_model_api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── studytime_model.pkl # Your trained model (not included)
```

### Adding New Features

1. **Extend the input schema** in `StudyTimeInput` class
2. **Update preprocessing** in the `predict_studytime` function
3. **Enhance recommendations** based on new features
4. **Add validation** for new input fields

## Troubleshooting

### Common Issues

1. **Model file not found**: Ensure `studytime_model.pkl` is in the project root
2. **Port already in use**: Change port with `uvicorn main:app --reload --port 8001`
3. **Import errors**: Verify all dependencies are installed with `pip install -r requirements.txt`

### Error Handling

The API includes basic error handling for:
- Invalid input data
- Missing model file
- Prediction errors


