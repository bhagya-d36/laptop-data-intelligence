/**
 * Copyright (c) 2025 Bhagya Dissanayake
 * All rights reserved. This code is proprietary and confidential.
 * Unauthorized copying, distribution, or use is strictly prohibited.
 */

import React, { useState, useEffect } from 'react';
import { chatAPI, recommendationsAPI } from '../services/api';
import ExploreCompare from './ExploreCompare';
import ReviewsIntelligence from './ReviewsIntelligence';
import './ChatRecommend.css';

const ChatRecommend = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeMode, setActiveMode] = useState('chat');
  const [recommendationConstraints, setRecommendationConstraints] = useState({
    brand: '',
    maxPrice: '',
    minRating: '',
    processorType: '',
    useCase: ''
  });
  const [recommendations, setRecommendations] = useState([]);
  const [recommendationLoading, setRecommendationLoading] = useState(false);

  useEffect(() => {
    // Initialize with welcome message
    setMessages([{
      id: 1,
      type: 'bot',
      content: 'Hello! I\'m your laptop intelligence assistant. I can help you find the perfect laptop based on your needs, answer questions about specifications, and provide personalized recommendations. How can I assist you today?',
      timestamp: new Date().toISOString()
    }]);
  }, []);

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;
    
    // console.log('sendMessage called - loading:', loading, 'inputMessage:', inputMessage.trim());

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      // console.log('Making API call...');
      const response = await chatAPI.query(inputMessage);
      // console.log('API Response:', response.data); // Add this for debugging
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.data.response, // Correct path: response.data.data.response
        timestamp: new Date().toISOString(),
        context: response.data.data.context_used // Correct path: response.data.data.context_used
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const getRecommendations = async () => {
    setRecommendationLoading(true);
    try {
      console.log('Sending constraints:', recommendationConstraints);
      const response = await recommendationsAPI.getConstraintBased(recommendationConstraints);
      console.log('API Response:', response);
      console.log('Recommendations data:', response.data.data.recommendations);
      setRecommendations(response.data.data.recommendations);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      console.error('Error details:', error.response?.data);
      setRecommendations([]);
    } finally {
      setRecommendationLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([{
      id: 1,
      type: 'bot',
      content: 'Hello! I\'m your laptop intelligence assistant. I can help you find the perfect laptop based on your needs, answer questions about specifications, and provide personalized recommendations. How can I assist you today?',
      timestamp: new Date().toISOString()
    }]);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const parsePrice = (priceDetails) => {
    try {
      // priceDetails is now an object, not a string
      if (typeof priceDetails === 'object' && priceDetails !== null) {
        return priceDetails['Current Price'] || 'Not Available';
      }
      return 'Not Available';
    } catch {
      return 'Not Available';
    }
  };

  const renderMessageContent = (content) => {
    // Split content by lines and process each line
    return content.split('\n').map((line, lineIndex) => {
      // Handle bold text (**text**)
      const processedLine = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      
      // Handle bullet points
      if (line.trim().startsWith('•')) {
        return (
          <div key={lineIndex} style={{ marginLeft: '20px', marginBottom: '4px' }}>
            <span dangerouslySetInnerHTML={{ __html: processedLine }} />
          </div>
        );
      }
      
      // Handle regular lines
      if (line.trim()) {
        return (
          <div key={lineIndex} style={{ marginBottom: '8px' }}>
            <span dangerouslySetInnerHTML={{ __html: processedLine }} />
          </div>
        );
      }
      
      // Handle empty lines
      return <div key={lineIndex} style={{ height: '8px' }} />;
    });
  };

  const quickQuestions = [
    "What are the best laptops under $1000?",
    "Compare Lenovo ThinkPad vs HP ProBook",
    "Which laptop has the best battery life?",
    "What's the difference between Intel and AMD processors?",
    "Recommend a laptop for business use"
  ];

  const renderActiveMode = () => {
    switch (activeMode) {
      case 'chat':
        return (
          <div className="chat-section">
            <div className="chat-container">
              <div className="chat-messages">
                {messages.map((message) => (
                  <div key={message.id} className={`message ${message.type}`}>
                    <div className="message-content">
                      {renderMessageContent(message.content)}
                    </div>
                    {message.context && (
                      <div className="message-context">
                        <small>Source: Laptop Intelligence Database</small>
                      </div>
                    )}
                    <div className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="message bot">
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="quick-questions">
                <h4>Quick Questions:</h4>
                <div className="quick-questions-grid">
                  {quickQuestions.map((question, index) => (
                    <button
                      key={index}
                      className="quick-question-btn"
                      onClick={() => setInputMessage(question)}
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>

              <div className="chat-input">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about laptops..."
                  rows="3"
                  disabled={loading}
                />
                <div className="chat-actions">
                  <button 
                    className="btn btn-secondary" 
                    onClick={clearChat}
                    disabled={loading}
                  >
                    Clear Chat
                  </button>
                  <button 
                    className="btn send-btn" 
                    onClick={sendMessage}
                    disabled={loading || !inputMessage.trim()}
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        );

      case 'recommend':
        return (
          <div className="recommend-section">
            <div className="recommendation-form">
              <h3>Tell us what you're looking for:</h3>
              
              <div className="form-grid">
                <div className="form-group">
                  <label>Brand Preference</label>
                  <select
                    value={recommendationConstraints.brand}
                    onChange={(e) => setRecommendationConstraints(prev => ({
                      ...prev,
                      brand: e.target.value
                    }))}
                    className="form-control"
                  >
                    <option value="">Any Brand</option>
                    <option value="Lenovo">Lenovo</option>
                    <option value="HP">HP</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Maximum Price ($)</label>
                  <input
                    type="number"
                    value={recommendationConstraints.maxPrice}
                    onChange={(e) => setRecommendationConstraints(prev => ({
                      ...prev,
                      maxPrice: e.target.value
                    }))}
                    className="form-control"
                    placeholder="e.g., 1500"
                  />
                </div>

                <div className="form-group">
                  <label>Minimum Rating</label>
                  <select
                    value={recommendationConstraints.minRating}
                    onChange={(e) => setRecommendationConstraints(prev => ({
                      ...prev,
                      minRating: e.target.value
                    }))}
                    className="form-control"
                  >
                    <option value="">Any Rating</option>
                    <option value="4.5">4.5+ Stars</option>
                    <option value="4.0">4.0+ Stars</option>
                    <option value="3.5">3.5+ Stars</option>
                    <option value="3.0">3.0+ Stars</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Use Case</label>
                  <select
                    value={recommendationConstraints.useCase}
                    onChange={(e) => setRecommendationConstraints(prev => ({
                      ...prev,
                      useCase: e.target.value
                    }))}
                    className="form-control"
                  >
                    <option value="">Any Use Case</option>
                    <option value="business">Business</option>
                    <option value="gaming">Gaming</option>
                    <option value="student">Student</option>
                    <option value="creative">Creative Work</option>
                    <option value="portable">Portable</option>
                  </select>
                </div>
              </div>

              <button 
                className="btn"
                onClick={getRecommendations}
                disabled={recommendationLoading}
              >
                {recommendationLoading ? 'Getting Recommendations...' : 'Get Recommendations'}
              </button>
            </div>

            {recommendations.length > 0 && (
              <div className="recommendations-results">
                <h3>Recommended Laptops:</h3>
                <div className="recommendations-grid">
                  {recommendations.map((rec, index) => (
                    <div key={index} className="recommendation-card">
                      <div className="rec-header">
                        <h4>{rec.brand} {rec.model}</h4>
                        <div className="rec-score">
                          Match: {Math.min(((rec.match_score || 0) * 10), 100).toFixed(0)}%
                        </div>
                      </div>
                      
                      <div className="rec-specs">
                        <div className="spec-item">
                          <strong>Processor:</strong> {rec.processor || 'N/A'}
                        </div>
                        <div className="spec-item">
                          <strong>Memory:</strong> {rec.memory || 'N/A'}
                        </div>
                        <div className="spec-item">
                          <strong>Storage:</strong> {rec.storage || 'N/A'}
                        </div>
                        <div className="spec-item">
                          <strong>Display:</strong> {rec.display || 'N/A'}
                        </div>
                      </div>
                      
                      <div className="rec-pricing">
                        <div className="price">
                          {parsePrice(rec.price_details)}
                        </div>
                      </div>
                      
                      {rec.match_reasons && rec.match_reasons.length > 0 && (
                        <div className="rec-reasons">
                          <strong>Why this matches:</strong>
                          <ul>
                            {rec.match_reasons.map((reason, idx) => (
                              <li key={idx}>{reason}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="rec-summary">
                        {rec.review_summary}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 'explore':
        return <ExploreCompare />;

      case 'reviews':
        return <ReviewsIntelligence />;

      default:
        return null;
    }
  };

  return (
    <div className="chat-recommend">
      <div className="container">
        <div className="page-header">
          <h1>Cross-Marketplace Laptop & Review Intelligence</h1>
        </div>

        <div className="mode-tabs">
          <button 
            className={`mode-tab ${activeMode === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveMode('chat')}
          >
            Chat Assistant
          </button>
          <button 
            className={`mode-tab ${activeMode === 'recommend' ? 'active' : ''}`}
            onClick={() => setActiveMode('recommend')}
          >
            Get Recommendations
          </button>
          <button 
            className={`mode-tab ${activeMode === 'explore' ? 'active' : ''}`}
            onClick={() => setActiveMode('explore')}
          >
            Explore & Compare
          </button>
          <button 
            className={`mode-tab ${activeMode === 'reviews' ? 'active' : ''}`}
            onClick={() => setActiveMode('reviews')}
          >
            Reviews Intelligence
          </button>
        </div>

        {renderActiveMode()}
      </div>
    </div>
  );
};

export default ChatRecommend;