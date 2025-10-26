"""
Integration Tests for API Endpoints
Tests API routes and responses
"""

import pytest
import json
from src.api import create_app


@pytest.fixture
def client():
    """Create test client"""
    app, socketio = create_app('testing')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestTradeEndpoints:
    """Test trade API endpoints"""
    
    def test_create_trade(self, client):
        """Test creating a trade"""
        trade_data = {
            'energy_type': 'solar',
            'quantity': 100.0,
            'price': 0.12,
            'order_type': 'buy',
            'user_id': 'test-user-1'
        }
        
        response = client.post(
            '/api/trades/create',
            data=json.dumps(trade_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'transaction' in data
    
    def test_list_trades(self, client):
        """Test listing trades"""
        response = client.get('/api/trades/list')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'trades' in data
        assert 'count' in data


class TestAnalyticsEndpoints:
    """Test analytics API endpoints"""
    
    def test_dashboard_metrics(self, client):
        """Test getting dashboard metrics"""
        response = client.get('/api/analytics/dashboard')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'metrics' in data
    
    def test_efficiency_metrics(self, client):
        """Test efficiency metrics endpoint"""
        response = client.get('/api/analytics/efficiency-metrics')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'metrics' in data
        
        metrics = data['metrics']
        assert 'transaction_efficiency' in metrics
        assert 'verification_time_reduction' in metrics
