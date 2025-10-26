/**
 * useSmartContracts Hook
 * Manages smart contract operations
 */

import { useState, useEffect, useCallback } from 'react'
import contractService from '@services/contractService'
import wsService from '@services/websocket'

export const useSmartContracts = (autoFetch = true) => {
  const [contracts, setContracts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [web3Available, setWeb3Available] = useState(false)
  const [account, setAccount] = useState(null)

  /**
   * Initialize Web3
   */
  const initializeWeb3 = useCallback(async () => {
    const available = contractService.isWeb3Available()
    setWeb3Available(available)

    if (available) {
      const success = await contractService.initWeb3()
      if (success) {
        setAccount(contractService.getAccount())
      }
      return success
    }

    return false
  }, [])

  /**
   * Fetch contracts
   */
  const fetchContracts = useCallback(async (status = null) => {
    setLoading(true)
    setError(null)

    try {
      const data = await contractService.listContracts(status)
      setContracts(data)
    } catch (err) {
      setError(err.message)
      console.error('Failed to fetch contracts:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Deploy contract
   */
  const deployContract = useCallback(async (buyerId, sellerId, energyType, quantity, price) => {
    setLoading(true)
    setError(null)

    try {
      const result = await contractService.deployContract(
        buyerId,
        sellerId,
        energyType,
        quantity,
        price
      )

      if (result.success) {
        // Add new contract to list
        setContracts(prev => [result.contract, ...prev])
      }

      return result
    } catch (err) {
      setError(err.message)
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Execute contract
   */
  const executeContract = useCallback(async (contractId) => {
    setLoading(true)
    setError(null)

    try {
      const result = await contractService.executeContract(contractId)

      if (result.success) {
        // Update contract status
        setContracts(prev =>
          prev.map(c =>
            c.id === contractId
              ? { ...c, status: 'completed', executed_at: new Date().toISOString() }
              : c
          )
        )
      }

      return result
    } catch (err) {
      setError(err.message)
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [])

  /**
   * Get contract details
   */
  const getContract = useCallback(async (contractId) => {
    try {
      const contract = await contractService.getContract(contractId)
      return contract
    } catch (err) {
      console.error('Failed to get contract:', err)
      return null
    }
  }, [])

  /**
   * Handle real-time contract updates
   */
  useEffect(() => {
    const handleContractExecuted = (data) => {
      setContracts(prev =>
        prev.map(c =>
          c.id === data.contract_id
            ? { ...c, status: 'completed', executed_at: data.executed_at }
            : c
        )
      )
    }

    wsService.on('contract_executed', handleContractExecuted)

    return () => {
      wsService.off('contract_executed', handleContractExecuted)
    }
  }, [])

  /**
   * Initial setup
   */
  useEffect(() => {
    initializeWeb3()
    
    if (autoFetch) {
      fetchContracts()
    }
  }, [autoFetch, fetchContracts, initializeWeb3])

  return {
    contracts,
    loading,
    error,
    web3Available,
    account,
    initializeWeb3,
    fetchContracts,
    deployContract,
    executeContract,
    getContract
  }
}
