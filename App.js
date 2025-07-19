
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
