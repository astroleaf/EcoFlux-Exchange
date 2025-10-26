/**
 * OrderBook Component
 * Displays buy and sell orders
 */

import React, { useState, useEffect } from 'react'
import { tradeApi } from '@services/api'
import { formatCurrency, formatEnergy } from '@utils/formatters'
import './OrderBook.css'

const OrderBook = ({ energyType }) => {
  const [orderBook, setOrderBook] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchOrderBook()
    const interval = setInterval(fetchOrderBook, 5000) // Refresh every 5s
    return () => clearInterval(interval)
  }, [energyType])

  const fetchOrderBook = async () => {
    setLoading(true)
    try {
      const response = await tradeApi.getOrderBook(energyType)
      setOrderBook(response.order_book)
    } catch (error) {
      console.error('Failed to fetch order book:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading && !orderBook) {
    return <div className="order-book__loading">Loading order book...</div>
  }

  return (
    <div className="order-book">
      <div className="order-book__header">
        <h3>Order Book</h3>
        {orderBook?.spread && (
          <div className="spread-info">
            <span className="spread-label">Spread:</span>
            <span className="spread-value">{formatCurrency(orderBook.spread.spread)}</span>
            <span className="spread-percentage">({orderBook.spread.spread_percentage}%)</span>
          </div>
        )}
      </div>

      <div className="order-book__body">
        {/* Sell Orders */}
        <div className="order-book__section">
          <div className="section-header section-header--sell">
            <span>Sell Orders ({orderBook?.total_sell_orders || 0})</span>
          </div>
          <div className="orders-list">
            <div className="orders-header">
              <span>Price</span>
              <span>Quantity</span>
              <span>Total</span>
            </div>
            {orderBook?.sell_orders.slice(0, 10).map((order, index) => (
              <div key={index} className="order-row order-row--sell">
                <span className="order-price">{formatCurrency(order.price)}</span>
                <span className="order-quantity">{formatEnergy(order.quantity)}</span>
                <span className="order-total">
                  {formatCurrency(order.price * order.quantity)}
                </span>
              </div>
            )) || <div className="no-orders">No sell orders</div>}
          </div>
        </div>

        {/* Market Price */}
        {orderBook?.spread && (
          <div className="market-price">
            <div className="market-price__label">Market Price</div>
            <div className="market-price__value">
              {formatCurrency((orderBook.spread.best_bid + orderBook.spread.best_ask) / 2)}
            </div>
          </div>
        )}

        {/* Buy Orders */}
        <div className="order-book__section">
          <div className="section-header section-header--buy">
            <span>Buy Orders ({orderBook?.total_buy_orders || 0})</span>
          </div>
          <div className="orders-list">
            <div className="orders-header">
              <span>Price</span>
              <span>Quantity</span>
              <span>Total</span>
            </div>
            {orderBook?.buy_orders.slice(0, 10).map((order, index) => (
              <div key={index} className="order-row order-row--buy">
                <span className="order-price">{formatCurrency(order.price)}</span>
                <span className="order-quantity">{formatEnergy(order.quantity)}</span>
                <span className="order-total">
                  {formatCurrency(order.price * order.quantity)}
                </span>
              </div>
            )) || <div className="no-orders">No buy orders</div>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default OrderBook
