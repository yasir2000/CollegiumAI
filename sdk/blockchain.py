"""
Blockchain Client for CollegiumAI SDK
Handles blockchain operations, credentials, and smart contracts
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum

class BlockchainNetwork(Enum):
    """Supported blockchain networks"""
    ETHEREUM_MAINNET = "ethereum_mainnet"
    ETHEREUM_GOERLI = "ethereum_goerli"
    ETHEREUM_SEPOLIA = "ethereum_sepolia"
    POLYGON = "polygon"
    POLYGON_MUMBAI = "polygon_mumbai"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BSC = "bsc"
    BSC_TESTNET = "bsc_testnet"
    LOCAL = "local"

class CredentialType(Enum):
    """Types of digital credentials"""
    DEGREE = "degree"
    CERTIFICATE = "certificate"
    DIPLOMA = "diploma"
    TRANSCRIPT = "transcript"
    BADGE = "badge"
    CERTIFICATION = "certification"
    LICENSE = "license"
    SKILL_VERIFICATION = "skill_verification"
    ATTENDANCE = "attendance"
    ACHIEVEMENT = "achievement"

class ContractType(Enum):
    """Smart contract types"""
    CREDENTIAL_REGISTRY = "credential_registry"
    GOVERNANCE = "governance"
    IDENTITY = "identity"
    VERIFICATION = "verification"
    MULTI_SIGNATURE = "multi_signature"
    CUSTOM = "custom"

class BlockchainClient:
    """Client for blockchain operations and digital credentials"""
    
    def __init__(self, client):
        self.client = client
    
    # Network and Connection Management
    async def get_network_status(
        self,
        network: Union[str, BlockchainNetwork] = None
    ) -> Dict[str, Any]:
        """Get blockchain network status"""
        params = {}
        if network:
            if isinstance(network, BlockchainNetwork):
                network = network.value
            params['network'] = network
        
        return await self.client.get('/blockchain/network/status', params=params)
    
    async def get_supported_networks(self) -> List[Dict[str, Any]]:
        """Get list of supported blockchain networks"""
        return await self.client.get('/blockchain/networks')
    
    async def switch_network(self, network: Union[str, BlockchainNetwork]) -> Dict[str, Any]:
        """Switch to a different blockchain network"""
        if isinstance(network, BlockchainNetwork):
            network = network.value
        
        return await self.client.post('/blockchain/network/switch', data={'network': network})
    
    async def get_gas_prices(
        self,
        network: Union[str, BlockchainNetwork] = None
    ) -> Dict[str, Any]:
        """Get current gas prices for transactions"""
        params = {}
        if network:
            if isinstance(network, BlockchainNetwork):
                network = network.value
            params['network'] = network
        
        return await self.client.get('/blockchain/gas-prices', params=params)
    
    # Credential Management
    async def create_credential(
        self,
        credential_data: Dict[str, Any],
        credential_type: Union[str, CredentialType],
        recipient_address: str,
        issuer_data: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a new digital credential on blockchain
        
        Args:
            credential_data: Core credential information
            credential_type: Type of credential being issued
            recipient_address: Blockchain address of recipient
            issuer_data: Information about the issuing institution
            metadata: Additional metadata for the credential
            
        Returns:
            Transaction details and credential ID
        """
        if isinstance(credential_type, CredentialType):
            credential_type = credential_type.value
        
        creation_data = {
            'credential_data': credential_data,
            'credential_type': credential_type,
            'recipient_address': recipient_address,
            'issuer_data': issuer_data or {},
            'metadata': metadata or {}
        }
        
        return await self.client.post('/blockchain/credentials', data=creation_data)
    
    async def get_credential(self, credential_id: str) -> Dict[str, Any]:
        """Get credential details from blockchain"""
        return await self.client.get(f'/blockchain/credentials/{credential_id}')
    
    async def verify_credential(
        self,
        credential_id: str,
        verify_signature: bool = True,
        verify_issuer: bool = True
    ) -> Dict[str, Any]:
        """
        Verify a digital credential
        
        Args:
            credential_id: Credential ID to verify
            verify_signature: Verify cryptographic signature
            verify_issuer: Verify issuer authenticity
            
        Returns:
            Verification results and status
        """
        verification_data = {
            'verify_signature': verify_signature,
            'verify_issuer': verify_issuer
        }
        
        return await self.client.post(
            f'/blockchain/credentials/{credential_id}/verify',
            data=verification_data
        )
    
    async def revoke_credential(
        self,
        credential_id: str,
        reason: str,
        revocation_date: datetime = None
    ) -> Dict[str, Any]:
        """Revoke a digital credential"""
        revocation_data = {
            'reason': reason,
            'revocation_date': (revocation_date or datetime.now()).isoformat()
        }
        
        return await self.client.post(
            f'/blockchain/credentials/{credential_id}/revoke',
            data=revocation_data
        )
    
    async def get_user_credentials(
        self,
        user_address: str,
        credential_type: Union[str, CredentialType] = None,
        issuer_address: str = None,
        active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Get all credentials for a user"""
        params = {
            'user_address': user_address,
            'active_only': active_only
        }
        
        if credential_type:
            if isinstance(credential_type, CredentialType):
                credential_type = credential_type.value
            params['credential_type'] = credential_type
        
        if issuer_address:
            params['issuer_address'] = issuer_address
        
        return await self.client.get('/blockchain/credentials/user', params=params)
    
    async def get_issued_credentials(
        self,
        issuer_address: str,
        credential_type: Union[str, CredentialType] = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[Dict[str, Any]]:
        """Get credentials issued by an institution"""
        params = {'issuer_address': issuer_address}
        
        if credential_type:
            if isinstance(credential_type, CredentialType):
                credential_type = credential_type.value
            params['credential_type'] = credential_type
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        return await self.client.get('/blockchain/credentials/issued', params=params)
    
    # Advanced Credential Features
    async def create_multi_signature_credential(
        self,
        credential_data: Dict[str, Any],
        required_signatures: int,
        signers: List[str],
        recipient_address: str
    ) -> Dict[str, Any]:
        """Create a credential requiring multiple signatures"""
        multisig_data = {
            'credential_data': credential_data,
            'required_signatures': required_signatures,
            'signers': signers,
            'recipient_address': recipient_address
        }
        
        return await self.client.post('/blockchain/credentials/multisig', data=multisig_data)
    
    async def sign_multisig_credential(
        self,
        credential_id: str,
        signature: str,
        signer_address: str
    ) -> Dict[str, Any]:
        """Add signature to a multi-signature credential"""
        signature_data = {
            'signature': signature,
            'signer_address': signer_address
        }
        
        return await self.client.post(
            f'/blockchain/credentials/multisig/{credential_id}/sign',
            data=signature_data
        )
    
    async def batch_issue_credentials(
        self,
        credentials: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Issue multiple credentials in a single transaction"""
        return await self.client.post('/blockchain/credentials/batch', data={'credentials': credentials})
    
    # Fraud Detection and Security
    async def detect_credential_fraud(
        self,
        credential_id: str,
        analysis_type: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """
        Run fraud detection analysis on a credential
        
        Args:
            credential_id: Credential to analyze
            analysis_type: Type of analysis (basic, comprehensive, deep)
            
        Returns:
            Fraud detection results and risk score
        """
        analysis_data = {
            'analysis_type': analysis_type
        }
        
        return await self.client.post(
            f'/blockchain/credentials/{credential_id}/fraud-detection',
            data=analysis_data
        )
    
    async def get_fraud_patterns(
        self,
        time_period: str = '30d',
        pattern_type: str = None
    ) -> Dict[str, Any]:
        """Get detected fraud patterns"""
        params = {'time_period': time_period}
        
        if pattern_type:
            params['pattern_type'] = pattern_type
        
        return await self.client.get('/blockchain/fraud-patterns', params=params)
    
    async def report_suspicious_activity(
        self,
        credential_id: str,
        report_type: str,
        description: str,
        evidence: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Report suspicious credential activity"""
        report_data = {
            'credential_id': credential_id,
            'report_type': report_type,
            'description': description,
            'evidence': evidence or {}
        }
        
        return await self.client.post('/blockchain/fraud/report', data=report_data)
    
    # IPFS Document Storage
    async def upload_document(
        self,
        file_data: bytes,
        filename: str,
        content_type: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Upload document to IPFS
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            content_type: MIME type of the file
            metadata: Additional metadata
            
        Returns:
            IPFS hash and upload details
        """
        upload_data = {
            'filename': filename,
            'content_type': content_type,
            'metadata': metadata or {}
        }
        
        # Note: In actual implementation, file_data would be handled differently
        # This is a simplified version for the SDK interface
        return await self.client.post('/blockchain/ipfs/upload', data=upload_data)
    
    async def get_document(self, ipfs_hash: str) -> Dict[str, Any]:
        """Retrieve document from IPFS"""
        return await self.client.get(f'/blockchain/ipfs/{ipfs_hash}')
    
    async def pin_document(self, ipfs_hash: str) -> Dict[str, Any]:
        """Pin document to prevent garbage collection"""
        return await self.client.post(f'/blockchain/ipfs/{ipfs_hash}/pin')
    
    async def unpin_document(self, ipfs_hash: str) -> Dict[str, Any]:
        """Unpin document from IPFS"""
        return await self.client.delete(f'/blockchain/ipfs/{ipfs_hash}/pin')
    
    async def get_document_metadata(self, ipfs_hash: str) -> Dict[str, Any]:
        """Get metadata for an IPFS document"""
        return await self.client.get(f'/blockchain/ipfs/{ipfs_hash}/metadata')
    
    # Smart Contract Management
    async def deploy_contract(
        self,
        contract_type: Union[str, ContractType],
        contract_code: str = None,
        constructor_args: List[Any] = None,
        network: Union[str, BlockchainNetwork] = None
    ) -> Dict[str, Any]:
        """Deploy a smart contract"""
        if isinstance(contract_type, ContractType):
            contract_type = contract_type.value
        if isinstance(network, BlockchainNetwork):
            network = network.value
        
        deployment_data = {
            'contract_type': contract_type,
            'contract_code': contract_code,
            'constructor_args': constructor_args or [],
            'network': network
        }
        
        return await self.client.post('/blockchain/contracts/deploy', data=deployment_data)
    
    async def get_contract(self, contract_address: str) -> Dict[str, Any]:
        """Get smart contract information"""
        return await self.client.get(f'/blockchain/contracts/{contract_address}')
    
    async def call_contract_method(
        self,
        contract_address: str,
        method_name: str,
        args: List[Any] = None,
        gas_limit: int = None
    ) -> Dict[str, Any]:
        """Call a smart contract method"""
        call_data = {
            'method_name': method_name,
            'args': args or [],
            'gas_limit': gas_limit
        }
        
        return await self.client.post(
            f'/blockchain/contracts/{contract_address}/call',
            data=call_data
        )
    
    async def upgrade_contract(
        self,
        contract_address: str,
        new_implementation: str,
        upgrade_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Upgrade a smart contract (proxy pattern)"""
        upgrade_request = {
            'new_implementation': new_implementation,
            'upgrade_data': upgrade_data or {}
        }
        
        return await self.client.post(
            f'/blockchain/contracts/{contract_address}/upgrade',
            data=upgrade_request
        )
    
    # Governance and Voting
    async def create_governance_proposal(
        self,
        title: str,
        description: str,
        proposal_type: str,
        voting_period: int,
        execution_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a governance proposal"""
        proposal_data = {
            'title': title,
            'description': description,
            'proposal_type': proposal_type,
            'voting_period': voting_period,
            'execution_data': execution_data or {}
        }
        
        return await self.client.post('/blockchain/governance/proposals', data=proposal_data)
    
    async def vote_on_proposal(
        self,
        proposal_id: str,
        vote: str,
        reason: str = None
    ) -> Dict[str, Any]:
        """Vote on a governance proposal"""
        vote_data = {
            'vote': vote,
            'reason': reason
        }
        
        return await self.client.post(
            f'/blockchain/governance/proposals/{proposal_id}/vote',
            data=vote_data
        )
    
    async def get_governance_proposals(
        self,
        status: str = None,
        proposal_type: str = None
    ) -> List[Dict[str, Any]]:
        """Get governance proposals"""
        params = {}
        
        if status:
            params['status'] = status
        if proposal_type:
            params['type'] = proposal_type
        
        return await self.client.get('/blockchain/governance/proposals', params=params)
    
    async def execute_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """Execute a passed governance proposal"""
        return await self.client.post(f'/blockchain/governance/proposals/{proposal_id}/execute')
    
    # Transaction Management
    async def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction details"""
        return await self.client.get(f'/blockchain/transactions/{tx_hash}')
    
    async def get_transaction_receipt(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction receipt"""
        return await self.client.get(f'/blockchain/transactions/{tx_hash}/receipt')
    
    async def estimate_gas(
        self,
        transaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Estimate gas for a transaction"""
        return await self.client.post('/blockchain/transactions/estimate-gas', data=transaction_data)
    
    async def get_pending_transactions(self, address: str = None) -> List[Dict[str, Any]]:
        """Get pending transactions"""
        params = {}
        if address:
            params['address'] = address
        
        return await self.client.get('/blockchain/transactions/pending', params=params)
    
    # Analytics and Reporting
    async def get_blockchain_analytics(
        self,
        time_period: str = '30d',
        metric_type: str = 'credentials'
    ) -> Dict[str, Any]:
        """Get blockchain analytics"""
        params = {
            'time_period': time_period,
            'metric_type': metric_type
        }
        
        return await self.client.get('/blockchain/analytics', params=params)
    
    async def get_credential_statistics(
        self,
        issuer_address: str = None,
        credential_type: Union[str, CredentialType] = None
    ) -> Dict[str, Any]:
        """Get credential issuance statistics"""
        params = {}
        
        if issuer_address:
            params['issuer_address'] = issuer_address
        if credential_type:
            if isinstance(credential_type, CredentialType):
                credential_type = credential_type.value
            params['credential_type'] = credential_type
        
        return await self.client.get('/blockchain/analytics/credentials', params=params)
    
    async def get_verification_metrics(
        self,
        time_period: str = '30d'
    ) -> Dict[str, Any]:
        """Get credential verification metrics"""
        params = {'time_period': time_period}
        
        return await self.client.get('/blockchain/analytics/verifications', params=params)
    
    # Identity and Authentication
    async def create_digital_identity(
        self,
        identity_data: Dict[str, Any],
        public_key: str
    ) -> Dict[str, Any]:
        """Create a digital identity on blockchain"""
        identity_creation = {
            'identity_data': identity_data,
            'public_key': public_key
        }
        
        return await self.client.post('/blockchain/identity/create', data=identity_creation)
    
    async def verify_identity(
        self,
        identity_id: str,
        challenge: str = None
    ) -> Dict[str, Any]:
        """Verify a digital identity"""
        verification_data = {}
        if challenge:
            verification_data['challenge'] = challenge
        
        return await self.client.post(
            f'/blockchain/identity/{identity_id}/verify',
            data=verification_data
        )
    
    async def update_identity(
        self,
        identity_id: str,
        updates: Dict[str, Any],
        signature: str
    ) -> Dict[str, Any]:
        """Update digital identity information"""
        update_data = {
            'updates': updates,
            'signature': signature
        }
        
        return await self.client.put(
            f'/blockchain/identity/{identity_id}',
            data=update_data
        )
    
    # Utility Methods
    async def get_wallet_balance(
        self,
        address: str,
        token_address: str = None
    ) -> Dict[str, Any]:
        """Get wallet balance for native token or specific ERC-20"""
        params = {'address': address}
        
        if token_address:
            params['token_address'] = token_address
        
        return await self.client.get('/blockchain/wallet/balance', params=params)
    
    async def get_supported_tokens(self) -> List[Dict[str, Any]]:
        """Get list of supported tokens"""
        return await self.client.get('/blockchain/tokens')
    
    async def validate_address(
        self,
        address: str,
        network: Union[str, BlockchainNetwork] = None
    ) -> Dict[str, Any]:
        """Validate blockchain address format"""
        validation_data = {'address': address}
        
        if network:
            if isinstance(network, BlockchainNetwork):
                network = network.value
            validation_data['network'] = network
        
        return await self.client.post('/blockchain/validate-address', data=validation_data)