/**
 * Copyright (c) 2025 Bhagya Dissanayake
 * All rights reserved. This code is proprietary and confidential.
 * Unauthorized copying, distribution, or use is strictly prohibited.
 */

import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// Components
import Header from './components/Header';
import ChatRecommend from './components/ChatRecommend';
import EasterEggModal from './components/EasterEggModal';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState(null);
  const [showEasterEgg, setShowEasterEgg] = useState(false);
  const [clickSequence, setClickSequence] = useState([]);
  const konamiCodeRef = useRef([]);
  const clickTimeoutRef = useRef(null);

  // Easter Egg Functions
  const showEasterEggModal = () => {
    setShowEasterEgg(true);
    console.log('%c🎉 Easter Egg Found!', 'color: #1e3c72; font-size: 20px; font-weight: bold;');
    console.log('%cDeveloped by Bhagya Dissanayake', 'color: #2a5298; font-size: 16px;');
    console.log('%cVisit: https://github.com/bhagya-d36', 'color: #666; font-size: 14px;');
    console.log('%cLinkedIn: https://www.linkedin.com/in/bhagya-dissanayake-3a1a43286/', 'color: #666; font-size: 14px;');
  };

  const handleElementClick = (element) => {
    setClickSequence(prev => {
      const newSequence = [...prev, element];
      
      if (newSequence.length > 5) {
        newSequence.shift();
      }
      
      // Check for sequence: header, footer, header, footer, header
      const targetSequence = ['header', 'footer', 'header', 'footer', 'header'];
      if (newSequence.join(',') === targetSequence.join(',')) {
        showEasterEggModal();
        return [];
      }
      
      return newSequence;
    });
    
    // Reset sequence after 3 seconds
    clearTimeout(clickTimeoutRef.current);
    clickTimeoutRef.current = setTimeout(() => {
      setClickSequence([]);
    }, 3000);
  };

  useEffect(() => {
    // Console Easter Egg
    window.showCredits = () => {
      showEasterEggModal();
    };
    
    console.log('%cType "showCredits()" in console for a surprise!', 'color: #666; font-style: italic;');
    
    // Konami Code Easter Egg
    const konamiSequence = [
      'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
      'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
      'KeyB', 'KeyA'
    ];

    const handleKeyPress = (e) => {
      konamiCodeRef.current.push(e.code);
      if (konamiCodeRef.current.length > konamiSequence.length) {
        konamiCodeRef.current.shift();
      }
      
      if (konamiCodeRef.current.join(',') === konamiSequence.join(',')) {
        showEasterEggModal();
        konamiCodeRef.current = [];
      }
    };

    // Check API health on app load
    const checkAPIHealth = async () => {
      try {
        const response = await fetch('/api/v1/health');
        const data = await response.json();
        setApiStatus(data.status === 'healthy' ? 'healthy' : 'unhealthy');
      } catch (error) {
        console.error('API Health Check Failed:', error);
        setApiStatus('unhealthy');
      } finally {
        setIsLoading(false);
      }
    };

    checkAPIHealth();
    window.addEventListener('keydown', handleKeyPress);
    
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
      clearTimeout(clickTimeoutRef.current);
    };
  }, []);

  if (isLoading) {
    return (
      <div className="loading">
        <h2>Loading Laptop Assistant...</h2>
        <p>Checking API connection...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <Header apiStatus={apiStatus} onHeaderClick={() => handleElementClick('header')} />
      
      <main className="main-content">
        <ChatRecommend />
      </main>
      
      <footer className="footer" onClick={() => handleElementClick('footer')}>
        <div className="container">
          <p>&copy; 2025 Laptop Insights and Recommendation System. AI-powered laptop recommendations and live chat.</p>
          <div className="api-status">
            <div className={`status-indicator ${apiStatus === 'healthy' ? 'status-healthy' : 'status-unhealthy'}`}></div>
            <span>API {apiStatus || 'Unknown'}</span>
          </div>
        </div>
      </footer>
      
      <EasterEggModal isOpen={showEasterEgg} onClose={() => setShowEasterEgg(false)} />
    </div>
  );
}

export default App;
