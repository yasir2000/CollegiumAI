"""
CollegiumAI SDK - Python Client Library
Comprehensive SDK for integrating with the CollegiumAI Framework
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum

# Import framework components
from ..framework.core import (
    PersonaType, GovernanceFramework, ProcessType, 
    UniversityContext, AgentResponse
)

logger = logging.getLogger(__name__)

@dataclass
class SDKConfig:
    """SDK configuration settings"""
    api_base_url: str = "http://localhost:4000/api/v1"
    api_key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    blockchain_enabled: bool = True
    debug: bool = False

class CollegiumAIClient:
    """
    Main client class for interacting with CollegiumAI Framework
    """
    
    def __init__(self, config: SDKConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self._agents: Dict[str, 'AgentClient'] = {}
        self._blockchain: Optional['BlockchainClient'] = None
        self._governance: Optional['GovernanceClient'] = None
        
        if config.debug:
            logging.basicConfig(level=logging.DEBUG)
    
    async def __aenter__(self):
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def initialize(self):
        """Initialize the client and create HTTP session"""
        headers = {'Content-Type': 'application/json'}
        if self.config.api_key:
            headers['Authorization'] = f'Bearer {self.config.api_key}'
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        
        # Initialize sub-clients
        self._blockchain = BlockchainClient(self)
        self._governance = GovernanceClient(self)
        
        logger.info("CollegiumAI client initialized")
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()
        logger.info("CollegiumAI client closed")
    
    @property
    def blockchain(self) -> 'BlockchainClient':
        """Access blockchain operations"""
        if not self._blockchain:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._blockchain
    
    @property
    def governance(self) -> 'GovernanceClient':
        """Access governance operations"""
        if not self._governance:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._governance
    
    def agent(self, agent_type: str) -> 'AgentClient':
        """Get or create an agent client"""
        if agent_type not in self._agents:
            self._agents[agent_type] = AgentClient(self, agent_type)
        return self._agents[agent_type]
    
    async def get_university_context(self) -> Dict[str, Any]:
        """Get university context information"""
        async with self.session.get(f"{self.config.api_base_url}/university/context") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get university context: {response.status}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health status of the CollegiumAI services"""
        async with self.session.get(f"{self.config.api_base_url}/health") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Health check failed: {response.status}")

class AgentClient:
    """
    Client for interacting with specific AI agents
    """
    
    def __init__(self, client: CollegiumAIClient, agent_type: str):
        self.client = client
        self.agent_type = agent_type
    
    async def query(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        user_id: str = None,
        user_type: Union[str, PersonaType] = None,
        collaborative: bool = True
    ) -> Dict[str, Any]:
        """
        Send a query to the agent
        
        Args:
            message: The query message
            context: Additional context information
            user_id: ID of the user making the query
            user_type: Type/persona of the user
            collaborative: Whether to enable agent collaboration
            
        Returns:
            Agent response with thoughts, actions, and final response
        """
        
        if context is None:
            context = {}
        
        # Convert PersonaType enum to string if needed
        if isinstance(user_type, PersonaType):
            user_type = user_type.value
        
        payload = {
            'message': message,
            'context': context,
            'user_id': user_id,
            'user_type': user_type,
            'collaborative': collaborative,
            'agent_type': self.agent_type
        }
        
        async with self.client.session.post(
            f"{self.client.config.api_base_url}/agents/{self.agent_type}/query",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Agent query failed: {response.status} - {error_text}")
    
    async def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent"""
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/agents/{self.agent_type}/info"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get agent info: {response.status}")
    
    async def update_knowledge_base(self, knowledge: Dict[str, Any]) -> bool:
        """Update the agent's knowledge base"""
        async with self.client.session.post(
            f"{self.client.config.api_base_url}/agents/{self.agent_type}/knowledge",
            json=knowledge
        ) as response:
            return response.status == 200

class BlockchainClient:
    """
    Client for blockchain operations
    """
    
    def __init__(self, client: CollegiumAIClient):
        self.client = client
    
    async def issue_credential(
        self,
        student_data: Dict[str, Any],
        credential_data: Dict[str, Any],
        governance_frameworks: List[str]
    ) -> Dict[str, Any]:
        """
        Issue a new academic credential on the blockchain
        
        Args:
            student_data: Student information including blockchain address
            credential_data: Credential details (title, program, grade, etc.)
            governance_frameworks: List of applicable governance frameworks
            
        Returns:
            Transaction result with credential ID and blockchain hash
        """
        payload = {
            'student_data': student_data,
            'credential_data': credential_data,
            'governance_frameworks': governance_frameworks
        }
        
        async with self.client.session.post(
            f"{self.client.config.api_base_url}/blockchain/credentials/issue",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Failed to issue credential: {response.status} - {error_text}")
    
    async def verify_credential(self, credential_id: int) -> Dict[str, Any]:
        """
        Verify a credential on the blockchain
        
        Args:
            credential_id: ID of the credential to verify
            
        Returns:
            Verification result with credential details
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/credentials/{credential_id}/verify"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to verify credential: {response.status}")
    
    async def get_student_credentials(self, student_address: str) -> List[Dict[str, Any]]:
        """
        Get all credentials for a student
        
        Args:
            student_address: Blockchain address of the student
            
        Returns:
            List of student credentials
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/students/{student_address}/credentials"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get student credentials: {response.status}")
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get blockchain network status"""
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/status"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get network status: {response.status}")
    
    # Bologna Process Functions
    
    async def set_bologna_compliance(
        self,
        credential_id: int,
        ects_credits: int,
        eqf_level: int,
        diploma_supplement_issued: bool,
        learning_outcomes: List[str],
        quality_assurance_agency: str,
        joint_degree_program: bool = False,
        mobility_partners: List[str] = None
    ) -> Dict[str, Any]:
        """
        Set Bologna Process compliance data for a credential
        
        Args:
            credential_id: ID of the credential
            ects_credits: European Credit Transfer System credits
            eqf_level: European Qualifications Framework level (1-8)
            diploma_supplement_issued: Whether diploma supplement is issued
            learning_outcomes: List of learning outcome descriptions
            quality_assurance_agency: Name of the quality assurance agency
            joint_degree_program: Whether this is a joint degree program
            mobility_partners: List of mobility partner institutions
            
        Returns:
            Transaction result
        """
        if mobility_partners is None:
            mobility_partners = []
            
        payload = {
            'credential_id': credential_id,
            'ects_credits': ects_credits,
            'eqf_level': eqf_level,
            'diploma_supplement_issued': diploma_supplement_issued,
            'learning_outcomes': learning_outcomes,
            'quality_assurance_agency': quality_assurance_agency,
            'joint_degree_program': joint_degree_program,
            'mobility_partners': mobility_partners
        }
        
        async with self.client.session.post(
            f"{self.client.config.api_base_url}/blockchain/credentials/bologna/compliance",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Failed to set Bologna compliance: {response.status} - {error_text}")
    
    async def get_bologna_compliance(self, credential_id: int) -> Dict[str, Any]:
        """
        Get Bologna Process compliance data for a credential
        
        Args:
            credential_id: ID of the credential
            
        Returns:
            Bologna Process compliance data
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/credentials/{credential_id}/bologna"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get Bologna compliance: {response.status}")
    
    async def update_ects_credits(self, credential_id: int, new_ects_credits: int) -> Dict[str, Any]:
        """
        Update ECTS credits for a credential
        
        Args:
            credential_id: ID of the credential
            new_ects_credits: New ECTS credit value
            
        Returns:
            Transaction result
        """
        payload = {
            'credential_id': credential_id,
            'new_ects_credits': new_ects_credits
        }
        
        async with self.client.session.put(
            f"{self.client.config.api_base_url}/blockchain/credentials/ects",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Failed to update ECTS credits: {response.status} - {error_text}")
    
    async def check_automatic_recognition_eligibility(self, credential_id: int) -> bool:
        """
        Check if credential qualifies for automatic recognition under Bologna Process
        
        Args:
            credential_id: ID of the credential
            
        Returns:
            True if eligible for automatic recognition
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/credentials/{credential_id}/auto-recognition"
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result.get('eligible', False)
            else:
                raise Exception(f"Failed to check automatic recognition eligibility: {response.status}")
    
    async def get_student_total_ects(self, student_address: str) -> int:
        """
        Get total ECTS credits for a student
        
        Args:
            student_address: Blockchain address of the student
            
        Returns:
            Total ECTS credits
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/students/{student_address}/ects-total"
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result.get('total_ects', 0)
            else:
                raise Exception(f"Failed to get student total ECTS: {response.status}")
    
    async def check_bologna_compliance_status(self, credential_id: int) -> Dict[str, Any]:
        """
        Check Bologna Process framework compliance for credential
        
        Args:
            credential_id: ID of the credential
            
        Returns:
            Compliance status and detailed report
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/blockchain/credentials/{credential_id}/bologna/compliance-check"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to check Bologna compliance status: {response.status}")

class GovernanceClient:
    """
    Client for governance and compliance operations
    """
    
    def __init__(self, client: CollegiumAIClient):
        self.client = client
    
    async def create_audit(
        self,
        institution: str,
        framework: Union[str, GovernanceFramework],
        audit_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a compliance audit
        
        Args:
            institution: Name of the institution
            framework: Governance framework (e.g., 'aacsb', 'wasc')
            audit_data: Audit details including area, findings, recommendations
            
        Returns:
            Audit creation result with audit ID and blockchain transaction
        """
        if isinstance(framework, GovernanceFramework):
            framework = framework.value
        
        payload = {
            'institution': institution,
            'framework': framework,
            'audit_data': audit_data
        }
        
        async with self.client.session.post(
            f"{self.client.config.api_base_url}/governance/audits",
            json=payload
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Failed to create audit: {response.status} - {error_text}")
    
    async def get_compliance_status(
        self,
        institution: str,
        framework: Union[str, GovernanceFramework]
    ) -> Dict[str, Any]:
        """
        Get compliance status for an institution and framework
        
        Args:
            institution: Name of the institution
            framework: Governance framework
            
        Returns:
            Compliance status information
        """
        if isinstance(framework, GovernanceFramework):
            framework = framework.value
        
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/governance/compliance/{institution}/{framework}"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get compliance status: {response.status}")
    
    async def get_upcoming_audits(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Get upcoming audits that need review
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of upcoming audits
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/governance/audits/upcoming?days={days_ahead}"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get upcoming audits: {response.status}")
    
    async def get_compliance_summary(self, institution: str) -> Dict[str, Any]:
        """
        Get comprehensive compliance summary for an institution
        
        Args:
            institution: Name of the institution
            
        Returns:
            Compliance summary across all frameworks
        """
        async with self.client.session.get(
            f"{self.client.config.api_base_url}/governance/compliance/{institution}/summary"
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get compliance summary: {response.status}")

# Utility classes and functions

class PersonaHelper:
    """Helper class for working with university personas"""
    
    @staticmethod
    def get_student_personas() -> List[PersonaType]:
        """Get all student persona types"""
        return [
            PersonaType.TRADITIONAL_STUDENT,
            PersonaType.NON_TRADITIONAL_STUDENT,
            PersonaType.INTERNATIONAL_STUDENT,
            PersonaType.TRANSFER_STUDENT,
            PersonaType.FIRST_GENERATION_STUDENT,
            PersonaType.GRADUATE_STUDENT,
            PersonaType.STUDENT_ATHLETE,
            PersonaType.ONLINE_STUDENT,
            PersonaType.PRE_PROFESSIONAL_STUDENT,
            PersonaType.RESEARCH_ORIENTED_STUDENT,
            PersonaType.SOCIAL_ACTIVIST,
            PersonaType.ENTREPRENEURIAL_STUDENT,
            PersonaType.GLOBAL_CITIZEN,
            PersonaType.CAREER_CHANGER,
            PersonaType.LATERAL_LEARNER,
            PersonaType.CREATIVE_MIND,
            PersonaType.INNOVATOR,
            PersonaType.COMMUNITY_BUILDER,
            PersonaType.CONTINUING_LEARNER,
            PersonaType.COMMUNITY_SERVER,
            PersonaType.DIGITAL_NATIVE,
            PersonaType.ADVOCATE_FOR_CHANGE,
            PersonaType.FAMILY_COMMITMENT,
            PersonaType.CREATIVE_PROBLEM_SOLVER,
            PersonaType.COMMUTER_STUDENT,
            PersonaType.RETURNING_ADULT_STUDENT,
            PersonaType.STUDENT_WITH_DISABILITIES
        ]
    
    @staticmethod
    def get_staff_personas() -> List[PersonaType]:
        """Get all staff persona types"""
        return [
            PersonaType.ACADEMIC_ADVISOR,
            PersonaType.REGISTRAR,
            PersonaType.FINANCIAL_AID_OFFICER,
            PersonaType.ADMISSIONS_OFFICER,
            PersonaType.HR_MANAGER,
            PersonaType.IT_SUPPORT_SPECIALIST,
            PersonaType.FACILITIES_MANAGER,
            PersonaType.COMMUNICATIONS_SPECIALIST,
            PersonaType.STUDENT_SERVICES_COORDINATOR,
            PersonaType.GRANTS_ADMIN_OFFICER,
            PersonaType.DIVERSITY_INCLUSION_COORDINATOR,
            PersonaType.LEGAL_AFFAIRS_OFFICER
        ]
    
    @staticmethod
    def get_faculty_personas() -> List[PersonaType]:
        """Get all faculty persona types"""
        return [
            PersonaType.PROFESSOR,
            PersonaType.LECTURER,
            PersonaType.RESEARCHER,
            PersonaType.DEPARTMENT_HEAD,
            PersonaType.ADJUNCT_FACULTY,
            PersonaType.POSTDOCTORAL_FELLOW,
            PersonaType.ACADEMIC_ADMINISTRATOR,
            PersonaType.LIBRARIAN,
            PersonaType.TEACHING_ASSISTANT,
            PersonaType.ACADEMIC_TECHNOLOGY_SPECIALIST,
            PersonaType.ACADEMIC_COUNSELOR
        ]

class GovernanceHelper:
    """Helper class for working with governance frameworks"""
    
    @staticmethod
    def get_framework_info(framework: GovernanceFramework) -> Dict[str, Any]:
        """Get detailed information about a governance framework"""
        framework_info = {
            GovernanceFramework.AACSB: {
                'name': 'Association to Advance Collegiate Schools of Business',
                'region': 'Global',
                'focus': 'Business school accreditation',
                'standards': ['Continuous improvement', 'Faculty qualifications', 'Curriculum relevance']
            },
            GovernanceFramework.HEFCE: {
                'name': 'Higher Education Funding Council for England',
                'region': 'England',
                'focus': 'Higher education governance and funding',
                'standards': ['Quality assurance', 'Student experience', 'Research excellence']
            },
            GovernanceFramework.MIDDLE_STATES: {
                'name': 'Middle States Commission on Higher Education',
                'region': 'Mid-Atlantic US',
                'focus': 'Regional accreditation',
                'standards': ['Mission and goals', 'Ethics and integrity', 'Design and delivery of education']
            },
            GovernanceFramework.WASC: {
                'name': 'Western Association of Schools and Colleges',
                'region': 'Western US',
                'focus': 'Institutional accreditation',
                'standards': ['Institutional capacity', 'Educational effectiveness', 'Meaning and quality']
            },
            GovernanceFramework.AACSU: {
                'name': 'American Association of Colleges and Universities',
                'region': 'United States',
                'focus': 'Liberal education and assessment',
                'standards': ['Educational effectiveness', 'Student learning outcomes', 'Faculty development']
            },
            GovernanceFramework.SPHEIR: {
                'name': 'Strategic Partnerships for Higher Education Innovation and Reform',
                'region': 'Global',
                'focus': 'Innovation and reform partnerships',
                'standards': ['Innovation practices', 'Partnership development', 'Reform implementation']
            },
            GovernanceFramework.QAA: {
                'name': 'Quality Assurance Agency for Higher Education',
                'region': 'United Kingdom',
                'focus': 'Quality assurance in higher education',
                'standards': ['Academic standards', 'Quality enhancement', 'Student protection']
            }
        }
        
        return framework_info.get(framework, {'name': 'Unknown Framework'})

class ResponseBuilder:
    """Helper class for building structured responses"""
    
    @staticmethod
    def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Build a success response"""
        return {
            'success': True,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def error_response(error: str, code: int = 400) -> Dict[str, Any]:
        """Build an error response"""
        return {
            'success': False,
            'error': error,
            'code': code,
            'timestamp': datetime.now().isoformat()
        }

# Async helper functions

async def create_client(config: SDKConfig) -> CollegiumAIClient:
    """
    Create and initialize a new CollegiumAI client
    
    Args:
        config: SDK configuration
        
    Returns:
        Initialized client instance
    """
    client = CollegiumAIClient(config)
    await client.initialize()
    return client

async def quick_query(
    agent_type: str,
    message: str,
    user_type: Union[str, PersonaType] = PersonaType.TRADITIONAL_STUDENT,
    api_key: Optional[str] = None,
    api_base_url: str = "http://localhost:4000/api/v1"
) -> Dict[str, Any]:
    """
    Quick utility function for sending a single query to an agent
    
    Args:
        agent_type: Type of agent to query
        message: Query message
        user_type: Type of user making the query
        api_key: API key for authentication
        api_base_url: Base URL for the API
        
    Returns:
        Agent response
    """
    config = SDKConfig(
        api_base_url=api_base_url,
        api_key=api_key
    )
    
    async with CollegiumAIClient(config) as client:
        agent = client.agent(agent_type)
        return await agent.query(message, user_type=user_type)

# Example usage and convenience functions

class Examples:
    """Example usage patterns for the SDK"""
    
    @staticmethod
    async def academic_advising_example():
        """Example of academic advising interaction"""
        config = SDKConfig(api_key="your-api-key")
        
        async with CollegiumAIClient(config) as client:
            advisor = client.agent("academic_advisor")
            
            response = await advisor.query(
                message="I need help selecting courses for next semester",
                context={
                    "major": "Computer Science",
                    "year": "sophomore",
                    "gpa": 3.2,
                    "completed_credits": 45
                },
                user_type=PersonaType.TRADITIONAL_STUDENT
            )
            
            return response
    
    @staticmethod
    async def credential_verification_example():
        """Example of credential verification"""
        config = SDKConfig(api_key="your-api-key", blockchain_enabled=True)
        
        async with CollegiumAIClient(config) as client:
            verification_result = await client.blockchain.verify_credential(12345)
            return verification_result
    
    @staticmethod
    async def compliance_audit_example():
        """Example of creating a compliance audit"""
        config = SDKConfig(api_key="your-api-key")
        
        async with CollegiumAIClient(config) as client:
            audit_result = await client.governance.create_audit(
                institution="University of Example",
                framework=GovernanceFramework.AACSB,
                audit_data={
                    "audit_area": "Faculty Qualifications",
                    "status": "compliant",
                    "findings": "All faculty meet minimum qualifications",
                    "recommendations": "Continue current hiring practices",
                    "next_review_date": datetime(2024, 12, 31)
                }
            )
            
            return audit_result

# Export main classes and functions
__all__ = [
    'CollegiumAIClient',
    'AgentClient', 
    'BlockchainClient',
    'GovernanceClient',
    'SDKConfig',
    'PersonaHelper',
    'GovernanceHelper',
    'ResponseBuilder',
    'Examples',
    'create_client',
    'quick_query'
]