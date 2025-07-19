# Create CSS files for React components

# App.css
app_css = '''
.App {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.App-header {
  text-align: center;
  padding: 30px 20px;
  color: white;
}

.App-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: bold;
}

.App-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.App-main {
  padding: 0 20px 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.App-footer {
  text-align: center;
  padding: 20px;
  color: white;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .container {
    grid-template-columns: 1fr;
  }
  
  .App-header h1 {
    font-size: 2rem;
  }
}
'''

# StudentForm.css
form_css = '''
.form-container {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  height: fit-content;
}

.form-container h2 {
  color: #333;
  margin-bottom: 25px;
  text-align: center;
  font-size: 1.5rem;
}

.student-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.predict-btn {
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
  margin-top: 10px;
}

.predict-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.predict-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
'''

# PredictionResult.css
result_css = '''
.result-container {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  height: fit-content;
}

.result-container h2 {
  color: #333;
  margin-bottom: 25px;
  text-align: center;
  font-size: 1.5rem;
}

.loading {
  text-align: center;
  padding: 40px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background: #ff6b6b;
  color: white;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  margin: 20px 0;
}

.result {
  text-align: center;
  padding: 25px;
  border-radius: 12px;
  margin: 20px 0;
}

.result.pass {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.result.fail {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.result h3 {
  font-size: 2.2rem;
  margin-bottom: 15px;
  font-weight: bold;
}

.probability {
  font-size: 1.3rem;
  margin: 15px 0;
  font-weight: bold;
}

.probability-bars {
  margin: 20px 0;
  text-align: left;
}

.prob-bar {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 12px;
  font-size: 0.9rem;
}

.prob-bar span:first-child {
  min-width: 120px;
  font-weight: bold;
}

.prob-bar span:last-child {
  min-width: 50px;
  font-weight: bold;
}

.bar {
  flex: 1;
  height: 20px;
  background: rgba(255,255,255,0.3);
  border-radius: 10px;
  overflow: hidden;
}

.fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.pass-bar {
  background: #4facfe;
}

.fail-bar {
  background: #fa709a;
}

.factors {
  margin-top: 25px;
  text-align: left;
}

.factors h4 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.2rem;
  font-weight: bold;
}

.factors-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.factor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: rgba(255,255,255,0.2);
  border-radius: 8px;
  font-size: 0.95rem;
}

.factor-name {
  font-weight: 500;
}

.factor-importance {
  font-weight: bold;
  font-size: 1rem;
}

.no-result {
  text-align: center;
  padding: 40px 20px;
  color: #666;
  font-style: italic;
}
'''

# Save CSS files
with open('App.css', 'w') as f:
    f.write(app_css)

with open('StudentForm.css', 'w') as f:
    f.write(form_css)

with open('PredictionResult.css', 'w') as f:
    f.write(result_css)

# Create requirements.txt for Python dependencies
requirements = '''
Flask==2.3.3
Flask-CORS==4.0.0
pandas==2.1.1
numpy==1.24.3
scikit-learn==1.3.0
joblib==1.3.2
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements)

# Create package.json for React dependencies
package_json = '''{
  "name": "student-performance-predictor-frontend",
  "version": "1.0.0",
  "description": "React frontend for Student Performance Predictor ML application",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.4",
    "@testing-library/react": "^13.3.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:5000"
}'''

with open('package.json', 'w') as f:
    f.write(package_json)

print("CSS files and configuration files created:")
print("- App.css")
print("- StudentForm.css") 
print("- PredictionResult.css")
print("- requirements.txt")
print("- package.json")