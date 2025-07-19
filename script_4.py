# Create React frontend components

# Main App.js
app_js = '''
import React, { useState } from 'react';
import StudentForm from './components/StudentForm';
import PredictionResult from './components/PredictionResult';
import './App.css';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePrediction = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction');
      }

      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 Student Performance Predictor</h1>
        <p>AI-powered prediction system to forecast student academic success</p>
      </header>
      
      <main className="App-main">
        <div className="container">
          <StudentForm 
            onSubmit={handlePrediction} 
            loading={loading} 
          />
          <PredictionResult 
            prediction={prediction}
            loading={loading}
            error={error}
          />
        </div>
      </main>
      
      <footer className="App-footer">
        <p>Built with React, Flask, and Machine Learning</p>
      </footer>
    </div>
  );
}

export default App;
'''

# StudentForm component
student_form = '''
import React, { useState } from 'react';
import './StudentForm.css';

const StudentForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    age: 17,
    sex: 'M',
    address: 'U',
    famsize: 'GT3',
    Pstatus: 'T',
    Medu: 2,
    Fedu: 2,
    studytime: 2,
    failures: 0,
    schoolsup: 'no',
    famsup: 'yes',
    paid: 'no',
    activities: 'yes',
    internet: 'yes',
    romantic: 'no',
    famrel: 4,
    freetime: 3,
    goout: 3,
    health: 4,
    absences: 2
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: ['age', 'Medu', 'Fedu', 'studytime', 'failures', 'famrel', 'freetime', 'goout', 'health', 'absences'].includes(name) 
        ? parseInt(value) 
        : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="form-container">
      <h2>Student Information</h2>
      <form onSubmit={handleSubmit} className="student-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="age">Age</label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              min="15"
              max="19"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="sex">Gender</label>
            <select
              id="sex"
              name="sex"
              value={formData.sex}
              onChange={handleChange}
              required
            >
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="address">Address Type</label>
            <select
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              required
            >
              <option value="U">Urban</option>
              <option value="R">Rural</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="famsize">Family Size</label>
            <select
              id="famsize"
              name="famsize"
              value={formData.famsize}
              onChange={handleChange}
              required
            >
              <option value="LE3">≤ 3 members</option>
              <option value="GT3">> 3 members</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="Medu">Mother's Education (0-4)</label>
            <input
              type="number"
              id="Medu"
              name="Medu"
              value={formData.Medu}
              onChange={handleChange}
              min="0"
              max="4"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="Fedu">Father's Education (0-4)</label>
            <input
              type="number"
              id="Fedu"
              name="Fedu"
              value={formData.Fedu}
              onChange={handleChange}
              min="0"
              max="4"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="studytime">Study Time (1-4)</label>
            <select
              id="studytime"
              name="studytime"
              value={formData.studytime}
              onChange={handleChange}
              required
            >
              <option value={1}>< 2 hours</option>
              <option value={2}>2 to 5 hours</option>
              <option value={3}>5 to 10 hours</option>
              <option value={4}>> 10 hours</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="failures">Past Failures</label>
            <input
              type="number"
              id="failures"
              name="failures"
              value={formData.failures}
              onChange={handleChange}
              min="0"
              max="3"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="health">Health Status (1-5)</label>
            <input
              type="number"
              id="health"
              name="health"
              value={formData.health}
              onChange={handleChange}
              min="1"
              max="5"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="absences">School Absences</label>
            <input
              type="number"
              id="absences"
              name="absences"
              value={formData.absences}
              onChange={handleChange}
              min="0"
              max="20"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="internet">Internet Access</label>
            <select
              id="internet"
              name="internet"
              value={formData.internet}
              onChange={handleChange}
              required
            >
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="famsup">Family Support</label>
            <select
              id="famsup"
              name="famsup"
              value={formData.famsup}
              onChange={handleChange}
              required
            >
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          className="predict-btn"
          disabled={loading}
        >
          {loading ? 'Predicting...' : 'Predict Performance'}
        </button>
      </form>
    </div>
  );
};

export default StudentForm;
'''

# PredictionResult component
prediction_result = '''
import React from 'react';
import './PredictionResult.css';

const PredictionResult = ({ prediction, loading, error }) => {
  const formatFeatureName = (feature) => {
    const featureNames = {
      'age': 'Age',
      'sex': 'Gender',
      'address': 'Address Type',
      'famsize': 'Family Size',
      'Pstatus': 'Parents Status',
      'Medu': 'Mother Education',
      'Fedu': 'Father Education',
      'studytime': 'Study Time',
      'failures': 'Past Failures',
      'schoolsup': 'School Support',
      'famsup': 'Family Support',
      'paid': 'Extra Paid Classes',
      'activities': 'Extra Activities',
      'internet': 'Internet Access',
      'romantic': 'Romantic Relationship',
      'famrel': 'Family Relations',
      'freetime': 'Free Time',
      'goout': 'Going Out',
      'health': 'Health Status',
      'absences': 'Absences'
    };
    return featureNames[feature] || feature;
  };

  return (
    <div className="result-container">
      <h2>Prediction Results</h2>
      
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>🤖 Analyzing student data...</p>
        </div>
      )}
      
      {error && (
        <div className="error">
          <p>Error: {error}</p>
        </div>
      )}
      
      {prediction && !loading && (
        <div className={`result ${prediction.prediction === 1 ? 'pass' : 'fail'}`}>
          <h3>{prediction.prediction_text}</h3>
          <div className="probability">
            Confidence: {Math.round(prediction.confidence * 100)}%
          </div>
          
          <div className="probability-bars">
            <div className="prob-bar">
              <span>Pass Probability:</span>
              <div className="bar">
                <div 
                  className="fill pass-bar" 
                  style={{width: `${prediction.probability.pass * 100}%`}}
                ></div>
              </div>
              <span>{Math.round(prediction.probability.pass * 100)}%</span>
            </div>
            <div className="prob-bar">
              <span>Fail Probability:</span>
              <div className="bar">
                <div 
                  className="fill fail-bar" 
                  style={{width: `${prediction.probability.fail * 100}%`}}
                ></div>
              </div>
              <span>{Math.round(prediction.probability.fail * 100)}%</span>
            </div>
          </div>
          
          <div className="factors">
            <h4>Top Contributing Factors:</h4>
            <div className="factors-list">
              {prediction.top_factors.map((factor, index) => (
                <div key={index} className="factor-item">
                  <span className="factor-name">
                    {formatFeatureName(factor.feature)}
                  </span>
                  <span className="factor-importance">
                    {Math.round(factor.importance * 100)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      
      {!prediction && !loading && !error && (
        <div className="no-result">
          <p>Enter student information and click "Predict Performance" to see results.</p>
        </div>
      )}
    </div>
  );
};

export default PredictionResult;
'''

# Save React components
with open('App.js', 'w') as f:
    f.write(app_js)

with open('StudentForm.js', 'w') as f:
    f.write(student_form)

with open('PredictionResult.js', 'w') as f:
    f.write(prediction_result)

print("React components created:")
print("- App.js")
print("- StudentForm.js") 
print("- PredictionResult.js")