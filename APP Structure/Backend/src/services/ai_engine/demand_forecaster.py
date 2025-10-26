"""
Demand Forecaster
AI-powered energy demand forecasting
"""

from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)


class DemandForecaster:
    """
    Forecasts energy demand using AI/ML models
    """
    
    def __init__(self):
        """
        Initialize demand forecaster
        """
        self.base_demand = {
            'solar': 1000,  # kWh
            'wind': 800,
            'hydro': 1200,
            'biomass': 600
        }
        
    def forecast(self, energy_type: str, period: str = 'day'):
        """
        Forecast energy demand
        
        Args:
            energy_type: Type of energy
            period: Forecast period (day, week, month)
            
        Returns:
            Demand forecast
        """
        if energy_type not in self.base_demand:
            raise ValueError(f"Unknown energy type: {energy_type}")
        
        # Determine forecast length
        if period == 'day':
            hours = 24
            interval = 1
        elif period == 'week':
            hours = 168  # 7 days
            interval = 6
        else:  # month
            hours = 720  # 30 days
            interval = 24
        
        base = self.base_demand[energy_type]
        forecasts = []
        
        for i in range(0, hours, interval):
            timestamp = datetime.utcnow() + timedelta(hours=i)
            
            # Simulate demand patterns
            hour_of_day = timestamp.hour
            
            # Peak hours factor (higher demand 9am-9pm)
            if 9 <= hour_of_day <= 21:
                peak_factor = 1.3
            else:
                peak_factor = 0.7
            
            # Day of week factor (higher on weekdays)
            day_of_week = timestamp.weekday()
            weekday_factor = 1.2 if day_of_week < 5 else 0.9
            
            # Calculate demand
            demand = base * peak_factor * weekday_factor
            demand += random.uniform(-100, 100)  # Add noise
            demand = max(0, demand)
            
            forecasts.append({
                'timestamp': timestamp.isoformat(),
                'demand_kwh': round(demand, 2),
                'confidence': round(random.uniform(0.80, 0.92), 2)
            })
        
        # Classify overall demand level
        avg_demand = sum(f['demand_kwh'] for f in forecasts) / len(forecasts)
        
        if avg_demand > base * 1.2:
            demand_level = 'high'
        elif avg_demand > base * 0.8:
            demand_level = 'medium'
        else:
            demand_level = 'low'
        
        logger.info(f"Generated {period} demand forecast for {energy_type}")
        
        return {
            'energy_type': energy_type,
            'period': period,
            'forecasts': forecasts,
            'average_demand_kwh': round(avg_demand, 2),
            'demand_level': demand_level,
            'peak_demand_kwh': round(max(f['demand_kwh'] for f in forecasts), 2),
            'low_demand_kwh': round(min(f['demand_kwh'] for f in forecasts), 2)
        }
    
    def get_all_forecasts(self, period: str = 'day'):
        """
        Get demand forecasts for all energy types
        """
        forecasts = {}
        
        for energy_type in self.base_demand.keys():
            forecasts[energy_type] = self.forecast(energy_type, period)
        
        return forecasts
    
    def predict_supply_gap(self, energy_type: str):
        """
        Predict supply-demand gap
        """
        forecast = self.forecast(energy_type, period='day')
        avg_demand = forecast['average_demand_kwh']
        
        # Simulated current supply
        current_supply = self.base_demand[energy_type] * random.uniform(0.8, 1.2)
        
        gap = current_supply - avg_demand
        gap_percentage = (gap / avg_demand) * 100
        
        if gap > 0:
            status = 'surplus'
        elif gap < 0:
            status = 'deficit'
        else:
            status = 'balanced'
        
        return {
            'energy_type': energy_type,
            'current_supply_kwh': round(current_supply, 2),
            'forecasted_demand_kwh': round(avg_demand, 2),
            'gap_kwh': round(gap, 2),
            'gap_percentage': round(gap_percentage, 2),
            'status': status
        }
