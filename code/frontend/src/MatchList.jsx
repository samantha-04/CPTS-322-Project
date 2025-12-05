import React, { useState, useEffect } from 'react';
import MatchCard from './MatchCard';
import './MatchList.css';

const MatchList = ({ userId }) => {
  const [matches, setMatches] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'accepted', 'denied'
  const [sortBy, setSortBy] = useState('compatibility'); // 'compatibility', 'name'
  const [loading, setLoading] = useState(false);

  // Mock data - replace with API call to backend when ready
  useEffect(() => {
    loadMatches();
  }, [userId]);

  const loadMatches = () => {
    setLoading(true);
    // Simulated matches - in real app, fetch from backend API
    setTimeout(() => {
      const mockMatches = [
        {
          id: 1,
          name: 'Alice Johnson',
          age: 21,
          major: 'Computer Science',
          compatibility: 85,
          bio: 'Early riser, loves pets, keeps things tidy. Looking for a quiet study environment.',
          profileImage: null,
          status: 'pending'
        },
        {
          id: 2,
          name: 'Bob Smith',
          age: 22,
          major: 'Engineering',
          compatibility: 72,
          bio: 'Night owl, enjoys gaming and music. Open to sharing groceries.',
          profileImage: null,
          status: 'pending'
        },
        {
          id: 3,
          name: 'Carol Davis',
          age: 20,
          major: 'Biology',
          compatibility: 91,
          bio: 'Clean, organized, and respectful. No smoking, no parties.',
          profileImage: null,
          status: 'pending'
        }
      ];
      setMatches(mockMatches);
      setLoading(false);
    }, 500);
  };

  const handleAccept = (matchId) => {
    setMatches(prev => 
      prev.map(m => m.id === matchId ? { ...m, status: 'accepted' } : m)
    );
    // TODO: Call backend API to save acceptance
    console.log('Accepted match:', matchId);
  };

  const handleDeny = (matchId) => {
    setMatches(prev => 
      prev.map(m => m.id === matchId ? { ...m, status: 'denied' } : m)
    );
    // TODO: Call backend API to save denial
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
        </div>
      </div>

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
