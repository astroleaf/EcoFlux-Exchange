"""
Notification Service
Handles real-time notifications via WebSocket
"""

import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for managing real-time notifications
    """
    
    def __init__(self):
        """
        Initialize notification service
        """
        self.subscribers = {}  # user_id -> callback
        self.notification_history = []
        
    def subscribe(self, user_id: str, callback):
        """
        Subscribe a user to notifications
        
        Args:
            user_id: User ID to subscribe
            callback: Function to call when notification is sent
        """
        self.subscribers[user_id] = callback
        logger.info(f"User subscribed to notifications: {user_id}")
    
    def unsubscribe(self, user_id: str):
        """
        Unsubscribe a user from notifications
        """
        if user_id in self.subscribers:
            del self.subscribers[user_id]
            logger.info(f"User unsubscribed from notifications: {user_id}")
    
    def notify_user(self, user_id: str, notification: Dict):
        """
        Send notification to specific user
        
        Args:
            user_id: Target user ID
            notification: Notification data
        """
        notification['timestamp'] = datetime.utcnow().isoformat()
        
        if user_id in self.subscribers:
            try:
                self.subscribers[user_id](notification)
                logger.info(f"Notification sent to user {user_id}: {notification['type']}")
            except Exception as e:
                logger.error(f"Error sending notification to {user_id}: {str(e)}")
        
        # Store in history
        self.notification_history.append({
            'user_id': user_id,
            'notification': notification
        })
    
    def broadcast(self, notification: Dict):
        """
        Broadcast notification to all subscribers
        """
        notification['timestamp'] = datetime.utcnow().isoformat()
        
        for user_id in list(self.subscribers.keys()):
            try:
                self.subscribers[user_id](notification)
            except Exception as e:
                logger.error(f"Error broadcasting to {user_id}: {str(e)}")
        
        logger.info(f"Broadcast sent to {len(self.subscribers)} subscribers: {notification['type']}")
    
    def notify_trade_matched(self, buyer_id: str, seller_id: str, transaction_data: Dict):
        """
        Notify users when their trade is matched
        """
        notification = {
            'type': 'trade_matched',
            'title': 'Trade Matched!',
            'message': f"Your {transaction_data['order_type']} order for {transaction_data['quantity']}kWh of {transaction_data['energy_type']} has been matched.",
            'data': transaction_data
        }
        
        self.notify_user(buyer_id, notification)
        self.notify_user(seller_id, notification)
    
    def notify_contract_executed(self, user_id: str, contract_data: Dict):
        """
        Notify user when contract is executed
        """
        notification = {
            'type': 'contract_executed',
            'title': 'Contract Executed',
            'message': f"Smart contract for {contract_data['quantity']}kWh of {contract_data['energy_type']} has been executed successfully.",
            'data': contract_data
        }
        
        self.notify_user(user_id, notification)
    
    def notify_price_alert(self, user_id: str, energy_type: str, price: float, threshold: float):
        """
        Notify user about price changes
        """
        notification = {
            'type': 'price_alert',
            'title': 'Price Alert',
            'message': f"{energy_type.capitalize()} energy price is now ${price}/kWh (threshold: ${threshold}/kWh)",
            'data': {
                'energy_type': energy_type,
                'current_price': price,
                'threshold': threshold
            }
        }
        
        self.notify_user(user_id, notification)
    
    def get_user_notifications(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Get notification history for a user
        """
        user_notifications = [
            item['notification'] for item in self.notification_history
            if item['user_id'] == user_id
        ]
        
        # Return most recent first
        return user_notifications[-limit:][::-1]
    
    def clear_old_notifications(self, days: int = 30):
        """
        Clear notifications older than specified days
        """
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        initial_count = len(self.notification_history)
        self.notification_history = [
            item for item in self.notification_history
            if datetime.fromisoformat(item['notification']['timestamp']) > cutoff
        ]
        
        removed = initial_count - len(self.notification_history)
        logger.info(f"Cleared {removed} old notifications")
        
        return removed
