/**
 * useWebSocket Hook
 * Manages WebSocket connection and events
 */

import { useEffect, useState, useCallback } from 'react'
import wsService from '@services/websocket'

export const useWebSocket = (autoConnect = true) => {
  const [isConnected, setIsConnected] = useState(false)
  const [reconnectAttempts, setReconnectAttempts] = useState(0)

  /**
   * Connect to WebSocket
   */
  const connect = useCallback(() => {
    wsService.connect()
  }, [])

  /**
   * Disconnect from WebSocket
   */
  const disconnect = useCallback(() => {
    wsService.disconnect()
  }, [])

  /**
   * Subscribe to event
   */
  const subscribe = useCallback((event, handler) => {
    wsService.on(event, handler)
  }, [])

  /**
   * Unsubscribe from event
   */
  const unsubscribe = useCallback((event, handler) => {
    wsService.off(event, handler)
  }, [])

  /**
   * Send message
   */
  const send = useCallback((event, data) => {
    wsService.send(event, data)
  }, [])

  /**
   * Setup connection status listener
   */
  useEffect(() => {
    const handleConnectionStatus = (status) => {
      setIsConnected(status.connected)
    }

    const handleConnectionError = () => {
      const status = wsService.getStatus()
      setReconnectAttempts(status.reconnectAttempts)
    }

    wsService.on('connection_status', handleConnectionStatus)
    wsService.on('connection_error', handleConnectionError)

    if (autoConnect) {
      connect()
    }

    return () => {
      wsService.off('connection_status', handleConnectionStatus)
      wsService.off('connection_error', handleConnectionError)
      
      if (autoConnect) {
        disconnect()
      }
    }
  }, [autoConnect, connect, disconnect])

  return {
    isConnected,
    reconnectAttempts,
    connect,
    disconnect,
    subscribe,
    unsubscribe,
    send
  }
}
