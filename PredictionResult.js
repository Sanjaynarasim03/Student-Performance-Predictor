
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
