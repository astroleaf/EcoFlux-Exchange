/**
 * Contract Service
 * Handles smart contract operations
 */

import { contractApi } from './api'
import Web3 from 'web3'

class ContractService {
  constructor() {
    this.web3 = null
    this.account = null
    this.chainId = null
  }

  /**
   * Initialize Web3
   */
  async initWeb3() {
    if (typeof window.ethereum !== 'undefined') {
      try {
        this.web3 = new Web3(window.ethereum)
        await window.ethereum.request({ method: 'eth_requestAccounts' })
        
        const accounts = await this.web3.eth.getAccounts()
        this.account = accounts
        
        this.chainId = await this.web3.eth.getChainId()
        
        console.log('Web3 initialized:', {
          account: this.account,
          chainId: this.chainId
        })
        
        return true
      } catch (error) {
        console.error('Web3 initialization failed:', error)
        return false
      }
    } else {
      console.warn('MetaMask not detected')
      return false
    }
  }

  /**
   * Deploy smart contract
   */
  async deployContract(buyerId, sellerId, energyType, quantity, price) {
    try {
      const response = await contractApi.deploy({
        buyer_id: buyerId,
        seller_id: sellerId,
        energy_type: energyType,
        quantity,
        price
      })

      return {
        success: true,
        contract: response.contract
      }
    } catch (error) {
      console.error('Contract deployment failed:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  /**
   * Execute smart contract
   */
  async executeContract(contractId) {
    try {
      const response = await contractApi.execute(contractId)

      return {
        success: true,
        result: response.result
      }
    } catch (error) {
      console.error('Contract execution failed:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  /**
   * Verify contract
   */
  async verifyContract(contractId, transactionHash) {
    try {
      const response = await contractApi.verify(contractId, transactionHash)

      return {
        success: true,
        verified: response.verified
      }
    } catch (error) {
      console.error('Contract verification failed:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }

  /**
   * List contracts
   */
  async listContracts(status = null) {
    try {
      const response = await contractApi.list(status)
      return response.contracts
    } catch (error) {
      console.error('Failed to list contracts:', error)
      return []
    }
  }

  /**
   * Get contract details
   */
  async getContract(contractId) {
    try {
      const response = await contractApi.getContract(contractId)
      return response.contract
    } catch (error) {
      console.error('Failed to get contract:', error)
      return null
    }
  }

  /**
   * Get contract statistics
   */
  async getStatistics() {
    try {
      const response = await contractApi.getStats()
      return response.stats
    } catch (error) {
      console.error('Failed to get contract statistics:', error)
      return null
    }
  }

  /**
   * Format contract data for display
   */
  formatContract(contract) {
    return {
      id: contract.id,
      buyer: contract.buyer_id,
      seller: contract.seller_id,
      energyType: contract.energy_type,
      quantity: `${contract.quantity} kWh`,
      price: `$${contract.price}/kWh`,
      totalValue: `$${contract.total_value}`,
      status: contract.status,
      hash: contract.transaction_hash,
      gasUsed: contract.gas_used ? `${contract.gas_used} ETH` : 'N/A',
      executionTime: contract.execution_time ? `${contract.execution_time}s` : 'N/A',
      createdAt: new Date(contract.created_at),
      deployedAt: contract.deployed_at ? new Date(contract.deployed_at) : null,
      executedAt: contract.executed_at ? new Date(contract.executed_at) : null
    }
  }

  /**
   * Get current account
   */
  getAccount() {
    return this.account
  }

  /**
   * Get chain ID
   */
  getChainId() {
    return this.chainId
  }

  /**
   * Check if Web3 is available
   */
  isWeb3Available() {
    return typeof window.ethereum !== 'undefined'
  }
}

// Create singleton instance
const contractService = new ContractService()

export default contractService
