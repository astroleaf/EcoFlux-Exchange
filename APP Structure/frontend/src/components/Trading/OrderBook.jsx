/**
 * Trading Component
 * Main trading interface with order book and forms
 */

import React, { useState } from 'react'
import { useTrade } from '@context/TradeContext'
import OrderForm from './OrderForm'
import OrderBook from './OrderBook'
import MyOrders from './MyOrders'
import { ENERGY_TYPES } from '@utils/constants'
import './Trading.css'

const Trading = () => {
  const { selectedEnergyType, setSelectedEnergyType } = useTrade()

  return (
    <div className="trading">
      <div className="trading__header">
        <h1>Energy Trading</h1>
        <div className="trading__energy-selector">
          {ENERGY_TYPES.map((type) => (
            <button
              key={type.value}
              className={`energy-tab ${selectedEnergyType === type.value ? 'active' : ''}`}
              onClick={() => setSelectedEnergyType(type.value)}
              style={{
                borderBottom: selectedEnergyType === type.value ? `3px solid ${type.color}` : 'none'
              }}
            >
              {type.label}
            </button>
          ))}
        </div>
      </div>

      <div className="trading__container">
        {/* Order Form */}
        <div className="trading__form">
          <OrderForm energyType={selectedEnergyType} />
        </div>

        {/* Order Book */}
        <div className="trading__orderbook">
          <OrderBook energyType={selectedEnergyType} />
        </div>
      </div>

      {/* User's Orders */}
      <div className="trading__my-orders">
        <MyOrders />
      </div>
    </div>
  )
}

export default Trading
