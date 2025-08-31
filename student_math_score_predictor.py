"""
End-to-End Machine Learning Solution for Student Math Score Prediction

This script implements a comprehensive regression pipeline to predict student math scores
using three datasets: student records, teacher information, and school facilities.

Author: AI Assistant
Date: 2024
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Try to import additional ensemble methods
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

def load_and_join_datasets():
    """
    Load the three datasets and join them using teacher_id and school_id keys.
    
    Returns:
        pd.DataFrame: Combined dataset ready for analysis
    """
    print("📊 Loading datasets...")
    
    # Load datasets
    student_data = pd.read_csv('enhanced_student_data.csv')
    teacher_data = pd.read_csv('teacher_data.csv')
    school_data = pd.read_csv('school_facilities_data.csv')
    
    print(f"✅ Student data: {len(student_data)} records")
    print(f"✅ Teacher data: {len(teacher_data)} records")
    print(f"✅ School data: {len(school_data)} records")
    
    # Join datasets
    print("🔗 Joining datasets...")
    
    # First join with teacher data
    combined_data = student_data.merge(teacher_data, on='teacher_id', how='left')
    print(f"After teacher join: {len(combined_data)} records")
    
    # Then join with school data
    combined_data = combined_data.merge(school_data, on='school_id', how='left')
    print(f"After school join: {len(combined_data)} records")
    
    # Check for missing values after joins
    missing_after_join = combined_data.isnull().sum().sum()
    if missing_after_join > 0:
        print(f"⚠️  Missing values after joins: {missing_after_join}")
    else:
        print("✅ No missing values after joins")
    
    return combined_data

def preprocess_data(data):
    """
    Comprehensive data preprocessing including:
    - Missing data handling
    - Categorical encoding
    - Feature scaling
    - Feature engineering
    
    Args:
        data (pd.DataFrame): Raw combined dataset
        
    Returns:
        tuple: (X_processed, y, feature_names, preprocessor)
    """
    print("\n🔧 Starting data preprocessing...")
    
    # Make a copy to avoid modifying original data
    df = data.copy()
    
    # Separate target variable
    y = df['math_score']
    X = df.drop(['math_score', 'student_id'], axis=1)  # Remove ID column
    
    print(f"Target variable stats: Mean={y.mean():.2f}, Std={y.std():.2f}, Range=[{y.min():.2f}, {y.max():.2f}]")
    
    # Handle missing values (fill with median for numerical, mode for categorical)
    print("🔨 Handling missing values...")
    for col in X.columns:
        if X[col].dtype in ['object']:
            # Categorical: fill with mode
            mode_value = X[col].mode()[0] if not X[col].mode().empty else 'unknown'
            X[col] = X[col].fillna(mode_value)
        else:
            # Numerical: fill with median
            X[col] = X[col].fillna(X[col].median())
    
    # Identify categorical and numerical columns
    categorical_columns = X.select_dtypes(include=['object']).columns.tolist()
    numerical_columns = X.select_dtypes(exclude=['object']).columns.tolist()
    
    print(f"📋 Categorical features ({len(categorical_columns)}): {categorical_columns[:5]}...")
    print(f"📋 Numerical features ({len(numerical_columns)}): {numerical_columns[:5]}...")
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_columns),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_columns)
        ]
    )
    
    # Apply preprocessing
    X_processed = preprocessor.fit_transform(X)
    
    # Get feature names after preprocessing
    num_feature_names = numerical_columns
    cat_feature_names = []
    
    # Get categorical feature names after one-hot encoding
    if hasattr(preprocessor.named_transformers_['cat'], 'get_feature_names_out'):
        cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_columns).tolist()
    else:
        # Fallback for older sklearn versions
        cat_feature_names = [f"{col}_{val}" for col in categorical_columns 
                           for val in preprocessor.named_transformers_['cat'].categories_[categorical_columns.tolist().index(col)][1:]]
    
    feature_names = num_feature_names + cat_feature_names
    
    print(f"✅ Preprocessing completed. Final feature count: {X_processed.shape[1]}")
    
    return X_processed, y, feature_names, preprocessor

def engineer_features(X, feature_names):
    """
    Create additional engineered features including interaction features.
    
    Args:
        X (np.array): Processed feature matrix
        feature_names (list): Names of features
        
    Returns:
        tuple: (X_engineered, engineered_feature_names)
    """
    print("\n⚙️ Engineering additional features...")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(X, columns=feature_names)
    
    # Create interaction features between important variables
    interaction_features = []
    interaction_names = []
    
    # Define key features for interactions (first few are most likely to be important)
    key_features = ['studytime', 'age', 'failures', 'absences', 'teacher_experience', 'teacher_rating']
    key_features = [f for f in key_features if f in df.columns]
    
    # Create pairwise interactions between key features
    for i, feat1 in enumerate(key_features):
        for feat2 in key_features[i+1:]:
            interaction = df[feat1] * df[feat2]
            interaction_features.append(interaction)
            interaction_names.append(f"{feat1}_x_{feat2}")
    
    # Create polynomial features for key numerical features
    poly_features = []
    poly_names = []
    
    for feat in key_features[:3]:  # Limit to top 3 to avoid feature explosion
        if feat in df.columns:
            squared = df[feat] ** 2
            poly_features.append(squared)
            poly_names.append(f"{feat}_squared")
    
    # Combine all features
    if interaction_features or poly_features:
        all_new_features = interaction_features + poly_features
        all_new_names = interaction_names + poly_names
        
        new_features_df = pd.DataFrame(np.column_stack(all_new_features), columns=all_new_names)
        engineered_df = pd.concat([df, new_features_df], axis=1)
        
        print(f"✅ Added {len(all_new_features)} engineered features")
        return engineered_df.values, engineered_df.columns.tolist()
    else:
        print("⚠️  No additional features engineered")
        return X, feature_names

def select_features(X, y, feature_names, k=50):
    """
    Select the most important features using statistical tests.
    
    Args:
        X (np.array): Feature matrix
        y (np.array): Target variable
        feature_names (list): Feature names
        k (int): Number of features to select
        
    Returns:
        tuple: (X_selected, selected_feature_names, selector)
    """
    print(f"\n🎯 Selecting top {k} features...")
    
    # Use SelectKBest with f_regression for feature selection
    k = min(k, X.shape[1])  # Ensure k doesn't exceed number of features
    selector = SelectKBest(score_func=f_regression, k=k)
    X_selected = selector.fit_transform(X, y)
    
    # Get selected feature names
    selected_indices = selector.get_support(indices=True)
    selected_feature_names = [feature_names[i] for i in selected_indices]
    
    print(f"✅ Selected {len(selected_feature_names)} features")
    print(f"📊 Feature selection scores range: [{selector.scores_.min():.2f}, {selector.scores_.max():.2f}]")
    
    return X_selected, selected_feature_names, selector

def train_models(X_train, X_test, y_train, y_test, feature_names):
    """
    Train multiple regression models and compare their performance.
    
    Args:
        X_train, X_test: Training and test features
        y_train, y_test: Training and test targets
        feature_names: List of feature names
        
    Returns:
        dict: Dictionary of trained models with their performance metrics
    """
    print("\n🚀 Training multiple regression models...")
    
    models = {}
    results = {}
    
    # 1. Random Forest Regressor
    print("🌳 Training Random Forest...")
    rf_params = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [5, 10],
        'min_samples_leaf': [2, 4]
    }
    rf = RandomForestRegressor(random_state=42)
    rf_grid = GridSearchCV(rf, rf_params, cv=5, scoring='r2', n_jobs=-1, verbose=0)
    rf_grid.fit(X_train, y_train)
    models['Random Forest'] = rf_grid.best_estimator_
    
    # 2. Gradient Boosting Regressor
    print("📈 Training Gradient Boosting...")
    gb_params = {
        'n_estimators': [100, 150],
        'learning_rate': [0.1, 0.15],
        'max_depth': [3, 5],
        'min_samples_split': [5, 10]
    }
    gb = GradientBoostingRegressor(random_state=42)
    gb_grid = GridSearchCV(gb, gb_params, cv=5, scoring='r2', n_jobs=-1, verbose=0)
    gb_grid.fit(X_train, y_train)
    models['Gradient Boosting'] = gb_grid.best_estimator_
    
    # 3. Linear Regression
    print("📏 Training Linear Regression...")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    models['Linear Regression'] = lr
    
    # 4. Ridge Regression
    print("🏔️ Training Ridge Regression...")
    ridge_params = {'alpha': [0.1, 1.0, 10.0, 100.0]}
    ridge = Ridge(random_state=42)
    ridge_grid = GridSearchCV(ridge, ridge_params, cv=5, scoring='r2', verbose=0)
    ridge_grid.fit(X_train, y_train)
    models['Ridge'] = ridge_grid.best_estimator_
    
    # 5. Lasso Regression
    print("🪢 Training Lasso Regression...")
    lasso_params = {'alpha': [0.1, 1.0, 10.0]}
    lasso = Lasso(random_state=42)
    lasso_grid = GridSearchCV(lasso, lasso_params, cv=5, scoring='r2', verbose=0)
    lasso_grid.fit(X_train, y_train)
    models['Lasso'] = lasso_grid.best_estimator_
    
    # 6. ElasticNet Regression
    print("🕸️ Training ElasticNet...")
    elastic_params = {'alpha': [0.1, 1.0], 'l1_ratio': [0.1, 0.5, 0.9]}
    elastic = ElasticNet(random_state=42)
    elastic_grid = GridSearchCV(elastic, elastic_params, cv=5, scoring='r2', verbose=0)
    elastic_grid.fit(X_train, y_train)
    models['ElasticNet'] = elastic_grid.best_estimator_
    
    # 7. XGBoost (if available)
    if XGBOOST_AVAILABLE:
        print("🚀 Training XGBoost...")
        xgb_params = {
            'n_estimators': [100, 150],
            'learning_rate': [0.1, 0.15],
            'max_depth': [3, 5]
        }
        xgb_model = xgb.XGBRegressor(random_state=42)
        xgb_grid = GridSearchCV(xgb_model, xgb_params, cv=5, scoring='r2', n_jobs=-1, verbose=0)
        xgb_grid.fit(X_train, y_train)
        models['XGBoost'] = xgb_grid.best_estimator_
    
    # 8. LightGBM (if available)
    if LIGHTGBM_AVAILABLE:
        print("💡 Training LightGBM...")
        lgb_params = {
            'n_estimators': [100, 150],
            'learning_rate': [0.1, 0.15],
            'max_depth': [3, 5]
        }
        lgb_model = lgb.LGBMRegressor(random_state=42, verbose=-1)
        lgb_grid = GridSearchCV(lgb_model, lgb_params, cv=5, scoring='r2', n_jobs=-1, verbose=0)
        lgb_grid.fit(X_train, y_train)
        models['LightGBM'] = lgb_grid.best_estimator_
    
    # Evaluate all models
    print("\n📊 Evaluating models...")
    for name, model in models.items():
        # Cross-validation scores
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        # Test set predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'cv_r2_mean': cv_scores.mean(),
            'cv_r2_std': cv_scores.std(),
            'test_r2': r2,
            'test_rmse': rmse,
            'test_mae': mae,
            'y_pred': y_pred
        }
        
        print(f"  {name:18} | CV R²: {cv_scores.mean():.4f} (±{cv_scores.std():.4f}) | Test R²: {r2:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f}")
    
    return results

def get_feature_importance(best_model, feature_names, top_n=15):
    """
    Extract and display feature importance from the best model.
    
    Args:
        best_model: Trained model
        feature_names: List of feature names
        top_n: Number of top features to display
        
    Returns:
        pd.DataFrame: Feature importance dataframe
    """
    print(f"\n🎯 Feature Importance Analysis (Top {top_n}):")
    
    # Get feature importance based on model type
    if hasattr(best_model, 'feature_importances_'):
        # Tree-based models
        importance_scores = best_model.feature_importances_
    elif hasattr(best_model, 'coef_'):
        # Linear models
        importance_scores = np.abs(best_model.coef_)
    else:
        print("⚠️  Model doesn't support feature importance extraction")
        return None
    
    # Create feature importance dataframe
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': importance_scores
    }).sort_values('importance', ascending=False)
    
    # Display top features
    print(feature_importance.head(top_n).to_string(index=False))
    
    return feature_importance

def main():
    """
    Main function to execute the complete ML pipeline.
    """
    print("🎓 Student Math Score Prediction - End-to-End ML Solution")
    print("=" * 60)
    
    # 1. Load and join datasets
    combined_data = load_and_join_datasets()
    
    # 2. Data preprocessing
    X_processed, y, feature_names, preprocessor = preprocess_data(combined_data)
    
    # 3. Feature engineering
    X_engineered, engineered_feature_names = engineer_features(X_processed, feature_names)
    
    # 4. Feature selection
    X_selected, selected_feature_names, feature_selector = select_features(
        X_engineered, y, engineered_feature_names, k=50
    )
    
    # 5. Train-test split
    print("\n🔀 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y, test_size=0.2, random_state=42
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # 6. Train multiple models
    results = train_models(X_train, X_test, y_train, y_test, selected_feature_names)
    
    # 7. Select best model
    print("\n🏆 Best Model Selection:")
    best_model_name = max(results.keys(), key=lambda k: results[k]['test_r2'])
    best_result = results[best_model_name]
    best_model = best_result['model']
    
    print(f"🥇 Best Model: {best_model_name}")
    print(f"   📊 Test R² Score: {best_result['test_r2']:.4f}")
    print(f"   📊 Test RMSE: {best_result['test_rmse']:.4f}")
    print(f"   📊 Test MAE: {best_result['test_mae']:.4f}")
    print(f"   📊 CV R² Score: {best_result['cv_r2_mean']:.4f} (±{best_result['cv_r2_std']:.4f})")
    
    # 8. Feature importance analysis
    feature_importance_df = get_feature_importance(best_model, selected_feature_names)
    
    # 9. Save the best model and preprocessing components
    print("\n💾 Saving model and components...")
    
    # Save the complete pipeline
    pipeline_components = {
        'preprocessor': preprocessor,
        'feature_selector': feature_selector,
        'model': best_model,
        'selected_features': selected_feature_names,
        'model_name': best_model_name,
        'metrics': {
            'test_r2': best_result['test_r2'],
            'test_rmse': best_result['test_rmse'],
            'test_mae': best_result['test_mae'],
            'cv_r2_mean': best_result['cv_r2_mean'],
            'cv_r2_std': best_result['cv_r2_std']
        }
    }
    
    joblib.dump(pipeline_components, 'best_regression_model_pipeline.pkl')
    
    # Save feature importance
    if feature_importance_df is not None:
        feature_importance_df.to_csv('feature_importance.csv', index=False)
    
    # Save detailed results
    results_summary = pd.DataFrame({
        'Model': list(results.keys()),
        'CV_R2_Mean': [results[k]['cv_r2_mean'] for k in results.keys()],
        'CV_R2_Std': [results[k]['cv_r2_std'] for k in results.keys()],
        'Test_R2': [results[k]['test_r2'] for k in results.keys()],
        'Test_RMSE': [results[k]['test_rmse'] for k in results.keys()],
        'Test_MAE': [results[k]['test_mae'] for k in results.keys()]
    }).sort_values('Test_R2', ascending=False)
    
    results_summary.to_csv('model_comparison_results.csv', index=False)
    
    print("✅ Model and components saved successfully!")
    print(f"   📁 best_regression_model_pipeline.pkl")
    print(f"   📁 feature_importance.csv")
    print(f"   📁 model_comparison_results.csv")
    
    # 10. Final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL RESULTS SUMMARY")
    print("=" * 60)
    print(f"🏆 Best Model: {best_model_name}")
    print(f"📊 R² Score: {best_result['test_r2']:.4f}")
    print(f"📊 RMSE: {best_result['test_rmse']:.4f}")
    print(f"📊 MAE: {best_result['test_mae']:.4f}")
    print(f"🔄 Cross-validation R²: {best_result['cv_r2_mean']:.4f} (±{best_result['cv_r2_std']:.4f})")
    print(f"🎯 Total Features Used: {len(selected_feature_names)}")
    print(f"📁 All results saved to files")
    
    return pipeline_components, results

if __name__ == "__main__":
    # Execute the complete pipeline
    pipeline, all_results = main()