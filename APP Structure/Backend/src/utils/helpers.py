"""
Helpers
General helper utilities
"""

import uuid
from datetime import datetime, timedelta
from typing import Any


def generate_id() -> str:
    """
    Generate unique ID
    
    Returns:
        str: UUID string
    """
    return str(uuid.uuid4())


def format_currency(amount: float, currency: str = 'USD') -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        str: Formatted currency string
    """
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'ETH': 'Ξ'
    }
    
    symbol = symbols.get(currency, '$')
    return f"{symbol}{amount:,.2f}"


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage
    
    Args:
        part: Part value
        total: Total value
        
    Returns:
        float: Percentage
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change
    """
    if old_value == 0:
        return 0.0
    return round(((new_value - old_value) / old_value) * 100, 2)


def format_timestamp(timestamp: datetime) -> str:
    """
    Format timestamp to ISO string
    """
    return timestamp.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse ISO timestamp string
    """
    return datetime.fromisoformat(timestamp_str)


def get_time_ago(timestamp: datetime) -> str:
    """
    Get human-readable time ago
    
    Returns:
        str: "2 hours ago", "3 days ago", etc.
    """
    now = datetime.utcnow()
    diff = now - timestamp
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours ago"
    else:
        return f"{int(seconds / 86400)} days ago"


def truncate_hash(hash_str: str, length: int = 8) -> str:
    """
    Truncate hash string for display
    
    Args:
        hash_str: Full hash string
        length: Number of characters to keep
        
    Returns:
        str: Truncated hash with ellipsis
    """
    if len(hash_str) <= length:
        return hash_str
    return f"{hash_str[:length]}..."


def round_to_precision(value: float, precision: int = 2) -> float:
    """
    Round value to specified precision
    """
    return round(value, precision)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min and max
    """
    return max(min_value, min(value, max_value))


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Split list into chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide, returning default if denominator is zero
    """
    return numerator / denominator if denominator != 0 else default
