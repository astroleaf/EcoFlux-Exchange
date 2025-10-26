/**
 * useTransactions Hook
 * Manages transaction state and operations
 */

import { useState, useEffect, useCallback } from 'react'
import { tradeApi } from '@services/api'
import wsService from '@services/websocket'

export const useTransactions = (autoRefresh = true) => {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetch transactions
   */
  const fetchTransactions = useCallback(async (params = {}) => {
    setLoading(true)
    setError(null)

    try {
      const response = await tradeApi.listTrades(params)
      setTransactions(response.trades)
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch transactions:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Create new transaction
   */
  const createTransaction = useCallback(async (tradeData) => {
    setLoading(true)
    setError(null)

    try {
      const response = await tradeApi.createTrade(tradeData)
      
      // Add new transaction to list
      setTransactions(prev => [response.transaction, ...prev])
      
      return { success: true, transaction: response.transaction }
    } catch (err) {
      setError(err.message)
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Cancel transaction
   */
  const cancelTransaction = useCallback(async (transactionId) => {
    setLoading(true)
    setError(null)

    try {
      await tradeApi.cancelTrade(transactionId)
      
      // Update transaction status
      setTransactions(prev =>
        prev.map(tx =>
          tx.id === transactionId
            ? { ...tx, status: 'cancelled' }
            : tx
        )
      )
      
      return { success: true }
    } catch (err) {
      setError(err.message)
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Get transaction by ID
   */
  const getTransaction = useCallback(async (transactionId) => {
    try {
      const response = await tradeApi.getTrade(transactionId)
      return response.trade
    } catch (err) {
      console.error('Failed to get transaction:', err)
      return null
    }
  }, [])

  /**
   * Handle real-time transaction updates
   */
  useEffect(() => {
    if (!autoRefresh) return

    const handleTradeMatched = (data) => {
      setTransactions(prev =>
        prev.map(tx =>
          tx.id === data.transaction_id
            ? { ...tx, status: 'matched', matched_with: data.matched_with }
            : tx
        )
      )
    }

    wsService.on('trade_matched', handleTradeMatched)

    return () => {
      wsService.off('trade_matched', handleTradeMatched)
    }
  }, [autoRefresh])

  /**
   * Initial fetch
   */
  useEffect(() => {
    if (autoRefresh) {
      fetchTransactions()
    }
  }, [autoRefresh, fetchTransactions])

  return {
    transactions,
    loading,
    error,
    fetchTransactions,
    createTransaction,
    cancelTransaction,
    getTransaction
  }
}
