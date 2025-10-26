"""
Analytics Routes
Handles analytics and metrics endpoints
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import logging

from ...services.analytics_service import AnalyticsService
from ...services.ai_engine.trend_analyzer import TrendAnalyzer

bp = Blueprint('analytics', __name__)
logger = logging.getLogger(__name__)

# Initialize services
analytics_service = AnalyticsService()
trend_analyzer = TrendAnalyzer()

@bp.route('/dashboard', methods=['GET'])
def get_dashboard_metrics():
    """
    Get comprehensive dashboard metrics
    GET /api/analytics/dashboard
    """
    try:
        metrics = analytics_service.get_dashboard_metrics()
        
        return jsonify({
            'success': True,
            'metrics': metrics
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting dashboard metrics: {str(e)}")
        return jsonify({'error': 'Failed to get dashboard metrics'}), 500


@bp.route('/price-trends', methods=['GET'])
def get_price_trends():
    """
    Get price trends for all energy types
    GET /api/analytics/price-trends?period=7d
    """
    try:
        period = request.args.get('period', '7d')
        
        trends = analytics_service.get_price_trends(period)
        
        return jsonify({
            'success': True,
            'trends': trends
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting price trends: {str(e)}")
        return jsonify({'error': 'Failed to get price trends'}), 500


@bp.route('/market-analysis', methods=['GET'])
def get_market_analysis():
    """
    Get AI-powered market analysis
    GET /api/analytics/market-analysis
    """
    try:
        analysis = trend_analyzer.analyze_market()
        
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting market analysis: {str(e)}")
        return jsonify({'error': 'Failed to get market analysis'}), 500


@bp.route('/volume-by-type', methods=['GET'])
def get_volume_by_type():
    """
    Get trading volume breakdown by energy type
    GET /api/analytics/volume-by-type?period=30d
    """
    try:
        period = request.args.get('period', '30d')
        
        volume_data = analytics_service.get_volume_by_energy_type(period)
        
        return jsonify({
            'success': True,
            'volume': volume_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting volume data: {str(e)}")
        return jsonify({'error': 'Failed to get volume data'}), 500


@bp.route('/efficiency-metrics', methods=['GET'])
def get_efficiency_metrics():
    """
    Get platform efficiency metrics
    GET /api/analytics/efficiency-metrics
    """
    try:
        metrics = {
            'transaction_efficiency': analytics_service.calculate_transaction_efficiency(),
            'verification_time_reduction': analytics_service.calculate_verification_reduction(),
            'average_execution_time': analytics_service.get_average_execution_time(),
            'success_rate': analytics_service.get_success_rate(),
            'uptime_percentage': analytics_service.get_uptime_percentage()
        }
        
        return jsonify({
            'success': True,
            'metrics': metrics
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting efficiency metrics: {str(e)}")
        return jsonify({'error': 'Failed to get efficiency metrics'}), 500


@bp.route('/historical-data', methods=['GET'])
def get_historical_data():
    """
    Get historical trading data
    GET /api/analytics/historical-data?start_date=2025-01-01&end_date=2025-10-25
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date are required'}), 400
        
        historical_data = analytics_service.get_historical_data(start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': historical_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting historical data: {str(e)}")
        return jsonify({'error': 'Failed to get historical data'}), 500
