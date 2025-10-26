"""
Unit Tests for AI Engine
Tests price predictor, demand forecaster, and trend analyzer
"""

import pytest
from datetime import datetime
from src.services.ai_engine.price_predictor import PricePredictor
from src.services.ai_engine.demand_forecaster import DemandForecaster
from src.services.ai_engine.trend_analyzer import TrendAnalyzer


class TestPricePredictor:
    """Test Price Predictor functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.predictor = PricePredictor()
    
    def test_initialization(self):
        """Test predictor initializes correctly"""
        assert self.predictor is not None
        assert len(self.predictor.base_prices) == 4
        assert 'solar' in self.predictor.base_prices
    
    def test_predict_valid_energy_type(self):
        """Test prediction for valid energy type"""
        result = self.predictor.predict('solar', horizon=24)
        
        assert 'energy_type' in result
        assert result['energy_type'] == 'solar'
        assert 'predictions' in result
        assert len(result['predictions']) == 24
        assert 'current_price' in result
    
    def test_predict_invalid_energy_type(self):
        """Test prediction with invalid energy type"""
        with pytest.raises(ValueError):
            self.predictor.predict('nuclear', horizon=24)
    
    def test_prediction_structure(self):
        """Test prediction output structure"""
        result = self.predictor.predict('wind', horizon=12)
        
        prediction = result['predictions']
        assert 'timestamp' in prediction
        assert 'price' in prediction
        assert 'confidence' in prediction
        assert 0.0 <= prediction['confidence'] <= 1.0
    
    def test_volatility_calculation(self):
        """Test volatility calculation"""
        volatility = self.predictor.calculate_volatility('solar')
        
        assert 'level' in volatility
        assert volatility['level'] in ['low', 'medium', 'high']
        assert 'coefficient_of_variation' in volatility
        assert 'std_deviation' in volatility
    
    def test_all_predictions(self):
        """Test getting predictions for all energy types"""
        all_predictions = self.predictor.get_all_predictions()
        
        assert len(all_predictions) == 4
        assert 'solar' in all_predictions
        assert 'wind' in all_predictions


class TestDemandForecaster:
    """Test Demand Forecaster functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.forecaster = DemandForecaster()
    
    def test_forecast_day(self):
        """Test daily demand forecast"""
        result = self.forecaster.forecast('solar', period='day')
        
        assert 'energy_type' in result
        assert 'period' in result
        assert result['period'] == 'day'
        assert 'forecasts' in result
        assert len(result['forecasts']) > 0
    
    def test_forecast_week(self):
        """Test weekly demand forecast"""
        result = self.forecaster.forecast('wind', period='week')
        
        assert result['period'] == 'week'
        assert 'average_demand_kwh' in result
        assert 'demand_level' in result
    
    def test_forecast_structure(self):
        """Test forecast output structure"""
        result = self.forecaster.forecast('hydro', period='day')
        
        forecast = result['forecasts']
        assert 'timestamp' in forecast
        assert 'demand_kwh' in forecast
        assert 'confidence' in forecast
    
    def test_supply_gap_prediction(self):
        """Test supply-demand gap prediction"""
        gap = self.forecaster.predict_supply_gap('biomass')
        
        assert 'energy_type' in gap
        assert 'current_supply_kwh' in gap
        assert 'forecasted_demand_kwh' in gap
        assert 'gap_kwh' in gap
        assert 'status' in gap
        assert gap['status'] in ['surplus', 'deficit', 'balanced']


class TestTrendAnalyzer:
    """Test Trend Analyzer functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = TrendAnalyzer()
    
    def test_analyze_single_energy(self):
        """Test trend analysis for single energy type"""
        result = self.analyzer.analyze('solar')
        
        assert 'energy_type' in result
        assert 'trend' in result
        assert result['trend'] in ['bullish', 'bearish', 'neutral']
        assert 'strength' in result
        assert 'momentum_score' in result
    
    def test_analyze_all_energies(self):
        """Test analysis for all energy types"""
        result = self.analyzer.analyze()
        
        assert len(result) == 4
        assert 'solar' in result
        assert 'wind' in result
    
    def test_market_analysis(self):
        """Test overall market analysis"""
        analysis = self.analyzer.analyze_market()
        
        assert 'overall_trend' in analysis
        assert 'average_momentum' in analysis
        assert 'average_sentiment' in analysis
        assert 'market_health' in analysis
    
    def test_recommendations(self):
        """Test trading recommendations"""
        recommendations = self.analyzer.get_recommendations()
        
        assert len(recommendations) == 4
        for rec in recommendations:
            assert 'energy_type' in rec
            assert 'action' in rec
            assert rec['action'] in ['buy', 'sell', 'hold']
            assert 'reason' in rec
