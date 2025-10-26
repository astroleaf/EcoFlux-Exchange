"""
Error Handling Middleware
Global error handling for the application
"""

from flask import jsonify
import logging
import traceback

logger = logging.getLogger(__name__)

def init_app(app):
    """
    Initialize error handlers with Flask app
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request"""
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized"""
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden"""
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed"""
        return jsonify({
            'error': 'Method Not Allowed',
            'message': str(error)
        }), 405
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle 429 Too Many Requests"""
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        logger.error(f"Internal server error: {str(error)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all uncaught exceptions"""
        logger.error(f"Unhandled exception: {str(error)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'details': str(error) if app.debug else None
        }), 500


class APIException(Exception):
    """
    Custom API Exception class
    """
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv


class ValidationError(APIException):
    """Validation error"""
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=400, payload=payload)


class AuthenticationError(APIException):
    """Authentication error"""
    def __init__(self, message='Authentication required', payload=None):
        super().__init__(message, status_code=401, payload=payload)


class AuthorizationError(APIException):
    """Authorization error"""
    def __init__(self, message='Permission denied', payload=None):
        super().__init__(message, status_code=403, payload=payload)


class NotFoundError(APIException):
    """Resource not found error"""
    def __init__(self, message='Resource not found', payload=None):
        super().__init__(message, status_code=404, payload=payload)
