"""
Blockchain Simulator
Simulates blockchain network for development and testing
"""

import logging
import hashlib
from datetime import datetime
from typing import List, Dict
import time

logger = logging.getLogger(__name__)


class Block:
    """
    Represents a block in the blockchain
    """
    
    def __init__(self, index: int, timestamp: datetime, transactions: List[Dict],
                 previous_hash: str):
        """
        Initialize a block
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate block hash
        """
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """
        Mine the block (Proof of Work)
        """
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        logger.info(f"Block mined: {self.hash}")
    
    def to_dict(self):
        """
        Convert block to dictionary
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp.isoformat(),
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce
        }


class BlockchainSimulator:
    """
    Simulates a blockchain network
    """
    
    def __init__(self):
        """
        Initialize blockchain
        """
        self.chain = []
        self.pending_transactions = []
        self.mining_difficulty = 2
        self.mining_reward = 0.001  # ETH
        
        # Create genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """
        Create the first block in the chain
        """
        genesis_block = Block(0, datetime.utcnow(), [], "0")
        genesis_block.mine_block(self.mining_difficulty)
        self.chain.append(genesis_block)
        logger.info("Genesis block created")
    
    def get_latest_block(self):
        """
        Get the latest block in the chain
        """
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict):
        """
        Add a transaction to pending transactions
        """
        self.pending_transactions.append(transaction)
        logger.info(f"Transaction added to pool: {transaction.get('id', 'unknown')}")
    
    def mine_pending_transactions(self, miner_address: str):
        """
        Mine all pending transactions
        """
        if not self.pending_transactions:
            logger.warning("No transactions to mine")
            return None
        
        # Create new block
        block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        start_time = time.time()
        block.mine_block(self.mining_difficulty)
        mining_time = time.time() - start_time
        
        # Add to chain
        self.chain.append(block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        # Add mining reward transaction
        self.pending_transactions.append({
            'from': 'system',
            'to': miner_address,
            'amount': self.mining_reward,
            'type': 'mining_reward'
        })
        
        logger.info(f"Block mined in {mining_time:.3f}s - {len(block.transactions)} transactions")
        
        return block.to_dict()
    
    def is_chain_valid(self):
        """
        Verify the blockchain integrity
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                logger.error(f"Invalid hash at block {i}")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"Invalid previous hash at block {i}")
                return False
        
        return True
    
    def get_blockchain_info(self):
        """
        Get blockchain information
        """
        return {
            'chain_length': len(self.chain),
            'pending_transactions': len(self.pending_transactions),
            'mining_difficulty': self.mining_difficulty,
            'mining_reward': self.mining_reward,
            'is_valid': self.is_chain_valid(),
            'latest_block': self.get_latest_block().to_dict()
        }
    
    def get_transaction_count(self):
        """
        Get total transaction count across all blocks
        """
        total = sum(len(block.transactions) for block in self.chain)
        return total
    
    def get_block_by_index(self, index: int):
        """
        Get block by index
        """
        if 0 <= index < len(self.chain):
            return self.chain[index].to_dict()
        return None
    
    def get_block_by_hash(self, block_hash: str):
        """
        Get block by hash
        """
        for block in self.chain:
            if block.hash == block_hash:
                return block.to_dict()
        return None
