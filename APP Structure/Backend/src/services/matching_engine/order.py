"""
Order Book
Manages the order book for energy trading
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class OrderBook:
    """
    Order book management for energy trading
    """
    
    def __init__(self):
        """
        Initialize order book
        """
        self.books = {
            'solar': {'buy': [], 'sell': []},
            'wind': {'buy': [], 'sell': []},
            'hydro': {'buy': [], 'sell': []},
            'biomass': {'buy': [], 'sell': []}
        }
        
    def add_order(self, order: Dict):
        """
        Add order to book
        
        Args:
            order: Order dictionary with energy_type, order_type, price, quantity
        """
        energy_type = order['energy_type']
        order_type = order['order_type']
        
        if energy_type not in self.books:
            logger.error(f"Unknown energy type: {energy_type}")
            return False
        
        # Add to appropriate book
        self.books[energy_type][order_type].append({
            'id': order['id'],
            'price': order['price'],
            'quantity': order['quantity'],
            'user_id': order['user_id'],
            'timestamp': datetime.utcnow()
        })
        
        # Sort orders
        self._sort_book(energy_type, order_type)
        
        logger.info(f"Order added to book: {order['id']} ({energy_type} {order_type})")
        
        return True
    
    def remove_order(self, energy_type: str, order_type: str, order_id: str):
        """
        Remove order from book
        """
        if energy_type not in self.books:
            return False
        
        initial_count = len(self.books[energy_type][order_type])
        self.books[energy_type][order_type] = [
            o for o in self.books[energy_type][order_type]
            if o['id'] != order_id
        ]
        
        removed = initial_count > len(self.books[energy_type][order_type])
        
        if removed:
            logger.info(f"Order removed from book: {order_id}")
        
        return removed
    
    def _sort_book(self, energy_type: str, order_type: str):
        """
        Sort orders in book
        
        Buy orders: Descending price, then ascending time
        Sell orders: Ascending price, then ascending time
        """
        if order_type == 'buy':
            # Highest price first
            self.books[energy_type][order_type].sort(
                key=lambda x: (-x['price'], x['timestamp'])
            )
        else:
            # Lowest price first
            self.books[energy_type][order_type].sort(
                key=lambda x: (x['price'], x['timestamp'])
            )
    
    def get_book(self, energy_type: str):
        """
        Get order book for energy type
        """
        if energy_type not in self.books:
            return None
        
        return {
            'energy_type': energy_type,
            'buy_orders': self.books[energy_type]['buy'].copy(),
            'sell_orders': self.books[energy_type]['sell'].copy(),
            'total_buy_volume': sum(o['quantity'] for o in self.books[energy_type]['buy']),
            'total_sell_volume': sum(o['quantity'] for o in self.books[energy_type]['sell']),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_all_books(self):
        """
        Get all order books
        """
        all_books = {}
        
        for energy_type in self.books.keys():
            all_books[energy_type] = self.get_book(energy_type)
        
        return all_books
    
    def get_best_bid_ask(self, energy_type: str):
        """
        Get best bid and ask prices
        """
        if energy_type not in self.books:
            return None
        
        buy_orders = self.books[energy_type]['buy']
        sell_orders = self.books[energy_type]['sell']
        
        best_bid = buy_orders['price'] if buy_orders else None
        best_ask = sell_orders['price'] if sell_orders else None
        
        spread = (best_ask - best_bid) if (best_bid and best_ask) else None
        
        return {
            'energy_type': energy_type,
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': round(spread, 3) if spread else None,
            'mid_price': round((best_bid + best_ask) / 2, 3) if (best_bid and best_ask) else None
        }
    
    def clear_filled_orders(self, energy_type: str):
        """
        Clear filled or expired orders
        """
        # In production, this would remove expired orders
        # For now, we keep all pending orders
        logger.info(f"Order book cleared for {energy_type}")
