"""
CollegiumAI REST API Server
==========================

Comprehensive REST API server for the CollegiumAI Framework providing
endpoints for AI agents, blockchain operations, governance compliance,
and university management.

Features:
- RESTful API endpoints for all framework components
- JWT-based authentication and authorization
- Rate limiting and request validation
- Comprehensive error handling and logging
- OpenAPI/Swagger documentation
- Health monitoring and metrics
- Multi-tenant support for different institutions
"""

import asyncio
import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import json
import jwt
from functools import wraps

# FastAPI and related imports
from fastapi import FastAPI, HTTPException, Depends, status, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Add the parent directory to the path to import framework components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.core import (
    UniversityFramework, PersonaType, GovernanceFramework,
    ProcessType, UniversityContext, AgentResponse
)
from framework.blockchain.integration import BlockchainIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Pydantic models for request/response validation
class AgentQueryRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="Query message for the agent")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context for the query")
    user_id: Optional[str] = Field(None, description="ID of the user making the query")
    user_type: Optional[PersonaType] = Field(None, description="Type/persona of the user")
    collaborative: bool = Field(True, description="Whether to enable agent collaboration")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "I need help selecting courses for next semester",
                "context": {
                    "major": "Computer Science",
                    "year": "sophomore",
                    "gpa": 3.2
                },
                "user_type": "traditional_student",
                "collaborative": True
            }
        }

class AgentQueryResponse(BaseModel):
    success: bool
    thoughts: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    final_response: str
    confidence: float
    collaborating_agents: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    timestamp: datetime

class CredentialIssuanceRequest(BaseModel):
    student_data: Dict[str, Any] = Field(..., description="Student information including blockchain address")
    credential_data: Dict[str, Any] = Field(..., description="Credential details")
    governance_frameworks: List[str] = Field(..., description="Applicable governance frameworks")
    
    class Config:
        schema_extra = {
            "example": {
                "student_data": {
                    "student_id": "STU123456",
                    "blockchain_address": "0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A",
                    "name": "John Doe",
                    "email": "john.doe@university.edu"
                },
                "credential_data": {
                    "title": "Bachelor of Science in Computer Science",
                    "program": "Computer Science",
                    "degree": "Bachelor",
                    "grade": "A",
                    "graduation_date": "2024-05-15"
                },
                "governance_frameworks": ["aacsb", "wasc"]
            }
        }

class CredentialIssuanceResponse(BaseModel):
    success: bool
    credential_id: int
    transaction_hash: str
    gas_used: str
    governance_compliance: List[str]
    timestamp: datetime

class ComplianceAuditRequest(BaseModel):
    institution: str = Field(..., description="Name of the institution")
    framework: GovernanceFramework = Field(..., description="Governance framework")
    audit_data: Dict[str, Any] = Field(..., description="Audit details")
    
    class Config:
        schema_extra = {
            "example": {
                "institution": "University of Example",
                "framework": "aacsb",
                "audit_data": {
                    "audit_area": "Faculty Qualifications",
                    "status": "compliant",
                    "findings": "All faculty meet minimum qualifications",
                    "recommendations": "Continue current hiring practices",
                    "next_review_date": "2024-12-31"
                }
            }
        }

class ComplianceAuditResponse(BaseModel):
    success: bool
    audit_id: int
    transaction_hash: str
    compliance_status: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, str]
    timestamp: datetime
    uptime_seconds: float

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: int
    timestamp: datetime
    request_id: Optional[str] = None

# Authentication and authorization
class AuthHandler:
    """Handle JWT authentication and authorization"""
    
    secret = os.getenv('JWT_SECRET', 'collegiumai-secret-key-change-in-production')
    algorithm = 'HS256'
    
    def encode_token(self, user_data: Dict[str, Any]) -> str:
        """Encode user data into JWT token"""
        payload = {
            'user_id': user_data.get('user_id'),
            'user_type': user_data.get('user_type'),
            'institution': user_data.get('institution'),
            'permissions': user_data.get('permissions', []),
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode JWT token and return user data"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

auth_handler = AuthHandler()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    return auth_handler.decode_token(token)

def require_permissions(required_permissions: List[str]):
    """Decorator to require specific permissions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user from kwargs (injected by FastAPI)
            user = kwargs.get('current_user')
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_permissions = user.get('permissions', [])
            if not any(perm in user_permissions for perm in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Initialize FastAPI app
app = FastAPI(
    title="CollegiumAI API",
    description="Comprehensive API for AI Multi-Agent Collaborative Framework for Digital Universities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add middleware
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Rate limiting error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Global variables for framework and blockchain integration
university_framework: Optional[UniversityFramework] = None
blockchain_integration: Optional[BlockchainIntegration] = None
app_start_time = datetime.utcnow()

@app.on_event("startup")
async def startup_event():
    """Initialize framework components on startup"""
    global university_framework, blockchain_integration
    
    logger.info("Starting CollegiumAI API Server...")
    
    try:
        # Initialize university framework
        university_context = UniversityContext(
            institution_name="CollegiumAI Demo University",
            accreditations=[],
            student_population=25000,
            academic_programs=["Computer Science", "Engineering", "Business", "Liberal Arts"],
            current_semester="Fall 2025",
            academic_year="2025-2026",
            policies={"academic_integrity": "strict", "attendance": "required"},
            systems={"lms": "active", "grading": "active"}
        )
        
        university_framework = UniversityFramework(university_context)
        logger.info("University framework initialized")
        
        # Initialize blockchain integration
        try:
            blockchain_integration = BlockchainIntegration()
            await blockchain_integration.initialize()
            logger.info("Blockchain integration initialized")
        except Exception as e:
            logger.warning(f"Blockchain integration failed: {e}")
            blockchain_integration = None
        
        logger.info("CollegiumAI API Server started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize framework: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global blockchain_integration
    
    logger.info("Shutting down CollegiumAI API Server...")
    
    if blockchain_integration:
        try:
            await blockchain_integration.close()
            logger.info("Blockchain integration closed")
        except Exception as e:
            logger.error(f"Error closing blockchain integration: {e}")
    
    logger.info("CollegiumAI API Server shut down complete")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            code=exc.status_code,
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            code=500,
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )

# Health and system endpoints
@app.get("/health", response_model=HealthResponse, tags=["System"])
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Check the health status of all services"""
    services = {}
    
    # Check university framework
    if university_framework:
        services["university_framework"] = "operational"
    else:
        services["university_framework"] = "unavailable"
    
    # Check blockchain integration
    if blockchain_integration:
        try:
            status = await blockchain_integration.get_network_status()
            services["blockchain"] = "connected" if status.get("connected") else "disconnected"
        except Exception as e:
            services["blockchain"] = f"error: {str(e)}"
    else:
        services["blockchain"] = "unavailable"
    
    # Calculate uptime
    uptime = (datetime.utcnow() - app_start_time).total_seconds()
    
    return HealthResponse(
        status="healthy" if all(s in ["operational", "connected"] for s in services.values()) else "degraded",
        version="1.0.0",
        services=services,
        timestamp=datetime.utcnow(),
        uptime_seconds=uptime
    )

@app.get("/university/context", tags=["University"])
@limiter.limit("10/minute")
async def get_university_context(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get university context information"""
    if not university_framework:
        raise HTTPException(
            status_code=503,
            detail="University framework not available"
        )
    
    context = university_framework.get_context()
    return {
        "success": True,
        "data": context,
        "timestamp": datetime.utcnow()
    }

# Authentication endpoints
@app.post("/auth/login", tags=["Authentication"])
@limiter.limit("5/minute")
async def login(request: Request, credentials: Dict[str, str]):
    """Authenticate user and return JWT token"""
    # In production, verify credentials against database
    username = credentials.get("username")
    password = credentials.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password required"
        )
    
    # Mock authentication - replace with real authentication
    if username == "admin" and password == "admin":
        user_data = {
            "user_id": "admin",
            "user_type": "administrator",
            "institution": "demo_university",
            "permissions": ["agent_query", "credential_issue", "governance_audit", "admin"]
        }
    elif username == "student" and password == "student":
        user_data = {
            "user_id": "student123",
            "user_type": "traditional_student",
            "institution": "demo_university",
            "permissions": ["agent_query"]
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    token = auth_handler.encode_token(user_data)
    
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user_data": user_data,
        "expires_in": 86400  # 24 hours
    }

# Agent endpoints
@app.post("/api/v1/agents/{agent_type}/query", response_model=AgentQueryResponse, tags=["Agents"])
@limiter.limit("20/minute")
async def query_agent(
    agent_type: str,
    request_data: AgentQueryRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Send a query to a specific agent"""
    if not university_framework:
        raise HTTPException(
            status_code=503,
            detail="University framework not available"
        )
    
    # Check permissions
    if "agent_query" not in current_user.get("permissions", []):
        raise HTTPException(
            status_code=403,
            detail="Agent query permission required"
        )
    
    try:
        # Get the appropriate agent
        if agent_type == "academic_advisor":
            from framework.agents.academic_advisor import AcademicAdvisorAgent
            agent = AcademicAdvisorAgent("academic_advisor", university_framework)
        elif agent_type == "student_services":
            from framework.agents.student_services import StudentServicesAgent
            agent = StudentServicesAgent("student_services", university_framework)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown agent type: {agent_type}"
            )
        
        # Process the query
        response = await agent.process_query(
            message=request_data.message,
            context=request_data.context,
            user_id=request_data.user_id or current_user.get("user_id"),
            user_type=request_data.user_type or PersonaType(current_user.get("user_type", "traditional_student")),
            collaborative=request_data.collaborative
        )
        
        # Log the interaction (background task)
        background_tasks.add_task(
            log_agent_interaction,
            agent_type,
            current_user.get("user_id"),
            request_data.message,
            response
        )
        
        return AgentQueryResponse(
            success=True,
            thoughts=response.thoughts,
            actions=response.actions,
            final_response=response.final_response,
            confidence=response.confidence,
            collaborating_agents=response.collaborating_agents,
            recommendations=response.recommendations,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error processing agent query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent query failed: {str(e)}"
        )

@app.get("/api/v1/agents/{agent_type}/info", tags=["Agents"])
@limiter.limit("30/minute")
async def get_agent_info(
    agent_type: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get information about a specific agent"""
    agent_info = {
        "academic_advisor": {
            "name": "Academic Advisor Agent",
            "description": "Provides academic guidance, course selection, and degree planning assistance",
            "capabilities": [
                "Course recommendation",
                "Degree planning",
                "Academic policy guidance",
                "GPA analysis",
                "Graduation requirements checking"
            ],
            "supported_personas": [persona.value for persona in PersonaType if "student" in persona.value.lower()]
        },
        "student_services": {
            "name": "Student Services Agent",
            "description": "Coordinates student support services and campus resources",
            "capabilities": [
                "Tutoring service coordination",
                "Mental health support",
                "Career counseling",
                "Financial aid guidance",
                "Accessibility services"
            ],
            "supported_personas": [persona.value for persona in PersonaType]
        }
    }
    
    if agent_type not in agent_info:
        raise HTTPException(
            status_code=404,
            detail=f"Agent type '{agent_type}' not found"
        )
    
    return {
        "success": True,
        "data": agent_info[agent_type],
        "timestamp": datetime.utcnow()
    }

# Blockchain endpoints
@app.post("/api/v1/blockchain/credentials/issue", response_model=CredentialIssuanceResponse, tags=["Blockchain"])
@limiter.limit("10/minute")
async def issue_credential(
    request_data: CredentialIssuanceRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Issue a new academic credential on the blockchain"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    # Check permissions
    if "credential_issue" not in current_user.get("permissions", []):
        raise HTTPException(
            status_code=403,
            detail="Credential issuance permission required"
        )
    
    try:
        result = await blockchain_integration.issue_credential(
            request_data.student_data,
            request_data.credential_data,
            request_data.governance_frameworks
        )
        
        return CredentialIssuanceResponse(
            success=True,
            credential_id=result["credential_id"],
            transaction_hash=result["transaction_hash"],
            gas_used=result["gas_used"],
            governance_compliance=request_data.governance_frameworks,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error issuing credential: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Credential issuance failed: {str(e)}"
        )

@app.get("/api/v1/blockchain/credentials/{credential_id}/verify", tags=["Blockchain"])
@limiter.limit("30/minute")
async def verify_credential(
    credential_id: int,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Verify a credential on the blockchain"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        verification_result = await blockchain_integration.verify_credential(credential_id)
        
        return {
            "success": True,
            "data": verification_result,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error verifying credential: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Credential verification failed: {str(e)}"
        )

@app.get("/api/v1/blockchain/students/{student_address}/credentials", tags=["Blockchain"])
@limiter.limit("20/minute")
async def get_student_credentials(
    student_address: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all credentials for a student"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        credentials = await blockchain_integration.get_student_credentials(student_address)
        
        return {
            "success": True,
            "data": credentials,
            "count": len(credentials),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting student credentials: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get student credentials: {str(e)}"
        )

@app.get("/api/v1/blockchain/status", tags=["Blockchain"])
@limiter.limit("60/minute")
async def get_blockchain_status(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get blockchain network status"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        status = await blockchain_integration.get_network_status()
        
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting blockchain status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get blockchain status: {str(e)}"
        )

# Bologna Process Models
class BolognaComplianceRequest(BaseModel):
    """Request model for setting Bologna Process compliance"""
    credential_id: int = Field(..., description="ID of the credential")
    ects_credits: int = Field(..., ge=1, description="ECTS credits (minimum 1)")
    eqf_level: int = Field(..., ge=1, le=8, description="EQF level between 1-8")
    diploma_supplement_issued: bool = Field(..., description="Whether diploma supplement is issued")
    learning_outcomes: List[str] = Field(..., description="List of learning outcome descriptions")
    quality_assurance_agency: str = Field(..., description="Quality assurance agency name")
    joint_degree_program: bool = Field(default=False, description="Whether this is a joint degree program")
    mobility_partners: List[str] = Field(default_factory=list, description="List of mobility partner institutions")

class BolognaComplianceResponse(BaseModel):
    """Response model for Bologna Process compliance"""
    success: bool
    transaction_hash: str
    gas_used: str
    timestamp: datetime

class BolognaDataResponse(BaseModel):
    """Response model for Bologna Process data"""
    success: bool
    data: Dict[str, Any]
    timestamp: datetime

class ECTSUpdateRequest(BaseModel):
    """Request model for updating ECTS credits"""
    credential_id: int = Field(..., description="ID of the credential")
    new_ects_credits: int = Field(..., ge=1, description="New ECTS credit value")

# Bologna Process Endpoints
@app.post("/api/v1/blockchain/credentials/bologna/compliance", response_model=BolognaComplianceResponse, tags=["Bologna Process"])
@limiter.limit("10/minute")
async def set_bologna_compliance(
    request_data: BolognaComplianceRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Set Bologna Process compliance data for a credential"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        # Call blockchain integration
        result = await blockchain_integration.set_bologna_compliance(
            credential_id=request_data.credential_id,
            ects_credits=request_data.ects_credits,
            eqf_level=request_data.eqf_level,
            diploma_supplement_issued=request_data.diploma_supplement_issued,
            learning_outcomes=request_data.learning_outcomes,
            quality_assurance_agency=request_data.quality_assurance_agency,
            joint_degree_program=request_data.joint_degree_program,
            mobility_partners=request_data.mobility_partners
        )
        
        return BolognaComplianceResponse(
            success=True,
            transaction_hash=result.get('transaction_hash', ''),
            gas_used=result.get('gas_used', '0'),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error setting Bologna compliance: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set Bologna compliance: {str(e)}"
        )

@app.get("/api/v1/blockchain/credentials/{credential_id}/bologna", response_model=BolognaDataResponse, tags=["Bologna Process"])
@limiter.limit("30/minute")
async def get_bologna_compliance(
    credential_id: int,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get Bologna Process compliance data for a credential"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        data = await blockchain_integration.get_bologna_compliance(credential_id)
        
        return BolognaDataResponse(
            success=True,
            data=data,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error getting Bologna compliance: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get Bologna compliance: {str(e)}"
        )

@app.put("/api/v1/blockchain/credentials/ects", response_model=BolognaComplianceResponse, tags=["Bologna Process"])
@limiter.limit("10/minute")
async def update_ects_credits(
    request_data: ECTSUpdateRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update ECTS credits for a credential"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        result = await blockchain_integration.update_ects_credits(
            credential_id=request_data.credential_id,
            new_ects_credits=request_data.new_ects_credits
        )
        
        return BolognaComplianceResponse(
            success=True,
            transaction_hash=result.get('transaction_hash', ''),
            gas_used=result.get('gas_used', '0'),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error updating ECTS credits: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update ECTS credits: {str(e)}"
        )

@app.get("/api/v1/blockchain/credentials/{credential_id}/auto-recognition", response_model=BolognaDataResponse, tags=["Bologna Process"])
@limiter.limit("30/minute")
async def check_automatic_recognition_eligibility(
    credential_id: int,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Check if credential qualifies for automatic recognition under Bologna Process"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        eligible = await blockchain_integration.is_eligible_for_automatic_recognition(credential_id)
        
        return BolognaDataResponse(
            success=True,
            data={
                "eligible": eligible,
                "credential_id": credential_id
            },
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error checking automatic recognition eligibility: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check automatic recognition eligibility: {str(e)}"
        )

@app.get("/api/v1/blockchain/students/{student_address}/ects-total", response_model=BolognaDataResponse, tags=["Bologna Process"])
@limiter.limit("30/minute")
async def get_student_total_ects(
    student_address: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get total ECTS credits for a student"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        total_ects = await blockchain_integration.get_student_total_ects(student_address)
        
        return BolognaDataResponse(
            success=True,
            data={
                "total_ects": total_ects,
                "student_address": student_address
            },
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error getting student total ECTS: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get student total ECTS: {str(e)}"
        )

@app.get("/api/v1/blockchain/credentials/{credential_id}/bologna/compliance-check", response_model=BolognaDataResponse, tags=["Bologna Process"])
@limiter.limit("30/minute")
async def check_bologna_compliance_status(
    credential_id: int,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Check Bologna Process framework compliance for credential"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    try:
        compliance_data = await blockchain_integration.check_bologna_compliance(credential_id)
        
        return BolognaDataResponse(
            success=True,
            data=compliance_data,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error checking Bologna compliance status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check Bologna compliance status: {str(e)}"
        )

# Governance endpoints
@app.post("/api/v1/governance/audits", response_model=ComplianceAuditResponse, tags=["Governance"])
@limiter.limit("5/minute")
async def create_compliance_audit(
    request_data: ComplianceAuditRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a compliance audit"""
    if not blockchain_integration:
        raise HTTPException(
            status_code=503,
            detail="Blockchain integration not available"
        )
    
    # Check permissions
    if "governance_audit" not in current_user.get("permissions", []):
        raise HTTPException(
            status_code=403,
            detail="Governance audit permission required"
        )
    
    try:
        result = await blockchain_integration.create_compliance_audit(
            request_data.institution,
            request_data.framework.value,
            request_data.audit_data
        )
        
        return ComplianceAuditResponse(
            success=True,
            audit_id=result["audit_id"],
            transaction_hash=result["transaction_hash"],
            compliance_status=request_data.audit_data.get("status", "unknown"),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error creating compliance audit: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Compliance audit creation failed: {str(e)}"
        )

@app.get("/api/v1/governance/compliance/{institution}/{framework}", tags=["Governance"])
@limiter.limit("30/minute")
async def get_compliance_status(
    institution: str,
    framework: GovernanceFramework,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get compliance status for an institution and framework"""
    try:
        # In a real implementation, this would query the blockchain
        compliance_status = {
            "institution": institution,
            "framework": framework.value,
            "overall_status": "compliant",
            "last_audit_date": datetime.utcnow() - timedelta(days=90),
            "next_audit_date": datetime.utcnow() + timedelta(days=275),
            "areas": [
                {
                    "area": "Faculty Qualifications",
                    "status": "compliant",
                    "last_reviewed": datetime.utcnow() - timedelta(days=30)
                },
                {
                    "area": "Curriculum Standards",
                    "status": "compliant", 
                    "last_reviewed": datetime.utcnow() - timedelta(days=60)
                }
            ]
        }
        
        return {
            "success": True,
            "data": compliance_status,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting compliance status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get compliance status: {str(e)}"
        )

# Background tasks
async def log_agent_interaction(
    agent_type: str,
    user_id: str,
    message: str,
    response: AgentResponse
):
    """Log agent interaction for analytics and monitoring"""
    try:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_type": agent_type,
            "user_id": user_id,
            "message_length": len(message),
            "response_confidence": response.confidence,
            "collaborating_agents": response.collaborating_agents,
            "processing_time": 0  # Would be calculated in real implementation
        }
        
        # In production, save to database or analytics service
        logger.info(f"Agent interaction logged: {json.dumps(log_data)}")
        
    except Exception as e:
        logger.error(f"Error logging agent interaction: {e}")

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="CollegiumAI API",
        version="1.0.0",
        description="""
        Comprehensive API for AI Multi-Agent Collaborative Framework for Digital Universities
        
        ## Features
        - AI Agent Interactions (Academic Advisor, Student Services)
        - Blockchain Credential Management 
        - Governance Compliance Tracking
        - Multi-tenant University Support
        - JWT Authentication & Authorization
        - Rate Limiting & Security
        
        ## Authentication
        Use the `/auth/login` endpoint to get a JWT token, then include it in the Authorization header:
        `Authorization: Bearer <your-token>`
        
        ## Rate Limits
        Most endpoints have rate limits to prevent abuse. See individual endpoint documentation for specific limits.
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Main entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='CollegiumAI REST API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=4000, help='Port to bind to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    parser.add_argument('--log-level', default='info', choices=['debug', 'info', 'warning', 'error'], help='Log level')
    
    args = parser.parse_args()
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level
    )