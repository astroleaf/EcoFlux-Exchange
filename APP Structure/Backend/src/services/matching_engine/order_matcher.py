"""
Order Matcher
Matches buy and sell orders using price-time priority
"""

import logging
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)


class OrderMatcher:
    """
    Matches trading orders using price-time priority algorithm
    """
    
    def __init__(self):
        """
        Initialize order matcher
        """
        self.matched_orders = []
        self.matching_statistics = {
            'total_matches': 0,
            'total_volume': 0.0,
            'average_match_time': 0.0
        }
        
    def match_order(self, new_order):
        """
        Attempt to match a new order
        
        Args:
            new_order: Transaction object to match
            
        Returns:
            bool: True if matched, False otherwise
        """
        from ...services.transaction_service import TransactionService
        
        transaction_service = TransactionService()
        
        # Get pending orders of opposite type
        opposite_type = 'sell' if new_order.order_type == 'buy' else 'buy'
        
        pending_orders = [
            t for t in transaction_service.get_pending_orders(new_order.energy_type)
            if t.order_type == opposite_type
        ]
        
        if not pending_orders:
            logger.info(f"No matching orders found for {new_order.id}")
            return False
        
        # Find best match using price-time priority
        best_match = self._find_best_match(new_order, pending_orders)
        
        if best_match:
            # Execute match
            self._execute_match(new_order, best_match)
            logger.info(f"Order matched: {new_order.id} with {best_match.id}")
            return True
        
        return False
    
    def _find_best_match(self, order, candidates: List):
        """
        Find best matching order using price-time priority
        
        Price-time priority:
        1. Best price (lowest for buy, highest for sell)
        2. Earliest timestamp if prices are equal
        """
        if not candidates:
            return None
        
        # Filter by price compatibility
        if order.order_type == 'buy':
            # Buyer willing to pay up to order.price
            # Match with sellers asking <= order.price
            compatible = [c for c in candidates if c.price <= order.price]
            # Sort by price (ascending) then time (ascending)
            compatible.sort(key=lambda x: (x.price, x.created_at))
        else:
            # Seller asking for >= order.price
            # Match with buyers willing to pay >= order.price
            compatible = [c for c in candidates if c.price >= order.price]
            # Sort by price (descending) then time (ascending)
            compatible.sort(key=lambda x: (-x.price, x.created_at))
        
        return compatible if compatible else None
    
    def _execute_match(self, order1, order2):
        """
        Execute a match between two orders
        """
        from ...services.blockchain.contract_deployer import ContractDeployer
        
        # Determine buyer and seller
        if order1.order_type == 'buy':
            buyer_order = order1
            seller_order = order2
        else:
            buyer_order = order2
            seller_order = order1
        
        # Calculate execution price (average of bid and ask)
        execution_price = (buyer_order.price + seller_order.price) / 2
        
        # Mark orders as matched
        order1.mark_matched(order2.id)
        order2.mark_matched(order1.id)
        
        # Deploy smart contract
        contract_deployer = ContractDeployer()
        contract = contract_deployer.deploy(
            buyer_id=buyer_order.user_id,
            seller_id=seller_order.user_id,
            energy_type=order1.energy_type,
            quantity=order1.quantity,
            price=execution_price
        )
        
        # Execute contract
        import time
        start_time = time.time()
        from ...services.blockchain.smart_contract import SmartContractExecutor
        
        executor = SmartContractExecutor()
        executor.execute(contract['id'])
        
        execution_time = time.time() - start_time
        
        # Mark orders as completed
        order1.mark_completed(contract['id'], execution_time)
        order2.mark_completed(contract['id'], execution_time)
        
        # Update statistics
        self.matching_statistics['total_matches'] += 1
        self.matching_statistics['total_volume'] += order1.quantity
        
        # Calculate average match time
        total_time = self.matching_statistics['average_match_time'] * (self.matching_statistics['total_matches'] - 1)
        total_time += execution_time
        self.matching_statistics['average_match_time'] = total_time / self.matching_statistics['total_matches']
        
        # Record match
        self.matched_orders.append({
            'order1_id': order1.id,
            'order2_id': order2.id,
            'contract_id': contract['id'],
            'execution_price': execution_price,
            'quantity': order1.quantity,
            'execution_time': execution_time,
            'matched_at': datetime.utcnow()
        })
        
        logger.info(f"Match executed: {execution_time:.3f}s, Price: ${execution_price}")
    
    def get_order_book(self, energy_type: Optional[str] = None):
        """
        Get current order book
        
        Args:
            energy_type: Filter by energy type
            
        Returns:
            Order book with buy and sell orders
        """
        from ...services.transaction_service import TransactionService
        
        transaction_service = TransactionService()
        pending = transaction_service.get_pending_orders(energy_type)
        
        buy_orders = [o.to_dict() for o in pending if o.order_type == 'buy']
        sell_orders = [o.to_dict() for o in pending if o.order_type == 'sell']
        
        # Sort orders
        buy_orders.sort(key=lambda x: (-x['price'], x['created_at']))  # Highest price first
        sell_orders.sort(key=lambda x: (x['price'], x['created_at']))  # Lowest price first
        
        return {
            'energy_type': energy_type,
            'buy_orders': buy_orders,
            'sell_orders': sell_orders,
            'total_buy_orders': len(buy_orders),
            'total_sell_orders': len(sell_orders),
            'spread': self._calculate_spread(buy_orders, sell_orders)
        }
    
    def _calculate_spread(self, buy_orders: List, sell_orders: List):
        """
        Calculate bid-ask spread
        """
        if not buy_orders or not sell_orders:
            return None
        
        best_bid = max(o['price'] for o in buy_orders)
        best_ask = min(o['price'] for o in sell_orders)
        
        spread = best_ask - best_bid
        spread_percentage = (spread / best_ask) * 100 if best_ask > 0 else 0
        
        return {
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': round(spread, 3),
            'spread_percentage': round(spread_percentage, 2)
        }
    
    def get_statistics(self):
        """
        Get matching engine statistics
        """
        return {
            'total_matches': self.matching_statistics['total_matches'],
            'total_volume_kwh': round(self.matching_statistics['total_volume'], 2),
            'average_match_time_seconds': round(self.matching_statistics['average_match_time'], 3),
            'recent_matches': len([m for m in self.matched_orders if (datetime.utcnow() - m['matched_at']).total_seconds() < 3600])
        }
