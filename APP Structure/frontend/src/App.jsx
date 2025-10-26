/**
 * Main App Component
 */

import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AppProvider } from '@context/AppContext'
import { TradeProvider } from '@context/TradeContext'
import { AnalyticsProvider } from '@context/AnalyticsContext'
import { useWebSocket } from '@hooks/useWebSocket'
import { useApp } from '@context/AppContext'

// Placeholder components - will be created in next batch
const Dashboard = () => <div>Dashboard</div>
const Trading = () => <div>Trading</div>
const Analytics = () => <div>Analytics</div>
const SmartContracts = () => <div>Smart Contracts</div>

function AppContent() {
  const { addNotification } = useApp()
  const { subscribe } = useWebSocket(true)

  useEffect(() => {
    // Subscribe to WebSocket notifications
    const handleNotification = (data) => {
      addNotification({
        type: data.type,
        title: data.title,
        message: data.message
      })
    }

    subscribe('notification', handleNotification)
  }, [subscribe, addNotification])

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/trading" element={<Trading />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/contracts" element={<SmartContracts />} />
      </Routes>
    </Router>
  )
}

function App() {
  return (
    <AppProvider>
      <TradeProvider>
        <AnalyticsProvider>
          <AppContent />
        </AnalyticsProvider>
      </TradeProvider>
    </AppProvider>
  )
}

export default App
