import React, { useState } from 'react';
import RoommateProfile from './RoommateProfile';
import MatchList from './MatchList';
import './Home.css';

const Home = ({ user, onLogout, onUserUpdate }) => {
  const [activeTab, setActiveTab] = useState('matches'); // 'matches', 'profile', 'settings'
  const [currentUser, setCurrentUser] = useState(user);

  const handleProfileUpdate = (updatedUser) => {
    setCurrentUser(updatedUser);
    if (onUserUpdate) {
      onUserUpdate(updatedUser);
    }
  };

  return (
    <div className="home-container">
      <header className="home-header">
        <h1 className="home-title">Roommate Finder</h1>
        <div className="header-user">
          <span className="user-greeting">Welcome, {currentUser?.name || currentUser?.email?.split('@')[0] || 'User'}</span>
          <button onClick={onLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>

      <nav className="home-nav">
        <button 
          className={`nav-tab ${activeTab === 'matches' ? 'active' : ''}`}
          onClick={() => setActiveTab('matches')}
        >
          My Matches
        </button>
        <button 
          className={`nav-tab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          My Profile
        </button>
        <button 
          className={`nav-tab ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </button>
      </nav>

      <main className="home-content">
        {activeTab === 'matches' && (
          <MatchList userId={currentUser?.email} />
        )}
        
        {activeTab === 'profile' && (
          <RoommateProfile 
            user={currentUser} 
            onProfileUpdate={handleProfileUpdate}
          />
        )}
        
        {activeTab === 'settings' && (
          <div className="settings-panel">
            <h2>Settings</h2>
            <div className="settings-section">
              <h3>Account Information</h3>
              <p><strong>Email:</strong> {currentUser?.email}</p>
              <p><strong>Survey Status:</strong> {currentUser?.surveyCompleted ? '✓ Completed' : '⚠ Not completed'}</p>
            </div>
            <div className="settings-section">
              <h3>Preferences</h3>
              <p>Additional account settings and preferences coming soon...</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Home;
