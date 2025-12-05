import React, { useState } from 'react';
import Home from './Home';
import Registration from './Registration';
import Login from './Login';

function App() {
  const [currentView, setCurrentView] = useState('registration'); // 'registration', 'login', 'home'
  const [user, setUser] = useState(null);

  const handleRegistration = (userData) => {
    console.log('Registration data:', userData);
    setUser(userData);
    setCurrentView('home');
  };

  const handleLogin = (userData) => {
    console.log('Login data:', userData);
    setUser(userData);
    setCurrentView('home');
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
      
      {currentView === 'home' && user && (
        <Home user={user} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;