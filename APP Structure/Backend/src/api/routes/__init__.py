"""
Routes Package
Exports all route blueprints
"""

from . import trades
from . import analytics
from . import contracts
from . import predictions

__all__ = ['trades', 'analytics', 'contracts', 'predictions']
