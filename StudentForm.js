
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
