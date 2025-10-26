/**
 * Constants
 * Application constants and configuration
 */

// Energy types
export const ENERGY_TYPES = [
  { value: 'solar', label: 'Solar', color: '#f59e0b' },
  { value: 'wind', label: 'Wind', color: '#3b82f6' },
  { value: 'hydro', label: 'Hydro', color: '#06b6d4' },
  { value: 'biomass', label: 'Biomass', color: '#10b981' }
]

// Order types
export const ORDER_TYPES = [
  { value: 'buy', label: 'Buy' },
  { value: 'sell', label: 'Sell' }
]

// Transaction statuses
export const TRANSACTION_STATUSES = {
  pending: { label: 'Pending', color: '#f59e0b' },
  matched: { label: 'Matched', color: '#3b82f6' },
  completed: { label: 'Completed', color: '#10b981' },
  cancelled: { label: 'Cancelled', color: '#ef4444' }
}

// Contract statuses
export const CONTRACT_STATUSES = {
  pending: { label: 'Pending', color: '#f59e0b' },
  active: { label: 'Active', color: '#3b82f6' },
  completed: { label: 'Completed', color: '#10b981' },
  failed: { label: 'Failed', color: '#ef4444' }
}

// Time periods
export const TIME_PERIODS = [
  { value: '7d', label: 'Last 7 Days' },
  { value: '30d', label: 'Last 30 Days' },
  { value: '90d', label: 'Last 90 Days' }
]

// Chart colors
export const CHART_COLORS = {
  primary: '#21808d',
  secondary: '#5e6c64',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6'
}

// Performance metrics
export const PERFORMANCE_TARGETS = {
  transactionEfficiency: 35,
  verificationReduction: 60,
  weeklyTransactions: 1200,
  successRate: 99.9,
  uptime: 99.9
}

// API endpoints
export const API_ENDPOINTS = {
  trades: '/api/trades',
  analytics: '/api/analytics',
  contracts: '/api/contracts',
  predictions: '/api/predictions'
}

// WebSocket events
export const WS_EVENTS = {
  connect: 'connect',
  disconnect: 'disconnect',
  tradeMatched: 'trade_matched',
  contractExecuted: 'contract_executed',
  priceUpdate: 'price_update',
  marketUpdate: 'market_update',
  notification: 'notification'
}

// Local storage keys
export const STORAGE_KEYS = {
  authToken: 'auth_token',
  user: 'user_data',
  theme: 'theme_preference',
  language: 'language_preference'
}
