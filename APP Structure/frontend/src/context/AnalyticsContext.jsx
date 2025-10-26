/**
 * Analytics Context
 * Analytics and metrics state management
 */

import React, { createContext, useContext, useState, useEffect } from 'react'
import { analyticsApi } from '@services/api'

const AnalyticsContext = createContext(null)

export const AnalyticsProvider = ({ children }) => {
  const [dashboardMetrics, setDashboardMetrics] = useState(null)
  const [efficiencyMetrics, setEfficiencyMetrics] = useState(null)
  const [loading, setLoading] = useState(false)
  const [lastUpdated, setLastUpdated] = useState(null)

  /**
   * Fetch dashboard metrics
   */
  const fetchDashboardMetrics = async () => {
    setLoading(true)
    try {
      const response = await analyticsApi.getDashboard()
      setDashboardMetrics(response.metrics)
      setLastUpdated(new Date())
    } catch (error) {
      console.error('Failed to fetch dashboard metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Fetch efficiency metrics
   */
  const fetchEfficiencyMetrics = async () => {
    setLoading(true)
    try {
      const response = await analyticsApi.getEfficiencyMetrics()
      setEfficiencyMetrics(response.metrics)
    } catch (error) {
      console.error('Failed to fetch efficiency metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Refresh all metrics
   */
  const refreshMetrics = async () => {
    await Promise.all([
      fetchDashboardMetrics(),
      fetchEfficiencyMetrics()
    ])
  }

  /**
   * Auto-refresh metrics every 30 seconds
   */
  useEffect(() => {
    fetchDashboardMetrics()
    fetchEfficiencyMetrics()

    const interval = setInterval(() => {
      fetchDashboardMetrics()
    }, 30000)

    return () => clearInterval(interval)
  }, [])

  const value = {
    dashboardMetrics,
    efficiencyMetrics,
    loading,
    lastUpdated,
    refreshMetrics,
    fetchDashboardMetrics,
    fetchEfficiencyMetrics
  }

  return <AnalyticsContext.Provider value={value}>{children}</AnalyticsContext.Provider>
}

export const useAnalytics = () => {
  const context = useContext(AnalyticsContext)
  if (!context) {
    throw new Error('useAnalytics must be used within AnalyticsProvider')
  }
  return context
}
