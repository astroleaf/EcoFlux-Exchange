/**
 * WebSocket Service
 * Handles real-time communication with backend
 */

import { io } from 'socket.io-client'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:5000'
const RECONNECT_ATTEMPTS = parseInt(import.meta.env.VITE_WS_RECONNECT_ATTEMPTS) || 5
const RECONNECT_DELAY = parseInt(import.meta.env.VITE_WS_RECONNECT_DELAY) || 3000

class WebSocketService {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.eventHandlers = new Map()
  }

  /**
   * Connect to WebSocket server
   */
  connect() {
    if (this.socket && this.isConnected) {
      console.log('WebSocket already connected')
      return
    }

    this.socket = io(WS_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: RECONNECT_ATTEMPTS,
      reconnectionDelay: RECONNECT_DELAY
    })

    this.setupEventListeners()
  }

  /**
   * Setup socket event listeners
   */
  setupEventListeners() {
    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.isConnected = true
      this.reconnectAttempts = 0
      this.emit('connection_status', { connected: true })
    })

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason)
      this.isConnected = false
      this.emit('connection_status', { connected: false, reason })
    })

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error)
      this.reconnectAttempts++
      
      if (this.reconnectAttempts >= RECONNECT_ATTEMPTS) {
        console.error('Max reconnection attempts reached')
        this.emit('connection_error', { 
          error: 'Failed to connect after multiple attempts' 
        })
      }
    })

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error)
      this.emit('error', { error })
    })

    // Real-time event listeners
    this.socket.on('trade_matched', (data) => {
      this.emit('trade_matched', data)
    })

    this.socket.on('contract_executed', (data) => {
      this.emit('contract_executed', data)
    })

    this.socket.on('price_update', (data) => {
      this.emit('price_update', data)
    })

    this.socket.on('market_update', (data) => {
      this.emit('market_update', data)
    })

    this.socket.on('notification', (data) => {
      this.emit('notification', data)
    })
  }

  /**
   * Subscribe to events
   */
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, [])
    }
    this.eventHandlers.get(event).push(handler)
  }

  /**
   * Unsubscribe from events
   */
  off(event, handler) {
    if (!this.eventHandlers.has(event)) return

    const handlers = this.eventHandlers.get(event)
    const index = handlers.indexOf(handler)
    
    if (index > -1) {
      handlers.splice(index, 1)
    }
  }

  /**
   * Emit event to handlers
   */
  emit(event, data) {
    if (!this.eventHandlers.has(event)) return

    const handlers = this.eventHandlers.get(event)
    handlers.forEach(handler => {
      try {
        handler(data)
      } catch (error) {
        console.error(`Error in event handler for ${event}:`, error)
      }
    })
  }

  /**
   * Send message to server
   */
  send(event, data) {
    if (!this.isConnected) {
      console.warn('WebSocket not connected. Message not sent:', event)
      return
    }

    this.socket.emit(event, data)
  }

  /**
   * Disconnect from server
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.isConnected = false
    }
  }

  /**
   * Get connection status
   */
  getStatus() {
    return {
      connected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts
    }
  }
}

// Create singleton instance
const wsService = new WebSocketService()

export default wsService
