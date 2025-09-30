/**
 * Copyright (c) 2025 Bhagya Dissanayake
 * All rights reserved. This code is proprietary and confidential.
 * Unauthorized copying, distribution, or use is strictly prohibited.
 */

import React from 'react';
import './EasterEggModal.css';

const EasterEggModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="easter-egg-modal" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>🎉 Easter Egg Found!</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <p>Congratulations! You discovered the hidden feature.</p>
          
          <div className="developer-info">
            <h3>Developed by Bhagya Dissanayake</h3>
            <p>Data Scientist & AI/ML Engineer</p>
            
            <div className="links">
              <a href="https://github.com/bhagya-d36" target="_blank" rel="noopener noreferrer">
                🔗 GitHub
              </a>
              <a href="https://www.linkedin.com/in/bhagya-dissanayake-3a1a43286/" target="_blank" rel="noopener noreferrer">
                🔗 LinkedIn
              </a>
            </div>
            
          </div>
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-primary" onClick={onClose}>
            Awesome! Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default EasterEggModal;
