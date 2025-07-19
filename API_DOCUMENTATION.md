# 📚 API Documentation - Student Performance Predictor

Complete API reference for the Student Performance Predictor Flask backend.

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, no authentication is required. All endpoints are publicly accessible.

## Response Format
All responses are returned in JSON format with appropriate HTTP status codes.

## Endpoints

### 1. Health Check

**GET** `/`

Returns the API status and basic information.

#### Response
```json
{
    "message": "Student Performance Prediction API",
    "status": "Active",
    "version": "1.0"
}
```

#### Status Codes
- `200 OK` - API is running successfully

#### Example Request
```bash
curl -X GET http://localhost:5000/
```

---

### 2. Predict Student Performance

**POST** `/predict`

Predicts whether a student will pass or fail based on provided features.

#### Request Body
The request body must contain a JSON object with the following fields:

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| age | integer | Yes | Student's age | 15-19 |
| sex | string | Yes | Student's gender | "M", "F" |
| address | string | Yes | Home address type | "U" (urban), "R" (rural) |
| famsize | string | Yes | Family size | "LE3" (≤3 members), "GT3" (>3 members) |
| Pstatus | string | No | Parent cohabitation status | "T" (together), "A" (apart) |
| Medu | integer | Yes | Mother's education level | 0-4 |
| Fedu | integer | Yes | Father's education level | 0-4 |
| studytime | integer | Yes | Weekly study time | 1-4 |
| failures | integer | Yes | Number of past failures | 0-3 |
| schoolsup | string | Yes | Extra educational support | "yes", "no" |
| famsup | string | Yes | Family educational support | "yes", "no" |
| paid | string | No | Extra paid classes | "yes", "no" |
| activities | string | No | Extra-curricular activities | "yes", "no" |
| internet | string | Yes | Internet access at home | "yes", "no" |
| romantic | string | Yes | In romantic relationship | "yes", "no" |
| famrel | integer | No | Quality of family relationships | 1-5 |
| freetime | integer | No | Free time after school | 1-5 |
| goout | integer | No | Going out with friends | 1-5 |
| health | integer | Yes | Current health status | 1-5 |
| absences | integer | Yes | Number of school absences | 0-20 |

#### Example Request
```json
{
    "age": 17,
    "sex": "F",
    "address": "U",
    "famsize": "GT3",
    "Medu": 3,
    "Fedu": 2,
    "studytime": 3,
    "failures": 0,
    "schoolsup": "no",
    "famsup": "yes",
    "internet": "yes",
    "romantic": "no",
    "health": 4,
    "absences": 2
}
```

#### Success Response
```json
{
    "prediction": 1,
    "prediction_text": "Pass",
    "probability": {
        "fail": 0.15,
        "pass": 0.85
    },
    "confidence": 0.85,
    "top_factors": [
        {
            "feature": "studytime",
            "importance": 0.245
        },
        {
            "feature": "Fedu",
            "importance": 0.154
        },
        {
            "feature": "Medu",
            "importance": 0.135
        },
        {
            "feature": "failures",
            "importance": 0.090
        },
        {
            "feature": "age",
            "importance": 0.078
        }
    ],
    "status": "success"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| prediction | integer | 0 = Fail, 1 = Pass |
| prediction_text | string | "Pass" or "Fail" |
| probability.fail | float | Probability of failing (0-1) |
| probability.pass | float | Probability of passing (0-1) |
| confidence | float | Highest probability value |
| top_factors | array | Top 5 most important features |
| top_factors[].feature | string | Feature name |
| top_factors[].importance | float | Feature importance score |
| status | string | "success" or "error" |

#### Error Response
```json
{
    "error": "Missing required field: age",
    "status": "error"
}
```

#### Status Codes
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid input data or missing required fields
- `500 Internal Server Error` - Server error during prediction

#### Example Requests

**cURL Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 17,
    "sex": "M",
    "address": "U",
    "famsize": "GT3",
    "Medu": 3,
    "Fedu": 2,
    "studytime": 3,
    "failures": 0,
    "schoolsup": "no",
    "famsup": "yes",
    "internet": "yes",
    "romantic": "no",
    "health": 4,
    "absences": 2
  }'
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/predict"
data = {
    "age": 17,
    "sex": "M",
    "address": "U",
    "famsize": "GT3",
    "Medu": 3,
    "Fedu": 2,
    "studytime": 3,
    "failures": 0,
    "schoolsup": "no",
    "famsup": "yes",
    "internet": "yes",
    "romantic": "no",
    "health": 4,
    "absences": 2
}

response = requests.post(url, json=data)
result = response.json()
print(result)
```

**JavaScript Example:**
```javascript
const url = 'http://localhost:5000/predict';
const data = {
    age: 17,
    sex: 'M',
    address: 'U',
    famsize: 'GT3',
    Medu: 3,
    Fedu: 2,
    studytime: 3,
    failures: 0,
    schoolsup: 'no',
    famsup: 'yes',
    internet: 'yes',
    romantic: 'no',
    health: 4,
    absences: 2
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => console.log(result));
```

---

### 3. Get Feature Information

**GET** `/feature_info`

Returns metadata about all available features, including valid values for categorical features and ranges for numerical features.

#### Response
```json
{
    "categorical_features": {
        "sex": ["M", "F"],
        "address": ["U", "R"],
        "famsize": ["LE3", "GT3"],
        "Pstatus": ["T", "A"],
        "schoolsup": ["yes", "no"],
        "famsup": ["yes", "no"],
        "paid": ["yes", "no"],
        "activities": ["yes", "no"],
        "internet": ["yes", "no"],
        "romantic": ["yes", "no"]
    },
    "numerical_features": {
        "age": {
            "min": 15,
            "max": 19,
            "description": "Student age"
        },
        "Medu": {
            "min": 0,
            "max": 4,
            "description": "Mother education level"
        },
        "Fedu": {
            "min": 0,
            "max": 4,
            "description": "Father education level"
        },
        "studytime": {
            "min": 1,
            "max": 4,
            "description": "Weekly study time"
        },
        "failures": {
            "min": 0,
            "max": 3,
            "description": "Number of past class failures"
        },
        "famrel": {
            "min": 1,
            "max": 5,
            "description": "Quality of family relationships"
        },
        "freetime": {
            "min": 1,
            "max": 5,
            "description": "Free time after school"
        },
        "goout": {
            "min": 1,
            "max": 5,
            "description": "Going out with friends"
        },
        "health": {
            "min": 1,
            "max": 5,
            "description": "Current health status"
        },
        "absences": {
            "min": 0,
            "max": 20,
            "description": "Number of school absences"
        }
    }
}
```

#### Status Codes
- `200 OK` - Feature information retrieved successfully

#### Example Request
```bash
curl -X GET http://localhost:5000/feature_info
```

---

## Feature Encoding Guide

### Categorical Features

#### Sex
- `"M"` - Male
- `"F"` - Female

#### Address
- `"U"` - Urban
- `"R"` - Rural

#### Family Size
- `"LE3"` - Less than or equal to 3 family members
- `"GT3"` - Greater than 3 family members

#### Parent Status
- `"T"` - Parents living together
- `"A"` - Parents living apart

#### Yes/No Features
For features like `schoolsup`, `famsup`, `paid`, `activities`, `internet`, `romantic`:
- `"yes"` - Feature is present/true
- `"no"` - Feature is absent/false

### Numerical Features

#### Education Levels (Medu, Fedu)
- `0` - No education
- `1` - Primary education (4th grade)
- `2` - Primary education (5th to 9th grade)
- `3` - Secondary education
- `4` - Higher education

#### Study Time
- `1` - Less than 2 hours
- `2` - 2 to 5 hours
- `3` - 5 to 10 hours
- `4` - More than 10 hours

#### Scale Features (famrel, freetime, goout, health)
- `1` - Very low
- `2` - Low
- `3` - Medium
- `4` - High
- `5` - Very high

---

## Error Handling

### Common Error Responses

#### Missing Required Fields
```json
{
    "error": "Missing required field: studytime",
    "status": "error"
}
```

#### Invalid Field Values
```json
{
    "error": "Invalid value for 'sex': expected 'M' or 'F'",
    "status": "error"
}
```

#### Server Error
```json
{
    "error": "Internal server error during prediction",
    "status": "error"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Endpoint not found
- `405 Method Not Allowed` - HTTP method not supported
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider implementing rate limiting to prevent abuse.

## CORS Configuration

The API is configured to accept requests from any origin (`*`). For production, update the CORS configuration to only allow specific domains.

## Model Information

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 93.0%
- **Features**: 20 input features
- **Classes**: Binary classification (Pass/Fail)
- **Framework**: Scikit-learn

## Version History

- **v1.0** - Initial release with basic prediction functionality
- **v1.1** - Added feature importance in response
- **v1.2** - Added feature information endpoint

---

For more information, see the main [README.md](README.md) file.