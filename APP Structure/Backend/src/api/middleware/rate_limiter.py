"""
Rate Limiting Middleware
Prevents API abuse through rate limiting
"""

from flask import request, jsonify
from functools import wraps
import time
from collections import defaultdict
import threading

# In-memory rate limit storage (use Redis in production)
rate_limit_storage = defaultdict(list)
storage_lock = threading.Lock()

# Configuration
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 100  # requests per window

def init_app(app):
    """
    Initialize rate limiter with Flask app
    """
    @app.before_request
    def check_rate_limit():
        # Skip rate limiting for health check
        if request.path == '/health':
            return None
        
        # Get client identifier (IP address)
        client_id = request.remote_addr
        
        # Check rate limit
        if is_rate_limited(client_id):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds'
            }), 429
        
        # Record request
        record_request(client_id)
        return None


def is_rate_limited(client_id):
    """
    Check if client has exceeded rate limit
    """
    with storage_lock:
        current_time = time.time()
        window_start = current_time - RATE_LIMIT_WINDOW
        
        # Clean old requests
        rate_limit_storage[client_id] = [
            req_time for req_time in rate_limit_storage[client_id]
            if req_time > window_start
        ]
        
        # Check if limit exceeded
        return len(rate_limit_storage[client_id]) >= RATE_LIMIT_MAX_REQUESTS


def record_request(client_id):
    """
    Record a request timestamp
    """
    with storage_lock:
        current_time = time.time()
        rate_limit_storage[client_id].append(current_time)


def rate_limit(max_requests=None, window=None):
    """
    Decorator for custom rate limiting on specific endpoints
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = request.remote_addr
            limit = max_requests or RATE_LIMIT_MAX_REQUESTS
            time_window = window or RATE_LIMIT_WINDOW
            
            with storage_lock:
                current_time = time.time()
                window_start = current_time - time_window
                
                # Clean and check
                rate_limit_storage[f"{client_id}:{f.__name__}"] = [
                    req_time for req_time in rate_limit_storage[f"{client_id}:{f.__name__}"]
                    if req_time > window_start
                ]
                
                if len(rate_limit_storage[f"{client_id}:{f.__name__}"]) >= limit:
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'message': f'Maximum {limit} requests per {time_window} seconds'
                    }), 429
                
                rate_limit_storage[f"{client_id}:{f.__name__}"].append(current_time)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def cleanup_old_entries():
    """
    Periodic cleanup of old rate limit entries
    """
    with storage_lock:
        current_time = time.time()
        for client_id in list(rate_limit_storage.keys()):
            rate_limit_storage[client_id] = [
                req_time for req_time in rate_limit_storage[client_id]
                if req_time > (current_time - RATE_LIMIT_WINDOW * 2)
            ]
            
            # Remove empty entries
            if not rate_limit_storage[client_id]:
                del rate_limit_storage[client_id]
