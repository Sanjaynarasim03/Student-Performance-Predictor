"""
Create the three required datasets for the Student Performance Predictor
- enhanced_student_data.csv: Student records with math scores
- teacher_data.csv: Teacher information  
- school_facilities_data.csv: School facilities data
"""

import pandas as pd
import numpy as np
import random

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

def create_enhanced_student_data():
    """Create enhanced student dataset with math scores and additional features"""
    
    # Load existing student data as base
    existing_data = pd.read_csv('student_data.csv')
    
    # Create enhanced dataset
    n_students = 1000  # Larger dataset for better training
    
    data = {
        'student_id': range(1, n_students + 1),
        'age': np.random.choice(range(15, 20), n_students),
        'sex': np.random.choice(['M', 'F'], n_students),
        'address': np.random.choice(['U', 'R'], n_students, p=[0.7, 0.3]),
        'famsize': np.random.choice(['LE3', 'GT3'], n_students, p=[0.3, 0.7]),
        'Pstatus': np.random.choice(['T', 'A'], n_students, p=[0.85, 0.15]),
        'Medu': np.random.choice(range(0, 5), n_students, p=[0.1, 0.15, 0.25, 0.35, 0.15]),
        'Fedu': np.random.choice(range(0, 5), n_students, p=[0.1, 0.15, 0.25, 0.35, 0.15]),
        'studytime': np.random.choice(range(1, 5), n_students, p=[0.2, 0.4, 0.3, 0.1]),
        'failures': np.random.choice(range(0, 4), n_students, p=[0.6, 0.25, 0.1, 0.05]),
        'schoolsup': np.random.choice(['yes', 'no'], n_students, p=[0.3, 0.7]),
        'famsup': np.random.choice(['yes', 'no'], n_students, p=[0.6, 0.4]),
        'paid': np.random.choice(['yes', 'no'], n_students, p=[0.4, 0.6]),
        'activities': np.random.choice(['yes', 'no'], n_students, p=[0.5, 0.5]),
        'internet': np.random.choice(['yes', 'no'], n_students, p=[0.8, 0.2]),
        'romantic': np.random.choice(['yes', 'no'], n_students, p=[0.35, 0.65]),
        'famrel': np.random.choice(range(1, 6), n_students, p=[0.05, 0.1, 0.2, 0.4, 0.25]),
        'freetime': np.random.choice(range(1, 6), n_students, p=[0.05, 0.1, 0.3, 0.35, 0.2]),
        'goout': np.random.choice(range(1, 6), n_students, p=[0.1, 0.15, 0.3, 0.3, 0.15]),
        'health': np.random.choice(range(1, 6), n_students, p=[0.05, 0.1, 0.2, 0.4, 0.25]),
        'absences': np.random.poisson(3, n_students),  # Poisson distribution for absences
        'teacher_id': np.random.choice(range(1, 51), n_students),  # 50 teachers
        'school_id': np.random.choice(range(1, 11), n_students)    # 10 schools
    }
    
    # Clip absences to reasonable range
    data['absences'] = np.clip(data['absences'], 0, 30)
    
    # Create math scores based on realistic relationships
    math_scores = []
    for i in range(n_students):
        # Base score
        score = 10.0
        
        # Study time impact (strongest predictor)
        score += data['studytime'][i] * 2.5
        
        # Parent education impact
        score += (data['Medu'][i] + data['Fedu'][i]) * 0.8
        
        # Failures impact (negative)
        score -= data['failures'][i] * 2.0
        
        # Age impact (slight positive)
        score += (data['age'][i] - 15) * 0.3
        
        # Health impact
        score += data['health'][i] * 0.4
        
        # Family relationship quality
        score += data['famrel'][i] * 0.3
        
        # Support systems
        if data['famsup'][i] == 'yes':
            score += 1.0
        if data['schoolsup'][i] == 'yes':
            score += 0.8
        if data['internet'][i] == 'yes':
            score += 0.5
        
        # Free time (moderate levels better)
        if data['freetime'][i] == 3:
            score += 0.5
        elif data['freetime'][i] in [1, 5]:
            score -= 0.3
            
        # Going out (moderate levels better)
        if data['goout'][i] <= 2:
            score += 0.3
        elif data['goout'][i] >= 4:
            score -= 0.5
        
        # Absences impact (negative)
        score -= data['absences'][i] * 0.1
        
        # Activities impact (slight positive)
        if data['activities'][i] == 'yes':
            score += 0.3
            
        # Romantic relationship (slight negative during school)
        if data['romantic'][i] == 'yes':
            score -= 0.2
            
        # Urban vs rural
        if data['address'][i] == 'U':
            score += 0.3
            
        # Add some random noise
        score += np.random.normal(0, 1.5)
        
        # Ensure score is in reasonable range (0-20)
        score = max(0, min(20, score))
        math_scores.append(round(score, 2))
    
    data['math_score'] = math_scores
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def create_teacher_data():
    """Create teacher information dataset"""
    
    n_teachers = 50
    
    data = {
        'teacher_id': range(1, n_teachers + 1),
        'teacher_experience': np.random.choice(range(1, 31), n_teachers),  # 1-30 years
        'teacher_education': np.random.choice(['Bachelor', 'Master', 'PhD'], n_teachers, p=[0.3, 0.6, 0.1]),
        'teacher_subject_specialty': np.random.choice(['Math', 'Science', 'Language', 'Social'], n_teachers, p=[0.4, 0.3, 0.2, 0.1]),
        'teacher_rating': np.random.normal(4.0, 0.8, n_teachers),  # Rating out of 5
        'class_size': np.random.choice(range(20, 36), n_teachers),  # Class size 20-35
        'teaching_method': np.random.choice(['Traditional', 'Interactive', 'Mixed'], n_teachers, p=[0.3, 0.4, 0.3])
    }
    
    # Clip teacher rating to 1-5 range
    data['teacher_rating'] = np.clip(data['teacher_rating'], 1.0, 5.0)
    data['teacher_rating'] = np.round(data['teacher_rating'], 2)
    
    df = pd.DataFrame(data)
    return df

def create_school_facilities_data():
    """Create school facilities dataset"""
    
    n_schools = 10
    
    data = {
        'school_id': range(1, n_schools + 1),
        'school_type': np.random.choice(['Public', 'Private'], n_schools, p=[0.7, 0.3]),
        'school_size': np.random.choice(['Small', 'Medium', 'Large'], n_schools, p=[0.3, 0.5, 0.2]),
        'library_quality': np.random.choice(range(1, 6), n_schools),  # 1-5 rating
        'computer_lab': np.random.choice(['yes', 'no'], n_schools, p=[0.8, 0.2]),
        'science_lab': np.random.choice(['yes', 'no'], n_schools, p=[0.9, 0.1]),
        'sports_facilities': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], n_schools, p=[0.2, 0.4, 0.3, 0.1]),
        'student_teacher_ratio': np.random.normal(25, 5, n_schools),  # Average ratio around 25
        'school_budget_per_student': np.random.normal(5000, 1500, n_schools),  # Budget in dollars
        'internet_speed': np.random.choice(['High', 'Medium', 'Low'], n_schools, p=[0.4, 0.4, 0.2]),
        'building_condition': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], n_schools, p=[0.2, 0.5, 0.2, 0.1])
    }
    
    # Round numerical values
    data['student_teacher_ratio'] = np.round(np.clip(data['student_teacher_ratio'], 15, 40), 1)
    data['school_budget_per_student'] = np.round(np.clip(data['school_budget_per_student'], 2000, 10000), 0)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Creating enhanced student dataset...")
    student_df = create_enhanced_student_data()
    student_df.to_csv('enhanced_student_data.csv', index=False)
    print(f"Created enhanced_student_data.csv with {len(student_df)} records")
    
    print("Creating teacher dataset...")
    teacher_df = create_teacher_data()
    teacher_df.to_csv('teacher_data.csv', index=False)
    print(f"Created teacher_data.csv with {len(teacher_df)} records")
    
    print("Creating school facilities dataset...")
    school_df = create_school_facilities_data()
    school_df.to_csv('school_facilities_data.csv', index=False)
    print(f"Created school_facilities_data.csv with {len(school_df)} records")
    
    print("\nDataset creation completed!")
    print("\nSample data preview:")
    print("\nEnhanced Student Data:")
    print(student_df.head())
    print("\nTeacher Data:")
    print(teacher_df.head())
    print("\nSchool Facilities Data:")
    print(school_df.head())