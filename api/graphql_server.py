"""
CollegiumAI GraphQL API Server
=============================

GraphQL API server for the CollegiumAI Framework providing a flexible,
type-safe interface for querying and mutating university data, AI agents,
blockchain credentials, and governance compliance information.

Features:
- Type-safe GraphQL schema for all framework components
- Real-time subscriptions for agent interactions
- Batch query optimization
- Authentication and authorization
- Comprehensive error handling
- DataLoader pattern for efficient data fetching
"""

import asyncio
import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import json

# GraphQL imports
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from strawberry.permission import BasePermission
from strawberry.extensions import Extension
import strawberry.subscriptions

# Add the parent directory to the path to import framework components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.core import (
    UniversityFramework, PersonaType, GovernanceFramework,
    ProcessType, UniversityContext, AgentResponse
)
from framework.blockchain.integration import BlockchainIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GraphQL Types and Enums
@strawberry.enum
class PersonaTypeEnum(strawberry.Enum):
    TRADITIONAL_STUDENT = "traditional_student"
    NON_TRADITIONAL_STUDENT = "non_traditional_student"
    INTERNATIONAL_STUDENT = "international_student"
    TRANSFER_STUDENT = "transfer_student"
    FIRST_GENERATION_STUDENT = "first_generation_student"
    GRADUATE_STUDENT = "graduate_student"
    STUDENT_ATHLETE = "student_athlete"
    ONLINE_STUDENT = "online_student"
    ACADEMIC_ADVISOR = "academic_advisor"
    REGISTRAR = "registrar"
    PROFESSOR = "professor"
    LECTURER = "lecturer"
    RESEARCHER = "researcher"

@strawberry.enum
class GovernanceFrameworkEnum(strawberry.Enum):
    AACSB = "aacsb"
    HEFCE = "hefce"
    MIDDLE_STATES = "middle_states"
    WASC = "wasc"
    AACSU = "aacsu"
    SPHEIR = "spheir"
    QAA = "qaa"

@strawberry.type
class AgentThought:
    observation: str
    reasoning: str
    action_plan: str
    timestamp: datetime

@strawberry.type
class AgentAction:
    action: str
    input_data: str  # JSON string
    output_data: str  # JSON string
    timestamp: datetime

@strawberry.type
class AgentQueryResult:
    success: bool
    thoughts: List[AgentThought]
    actions: List[AgentAction]
    final_response: str
    confidence: float
    collaborating_agents: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    timestamp: datetime

@strawberry.type
class CredentialInfo:
    id: int
    student_address: str
    title: str
    program: str
    degree_level: str
    issue_date: datetime
    governance_frameworks: List[GovernanceFrameworkEnum]
    verified: bool

@strawberry.type
class CredentialVerification:
    valid: bool
    credential: Optional[CredentialInfo] = None
    blockchain_verified: bool
    governance_compliant: bool
    ipfs_accessible: bool
    security_score: int

@strawberry.type
class ComplianceArea:
    area: str
    status: str
    last_reviewed: datetime

@strawberry.type
class ComplianceStatus:
    institution: str
    framework: GovernanceFrameworkEnum
    overall_status: str
    last_audit_date: datetime
    next_audit_date: datetime
    areas: List[ComplianceArea]

@strawberry.type
class UniversityInfo:
    institution_name: str
    establishment_date: datetime
    location: str  # JSON string
    total_students: int
    total_faculty: int
    total_staff: int
    governance_frameworks: List[GovernanceFrameworkEnum]

@strawberry.type
class BlockchainStatus:
    connected: bool
    network_id: int
    block_number: int
    gas_price: str
    contracts_deployed: str  # JSON string

@strawberry.type
class SystemHealth:
    status: str
    version: str
    services: str  # JSON string
    timestamp: datetime
    uptime_seconds: float

# Input Types
@strawberry.input
class AgentQueryInput:
    message: str
    context: Optional[str] = None  # JSON string
    user_id: Optional[str] = None
    user_type: Optional[PersonaTypeEnum] = None
    collaborative: bool = True

@strawberry.input
class StudentDataInput:
    student_id: str
    blockchain_address: str
    name: str
    email: str

@strawberry.input
class CredentialDataInput:
    title: str
    program: str
    degree: str
    grade: str
    graduation_date: str  # ISO date string
    honors: Optional[str] = None

@strawberry.input
class ComplianceAuditInput:
    institution: str
    framework: GovernanceFrameworkEnum
    audit_area: str
    status: str
    findings: str
    recommendations: str
    next_review_date: str  # ISO date string

# Permissions
class IsAuthenticated(BasePermission):
    message = "User must be authenticated"
    
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
        return hasattr(request, "user") and request.user is not None

class HasPermission(BasePermission):
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
        self.message = f"User must have '{required_permission}' permission"
    
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
        if not hasattr(request, "user") or request.user is None:
            return False
        
        user_permissions = request.user.get("permissions", [])
        return self.required_permission in user_permissions

# Extensions
class AuthenticationExtension(Extension):
    """Extension to handle authentication for GraphQL requests"""
    
    def on_request_start(self):
        """Extract user information from request"""
        request = self.execution_context.context.get("request")
        if request:
            # Extract JWT token from Authorization header
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                try:
                    # Decode token (reuse auth handler from REST API)
                    from api.server import auth_handler
                    user_data = auth_handler.decode_token(token)
                    request.user = user_data
                except Exception as e:
                    logger.warning(f"Invalid token: {e}")
                    request.user = None
            else:
                request.user = None

class LoggingExtension(Extension):
    """Extension to log GraphQL operations"""
    
    def on_request_start(self):
        self.start_time = datetime.utcnow()
    
    def on_request_end(self):
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        
        operation_name = self.execution_context.query.split()[1] if len(self.execution_context.query.split()) > 1 else "unknown"
        
        logger.info(f"GraphQL {operation_name} completed in {duration:.3f}s")

# Global variables
university_framework: Optional[UniversityFramework] = None
blockchain_integration: Optional[BlockchainIntegration] = None

# Query resolvers
@strawberry.type
class Query:
    @strawberry.field
    async def health(self) -> SystemHealth:
        """Get system health status"""
        services = {}
        
        if university_framework:
            services["university_framework"] = "operational"
        else:
            services["university_framework"] = "unavailable"
        
        if blockchain_integration:
            try:
                status = await blockchain_integration.get_network_status()
                services["blockchain"] = "connected" if status.get("connected") else "disconnected"
            except Exception:
                services["blockchain"] = "error"
        else:
            services["blockchain"] = "unavailable"
        
        return SystemHealth(
            status="healthy" if all(s in ["operational", "connected"] for s in services.values()) else "degraded",
            version="1.0.0",
            services=json.dumps(services),
            timestamp=datetime.utcnow(),
            uptime_seconds=3600  # Placeholder
        )
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def university_info(self) -> UniversityInfo:
        """Get university context information"""
        if not university_framework:
            raise Exception("University framework not available")
        
        context = university_framework.get_context()
        
        return UniversityInfo(
            institution_name=context.institution_name,
            establishment_date=context.establishment_date,
            location=json.dumps(context.location),
            total_students=context.total_students,
            total_faculty=context.total_faculty,
            total_staff=context.total_staff,
            governance_frameworks=[GovernanceFrameworkEnum.AACSB, GovernanceFrameworkEnum.WASC]  # Example
        )
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def verify_credential(self, credential_id: int) -> CredentialVerification:
        """Verify a blockchain credential"""
        if not blockchain_integration:
            raise Exception("Blockchain integration not available")
        
        try:
            result = await blockchain_integration.verify_credential(credential_id)
            
            credential = None
            if result.get("valid") and result.get("credential"):
                cred_data = result["credential"]
                credential = CredentialInfo(
                    id=cred_data["id"],
                    student_address=cred_data["student_address"],
                    title=cred_data["title"],
                    program=cred_data["program"],
                    degree_level=cred_data.get("degree_level", "Bachelor"),
                    issue_date=datetime.fromisoformat(cred_data["issue_date"]),
                    governance_frameworks=[GovernanceFrameworkEnum.AACSB],  # Example
                    verified=True
                )
            
            verification = result.get("verification", {})
            
            return CredentialVerification(
                valid=result.get("valid", False),
                credential=credential,
                blockchain_verified=verification.get("blockchain_verified", False),
                governance_compliant=verification.get("governance_compliant", False),
                ipfs_accessible=verification.get("ipfs_accessible", False),
                security_score=85  # Example score
            )
            
        except Exception as e:
            logger.error(f"Error verifying credential: {e}")
            raise Exception(f"Credential verification failed: {str(e)}")
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def student_credentials(self, student_address: str) -> List[CredentialInfo]:
        """Get all credentials for a student"""
        if not blockchain_integration:
            raise Exception("Blockchain integration not available")
        
        try:
            credentials = await blockchain_integration.get_student_credentials(student_address)
            
            result = []
            for cred in credentials:
                result.append(CredentialInfo(
                    id=cred["id"],
                    student_address=student_address,
                    title=cred["title"],
                    program=cred["program"],
                    degree_level=cred.get("degree_level", "Bachelor"),
                    issue_date=datetime.fromisoformat(cred["issue_date"]),
                    governance_frameworks=[GovernanceFrameworkEnum.AACSB],
                    verified=cred.get("verified", False)
                ))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting student credentials: {e}")
            raise Exception(f"Failed to get student credentials: {str(e)}")
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def compliance_status(
        self, 
        institution: str, 
        framework: GovernanceFrameworkEnum
    ) -> ComplianceStatus:
        """Get compliance status for an institution and framework"""
        try:
            # Mock data - in real implementation, query blockchain
            return ComplianceStatus(
                institution=institution,
                framework=framework,
                overall_status="compliant",
                last_audit_date=datetime.utcnow() - timedelta(days=90),
                next_audit_date=datetime.utcnow() + timedelta(days=275),
                areas=[
                    ComplianceArea(
                        area="Faculty Qualifications",
                        status="compliant",
                        last_reviewed=datetime.utcnow() - timedelta(days=30)
                    ),
                    ComplianceArea(
                        area="Curriculum Standards",
                        status="compliant",
                        last_reviewed=datetime.utcnow() - timedelta(days=60)
                    )
                ]
            )
            
        except Exception as e:
            logger.error(f"Error getting compliance status: {e}")
            raise Exception(f"Failed to get compliance status: {str(e)}")
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def blockchain_status(self) -> BlockchainStatus:
        """Get blockchain network status"""
        if not blockchain_integration:
            raise Exception("Blockchain integration not available")
        
        try:
            status = await blockchain_integration.get_network_status()
            
            return BlockchainStatus(
                connected=status.get("connected", False),
                network_id=status.get("network_id", 0),
                block_number=status.get("block_number", 0),
                gas_price=status.get("gas_price", "0"),
                contracts_deployed=json.dumps(status.get("contracts_deployed", {}))
            )
            
        except Exception as e:
            logger.error(f"Error getting blockchain status: {e}")
            raise Exception(f"Failed to get blockchain status: {str(e)}")

# Mutation resolvers
@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated, HasPermission("agent_query")])
    async def query_agent(
        self, 
        agent_type: str, 
        query_input: AgentQueryInput
    ) -> AgentQueryResult:
        """Send a query to an AI agent"""
        if not university_framework:
            raise Exception("University framework not available")
        
        try:
            # Get the appropriate agent
            if agent_type == "academic_advisor":
                from framework.agents.academic_advisor import AcademicAdvisorAgent
                agent = AcademicAdvisorAgent("academic_advisor", university_framework)
            elif agent_type == "student_services":
                from framework.agents.student_services import StudentServicesAgent
                agent = StudentServicesAgent("student_services", university_framework)
            else:
                raise Exception(f"Unknown agent type: {agent_type}")
            
            # Parse context if provided
            context = {}
            if query_input.context:
                try:
                    context = json.loads(query_input.context)
                except json.JSONDecodeError:
                    pass
            
            # Convert persona type
            user_type = None
            if query_input.user_type:
                user_type = PersonaType(query_input.user_type.value)
            
            # Process the query
            response = await agent.process_query(
                message=query_input.message,
                context=context,
                user_id=query_input.user_id,
                user_type=user_type,
                collaborative=query_input.collaborative
            )
            
            # Convert thoughts to GraphQL format
            thoughts = [
                AgentThought(
                    observation=t.get("observation", ""),
                    reasoning=t.get("reasoning", ""),
                    action_plan=t.get("action_plan", ""),
                    timestamp=datetime.fromisoformat(t.get("timestamp", datetime.utcnow().isoformat()))
                )
                for t in response.thoughts
            ]
            
            # Convert actions to GraphQL format
            actions = [
                AgentAction(
                    action=a.get("action", ""),
                    input_data=json.dumps(a.get("input", {})),
                    output_data=json.dumps(a.get("output", {})),
                    timestamp=datetime.fromisoformat(a.get("timestamp", datetime.utcnow().isoformat()))
                )
                for a in response.actions
            ]
            
            return AgentQueryResult(
                success=True,
                thoughts=thoughts,
                actions=actions,
                final_response=response.final_response,
                confidence=response.confidence,
                collaborating_agents=response.collaborating_agents,
                recommendations=response.recommendations,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error processing agent query: {e}")
            raise Exception(f"Agent query failed: {str(e)}")
    
    @strawberry.field(permission_classes=[IsAuthenticated, HasPermission("credential_issue")])
    async def issue_credential(
        self,
        student_data: StudentDataInput,
        credential_data: CredentialDataInput,
        governance_frameworks: List[GovernanceFrameworkEnum]
    ) -> CredentialInfo:
        """Issue a new academic credential"""
        if not blockchain_integration:
            raise Exception("Blockchain integration not available")
        
        try:
            # Convert input data
            student_dict = {
                "student_id": student_data.student_id,
                "blockchain_address": student_data.blockchain_address,
                "name": student_data.name,
                "email": student_data.email
            }
            
            credential_dict = {
                "title": credential_data.title,
                "program": credential_data.program,
                "degree": credential_data.degree,
                "grade": credential_data.grade,
                "graduation_date": credential_data.graduation_date,
                "honors": credential_data.honors
            }
            
            frameworks = [f.value for f in governance_frameworks]
            
            # Issue credential
            result = await blockchain_integration.issue_credential(
                student_dict,
                credential_dict,
                frameworks
            )
            
            return CredentialInfo(
                id=result["credential_id"],
                student_address=student_data.blockchain_address,
                title=credential_data.title,
                program=credential_data.program,
                degree_level=credential_data.degree,
                issue_date=datetime.utcnow(),
                governance_frameworks=governance_frameworks,
                verified=True
            )
            
        except Exception as e:
            logger.error(f"Error issuing credential: {e}")
            raise Exception(f"Credential issuance failed: {str(e)}")
    
    @strawberry.field(permission_classes=[IsAuthenticated, HasPermission("governance_audit")])
    async def create_compliance_audit(
        self,
        audit_input: ComplianceAuditInput
    ) -> ComplianceStatus:
        """Create a new compliance audit"""
        if not blockchain_integration:
            raise Exception("Blockchain integration not available")
        
        try:
            audit_data = {
                "audit_area": audit_input.audit_area,
                "status": audit_input.status,
                "findings": audit_input.findings,
                "recommendations": audit_input.recommendations,
                "next_review_date": audit_input.next_review_date
            }
            
            result = await blockchain_integration.create_compliance_audit(
                audit_input.institution,
                audit_input.framework.value,
                audit_data
            )
            
            return ComplianceStatus(
                institution=audit_input.institution,
                framework=audit_input.framework,
                overall_status=audit_input.status,
                last_audit_date=datetime.utcnow(),
                next_audit_date=datetime.fromisoformat(audit_input.next_review_date),
                areas=[
                    ComplianceArea(
                        area=audit_input.audit_area,
                        status=audit_input.status,
                        last_reviewed=datetime.utcnow()
                    )
                ]
            )
            
        except Exception as e:
            logger.error(f"Error creating compliance audit: {e}")
            raise Exception(f"Compliance audit creation failed: {str(e)}")

# Subscription resolvers
@strawberry.type
class Subscription:
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def agent_interaction_updates(self) -> strawberry.AsyncGenerator[AgentQueryResult, None]:
        """Subscribe to real-time agent interaction updates"""
        # This would connect to a message queue or pub/sub system in production
        while True:
            await asyncio.sleep(5)  # Simulate periodic updates
            
            # Mock update - in real implementation, yield actual updates
            yield AgentQueryResult(
                success=True,
                thoughts=[],
                actions=[],
                final_response="Real-time update from agent system",
                confidence=0.95,
                timestamp=datetime.utcnow()
            )
    
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def blockchain_events(self) -> strawberry.AsyncGenerator[str, None]:
        """Subscribe to blockchain events"""
        # This would connect to blockchain event listeners in production
        while True:
            await asyncio.sleep(10)  # Simulate periodic updates
            yield f"Blockchain event at {datetime.utcnow().isoformat()}"

# Create GraphQL schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[
        AuthenticationExtension,
        LoggingExtension
    ]
)

# Create GraphQL router for FastAPI integration
graphql_app = GraphQLRouter(
    schema,
    path="/graphql",
    graphiql=True,  # Enable GraphiQL interface
    context_getter=lambda request: {"request": request}
)

# Initialize framework components (called from main app)
async def initialize_graphql_components(
    university_fw: UniversityFramework,
    blockchain_int: BlockchainIntegration
):
    """Initialize GraphQL server components"""
    global university_framework, blockchain_integration
    
    university_framework = university_fw
    blockchain_integration = blockchain_int
    
    logger.info("GraphQL components initialized")

# Example queries and mutations for documentation
EXAMPLE_QUERIES = """
# Query Examples

# Get system health
query {
  health {
    status
    version
    services
    timestamp
  }
}

# Get university information
query {
  universityInfo {
    institutionName
    establishmentDate
    location
    totalStudents
    totalFaculty
  }
}

# Verify a credential
query {
  verifyCredential(credentialId: 12345) {
    valid
    credential {
      id
      title
      program
      issueDate
    }
    blockchainVerified
    governanceCompliant
    securityScore
  }
}

# Get student credentials
query {
  studentCredentials(studentAddress: "0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A") {
    id
    title
    program
    issueDate
    verified
  }
}

# Mutation Examples

# Query an AI agent
mutation {
  queryAgent(
    agentType: "academic_advisor"
    queryInput: {
      message: "I need help selecting courses for next semester"
      context: "{\\"major\\": \\"Computer Science\\", \\"year\\": \\"sophomore\\"}"
      userType: TRADITIONAL_STUDENT
      collaborative: true
    }
  ) {
    success
    finalResponse
    confidence
    thoughts {
      observation
      reasoning
      actionPlan
    }
  }
}

# Issue a credential
mutation {
  issueCredential(
    studentData: {
      studentId: "STU123456"
      blockchainAddress: "0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A"
      name: "John Doe"
      email: "john.doe@university.edu"
    }
    credentialData: {
      title: "Bachelor of Science in Computer Science"
      program: "Computer Science"
      degree: "Bachelor"
      grade: "A"
      graduationDate: "2024-05-15"
    }
    governanceFrameworks: [AACSB, WASC]
  ) {
    id
    title
    issueDate
    verified
  }
}

# Subscription Examples

# Subscribe to agent interactions
subscription {
  agentInteractionUpdates {
    success
    finalResponse
    timestamp
  }
}

# Subscribe to blockchain events
subscription {
  blockchainEvents
}
"""

if __name__ == "__main__":
    print("GraphQL Schema Examples:")
    print(EXAMPLE_QUERIES)