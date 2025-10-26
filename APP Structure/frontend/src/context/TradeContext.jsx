/**
 * Trade Context
 * Trading-specific state management
 */

import React, { createContext, useContext, useState } from 'react'

const TradeContext = createContext(null)

export const TradeProvider = ({ children }) => {
  const [selectedEnergyType, setSelectedEnergyType] = useState('solar')
  const [orderBook, setOrderBook] = useState(null)
  const [activeFilters, setActiveFilters] = useState({
    status: null,
    energyType: null,
    orderType: null
  })

  /**
   * Update order book
   */
  const updateOrderBook = (data) => {
    setOrderBook(data)
  }

  /**
   * Set filter
   */
  const setFilter = (key, value) => {
    setActiveFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  /**
   * Clear filters
   */
  const clearFilters = () => {
    setActiveFilters({
      status: null,
      energyType: null,
      orderType: null
    })
  }

  /**
   * Get active filters count
   */
  const getActiveFiltersCount = () => {
    return Object.values(activeFilters).filter(v => v !== null).length
  }

  const value = {
    selectedEnergyType,
    setSelectedEnergyType,
    orderBook,
    updateOrderBook,
    activeFilters,
    setFilter,
    clearFilters,
    getActiveFiltersCount
  }

  return <TradeContext.Provider value={value}>{children}</TradeContext.Provider>
}

export const useTrade = () => {
  const context = useContext(TradeContext)
  if (!context) {
    throw new Error('useTrade must be used within TradeProvider')
  }
  return context
}
