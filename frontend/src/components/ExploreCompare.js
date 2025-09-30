import React, { useState, useEffect } from 'react';
import { exploreAPI } from '../services/api';
import './ExploreCompare.css';

const ExploreCompare = () => {
  const [laptops, setLaptops] = useState([]);
  const [filteredLaptops, setFilteredLaptops] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedLaptops, setSelectedLaptops] = useState([]);
  const [showComparison, setShowComparison] = useState(false);
  const [priceTrends, setPriceTrends] = useState([]);
  const [availability, setAvailability] = useState([]);

  // Filter states
  const [filters, setFilters] = useState({
    brand: '',
    minPrice: '',
    maxPrice: '',
    minRating: '',
    processor: '',
    memory: '',
    storage: '',
    display: ''
  });

  // Available filter options
  const [filterOptions, setFilterOptions] = useState({
    brands: [],
    processors: [],
    memory: [],
    storage: [],
    displays: []
  });

  useEffect(() => {
    loadLaptops();
    loadFilterOptions();
    loadPriceTrends();
    loadAvailability();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters, laptops]);

  const loadLaptops = async () => {
    setLoading(true);
    try {
      const response = await exploreAPI.getAll();
      console.log('API Response:', response.data);
      console.log('First few laptops:', response.data.data?.laptops?.slice(0, 3));
      setLaptops(response.data.data?.laptops || []);
    } catch (error) {
      console.error('Error loading laptops:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadFilterOptions = async () => {
    try {
      const response = await exploreAPI.getFilterOptions();
      setFilterOptions(response.data.data || {});
    } catch (error) {
      console.error('Error loading filter options:', error);
    }
  };

  const loadPriceTrends = async () => {
    try {
      const response = await exploreAPI.getPriceTrends();
      setPriceTrends(response.data.data?.trends || []);
    } catch (error) {
      console.error('Error loading price trends:', error);
    }
  };

  const loadAvailability = async () => {
    try {
      const response = await exploreAPI.getAvailability();
      setAvailability(response.data.data?.availability || []);
    } catch (error) {
      console.error('Error loading availability:', error);
    }
  };

  const applyFilters = () => {
    let filtered = [...laptops];

    if (filters.brand) {
      filtered = filtered.filter(laptop => 
        laptop.brand?.toLowerCase().includes(filters.brand.toLowerCase())
      );
    }

    if (filters.minPrice) {
      filtered = filtered.filter(laptop => {
        const price = parseLaptopPrice(laptop.price_details);
        return price >= parseFloat(filters.minPrice);
      });
    }

    if (filters.maxPrice) {
      filtered = filtered.filter(laptop => {
        const price = parseLaptopPrice(laptop.price_details);
        return price <= parseFloat(filters.maxPrice);
      });
    }

    if (filters.minRating) {
      filtered = filtered.filter(laptop => {
        const rating = parseLaptopRating(laptop.review_details || laptop['Review Details']);
        return rating >= parseFloat(filters.minRating);
      });
    }

    if (filters.processor) {
      filtered = filtered.filter(laptop => 
        laptop.processor?.toLowerCase().includes(filters.processor.toLowerCase())
      );
    }

    if (filters.memory) {
      filtered = filtered.filter(laptop => 
        laptop.memory?.toLowerCase().includes(filters.memory.toLowerCase())
      );
    }

    if (filters.storage) {
      filtered = filtered.filter(laptop => 
        laptop.storage?.toLowerCase().includes(filters.storage.toLowerCase())
      );
    }

    if (filters.display) {
      filtered = filtered.filter(laptop => 
        laptop.display?.toLowerCase().includes(filters.display.toLowerCase())
      );
    }

    setFilteredLaptops(filtered);
  };

  const parseLaptopPrice = (priceDetails) => {
    console.log('Parsing price details:', priceDetails, typeof priceDetails); // Add this debug line
    try {
      let priceObj;
      
      // Handle both string and object inputs
      if (typeof priceDetails === 'string') {
        priceObj = JSON.parse(priceDetails);
      } else if (typeof priceDetails === 'object' && priceDetails !== null) {
        priceObj = priceDetails;
      } else {
        return 0;
      }
      
      const priceStr = priceObj['Current Price'] || '0';
      console.log('Price string:', priceStr); // Add this debug line
      
      // Handle "Not Available" and other non-numeric values
      if (priceStr === 'Not Available' || priceStr === 'N/A' || priceStr === '') {
        return 0;
      }
      
      const numericPrice = parseFloat(priceStr.replace(/[$,]/g, ''));
      console.log('Numeric price:', numericPrice); // Add this debug line
      return isNaN(numericPrice) ? 0 : numericPrice;
    } catch (error) {
      console.log('Price parsing error:', error); // Add this debug line
      return 0;
    }
  };

  const parseLaptopRating = (reviewDetails) => {
    try {
      // Handle null, undefined, or empty values
      if (!reviewDetails || reviewDetails === '-' || reviewDetails === '{}') {
        return 0;
      }

      // If it's a plain text rating like "4.2 out of 5 stars, 48 reviews."
      if (typeof reviewDetails === 'string' && reviewDetails.includes('out of 5 stars')) {
        const match = reviewDetails.match(/(\d+\.?\d*)\s+out of 5 stars/);
        if (match) {
          return parseFloat(match[1]) || 0;
        }
      }

      // If it's a JSON string, try to parse it
      let reviewObj;
      if (typeof reviewDetails === 'string') {
        try {
          reviewObj = JSON.parse(reviewDetails);
        } catch {
          // If JSON parsing fails, return 0
          return 0;
        }
      } else if (typeof reviewDetails === 'object' && reviewDetails !== null) {
        reviewObj = reviewDetails;
      } else {
        return 0;
      }
      
      const ratingStr = reviewObj['Overall Rating'] || '0';
      // Extract numeric rating from strings like "4.5/5 (116 reviews)"
      const numericRating = parseFloat(ratingStr.split('/')[0]) || 0;
      return numericRating;
    } catch {
      return 0;
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    setFilters({
      brand: '',
      minPrice: '',
      maxPrice: '',
      minRating: '',
      processor: '',
      memory: '',
      storage: '',
      display: ''
    });
  };

  const toggleLaptopSelection = (laptop) => {
    setSelectedLaptops(prev => {
      const isSelected = prev.some(l => l.laptop_id === laptop.laptop_id);
      if (isSelected) {
        return prev.filter(l => l.laptop_id !== laptop.laptop_id);
      } else {
        return [...prev, laptop];
      }
    });
  };

  const compareSelected = () => {
    if (selectedLaptops.length >= 2) {
      setShowComparison(true);
    }
  };


  return (
    <div className="explore-compare">
      <div className="container">

        <div className="explore-content">
          {/* Filters Section */}
          <div className="filters-section">
            <div className="filters-header">
              <h3>Filters</h3>
              <button className="btn btn-secondary" onClick={clearFilters}>
                Clear All
              </button>
            </div>

            <div className="filters-grid">
              <div className="form-group">
                <label>Brand</label>
                <select
                  value={filters.brand}
                  onChange={(e) => handleFilterChange('brand', e.target.value)}
                  className="form-control"
                >
                  <option value="">All Brands</option>
                  {filterOptions.brands?.map(brand => (
                    <option key={brand} value={brand}>{brand}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Min Price ($)</label>
                <input
                  type="number"
                  value={filters.minPrice}
                  onChange={(e) => handleFilterChange('minPrice', e.target.value)}
                  className="form-control"
                  placeholder="0"
                />
              </div>

              <div className="form-group">
                <label>Max Price ($)</label>
                <input
                  type="number"
                  value={filters.maxPrice}
                  onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
                  className="form-control"
                  placeholder="5000"
                />
              </div>

              <div className="form-group">
                <label>Min Rating</label>
                <select
                  value={filters.minRating}
                  onChange={(e) => handleFilterChange('minRating', e.target.value)}
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
                <label>Processor</label>
                <select
                  value={filters.processor}
                  onChange={(e) => handleFilterChange('processor', e.target.value)}
                  className="form-control"
                >
                  <option value="">All Processors</option>
                  {filterOptions.processors?.map(processor => (
                    <option key={processor} value={processor}>{processor}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Memory</label>
                <select
                  value={filters.memory}
                  onChange={(e) => handleFilterChange('memory', e.target.value)}
                  className="form-control"
                >
                  <option value="">All Memory</option>
                  {filterOptions.memory?.map(memory => (
                    <option key={memory} value={memory}>{memory}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Storage</label>
                <select
                  value={filters.storage}
                  onChange={(e) => handleFilterChange('storage', e.target.value)}
                  className="form-control"
                >
                  <option value="">All Storage</option>
                  {filterOptions.storage?.map(storage => (
                    <option key={storage} value={storage}>{storage}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Display</label>
                <select
                  value={filters.display}
                  onChange={(e) => handleFilterChange('display', e.target.value)}
                  className="form-control"
                >
                  <option value="">All Displays</option>
                  {filterOptions.displays?.map(display => (
                    <option key={display} value={display}>{display}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="results-section">
            <div className="results-header">
              <h3>Results ({filteredLaptops.length} laptops)</h3>
              <div className="results-actions">
                <span className="selected-count">
                  {selectedLaptops.length} selected
                </span>
                <button 
                  className="btn"
                  onClick={compareSelected}
                  disabled={selectedLaptops.length < 2}
                >
                  Compare Selected
                </button>
              </div>
            </div>

            {loading ? (
              <div className="loading">Loading laptops...</div>
            ) : (
              <div className="laptops-grid">
                {filteredLaptops.map((laptop, index) => (
                  <div 
                    key={laptop.laptop_id || `laptop-${index}`} 
                    className={`laptop-card ${selectedLaptops.some(l => l.laptop_id === laptop.laptop_id) ? 'selected' : ''}`}
                    onClick={() => toggleLaptopSelection(laptop)}
                  >
                    <div className="card-header">
                      <h4>{laptop.brand} {laptop.model}</h4>
                      <div className="card-actions">
                        <input 
                          type="checkbox" 
                          checked={selectedLaptops.some(l => l.laptop_id === laptop.laptop_id)}
                          onChange={() => toggleLaptopSelection(laptop)}
                          onClick={(e) => e.stopPropagation()}
                        />
                      </div>
                    </div>

                    <div className="card-specs">
                      <div className="spec-item">
                        <strong>Processor:</strong> {laptop.processor || 'N/A'}
                      </div>
                      <div className="spec-item">
                        <strong>Memory:</strong> {laptop.memory || 'N/A'}
                      </div>
                      <div className="spec-item">
                        <strong>Storage:</strong> {laptop.storage || 'N/A'}
                      </div>
                      <div className="spec-item">
                        <strong>Display:</strong> {laptop.display || 'N/A'}
                      </div>
                    </div>

                    <div className="card-pricing">
                      <div className="price">
                        {(() => {
                          const price = parseLaptopPrice(laptop.price_details);
                          if (price === 0) {
                            return 'Price Not Available';
                          }
                          return `$${price.toLocaleString()}`;
                        })()}
                      </div>
                      <div className="rating">
                        ⭐ {parseLaptopRating(laptop.review_details || laptop['Review Details']).toFixed(1)}
                      </div>
                    </div>

                    <div className="card-actions">
                      <button 
                        className="btn btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          // TODO: Open detailed view
                        }}
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Price Trends Section */}
          <div className="trends-section">
            <h3>Price Trends</h3>
            <div className="trends-grid">
              {priceTrends.slice(0, 6).map(trend => (
                <div key={trend.laptop_id} className="trend-card">
                  <h4>{trend.brand} {trend.model}</h4>
                  <div className="trend-chart">
                    <div className="trend-bar">
                      <div 
                        className="trend-fill"
                        style={{ 
                          width: `${Math.min(100, (trend.price_change / 100) * 100)}%`,
                          backgroundColor: trend.price_change > 0 ? '#ff4757' : '#00d4aa'
                        }}
                      ></div>
                    </div>
                    <span className="trend-value">
                      {trend.price_change > 0 ? '+' : ''}{trend.price_change.toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExploreCompare;
