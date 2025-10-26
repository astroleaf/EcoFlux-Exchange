"""
Constants
Application constants and configuration values
"""

# Energy types
ENERGY_TYPES = ['solar', 'wind', 'hydro', 'biomass']

# Order types
ORDER_TYPES = ['buy', 'sell']

# Transaction statuses
TRANSACTION_STATUSES = ['pending', 'matched', 'completed', 'cancelled']

# Contract statuses
CONTRACT_STATUSES = ['pending', 'active', 'completed', 'failed']

# User roles
USER_ROLES = ['trader', 'admin', 'viewer']

# Asset statuses
ASSET_STATUSES = ['active', 'inactive', 'maintenance']

# Verification statuses
VERIFICATION_STATUSES = ['unverified', 'verified', 'failed']

# API rate limits
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 100  # requests per window

# Performance targets
TARGET_TRANSACTION_EFFICIENCY = 35  # % improvement
TARGET_VERIFICATION_REDUCTION = 60  # % reduction
TARGET_WEEKLY_TRANSACTIONS = 1200  # minimum weekly volume
TARGET_SUCCESS_RATE = 99.9  # % success rate
TARGET_UPTIME = 99.9  # % uptime

# Price ranges (USD per kWh)
PRICE_RANGES = {
    'solar': {'min': 0.05, 'max': 0.25},
    'wind': {'min': 0.04, 'max': 0.20},
    'hydro': {'min': 0.03, 'max': 0.15},
    'biomass': {'min': 0.08, 'max': 0.30}
}

# Blockchain configuration
BLOCKCHAIN_MINING_DIFFICULTY = 2
BLOCKCHAIN_MINING_REWARD = 0.001  # ETH
BLOCKCHAIN_GAS_PRICE = 30  # Gwei
BLOCKCHAIN_CONFIRMATIONS_REQUIRED = 12

# Database tables
DATABASE_TABLES = ['transactions', 'users', 'contracts', 'assets']

# Time periods
TIME_PERIODS = ['day', 'week', 'month', 'year']

# Trend types
TREND_TYPES = ['bullish', 'bearish', 'neutral']

# Demand levels
DEMAND_LEVELS = ['low', 'medium', 'high']

# Volatility levels
VOLATILITY_LEVELS = ['low', 'medium', 'high']

# HTTP status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_RATE_LIMIT = 429
HTTP_SERVER_ERROR = 500

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200

# Cache settings
CACHE_TTL = 300  # seconds (5 minutes)
CACHE_MAX_SIZE = 1000  # entries

# File paths
MODEL_DIR = 'ai-models/trained_models'
DATA_DIR = 'ai-models/datasets'
LOG_DIR = 'logs'

# Model versions
PRICE_PREDICTOR_VERSION = 'v1.0'
DEMAND_FORECASTER_VERSION = 'v1.0'
TREND_ANALYZER_VERSION = 'v1.0'
