"""
Main Application Entry Point
Runs the Flask application
"""

import os
from api import create_app
from utils.logger import setup_logger

# Setup logger
logger = setup_logger()

# Get environment
env = os.getenv('FLASK_ENV', 'development')

# Create Flask app
app, socketio = create_app(env)

if __name__ == '__main__':
    """
    Run the application
    """
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = env == 'development'
    
    logger.info(f"Starting Green Energy Platform - Environment: {env}")
    logger.info(f"Server running on http://{host}:{port}")
    logger.info(f"API endpoints available at http://{host}:{port}/api")
    
    # Run with SocketIO
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        log_output=True
    )
