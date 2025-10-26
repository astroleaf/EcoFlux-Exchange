/**
 * App Context
 * Global application state
 */

import React, { createContext, useContext, useState, useEffect } from 'react'
import { healthApi } from '@services/api'

const AppContext = createContext(null)

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [theme, setTheme] = useState('light')
  const [notifications, setNotifications] = useState([])
  const [systemHealth, setSystemHealth] = useState('healthy')

  /**
   * Check system health
   */
  const checkHealth = async () => {
    try {
      const response = await healthApi.check()
      setSystemHealth(response.status)
    } catch (error) {
      setSystemHealth('unhealthy')
    }
  }

  /**
   * Add notification
   */
  const addNotification = (notification) => {
    const newNotification = {
      id: Date.now(),
      timestamp: new Date(),
      ...notification
    }
    
    setNotifications(prev => [newNotification, ...prev].slice(0, 50))
  }

  /**
   * Remove notification
   */
  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  /**
   * Clear all notifications
   */
  const clearNotifications = () => {
    setNotifications([])
  }

  /**
   * Toggle theme
   */
  const toggleTheme = () => {
    setTheme(prev => {
      const newTheme = prev === 'light' ? 'dark' : 'light'
      localStorage.setItem('theme_preference', newTheme)
      return newTheme
    })
  }

  /**
   * Login user
   */
  const login = (userData, token) => {
    setUser(userData)
    localStorage.setItem('auth_token', token)
    localStorage.setItem('user_data', JSON.stringify(userData))
  }

  /**
   * Logout user
   */
  const logout = () => {
    setUser(null)
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
  }

  /**
   * Load user from storage
   */
  useEffect(() => {
    const savedUser = localStorage.getItem('user_data')
    const savedTheme = localStorage.getItem('theme_preference')
    
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    
    if (savedTheme) {
      setTheme(savedTheme)
    }

    // Check system health on mount
    checkHealth()

    // Check health every 5 minutes
    const interval = setInterval(checkHealth, 5 * 60 * 1000)
    
    return () => clearInterval(interval)
  }, [])

  /**
   * Apply theme to document
   */
  useEffect(() => {
    document.documentElement.setAttribute('data-color-scheme', theme)
  }, [theme])

  const value = {
    user,
    theme,
    notifications,
    systemHealth,
    login,
    logout,
    toggleTheme,
    addNotification,
    removeNotification,
    clearNotifications,
    checkHealth
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
