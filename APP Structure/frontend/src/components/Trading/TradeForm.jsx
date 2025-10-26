/**
 * OrderForm Component
 * Form for creating buy/sell orders
 */

import React, { useState } from 'react'
import { useTransactions } from '@hooks/useTransactions'
import { useApp } from '@context/AppContext'
import { validateTradeForm } from '@utils/validators'
import { formatCurrency, formatEnergy } from '@utils/formatters'
import './OrderForm.css'

const OrderForm = ({ energyType }) => {
  const { createTransaction, loading } = useTransactions(false)
  const { addNotification } = useApp()

  const [formData, setFormData] = useState({
    order_type: 'buy',
    quantity: '',
    price: ''
  })

  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validate
    const validation = validateTradeForm({
      ...formData,
      energy_type: energyType,
      user_id: 'current-user' // Replace with actual user ID
    })

    if (!validation.isValid) {
      setErrors(validation.errors)
      return
    }

    // Create order
    const result = await createTransaction({
      energy_type: energyType,
      quantity: parseFloat(formData.quantity),
      price: parseFloat(formData.price),
      order_type: formData.order_type,
      user_id: 'current-user' // Replace with actual user ID
    })

    if (result.success) {
      addNotification({
        type: 'success',
        title: 'Order Created',
        message: `${formData.order_type.toUpperCase()} order for ${formData.quantity} kWh at ${formatCurrency(formData.price)}/kWh created successfully`
      })

      // Reset form
      setFormData({
        order_type: formData.order_type,
        quantity: '',
        price: ''
      })
    } else {
      addNotification({
        type: 'error',
        title: 'Order Failed',
        message: result.error || 'Failed to create order'
      })
    }
  }

  const totalCost = formData.quantity && formData.price
    ? (parseFloat(formData.quantity) * parseFloat(formData.price)).toFixed(2)
    : '0.00'

  return (
    <div className="order-form">
      <div className="order-form__header">
        <h3>Place Order</h3>
      </div>

      <form onSubmit={handleSubmit} className="order-form__body">
        {/* Order Type */}
        <div className="form-group">
          <label className="form-label">Order Type</label>
          <div className="order-type-selector">
            <button
              type="button"
              className={`btn ${formData.order_type === 'buy' ? 'btn--success' : 'btn--outline'}`}
              onClick={() => setFormData(prev => ({ ...prev, order_type: 'buy' }))}
            >
              Buy
            </button>
            <button
              type="button"
              className={`btn ${formData.order_type === 'sell' ? 'btn--error' : 'btn--outline'}`}
              onClick={() => setFormData(prev => ({ ...prev, order_type: 'sell' }))}
            >
              Sell
            </button>
          </div>
        </div>

        {/* Quantity */}
        <div className="form-group">
          <label htmlFor="quantity" className="form-label">
            Quantity (kWh)
          </label>
          <input
            type="number"
            id="quantity"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
            className={`form-control ${errors.quantity ? 'error' : ''}`}
            placeholder="Enter quantity"
            step="0.01"
            min="0"
          />
          {errors.quantity && (
            <span className="form-error">{errors.quantity}</span>
          )}
        </div>

        {/* Price */}
        <div className="form-group">
          <label htmlFor="price" className="form-label">
            Price ($/kWh)
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            className={`form-control ${errors.price ? 'error' : ''}`}
            placeholder="Enter price"
            step="0.001"
            min="0"
          />
          {errors.price && (
            <span className="form-error">{errors.price}</span>
          )}
        </div>

        {/* Total Cost */}
        <div className="order-summary">
          <div className="summary-row">
            <span>Total Cost:</span>
            <strong>{formatCurrency(totalCost)}</strong>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className={`btn btn--primary btn--full-width ${formData.order_type === 'buy' ? 'btn--success' : 'btn--error'}`}
          disabled={loading}
        >
          {loading ? 'Processing...' : `Place ${formData.order_type.toUpperCase()} Order`}
        </button>
      </form>
    </div>
  )
}

export default OrderForm
