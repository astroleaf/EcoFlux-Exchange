/**
 * API Service
 * Handles all HTTP requests to the backend
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 30000

// Create axios instance
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      // Server responded with error
      const { status, data } = error.response
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('auth_token')
        window.location.href = '/login'
      }
      
      return Promise.reject({
        status,
        message: data.error || data.message || 'An error occurred',
        details: data.details
      })
    } else if (error.request) {
      // Request made but no response
      return Promise.reject({
        status: 0,
        message: 'Network error. Please check your connection.',
        details: error.message
      })
    } else {
      // Error setting up request
      return Promise.reject({
        status: 0,
        message: 'Request failed',
        details: error.message
      })
    }
  }
)

/**
 * Trade API
 */
export const tradeApi = {
  // Create new trade
  createTrade: (data) => apiClient.post('/trades/create', data),
  
  // List trades
  listTrades: (params = {}) => apiClient.get('/trades/list', { params }),
  
  // Get specific trade
  getTrade: (id) => apiClient.get(`/trades/${id}`),
  
  // Cancel trade
  cancelTrade: (id) => apiClient.post(`/trades/${id}/cancel`),
  
  // Get order book
  getOrderBook: (energyType) => apiClient.get('/trades/order-book', { 
    params: { energy_type: energyType } 
  }),
  
  // Get trade statistics
  getStats: () => apiClient.get('/trades/stats')
}

/**
 * Analytics API
 */
export const analyticsApi = {
  // Dashboard metrics
  getDashboard: () => apiClient.get('/analytics/dashboard'),
  
  // Price trends
  getPriceTrends: (period = '7d') => apiClient.get('/analytics/price-trends', { 
    params: { period } 
  }),
  
  // Market analysis
  getMarketAnalysis: () => apiClient.get('/analytics/market-analysis'),
  
  // Volume by type
  getVolumeByType: (period = '30d') => apiClient.get('/analytics/volume-by-type', { 
    params: { period } 
  }),
  
  // Efficiency metrics
  getEfficiencyMetrics: () => apiClient.get('/analytics/efficiency-metrics'),
  
  // Historical data
  getHistoricalData: (startDate, endDate) => apiClient.get('/analytics/historical-data', {
    params: { start_date: startDate, end_date: endDate }
  })
}

/**
 * Smart Contract API
 */
export const contractApi = {
  // Deploy contract
  deploy: (data) => apiClient.post('/contracts/deploy', data),
  
  // Execute contract
  execute: (contractId) => apiClient.post('/contracts/execute', { contract_id: contractId }),
  
  // Verify contract
  verify: (contractId, transactionHash) => apiClient.post('/contracts/verify', {
    contract_id: contractId,
    transaction_hash: transactionHash
  }),
  
  // List contracts
  list: (status) => apiClient.get('/contracts/list', { 
    params: { status } 
  }),
  
  // Get contract details
  getContract: (id) => apiClient.get(`/contracts/${id}`),
  
  // Get contract statistics
  getStats: () => apiClient.get('/contracts/stats')
}

/**
 * AI Predictions API
 */
export const predictionApi = {
  // Predict price
  predictPrice: (energyType, horizon = 24) => apiClient.post('/predictions/price', {
    energy_type: energyType,
    horizon
  }),
  
  // Forecast demand
  forecastDemand: (energyType, period = 'day') => apiClient.post('/predictions/demand', {
    energy_type: energyType,
    period
  }),
  
  // Analyze trends
  analyzeTrends: (energyType) => apiClient.get('/predictions/trends', {
    params: { energy_type: energyType }
  }),
  
  // Market outlook
  getMarketOutlook: () => apiClient.get('/predictions/market-outlook'),
  
  // Get volatility
  getVolatility: (energyType) => apiClient.get('/predictions/volatility', {
    params: { energy_type: energyType }
  })
}

/**
 * Health check
 */
export const healthApi = {
  check: () => axios.get(`${API_BASE_URL}/health`)
}

export default apiClient
