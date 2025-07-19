# Prepare data for machine learning
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Create a copy for processing
data_processed = student_data.copy()

# Encode categorical variables
categorical_columns = ['sex', 'address', 'famsize', 'Pstatus', 'schoolsup', 'famsup', 'paid', 'activities', 'internet', 'romantic']

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    data_processed[col] = le.fit_transform(data_processed[col])
    label_encoders[col] = le

# Prepare features and target
X = data_processed.drop('final_grade', axis=1)
y = data_processed['final_grade']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Random Forest model
print("Training Random Forest model...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2
)

rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Cross-validation
cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5)
print(f"\nCross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10))

# Save the model and encoders
print("\nSaving model and encoders...")
joblib.dump(rf_model, 'student_performance_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

# Save sample data for testing
student_data.to_csv('student_data.csv', index=False)

print("Model training completed and saved!")