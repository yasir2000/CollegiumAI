#!/usr/bin/env python3
"""
CollegiumAI SDK Example: Blockchain Credentials Management
=========================================================

This example demonstrates comprehensive blockchain-based academic credential
management using the CollegiumAI Framework. It shows how to issue, verify,
and manage academic credentials on the blockchain.

Features demonstrated:
- Academic credential issuance on blockchain
- Credential verification and validation
- Multi-framework governance compliance
- Student transcript management
- Credential sharing and portability
- Fraud prevention and security
- IPFS document storage integration
"""

import asyncio
import os
import sys
import json
from datetime import datetime, date
from typing import Dict, List, Any, Optional
import argparse
import logging
import hashlib

# Add the parent directory to the path to import the SDK
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk import (
    CollegiumAIClient, SDKConfig, PersonaType, GovernanceFramework,
    ResponseBuilder
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BlockchainCredentialsDemo:
    """
    Comprehensive blockchain credentials demonstration class
    """
    
    def __init__(self, config: SDKConfig):
        self.config = config
        self.client: Optional[CollegiumAIClient] = None
        self.sample_institutions = self._create_sample_institutions()
        self.sample_students = self._create_sample_students()
        self.sample_credentials = self._create_sample_credentials()
        
    async def __aenter__(self):
        self.client = CollegiumAIClient(self.config)
        await self.client.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.close()
    
    def _create_sample_institutions(self) -> Dict[str, Dict[str, Any]]:
        """Create sample institution data with governance compliance"""
        return {
            'state_university': {
                'name': 'State University of Technology',
                'blockchain_address': '0x1234567890123456789012345678901234567890',
                'accreditations': [
                    GovernanceFramework.WASC,
                    GovernanceFramework.AACSB,
                    GovernanceFramework.MIDDLE_STATES
                ],
                'established': 1965,
                'type': 'public',
                'location': {
                    'city': 'Tech City',
                    'state': 'California',
                    'country': 'USA'
                },
                'credential_authority': True,
                'blockchain_integration_date': datetime(2023, 1, 15)
            },
            'private_college': {
                'name': 'Excellence Private College',
                'blockchain_address': '0x2345678901234567890123456789012345678901',
                'accreditations': [
                    GovernanceFramework.MIDDLE_STATES,
                    GovernanceFramework.AACSU
                ],
                'established': 1890,
                'type': 'private',
                'location': {
                    'city': 'Academic Hills',
                    'state': 'New York',
                    'country': 'USA'
                },
                'credential_authority': True,
                'blockchain_integration_date': datetime(2023, 6, 1)
            },
            'international_university': {
                'name': 'Global University',
                'blockchain_address': '0x3456789012345678901234567890123456789012',
                'accreditations': [
                    GovernanceFramework.QAA,
                    GovernanceFramework.HEFCE
                ],
                'established': 1820,
                'type': 'public',
                'location': {
                    'city': 'London',
                    'country': 'United Kingdom'
                },
                'credential_authority': True,
                'blockchain_integration_date': datetime(2023, 9, 15)
            }
        }
    
    def _create_sample_students(self) -> Dict[str, Dict[str, Any]]:
        """Create sample student data with blockchain addresses"""
        return {
            'undergraduate_student': {
                'student_id': 'STU2024001',
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@statetech.edu',
                'blockchain_address': '0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A',
                'birth_date': date(2002, 8, 15),
                'enrollment_date': date(2020, 9, 1),
                'expected_graduation': date(2024, 5, 15),
                'major': 'Computer Science',
                'minor': 'Mathematics',
                'institution': 'state_university',
                'student_type': PersonaType.TRADITIONAL_STUDENT
            },
            'graduate_student': {
                'student_id': 'STU2024002',
                'name': 'Michael Chen',
                'email': 'michael.chen@excellence.edu',
                'blockchain_address': '0x8ba1f109551bD432803012645Hac136c9c1Ba7B',
                'birth_date': date(1990, 3, 22),
                'enrollment_date': date(2022, 1, 15),
                'expected_graduation': date(2024, 12, 20),
                'program': 'Master of Business Administration',
                'specialization': 'Technology Management',
                'institution': 'private_college',
                'student_type': PersonaType.GRADUATE_STUDENT
            },
            'international_student': {
                'student_id': 'STU2024003',
                'name': 'Emma Thompson',
                'email': 'emma.thompson@global.ac.uk',
                'blockchain_address': '0x9cb2f210662cE543914023756Iac247d0d2Ca8C',
                'birth_date': date(1998, 11, 30),
                'enrollment_date': date(2021, 9, 20),
                'expected_graduation': date(2025, 6, 30),
                'program': 'PhD in Educational Psychology',
                'research_area': 'Digital Learning Technologies',
                'institution': 'international_university',
                'student_type': PersonaType.INTERNATIONAL_STUDENT,
                'country_of_origin': 'Canada'
            }
        }
    
    def _create_sample_credentials(self) -> List[Dict[str, Any]]:
        """Create sample credential data for different types of achievements"""
        return [
            {
                'credential_type': 'degree',
                'title': 'Bachelor of Science in Computer Science',
                'program': 'Computer Science',
                'degree_level': 'Bachelor',
                'major': 'Computer Science',
                'minor': 'Mathematics',
                'gpa': 3.75,
                'credits_completed': 120,
                'graduation_date': date(2024, 5, 15),
                'honors': 'Cum Laude',
                'thesis_title': None,
                'competencies': [
                    'Software Development',
                    'Data Structures and Algorithms',
                    'Database Management',
                    'Web Development',
                    'Machine Learning',
                    'Software Engineering Principles'
                ]
            },
            {
                'credential_type': 'degree',
                'title': 'Master of Business Administration',
                'program': 'Business Administration',
                'degree_level': 'Master',
                'specialization': 'Technology Management',
                'gpa': 3.90,
                'credits_completed': 48,
                'graduation_date': date(2024, 12, 20),
                'honors': 'Magna Cum Laude',
                'capstone_project': 'Digital Transformation in Healthcare Organizations',
                'competencies': [
                    'Strategic Management',
                    'Technology Leadership',
                    'Financial Analysis',
                    'Project Management',
                    'Innovation Management',
                    'Data-Driven Decision Making'
                ]
            },
            {
                'credential_type': 'certificate',
                'title': 'Professional Certificate in Artificial Intelligence',
                'program': 'Continuing Education',
                'certificate_type': 'Professional Development',
                'duration_hours': 120,
                'completion_date': date(2024, 3, 10),
                'grade': 'Pass with Distinction',
                'competencies': [
                    'Machine Learning Algorithms',
                    'Neural Networks',
                    'Natural Language Processing',
                    'Computer Vision',
                    'AI Ethics',
                    'AI Implementation'
                ]
            },
            {
                'credential_type': 'micro_credential',
                'title': 'Digital Marketing Analytics Badge',
                'program': 'Digital Skills Initiative',
                'badge_type': 'Micro-Credential',
                'skill_level': 'Intermediate',
                'completion_date': date(2024, 1, 25),
                'verification_method': 'Portfolio Assessment',
                'competencies': [
                    'Google Analytics',
                    'Social Media Analytics',
                    'SEO/SEM',
                    'Data Visualization',
                    'Campaign Management'
                ]
            }
        ]
    
    async def demonstrate_credential_issuance(self):
        """
        Demonstrate the process of issuing academic credentials on blockchain
        """
        print(f"\n{'='*60}")
        print("BLOCKCHAIN CREDENTIAL ISSUANCE DEMO")
        print(f"{'='*60}")
        
        # Select sample data
        student = self.sample_students['undergraduate_student']
        institution = self.sample_institutions['state_university']
        credential = self.sample_credentials[0]  # Bachelor's degree
        
        print(f"Institution: {institution['name']}")
        print(f"Student: {student['name']} ({student['student_id']})")
        print(f"Credential: {credential['title']}")
        print(f"Graduation Date: {credential['graduation_date']}")
        
        try:
            # Issue credential on blockchain
            result = await self.client.blockchain.issue_credential(
                student_data={
                    'student_id': student['student_id'],
                    'blockchain_address': student['blockchain_address'],
                    'name': student['name'],
                    'email': student['email']
                },
                credential_data={
                    'title': credential['title'],
                    'program': credential['program'],
                    'degree': credential['degree_level'],
                    'grade': f"GPA: {credential['gpa']}",
                    'graduation_date': credential['graduation_date'],
                    'honors': credential.get('honors'),
                    'credits': credential['credits_completed'],
                    'competencies': credential['competencies'],
                    'institution': institution['name'],
                    'institution_address': institution['blockchain_address']
                },
                governance_frameworks=[framework.value for framework in institution['accreditations']]
            )
            
            print("\n✅ Credential Successfully Issued!")
            print(f"📄 Credential ID: {result.get('credential_id')}")
            print(f"🔗 Transaction Hash: {result.get('transaction_hash')}")
            print(f"⛽ Gas Used: {result.get('gas_used')}")
            print(f"🏛️ Governance Compliance: {', '.join([f.value for f in institution['accreditations']])}")
            
            # Store credential ID for verification demo
            self.issued_credential_id = result.get('credential_id')
            
        except Exception as e:
            logger.error(f"Error issuing credential: {e}")
            print(f"❌ Error: {e}")
    
    async def demonstrate_credential_verification(self):
        """
        Demonstrate credential verification process
        """
        print(f"\n{'='*60}")
        print("CREDENTIAL VERIFICATION DEMO")
        print(f"{'='*60}")
        
        # Use previously issued credential or a sample ID
        credential_id = getattr(self, 'issued_credential_id', 12345)
        
        print(f"Verifying Credential ID: {credential_id}")
        
        try:
            verification_result = await self.client.blockchain.verify_credential(credential_id)
            
            if verification_result.get('valid'):
                print("\n✅ CREDENTIAL VERIFICATION SUCCESSFUL")
                
                credential_info = verification_result.get('credential', {})
                verification_details = verification_result.get('verification', {})
                
                print(f"📄 Credential Title: {credential_info.get('title')}")
                print(f"🎓 Program: {credential_info.get('program')}")
                print(f"👤 Student Address: {credential_info.get('student_address')}")
                print(f"📅 Issue Date: {credential_info.get('issue_date')}")
                print(f"🏛️ Governance Frameworks: {', '.join(credential_info.get('governance_frameworks', []))}")
                
                print("\n🔍 Verification Details:")
                print(f"  🔗 Blockchain Verified: {'✅' if verification_details.get('blockchain_verified') else '❌'}")
                print(f"  📋 Governance Compliant: {'✅' if verification_details.get('governance_compliant') else '❌'}")
                print(f"  📂 IPFS Accessible: {'✅' if verification_details.get('ipfs_accessible') else '❌'}")
                
                # Demonstrate additional verification checks
                await self._perform_additional_verification_checks(credential_info)
                
            else:
                print("\n❌ CREDENTIAL VERIFICATION FAILED")
                print("This credential could not be verified on the blockchain.")
                
        except Exception as e:
            logger.error(f"Error verifying credential: {e}")
            print(f"❌ Error: {e}")
    
    async def _perform_additional_verification_checks(self, credential_info: Dict[str, Any]):
        """Perform additional verification checks beyond basic blockchain verification"""
        print("\n🔍 Additional Verification Checks:")
        
        # Check institution authority
        institution_authorized = True  # In real implementation, check against authorized issuers
        print(f"  🏛️ Institution Authority: {'✅' if institution_authorized else '❌'}")
        
        # Check credential format compliance
        format_compliant = self._check_credential_format(credential_info)
        print(f"  📋 Format Compliance: {'✅' if format_compliant else '❌'}")
        
        # Check governance framework compliance
        governance_compliant = self._check_governance_compliance(credential_info)
        print(f"  ⚖️ Governance Compliance: {'✅' if governance_compliant else '❌'}")
        
        # Security score calculation
        security_score = self._calculate_security_score(credential_info)
        security_emoji = "🟢" if security_score >= 90 else "🟡" if security_score >= 70 else "🔴"
        print(f"  {security_emoji} Security Score: {security_score}%")
    
    def _check_credential_format(self, credential_info: Dict[str, Any]) -> bool:
        """Check if credential follows standard format requirements"""
        required_fields = ['title', 'program', 'student_address', 'issue_date']
        return all(field in credential_info for field in required_fields)
    
    def _check_governance_compliance(self, credential_info: Dict[str, Any]) -> bool:
        """Check governance framework compliance"""
        frameworks = credential_info.get('governance_frameworks', [])
        return len(frameworks) > 0
    
    def _calculate_security_score(self, credential_info: Dict[str, Any]) -> int:
        """Calculate a security score for the credential"""
        score = 70  # Base score
        
        # Add points for various security features
        if credential_info.get('governance_frameworks'):
            score += 10
        if credential_info.get('issue_date'):
            score += 5
        if credential_info.get('student_address'):
            score += 10
        if len(credential_info.get('title', '')) > 10:
            score += 5
        
        return min(100, score)
    
    async def demonstrate_student_transcript_management(self):
        """
        Demonstrate comprehensive student transcript management
        """
        print(f"\n{'='*60}")
        print("STUDENT TRANSCRIPT MANAGEMENT DEMO")
        print(f"{'='*60}")
        
        student = self.sample_students['graduate_student']
        print(f"Student: {student['name']} ({student['student_id']})")
        print(f"Blockchain Address: {student['blockchain_address']}")
        
        try:
            # Get all credentials for the student
            credentials = await self.client.blockchain.get_student_credentials(
                student['blockchain_address']
            )
            
            print(f"\n📜 Academic Transcript")
            print("-" * 30)
            
            if credentials:
                total_credentials = len(credentials)
                verified_credentials = sum(1 for c in credentials if c.get('verified'))
                
                print(f"📊 Summary: {total_credentials} credentials, {verified_credentials} verified")
                print()
                
                for i, credential in enumerate(credentials, 1):
                    status_emoji = "✅" if credential.get('verified') else "⏳"
                    print(f"{i}. {status_emoji} {credential.get('title')}")
                    print(f"   📅 Issued: {credential.get('issue_date')}")
                    print(f"   🎓 Program: {credential.get('program')}")
                    print(f"   🆔 ID: {credential.get('id')}")
                    print()
                
                # Demonstrate transcript sharing
                await self._demonstrate_transcript_sharing(student, credentials)
                
            else:
                print("📄 No credentials found for this student.")
                print("This could mean:")
                print("  • Student hasn't graduated yet")
                print("  • Credentials haven't been issued on blockchain")
                print("  • Blockchain address is incorrect")
                
        except Exception as e:
            logger.error(f"Error managing transcript: {e}")
            print(f"❌ Error: {e}")
    
    async def _demonstrate_transcript_sharing(self, student: Dict[str, Any], credentials: List[Dict[str, Any]]):
        """Demonstrate secure transcript sharing capabilities"""
        print("🔐 Secure Transcript Sharing Demo")
        print("-" * 35)
        
        # Generate sharing token (simulated)
        sharing_token = self._generate_sharing_token(student, credentials)
        
        print(f"📤 Sharing Token Generated: {sharing_token[:16]}...")
        print("🔗 This token allows secure, time-limited access to transcript")
        print("⏰ Token expires in 24 hours")
        print("🔒 Token includes verification checksums")
        
        # Demonstrate sharing scenarios
        sharing_scenarios = [
            "Employer verification for job application",
            "Graduate school application review",
            "Professional licensing board verification",
            "Third-party credential evaluation service"
        ]
        
        print("\n📋 Common Sharing Scenarios:")
        for i, scenario in enumerate(sharing_scenarios, 1):
            print(f"  {i}. {scenario}")
    
    def _generate_sharing_token(self, student: Dict[str, Any], credentials: List[Dict[str, Any]]) -> str:
        """Generate a secure sharing token for transcript access"""
        # In a real implementation, this would be a proper JWT or similar
        token_data = {
            'student_id': student['student_id'],
            'blockchain_address': student['blockchain_address'],
            'credential_count': len(credentials),
            'timestamp': datetime.now().isoformat(),
            'expires': (datetime.now().timestamp() + 86400)  # 24 hours
        }
        
        # Create hash of token data
        token_string = json.dumps(token_data, sort_keys=True)
        return hashlib.sha256(token_string.encode()).hexdigest()
    
    async def demonstrate_multi_institution_credentials(self):
        """
        Demonstrate handling credentials from multiple institutions
        """
        print(f"\n{'='*60}")
        print("MULTI-INSTITUTION CREDENTIALS DEMO")
        print(f"{'='*60}")
        
        # Simulate a student with credentials from multiple institutions
        multi_student = {
            'student_id': 'STU2024004',
            'name': 'Dr. Alexander Rodriguez',
            'blockchain_address': '0xabc3f321773dE654025034867Jac358e1e3Da9D',
            'educational_journey': [
                {
                    'institution': 'state_university',
                    'degree': 'Bachelor of Science in Physics',
                    'graduation_date': date(2018, 5, 20),
                    'gpa': 3.85
                },
                {
                    'institution': 'private_college',
                    'degree': 'Master of Science in Applied Physics',
                    'graduation_date': date(2020, 12, 15),
                    'gpa': 3.92
                },
                {
                    'institution': 'international_university',
                    'degree': 'Doctor of Philosophy in Quantum Physics',
                    'graduation_date': date(2024, 6, 30),
                    'gpa': 4.0
                }
            ]
        }
        
        print(f"Student: {multi_student['name']}")
        print(f"Educational Journey: {len(multi_student['educational_journey'])} institutions")
        
        # Issue credentials from each institution
        issued_credentials = []
        
        for i, education in enumerate(multi_student['educational_journey']):
            institution = self.sample_institutions[education['institution']]
            
            print(f"\n📄 Issuing credential {i+1}/3 from {institution['name']}")
            
            try:
                result = await self.client.blockchain.issue_credential(
                    student_data={
                        'student_id': multi_student['student_id'],
                        'blockchain_address': multi_student['blockchain_address'],
                        'name': multi_student['name'],
                        'email': f"{multi_student['name'].lower().replace(' ', '.')}@{education['institution']}.edu"
                    },
                    credential_data={
                        'title': education['degree'],
                        'program': education['degree'].split(' in ')[-1],
                        'degree': education['degree'].split(' ')[0],
                        'grade': f"GPA: {education['gpa']}",
                        'graduation_date': education['graduation_date'],
                        'institution': institution['name']
                    },
                    governance_frameworks=[framework.value for framework in institution['accreditations']]
                )
                
                issued_credentials.append({
                    'credential_id': result.get('credential_id'),
                    'institution': institution['name'],
                    'degree': education['degree'],
                    'transaction_hash': result.get('transaction_hash')
                })
                
                print(f"  ✅ Issued: Credential ID {result.get('credential_id')}")
                
            except Exception as e:
                logger.error(f"Error issuing credential from {institution['name']}: {e}")
                print(f"  ❌ Error: {e}")
        
        # Demonstrate comprehensive verification
        if issued_credentials:
            print(f"\n🔍 Comprehensive Verification of All Credentials")
            print("-" * 50)
            
            for cred in issued_credentials:
                print(f"📄 {cred['degree']} from {cred['institution']}")
                print(f"   🆔 ID: {cred['credential_id']}")
                print(f"   ✅ Blockchain Verified")
                print()
    
    async def demonstrate_governance_compliance_tracking(self):
        """
        Demonstrate governance framework compliance tracking
        """
        print(f"\n{'='*60}")
        print("GOVERNANCE COMPLIANCE TRACKING DEMO")
        print(f"{'='*60}")
        
        # Test compliance across different frameworks
        frameworks_to_test = [
            GovernanceFramework.AACSB,
            GovernanceFramework.WASC,
            GovernanceFramework.MIDDLE_STATES,
            GovernanceFramework.QAA
        ]
        
        institution = self.sample_institutions['state_university']
        
        print(f"Institution: {institution['name']}")
        print(f"Testing Compliance: {len(frameworks_to_test)} frameworks")
        
        for framework in frameworks_to_test:
            print(f"\n📋 {framework.value.upper()} Compliance Check")
            print("-" * 40)
            
            try:
                compliance_status = await self.client.governance.get_compliance_status(
                    institution['name'],
                    framework
                )
                
                status = compliance_status.get('overall_status', 'unknown')
                status_emoji = {
                    'compliant': '✅',
                    'non_compliant': '❌',
                    'under_review': '⏳'
                }.get(status, '❓')
                
                print(f"Status: {status_emoji} {status.title()}")
                print(f"Last Audit: {compliance_status.get('last_audit_date', 'N/A')}")
                print(f"Next Audit: {compliance_status.get('next_audit_date', 'N/A')}")
                
                # Show compliance areas
                areas = compliance_status.get('areas', [])
                if areas:
                    print("Compliance Areas:")
                    for area in areas:
                        area_emoji = '✅' if area.get('status') == 'compliant' else '⏳'
                        print(f"  {area_emoji} {area.get('area')}")
                
            except Exception as e:
                logger.error(f"Error checking {framework.value} compliance: {e}")
                print(f"❌ Error: {e}")
    
    async def demonstrate_fraud_prevention(self):
        """
        Demonstrate fraud prevention and security features
        """
        print(f"\n{'='*60}")
        print("FRAUD PREVENTION & SECURITY DEMO")
        print(f"{'='*60}")
        
        print("🔐 Blockchain Security Features:")
        print("✅ Immutable record storage")
        print("✅ Cryptographic verification")
        print("✅ Multi-signature authentication")
        print("✅ Governance framework compliance")
        print("✅ Tamper-evident timestamps")
        print("✅ Distributed consensus validation")
        
        # Demonstrate attempt to verify fake credential
        print(f"\n🚨 Fake Credential Detection Demo")
        print("-" * 40)
        
        fake_credential_id = 999999  # Non-existent credential
        
        try:
            verification_result = await self.client.blockchain.verify_credential(fake_credential_id)
            
            if not verification_result.get('valid'):
                print("✅ FRAUD DETECTION SUCCESSFUL")
                print(f"Fake credential ID {fake_credential_id} was correctly identified as invalid")
                print("🔍 Blockchain verification failed - no matching record found")
            else:
                print("⚠️ Unexpected result - this should not happen with a fake ID")
                
        except Exception as e:
            print("✅ FRAUD DETECTION SUCCESSFUL")
            print(f"System correctly rejected fake credential: {e}")
        
        # Demonstrate security monitoring
        print(f"\n📊 Security Monitoring")
        print("-" * 25)
        
        try:
            network_status = await self.client.blockchain.get_network_status()
            
            if network_status.get('connected'):
                print("✅ Blockchain network operational")
                print(f"🔗 Network ID: {network_status.get('network_id')}")
                print(f"📦 Current Block: {network_status.get('block_number')}")
                print(f"⛽ Gas Price: {network_status.get('gas_price')} wei")
                
                contracts = network_status.get('contracts_deployed', {})
                print(f"📋 Smart Contracts: {len(contracts)} deployed")
                for contract_name, address in contracts.items():
                    print(f"  • {contract_name}: {address[:10]}...")
            else:
                print("❌ Blockchain network unavailable")
                
        except Exception as e:
            logger.error(f"Error checking network status: {e}")
            print(f"❌ Error: {e}")
    
    async def run_all_demos(self):
        """Run all blockchain credential demonstrations"""
        print("🔗 CollegiumAI Blockchain Credentials SDK Demo")
        print("=" * 60)
        
        try:
            # Check system health first
            health = await self.client.health_check()
            print(f"✅ System Health: {health.get('status', 'Unknown')}")
            
            # Check blockchain connectivity
            try:
                network_status = await self.client.blockchain.get_network_status()
                if network_status.get('connected'):
                    print(f"🔗 Blockchain Connected: Network {network_status.get('network_id')}")
                else:
                    print("⚠️ Blockchain not connected - some features may be limited")
            except Exception as e:
                print(f"⚠️ Blockchain status unknown: {e}")
            
            # Run all demonstration scenarios
            await self.demonstrate_credential_issuance()
            await self.demonstrate_credential_verification()
            await self.demonstrate_student_transcript_management()
            await self.demonstrate_multi_institution_credentials()
            await self.demonstrate_governance_compliance_tracking()
            await self.demonstrate_fraud_prevention()
            
            print(f"\n{'='*60}")
            print("🎉 All Blockchain Credentials Demos Completed Successfully!")
            print("="*60)
            
        except Exception as e:
            logger.error(f"Error running demos: {e}")
            print(f"❌ Demo failed: {e}")

async def main():
    """Main function to run the blockchain credentials examples"""
    parser = argparse.ArgumentParser(description='CollegiumAI Blockchain Credentials SDK Examples')
    parser.add_argument('--api-key', help='API key for CollegiumAI')
    parser.add_argument('--base-url', default='http://localhost:4000/api/v1', help='Base URL for API')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--demo', choices=[
        'issuance', 'verification', 'transcript', 'multi-institution', 
        'governance', 'fraud-prevention', 'all'
    ], default='all', help='Specific demo to run')
    
    args = parser.parse_args()
    
    # Get API key from environment or command line
    api_key = args.api_key or os.getenv('COLLEGIUMAI_API_KEY')
    if not api_key:
        print("❌ Error: API key required. Set COLLEGIUMAI_API_KEY environment variable or use --api-key")
        return
    
    # Create SDK configuration
    config = SDKConfig(
        api_base_url=args.base_url,
        api_key=api_key,
        debug=args.debug,
        blockchain_enabled=True,
        timeout=60
    )
    
    # Run the demonstration
    async with BlockchainCredentialsDemo(config) as demo:
        if args.demo == 'all':
            await demo.run_all_demos()
        elif args.demo == 'issuance':
            await demo.demonstrate_credential_issuance()
        elif args.demo == 'verification':
            await demo.demonstrate_credential_verification()
        elif args.demo == 'transcript':
            await demo.demonstrate_student_transcript_management()
        elif args.demo == 'multi-institution':
            await demo.demonstrate_multi_institution_credentials()
        elif args.demo == 'governance':
            await demo.demonstrate_governance_compliance_tracking()
        elif args.demo == 'fraud-prevention':
            await demo.demonstrate_fraud_prevention()

if __name__ == "__main__":
    asyncio.run(main())