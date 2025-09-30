import React, { useState } from 'react';
import './Header.css';

const Header = ({ apiStatus, onHeaderClick }) => {
  const [logoClickCount, setLogoClickCount] = useState(0);
  const [developerClickCount, setDeveloperClickCount] = useState(0);

  const handleLogoClick = () => {
    setLogoClickCount(prev => prev + 1);
    
    if (logoClickCount === 2) { // Third click
      // Trigger easter egg
      if (window.showCredits) {
        window.showCredits();
      }
      setLogoClickCount(0);
    }
    
    // Reset counter after 2 seconds
    setTimeout(() => setLogoClickCount(0), 2000);
  };

  const handleDeveloperClick = () => {
    setDeveloperClickCount(prev => prev + 1);
    
    if (developerClickCount === 1) { // Second click (double click)
      // Trigger easter egg
      if (window.showCredits) {
        window.showCredits();
      }
      setDeveloperClickCount(0);
    }
    
    // Reset counter after 1 second
    setTimeout(() => setDeveloperClickCount(0), 1000);
  };

  return (
    <nav className="navbar" onClick={onHeaderClick}>
      <div className="container">
        <div className="navbar-brand" onClick={handleLogoClick} style={{ cursor: 'pointer' }}>
        Laptop Data Intelligence Platform
        </div>
        <div className="developer-credit">
          <span className="credit-text">Developed by</span>
          <span 
            className="developer-name" 
            onClick={handleDeveloperClick}
            style={{ cursor: 'pointer' }}
          >
            Bhagya Dissanayake
          </span>
        </div>
      </div>
    </nav>
  );
};

export default Header;
