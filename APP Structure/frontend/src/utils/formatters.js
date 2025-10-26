/**
 * Formatters
 * Utility functions for formatting data
 */

/**
 * Format currency
 */
export const formatCurrency = (amount, currency = 'USD', decimals = 2) => {
  const symbols = {
    USD: '$',
    EUR: '€',
    GBP: '£',
    ETH: 'Ξ'
  }

  const symbol = symbols[currency] || '$'
  return `${symbol}${Number(amount).toFixed(decimals)}`
}

/**
 * Format number with commas
 */
export const formatNumber = (num, decimals = 0) => {
  return Number(num).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}

/**
 * Format percentage
 */
export const formatPercentage = (value, decimals = 1) => {
  return `${Number(value).toFixed(decimals)}%`
}

/**
 * Format energy quantity
 */
export const formatEnergy = (kwh) => {
  return `${formatNumber(kwh, 2)} kWh`
}

/**
 * Format date
 */
export const formatDate = (date, format = 'short') => {
  const d = new Date(date)
  
  if (format === 'short') {
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  } else if (format === 'long') {
    return d.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    })
  } else if (format === 'time') {
    return d.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } else if (format === 'datetime') {
    return d.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  return d.toLocaleDateString()
}

/**
 * Format time ago
 */
export const formatTimeAgo = (date) => {
  const now = new Date()
  const past = new Date(date)
  const diffInSeconds = Math.floor((now - past) / 1000)

  if (diffInSeconds < 60) {
    return `${diffInSeconds}s ago`
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60)
    return `${minutes}m ago`
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600)
    return `${hours}h ago`
  } else {
    const days = Math.floor(diffInSeconds / 86400)
    return `${days}d ago`
  }
}

/**
 * Format hash (truncate)
 */
export const formatHash = (hash, length = 8) => {
  if (!hash) return 'N/A'
  if (hash.length <= length) return hash
  return `${hash.slice(0, length)}...`
}

/**
 * Capitalize first letter
 */
export const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

/**
 * Format energy type
 */
export const formatEnergyType = (type) => {
  return capitalize(type)
}

/**
 * Format status
 */
export const formatStatus = (status) => {
  return capitalize(status.replace('_', ' '))
}
