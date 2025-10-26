"""
Unit Tests for Smart Contracts
Tests contract execution, deployment, and verification
"""

import pytest
from src.services.blockchain.smart_contract import SmartContractExecutor
from src.services.blockchain.contract_deployer import ContractDeployer
from src.services.blockchain.verification import VerificationService
from src.models.smart_contract import SmartContract


class TestSmartContract:
    """Test Smart Contract model"""
    
    def test_contract_creation(self):
        """Test creating a smart contract"""
        contract = SmartContract(
            buyer_id='user-1',
            seller_id='user-2',
            energy_type='solar',
            quantity=100.0,
            price=0.12
        )
        
        assert contract.id is not None
        assert contract.buyer_id == 'user-1'
        assert contract.seller_id == 'user-2'
        assert contract.total_value == 12.0
        assert contract.status == 'pending'
    
    def test_contract_hash_generation(self):
        """Test transaction hash generation"""
        contract = SmartContract(
            buyer_id='user-1',
            seller_id='user-2',
            energy_type='wind',
            quantity=150.0,
            price=0.10
        )
        
        assert contract.transaction_hash is not None
        assert len(contract.transaction_hash) == 64  # SHA-256 hash length
    
    def test_contract_deployment(self):
        """Test contract deployment"""
        contract = SmartContract(
            buyer_id='user-1',
            seller_id='user-2',
            energy_type='hydro',
            quantity=200.0,
            price=0.08
        )
        
        hash_value = contract.deploy()
        
        assert contract.status == 'active'
        assert contract.deployed_at is not None
        assert hash_value == contract.transaction_hash
    
    def test_contract_execution(self):
        """Test contract execution"""
        contract = SmartContract(
            buyer_id='user-1',
            seller_id='user-2',
            energy_type='biomass',
            quantity=80.0,
            price=0.15
        )
        
        contract.deploy()
        success = contract.execute(execution_time=2.3)
        
        assert success is True
        assert contract.status == 'completed'
        assert contract.executed_at is not None
        assert contract.gas_used > 0


class TestContractDeployer:
    """Test Contract Deployer"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.deployer = ContractDeployer()
    
    def test_deploy_contract(self):
        """Test deploying a contract"""
        contract_data = self.deployer.deploy(
            buyer_id='user-1',
            seller_id='user-2',
            energy_type='solar',
            quantity=100.0,
            price=0.12
        )
        
        assert contract_data is not None
        assert 'id' in contract_data
        assert 'transaction_hash' in contract_data
        assert contract_data['status'] == 'active'
    
    def test_gas_estimation(self):
        """Test gas cost estimation"""
        estimate = self.deployer.estimate_gas(quantity=100.0, price=0.12)
        
        assert 'estimated_gas' in estimate
        assert 'gas_price_gwei' in estimate
        assert 'estimated_cost_eth' in estimate
        assert estimate['estimated_gas'] > 0


class TestVerificationService:
    """Test Verification Service"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.verification = VerificationService()
    
    def test_verify_valid_contract(self):
        """Test verifying a valid contract"""
        contract_id = 'test-contract-1'
        
        # Generate a valid hash
        import hashlib
        transaction_hash = hashlib.sha256(contract_id.encode()).hexdigest()
        
        is_valid = self.verification.verify(contract_id, transaction_hash)
        
        assert is_valid is True
    
    def test_verification_status(self):
        """Test getting verification status"""
        contract_id = 'test-contract-2'
        transaction_hash = 'abc123'
        
        self.verification.verify(contract_id, transaction_hash)
        status = self.verification.get_verification_status(contract_id)
        
        assert status is not None
        assert 'contract_id' in status
        assert 'verified' in status
        assert 'status' in status
    
    def test_verification_statistics(self):
        """Test verification statistics"""
        stats = self.verification.get_verification_statistics()
        
        assert 'total_verifications' in stats
        assert 'successful' in stats
        assert 'average_verification_time' in stats
        assert 'time_reduction_percentage' in stats
