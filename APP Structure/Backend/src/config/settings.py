"""
Settings
Application settings and configuration
"""

import os
from typing import Dict


class Config:
    """
    Base configuration class
    """
    # Application settings
    APP_NAME = 'Green Energy Platform'
    APP_VERSION = '1.0.0'
    DEBUG = False
    TESTING = False
    
    # Secret key for JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_EXPIRATION_HOURS = 24
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///energy_platform.db')
    DATABASE_POOL_SIZE = 10
    DATABASE_MAX_OVERFLOW = 20
    
    # Redis Cache
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TTL = 300  # 5 minutes
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_WINDOW = 60  # seconds
    RATE_LIMIT_MAX_REQUESTS = 100
    
    # Performance Targets
    TARGET_TRANSACTION_EFFICIENCY = 35  # %
    TARGET_VERIFICATION_REDUCTION = 60  # %
    TARGET_WEEKLY_TRANSACTIONS = 1200
    TARGET_SUCCESS_RATE = 99.9  # %
    TARGET_UPTIME = 99.9  # %
    
    # Blockchain
    BLOCKCHAIN_NETWORK = os.getenv('BLOCKCHAIN_NETWORK', 'testnet')
    BLOCKCHAIN_RPC_URL = os.getenv('BLOCKCHAIN_RPC_URL', 'http://localhost:8545')
    BLOCKCHAIN_GAS_PRICE = 30  # Gwei
    BLOCKCHAIN_GAS_LIMIT = 300000
    
    # AI Models
    AI_MODELS_DIR = 'ai-models/trained_models'
    AI_DATASETS_DIR = 'ai-models/datasets'
    AI_MODEL_TRAINING_ENABLED = True
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = 'logs'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # WebSocket
    WEBSOCKET_PING_INTERVAL = 25
    WEBSOCKET_PING_TIMEOUT = 60
    
    # API
    API_PREFIX = '/api'
    API_VERSION = 'v1'
    
    @classmethod
    def get_config(cls) -> Dict:
        """
        Get all configuration as dictionary
        """
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'
    
    # Use SQLite for development
    DATABASE_URL = 'sqlite:///dev_energy_platform.db'
    
    # Disable rate limiting in development
    RATE_LIMIT_ENABLED = False


class TestingConfig(Config):
    """
    Testing configuration
    """
    DEBUG = True
    TESTING = True
    
    # Use in-memory database for testing
    DATABASE_URL = 'sqlite:///:memory:'
    
    # Disable external services
    RATE_LIMIT_ENABLED = False
    AI_MODEL_TRAINING_ENABLED = False


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    TESTING = False
    
    # Production database (PostgreSQL)
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/energy_platform')
    
    # Strict security
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    if not SECRET_KEY or not JWT_SECRET_KEY:
        raise ValueError("SECRET_KEY and JWT_SECRET_KEY must be set in production")
    
    # Production rate limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_MAX_REQUESTS = 1000
    
    # Production blockchain
    BLOCKCHAIN_NETWORK = 'mainnet'
    BLOCKCHAIN_RPC_URL = os.getenv('BLOCKCHAIN_RPC_URL')
    
    # Production logging
    LOG_LEVEL = 'WARNING'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: str = None) -> Config:
    """
    Get configuration for environment
    
    Args:
        env: Environment name (development, testing, production)
        
    Returns:
        Config class
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])
