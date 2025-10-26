"""
AI Prediction Routes
Handles AI/ML prediction endpoints
"""

from flask import Blueprint, request, jsonify
import logging

from ...services.ai_engine.price_predictor import PricePredictor
from ...services.ai_engine.demand_forecaster import DemandForecaster
from ...services.ai_engine.trend_analyzer import TrendAnalyzer

bp = Blueprint('predictions', __name__)
logger = logging.getLogger(__name__)

# Initialize AI services
price_predictor = PricePredictor()
demand_forecaster = DemandForecaster()
trend_analyzer = TrendAnalyzer()

@bp.route('/price', methods=['POST'])
def predict_price():
    """
    Predict future energy prices
    POST /api/predictions/price
    Body: {
        "energy_type": str,
        "horizon": int  // hours ahead
    }
    """
    try:
        data = request.get_json()
        
        if 'energy_type' not in data:
            return jsonify({'error': 'energy_type is required'}), 400
        
        horizon = data.get('horizon', 24)  # Default 24 hours
        
        prediction = price_predictor.predict(
            energy_type=data['energy_type'],
            horizon=horizon
        )
        
        return jsonify({
            'success': True,
            'prediction': prediction
        }), 200
        
    except Exception as e:
        logger.error(f"Error predicting price: {str(e)}")
        return jsonify({'error': 'Failed to predict price', 'details': str(e)}), 500


@bp.route('/demand', methods=['POST'])
def forecast_demand():
    """
    Forecast energy demand
    POST /api/predictions/demand
    Body: {
        "energy_type": str,
        "period": str  // "day", "week", "month"
    }
    """
    try:
        data = request.get_json()
        
        if 'energy_type' not in data:
            return jsonify({'error': 'energy_type is required'}), 400
        
        period = data.get('period', 'day')
        
        forecast = demand_forecaster.forecast(
            energy_type=data['energy_type'],
            period=period
        )
        
        return jsonify({
            'success': True,
            'forecast': forecast
        }), 200
        
    except Exception as e:
        logger.error(f"Error forecasting demand: {str(e)}")
        return jsonify({'error': 'Failed to forecast demand'}), 500


@bp.route('/trends', methods=['GET'])
def analyze_trends():
    """
    Analyze market trends
    GET /api/predictions/trends?energy_type=solar
    """
    try:
        energy_type = request.args.get('energy_type', None)
        
        trends = trend_analyzer.analyze(energy_type)
        
        return jsonify({
            'success': True,
            'trends': trends
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing trends: {str(e)}")
        return jsonify({'error': 'Failed to analyze trends'}), 500


@bp.route('/market-outlook', methods=['GET'])
def get_market_outlook():
    """
    Get comprehensive market outlook
    GET /api/predictions/market-outlook
    """
    try:
        outlook = {
            'price_predictions': price_predictor.get_all_predictions(),
            'demand_forecasts': demand_forecaster.get_all_forecasts(),
            'trend_analysis': trend_analyzer.analyze_market(),
            'recommendations': trend_analyzer.get_recommendations()
        }
        
        return jsonify({
            'success': True,
            'outlook': outlook
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting market outlook: {str(e)}")
        return jsonify({'error': 'Failed to get market outlook'}), 500


@bp.route('/volatility', methods=['GET'])
def get_volatility():
    """
    Get price volatility analysis
    GET /api/predictions/volatility?energy_type=wind
    """
    try:
        energy_type = request.args.get('energy_type')
        
        if not energy_type:
            return jsonify({'error': 'energy_type is required'}), 400
        
        volatility = price_predictor.calculate_volatility(energy_type)
        
        return jsonify({
            'success': True,
            'volatility': volatility
        }), 200
        
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}")
        return jsonify({'error': 'Failed to calculate volatility'}), 500
