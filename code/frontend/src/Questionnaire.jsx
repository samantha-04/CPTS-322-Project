import React, { useEffect, useState } from 'react';
import './Questionnaire.css';

const API_BASE = 'http://localhost:5646';

// Fallback questions if backend is unavailable
const FALLBACK_QUESTIONS = {
  "q_smoking": {"type": "yes_no", "label": "Do you smoke?", "weight": 1.0},
  "q_pets": {"type": "yes_no", "label": "Do you have pets?", "weight": 1.0},
  "q_clean_freq": {"type": "frequency_4", "label": "How often do you clean?", "weight": 1.0},
  "q_social": {"type": "likert_5", "label": "I like having friends over.", "weight": 1.0},
  "q_noise": {"type": "likert_5", "label": "I don't mind loud music.", "weight": 1.0},
  "q_quiet_hours": {"type": "yes_no", "label": "Should we have quiet hours?", "weight": 1.0},
  "q_shared_food": {"type": "yes_no", "label": "Are you ok with shared groceries?", "weight": 1.0},
  "q_lifestyle": {"type": null, "label": "Describe your lifestyle (optional).", "weight": 0.5},
  "q_sleep_schedule": {"type": "likert_5", "label": "I prefer to go to bed early.", "weight": 1.0},
  "q_noise_tolerance": {"type": "likert_5", "label": "I am comfortable with background noise.", "weight": 1.0},
  "q_alcohol": {"type": "yes_no", "label": "Are you okay with alcohol being consumed in the home?", "weight": 1.0},
  "q_share_chores": {"type": "yes_no", "label": "Are you willing to share chores fairly?", "weight": 1.0},
  "q_temperature_pref": {"type": "likert_5", "label": "I prefer a cooler apartment (lower thermostat).", "weight": 1.0},
  "q_vehicle": {"type": null, "label": "Do you have a vehicle (optional comments)?", "weight": 0.5},
  "q_overnight_guests": {"type": "frequency_4", "label": "How often do you have overnight guests?", "weight": 1.0},
  "q_shared_groceries": {"type": "likert_5", "label": "I am open to sharing kitchen appliances and cookware.", "weight": 0.8},
  "q_work_from_home": {"type": "frequency_4", "label": "How often do you work/study from home?", "weight": 0.9},
  "q_morning_routine": {"type": "likert_5", "label": "I need the bathroom for a long time in the morning.", "weight": 0.7},
  "q_social_events": {"type": "frequency_4", "label": "How often do you attend social events outside the home?", "weight": 0.8},
  "q_tv_music": {"type": "likert_5", "label": "I often play music or watch TV in common areas.", "weight": 0.9},
  "q_visitors_notice": {"type": "yes_no", "label": "Should roommates give advance notice before having visitors?", "weight": 1.0},
  "q_decorating": {"type": "likert_5", "label": "I like to personalize and decorate shared spaces.", "weight": 0.6},
  "q_conflict_style": {"type": "likert_5", "label": "I prefer to address conflicts directly rather than avoid them.", "weight": 1.0},
  "q_budget_conscious": {"type": "likert_5", "label": "I am budget-conscious with utilities and shared expenses.", "weight": 0.9}
};

const Questionnaire = ({ onSubmitted }) => {
  const [questions, setQuestions] = useState(FALLBACK_QUESTIONS);
  const [answers, setAnswers] = useState({});
  const [userId, setUserId] = useState('');
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/questions`)
      .then(res => res.json())
      .then(data => {
        setQuestions(data);
      }).catch(err => {
        console.error('Failed to fetch questions, using fallback', err);
        // Keep using fallback questions
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
      const res = await fetch(`${API_BASE}/api/survey/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: userId, answers })
      });
      const json = await res.json();
      if (res.ok) {
        setStatus('Saved successfully!');
        if (onSubmitted) onSubmitted(userId);
      } else {
        setStatus(json.message || 'Error');
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
