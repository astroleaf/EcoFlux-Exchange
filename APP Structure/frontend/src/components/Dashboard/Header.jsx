/**
 * MetricsCard Component
 * Displays a single metric with trend indicator
 */

import React from 'react'
import { formatNumber } from '@utils/formatters'
import './MetricsCard.css'

const MetricsCard = ({ title, value, subtitle, trend, color = 'primary' }) => {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return '↑'
      case 'down':
        return '↓'
      default:
        return '→'
    }
  }

  const getTrendClass = () => {
    switch (trend) {
      case 'up':
        return 'trend-up'
      case 'down':
        return 'trend-down'
      default:
        return 'trend-stable'
    }
  }

  return (
    <div className={`metrics-card metrics-card--${color}`}>
      <div className="metrics-card__header">
        <h3 className="metrics-card__title">{title}</h3>
        <span className={`metrics-card__trend ${getTrendClass()}`}>
          {getTrendIcon()}
        </span>
      </div>
      <div className="metrics-card__value">
        {typeof value === 'number' ? formatNumber(value) : value}
      </div>
      {subtitle && (
        <div className="metrics-card__subtitle">{subtitle}</div>
      )}
    </div>
  )
}

export default MetricsCard
