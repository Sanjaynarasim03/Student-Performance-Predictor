// Student Performance Predictor JavaScript

class StudentPredictor {
    constructor() {
        this.formData = {};
        this.features = {
            age: { min: 15, max: 19, type: 'number', description: "Student's age" },
            sex: { options: ['M', 'F'], type: 'select', description: "Student's gender" },
            address: { options: ['U', 'R'], labels: ['Urban', 'Rural'], type: 'select', description: 'Home address type' },
            famsize: { options: ['LE3', 'GT3'], labels: ['≤ 3 members', '> 3 members'], type: 'select', description: 'Family size' },
            Medu: { min: 0, max: 4, type: 'slider', description: "Mother's education level", labels: ['None', 'Primary', '5th-9th grade', 'Secondary', 'Higher'] },
            Fedu: { min: 0, max: 4, type: 'slider', description: "Father's education level", labels: ['None', 'Primary', '5th-9th grade', 'Secondary', 'Higher'] },
            studytime: { options: [1, 2, 3, 4], labels: ['<2 hours', '2-5 hours', '5-10 hours', '>10 hours'], type: 'select', description: 'Weekly study time' },
            failures: { min: 0, max: 3, type: 'number', description: 'Number of past class failures' },
            schoolsup: { options: ['yes', 'no'], type: 'radio', description: 'Extra educational school support' },
            famsup: { options: ['yes', 'no'], type: 'radio', description: 'Family educational support' },
            internet: { options: ['yes', 'no'], type: 'radio', description: 'Internet access at home' },
            romantic: { options: ['yes', 'no'], type: 'radio', description: 'In a romantic relationship' },
            health: { min: 1, max: 5, type: 'slider', description: 'Current health status', labels: ['Very bad', 'Bad', 'OK', 'Good', 'Very good'] },
            absences: { min: 0, max: 20, type: 'number', description: 'Number of school absences' }
        };

        this.featureImportance = {
            studytime: 0.245,
            Fedu: 0.154,
            Medu: 0.135,
            failures: 0.090,
            age: 0.078,
            absences: 0.046,
            health: 0.042,
            famsup: 0.038,
            internet: 0.035,
            schoolsup: 0.032
        };

        this.sampleData = {
            age: 17,
            sex: 'F',
            address: 'U',
            famsize: 'GT3',
            Medu: 3,
            Fedu: 2,
            studytime: 3,
            failures: 0,
            schoolsup: 'no',
            famsup: 'yes',
            internet: 'yes',
            romantic: 'no',
            health: 4,
            absences: 2
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeSliders();
        this.setupFormValidation();
    }

    setupEventListeners() {
        // Form submission
        document.getElementById('studentForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });

        // Fill example data button
        document.getElementById('fillExampleBtn').addEventListener('click', () => {
            this.fillExampleData();
        });

        // Reset form button
        document.getElementById('resetFormBtn').addEventListener('click', () => {
            this.resetForm();
        });

        // New prediction button
        document.getElementById('newPredictionBtn').addEventListener('click', () => {
            this.showForm();
        });

        // Slider updates
        document.getElementById('Medu').addEventListener('input', (e) => {
            this.updateSliderValue('Medu', e.target.value);
        });

        document.getElementById('Fedu').addEventListener('input', (e) => {
            this.updateSliderValue('Fedu', e.target.value);
        });

        document.getElementById('health').addEventListener('input', (e) => {
            this.updateSliderValue('health', e.target.value);
        });

        // Real-time validation
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });

            input.addEventListener('input', () => {
                this.clearError(input.name);
            });
        });
    }

    initializeSliders() {
        this.updateSliderValue('Medu', 2);
        this.updateSliderValue('Fedu', 2);
        this.updateSliderValue('health', 3);
    }

    updateSliderValue(fieldName, value) {
        const labels = this.features[fieldName].labels;
        const displayValue = labels[parseInt(value)];
        const valueElement = document.getElementById(`${fieldName}-value`);
        if (valueElement) {
            valueElement.textContent = displayValue;
        }
    }

    setupFormValidation() {
        const form = document.getElementById('studentForm');
        const inputs = form.querySelectorAll('input[required], select[required]');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.clearError(input.name);
            });
        });
    }

    validateField(field) {
        const value = field.value;
        const name = field.name;

        if (field.hasAttribute('required') && !value) {
            this.showError(name, 'This field is required');
            return false;
        }

        if (field.type === 'number') {
            const min = parseInt(field.min);
            const max = parseInt(field.max);
            const numValue = parseInt(value);

            if (isNaN(numValue) || numValue < min || numValue > max) {
                this.showError(name, `Please enter a value between ${min} and ${max}`);
                return false;
            }
        }

        this.clearError(name);
        return true;
    }

    showError(fieldName, message) {
        const errorElement = document.getElementById(`${fieldName}-error`);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }
    }

    clearError(fieldName) {
        const errorElement = document.getElementById(`${fieldName}-error`);
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.classList.remove('show');
        }
    }

    fillExampleData() {
        // Clear any existing errors first
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(el => {
            el.textContent = '';
            el.classList.remove('show');
        });

        // Fill all form fields with sample data
        Object.keys(this.sampleData).forEach(key => {
            const value = this.sampleData[key];

            if (key === 'schoolsup' || key === 'famsup' || key === 'internet' || key === 'romantic') {
                // Handle radio buttons
                const radioButton = document.querySelector(`input[name="${key}"][value="${value}"]`);
                if (radioButton) {
                    radioButton.checked = true;
                }
            } else {
                // Handle regular inputs and selects
                const element = document.querySelector(`[name="${key}"]`);
                if (element) {
                    element.value = value;
                    
                    // Update slider displays
                    if (element.type === 'range') {
                        this.updateSliderValue(key, value);
                    }
                    
                    // Trigger change event for validation
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        });

        // Show success notification
        this.showNotification('✨ Example data filled successfully!', 'success');
    }

    resetForm() {
        const form = document.getElementById('studentForm');
        form.reset();
        
        // Reset sliders to default values
        this.initializeSliders();
        
        // Clear all errors
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(el => {
            el.textContent = '';
            el.classList.remove('show');
        });

        // Reset radio buttons to default
        document.querySelector('input[name="schoolsup"][value="no"]').checked = true;
        document.querySelector('input[name="famsup"][value="yes"]').checked = true;
        document.querySelector('input[name="internet"][value="yes"]').checked = true;
        document.querySelector('input[name="romantic"][value="no"]').checked = true;

        this.showNotification('🔄 Form reset successfully!', 'info');
    }

    handleFormSubmit() {
        if (!this.validateForm()) {
            this.showNotification('❌ Please fix the errors in the form', 'error');
            return;
        }

        this.collectFormData();
        this.showLoading();
        
        // Simulate API call delay
        setTimeout(() => {
            try {
                const prediction = this.makePrediction(this.formData);
                this.hideLoading();
                this.displayResults(prediction);
            } catch (error) {
                console.error('Prediction error:', error);
                this.hideLoading();
                this.showNotification('❌ Error making prediction. Please try again.', 'error');
            }
        }, 2000);
    }

    validateForm() {
        let isValid = true;
        const errors = [];

        // Validate required text/number inputs
        const requiredFields = ['age', 'sex', 'address', 'famsize', 'studytime'];
        requiredFields.forEach(fieldName => {
            const field = document.querySelector(`[name="${fieldName}"]`);
            if (field && !field.value) {
                this.showError(fieldName, 'This field is required');
                errors.push(fieldName);
                isValid = false;
            } else if (field) {
                this.validateField(field);
            }
        });

        // Validate radio groups
        const radioGroups = ['schoolsup', 'famsup', 'internet', 'romantic'];
        radioGroups.forEach(group => {
            const checked = document.querySelector(`input[name="${group}"]:checked`);
            if (!checked) {
                this.showError(group, 'Please select an option');
                errors.push(group);
                isValid = false;
            }
        });

        if (!isValid) {
            console.log('Validation errors:', errors);
        }

        return isValid;
    }

    collectFormData() {
        this.formData = {};

        // Collect regular form fields
        const fields = ['age', 'sex', 'address', 'famsize', 'Medu', 'Fedu', 'studytime', 'failures', 'health', 'absences'];
        fields.forEach(field => {
            const element = document.querySelector(`[name="${field}"]`);
            if (element) {
                const value = element.value;
                // Convert numeric values
                if (['age', 'Medu', 'Fedu', 'studytime', 'failures', 'health', 'absences'].includes(field)) {
                    this.formData[field] = parseInt(value) || 0;
                } else {
                    this.formData[field] = value;
                }
            }
        });

        // Collect radio button values
        const radioGroups = ['schoolsup', 'famsup', 'internet', 'romantic'];
        radioGroups.forEach(group => {
            const checked = document.querySelector(`input[name="${group}"]:checked`);
            if (checked) {
                this.formData[group] = checked.value;
            }
        });

        console.log('Collected form data:', this.formData);
    }

    makePrediction(data) {
        // Simulate ML model prediction with realistic logic
        let score = 0.5; // Base probability

        // Study time impact (most important feature)
        const studyTimeImpact = (data.studytime - 1) * 0.15; // 0 to 0.45
        score += studyTimeImpact * this.featureImportance.studytime;

        // Parents' education impact
        const parentEduImpact = ((data.Medu + data.Fedu) / 8) * 0.3; // 0 to 0.3
        score += parentEduImpact * (this.featureImportance.Medu + this.featureImportance.Fedu);

        // Failures impact (negative)
        const failuresImpact = data.failures * -0.2; // 0 to -0.6
        score += failuresImpact * this.featureImportance.failures;

        // Age impact (older students slightly better)
        const ageImpact = (data.age - 15) / 4 * 0.1; // 0 to 0.1
        score += ageImpact * this.featureImportance.age;

        // Health impact
        const healthImpact = (data.health - 1) / 4 * 0.1; // 0 to 0.1
        score += healthImpact * this.featureImportance.health;

        // Absences impact (negative)
        const absenceImpact = Math.min(data.absences / 20, 1) * -0.15; // 0 to -0.15
        score += absenceImpact * this.featureImportance.absences;

        // Support systems impact
        const famsupImpact = (data.famsup === 'yes') ? 0.05 : -0.05;
        score += famsupImpact * this.featureImportance.famsup;

        const schoolsupImpact = (data.schoolsup === 'yes') ? 0.03 : -0.03;
        score += schoolsupImpact * this.featureImportance.schoolsup;

        const internetImpact = (data.internet === 'yes') ? 0.03 : -0.03;
        score += internetImpact * this.featureImportance.internet;

        // Add some randomness for realism
        score += (Math.random() - 0.5) * 0.1;

        // Clamp to [0, 1]
        score = Math.max(0, Math.min(1, score));

        const confidence = Math.abs(score - 0.5) * 2; // 0 to 1
        const prediction = score > 0.5 ? 'pass' : 'fail';

        return {
            prediction,
            probability: score,
            confidence: Math.max(confidence, 0.6), // Ensure minimum confidence for demo
            features: this.getTopFeatures(data)
        };
    }

    getTopFeatures(data) {
        const features = [];
        
        // Calculate feature contributions based on actual data
        Object.keys(this.featureImportance).forEach(feature => {
            let value = data[feature];
            let impact = 0;
            let description = '';

            switch(feature) {
                case 'studytime':
                    const studyLabels = ['<2 hours', '2-5 hours', '5-10 hours', '>10 hours'];
                    impact = ((value - 1) / 3) * this.featureImportance[feature];
                    description = `Study Time: ${studyLabels[value - 1] || 'Unknown'}`;
                    break;
                case 'Medu':
                    const meduLabels = ['None', 'Primary', '5th-9th grade', 'Secondary', 'Higher'];
                    impact = (value / 4) * this.featureImportance[feature];
                    description = `Mother's Education: ${meduLabels[value] || 'Unknown'}`;
                    break;
                case 'Fedu':
                    const feduLabels = ['None', 'Primary', '5th-9th grade', 'Secondary', 'Higher'];
                    impact = (value / 4) * this.featureImportance[feature];
                    description = `Father's Education: ${feduLabels[value] || 'Unknown'}`;
                    break;
                case 'failures':
                    impact = (3 - value) / 3 * this.featureImportance[feature];
                    description = `Past Failures: ${value}`;
                    break;
                case 'age':
                    impact = ((value - 15) / 4) * this.featureImportance[feature];
                    description = `Age: ${value} years`;
                    break;
                case 'absences':
                    impact = ((20 - value) / 20) * this.featureImportance[feature];
                    description = `Absences: ${value}`;
                    break;
                case 'health':
                    const healthLabels = ['Very bad', 'Bad', 'OK', 'Good', 'Very good'];
                    impact = ((value - 1) / 4) * this.featureImportance[feature];
                    description = `Health: ${healthLabels[value - 1] || 'Unknown'}`;
                    break;
                case 'famsup':
                    impact = (value === 'yes' ? 1 : 0) * this.featureImportance[feature];
                    description = `Family Support: ${value === 'yes' ? 'Yes' : 'No'}`;
                    break;
                case 'internet':
                    impact = (value === 'yes' ? 1 : 0) * this.featureImportance[feature];
                    description = `Internet Access: ${value === 'yes' ? 'Yes' : 'No'}`;
                    break;
                case 'schoolsup':
                    impact = (value === 'yes' ? 1 : 0) * this.featureImportance[feature];
                    description = `School Support: ${value === 'yes' ? 'Yes' : 'No'}`;
                    break;
            }

            features.push({
                name: description,
                importance: Math.abs(impact),
                baseImportance: this.featureImportance[feature]
            });
        });

        // Sort by importance and return top 5
        return features.sort((a, b) => b.baseImportance - a.baseImportance).slice(0, 5);
    }

    displayResults(prediction) {
        console.log('Displaying results:', prediction);

        // Update result status
        const resultStatus = document.getElementById('resultStatus');
        resultStatus.className = `result-status ${prediction.prediction}`;
        resultStatus.textContent = prediction.prediction === 'pass' ? 
            '✅ LIKELY TO PASS' : '❌ AT RISK OF FAILING';

        // Update confidence bar with animation
        const confidenceFill = document.getElementById('confidenceFill');
        const confidenceText = document.getElementById('confidenceText');
        const confidencePercentage = Math.round(prediction.confidence * 100);
        
        // Reset confidence bar
        confidenceFill.style.width = '0%';
        confidenceText.textContent = '0%';
        
        // Animate confidence bar
        setTimeout(() => {
            confidenceFill.style.width = `${confidencePercentage}%`;
            confidenceText.textContent = `${confidencePercentage}%`;
        }, 500);

        // Update factors list
        this.displayFactors(prediction.features);

        // Update interpretation
        this.displayInterpretation(prediction);

        // Hide form and show results
        const formSection = document.querySelector('.form-section');
        const resultsSection = document.getElementById('resultsSection');
        
        if (formSection) {
            formSection.classList.add('hidden');
        }
        
        if (resultsSection) {
            resultsSection.classList.remove('hidden');
            
            // Scroll to results after a brief delay
            setTimeout(() => {
                resultsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 300);
        }

        // Show success notification
        this.showNotification('🔮 Prediction complete!', 'success');
    }

    displayFactors(features) {
        const factorsList = document.getElementById('factorsList');
        if (!factorsList) return;

        factorsList.innerHTML = '';

        features.forEach((feature, index) => {
            const factorItem = document.createElement('div');
            factorItem.className = 'factor-item';
            factorItem.style.animationDelay = `${index * 100}ms`;
            
            const percentage = Math.round(feature.baseImportance * 100);
            
            factorItem.innerHTML = `
                <span class="factor-name">${feature.name}</span>
                <span class="factor-importance">${percentage}%</span>
            `;
            
            factorsList.appendChild(factorItem);
        });
    }

    displayInterpretation(prediction) {
        const interpretationContent = document.getElementById('interpretationContent');
        if (!interpretationContent) return;

        const probability = Math.round(prediction.probability * 100);
        
        let interpretation = '';
        
        if (prediction.prediction === 'pass') {
            interpretation = `
                <p><strong>🎉 Good news!</strong> Based on the provided information, this student has a <strong>${probability}%</strong> probability of academic success.</p>
                <p><strong>Key strengths identified:</strong></p>
                <ul>
                    <li>Study habits and time management appear supportive of success</li>
                    <li>Family and educational background factors are favorable</li>
                    <li>Support systems are in place to help with academic challenges</li>
                </ul>
                <p><em>Continue focusing on consistent study habits and leveraging available support systems.</em></p>
            `;
        } else {
            interpretation = `
                <p><strong>⚠️ Attention needed.</strong> The analysis suggests this student may be at risk, with a <strong>${100 - probability}%</strong> probability of academic challenges.</p>
                <p><strong>Areas for improvement:</strong></p>
                <ul>
                    <li>Consider increasing study time and improving study techniques</li>
                    <li>Leverage family and school support systems more effectively</li>
                    <li>Address any attendance or health issues that may impact learning</li>
                </ul>
                <p><em>Early intervention and additional support can significantly improve outcomes.</em></p>
            `;
        }
        
        interpretationContent.innerHTML = interpretation;
    }

    showForm() {
        const formSection = document.querySelector('.form-section');
        const resultsSection = document.getElementById('resultsSection');
        
        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }
        
        if (formSection) {
            formSection.classList.remove('hidden');
            
            // Scroll to form
            setTimeout(() => {
                formSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 300);
        }
    }

    showLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.classList.remove('hidden');
        }
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        
        // Set styles for different notification types
        let backgroundColor = '';
        switch(type) {
            case 'success':
                backgroundColor = '#10b981';
                break;
            case 'error':
                backgroundColor = '#ef4444';
                break;
            case 'info':
            default:
                backgroundColor = '#3b82f6';
                break;
        }

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 16px;
            background: ${backgroundColor};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            font-size: 14px;
            font-weight: 500;
            max-width: 300px;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentPredictor();
});