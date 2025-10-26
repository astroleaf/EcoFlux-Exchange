"""
Price Predictor
AI-powered energy price prediction using machine learning
"""

import numpy as np
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)


class PricePredictor:
    """
    Predicts future energy prices using AI/ML models
    """
    
    def __init__(self):
        """
        Initialize price predictor
        In production, this would load trained ML models
        """
        self.models = {}
        self.base_prices = {
            'solar': 0.12,
            'wind': 0.10,
            'hydro': 0.08,
            'biomass': 0.15
        }
        self.historical_data = self._initialize_historical_data()
        
    def _initialize_historical_data(self):
        """
        Initialize historical price data
        """
        data = {}
        for energy_type in self.base_prices.keys():
            prices = []
            base = self.base_prices[energy_type]
            
            # Generate 30 days of historical data
            for i in range(30):
                date = datetime.utcnow() - timedelta(days=30-i)
                # Simulate price with trend and volatility
                trend = 0.001 * i  # Slight upward trend
                noise = random.uniform(-0.02, 0.02)
                price = base + trend + noise
                prices.append({
                    'date': date,
                    'price': round(price, 3)
                })
            
            data[energy_type] = prices
        
        return data
    
    def predict(self, energy_type: str, horizon: int = 24):
        """
        Predict future prices
        
        Args:
            energy_type: Type of energy to predict
            horizon: Hours ahead to predict
            
        Returns:
            Dict with predictions
        """
        if energy_type not in self.base_prices:
            raise ValueError(f"Unknown energy type: {energy_type}")
        
        # Get recent prices
        recent_prices = [p['price'] for p in self.historical_data[energy_type][-7:]]
        current_price = recent_prices[-1]
        
        # Calculate trend
        trend = (recent_prices[-1] - recent_prices) / len(recent_prices)
        
        # Generate predictions
        predictions = []
        for i in range(horizon):
            time_ahead = datetime.utcnow() + timedelta(hours=i+1)
            
            # Simple linear prediction with noise
            predicted_price = current_price + (trend * i) + random.uniform(-0.005, 0.005)
            predicted_price = max(0.05, predicted_price)  # Floor price
            
            predictions.append({
                'timestamp': time_ahead.isoformat(),
                'price': round(predicted_price, 3),
                'confidence': round(random.uniform(0.85, 0.95), 2)
            })
        
        logger.info(f"Generated {horizon}h price prediction for {energy_type}")
        
        return {
            'energy_type': energy_type,
            'current_price': current_price,
            'predictions': predictions,
            'trend': 'upward' if trend > 0 else 'downward',
            'volatility': self.calculate_volatility(energy_type)
        }
    
    def calculate_volatility(self, energy_type: str):
        """
        Calculate price volatility
        
        Args:
            energy_type: Type of energy
            
        Returns:
            Volatility metrics
        """
        prices = [p['price'] for p in self.historical_data[energy_type][-7:]]
        
        # Calculate standard deviation
        mean_price = np.mean(prices)
        std_dev = np.std(prices)
        
        # Coefficient of variation
        cv = (std_dev / mean_price) * 100
        
        # Classify volatility
        if cv < 5:
            level = 'low'
        elif cv < 10:
            level = 'medium'
        else:
            level = 'high'
        
        return {
            'level': level,
            'coefficient_of_variation': round(cv, 2),
            'std_deviation': round(std_dev, 4),
            'mean_price': round(mean_price, 3)
        }
    
    def get_all_predictions(self):
        """
        Get predictions for all energy types
        """
        predictions = {}
        
        for energy_type in self.base_prices.keys():
            predictions[energy_type] = self.predict(energy_type, horizon=24)
        
        return predictions
    
    def update_historical_data(self, energy_type: str, price: float):
        """
        Update historical data with new price
        """
        self.historical_data[energy_type].append({
            'date': datetime.utcnow(),
            'price': price
        })
        
        # Keep only last 30 days
        self.historical_data[energy_type] = self.historical_data[energy_type][-30:]
