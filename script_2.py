# Create the Flask backend API
flask_app_code = '''
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model and encoders
model = joblib.load('student_performance_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

@app.route('/')
def home():
    return jsonify({
        'message': 'Student Performance Prediction API',
        'status': 'Active',
        'version': '1.0'
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Create DataFrame from input data
        input_df = pd.DataFrame([data])
        
        # Encode categorical variables
        categorical_columns = ['sex', 'address', 'famsize', 'Pstatus', 'schoolsup', 
                              'famsup', 'paid', 'activities', 'internet', 'romantic']
        
        for col in categorical_columns:
            if col in input_df.columns:
                # Handle unseen categories by using the most frequent category
                try:
                    input_df[col] = label_encoders[col].transform(input_df[col])
                except ValueError:
                    # If unseen category, use the most frequent encoded value
                    input_df[col] = 0  # Default encoding
        
        # Ensure all required columns are present
        required_columns = ['age', 'sex', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
                           'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities',
                           'internet', 'romantic', 'famrel', 'freetime', 'goout', 'health', 'absences']
        
        for col in required_columns:
            if col not in input_df.columns:
                input_df[col] = 0  # Default value
        
        # Reorder columns to match training data
        input_df = input_df[required_columns]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Get feature importance for explanation
        feature_importance = model.feature_importances_
        feature_names = required_columns
        
        # Create explanation
        top_features = sorted(zip(feature_names, feature_importance), 
                             key=lambda x: x[1], reverse=True)[:5]
        
        result = {
            'prediction': int(prediction),
            'prediction_text': 'Pass' if prediction == 1 else 'Fail',
            'probability': {
                'fail': float(prediction_proba[0]),
                'pass': float(prediction_proba[1])
            },
            'confidence': float(max(prediction_proba)),
            'top_factors': [{'feature': feat, 'importance': float(imp)} 
                           for feat, imp in top_features],
            'status': 'success'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/feature_info', methods=['GET'])
def feature_info():
    """Provide information about features for the frontend"""
    feature_info = {
        'categorical_features': {
            'sex': ['M', 'F'],
            'address': ['U', 'R'],  # Urban, Rural
            'famsize': ['LE3', 'GT3'],  # <=3, >3
            'Pstatus': ['T', 'A'],  # Together, Apart
            'schoolsup': ['yes', 'no'],
            'famsup': ['yes', 'no'],
            'paid': ['yes', 'no'],
            'activities': ['yes', 'no'],
            'internet': ['yes', 'no'],
            'romantic': ['yes', 'no']
        },
        'numerical_features': {
            'age': {'min': 15, 'max': 19, 'description': 'Student age'},
            'Medu': {'min': 0, 'max': 4, 'description': 'Mother education level'},
            'Fedu': {'min': 0, 'max': 4, 'description': 'Father education level'},
            'studytime': {'min': 1, 'max': 4, 'description': 'Weekly study time'},
            'failures': {'min': 0, 'max': 3, 'description': 'Number of past class failures'},
            'famrel': {'min': 1, 'max': 5, 'description': 'Quality of family relationships'},
            'freetime': {'min': 1, 'max': 5, 'description': 'Free time after school'},
            'goout': {'min': 1, 'max': 5, 'description': 'Going out with friends'},
            'health': {'min': 1, 'max': 5, 'description': 'Current health status'},
            'absences': {'min': 0, 'max': 20, 'description': 'Number of school absences'}
        }
    }
    
    return jsonify(feature_info)

if __name__ == '__main__':
    print("Starting Student Performance Prediction API...")
    print("Model loaded successfully!")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

# Save Flask app
with open('app.py', 'w') as f:
    f.write(flask_app_code)

print("Flask backend API created: app.py")