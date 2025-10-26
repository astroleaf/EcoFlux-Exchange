/**
 * VolumeChart Component
 * Displays trading volume by energy type
 */

import React, { useState, useEffect } from 'react'
import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { analyticsApi } from '@services/api'
import { ENERGY_TYPES } from '@utils/constants'
import './VolumeChart.css'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const VolumeChart = () => {
  const [chartData, setChartData] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchVolumeData()
  }, [])

  const fetchVolumeData = async () => {
    setLoading(true)
    try {
      const response = await analyticsApi.getVolumeByType('30d')
      
      const data = {
        labels: ENERGY_TYPES.map(t => t.label),
        datasets: [{
          label: 'Trading Volume (kWh)',
          data: ENERGY_TYPES.map(t => response.volumes[t.value] || 0),
          backgroundColor: ENERGY_TYPES.map(t => `${t.color}99`),
          borderColor: ENERGY_TYPES.map(t => t.color),
          borderWidth: 2
        }]
      }

      setChartData(data)
    } catch (error) {
      console.error('Failed to fetch volume data:', error)
    } finally {
      setLoading(false)
    }
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: 'Trading Volume by Energy Type (Last 30 Days)',
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Volume (kWh)'
        }
      }
    }
  }

  return (
    <div className="volume-chart">
      <div className="volume-chart__body">
        {loading ? (
          <div className="chart-loading">Loading chart...</div>
        ) : chartData ? (
          <Bar data={chartData} options={options} />
        ) : (
          <div className="chart-empty">No data available</div>
        )}
      </div>
    </div>
  )
}

export default VolumeChart
