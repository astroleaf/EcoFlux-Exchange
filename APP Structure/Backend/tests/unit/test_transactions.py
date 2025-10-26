"""
Unit Tests for Transactions
Tests transaction model and service
"""

import pytest
from datetime import datetime
from src.models.transaction import Transaction
from src.services.transaction_service import TransactionService


class TestTransactionModel:
    """Test Transaction model"""
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        tx = Transaction(
            energy_type='solar',
            quantity=100.0,
            price=0.12,
            order_type='buy',
            user_id='user-1'
        )
        
        assert tx.id is not None
        assert tx.energy_type == 'solar'
        assert tx.quantity == 100.0
        assert tx.price == 0.12
        assert tx.order_type == 'buy'
        assert tx.status == 'pending'
    
    def test_transaction_to_dict(self):
        """Test transaction serialization"""
        tx = Transaction(
            energy_type='wind',
            quantity=150.0,
            price=0.10,
            order_type='sell',
            user_id='user-2'
        )
        
        data = tx.to_dict()
        
        assert 'id' in data
        assert data['energy_type'] == 'wind'
        assert data['quantity'] == 150.0
        assert data['status'] == 'pending'
    
    def test_transaction_from_dict(self):
        """Test transaction deserialization"""
        data = {
            'id': 'test-tx-1',
            'energy_type': 'hydro',
            'quantity': 200.0,
            'price': 0.08,
            'order_type': 'buy',
            'user_id': 'user-3',
            'status': 'pending'
        }
        
        tx = Transaction.from_dict(data)
        
        assert tx.id == 'test-tx-1'
        assert tx.energy_type == 'hydro'
        assert tx.quantity == 200.0
    
    def test_update_status(self):
        """Test updating transaction status"""
        tx = Transaction(
            energy_type='biomass',
            quantity=80.0,
            price=0.15,
            order_type='sell',
            user_id='user-4'
        )
        
        tx.update_status('matched')
        
        assert tx.status == 'matched'
        assert tx.updated_at is not None
    
    def test_mark_completed(self):
        """Test marking transaction as completed"""
        tx = Transaction(
            energy_type='solar',
            quantity=100.0,
            price=0.12,
            order_type='buy',
            user_id='user-1'
        )
        
        tx.mark_completed('contract-123', execution_time=2.5)
        
        assert tx.status == 'completed'
        assert tx.contract_id == 'contract-123'
        assert tx.execution_time == 2.5
    
    def test_can_be_cancelled(self):
        """Test cancel eligibility"""
        tx = Transaction(
            energy_type='wind',
            quantity=150.0,
            price=0.10,
            order_type='sell',
            user_id='user-2'
        )
        
        assert tx.can_be_cancelled() is True
        
        tx.update_status('completed')
        assert tx.can_be_cancelled() is False


class TestTransactionService:
    """Test Transaction Service"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = TransactionService()
    
    def test_create_transaction(self):
        """Test creating a transaction via service"""
        tx = self.service.create_transaction(
            energy_type='solar',
            quantity=100.0,
            price=0.12,
            order_type='buy',
            user_id='user-1'
        )
        
        assert tx is not None
        assert tx.id is not None
        assert tx.status == 'pending'
    
    def test_get_transaction_by_id(self):
        """Test retrieving transaction by ID"""
        tx = self.service.create_transaction(
            energy_type='wind',
            quantity=150.0,
            price=0.10,
            order_type='sell',
            user_id='user-2'
        )
        
        retrieved = self.service.get_transaction_by_id(tx.id)
        
        assert retrieved is not None
        assert retrieved.id == tx.id
    
    def test_get_transactions(self):
        """Test listing transactions"""
        # Create some transactions
        self.service.create_transaction('solar', 100.0, 0.12, 'buy', 'user-1')
        self.service.create_transaction('wind', 150.0, 0.10, 'sell', 'user-2')
        
        transactions = self.service.get_transactions(limit=10)
        
        assert len(transactions) >= 2
    
    def test_get_statistics(self):
        """Test getting transaction statistics"""
        stats = self.service.get_statistics()
        
        assert 'total_transactions' in stats
        assert 'pending' in stats
        assert 'completed' in stats
        assert 'success_rate_percentage' in stats
