import React from 'react';
import './MatchCard.css';

const MatchCard = ({ match, onAccept, onDeny }) => {
  const {
    id,
    name,
    age,
    major,
    compatibility,
    bio,
    profileImage,
    status = 'pending' // 'pending', 'accepted', 'denied'
  } = match;

  return (
    <div className={`match-card ${status}`}>
      <div className="match-header">
        <div className="match-avatar">
          {profileImage ? (
            <img src={profileImage} alt={name} className="match-avatar-img" />
          ) : (
            <div className="match-avatar-placeholder">
              {name?.charAt(0)?.toUpperCase() || '?'}
            </div>
          )}
        </div>
        <div className="match-info">
          <h3 className="match-name">{name || 'Unknown'}</h3>
          <p className="match-details">
            {age && `${age} years old`} {major && `• ${major}`}
          </p>
        </div>
        <div className="match-compatibility">
          <div className="compatibility-score">
            {Math.round(compatibility || 0)}%
          </div>
          <span className="compatibility-label">Match</span>
        </div>
      </div>

      {bio && (
        <div className="match-bio">
          <p>{bio}</p>
        </div>
      )}

      {status === 'pending' && (
        <div className="match-actions">
          <button 
            className="btn-deny" 
            onClick={() => onDeny(id)}
          >
            ✕ Deny
          </button>
          <button 
            className="btn-accept" 
            onClick={() => onAccept(id)}
          >
            ✓ Accept
          </button>
        </div>
      )}

      {status === 'accepted' && (
        <div className="match-status accepted">
          <span>✓ Accepted</span>
        </div>
      )}

      {status === 'denied' && (
        <div className="match-status denied">
          <span>✕ Denied</span>
        </div>
      )}
    </div>
  );
};

export default MatchCard;
