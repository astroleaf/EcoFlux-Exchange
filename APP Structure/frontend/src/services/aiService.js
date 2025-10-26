/**
 * AI Service
 * Handles AI predictions and analytics
 */

import { predictionApi } from './api'

class AIService {
  constructor() {
    this.cache = new Map()
    this.cacheTTL = 5 * 60 * 1000 // 5 minutes
  }

  /**
   * Get cached data or fetch new
   */
  async getCached(key, fetchFn) {
    const cached = this.cache.get(key)
    
    if (cached && Date.now() - cached.timestamp < this.cacheTTL) {
      return cached.data
    }

    const data = await fetchFn()
    this.cache.set(key, { data, timestamp: Date.now() })
    
    return data
  }

  /**
   * Predict energy prices
   */
  async predictPrices(energyType, horizon = 24) {
    const cacheKey = `price_${energyType}_${horizon}`
    
    return this.getCached(cacheKey, async () => {
      const response = await predictionApi.predictPrice(energyType, horizon)
      return response.prediction
    })
  }

  /**
   * Forecast demand
   */
  async forecastDemand(energyType, period = 'day') {
    const cacheKey = `demand_${energyType}_${period}`
    
    return this.getCached(cacheKey, async () => {
      const response = await predictionApi.forecastDemand(energyType, period)
      return response.forecast
    })
  }

  /**
   * Analyze market trends
   */
  async analyzeTrends(energyType = null) {
    const cacheKey = `trends_${energyType || 'all'}`
    
    return this.getCached(cacheKey, async () => {
      const response = await predictionApi.analyzeTrends(energyType)
      return response.trends
    })
  }

  /**
   * Get market outlook
   */
  async getMarketOutlook() {
    const cacheKey = 'market_outlook'
    
    return this.getCached(cacheKey, async () => {
      const response = await predictionApi.getMarketOutlook()
      return response.outlook
    })
  }

  /**
   * Get price volatility
   */
  async getVolatility(energyType) {
    const cacheKey = `volatility_${energyType}`
    
    return this.getCached(cacheKey, async () => {
      const response = await predictionApi.getVolatility(energyType)
      return response.volatility
    })
  }

  /**
   * Get all predictions for dashboard
   */
  async getAllPredictions() {
    const energyTypes = ['solar', 'wind', 'hydro', 'biomass']
    
    const predictions = await Promise.all(
      energyTypes.map(async (type) => ({
        energyType: type,
        price: await this.predictPrices(type, 24),
        demand: await this.forecastDemand(type, 'day'),
        trend: await this.analyzeTrends(type)
      }))
    )

    return predictions
  }

  /**
   * Clear cache
   */
  clearCache() {
    this.cache.clear()
  }

  /**
   * Clear specific cache entry
   */
  clearCacheEntry(key) {
    this.cache.delete(key)
  }
}

// Create singleton instance
const aiService = new AIService()

export default aiService
