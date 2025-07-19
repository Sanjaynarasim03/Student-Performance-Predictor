# 🎓 Student Performance Predictor -  ML Project

A comprehensive full-stack machine learning application that predicts student academic performance based on demographic, social, and educational factors using Python, Flask, and React/HTML.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

## 🌟 Project Overview

This project demonstrates a complete end-to-end machine learning workflow, from data generation and model training to full-stack web deployment. It predicts whether a student will pass or fail based on various personal, family, and academic factors.

### Key Features

- **🤖 Machine Learning Model**: Random Forest classifier with 93% accuracy
- **🔧 Flask Backend API**: RESTful API for model inference
- **🌐 Frontend Options**: Both React and HTML/CSS/JS implementations
- **📊 Feature Importance Analysis**: Explains prediction factors
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🚀 Easy Deployment**: Docker-ready configuration
- **📚 Complete Documentation**: Comprehensive setup and usage guides

## 🏗️ Project Structure

```
student-performance-predictor/
│
├── backend/
│   ├── app.py                     # Flask API server
│   ├── student_performance_model.pkl  # Trained ML model
│   ├── label_encoders.pkl         # Categorical encoders
│   ├── student_data.csv           # Sample dataset
│   └── requirements.txt           # Python dependencies
│
├── frontend/
│   ├── html-version/
│   │   └── index.html            # Standalone HTML app
│   │
│   └── react-version/
│       ├── src/
│       │   ├── App.js            # Main React component
│       │   ├── App.css           # App styles
│       │   ├── components/
│       │   │   ├── StudentForm.js
│       │   │   ├── StudentForm.css
│       │   │   ├── PredictionResult.js
│       │   │   └── PredictionResult.css
│       │   └── index.js          # React entry point
│       └── package.json          # Node.js dependencies
│
├── notebooks/
│   └── model_training.ipynb      # Jupyter notebook for EDA and training
│
├── docs/
│   ├── API_DOCUMENTATION.md      # API reference
│   ├── DEPLOYMENT_GUIDE.md       # Deployment instructions
│   └── MODEL_DOCUMENTATION.md    # Model details and performance
│
├── tests/
│   ├── test_api.py               # API tests
│   └── test_model.py             # Model tests
│
├── docker/
│   ├── Dockerfile                # Docker configuration
│   └── docker-compose.yml        # Multi-service setup
│
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+ (for React version)
- pip (Python package manager)
- npm or yarn (for React dependencies)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student-performance-predictor.git
cd student-performance-predictor
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the Flask API**
```bash
python app.py
```

The API will be running at `http://localhost:5000`

### Frontend Setup

#### Option 1: HTML Version (Simple)
1. Open `index.html` in your browser
2. Make sure the Flask API is running on port 5000

#### Option 2: React Version (Advanced)
1. **Navigate to React directory**
```bash
cd frontend/react-version
```

2. **Install Node.js dependencies**
```bash
npm install
```

3. **Start React development server**
```bash
npm start
```

The React app will be running at `http://localhost:3000`

## 📖 Usage Guide

### Making Predictions

1. **Start the backend API** (Flask server on port 5000)
2. **Open the frontend** (either HTML file or React app)
3. **Fill in the student information form**:
   - **Demographics**: Age, gender, address type
   - **Family Background**: Family size, parent education levels
   - **Academic**: Study time, past failures, school support
   - **Social**: Internet access, relationships, health status
   - **Attendance**: Number of absences

4. **Click "Predict Performance"** to get results
5. **View the prediction** with confidence score and contributing factors

### API Endpoints

#### GET `/`
Returns API status and information.

#### POST `/predict`
Predicts student performance based on input features.

**Request Body:**
```json
{
    "age": 17,
    "sex": "M",
    "address": "U",
    "famsize": "GT3",
    "Medu": 3,
    "Fedu": 2,
    "studytime": 2,
    "failures": 0,
    "schoolsup": "no",
    "famsup": "yes",
    "internet": "yes",
    "romantic": "no",
    "health": 4,
    "absences": 2
}
```

**Response:**
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
        {"feature": "studytime", "importance": 0.245},
        {"feature": "Fedu", "importance": 0.154}
    ],
    "status": "success"
}
```

#### GET `/feature_info`
Returns information about available features and their valid values.

## 🔧 Model Information

### Algorithm: Random Forest Classifier

**Performance Metrics:**
- **Accuracy**: 93.0%
- **Precision**: 93%
- **Recall**: 93%
- **F1-Score**: 93%
- **Cross-validation Score**: 86.5% ± 3.0%

### Top Contributing Features

1. **Study Time** (24.5%) - Weekly study time allocation
2. **Father Education** (15.4%) - Father's education level
3. **Mother Education** (13.5%) - Mother's education level
4. **Past Failures** (9.0%) - Number of previous academic failures
5. **Age** (7.8%) - Student's age

### Feature Descriptions

| Feature | Type | Description | Values |
|---------|------|-------------|---------|
| age | Numeric | Student's age | 15-19 |
| sex | Categorical | Student's gender | M/F |
| address | Categorical | Home address type | U (urban) / R (rural) |
| famsize | Categorical | Family size | LE3 (≤3) / GT3 (>3) |
| Pstatus | Categorical | Parent's cohabitation | T (together) / A (apart) |
| Medu | Numeric | Mother's education | 0-4 |
| Fedu | Numeric | Father's education | 0-4 |
| studytime | Numeric | Weekly study time | 1-4 |
| failures | Numeric | Past class failures | 0-3 |
| schoolsup | Categorical | Extra educational support | yes/no |
| famsup | Categorical | Family educational support | yes/no |
| paid | Categorical | Extra paid classes | yes/no |
| activities | Categorical | Extra-curricular activities | yes/no |
| internet | Categorical | Internet access at home | yes/no |
| romantic | Categorical | In romantic relationship | yes/no |
| famrel | Numeric | Quality of family relationships | 1-5 |
| freetime | Numeric | Free time after school | 1-5 |
| goout | Numeric | Going out with friends | 1-5 |
| health | Numeric | Current health status | 1-5 |
| absences | Numeric | Number of school absences | 0-20 |

## 🧪 Testing

### Run Backend Tests
```bash
pytest tests/test_api.py -v
pytest tests/test_model.py -v
```

### Test API Endpoints
```bash
# Test health check
curl http://localhost:5000/

# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 17, "sex": "M", "studytime": 3, "failures": 0, "health": 4, "absences": 2}'
```

## 🚀 Deployment

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Cloud Deployment Options

1. **Heroku** - See `docs/DEPLOYMENT_GUIDE.md`
2. **AWS EC2** - See `docs/DEPLOYMENT_GUIDE.md`
3. **Google Cloud Platform** - See `docs/DEPLOYMENT_GUIDE.md`

## 📊 Development Workflow

### Data Science Workflow
1. **Data Collection** - Generated synthetic student dataset
2. **Exploratory Data Analysis** - Feature correlation and distribution analysis
3. **Data Preprocessing** - Label encoding, train-test split
4. **Model Training** - Random Forest with hyperparameter tuning
5. **Model Evaluation** - Cross-validation and performance metrics
6. **Model Serialization** - Saved using joblib for deployment

### Software Development Workflow
1. **Backend Development** - Flask API with CORS support
2. **Frontend Development** - React components and HTML interface
3. **Testing** - Unit tests for API and model functionality
4. **Documentation** - Comprehensive README and API docs
5. **Containerization** - Docker configuration for easy deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Add tests for new features
- Update documentation for any API changes
- Use conventional commit messages

## 🐛 Troubleshooting

### Common Issues

1. **CORS Error**: Make sure Flask-CORS is installed and configured
2. **Model Loading Error**: Ensure model files are in the correct directory
3. **Port Conflicts**: Change default ports in configuration files
4. **Package Version Issues**: Use exact versions from requirements.txt

### Support

- Create an issue on GitHub
- Check existing issues for solutions
- Review the API documentation
- Verify your environment setup

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **UCI Machine Learning Repository** - Inspiration for student performance datasets
- **Scikit-learn Community** - Excellent machine learning library
- **Flask Community** - Lightweight and powerful web framework
- **React Community** - Modern frontend development framework

## 📈 Future Enhancements

- [ ] Add more sophisticated ML models (XGBoost, Neural Networks)
- [ ] Implement real-time model updating
- [ ] Add data visualization dashboards
- [ ] Create mobile app versions
- [ ] Implement user authentication and data persistence
- [ ] Add multi-language support
- [ ] Integrate with educational platforms APIs
- [ ] Add batch prediction capabilities

## 📞 Contact

- **Author**: Sanjay Narasimhan


---

⭐ If you found this project helpful, please give it a star on GitHub!

Made with ❤️ and ☕ by passionate developers
