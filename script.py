# Let's start by creating the project structure and generating sample data
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic student performance dataset
def generate_student_data(n_students=1000):
    """Generate synthetic student performance dataset"""
    
    # Student demographics
    ages = np.random.choice([15, 16, 17, 18, 19], size=n_students, p=[0.1, 0.25, 0.3, 0.25, 0.1])
    genders = np.random.choice(['M', 'F'], size=n_students, p=[0.52, 0.48])
    addresses = np.random.choice(['U', 'R'], size=n_students, p=[0.7, 0.3])
    
    # Family background
    family_sizes = np.random.choice(['LE3', 'GT3'], size=n_students, p=[0.3, 0.7])
    parent_status = np.random.choice(['T', 'A'], size=n_students, p=[0.85, 0.15])
    mother_edu = np.random.choice([0, 1, 2, 3, 4], size=n_students, p=[0.1, 0.15, 0.25, 0.3, 0.2])
    father_edu = np.random.choice([0, 1, 2, 3, 4], size=n_students, p=[0.12, 0.18, 0.25, 0.28, 0.17])
    
    # Study habits and environment
    study_time = np.random.choice([1, 2, 3, 4], size=n_students, p=[0.2, 0.4, 0.25, 0.15])
    failures = np.random.choice([0, 1, 2, 3], size=n_students, p=[0.6, 0.25, 0.1, 0.05])
    school_support = np.random.choice(['yes', 'no'], size=n_students, p=[0.3, 0.7])
    family_support = np.random.choice(['yes', 'no'], size=n_students, p=[0.7, 0.3])
    paid_classes = np.random.choice(['yes', 'no'], size=n_students, p=[0.4, 0.6])
    activities = np.random.choice(['yes', 'no'], size=n_students, p=[0.5, 0.5])
    
    # Social and health factors
    internet = np.random.choice(['yes', 'no'], size=n_students, p=[0.8, 0.2])
    romantic = np.random.choice(['yes', 'no'], size=n_students, p=[0.35, 0.65])
    family_quality = np.random.choice([1, 2, 3, 4, 5], size=n_students, p=[0.05, 0.1, 0.2, 0.4, 0.25])
    freetime = np.random.choice([1, 2, 3, 4, 5], size=n_students, p=[0.1, 0.2, 0.4, 0.2, 0.1])
    go_out = np.random.choice([1, 2, 3, 4, 5], size=n_students, p=[0.15, 0.25, 0.35, 0.15, 0.1])
    health = np.random.choice([1, 2, 3, 4, 5], size=n_students, p=[0.05, 0.1, 0.25, 0.35, 0.25])
    absences = np.random.poisson(5, n_students)
    
    # Create performance score based on weighted factors
    performance_score = (
        (5 - ages + 15) * 0.1 +  # Younger students might perform better
        (mother_edu + father_edu) * 0.15 +  # Parent education impact
        study_time * 0.25 +  # Study time has high impact
        (4 - failures) * 0.2 +  # Past failures negatively impact
        (school_support == 'yes') * 0.05 +
        (family_support == 'yes') * 0.1 +
        (internet == 'yes') * 0.05 +
        family_quality * 0.05 +
        health * 0.03 +
        np.random.normal(0, 1, n_students) * 0.1  # Random noise
    )
    
    # Convert to pass/fail (binary classification)
    # Students with score > median pass (1), others fail (0)
    median_score = np.median(performance_score)
    final_grade = (performance_score > median_score).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'age': ages,
        'sex': genders,
        'address': addresses,
        'famsize': family_sizes,
        'Pstatus': parent_status,
        'Medu': mother_edu,
        'Fedu': father_edu,
        'studytime': study_time,
        'failures': failures,
        'schoolsup': school_support,
        'famsup': family_support,
        'paid': paid_classes,
        'activities': activities,
        'internet': internet,
        'romantic': romantic,
        'famrel': family_quality,
        'freetime': freetime,
        'goout': go_out,
        'health': health,
        'absences': absences,
        'final_grade': final_grade
    })
    
    return data

# Generate the dataset
print("Generating student performance dataset...")
student_data = generate_student_data(1000)
print(f"Dataset shape: {student_data.shape}")
print("\nDataset info:")
print(student_data.head())
print("\nTarget variable distribution:")
print(student_data['final_grade'].value_counts())