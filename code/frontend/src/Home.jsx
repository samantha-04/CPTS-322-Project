import React, { useState } from 'react';
import RoommateProfile from './RoommateProfile';
import MatchList from './MatchList';
import './Home.css';

const Home = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('matches'); // 'matches', 'profile', 'settings'

  return (
    <div className="home-container">
      <header className="home-header">
        <h1 className="home-title">Roommate Finder</h1>
        <button onClick={onLogout} className="logout-btn">
          Logout
        </button>
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
          <MatchList userId={user?.email || user?.name} />
        )}
        
        {activeTab === 'profile' && (
          <RoommateProfile />
        )}
        
        {activeTab === 'settings' && (
          <div className="settings-panel">
            <h2>Settings</h2>
            <p>Account settings and preferences coming soon...</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default Home;
