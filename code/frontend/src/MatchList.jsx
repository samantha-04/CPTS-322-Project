import React, { useState, useEffect, useCallback } from 'react';
import MatchCard from './MatchCard';
import './MatchList.css';

const API_BASE = 'http://localhost:5646';

const MatchList = ({ userId }) => {
  const [matches, setMatches] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'accepted', 'denied'
  const [sortBy, setSortBy] = useState('compatibility'); // 'compatibility', 'name'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [surveyRequired, setSurveyRequired] = useState(false);

  const loadMatches = useCallback(async () => {
    if (!userId) return;
    
    setLoading(true);
    setError(null);
    setSurveyRequired(false);
    
    try {
      const response = await fetch(`${API_BASE}/api/matches/${encodeURIComponent(userId)}`);
      const data = await response.json();
      
      if (response.ok) {
        setMatches(data.matches || []);
        if (data.matches && data.matches.length === 0) {
          setError('No matches found yet. More users need to complete the questionnaire.');
        }
      } else if (response.status === 404) {
        setSurveyRequired(true);
        setMatches([]);
      } else {
        setError(data.message || 'Failed to load matches');
        setMatches([]);
      }
    } catch (err) {
      console.error('Error loading matches:', err);
      setError('Network error. Please check if the server is running.');
      // Fall back to mock data for demo purposes
      setMatches([
        {
          id: 'demo1',
          name: 'Alice Johnson',
          age: 21,
          major: 'Computer Science',
          compatibility: 85,
          bio: 'Early riser, loves pets, keeps things tidy. Looking for a quiet study environment.',
          profileImage: null,
          status: 'pending'
        },
        {
          id: 'demo2',
          name: 'Bob Smith',
          age: 22,
          major: 'Engineering',
          compatibility: 72,
          bio: 'Night owl, enjoys gaming and music. Open to sharing groceries.',
          profileImage: null,
          status: 'pending'
        },
        {
          id: 'demo3',
          name: 'Carol Davis',
          age: 20,
          major: 'Biology',
          compatibility: 91,
          bio: 'Clean, organized, and respectful. No smoking, no parties.',
          profileImage: null,
          status: 'pending'
        }
      ]);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    loadMatches();
  }, [loadMatches]);

  const handleAccept = (matchId) => {
    setMatches(prev => 
      prev.map(m => m.id === matchId ? { ...m, status: 'accepted' } : m)
    );
    // TODO: Add API call to save acceptance when backend supports it
    console.log('Accepted match:', matchId);
  };

  const handleDeny = (matchId) => {
    setMatches(prev => 
      prev.map(m => m.id === matchId ? { ...m, status: 'denied' } : m)
    );
    // TODO: Add API call to save denial when backend supports it
    console.log('Denied match:', matchId);
  };

  const filteredMatches = matches.filter(match => {
    if (filter === 'all') return true;
    return match.status === filter;
  });

  const sortedMatches = [...filteredMatches].sort((a, b) => {
    if (sortBy === 'compatibility') {
      return b.compatibility - a.compatibility;
    }
    return a.name.localeCompare(b.name);
  });

  if (surveyRequired) {
    return (
      <div className="match-list-container">
        <div className="match-list-header">
          <h2>Your Matches</h2>
        </div>
        <div className="survey-required">
          <div className="survey-icon">📋</div>
          <h3>Complete Your Questionnaire</h3>
          <p>Please complete the roommate questionnaire in your profile to see your matches.</p>
          <p className="survey-hint">Go to "My Profile" tab and fill out the questionnaire to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="match-list-container">
      <div className="match-list-header">
        <h2>Your Matches</h2>
        <div className="match-controls">
          <div className="filter-group">
            <label>Filter:</label>
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="all">All Matches</option>
              <option value="pending">Pending</option>
              <option value="accepted">Accepted</option>
              <option value="denied">Denied</option>
            </select>
          </div>
          <div className="sort-group">
            <label>Sort by:</label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
              <option value="compatibility">Compatibility</option>
              <option value="name">Name</option>
            </select>
          </div>
          <button className="refresh-btn" onClick={loadMatches} disabled={loading}>
            {loading ? 'Refreshing...' : '🔄 Refresh'}
          </button>
        </div>
      </div>

      {error && !matches.length && (
        <div className="error-banner">
          <p>{error}</p>
        </div>
      )}

      {loading ? (
        <div className="loading">Loading matches...</div>
      ) : sortedMatches.length === 0 ? (
        <div className="no-matches">
          <p>No matches found.</p>
          {filter !== 'all' && (
            <button onClick={() => setFilter('all')}>Show all matches</button>
          )}
        </div>
      ) : (
        <div className="matches-grid">
          {sortedMatches.map(match => (
            <MatchCard
              key={match.id}
              match={match}
              onAccept={handleAccept}
              onDeny={handleDeny}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default MatchList;

