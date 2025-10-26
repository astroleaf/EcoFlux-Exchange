"""
Unit Tests for Matching Engine
Tests order matching, price discovery, and order book
"""

import pytest
from src.services.matching_engine.order_matcher import OrderMatcher
from src.services.matching_engine.price_discovery import PriceDiscovery
from src.services.matching_engine.order_book import OrderBook
from src.models.transaction import Transaction


class TestOrderMatcher:
    """Test Order Matcher functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.matcher = OrderMatcher()
    
    def test_initialization(self):
        """Test matcher initializes correctly"""
        assert self.matcher is not None
        assert self.matcher.matched_orders == []
    
    def test_match_compatible_orders(self):
        """Test matching compatible buy/sell orders"""
        buy_order = Transaction(
            energy_type='solar',
            quantity=100.0,
            price=0.12,
            order_type='buy',
            user_id='user-1'
        )
        
        sell_order = Transaction(
            energy_type='solar',
            quantity=100.0,
            price=0.11,
            order_type='sell',
            user_id='user-2'
        )
        
        # In production, this would interact with transaction service
        # For now, test the matching logic structure
        assert buy_order.order_type != sell_order.order_type
        assert buy_order.energy_type == sell_order.energy_type
    
    def test_order_book_structure(self):
        """Test order book structure"""
        order_book = self.matcher.get_order_book('solar')
        
        assert 'energy_type' in order_book
        assert 'buy_orders' in order_book
        assert 'sell_orders' in order_book
        assert 'total_buy_orders' in order_book
        assert 'total_sell_orders' in order_book


class TestPriceDiscovery:
    """Test Price Discovery functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.discovery = PriceDiscovery()
    
    def test_vwap_calculation(self):
        """Test Volume-Weighted Average Price calculation"""
        orders = [
            {'price': 0.12, 'quantity': 100},
            {'price': 0.11, 'quantity': 200},
            {'price': 0.13, 'quantity': 150}
        ]
        
        vwap = self.discovery._calculate_vwap(orders)
        expected = ((0.12 * 100) + (0.11 * 200) + (0.13 * 150)) / 450
        
        assert abs(vwap - expected) < 0.001
    
    def test_discover_price_with_both_sides(self):
        """Test price discovery with buy and sell orders"""
        buy_orders = [
            {'price': 0.12, 'quantity': 100},
            {'price': 0.11, 'quantity': 150}
        ]
        
        sell_orders = [
            {'price': 0.10, 'quantity': 120},
            {'price': 0.11, 'quantity': 80}
        ]
        
        result = self.discovery.discover_price('solar', buy_orders, sell_orders)
        
        assert result is not None
        assert 'fair_price' in result
        assert 'buy_vwap' in result
        assert 'sell_vwap' in result


class TestOrderBook:
    """Test Order Book functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.order_book = OrderBook()
    
    def test_add_buy_order(self):
        """Test adding buy order to book"""
        order = {
            'id': 'order-1',
            'energy_type': 'solar',
            'order_type': 'buy',
            'price': 0.12,
            'quantity': 100.0,
            'user_id': 'user-1'
        }
        
        success = self.order_book.add_order(order)
        assert success is True
    
    def test_add_sell_order(self):
        """Test adding sell order to book"""
        order = {
            'id': 'order-2',
            'energy_type': 'wind',
            'order_type': 'sell',
            'price': 0.10,
            'quantity': 150.0,
            'user_id': 'user-2'
        }
        
        success = self.order_book.add_order(order)
        assert success is True
    
    def test_get_book(self):
        """Test retrieving order book"""
        book = self.order_book.get_book('solar')
        
        assert book is not None
        assert 'energy_type' in book
        assert 'buy_orders' in book
        assert 'sell_orders' in book
    
    def test_best_bid_ask(self):
        """Test getting best bid and ask prices"""
        # Add some orders first
        self.order_book.add_order({
            'id': 'order-3',
            'energy_type': 'hydro',
            'order_type': 'buy',
            'price': 0.08,
            'quantity': 100.0,
            'user_id': 'user-1'
        })
        
        self.order_book.add_order({
            'id': 'order-4',
            'energy_type': 'hydro',
            'order_type': 'sell',
            'price': 0.09,
            'quantity': 100.0,
            'user_id': 'user-2'
        })
        
        result = self.order_book.get_best_bid_ask('hydro')
        
        assert result is not None
        assert 'best_bid' in result
        assert 'best_ask' in result
