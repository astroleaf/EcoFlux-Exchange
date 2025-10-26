/**
 * MyOrders Component
 * Displays user's trading orders
 */

import React, { useState, useEffect } from 'react'
import { useTransactions } from '@hooks/useTransactions'
import { formatCurrency, formatEnergy, formatDate, formatEnergyType } from '@utils/formatters'
import { TRANSACTION_STATUSES } from '@utils/constants'
import './MyOrders.css'

const MyOrders = () => {
  const { transactions, loading, cancelTransaction } = useTransactions()
  const [filter, setFilter] = useState('all')

  const filteredTransactions = transactions.filter(tx => {
    if (filter === 'all') return true
    return tx.status === filter
  })

  const handleCancel = async (orderId) => {
    if (window.confirm('Are you sure you want to cancel this order?')) {
      const result = await cancelTransaction(orderId)
      if (result.success) {
        // Success notification handled by hook
      }
    }
  }

  return (
    <div className="my-orders">
      <div className="my-orders__header">
        <h3>My Orders</h3>
        <div className="my-orders__filters">
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
            onClick={() => setFilter('pending')}
          >
            Pending
          </button>
          <button
            className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
            onClick={() => setFilter('completed')}
          >
            Completed
          </button>
        </div>
      </div>

      <div className="my-orders__body">
        {loading ? (
          <div className="my-orders__loading">Loading orders...</div>
        ) : filteredTransactions.length > 0 ? (
          <div className="orders-table">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Type</th>
                  <th>Energy</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredTransactions.map((order) => (
                  <tr key={order.id}>
                    <td>{formatDate(order.created_at, 'datetime')}</td>
                    <td>
                      <span className={`order-type order-type--${order.order_type}`}>
                        {order.order_type.toUpperCase()}
                      </span>
                    </td>
                    <td>{formatEnergyType(order.energy_type)}</td>
                    <td>{formatEnergy(order.quantity)}</td>
                    <td>{formatCurrency(order.price)}/kWh</td>
                    <td>{formatCurrency(order.quantity * order.price)}</td>
                    <td>
                      <span className={`status status--${order.status}`}>
                        {TRANSACTION_STATUSES[order.status]?.label || order.status}
                      </span>
                    </td>
                    <td>
                      {order.status === 'pending' && (
                        <button
                          className="btn btn--sm btn--outline"
                          onClick={() => handleCancel(order.id)}
                        >
                          Cancel
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="my-orders__empty">
            No {filter !== 'all' ? filter : ''} orders found
          </div>
        )}
      </div>
    </div>
  )
}

export default MyOrders
