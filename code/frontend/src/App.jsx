import React, { useState } from 'react';
import RoommateProfile from './RoommateProfile';
import Registration from './Registration';
import Login from './Login';

function App() {
  const [currentView, setCurrentView] = useState('registration'); // 'registration', 'login', 'profile'
  const [user, setUser] = useState(null);

  const handleRegistration = (userData) => {
    console.log('Registration data:', userData);
    setUser(userData);
    setCurrentView('profile');
  };

  const handleLogin = (userData) => {
    console.log('Login data:', userData);
    setUser(userData);
    setCurrentView('profile');
  };

  const handleSwitchToLogin = () => {
    setCurrentView('login');
  };

  const handleSwitchToRegister = () => {
    setCurrentView('registration');
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentView('registration');
  };

  return (
    <div className="App">
      {currentView === 'registration' && (
        <Registration 
          onRegister={handleRegistration}
          onSwitchToLogin={handleSwitchToLogin}
        />
      )}
      
      {currentView === 'login' && (
        <Login 
          onLogin={handleLogin}
          onSwitchToRegister={handleSwitchToRegister}
        />
      )}
      
      {currentView === 'profile' && user && (
        <div>
          <div style={{ position: 'absolute', top: '20px', right: '20px' }}>
            <button 
              onClick={handleLogout}
              style={{
                background: '#4a5c4a',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </div>
          <RoommateProfile />
        </div>
      )}
    </div>
  );
}

export default App;