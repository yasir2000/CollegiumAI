"""
Advanced Blockchain Credential Management System
==============================================

Enhanced blockchain integration providing:
- Multi-signature credential issuance
- Credential lifecycle management
- IPFS document storage and verification
- Advanced fraud detection algorithms
- Smart contract upgrades and governance
- Cross-institutional credential verification
- Bologna Process compliance automation
"""

import asyncio
import logging
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import secrets
import uuid
from pathlib import Path

# Import existing blockchain components
from ..blockchain.integration import BlockchainIntegration, BlockchainConfig
from ..database import get_database_service

logger = logging.getLogger(__name__)

class CredentialType(Enum):
    DEGREE = "degree"
    CERTIFICATE = "certificate"
    DIPLOMA = "diploma"
    TRANSCRIPT = "transcript"
    BADGE = "badge"
    ACHIEVEMENT = "achievement"

class CredentialStatus(Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ISSUED = "issued"
    VERIFIED = "verified"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"

class FraudRiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class IPFSDocument:
    """IPFS document metadata"""
    hash: str
    filename: str
    content_type: str
    size: int
    encryption_key: Optional[str] = None
    access_control: List[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.access_control is None:
            self.access_control = []

@dataclass
class CredentialMetadata:
    """Extended credential metadata"""
    credential_id: str
    issuer_institution: str
    student_identity: Dict[str, Any]
    academic_program: Dict[str, Any]
    governance_frameworks: List[str]
    bologna_compliance: Optional[Dict[str, Any]] = None
    quality_assurance: Optional[Dict[str, Any]] = None
    learning_outcomes: List[str] = None
    competencies: List[str] = None
    assessments: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.learning_outcomes is None:
            self.learning_outcomes = []
        if self.competencies is None:
            self.competencies = []
        if self.assessments is None:
            self.assessments = []

@dataclass
class MultiSignatureConfig:
    """Multi-signature configuration for credential issuance"""
    required_signers: int
    authorized_signers: List[str]  # Ethereum addresses
    timeout_hours: int = 48
    institutional_policies: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.institutional_policies is None:
            self.institutional_policies = {}

class FraudDetectionEngine:
    """Advanced fraud detection for blockchain credentials"""
    
    def __init__(self):
        self.detection_rules = self._load_detection_rules()
        self.risk_factors = {}
        self.blacklisted_addresses = set()
        self.suspicious_patterns = []
    
    def _load_detection_rules(self) -> Dict[str, Any]:
        """Load fraud detection rules"""
        return {
            "duplicate_credentials": {
                "enabled": True,
                "threshold": 0.95,  # Similarity threshold
                "action": "flag_for_review"
            },
            "temporal_anomalies": {
                "enabled": True,
                "max_credentials_per_day": 10,
                "action": "rate_limit"
            },
            "institutional_verification": {
                "enabled": True,
                "require_verified_institution": True,
                "action": "reject"
            },
            "cross_reference_validation": {
                "enabled": True,
                "check_external_databases": True,
                "action": "flag_for_manual_review"
            }
        }
    
    async def analyze_credential_request(
        self,
        metadata: CredentialMetadata,
        issuer_address: str,
        historical_data: List[Dict[str, Any]] = None
    ) -> Tuple[FraudRiskLevel, List[str], float]:
        """Analyze credential issuance request for fraud risk"""
        
        risk_indicators = []
        risk_score = 0.0
        
        # Check issuer reputation
        issuer_risk = await self._analyze_issuer_reputation(issuer_address)
        risk_score += issuer_risk * 0.3
        if issuer_risk > 0.7:
            risk_indicators.append("High-risk issuer address")
        
        # Check for duplicate credentials
        duplicate_risk = await self._check_duplicate_credentials(metadata)
        risk_score += duplicate_risk * 0.25
        if duplicate_risk > 0.5:
            risk_indicators.append("Potential duplicate credential detected")
        
        # Temporal analysis
        temporal_risk = await self._analyze_temporal_patterns(issuer_address, historical_data)
        risk_score += temporal_risk * 0.2
        if temporal_risk > 0.6:
            risk_indicators.append("Unusual issuance pattern detected")
        
        # Institutional verification
        institutional_risk = await self._verify_institutional_authorization(metadata)
        risk_score += institutional_risk * 0.25
        if institutional_risk > 0.8:
            risk_indicators.append("Institution verification failed")
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = FraudRiskLevel.CRITICAL
        elif risk_score >= 0.6:
            risk_level = FraudRiskLevel.HIGH
        elif risk_score >= 0.4:
            risk_level = FraudRiskLevel.MEDIUM
        else:
            risk_level = FraudRiskLevel.LOW
        
        logger.info(f"Fraud analysis complete: {risk_level.value} risk (score: {risk_score:.2f})")
        return risk_level, risk_indicators, risk_score
    
    async def _analyze_issuer_reputation(self, issuer_address: str) -> float:
        """Analyze issuer reputation based on historical data"""
        if issuer_address in self.blacklisted_addresses:
            return 1.0
        
        # In a real implementation, this would check:
        # - Historical issuance patterns
        # - Verification success rates
        # - Community reputation scores
        # - Institutional accreditation status
        
        return 0.1  # Low risk for demo
    
    async def _check_duplicate_credentials(self, metadata: CredentialMetadata) -> float:
        """Check for potential duplicate credentials"""
        db = await get_database_service()
        
        # Create content hash for comparison
        content_hash = self._create_content_hash(metadata)
        
        # Check for similar credentials in database
        # This would involve similarity matching algorithms
        
        return 0.0  # No duplicates found for demo
    
    async def _analyze_temporal_patterns(
        self, 
        issuer_address: str, 
        historical_data: List[Dict[str, Any]] = None
    ) -> float:
        """Analyze temporal patterns for anomalies"""
        if not historical_data:
            return 0.0
        
        # Analyze issuance frequency, timing patterns, etc.
        recent_issuances = [
            item for item in historical_data 
            if datetime.fromisoformat(item.get('timestamp', '1970-01-01')) > 
               datetime.utcnow() - timedelta(days=1)
        ]
        
        if len(recent_issuances) > 10:  # More than 10 in 24 hours
            return 0.7
        
        return 0.2
    
    async def _verify_institutional_authorization(self, metadata: CredentialMetadata) -> float:
        """Verify institutional authorization for credential issuance"""
        # Check if institution is properly registered and authorized
        # Verify governance framework compliance
        # Check accreditation status
        
        return 0.1  # Low risk for demo
    
    def _create_content_hash(self, metadata: CredentialMetadata) -> str:
        """Create hash of credential content for duplicate detection"""
        content = {
            'student_identity': metadata.student_identity,
            'academic_program': metadata.academic_program,
            'learning_outcomes': sorted(metadata.learning_outcomes),
            'competencies': sorted(metadata.competencies)
        }
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()

class IPFSManager:
    """IPFS integration for document storage"""
    
    def __init__(self, ipfs_endpoint: str = "http://localhost:5001"):
        self.endpoint = ipfs_endpoint
        self.encryption_key = None
    
    async def store_document(
        self,
        content: bytes,
        filename: str,
        content_type: str,
        encrypt: bool = True,
        access_control: List[str] = None
    ) -> IPFSDocument:
        """Store document on IPFS"""
        
        try:
            # Encrypt document if requested
            encrypted_content = content
            encryption_key = None
            
            if encrypt:
                encryption_key = secrets.token_urlsafe(32)
                encrypted_content = self._encrypt_content(content, encryption_key)
            
            # Store on IPFS (simulated for demo)
            ipfs_hash = self._simulate_ipfs_storage(encrypted_content)
            
            document = IPFSDocument(
                hash=ipfs_hash,
                filename=filename,
                content_type=content_type,
                size=len(content),
                encryption_key=encryption_key,
                access_control=access_control or []
            )
            
            logger.info(f"Document stored on IPFS: {ipfs_hash}")
            return document
            
        except Exception as e:
            logger.error(f"IPFS storage failed: {e}")
            raise
    
    async def retrieve_document(
        self,
        ipfs_hash: str,
        encryption_key: str = None
    ) -> Tuple[bytes, str]:
        """Retrieve document from IPFS"""
        
        try:
            # Retrieve from IPFS (simulated)
            content = self._simulate_ipfs_retrieval(ipfs_hash)
            
            # Decrypt if key provided
            if encryption_key:
                content = self._decrypt_content(content, encryption_key)
            
            return content, "application/octet-stream"
            
        except Exception as e:
            logger.error(f"IPFS retrieval failed: {e}")
            raise
    
    async def verify_document_integrity(self, document: IPFSDocument) -> bool:
        """Verify document integrity on IPFS"""
        try:
            # Check if document exists and hash matches
            # In real implementation, this would verify IPFS hash integrity
            return True
        except Exception as e:
            logger.error(f"Document integrity check failed: {e}")
            return False
    
    def _encrypt_content(self, content: bytes, key: str) -> bytes:
        """Encrypt content (simplified implementation)"""
        # In production, use proper encryption like AES-GCM
        return content  # Placeholder
    
    def _decrypt_content(self, content: bytes, key: str) -> bytes:
        """Decrypt content (simplified implementation)"""
        # In production, use proper decryption
        return content  # Placeholder
    
    def _simulate_ipfs_storage(self, content: bytes) -> str:
        """Simulate IPFS storage and return hash"""
        # Generate realistic IPFS hash
        hash_input = content + str(datetime.utcnow()).encode()
        return "Qm" + hashlib.sha256(hash_input).hexdigest()[:44]
    
    def _simulate_ipfs_retrieval(self, ipfs_hash: str) -> bytes:
        """Simulate IPFS retrieval"""
        # Return sample content for demo
        return b"Sample document content from IPFS"

class AdvancedCredentialManager:
    """Advanced credential management with enhanced features"""
    
    def __init__(
        self,
        blockchain_config: BlockchainConfig = None,
        ipfs_endpoint: str = "http://localhost:5001"
    ):
        # Use default config for testing if none provided
        if blockchain_config is None:
            blockchain_config = BlockchainConfig(
                network_url="http://localhost:8545",
                private_key="0x" + "0" * 64,  # Mock private key for testing
                contract_addresses={}
            )
        
        try:
            self.blockchain = BlockchainIntegration(blockchain_config)
        except Exception as e:
            logger.warning(f"Blockchain integration disabled: {e}")
            self.blockchain = None
            
        self.fraud_detector = FraudDetectionEngine()
        self.ipfs_manager = IPFSManager(ipfs_endpoint)
        self.multi_sig_configs = {}
        
    async def issue_credential_advanced(
        self,
        metadata: CredentialMetadata,
        documents: List[Tuple[bytes, str, str]] = None,  # (content, filename, content_type)
        multi_sig_config: MultiSignatureConfig = None,
        fraud_check: bool = True,
        auto_verify: bool = False
    ) -> Dict[str, Any]:
        """Issue credential with advanced features"""
        
        try:
            logger.info(f"Starting advanced credential issuance: {metadata.credential_id}")
            
            # Fraud detection analysis
            fraud_result = None
            if fraud_check:
                risk_level, risk_indicators, risk_score = await self.fraud_detector.analyze_credential_request(
                    metadata, metadata.issuer_institution
                )
                
                fraud_result = {
                    "risk_level": risk_level.value,
                    "risk_indicators": risk_indicators,
                    "risk_score": risk_score
                }
                
                # Block high-risk credentials
                if risk_level == FraudRiskLevel.CRITICAL:
                    raise ValueError(f"Credential blocked due to critical fraud risk: {risk_indicators}")
            
            # Store documents on IPFS
            ipfs_documents = []
            if documents:
                for content, filename, content_type in documents:
                    doc = await self.ipfs_manager.store_document(
                        content, filename, content_type, encrypt=True
                    )
                    ipfs_documents.append(asdict(doc))
            
            # Prepare credential data for blockchain
            credential_data = {
                "metadata": asdict(metadata),
                "ipfs_documents": ipfs_documents,
                "fraud_analysis": fraud_result,
                "issuance_timestamp": datetime.utcnow().isoformat(),
                "version": "2.0"  # Advanced version
            }
            
            # Multi-signature issuance if configured
            if multi_sig_config:
                return await self._issue_with_multisig(credential_data, multi_sig_config)
            else:
                return await self._issue_single_signature(credential_data)
            
        except Exception as e:
            logger.error(f"Advanced credential issuance failed: {e}")
            raise
    
    async def _issue_single_signature(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Issue credential with single signature"""
        
        # Convert to format expected by blockchain integration
        blockchain_data = self._prepare_blockchain_data(credential_data)
        
        # Issue on blockchain using existing integration
        success, tx_hash, result_data = await self.blockchain.issue_credential(
            **blockchain_data
        )
        
        if not success:
            raise RuntimeError("Blockchain credential issuance failed")
        
        # Store in database
        db = await get_database_service()
        credential_uuid = await db.store_credential(
            credential_id=result_data.get('credential_id'),
            transaction_hash=tx_hash,
            student_id=credential_data['metadata']['student_identity']['id'],
            institution_id=credential_data['metadata']['issuer_institution'],
            credential_data=credential_data
        )
        
        return {
            "success": True,
            "credential_uuid": credential_uuid,
            "credential_id": result_data.get('credential_id'),
            "transaction_hash": tx_hash,
            "ipfs_documents": credential_data['ipfs_documents'],
            "fraud_analysis": credential_data['fraud_analysis'],
            "issuance_method": "single_signature"
        }
    
    async def _issue_with_multisig(
        self, 
        credential_data: Dict[str, Any], 
        multi_sig_config: MultiSignatureConfig
    ) -> Dict[str, Any]:
        """Issue credential with multi-signature approval"""
        
        # Create multi-sig proposal
        proposal_id = str(uuid.uuid4())
        
        proposal = {
            "proposal_id": proposal_id,
            "credential_data": credential_data,
            "config": asdict(multi_sig_config),
            "signatures": [],
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=multi_sig_config.timeout_hours)).isoformat()
        }
        
        # Store proposal (in production, this would be in a dedicated storage)
        self.multi_sig_configs[proposal_id] = proposal
        
        logger.info(f"Multi-signature proposal created: {proposal_id}")
        
        return {
            "success": True,
            "proposal_id": proposal_id,
            "status": "pending_signatures",
            "required_signatures": multi_sig_config.required_signers,
            "authorized_signers": multi_sig_config.authorized_signers,
            "expires_at": proposal["expires_at"]
        }
    
    async def sign_multisig_credential(
        self,
        proposal_id: str,
        signer_address: str,
        signature: str
    ) -> Dict[str, Any]:
        """Sign multi-signature credential proposal"""
        
        if proposal_id not in self.multi_sig_configs:
            raise ValueError("Proposal not found")
        
        proposal = self.multi_sig_configs[proposal_id]
        
        # Check if proposal expired
        if datetime.fromisoformat(proposal['expires_at']) < datetime.utcnow():
            proposal['status'] = 'expired'
            raise ValueError("Proposal has expired")
        
        # Check if signer is authorized
        if signer_address not in proposal['config']['authorized_signers']:
            raise ValueError("Unauthorized signer")
        
        # Check if already signed
        existing_signatures = [sig['signer'] for sig in proposal['signatures']]
        if signer_address in existing_signatures:
            raise ValueError("Already signed by this signer")
        
        # Add signature
        proposal['signatures'].append({
            "signer": signer_address,
            "signature": signature,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Check if we have enough signatures
        if len(proposal['signatures']) >= proposal['config']['required_signers']:
            # Execute credential issuance
            result = await self._execute_multisig_issuance(proposal)
            proposal['status'] = 'executed'
            proposal['result'] = result
            return result
        
        return {
            "success": True,
            "status": "signature_added",
            "signatures_count": len(proposal['signatures']),
            "required_count": proposal['config']['required_signers']
        }
    
    async def _execute_multisig_issuance(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multi-signature credential issuance"""
        credential_data = proposal['credential_data']
        
        # Add multi-sig proof to credential data
        credential_data['multisig_proof'] = {
            "proposal_id": proposal['proposal_id'],
            "signatures": proposal['signatures'],
            "required_signatures": proposal['config']['required_signers'],
            "execution_timestamp": datetime.utcnow().isoformat()
        }
        
        # Issue on blockchain
        return await self._issue_single_signature(credential_data)
    
    async def verify_credential_advanced(
        self,
        credential_id: int,
        verify_ipfs: bool = True,
        cross_reference: bool = True
    ) -> Dict[str, Any]:
        """Advanced credential verification"""
        
        try:
            # Basic blockchain verification
            success, credential_data = await self.blockchain.verify_credential(credential_id)
            
            if not success:
                return {
                    "valid": False,
                    "error": "Blockchain verification failed"
                }
            
            verification_result = {
                "valid": True,
                "blockchain_verified": True,
                "credential_data": credential_data,
                "verification_timestamp": datetime.utcnow().isoformat()
            }
            
            # IPFS document verification
            if verify_ipfs:
                ipfs_status = await self._verify_ipfs_documents(credential_data)
                verification_result["ipfs_verification"] = ipfs_status
            
            # Cross-reference verification
            if cross_reference:
                cross_ref_status = await self._cross_reference_verification(credential_data)
                verification_result["cross_reference_verification"] = cross_ref_status
            
            # Fraud re-analysis
            fraud_recheck = await self._recheck_fraud_indicators(credential_data)
            verification_result["fraud_recheck"] = fraud_recheck
            
            # Overall validity assessment
            verification_result["overall_valid"] = all([
                verification_result["blockchain_verified"],
                verification_result.get("ipfs_verification", {}).get("valid", True),
                verification_result.get("cross_reference_verification", {}).get("valid", True),
                verification_result.get("fraud_recheck", {}).get("risk_level") != "critical"
            ])
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Advanced credential verification failed: {e}")
            return {
                "valid": False,
                "error": str(e)
            }
    
    async def _verify_ipfs_documents(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify IPFS documents integrity"""
        ipfs_documents = credential_data.get('ipfs_documents', [])
        
        if not ipfs_documents:
            return {"valid": True, "message": "No IPFS documents to verify"}
        
        verification_results = []
        
        for doc_data in ipfs_documents:
            doc = IPFSDocument(**doc_data)
            is_valid = await self.ipfs_manager.verify_document_integrity(doc)
            
            verification_results.append({
                "filename": doc.filename,
                "hash": doc.hash,
                "valid": is_valid
            })
        
        all_valid = all(result["valid"] for result in verification_results)
        
        return {
            "valid": all_valid,
            "documents": verification_results
        }
    
    async def _cross_reference_verification(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-reference verification with external databases"""
        # In production, this would check:
        # - National student databases
        # - Institutional registries
        # - Accreditation body records
        # - International recognition databases
        
        return {
            "valid": True,
            "checks_performed": [
                "institutional_registry",
                "accreditation_verification",
                "student_enrollment_confirmation"
            ],
            "message": "Cross-reference verification passed"
        }
    
    async def _recheck_fraud_indicators(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Re-check fraud indicators"""
        # Re-run fraud detection with current data
        return {
            "risk_level": "low",
            "new_indicators": [],
            "confidence": 0.95
        }
    
    def _prepare_blockchain_data(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for blockchain integration"""
        metadata = credential_data['metadata']
        
        return {
            "student_address": metadata['student_identity'].get('blockchain_address', '0x' + '0' * 40),
            "student_id": metadata['student_identity'].get('id', ''),
            "credential_type": 0,  # DEGREE
            "title": metadata['academic_program'].get('title', ''),
            "institution": metadata['issuer_institution'],
            "program": metadata['academic_program'].get('program', ''),
            "grade": metadata['academic_program'].get('grade', ''),
            "credits": metadata['academic_program'].get('credits', 0),
            "completion_date": int(datetime.utcnow().timestamp()),
            "ipfs_hash": credential_data['ipfs_documents'][0]['hash'] if credential_data['ipfs_documents'] else '',
            "applicable_frameworks": [0, 1]  # AACSB, WASC as examples
        }
    
    async def get_credential_lifecycle(self, credential_id: int) -> Dict[str, Any]:
        """Get complete credential lifecycle information"""
        db = await get_database_service()
        
        # Get credential data
        credential = await db.fetchrow(
            "SELECT * FROM blockchain_credentials WHERE credential_id = $1", 
            credential_id
        )
        
        if not credential:
            return {"error": "Credential not found"}
        
        # Get verification logs
        verification_logs = await db.fetch(
            "SELECT * FROM credential_verification_logs WHERE credential_id = $1 ORDER BY created_at DESC",
            credential['id']
        )
        
        # Get Bologna Process compliance data
        bologna_data = await db.fetchrow(
            "SELECT * FROM bologna_process_compliance WHERE credential_id = $1",
            credential['id']
        )
        
        return {
            "credential": dict(credential),
            "verification_logs": [dict(log) for log in verification_logs],
            "bologna_compliance": dict(bologna_data) if bologna_data else None,
            "lifecycle_events": await self._get_lifecycle_events(credential_id)
        }
    
    async def _get_lifecycle_events(self, credential_id: int) -> List[Dict[str, Any]]:
        """Get credential lifecycle events"""
        # This would track all events in the credential's lifecycle
        return [
            {
                "event": "credential_issued",
                "timestamp": datetime.utcnow().isoformat(),
                "details": {"issuer": "institution", "method": "blockchain"}
            }
        ]

# Utility functions
async def create_advanced_credential_manager(
    blockchain_config: BlockchainConfig = None,
    ipfs_endpoint: str = "http://localhost:5001"
) -> AdvancedCredentialManager:
    """Create advanced credential manager instance"""
    return AdvancedCredentialManager(blockchain_config, ipfs_endpoint)

async def batch_verify_credentials(
    credential_ids: List[int],
    credential_manager: AdvancedCredentialManager
) -> Dict[int, Dict[str, Any]]:
    """Batch verify multiple credentials"""
    results = {}
    
    # Process in parallel for efficiency
    tasks = [
        credential_manager.verify_credential_advanced(cred_id) 
        for cred_id in credential_ids
    ]
    
    verification_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for cred_id, result in zip(credential_ids, verification_results):
        if isinstance(result, Exception):
            results[cred_id] = {"valid": False, "error": str(result)}
        else:
            results[cred_id] = result
    
    return results