/**
 * usePredictions Hook
 * Manages AI predictions and forecasts
 */

import { useState, useEffect, useCallback } from 'react'
import aiService from '@services/aiService'

export const usePredictions = (energyType = null, autoFetch = true) => {
  const [predictions, setPredictions] = useState(null)
  const [demand, setDemand] = useState(null)
  const [trends, setTrends] = useState(null)
  const [volatility, setVolatility] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetch price predictions
   */
  const fetchPricePredictions = useCallback(async (type, horizon = 24) => {
    setLoading(true)
    setError(null)

    try {
      const data = await aiService.predictPrices(type, horizon)
      setPredictions(data)
      return data
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch predictions:', err)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Fetch demand forecast
   */
  const fetchDemandForecast = useCallback(async (type, period = 'day') => {
    setLoading(true)
    setError(null)

    try {
      const data = await aiService.forecastDemand(type, period)
      setDemand(data)
      return data
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch demand:', err)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Fetch market trends
   */
  const fetchTrends = useCallback(async (type = null) => {
    setLoading(true)
    setError(null)

    try {
      const data = await aiService.analyzeTrends(type)
      setTrends(data)
      return data
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch trends:', err)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Fetch volatility
   */
  const fetchVolatility = useCallback(async (type) => {
    setLoading(true)
    setError(null)

    try {
      const data = await aiService.getVolatility(type)
      setVolatility(data)
      return data
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch volatility:', err)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Fetch all data for energy type
   */
  const fetchAll = useCallback(async (type) => {
    setLoading(true)
    setError(null)

    try {
      const [priceData, demandData, trendData, volatilityData] = await Promise.all([
        aiService.predictPrices(type, 24),
        aiService.forecastDemand(type, 'day'),
        aiService.analyzeTrends(type),
        aiService.getVolatility(type)
      ])

      setPredictions(priceData)
      setDemand(demandData)
      setTrends(trendData)
      setVolatility(volatilityData)

      return { priceData, demandData, trendData, volatilityData }
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch all data:', err)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Clear cache
   */
  const clearCache = useCallback(() => {
    aiService.clearCache()
  }, [])

  /**
   * Auto-fetch on mount
   */
  useEffect(() => {
    if (autoFetch && energyType) {
      fetchAll(energyType)
    }
  }, [autoFetch, energyType, fetchAll])

  return {
    predictions,
    demand,
    trends,
    volatility,
    loading,
    error,
    fetchPricePredictions,
    fetchDemandForecast,
    fetchTrends,
    fetchVolatility,
    fetchAll,
    clearCache
  }
}
