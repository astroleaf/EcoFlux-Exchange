"""
Smart Contract Model
Represents a blockchain smart contract
"""

from datetime import datetime
import uuid
import hashlib
import json


class SmartContract:
    """
    Smart contract model for energy trading
    """
    
    def __init__(self, buyer_id, seller_id, energy_type, quantity, price,
                 contract_id=None, status='pending', created_at=None):
        """
        Initialize a smart contract
        
        Args:
            buyer_id: ID of the buyer
            seller_id: ID of the seller
            energy_type: Type of energy being traded
            quantity: Amount of energy in kWh
            price: Price per kWh
            contract_id: Unique contract ID (generated if not provided)
            status: Contract status (pending, active, completed, failed)
            created_at: Creation timestamp
        """
        self.id = contract_id or str(uuid.uuid4())
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.energy_type = energy_type
        self.quantity = quantity
        self.price = price
        self.total_value = quantity * price
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.deployed_at = None
        self.executed_at = None
        self.transaction_hash = self._generate_hash()
        self.verification_status = 'unverified'
        self.execution_time = None
        self.gas_used = 0
        
    def _generate_hash(self):
        """
        Generate blockchain-style transaction hash
        """
        data = f"{self.buyer_id}{self.seller_id}{self.energy_type}{self.quantity}{self.price}{self.created_at}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self):
        """
        Convert contract to dictionary
        """
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'energy_type': self.energy_type,
            'quantity': self.quantity,
            'price': self.price,
            'total_value': self.total_value,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'deployed_at': self.deployed_at.isoformat() if self.deployed_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'transaction_hash': self.transaction_hash,
            'verification_status': self.verification_status,
            'execution_time': self.execution_time,
            'gas_used': self.gas_used
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create contract from dictionary
        """
        contract = cls(
            buyer_id=data['buyer_id'],
            seller_id=data['seller_id'],
            energy_type=data['energy_type'],
            quantity=data['quantity'],
            price=data['price'],
            contract_id=data.get('id'),
            status=data.get('status', 'pending')
        )
        
        if 'created_at' in data:
            contract.created_at = datetime.fromisoformat(data['created_at'])
        if 'deployed_at' in data and data['deployed_at']:
            contract.deployed_at = datetime.fromisoformat(data['deployed_at'])
        if 'executed_at' in data and data['executed_at']:
            contract.executed_at = datetime.fromisoformat(data['executed_at'])
        if 'transaction_hash' in data:
            contract.transaction_hash = data['transaction_hash']
        if 'verification_status' in data:
            contract.verification_status = data['verification_status']
        if 'execution_time' in data:
            contract.execution_time = data['execution_time']
        if 'gas_used' in data:
            contract.gas_used = data['gas_used']
            
        return contract
    
    def deploy(self):
        """
        Mark contract as deployed
        """
        self.status = 'active'
        self.deployed_at = datetime.utcnow()
        return self.transaction_hash
    
    def execute(self, execution_time):
        """
        Execute the contract
        """
        self.status = 'completed'
        self.executed_at = datetime.utcnow()
        self.execution_time = execution_time
        # Simulate gas usage (0.001 to 0.005 ETH equivalent)
        import random
        self.gas_used = round(random.uniform(0.001, 0.005), 6)
        return True
    
    def verify(self):
        """
        Verify the contract
        """
        if self.status == 'completed':
            self.verification_status = 'verified'
            return True
        return False
    
    def fail(self, reason='Unknown error'):
        """
        Mark contract as failed
        """
        self.status = 'failed'
        self.failure_reason = reason
        return False
    
    def get_contract_code(self):
        """
        Generate Solidity-like contract code representation
        """
        return f"""
        contract EnergyTrade_{self.id[:8]} {{
            address public buyer = {self.buyer_id};
            address public seller = {self.seller_id};
            string public energyType = "{self.energy_type}";
            uint256 public quantity = {self.quantity};
            uint256 public pricePerUnit = {self.price};
            uint256 public totalValue = {self.total_value};
            
            function execute() public returns (bool) {{
                // Transfer energy tokens from seller to buyer
                // Transfer payment from buyer to seller
                return true;
            }}
        }}
        """
    
    def __repr__(self):
        return f"<SmartContract {self.id} - {self.energy_type} {self.quantity}kWh @ ${self.price}>"
