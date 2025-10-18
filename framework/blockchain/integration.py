"""
Blockchain Integration Module for CollegiumAI
Provides integration with Ethereum blockchain for credential management and governance compliance
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from web3 import Web3
from eth_account import Account
import json
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class BlockchainConfig:
    """Blockchain configuration settings"""
    network_url: str
    private_key: str
    contract_addresses: Dict[str, str]
    gas_limit: int = 6000000
    gas_price: int = 20000000000  # 20 gwei
    confirmation_blocks: int = 1

class BlockchainIntegration:
    """
    Main blockchain integration class for CollegiumAI
    Handles credential management and governance compliance on Ethereum
    """
    
    def __init__(self, config: BlockchainConfig):
        self.config = config
        self.w3 = Web3(Web3.HTTPProvider(config.network_url))
        self.account = Account.from_key(config.private_key)
        
        # Load contract ABIs
        self.contracts = {}
        self._load_contracts()
        
        logger.info(f"Blockchain integration initialized for network: {config.network_url}")
    
    def _load_contracts(self):
        """Load smart contract ABIs and create contract instances"""
        try:
            # Load Academic Credentials contract
            credentials_abi = self._load_contract_abi('AcademicCredentials')
            if 'academic_credentials' in self.config.contract_addresses:
                self.contracts['academic_credentials'] = self.w3.eth.contract(
                    address=self.config.contract_addresses['academic_credentials'],
                    abi=credentials_abi
                )
            
            # Load Governance Compliance contract
            governance_abi = self._load_contract_abi('GovernanceCompliance')
            if 'governance_compliance' in self.config.contract_addresses:
                self.contracts['governance_compliance'] = self.w3.eth.contract(
                    address=self.config.contract_addresses['governance_compliance'],
                    abi=governance_abi
                )
            
            logger.info("Smart contracts loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load contracts: {str(e)}")
            raise
    
    def _load_contract_abi(self, contract_name: str) -> List[Dict]:
        """Load contract ABI from compiled artifacts"""
        # In a real implementation, this would load from build artifacts
        # For now, we'll return a simplified ABI structure
        
        if contract_name == 'AcademicCredentials':
            return [
                {
                    "inputs": [
                        {"name": "_student", "type": "address"},
                        {"name": "_studentId", "type": "string"},
                        {"name": "_credentialType", "type": "uint8"},
                        {"name": "_title", "type": "string"},
                        {"name": "_institution", "type": "string"},
                        {"name": "_program", "type": "string"},
                        {"name": "_grade", "type": "string"},
                        {"name": "_credits", "type": "uint256"},
                        {"name": "_completionDate", "type": "uint256"},
                        {"name": "_ipfsHash", "type": "string"},
                        {"name": "_applicableFrameworks", "type": "uint8[]"}
                    ],
                    "name": "issueCredential",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "inputs": [{"name": "_credentialId", "type": "uint256"}],
                    "name": "verifyCredential",
                    "outputs": [
                        {"name": "isValid", "type": "bool"},
                        {"name": "student", "type": "address"},
                        {"name": "title", "type": "string"},
                        {"name": "institution", "type": "string"},
                        {"name": "issueDate", "type": "uint256"},
                        {"name": "isActive", "type": "bool"}
                    ],
                    "type": "function"
                }
            ]
        
        elif contract_name == 'GovernanceCompliance':
            return [
                {
                    "inputs": [
                        {"name": "_framework", "type": "uint8"},
                        {"name": "_institution", "type": "string"},
                        {"name": "_policyType", "type": "uint8"},
                        {"name": "_auditArea", "type": "string"},
                        {"name": "_status", "type": "uint8"},
                        {"name": "_nextReviewDate", "type": "uint256"},
                        {"name": "_findings", "type": "string"},
                        {"name": "_recommendations", "type": "string"},
                        {"name": "_evidenceHash", "type": "string"}
                    ],
                    "name": "createComplianceAudit",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                }
            ]
        
        return []
    
    async def issue_credential(
        self,
        student_address: str,
        student_id: str,
        credential_type: int,
        title: str,
        institution: str,
        program: str,
        grade: str,
        credits: int,
        completion_date: int,
        ipfs_hash: str,
        applicable_frameworks: List[int]
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Issue a new academic credential on the blockchain
        
        Returns:
            Tuple of (success, transaction_hash, credential_data)
        """
        try:
            if 'academic_credentials' not in self.contracts:
                raise ValueError("Academic credentials contract not available")
            
            contract = self.contracts['academic_credentials']
            
            # Build transaction
            function_call = contract.functions.issueCredential(
                student_address,
                student_id,
                credential_type,
                title,
                institution,
                program,
                grade,
                credits,
                completion_date,
                ipfs_hash,
                applicable_frameworks
            )
            
            # Estimate gas
            gas_estimate = function_call.estimateGas({'from': self.account.address})
            
            # Build transaction
            transaction = function_call.buildTransaction({
                'from': self.account.address,
                'gas': min(gas_estimate * 2, self.config.gas_limit),
                'gasPrice': self.config.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.config.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if receipt.status == 1:
                # Parse logs to get credential ID
                credential_id = self._parse_credential_issued_event(receipt.logs)
                
                credential_data = {
                    'credential_id': credential_id,
                    'transaction_hash': tx_hash.hex(),
                    'block_number': receipt.blockNumber,
                    'gas_used': receipt.gasUsed
                }
                
                logger.info(f"Credential issued successfully: {credential_id}")
                return True, tx_hash.hex(), credential_data
            else:
                logger.error("Transaction failed")
                return False, tx_hash.hex(), None
                
        except Exception as e:
            logger.error(f"Failed to issue credential: {str(e)}")
            return False, None, None
    
    async def verify_credential(self, credential_id: int) -> Tuple[bool, Optional[Dict]]:
        """
        Verify a credential on the blockchain
        
        Returns:
            Tuple of (success, credential_data)
        """
        try:
            if 'academic_credentials' not in self.contracts:
                raise ValueError("Academic credentials contract not available")
            
            contract = self.contracts['academic_credentials']
            
            # Call verify function
            result = contract.functions.verifyCredential(credential_id).call()
            
            credential_data = {
                'is_valid': result[0],
                'student_address': result[1],
                'title': result[2],
                'institution': result[3],
                'issue_date': result[4],
                'is_active': result[5],
                'credential_id': credential_id
            }
            
            logger.info(f"Credential {credential_id} verification: {'Valid' if result[0] else 'Invalid'}")
            return True, credential_data
            
        except Exception as e:
            logger.error(f"Failed to verify credential {credential_id}: {str(e)}")
            return False, None
    
    async def get_credential_details(self, credential_id: int) -> Tuple[bool, Optional[Dict]]:
        """
        Get detailed credential information from the blockchain
        """
        try:
            if 'academic_credentials' not in self.contracts:
                raise ValueError("Academic credentials contract not available")
            
            contract = self.contracts['academic_credentials']
            
            # Call getCredentialDetails function
            result = contract.functions.getCredentialDetails(credential_id).call()
            
            credential_details = {
                'id': result[0],
                'student_address': result[1],
                'student_id': result[2],
                'credential_type': result[3],
                'title': result[4],
                'institution': result[5],
                'program': result[6],
                'grade': result[7],
                'credits': result[8],
                'issue_date': result[9],
                'completion_date': result[10],
                'ipfs_hash': result[11]
            }
            
            return True, credential_details
            
        except Exception as e:
            logger.error(f"Failed to get credential details for {credential_id}: {str(e)}")
            return False, None
    
    async def create_compliance_audit(
        self,
        framework: int,
        institution: str,
        policy_type: int,
        audit_area: str,
        status: int,
        next_review_date: int,
        findings: str,
        recommendations: str,
        evidence_hash: str
    ) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Create a new compliance audit on the blockchain
        """
        try:
            if 'governance_compliance' not in self.contracts:
                raise ValueError("Governance compliance contract not available")
            
            contract = self.contracts['governance_compliance']
            
            # Build transaction
            function_call = contract.functions.createComplianceAudit(
                framework,
                institution,
                policy_type,
                audit_area,
                status,
                next_review_date,
                findings,
                recommendations,
                evidence_hash
            )
            
            # Estimate gas
            gas_estimate = function_call.estimateGas({'from': self.account.address})
            
            # Build transaction
            transaction = function_call.buildTransaction({
                'from': self.account.address,
                'gas': min(gas_estimate * 2, self.config.gas_limit),
                'gasPrice': self.config.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.config.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
            
            if receipt.status == 1:
                # Parse logs to get audit ID
                audit_id = self._parse_audit_created_event(receipt.logs)
                
                audit_data = {
                    'audit_id': audit_id,
                    'transaction_hash': tx_hash.hex(),
                    'block_number': receipt.blockNumber,
                    'gas_used': receipt.gasUsed
                }
                
                logger.info(f"Compliance audit created successfully: {audit_id}")
                return True, tx_hash.hex(), audit_data
            else:
                logger.error("Transaction failed")
                return False, tx_hash.hex(), None
                
        except Exception as e:
            logger.error(f"Failed to create compliance audit: {str(e)}")
            return False, None, None
    
    async def get_institution_compliance_status(
        self,
        institution: str,
        framework: int
    ) -> Tuple[bool, Optional[Dict]]:
        """
        Get compliance status for an institution and framework
        """
        try:
            if 'governance_compliance' not in self.contracts:
                raise ValueError("Governance compliance contract not available")
            
            contract = self.contracts['governance_compliance']
            
            result = contract.functions.getInstitutionComplianceStatus(
                institution, framework
            ).call()
            
            compliance_data = {
                'status': result[0],
                'last_audit_date': result[1],
                'next_audit_date': result[2],
                'institution': institution,
                'framework': framework
            }
            
            return True, compliance_data
            
        except Exception as e:
            logger.error(f"Failed to get compliance status: {str(e)}")
            return False, None
    
    async def get_student_credentials(self, student_address: str) -> Tuple[bool, Optional[List[int]]]:
        """
        Get all credentials for a student
        """
        try:
            if 'academic_credentials' not in self.contracts:
                raise ValueError("Academic credentials contract not available")
            
            contract = self.contracts['academic_credentials']
            
            credential_ids = contract.functions.getStudentCredentials(student_address).call()
            
            logger.info(f"Found {len(credential_ids)} credentials for student {student_address}")
            return True, credential_ids
            
        except Exception as e:
            logger.error(f"Failed to get student credentials: {str(e)}")
            return False, None
    
    async def check_framework_compliance(
        self,
        credential_id: int,
        framework: int
    ) -> Tuple[bool, Optional[bool]]:
        """
        Check if a credential complies with a specific governance framework
        """
        try:
            if 'academic_credentials' not in self.contracts:
                raise ValueError("Academic credentials contract not available")
            
            contract = self.contracts['academic_credentials']
            
            is_compliant = contract.functions.checkFrameworkCompliance(
                credential_id, framework
            ).call()
            
            return True, is_compliant
            
        except Exception as e:
            logger.error(f"Failed to check framework compliance: {str(e)}")
            return False, None
    
    def _parse_credential_issued_event(self, logs: List) -> Optional[int]:
        """Parse CredentialIssued event to extract credential ID"""
        try:
            contract = self.contracts['academic_credentials']
            for log in logs:
                if log.address.lower() == contract.address.lower():
                    # In a real implementation, you would decode the log properly
                    # For now, we'll simulate returning a credential ID
                    return 12345  # Mock credential ID
            return None
        except Exception as e:
            logger.error(f"Failed to parse credential issued event: {str(e)}")
            return None
    
    def _parse_audit_created_event(self, logs: List) -> Optional[int]:
        """Parse AuditCreated event to extract audit ID"""
        try:
            contract = self.contracts['governance_compliance']
            for log in logs:
                if log.address.lower() == contract.address.lower():
                    # In a real implementation, you would decode the log properly
                    # For now, we'll simulate returning an audit ID
                    return 67890  # Mock audit ID
            return None
        except Exception as e:
            logger.error(f"Failed to parse audit created event: {str(e)}")
            return None
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get blockchain network status"""
        try:
            latest_block = self.w3.eth.get_block('latest')
            balance = self.w3.eth.get_balance(self.account.address)
            
            return {
                'connected': self.w3.isConnected(),
                'latest_block': latest_block.number,
                'block_timestamp': latest_block.timestamp,
                'account_address': self.account.address,
                'account_balance': Web3.fromWei(balance, 'ether'),
                'network_id': self.w3.eth.chain_id
            }
        except Exception as e:
            logger.error(f"Failed to get network status: {str(e)}")
            return {'connected': False, 'error': str(e)}
    
    def estimate_gas_cost(self, transaction_type: str) -> Dict[str, Any]:
        """Estimate gas cost for different transaction types"""
        gas_estimates = {
            'issue_credential': 150000,
            'verify_credential': 30000,
            'create_audit': 120000,
            'update_compliance': 80000
        }
        
        gas_limit = gas_estimates.get(transaction_type, 100000)
        gas_cost_wei = gas_limit * self.config.gas_price
        gas_cost_eth = Web3.fromWei(gas_cost_wei, 'ether')
        
        return {
            'gas_limit': gas_limit,
            'gas_price_gwei': Web3.fromWei(self.config.gas_price, 'gwei'),
            'estimated_cost_wei': gas_cost_wei,
            'estimated_cost_eth': float(gas_cost_eth)
        }

class CredentialManager:
    """
    High-level credential management interface
    """
    
    def __init__(self, blockchain: BlockchainIntegration):
        self.blockchain = blockchain
    
    async def issue_degree(
        self,
        student_data: Dict[str, Any],
        degree_data: Dict[str, Any],
        governance_frameworks: List[str]
    ) -> Dict[str, Any]:
        """Issue a degree credential"""
        
        # Map governance frameworks to enum values
        framework_mapping = {
            'aacsb': 0,
            'hefce': 1,
            'middle_states': 2,
            'wasc': 3,
            'aacsu': 4,
            'spheir': 5,
            'qaa': 6
        }
        
        framework_ids = [
            framework_mapping[fw.lower()] 
            for fw in governance_frameworks 
            if fw.lower() in framework_mapping
        ]
        
        success, tx_hash, credential_data = await self.blockchain.issue_credential(
            student_address=student_data['blockchain_address'],
            student_id=student_data['student_id'],
            credential_type=0,  # DEGREE
            title=degree_data['title'],
            institution=degree_data['institution'],
            program=degree_data['program'],
            grade=degree_data['grade'],
            credits=degree_data['credits'],
            completion_date=int(degree_data['completion_date'].timestamp()),
            ipfs_hash=degree_data.get('ipfs_hash', ''),
            applicable_frameworks=framework_ids
        )
        
        return {
            'success': success,
            'transaction_hash': tx_hash,
            'credential_data': credential_data,
            'governance_frameworks': governance_frameworks
        }
    
    async def verify_degree(self, credential_id: int) -> Dict[str, Any]:
        """Verify a degree credential"""
        
        success, credential_data = await self.blockchain.verify_credential(credential_id)
        
        if success and credential_data:
            # Get detailed information
            details_success, details = await self.blockchain.get_credential_details(credential_id)
            
            if details_success:
                credential_data.update(details)
        
        return {
            'success': success,
            'credential_data': credential_data,
            'verified_at': datetime.now().isoformat()
        }

class ComplianceManager:
    """
    High-level compliance management interface
    """
    
    def __init__(self, blockchain: BlockchainIntegration):
        self.blockchain = blockchain
    
    async def create_audit(
        self,
        institution: str,
        framework: str,
        audit_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a compliance audit"""
        
        # Map framework to enum value
        framework_mapping = {
            'aacsb': 0,
            'hefce': 1,
            'middle_states': 2,
            'wasc': 3,
            'aacsu': 4,
            'spheir': 5,
            'qaa': 6
        }
        
        framework_id = framework_mapping.get(framework.lower(), 0)
        
        success, tx_hash, audit_result = await self.blockchain.create_compliance_audit(
            framework=framework_id,
            institution=institution,
            policy_type=audit_data.get('policy_type', 0),
            audit_area=audit_data['audit_area'],
            status=audit_data.get('status', 0),  # COMPLIANT
            next_review_date=int(audit_data['next_review_date'].timestamp()),
            findings=audit_data.get('findings', ''),
            recommendations=audit_data.get('recommendations', ''),
            evidence_hash=audit_data.get('evidence_hash', '')
        )
        
        return {
            'success': success,
            'transaction_hash': tx_hash,
            'audit_data': audit_result,
            'framework': framework,
            'institution': institution
        }
    
    async def get_compliance_status(
        self,
        institution: str,
        framework: str
    ) -> Dict[str, Any]:
        """Get compliance status for institution and framework"""
        
        framework_mapping = {
            'aacsb': 0,
            'hefce': 1,
            'middle_states': 2,
            'wasc': 3,
            'aacsu': 4,
            'spheir': 5,
            'qaa': 6
        }
        
        framework_id = framework_mapping.get(framework.lower(), 0)
        
        success, compliance_data = await self.blockchain.get_institution_compliance_status(
            institution, framework_id
        )
        
        if success and compliance_data:
            # Map status enum back to readable format
            status_mapping = {
                0: 'compliant',
                1: 'non_compliant',
                2: 'under_review',
                3: 'pending_review',
                4: 'conditionally_compliant'
            }
            
            compliance_data['status_text'] = status_mapping.get(
                compliance_data['status'], 'unknown'
            )
        
        return {
            'success': success,
            'compliance_data': compliance_data,
            'framework': framework,
            'institution': institution
        }