"""
Transaction Service
Handles transaction business logic
"""

from datetime import datetime, timedelta
from typing import List, Optional
import logging

from ..models.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionService:
    """
    Service for managing energy trading transactions
    """
    
    def __init__(self):
        """
        Initialize transaction service
        In production, this would connect to a database
        """
        self.transactions = []  # In-memory storage (use DB in production)
        
    def create_transaction(self, energy_type, quantity, price, order_type, user_id):
        """
        Create a new transaction
        
        Args:
            energy_type: Type of energy
            quantity: Amount in kWh
            price: Price per kWh
            order_type: 'buy' or 'sell'
            user_id: ID of user creating transaction
            
        Returns:
            Transaction: Created transaction object
        """
        transaction = Transaction(
            energy_type=energy_type,
            quantity=quantity,
            price=price,
            order_type=order_type,
            user_id=user_id
        )
        
        self.transactions.append(transaction)
        logger.info(f"Transaction created: {transaction.id}")
        
        return transaction
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """
        Get transaction by ID
        """
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    
    def get_transactions(self, status: Optional[str] = None, limit: int = 50) -> List[Transaction]:
        """
        Get list of transactions with optional filtering
        
        Args:
            status: Filter by status (pending, matched, completed, cancelled)
            limit: Maximum number of transactions to return
            
        Returns:
            List of transactions
        """
        filtered = self.transactions
        
        if status:
            filtered = [t for t in filtered if t.status == status]
        
        # Sort by creation date (newest first)
        filtered = sorted(filtered, key=lambda x: x.created_at, reverse=True)
        
        return filtered[:limit]
    
    def cancel_transaction(self, transaction_id: str) -> bool:
        """
        Cancel a transaction
        
        Args:
            transaction_id: ID of transaction to cancel
            
        Returns:
            bool: True if cancelled successfully
        """
        transaction = self.get_transaction_by_id(transaction_id)
        
        if not transaction:
            logger.warning(f"Transaction not found: {transaction_id}")
            return False
        
        if not transaction.can_be_cancelled():
            logger.warning(f"Transaction cannot be cancelled: {transaction_id} (status: {transaction.status})")
            return False
        
        transaction.update_status('cancelled')
        logger.info(f"Transaction cancelled: {transaction_id}")
        
        return True
    
    def get_pending_orders(self, energy_type: Optional[str] = None) -> List[Transaction]:
        """
        Get all pending orders
        
        Args:
            energy_type: Filter by energy type
            
        Returns:
            List of pending transactions
        """
        pending = [t for t in self.transactions if t.status == 'pending']
        
        if energy_type:
            pending = [t for t in pending if t.energy_type == energy_type]
        
        return pending
    
    def get_statistics(self) -> dict:
        """
        Get transaction statistics
        
        Returns:
            Dictionary with various statistics
        """
        total = len(self.transactions)
        pending = len([t for t in self.transactions if t.status == 'pending'])
        matched = len([t for t in self.transactions if t.status == 'matched'])
        completed = len([t for t in self.transactions if t.status == 'completed'])
        cancelled = len([t for t in self.transactions if t.status == 'cancelled'])
        
        # Calculate total volume
        total_volume = sum(t.quantity for t in self.transactions if t.status == 'completed')
        
        # Calculate average execution time (in seconds)
        execution_times = [t.execution_time for t in self.transactions 
                          if t.execution_time is not None]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Success rate
        success_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            'total_transactions': total,
            'pending': pending,
            'matched': matched,
            'completed': completed,
            'cancelled': cancelled,
            'total_volume_kwh': total_volume,
            'average_execution_time_seconds': round(avg_execution_time, 2),
            'success_rate_percentage': round(success_rate, 2)
        }
    
    def get_user_transactions(self, user_id: str, limit: int = 50) -> List[Transaction]:
        """
        Get all transactions for a specific user
        """
        user_transactions = [t for t in self.transactions if t.user_id == user_id]
        user_transactions = sorted(user_transactions, key=lambda x: x.created_at, reverse=True)
        return user_transactions[:limit]
    
    def get_volume_by_energy_type(self) -> dict:
        """
        Get trading volume breakdown by energy type
        """
        volumes = {
            'solar': 0,
            'wind': 0,
            'hydro': 0,
            'biomass': 0
        }
        
        for transaction in self.transactions:
            if transaction.status == 'completed':
                volumes[transaction.energy_type] += transaction.quantity
        
        return volumes
    
    def cleanup_old_transactions(self, days: int = 90):
        """
        Remove transactions older than specified days
        
        Args:
            days: Number of days to keep
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        initial_count = len(self.transactions)
        
        self.transactions = [
            t for t in self.transactions 
            if t.created_at > cutoff_date or t.status in ['pending', 'matched']
        ]
        
        removed_count = initial_count - len(self.transactions)
        logger.info(f"Cleaned up {removed_count} old transactions")
        
        return removed_count
