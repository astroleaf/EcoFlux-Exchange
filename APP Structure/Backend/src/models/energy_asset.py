"""
Energy Asset Model
Represents an energy production or consumption asset
"""

from datetime import datetime
import uuid


class EnergyAsset:
    """
    Energy asset model (solar panel, wind turbine, etc.)
    """
    
    def __init__(self, owner_id, asset_type, capacity, location,
                 asset_id=None, status='active', created_at=None):
        """
        Initialize an energy asset
        
        Args:
            owner_id: ID of the asset owner
            asset_type: Type of asset (solar, wind, hydro, biomass)
            capacity: Production capacity in kWh
            location: Geographic location
            asset_id: Unique asset ID (generated if not provided)
            status: Asset status (active, inactive, maintenance)
            created_at: Creation timestamp
        """
        self.id = asset_id or str(uuid.uuid4())
        self.owner_id = owner_id
        self.asset_type = asset_type
        self.capacity = capacity
        self.location = location
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.last_maintenance = None
        self.total_production = 0.0
        self.current_production = 0.0
        self.efficiency = 95.0  # Percentage
        self.age_months = 0
        
    def to_dict(self):
        """
        Convert asset to dictionary
        """
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'asset_type': self.asset_type,
            'capacity': self.capacity,
            'location': self.location,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_maintenance': self.last_maintenance.isoformat() if self.last_maintenance else None,
            'total_production': self.total_production,
            'current_production': self.current_production,
            'efficiency': self.efficiency,
            'age_months': self.age_months
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create asset from dictionary
        """
        asset = cls(
            owner_id=data['owner_id'],
            asset_type=data['asset_type'],
            capacity=data['capacity'],
            location=data['location'],
            asset_id=data.get('id'),
            status=data.get('status', 'active')
        )
        
        if 'created_at' in data:
            asset.created_at = datetime.fromisoformat(data['created_at'])
        if 'last_maintenance' in data and data['last_maintenance']:
            asset.last_maintenance = datetime.fromisoformat(data['last_maintenance'])
        if 'total_production' in data:
            asset.total_production = data['total_production']
        if 'current_production' in data:
            asset.current_production = data['current_production']
        if 'efficiency' in data:
            asset.efficiency = data['efficiency']
        if 'age_months' in data:
            asset.age_months = data['age_months']
            
        return asset
    
    def update_production(self, amount):
        """
        Update production metrics
        """
        self.current_production = amount
        self.total_production += amount
    
    def perform_maintenance(self):
        """
        Record maintenance activity
        """
        self.last_maintenance = datetime.utcnow()
        self.status = 'active'
        # Restore efficiency
        self.efficiency = min(95.0, self.efficiency + 5.0)
    
    def degrade_efficiency(self):
        """
        Simulate natural efficiency degradation
        """
        # Efficiency degrades ~0.5% per year
        degradation = 0.5 / 12  # Monthly degradation
        self.efficiency = max(70.0, self.efficiency - degradation)
    
    def calculate_expected_production(self, hours=24):
        """
        Calculate expected production over time period
        """
        base_production = self.capacity * hours
        adjusted_production = base_production * (self.efficiency / 100)
        return round(adjusted_production, 2)
    
    def is_operational(self):
        """
        Check if asset is operational
        """
        return self.status == 'active' and self.efficiency >= 70.0
    
    def __repr__(self):
        return f"<EnergyAsset {self.id} - {self.asset_type} {self.capacity}kWh capacity>"
