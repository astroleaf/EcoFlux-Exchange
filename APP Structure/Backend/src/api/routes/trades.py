"""
Trade Routes
Handles all trading-related endpoints
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

from ...services.transaction_service import TransactionService
from ...services.matching_engine.order_matcher import OrderMatcher
from ...models.transaction import Transaction
from ..middleware.auth import require_auth

bp = Blueprint('trades', __name__)
logger = logging.getLogger(__name__)

# Initialize services
transaction_service = TransactionService()
order_matcher = OrderMatcher()

@bp.route('/create', methods=['POST'])
def create_trade():
    """
    Create a new trade order
    POST /api/trades/create
    Body: {
        "energy_type": "solar|wind|hydro|biomass",
        "quantity": float,
        "price": float,
        "order_type": "buy|sell",
        "user_id": str
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['energy_type', 'quantity', 'price', 'order_type', 'user_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate energy type
        valid_energy_types = ['solar', 'wind', 'hydro', 'biomass']
        if data['energy_type'] not in valid_energy_types:
            return jsonify({'error': f'Invalid energy type. Must be one of: {valid_energy_types}'}), 400
        
        # Validate order type
        if data['order_type'] not in ['buy', 'sell']:
            return jsonify({'error': 'Invalid order type. Must be buy or sell'}), 400
        
        # Validate quantities
        if data['quantity'] <= 0 or data['price'] <= 0:
            return jsonify({'error': 'Quantity and price must be positive'}), 400
        
        # Create transaction
        transaction = transaction_service.create_transaction(
            energy_type=data['energy_type'],
            quantity=data['quantity'],
            price=data['price'],
            order_type=data['order_type'],
            user_id=data['user_id']
        )
        
        # Attempt to match order
        matched = order_matcher.match_order(transaction)
        
        logger.info(f"Trade created: {transaction.id}, Matched: {matched}")
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict(),
            'matched': matched,
            'message': 'Trade created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating trade: {str(e)}")
        return jsonify({'error': 'Failed to create trade', 'details': str(e)}), 500


@bp.route('/list', methods=['GET'])
def list_trades():
    """
    Get list of all trades
    GET /api/trades/list?status=pending|matched|completed&limit=50
    """
    try:
        status = request.args.get('status', None)
        limit = int(request.args.get('limit', 50))
        
        trades = transaction_service.get_transactions(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'trades': [trade.to_dict() for trade in trades],
            'count': len(trades)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing trades: {str(e)}")
        return jsonify({'error': 'Failed to list trades'}), 500


@bp.route('/<transaction_id>', methods=['GET'])
def get_trade(transaction_id):
    """
    Get specific trade by ID
    GET /api/trades/{transaction_id}
    """
    try:
        trade = transaction_service.get_transaction_by_id(transaction_id)
        
        if not trade:
            return jsonify({'error': 'Trade not found'}), 404
        
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting trade: {str(e)}")
        return jsonify({'error': 'Failed to get trade'}), 500


@bp.route('/<transaction_id>/cancel', methods=['POST'])
def cancel_trade(transaction_id):
    """
    Cancel a pending trade
    POST /api/trades/{transaction_id}/cancel
    """
    try:
        success = transaction_service.cancel_transaction(transaction_id)
        
        if not success:
            return jsonify({'error': 'Trade not found or cannot be cancelled'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Trade cancelled successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error cancelling trade: {str(e)}")
        return jsonify({'error': 'Failed to cancel trade'}), 500


@bp.route('/order-book', methods=['GET'])
def get_order_book():
    """
    Get current order book (all pending orders)
    GET /api/trades/order-book?energy_type=solar
    """
    try:
        energy_type = request.args.get('energy_type', None)
        
        order_book = order_matcher.get_order_book(energy_type)
        
        return jsonify({
            'success': True,
            'order_book': order_book
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting order book: {str(e)}")
        return jsonify({'error': 'Failed to get order book'}), 500


@bp.route('/stats', methods=['GET'])
def get_trade_stats():
    """
    Get trading statistics
    GET /api/trades/stats
    """
    try:
        stats = transaction_service.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Failed to get statistics'}), 500
