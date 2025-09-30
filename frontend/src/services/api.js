/**
 * Copyright (c) 2025 Bhagya Dissanayake
 * All rights reserved. This code is proprietary and confidential.
 * Unauthorized copying, distribution, or use is strictly prohibited.
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Recommendations API
export const recommendationsAPI = {
  getConstraintBased: (constraints) => api.post('/recommendations/constraint-based', { constraints }),
  getSimilar: (id, limit = 5) => api.get(`/recommendations/similar/${id}`, { params: { limit } }),
  getTrending: (limit = 5) => api.get('/recommendations/trending', { params: { limit } }),
  getBudget: (maxPrice) => api.get(`/recommendations/budget/${maxPrice}`),
  getBrand: (brand) => api.get(`/recommendations/brand/${brand}`),
  getUseCase: (data) => api.post('/recommendations/use-case', data),
};

// Chat API
export const chatAPI = {
  query: (query, context = '') => api.post('/chat/query', { query, context }, { timeout: 60000 }), // 60 seconds
  recommend: (constraints) => api.post('/chat/recommend', { constraints }, { timeout: 60000 }), // 60 seconds
  compare: (laptopIds) => api.post('/chat/compare', { laptop_ids: laptopIds }, { timeout: 60000 }), // 60 seconds
};

// Explore API
export const exploreAPI = {
  getAll: () => api.get('/explore/'),
  getFilterOptions: () => api.get('/explore/filter-options'),
  getPriceTrends: () => api.get('/explore/price-trends'),
  getAvailability: () => api.get('/explore/availability'),
  search: (params) => api.get('/explore/search', { params }),
  getById: (id) => api.get(`/explore/${id}`),
  getSpecifications: (id) => api.get(`/explore/${id}/specifications`),
};

// Reviews API
export const reviewsAPI = {
  getAll: () => api.get('/reviews/'),
  getVolumeTrends: (timeframe = '30d', brand = 'all') => api.get('/reviews/volume-trends', { params: { timeframe, brand } }),
  getRatingTrends: (timeframe = '30d', brand = 'all') => api.get('/reviews/rating-trends', { params: { timeframe, brand } }),
  getTopThemes: (brand = 'all') => api.get('/reviews/top-themes', { params: { brand } }),
  getTopAttributes: (brand = 'all') => api.get('/reviews/top-attributes', { params: { brand } }),
  getRatingDistribution: (brand = 'all') => api.get('/reviews/rating-distribution', { params: { brand } }),
  getBrandComparison: () => api.get('/reviews/brand-comparison'),
  getStats: () => api.get('/reviews/stats'),
};

// Health check
export const healthAPI = {
  check: () => api.get('/health'),
  info: () => api.get('/info'),
};

export default api;