"""
Smart Contract Routes
Handles smart contract operations
"""

from flask import Blueprint, request, jsonify
import logging

from ...services.blockchain.smart_contract import SmartContractExecutor
from ...services.blockchain.contract_deployer import ContractDeployer
from ...services.blockchain.verification import VerificationService

bp = Blueprint('contracts', __name__)
logger = logging.getLogger(__name__)

# Initialize services
contract_executor = SmartContractExecutor()
contract_deployer = ContractDeployer()
verification_service = VerificationService()

@bp.route('/deploy', methods=['POST'])
def deploy_contract():
    """
    Deploy a new smart contract
    POST /api/contracts/deploy
    Body: {
        "buyer_id": str,
        "seller_id": str,
        "energy_type": str,
        "quantity": float,
        "price": float
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['buyer_id', 'seller_id', 'energy_type', 'quantity', 'price']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Deploy contract
        contract = contract_deployer.deploy(
            buyer_id=data['buyer_id'],
            seller_id=data['seller_id'],
            energy_type=data['energy_type'],
            quantity=data['quantity'],
            price=data['price']
        )
        
        logger.info(f"Contract deployed: {contract['id']}")
        
        return jsonify({
            'success': True,
            'contract': contract,
            'message': 'Contract deployed successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error deploying contract: {str(e)}")
        return jsonify({'error': 'Failed to deploy contract', 'details': str(e)}), 500


@bp.route('/execute', methods=['POST'])
def execute_contract():
    """
    Execute a deployed smart contract
    POST /api/contracts/execute
    Body: {
        "contract_id": str
    }
    """
    try:
        data = request.get_json()
        
        if 'contract_id' not in data:
            return jsonify({'error': 'contract_id is required'}), 400
        
        # Execute contract
        result = contract_executor.execute(data['contract_id'])
        
        logger.info(f"Contract executed: {data['contract_id']}")
        
        return jsonify({
            'success': True,
            'result': result,
            'message': 'Contract executed successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error executing contract: {str(e)}")
        return jsonify({'error': 'Failed to execute contract', 'details': str(e)}), 500


@bp.route('/verify', methods=['POST'])
def verify_contract():
    """
    Verify a contract transaction
    POST /api/contracts/verify
    Body: {
        "contract_id": str,
        "transaction_hash": str
    }
    """
    try:
        data = request.get_json()
        
        if 'contract_id' not in data or 'transaction_hash' not in data:
            return jsonify({'error': 'contract_id and transaction_hash are required'}), 400
        
        # Verify contract
        is_valid = verification_service.verify(
            contract_id=data['contract_id'],
            transaction_hash=data['transaction_hash']
        )
        
        return jsonify({
            'success': True,
            'verified': is_valid,
            'message': 'Verification complete'
        }), 200
        
    except Exception as e:
        logger.error(f"Error verifying contract: {str(e)}")
        return jsonify({'error': 'Failed to verify contract'}), 500


@bp.route('/list', methods=['GET'])
def list_contracts():
    """
    List all smart contracts
    GET /api/contracts/list?status=active|completed|failed
    """
    try:
        status = request.args.get('status', None)
        
        contracts = contract_executor.list_contracts(status)
        
        return jsonify({
            'success': True,
            'contracts': contracts,
            'count': len(contracts)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing contracts: {str(e)}")
        return jsonify({'error': 'Failed to list contracts'}), 500


@bp.route('/<contract_id>', methods=['GET'])
def get_contract(contract_id):
    """
    Get specific contract details
    GET /api/contracts/{contract_id}
    """
    try:
        contract = contract_executor.get_contract(contract_id)
        
        if not contract:
            return jsonify({'error': 'Contract not found'}), 404
        
        return jsonify({
            'success': True,
            'contract': contract
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting contract: {str(e)}")
        return jsonify({'error': 'Failed to get contract'}), 500


@bp.route('/stats', methods=['GET'])
def get_contract_stats():
    """
    Get smart contract statistics
    GET /api/contracts/stats
    """
    try:
        stats = contract_executor.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting contract stats: {str(e)}")
        return jsonify({'error': 'Failed to get statistics'}), 500
