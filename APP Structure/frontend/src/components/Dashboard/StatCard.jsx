/**
 * PriceChart Component
 * Displays energy price trends
 */

import React, { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { analyticsApi } from '@services/api'
import { ENERGY_TYPES, CHART_COLORS } from '@utils/constants'
import './PriceChart.css'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const PriceChart = () => {
  const [chartData, setChartData] = useState(null)
  const [period, setPeriod] = useState('7d')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchPriceTrends()
  }, [period])

  const fetchPriceTrends = async () => {
    setLoading(true)
    try {
      const response = await analyticsApi.getPriceTrends(period)
      
      const datasets = ENERGY_TYPES.map((type, index) => ({
        label: type.label,
        data: response.trends[type.value] || [],
        borderColor: type.color,
        backgroundColor: `${type.color}33`,
        tension: 0.4,
        fill: false
      }))

      setChartData({
        labels: response.labels,
        datasets
      })
    } catch (error) {
      console.error('Failed to fetch price trends:', error)
    } finally {
      setLoading(false)
    }
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Energy Price Trends',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: 'Price ($/kWh)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Time'
        }
      }
    }
  }

  return (
    <div className="price-chart">
      <div className="price-chart__header">
        <h3>Price Trends</h3>
        <div className="price-chart__controls">
          <select 
            value={period} 
            onChange={(e) => setPeriod(e.target.value)}
            className="form-control"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
        </div>
      </div>
      <div className="price-chart__body">
        {loading ? (
          <div className="chart-loading">Loading chart...</div>
        ) : chartData ? (
          <Line data={chartData} options={options} />
        ) : (
          <div className="chart-empty">No data available</div>
        )}
      </div>
    </div>
  )
}

export default PriceChart
