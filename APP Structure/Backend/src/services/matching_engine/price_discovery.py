"""
Price Discovery
Algorithms for determining fair market prices
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class PriceDiscovery:
    """
    Price discovery mechanisms for energy trading
    """
    
    def __init__(self):
        """
        Initialize price discovery
        """
        self.price_history = {}
        
    def discover_price(self, energy_type: str, buy_orders: List, sell_orders: List):
        """
        Discover fair market price
        
        Uses volume-weighted average price (VWAP) methodology
        
        Args:
            energy_type: Type of energy
            buy_orders: List of buy orders
            sell_orders: List of sell orders
            
        Returns:
            Discovered price
        """
        if not buy_orders and not sell_orders:
            logger.warning(f"No orders for price discovery: {energy_type}")
            return None
        
        # Calculate VWAP for buy orders
        buy_vwap = self._calculate_vwap(buy_orders) if buy_orders else None
        
        # Calculate VWAP for sell orders
        sell_vwap = self._calculate_vwap(sell_orders) if sell_orders else None
        
        # Determine fair price
        if buy_vwap and sell_vwap:
            fair_price = (buy_vwap + sell_vwap) / 2
        elif buy_vwap:
            fair_price = buy_vwap
        else:
            fair_price = sell_vwap
        
        # Store in history
        if energy_type not in self.price_history:
            self.price_history[energy_type] = []
        
        self.price_history[energy_type].append({
            'price': fair_price,
            'buy_vwap': buy_vwap,
            'sell_vwap': sell_vwap,
            'timestamp': datetime.utcnow()
        })
        
        logger.info(f"Price discovered for {energy_type}: ${fair_price:.3f}")
        
        return {
            'energy_type': energy_type,
            'fair_price': round(fair_price, 3),
            'buy_vwap': round(buy_vwap, 3) if buy_vwap else None,
            'sell_vwap': round(sell_vwap, 3) if sell_vwap else None,
            'method': 'VWAP'
        }
    
    def _calculate_vwap(self, orders: List[Dict]):
        """
        Calculate Volume-Weighted Average Price
        
        VWAP = Σ(Price × Volume) / Σ(Volume)
        """
        total_value = sum(o['price'] * o['quantity'] for o in orders)
        total_volume = sum(o['quantity'] for o in orders)
        
        return total_value / total_volume if total_volume > 0 else 0
    
    def get_market_depth(self, energy_type: str, buy_orders: List, sell_orders: List):
        """
        Calculate market depth
        
        Shows cumulative volume at different price levels
        """
        # Sort orders by price
        buy_orders_sorted = sorted(buy_orders, key=lambda x: -x['price'])
        sell_orders_sorted = sorted(sell_orders, key=lambda x: x['price'])
        
        # Calculate cumulative volumes
        buy_depth = []
        cumulative_buy_volume = 0
        for order in buy_orders_sorted:
            cumulative_buy_volume += order['quantity']
            buy_depth.append({
                'price': order['price'],
                'cumulative_volume': cumulative_buy_volume
            })
        
        sell_depth = []
        cumulative_sell_volume = 0
        for order in sell_orders_sorted:
            cumulative_sell_volume += order['quantity']
            sell_depth.append({
                'price': order['price'],
                'cumulative_volume': cumulative_sell_volume
            })
        
        return {
            'energy_type': energy_type,
            'buy_depth': buy_depth,
            'sell_depth': sell_depth,
            'total_buy_volume': cumulative_buy_volume,
            'total_sell_volume': cumulative_sell_volume
        }
    
    def get_price_history(self, energy_type: str, limit: int = 50):
        """
        Get price discovery history
        """
        if energy_type not in self.price_history:
            return []
        
        history = self.price_history[energy_type][-limit:]
        
        return [
            {
                'price': h['price'],
                'timestamp': h['timestamp'].isoformat()
            }
            for h in history
        ]
