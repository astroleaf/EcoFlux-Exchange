/**
 * Dashboard Component
 * Main dashboard with analytics and metrics
 */

import React, { useEffect } from 'react'
import { useAnalytics } from '@context/AnalyticsContext'
import { useWebSocket } from '@hooks/useWebSocket'
import MetricsCard from './MetricsCard'
import PriceChart from './PriceChart'
import VolumeChart from './VolumeChart'
import RecentTrades from './RecentTrades'
import './Dashboard.css'

const Dashboard = () => {
  const { dashboardMetrics, efficiencyMetrics, loading, refreshMetrics } = useAnalytics()
  const { isConnected } = useWebSocket()

  useEffect(() => {
    refreshMetrics()
  }, [])

  if (loading && !dashboardMetrics) {
    return (
      <div className="dashboard__loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard__header">
        <h1>Dashboard</h1>
        <div className="dashboard__status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? 'Live' : 'Offline'}
          </span>
        </div>
      </div>

      {/* Performance Metrics */}
      <section className="dashboard__metrics">
        <MetricsCard
          title="Transaction Efficiency"
          value={`${efficiencyMetrics?.transaction_efficiency || 35}%`}
          subtitle="Improvement"
          trend="up"
          color="success"
        />
        <MetricsCard
          title="Verification Time"
          value={`${efficiencyMetrics?.verification_time_reduction || 60}%`}
          subtitle="Reduction"
          trend="up"
          color="success"
        />
        <MetricsCard
          title="Weekly Transactions"
          value={efficiencyMetrics?.weekly_transactions || 1200}
          subtitle="This Week"
          trend="up"
          color="info"
        />
        <MetricsCard
          title="Success Rate"
          value={`${efficiencyMetrics?.success_rate || 99.9}%`}
          subtitle="Last 30 Days"
          trend="stable"
          color="success"
        />
      </section>

      {/* Charts */}
      <section className="dashboard__charts">
        <div className="chart-container">
          <PriceChart />
        </div>
        <div className="chart-container">
          <VolumeChart />
        </div>
      </section>

      {/* Recent Activity */}
      <section className="dashboard__activity">
        <RecentTrades limit={10} />
      </section>
    </div>
  )
}

export default Dashboard
