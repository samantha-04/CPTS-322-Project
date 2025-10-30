import React, { useEffect, useState } from 'react';
import './Questionnaire.css';

const API_BASE = 'http://localhost:5646';

const Questionnaire = ({ onSubmitted }) => {
  const [questions, setQuestions] = useState({});
  const [answers, setAnswers] = useState({});
  const [userId, setUserId] = useState('');
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/questions`)
      .then(res => res.json())
      .then(data => {
        setQuestions(data);
      }).catch(err => {
        console.error('Failed to fetch questions', err);
      });
  }, []);

  const handleChange = (key, value) => {
    setAnswers(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userId) {
      setStatus('Please enter a user id');
      return;
    }
    // Validate that all questions have answers
    const missing = [];
    Object.keys(questions).forEach((k) => {
      const meta = questions[k] || {};
      const val = answers[k];
      // treat empty string, undefined or null as missing
      if (val === undefined || val === null || String(val).trim() === '') {
        missing.push(meta.label || k);
      }
    });

    if (missing.length > 0) {
      setStatus(`Please answer all questions. Missing: ${missing.join(', ')}`);
      return;
    }

    setStatus('Submitting...');
    try {
      const res = await fetch(`${API_BASE}/submit_answers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, answers })
      });
      const json = await res.json();
      if (res.ok) {
        setStatus('Saved');
        if (onSubmitted) onSubmitted(userId);
      } else {
        setStatus(json.error || 'Error');
      }
    } catch (err) {
      console.error(err);
      setStatus('Network error');
    }
  };

  return (
    <div className="questionnaire">
      <h3>Questionnaire</h3>
      <form onSubmit={handleSubmit} className="questionnaire-form">
        <div className="form-row">
          <label>User ID</label>
          <input value={userId} onChange={e => setUserId(e.target.value)} placeholder="unique-id" />
        </div>

        {Object.entries(questions).map(([key, meta]) => (
          <div className="form-row" key={key}>
            <label>{meta.label || key} <span className="required">*</span></label>
            {meta.type === 'yes_no' && (
              <select value={answers[key] || ''} onChange={e => handleChange(key, e.target.value)}>
                <option value="">--</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            )}
            {meta.type === 'likert_5' && (
              <select value={answers[key] || ''} onChange={e => handleChange(key, e.target.value)}>
                <option value="">--</option>
                <option>Strongly Disagree</option>
                <option>Disagree</option>
                <option>Neutral</option>
                <option>Agree</option>
                <option>Strongly Agree</option>
              </select>
            )}
            {meta.type === 'frequency_4' && (
              <select value={answers[key] || ''} onChange={e => handleChange(key, e.target.value)}>
                <option value="">--</option>
                <option>Never</option>
                <option>Sometimes</option>
                <option>Often</option>
                <option>Always</option>
              </select>
            )}
            {!meta.type && (
              <input value={answers[key] || ''} onChange={e => handleChange(key, e.target.value)} />
            )}
          </div>
        ))}

        <div className="form-row">
          <button type="submit">Submit Answers</button>
          {status && <span className="status">{status}</span>}
        </div>
      </form>
    </div>
  );
};

export default Questionnaire;
