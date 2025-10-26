"""
User Model
Represents a platform user
"""

from datetime import datetime
import uuid
import hashlib


class User:
    """
    User model for the energy trading platform
    """
    
    def __init__(self, username, email, password_hash=None, user_id=None, 
                 role='trader', created_at=None):
        """
        Initialize a user
        
        Args:
            username: User's username
            email: User's email address
            password_hash: Hashed password
            user_id: Unique user ID (generated if not provided)
            role: User role (trader, admin, viewer)
            created_at: Account creation timestamp
        """
        self.id = user_id or str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.last_login = None
        self.is_active = True
        self.total_trades = 0
        self.total_volume = 0.0
        self.wallet_balance = 10000.0  # Starting balance
        
    def to_dict(self, include_sensitive=False):
        """
        Convert user to dictionary
        
        Args:
            include_sensitive: Whether to include password hash
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'total_trades': self.total_trades,
            'total_volume': self.total_volume,
            'wallet_balance': self.wallet_balance
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create user from dictionary
        """
        user = cls(
            username=data['username'],
            email=data['email'],
            password_hash=data.get('password_hash'),
            user_id=data.get('id'),
            role=data.get('role', 'trader')
        )
        
        if 'created_at' in data:
            user.created_at = datetime.fromisoformat(data['created_at'])
        if 'last_login' in data and data['last_login']:
            user.last_login = datetime.fromisoformat(data['last_login'])
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'total_trades' in data:
            user.total_trades = data['total_trades']
        if 'total_volume' in data:
            user.total_volume = data['total_volume']
        if 'wallet_balance' in data:
            user.wallet_balance = data['wallet_balance']
            
        return user
    
    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA-256
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """
        Verify password against hash
        """
        return self.password_hash == self.hash_password(password)
    
    def update_last_login(self):
        """
        Update last login timestamp
        """
        self.last_login = datetime.utcnow()
    
    def increment_trade_count(self, volume):
        """
        Increment total trades and volume
        """
        self.total_trades += 1
        self.total_volume += volume
    
    def update_balance(self, amount):
        """
        Update wallet balance
        
        Args:
            amount: Amount to add (positive) or subtract (negative)
        """
        self.wallet_balance += amount
        return self.wallet_balance
    
    def has_sufficient_balance(self, required_amount):
        """
        Check if user has sufficient balance
        """
        return self.wallet_balance >= required_amount
    
    def __repr__(self):
        return f"<User {self.username} ({self.email})>"
