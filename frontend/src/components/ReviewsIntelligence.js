import React, { useState, useEffect } from 'react';
import { reviewsAPI } from '../services/api';
import './ReviewsIntelligence.css';

const ReviewsIntelligence = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTimeframe, setSelectedTimeframe] = useState('30d');
  const [selectedBrand, setSelectedBrand] = useState('all');
  
  // Data states
  const [volumeTrends, setVolumeTrends] = useState([]);
  const [ratingTrends, setRatingTrends] = useState([]);
  const [topThemes, setTopThemes] = useState([]);
  const [topAttributes, setTopAttributes] = useState([]);
  const [ratingDistribution, setRatingDistribution] = useState([]);
  const [brandComparison, setBrandComparison] = useState([]);
  const [reviewStats, setReviewStats] = useState({});

  useEffect(() => {
    loadReviewsData();
  }, [selectedTimeframe, selectedBrand]);

  const loadReviewsData = async () => {
    setLoading(true);
    try {
      // Load all reviews data
      const [reviewsRes, volumeRes, ratingRes, themesRes, attributesRes, distributionRes, comparisonRes, statsRes] = await Promise.all([
        reviewsAPI.getAll(),
        reviewsAPI.getVolumeTrends(selectedTimeframe, selectedBrand),
        reviewsAPI.getRatingTrends(selectedTimeframe, selectedBrand),
        reviewsAPI.getTopThemes(selectedBrand),
        reviewsAPI.getTopAttributes(selectedBrand),
        reviewsAPI.getRatingDistribution(selectedBrand),
        reviewsAPI.getBrandComparison(),
        reviewsAPI.getStats()
      ]);

      setReviews(reviewsRes.data.data?.reviews || []);
      setVolumeTrends(volumeRes.data.data || []);
      setRatingTrends(ratingRes.data.data || []);
      setTopThemes(themesRes.data.data || []);
      setTopAttributes(attributesRes.data.data || []);
      setRatingDistribution(distributionRes.data.data || []);
      // Filter out Dell and Apple from brand comparison
      const filteredBrandComparison = (comparisonRes.data.data || []).filter(brand => 
        brand.brand && !brand.brand.toLowerCase().includes('dell') && !brand.brand.toLowerCase().includes('apple')
      );
      setBrandComparison(filteredBrandComparison);
      setReviewStats(statsRes.data.data || {});
    } catch (error) {
      console.error('Error loading reviews data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getThemeColor = (index) => {
    return '#4682b4'; // Steel blue for all themes and attributes
  };

  const getAttributeIcon = (attribute) => {
    const icons = {
      'performance': '⚡',
      'battery': '🔋',
      'display': '🖥️',
      'build': '🏗️',
      'price': '💰',
      'portability': '📱',
      'keyboard': '⌨️',
      'trackpad': '🖱️',
      'audio': '🔊',
      'connectivity': '🔌'
    };
    return icons[attribute.toLowerCase()] || '⭐';
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined || isNaN(num)) return '0';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const getRatingColor = (rating) => {
    if (rating >= 4.5) return '#1e3c72';
    if (rating >= 4.0) return '#2a5298';
    if (rating >= 3.5) return '#3b82f6';
    if (rating >= 3.0) return '#60a5fa';
    return '#93c5fd';
  };

  return (
    <div className="reviews-intelligence">
      <div className="container">

        {/* Controls */}
        <div className="controls-section">
          <div className="controls-grid">
            <div className="form-group">
              <label>Timeframe</label>
              <select
                value={selectedTimeframe}
                onChange={(e) => setSelectedTimeframe(e.target.value)}
                className="form-control"
              >
                <option value="7d">Last 7 days</option>
                <option value="30d">Last 30 days</option>
                <option value="90d">Last 90 days</option>
                <option value="1y">Last year</option>
                <option value="all">All time</option>
              </select>
            </div>

            <div className="form-group">
              <label>Brand Filter</label>
              <select
                value={selectedBrand}
                onChange={(e) => setSelectedBrand(e.target.value)}
                className="form-control"
              >
                <option value="all">All Brands</option>
                <option value="lenovo">Lenovo</option>
                <option value="hp">HP</option>
              </select>
            </div>

            <div className="form-group">
              <button 
                className="btn"
                onClick={loadReviewsData}
                disabled={loading}
              >
                {loading ? 'Loading...' : 'Refresh Data'}
              </button>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading reviews intelligence data...</div>
        ) : (
          <div className="intelligence-content">
            {/* Overview Cards */}
            <div className="overview-cards">
              <div className="overview-card">
                <div className="card-icon">📊</div>
                <div className="card-content">
                  <h3>{formatNumber(reviews.length)}</h3>
                  <p>Total Reviews</p>
                </div>
              </div>

              <div className="overview-card">
                <div className="card-icon">⭐</div>
                <div className="card-content">
                  <h3>
                    {reviewStats.average_rating || '0.0'}
                  </h3>
                  <p>Average Rating</p>
                </div>
              </div>

              <div className="overview-card">
                <div className="card-icon">📈</div>
                <div className="card-content">
                  <h3>{volumeTrends.length > 0 ? formatNumber(volumeTrends[volumeTrends.length - 1]?.volume || 0) : '0'}</h3>
                  <p>Recent Volume</p>
                </div>
              </div>

              <div className="overview-card">
                <div className="card-icon">🎯</div>
                <div className="card-content">
                  <h3>{topThemes.length}</h3>
                  <p>Key Themes</p>
                </div>
              </div>
            </div>

            {/* Charts Section */}
            <div className="charts-section">
              {/* Volume Trends */}
              <div className="chart-card">
                <h3>Review Volume Trends</h3>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'end', 
                  gap: '10px', 
                  height: '200px', 
                  padding: '20px 0',
                  border: '1px solid #eee'
                }}>
                  {volumeTrends.length > 0 ? volumeTrends.map((trend, index) => {
                    const maxVolume = Math.max(...volumeTrends.map(t => t.volume || 0));
                    const heightPx = maxVolume > 0 ? Math.max(20, ((trend.volume || 0) / maxVolume) * 150) : 20;
                    return (
                      <div key={index} style={{ 
                        display: 'flex', 
                        flexDirection: 'column', 
                        alignItems: 'center', 
                        flex: 1,
                        gap: '5px'
                      }}>
                        <div style={{ fontSize: '12px', color: '#666' }}>{trend.period}</div>
                        <div style={{ 
                          width: '100%', 
                          height: '150px', 
                          display: 'flex', 
                          alignItems: 'end', 
                          justifyContent: 'center' 
                        }}>
                          <div 
                            style={{ 
                              width: '80%',
                              height: `${heightPx}px`,
                              backgroundColor: '#1e3c72',
                              borderRadius: '4px 4px 0 0',
                              minHeight: '20px',
                              border: '1px solid #1e3c72'
                            }}
                          ></div>
                        </div>
                        <div style={{ fontSize: '12px', fontWeight: 'bold' }}>{formatNumber(trend.volume)}</div>
                      </div>
                    );
                  }) : <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>No volume trends data available</div>}
                </div>
              </div>

              {/* Rating Distribution */}
              <div className="chart-card">
                <h3>Rating Distribution</h3>
                <div className="rating-distribution">
                  {ratingDistribution.map((dist, index) => (
                    <div key={index} className="rating-bar">
                      <div className="rating-label">
                        {dist.rating} ⭐
                      </div>
                      <div className="rating-container">
                        <div 
                          className="rating-fill"
                          style={{ 
                            width: `${((dist.count || 0) / Math.max(...ratingDistribution.map(d => d.count || 0))) * 100}%`,
                            backgroundColor: getRatingColor(dist.rating)
                          }}
                        ></div>
                      </div>
                      <div className="rating-count">{dist.count}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Themes and Attributes */}
            <div className="analysis-section">
              {/* Top Themes */}
              <div className="analysis-card">
                <h3>Top Review Themes</h3>
                <div className="themes-grid">
                  {topThemes.map((theme, index) => (
                    <div key={index} className="theme-item">
                      <div className="theme-header">
                        <span 
                          className="theme-color"
                          style={{ backgroundColor: getThemeColor(index) }}
                        ></span>
                        <span className="theme-name">{theme.theme}</span>
                        <span className="theme-count">{theme.count}</span>
                      </div>
                      <div className="theme-bar">
                        <div 
                          className="theme-fill"
                          style={{ 
                            width: `${((theme.count || 0) / Math.max(...topThemes.map(t => t.count || 0))) * 100}%`,
                            backgroundColor: getThemeColor(index)
                          }}
                        ></div>
                      </div>
                      <div className="theme-sentiment">
                        <span className={`sentiment-badge ${theme.sentiment}`}>
                          {theme.sentiment}
                        </span>
                        <span className="sentiment-score">
                          {(theme.sentiment_score || 0).toFixed(1)}/5
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Attributes */}
              <div className="analysis-card">
                <h3>Key Product Attributes</h3>
                <div className="attributes-grid">
                  {topAttributes.map((attr, index) => (
                    <div key={index} className="attribute-item">
                      <div className="attribute-header">
                        <span className="attribute-icon">
                          {getAttributeIcon(attr.attribute)}
                        </span>
                        <span className="attribute-name">{attr.attribute}</span>
                        <span className="attribute-mentions">{attr.mentions}</span>
                      </div>
                      <div className="attribute-bar">
                        <div 
                          className="attribute-fill"
                          style={{ 
                            width: `${((attr.mentions || 0) / Math.max(...topAttributes.map(a => a.mentions || 0))) * 100}%`,
                            backgroundColor: getThemeColor(index + 3)
                          }}
                        ></div>
                      </div>
                      <div className="attribute-sentiment">
                        <span className={`sentiment-badge ${attr.sentiment}`}>
                          {attr.sentiment}
                        </span>
                        <span className="sentiment-score">
                          {(attr.avg_rating || 0).toFixed(1)}/5
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Brand Comparison */}
            <div className="comparison-section">
              <h3>Brand Performance Comparison</h3>
              <div className="comparison-grid">
                {brandComparison.map((brand, index) => (
                  <div key={index} className="brand-card">
                    <div className="brand-header">
                      <h4>{brand.brand}</h4>
                      <div className="brand-rating">
                        <span className="rating-value" style={{ color: getRatingColor(brand.avg_rating || 0) }}>
                          {(brand.avg_rating || 0).toFixed(1)}
                        </span>
                        <span className="rating-stars">⭐</span>
                      </div>
                    </div>
                    
                    <div className="brand-stats">
                      <div className="stat-item">
                        <span className="stat-label">Reviews:</span>
                        <span className="stat-value">{formatNumber(brand.review_count)}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Volume:</span>
                        <span className="stat-value">{formatNumber(brand.volume)}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Top Theme:</span>
                        <span className="stat-value">{brand.top_theme}</span>
                      </div>
                    </div>

                    <div className="brand-sentiment">
                      <div className="sentiment-breakdown">
                        <div className="sentiment-item positive">
                          <span>Positive: {brand.positive_percentage}%</span>
                        </div>
                        <div className="sentiment-item neutral">
                          <span>Neutral: {brand.neutral_percentage}%</span>
                        </div>
                        <div className="sentiment-item negative">
                          <span>Negative: {brand.negative_percentage}%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReviewsIntelligence;
