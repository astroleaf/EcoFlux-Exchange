"""
Logger
Logging configuration and utilities
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = 'green_energy_platform', 
                level: int = logging.INFO,
                log_to_file: bool = True):
    """
    Setup application logger
    
    Args:
        name: Logger name
        level: Logging level
        log_to_file: Whether to log to file
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance
    """
    return logging.getLogger(name)


def log_performance(logger: logging.Logger, operation: str, duration: float):
    """
    Log performance metric
    
    Args:
        logger: Logger instance
        operation: Operation name
        duration: Duration in seconds
    """
    logger.info(f"Performance: {operation} completed in {duration:.3f}s")


def log_error_with_context(logger: logging.Logger, error: Exception, context: dict):
    """
    Log error with context information
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Context dictionary
    """
    logger.error(f"Error: {str(error)}")
    logger.error(f"Context: {context}")
    
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")


def log_api_request(logger: logging.Logger, method: str, endpoint: str, 
                   status_code: int, duration: float):
    """
    Log API request
    """
    logger.info(f"API: {method} {endpoint} - {status_code} ({duration:.3f}s)")


def log_transaction(logger: logging.Logger, transaction_id: str, 
                   action: str, status: str):
    """
    Log transaction event
    """
    logger.info(f"Transaction [{transaction_id}]: {action} - {status}")


def log_contract(logger: logging.Logger, contract_id: str, 
                action: str, status: str):
    """
    Log contract event
    """
    logger.info(f"Contract [{contract_id}]: {action} - {status}")
