"""
Validators
Input validation utilities
"""

from typing import Any, List


def validate_energy_type(energy_type: str) -> bool:
    """
    Validate energy type
    
    Args:
        energy_type: Energy type to validate
        
    Returns:
        bool: True if valid
    """
    valid_types = ['solar', 'wind', 'hydro', 'biomass']
    return energy_type in valid_types


def validate_price(price: float) -> bool:
    """
    Validate price
    
    Args:
        price: Price to validate
        
    Returns:
        bool: True if valid
    """
    return isinstance(price, (int, float)) and price > 0


def validate_quantity(quantity: float) -> bool:
    """
    Validate quantity
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        bool: True if valid
    """
    return isinstance(quantity, (int, float)) and quantity > 0


def validate_order_type(order_type: str) -> bool:
    """
    Validate order type
    """
    return order_type in ['buy', 'sell']


def validate_email(email: str) -> bool:
    """
    Validate email format
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format
    """
    return isinstance(user_id, str) and len(user_id) > 0


def validate_contract_status(status: str) -> bool:
    """
    Validate contract status
    """
    valid_statuses = ['pending', 'active', 'completed', 'failed']
    return status in valid_statuses


def validate_transaction_status(status: str) -> bool:
    """
    Validate transaction status
    """
    valid_statuses = ['pending', 'matched', 'completed', 'cancelled']
    return status in valid_statuses


def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate date range
    """
    from datetime import datetime
    
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        return start <= end
    except (ValueError, TypeError):
        return False


def validate_required_fields(data: dict, required_fields: List[str]) -> tuple:
    """
    Validate required fields in data
    
    Returns:
        tuple: (is_valid, missing_fields)
    """
    missing = [field for field in required_fields if field not in data]
    return len(missing) == 0, missing
