"""
Smart Contract Executor
Executes smart contracts for energy trading
"""

import logging
from datetime import datetime
import time

from ...models.smart_contract import SmartContract

logger = logging.getLogger(__name__)


class SmartContractExecutor:
    """
    Executes and manages smart contracts
    """
    
    def __init__(self):
        """
        Initialize contract executor
        """
        self.contracts = []  # In-memory storage (use DB in production)
        
    def execute(self, contract_id: str):
        """
        Execute a smart contract
        
        Args:
            contract_id: ID of contract to execute
            
        Returns:
            Execution result
        """
        contract = self.get_contract(contract_id)
        
        if not contract:
            logger.error(f"Contract not found: {contract_id}")
            raise ValueError(f"Contract not found: {contract_id}")
        
        if contract.status != 'active':
            logger.error(f"Contract not in active state: {contract_id}")
            raise ValueError(f"Contract cannot be executed. Status: {contract.status}")
        
        # Simulate contract execution
        start_time = time.time()
        
        try:
            # Simulate blockchain transaction processing
            time.sleep(0.1)  # Simulate network delay
            
            execution_time = time.time() - start_time
            
            # Execute contract
            contract.execute(execution_time)
            
            logger.info(f"Contract executed successfully: {contract_id} in {execution_time:.3f}s")
            
            return {
                'success': True,
                'contract_id': contract_id,
                'transaction_hash': contract.transaction_hash,
                'execution_time': execution_time,
                'gas_used': contract.gas_used,
                'status': contract.status
            }
            
        except Exception as e:
            logger.error(f"Contract execution failed: {contract_id} - {str(e)}")
            contract.fail(str(e))
            
            return {
                'success': False,
                'contract_id': contract_id,
                'error': str(e)
            }
    
    def get_contract(self, contract_id: str):
        """
        Get contract by ID
        """
        for contract in self.contracts:
            if contract.id == contract_id:
                return contract
        return None
    
    def list_contracts(self, status: str = None):
        """
        List all contracts with optional status filter
        """
        if status:
            filtered = [c for c in self.contracts if c.status == status]
        else:
            filtered = self.contracts
        
        return [c.to_dict() for c in filtered]
    
    def get_statistics(self):
        """
        Get contract execution statistics
        """
        total = len(self.contracts)
        active = len([c for c in self.contracts if c.status == 'active'])
        completed = len([c for c in self.contracts if c.status == 'completed'])
        failed = len([c for c in self.contracts if c.status == 'failed'])
        
        # Calculate average execution time
        execution_times = [c.execution_time for c in self.contracts if c.execution_time]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Success rate
        success_rate = (completed / total * 100) if total > 0 else 100
        
        return {
            'total_contracts': total,
            'active': active,
            'completed': completed,
            'failed': failed,
            'success_rate': round(success_rate, 2),
            'average_execution_time': round(avg_execution_time, 3)
        }
    
    def add_contract(self, contract: SmartContract):
        """
        Add a contract to the executor
        """
        self.contracts.append(contract)
        logger.info(f"Contract added: {contract.id}")
