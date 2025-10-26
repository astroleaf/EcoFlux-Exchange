"""
API Package Initialization
Configures Flask app with all routes and middleware
"""

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import logging

# Initialize Flask app
def create_app(config_name='development'):
    """
    Application factory pattern
    Creates and configures Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    from ..config.settings import config
    app.config.from_object(config[config_name])
    
    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize SocketIO for real-time updates
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from .routes import trades, analytics, contracts, predictions
    
    app.register_blueprint(trades.bp, url_prefix='/api/trades')
    app.register_blueprint(analytics.bp, url_prefix='/api/analytics')
    app.register_blueprint(contracts.bp, url_prefix='/api/contracts')
    app.register_blueprint(predictions.bp, url_prefix='/api/predictions')
    
    # Register middleware
    from .middleware import auth, rate_limiter, error_handler
    
    error_handler.init_app(app)
    rate_limiter.init_app(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'green-energy-platform'}, 200
    
    return app, socketio

__all__ = ['create_app']
