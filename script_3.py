# Create the HTML frontend
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Performance Predictor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }

        .form-container, .result-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .form-container h2, .result-container h2 {
            color: #333;
            margin-bottom: 25px;
            text-align: center;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
            font-size: 0.9rem;
        }

        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }

        .predict-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 20px;
        }

        .predict-btn:hover {
            transform: translateY(-2px);
        }

        .predict-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .result {
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            display: none;
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
            font-size: 2rem;
            margin-bottom: 10px;
        }

        .probability {
            font-size: 1.2rem;
            margin: 10px 0;
        }

        .factors {
            margin-top: 20px;
            text-align: left;
        }

        .factors h4 {
            margin-bottom: 15px;
            text-align: center;
        }

        .factor-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 8px;
            background: rgba(255,255,255,0.2);
            border-radius: 5px;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }

        .error {
            display: none;
            padding: 15px;
            background: #ff6b6b;
            color: white;
            border-radius: 8px;
            margin-top: 20px;
            text-align: center;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Student Performance Predictor</h1>
            <p>AI-powered prediction system to forecast student academic success</p>
        </div>

        <div class="main-content">
            <div class="form-container">
                <h2>Student Information</h2>
                <form id="studentForm">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="age">Age</label>
                            <input type="number" id="age" name="age" min="15" max="19" value="17" required>
                        </div>
                        <div class="form-group">
                            <label for="sex">Gender</label>
                            <select id="sex" name="sex" required>
                                <option value="M">Male</option>
                                <option value="F">Female</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="address">Address Type</label>
                            <select id="address" name="address" required>
                                <option value="U">Urban</option>
                                <option value="R">Rural</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="famsize">Family Size</label>
                            <select id="famsize" name="famsize" required>
                                <option value="LE3">≤ 3 members</option>
                                <option value="GT3">> 3 members</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="Medu">Mother's Education (0-4)</label>
                            <input type="number" id="Medu" name="Medu" min="0" max="4" value="2" required>
                        </div>
                        <div class="form-group">
                            <label for="Fedu">Father's Education (0-4)</label>
                            <input type="number" id="Fedu" name="Fedu" min="0" max="4" value="2" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="studytime">Study Time (1-4)</label>
                            <select id="studytime" name="studytime" required>
                                <option value="1">< 2 hours</option>
                                <option value="2" selected>2 to 5 hours</option>
                                <option value="3">5 to 10 hours</option>
                                <option value="4">> 10 hours</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="failures">Past Failures</label>
                            <input type="number" id="failures" name="failures" min="0" max="3" value="0" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="schoolsup">School Support</label>
                            <select id="schoolsup" name="schoolsup" required>
                                <option value="yes">Yes</option>
                                <option value="no" selected>No</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="famsup">Family Support</label>
                            <select id="famsup" name="famsup" required>
                                <option value="yes" selected>Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="internet">Internet Access</label>
                            <select id="internet" name="internet" required>
                                <option value="yes" selected>Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="romantic">In Romantic Relationship</label>
                            <select id="romantic" name="romantic" required>
                                <option value="yes">Yes</option>
                                <option value="no" selected>No</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="health">Health Status (1-5)</label>
                            <input type="number" id="health" name="health" min="1" max="5" value="4" required>
                        </div>
                        <div class="form-group">
                            <label for="absences">School Absences</label>
                            <input type="number" id="absences" name="absences" min="0" max="20" value="2" required>
                        </div>
                    </div>

                    <button type="submit" class="predict-btn" id="predictBtn">
                        Predict Performance
                    </button>
                </form>
            </div>

            <div class="result-container">
                <h2>Prediction Results</h2>
                
                <div class="loading" id="loading">
                    <p>🤖 Analyzing student data...</p>
                </div>

                <div class="error" id="error">
                    <p>Error occurred while making prediction. Please try again.</p>
                </div>

                <div class="result" id="result">
                    <h3 id="resultText"></h3>
                    <div class="probability" id="probability"></div>
                    
                    <div class="factors">
                        <h4>Top Contributing Factors:</h4>
                        <div id="factorsList"></div>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 30px; color: #666;">
                    <p><em>This prediction is based on machine learning analysis of student performance patterns.</em></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE_URL = 'http://localhost:5000';
        
        document.getElementById('studentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = {};
            
            // Collect form data
            for (let [key, value] of formData.entries()) {
                // Convert numeric fields to numbers
                if (['age', 'Medu', 'Fedu', 'studytime', 'failures', 'health', 'absences'].includes(key)) {
                    data[key] = parseInt(value);
                } else {
                    data[key] = value;
                }
            }
            
            // Add default values for missing fields
            data.Pstatus = 'T';
            data.paid = 'no';
            data.activities = 'yes';
            data.famrel = 4;
            data.freetime = 3;
            data.goout = 3;
            
            // Show loading state
            showLoading();
            
            try {
                const response = await fetch(`${API_BASE_URL}/predict`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const result = await response.json();
                displayResult(result);
                
            } catch (error) {
                console.error('Error:', error);
                showError();
            }
        });
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('predictBtn').disabled = true;
        }
        
        function showError() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'block';
            document.getElementById('predictBtn').disabled = false;
        }
        
        function displayResult(result) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('predictBtn').disabled = false;
            
            const resultDiv = document.getElementById('result');
            const resultText = document.getElementById('resultText');
            const probability = document.getElementById('probability');
            const factorsList = document.getElementById('factorsList');
            
            // Set result text and styling
            resultText.textContent = result.prediction_text;
            resultDiv.className = 'result ' + (result.prediction === 1 ? 'pass' : 'fail');
            
            // Set probability
            const confidence = Math.round(result.confidence * 100);
            probability.textContent = `Confidence: ${confidence}%`;
            
            // Display top factors
            factorsList.innerHTML = '';
            result.top_factors.forEach(factor => {
                const factorDiv = document.createElement('div');
                factorDiv.className = 'factor-item';
                factorDiv.innerHTML = `
                    <span>${formatFeatureName(factor.feature)}</span>
                    <span>${Math.round(factor.importance * 100)}%</span>
                `;
                factorsList.appendChild(factorDiv);
            });
            
            resultDiv.style.display = 'block';
        }
        
        function formatFeatureName(feature) {
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
        }
    </script>
</body>
</html>
'''

# Save HTML frontend
with open('index.html', 'w') as f:
    f.write(html_code)

print("HTML frontend created: index.html")