import React, { useState, useRef, useEffect } from 'react';
import './RoommateProfile.css';
import Questionnaire from './Questionnaire';

const API_BASE = 'http://localhost:5646';

const RoommateProfile = ({ user, onProfileUpdate }) => {
  const [name, setName] = useState(user?.name || 'Your Name');
  const [profileImage, setProfileImage] = useState(null);
  const [isEditingName, setIsEditingName] = useState(false);
  const [bioData, setBioData] = useState({
    age: user?.profile?.age || '',
    major: user?.profile?.major || '',
    bio: user?.profile?.bio || ''
  });
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState(null);
  const [showQuestionnaire, setShowQuestionnaire] = useState(!user?.surveyCompleted);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (user) {
      setName(user.name || 'Your Name');
      setBioData({
        age: user.profile?.age || '',
        major: user.profile?.major || '',
        bio: user.profile?.bio || ''
      });
      setShowQuestionnaire(!user.surveyCompleted);
    }
  }, [user]);

  const handleNameClick = () => {
    setIsEditingName(true);
  };

  const handleNameBlur = () => {
    setIsEditingName(false);
    saveProfile();
  };

  const handleNameKeyPress = (e) => {
    if (e.key === 'Enter') {
      setIsEditingName(false);
      saveProfile();
    }
  };

  const handlePhotoUpload = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setProfileImage(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleBioChange = (field, value) => {
    setBioData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const saveProfile = async () => {
    if (!user?.email) return;
    
    setSaving(true);
    setSaveMessage(null);
    
    try {
      const response = await fetch(`${API_BASE}/api/user/${encodeURIComponent(user.email)}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          profile: {
            age: bioData.age ? parseInt(bioData.age) : null,
            major: bioData.major,
            bio: bioData.bio
          }
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSaveMessage('Profile saved!');
        if (onProfileUpdate && data.user) {
          onProfileUpdate(data.user);
        }
      } else {
        setSaveMessage(data.message || 'Failed to save profile');
      }
    } catch (error) {
      console.error('Error saving profile:', error);
      setSaveMessage('Network error. Profile saved locally.');
    } finally {
      setSaving(false);
      setTimeout(() => setSaveMessage(null), 3000);
    }
  };

  const handleQuestionnaireSubmitted = (submittedUserId) => {
    setShowQuestionnaire(false);
    if (onProfileUpdate && user) {
      onProfileUpdate({ ...user, surveyCompleted: true });
    }
  };

  return (
    <div className="roommate-container">
      <div className="profile-card">
        <div className="profile-header">
          <div className="avatar-container">
            <div className="avatar" onClick={handlePhotoUpload}>
              {profileImage ? (
                <img src={profileImage} alt="Profile" className="avatar-image" />
              ) : (
                <div className="avatar-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M21 21V19C21 17.1435 20.2625 15.363 18.9497 14.0503C17.637 12.7375 15.8565 12 14 12H10C8.14348 12 6.36301 12.7375 5.05025 14.0503C3.7375 15.363 3 17.1435 3 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              )}
              <div className="avatar-edit-overlay">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className="file-input"
            />
          </div>
          
          {isEditingName ? (
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              onBlur={handleNameBlur}
              onKeyPress={handleNameKeyPress}
              className="name-input"
              autoFocus
            />
          ) : (
            <h2 className="profile-name" onClick={handleNameClick}>
              {name}
            </h2>
          )}
          
          {user?.email && (
            <p className="profile-email">{user.email}</p>
          )}
        </div>
        
        <div className="bio-section">
          <h3 className="bio-title">Profile Information</h3>
          
          <div className="bio-field">
            <label className="bio-label">Age</label>
            <input
              type="number"
              value={bioData.age}
              onChange={(e) => handleBioChange('age', e.target.value)}
              onBlur={saveProfile}
              className="bio-input"
              placeholder="Enter your age"
              min="18"
              max="100"
            />
          </div>
          
          <div className="bio-field">
            <label className="bio-label">Major</label>
            <input
              type="text"
              value={bioData.major}
              onChange={(e) => handleBioChange('major', e.target.value)}
              onBlur={saveProfile}
              className="bio-input"
              placeholder="Enter your major"
            />
          </div>
          
          <div className="bio-field">
            <label className="bio-label">Bio</label>
            <textarea
              value={bioData.bio}
              onChange={(e) => handleBioChange('bio', e.target.value)}
              onBlur={saveProfile}
              className="bio-input bio-textarea"
              placeholder="Tell potential roommates about yourself..."
              rows="3"
            />
          </div>
          
          {saveMessage && (
            <div className={`save-message ${saveMessage.includes('error') || saveMessage.includes('Failed') ? 'error' : 'success'}`}>
              {saving ? 'Saving...' : saveMessage}
            </div>
          )}
        </div>
      </div>
      
      {/* Questionnaire Section */}
      <div className="questionnaire-section">
        <div className="questionnaire-header">
          <h3>Roommate Preferences Questionnaire</h3>
          {user?.surveyCompleted && !showQuestionnaire && (
            <button 
              className="edit-questionnaire-btn"
              onClick={() => setShowQuestionnaire(true)}
            >
              Edit Answers
            </button>
          )}
        </div>
        
        {showQuestionnaire ? (
          <Questionnaire 
            userId={user?.email} 
            onSubmitted={handleQuestionnaireSubmitted}
          />
        ) : (
          <div className="questionnaire-complete">
            <span className="check-icon">✓</span>
            <p>Questionnaire completed! Your matches are being calculated based on your preferences.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RoommateProfile;
