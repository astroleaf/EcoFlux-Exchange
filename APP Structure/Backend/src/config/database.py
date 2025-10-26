"""
Database Configuration
Database-specific configuration and utilities
"""

import os


class DatabaseConfig:
    """
    Database configuration
    """
    
    # Connection settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///energy_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
    
    # Pool settings
    SQLALCHEMY_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', '10'))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('DATABASE_POOL_TIMEOUT', '30'))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('DATABASE_POOL_RECYCLE', '3600'))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', '20'))
    
    # Migration settings
    MIGRATION_DIR = 'backend/src/database/migrations'
    
    # Backup settings
    BACKUP_ENABLED = True
    BACKUP_DIR = 'backups/database'
    BACKUP_RETENTION_DAYS = 30
    
    @classmethod
    def get_connection_string(cls) -> str:
        """
        Get database connection string
        """
        return cls.SQLALCHEMY_DATABASE_URI
    
    @classmethod
    def is_postgres(cls) -> bool:
        """
        Check if using PostgreSQL
        """
        return cls.SQLALCHEMY_DATABASE_URI.startswith('postgresql')
    
    @classmethod
    def is_sqlite(cls) -> bool:
        """
        Check if using SQLite
        """
        return cls.SQLALCHEMY_DATABASE_URI.startswith('sqlite')
    
    @classmethod
    def get_config(cls) -> dict:
        """
        Get database configuration dictionary
        """
        return {
            'database_uri': cls.SQLALCHEMY_DATABASE_URI,
            'pool_size': cls.SQLALCHEMY_POOL_SIZE,
            'pool_timeout': cls.SQLALCHEMY_POOL_TIMEOUT,
            'pool_recycle': cls.SQLALCHEMY_POOL_RECYCLE,
            'max_overflow': cls.SQLALCHEMY_MAX_OVERFLOW,
            'echo': cls.SQLALCHEMY_ECHO
        }
