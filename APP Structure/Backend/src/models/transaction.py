"""
Transaction Model
Represents an energy trading transaction
"""

from datetime import datetime
import uuid


class Transaction:
    """
    Energy trading transaction model
    """
    
    def __init__(self, energy_type, quantity, price, order_type, user_id, 
                 transaction_id=None, status='pending', created_at=None):
        """
        Initialize a transaction
        
        Args:
            energy_type: Type of energy (solar, wind, hydro, biomass)
            quantity: Amount of energy in kWh
            price: Price per kWh
            order_type: Type of order (buy, sell)
            user_id: ID of user creating transaction
            transaction_id: Unique transaction ID (generated if not provided)
            status: Transaction status (pending, matched, completed, cancelled)
            created_at: Timestamp of creation
        """
        self.id = transaction_id or str(uuid.uuid4())
        self.energy_type = energy_type
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.user_id = user_id
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.matched_with = None
        self.contract_id = None
        self.execution_time = None
        
    def to_dict(self):
        """
        Convert transaction to dictionary
        """
        return {
            'id': self.id,
            'energy_type': self.energy_type,
            'quantity': self.quantity,
            'price': self.price,
            'order_type': self.order_type,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'matched_with': self.matched_with,
            'contract_id': self.contract_id,
            'execution_time': self.execution_time
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create transaction from dictionary
        """
        transaction = cls(
            energy_type=data['energy_type'],
            quantity=data['quantity'],
            price=data['price'],
            order_type=data['order_type'],
            user_id=data['user_id'],
            transaction_id=data.get('id'),
            status=data.get('status', 'pending')
        )
        
        if 'created_at' in data:
            transaction.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            transaction.updated_at = datetime.fromisoformat(data['updated_at'])
        if 'matched_with' in data:
            transaction.matched_with = data['matched_with']
        if 'contract_id' in data:
            transaction.contract_id = data['contract_id']
        if 'execution_time' in data:
            transaction.execution_time = data['execution_time']
            
        return transaction
    
    def update_status(self, new_status):
        """
        Update transaction status
        """
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def mark_matched(self, matched_transaction_id):
        """
        Mark transaction as matched with another
        """
        self.matched_with = matched_transaction_id
        self.update_status('matched')
    
    def mark_completed(self, contract_id, execution_time):
        """
        Mark transaction as completed
        """
        self.contract_id = contract_id
        self.execution_time = execution_time
        self.update_status('completed')
    
    def can_be_cancelled(self):
        """
        Check if transaction can be cancelled
        """
        return self.status in ['pending', 'matched']
    
    def __repr__(self):
        return f"<Transaction {self.id} - {self.order_type} {self.quantity}kWh {self.energy_type} @ ${self.price}>"
