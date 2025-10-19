"""
FastAPI Authentication Integration for CollegiumAI
=================================================

FastAPI-specific authentication middleware, dependencies, and security
configurations for the CollegiumAI platform.
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
import jwt

from .authentication import (
    get_auth_service, AuthenticationService, AuthenticationError, 
    AuthorizationError, PermissionChecker
)

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class LoginRequest(BaseModel):
    email: str
    password: str
    mfa_token: Optional[str] = None

class LoginResponse(BaseModel):
    success: bool
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_data: Dict[str, Any]

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    persona_type: str
    institution_id: str
    student_id: Optional[str] = None
    employee_id: Optional[str] = None
    blockchain_address: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class MFASetupResponse(BaseModel):
    secret: str
    qr_code: str
    backup_codes: Optional[List[str]] = None

class MFAConfirmRequest(BaseModel):
    token: str

class AuthenticatedUser(BaseModel):
    """Represents an authenticated user in the system"""
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    persona_type: str
    institution_id: str
    permissions: List[str]
    roles: List[str]
    session_id: str
    is_verified: bool
    mfa_enabled: bool

# FastAPI Security
security = HTTPBearer()

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for FastAPI"""
    
    def __init__(self, app, auth_service: AuthenticationService = None):
        super().__init__(app)
        self.auth_service = auth_service or get_auth_service()
        
        # Public endpoints that don't require authentication
        self.public_endpoints = {
            "/docs", "/redoc", "/openapi.json", "/health",
            "/auth/login", "/auth/register", "/auth/refresh"
        }
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public endpoints
        if any(request.url.path.startswith(endpoint) for endpoint in self.public_endpoints):
            return await call_next(request)
        
        # Get authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content="Authentication required",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        try:
            # Extract and verify token
            token = auth_header.split(" ")[1]
            payload = await self.auth_service.verify_token(token)
            
            # Add user info to request state
            request.state.user = payload
            request.state.authenticated = True
            
        except AuthenticationError as e:
            return Response(
                content=f"Authentication failed: {str(e)}",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception as e:
            logger.error(f"Authentication middleware error: {e}")
            return Response(
                content="Authentication error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return await call_next(request)

# Dependency functions
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AuthenticatedUser:
    """Get current authenticated user"""
    auth_service = get_auth_service()
    
    try:
        # Verify token
        payload = await auth_service.verify_token(credentials.credentials)
        
        # Create authenticated user object
        return AuthenticatedUser(
            id=payload['user_id'],
            username=payload['username'],
            email=payload['email'],
            first_name=payload.get('first_name', ''),
            last_name=payload.get('last_name', ''),
            persona_type=payload['persona_type'],
            institution_id=payload['institution_id'],
            permissions=payload.get('permissions', []),
            roles=payload.get('roles', []),
            session_id=payload['session_id'],
            is_verified=payload.get('is_verified', False),
            mfa_enabled=payload.get('mfa_enabled', False)
        )
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[AuthenticatedUser]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

def require_permissions(required_permissions: List[str]):
    """Dependency factory for requiring specific permissions"""
    async def permission_dependency(
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> AuthenticatedUser:
        if not PermissionChecker.has_any_permission(current_user.permissions, required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {', '.join(required_permissions)}"
            )
        return current_user
    
    return permission_dependency

def require_all_permissions(required_permissions: List[str]):
    """Dependency factory for requiring all specified permissions"""
    async def permission_dependency(
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> AuthenticatedUser:
        if not PermissionChecker.has_all_permissions(current_user.permissions, required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {', '.join(required_permissions)}"
            )
        return current_user
    
    return permission_dependency

def require_persona_types(allowed_types: List[str]):
    """Dependency factory for requiring specific persona types"""
    async def persona_dependency(
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> AuthenticatedUser:
        if current_user.persona_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed persona types: {', '.join(allowed_types)}"
            )
        return current_user
    
    return persona_dependency

# Route handlers for authentication endpoints
class AuthenticationRoutes:
    """Authentication route handlers"""
    
    def __init__(self, auth_service: AuthenticationService = None):
        self.auth_service = auth_service or get_auth_service()
    
    async def login(self, request: LoginRequest, req: Request) -> LoginResponse:
        """User login endpoint"""
        try:
            # Get client info
            ip_address = req.client.host if req.client else None
            user_agent = req.headers.get("user-agent")
            
            # Authenticate user
            access_token, refresh_token, user_data = await self.auth_service.authenticate_user(
                email=request.email,
                password=request.password,
                mfa_token=request.mfa_token,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            logger.info(f"User login successful: {request.email}")
            
            return LoginResponse(
                success=True,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=self.auth_service.config.access_token_expire_minutes * 60,
                user_data=user_data
            )
            
        except AuthenticationError as e:
            logger.warning(f"Login failed for {request.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Login error for {request.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed"
            )
    
    async def refresh_token(self, request: RefreshTokenRequest) -> Dict[str, Any]:
        """Refresh access token"""
        try:
            new_access_token = await self.auth_service.refresh_access_token(request.refresh_token)
            
            return {
                "success": True,
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": self.auth_service.config.access_token_expire_minutes * 60
            }
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
    
    async def register(self, request: RegisterRequest) -> Dict[str, Any]:
        """User registration endpoint"""
        try:
            user_id, warnings = await self.auth_service.register_user(
                username=request.username,
                email=request.email,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name,
                persona_type=request.persona_type,
                institution_id=request.institution_id,
                student_id=request.student_id,
                employee_id=request.employee_id,
                blockchain_address=request.blockchain_address
            )
            
            logger.info(f"User registered successfully: {request.email}")
            
            return {
                "success": True,
                "user_id": user_id,
                "message": "User registered successfully",
                "warnings": warnings
            }
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def logout(
        self, 
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """User logout endpoint"""
        try:
            await self.auth_service.logout(current_user.session_id)
            
            return {
                "success": True,
                "message": "Logout successful"
            }
            
        except Exception as e:
            logger.error(f"Logout error for user {current_user.id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Logout failed"
            )
    
    async def change_password(
        self,
        request: ChangePasswordRequest,
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Change password endpoint"""
        try:
            await self.auth_service.change_password(
                user_id=current_user.id,
                current_password=request.current_password,
                new_password=request.new_password
            )
            
            return {
                "success": True,
                "message": "Password changed successfully"
            }
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def setup_mfa(
        self,
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> MFASetupResponse:
        """Setup MFA endpoint"""
        try:
            secret, qr_code = await self.auth_service.setup_mfa(current_user.id)
            
            return MFASetupResponse(
                secret=secret,
                qr_code=qr_code
            )
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def confirm_mfa(
        self,
        request: MFAConfirmRequest,
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Confirm MFA setup endpoint"""
        try:
            backup_codes = await self.auth_service.confirm_mfa_setup(
                user_id=current_user.id,
                token=request.token
            )
            
            return {
                "success": True,
                "message": "MFA enabled successfully",
                "backup_codes": backup_codes
            }
            
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def get_profile(
        self,
        current_user: AuthenticatedUser = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get user profile endpoint"""
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "persona_type": current_user.persona_type,
            "institution_id": current_user.institution_id,
            "permissions": current_user.permissions,
            "roles": current_user.roles,
            "is_verified": current_user.is_verified,
            "mfa_enabled": current_user.mfa_enabled
        }

# Helper functions for FastAPI setup
def create_auth_routes(auth_service: AuthenticationService = None):
    """Create authentication routes for FastAPI"""
    return AuthenticationRoutes(auth_service)

def setup_auth_middleware(app, auth_service: AuthenticationService = None):
    """Setup authentication middleware for FastAPI app"""
    app.add_middleware(AuthenticationMiddleware, auth_service=auth_service)

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.utcnow()
        minute = now.replace(second=0, microsecond=0)
        
        # Clean old entries
        self.request_counts = {
            key: count for key, count in self.request_counts.items()
            if key[1] == minute
        }
        
        # Check rate limit
        key = (client_ip, minute)
        current_count = self.request_counts.get(key, 0)
        
        if current_count >= self.requests_per_minute:
            return Response(
                content="Rate limit exceeded",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Increment counter
        self.request_counts[key] = current_count + 1
        
        return await call_next(request)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Security headers middleware"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response