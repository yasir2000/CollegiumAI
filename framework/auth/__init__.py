"""
CollegiumAI Authentication & Authorization Package
=================================================

Advanced authentication and authorization system providing:
- JWT token management with refresh tokens
- Role-based access control (RBAC)
- Multi-factor authentication (MFA)
- Session management
- FastAPI integration with middleware
- Security utilities and rate limiting
- Audit logging for security events
"""

from .authentication import (
    AuthenticationService, AuthConfig, PasswordValidator, MFAManager,
    JWTManager, SessionManager, AuthenticationError, AuthorizationError,
    get_auth_service, PermissionChecker, require_authentication, require_permissions
)

from .fastapi_integration import (
    AuthenticationMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware,
    get_current_user, get_optional_user, require_permissions as require_permissions_dep,
    require_all_permissions, require_persona_types, AuthenticatedUser,
    LoginRequest, LoginResponse, RegisterRequest, ChangePasswordRequest,
    MFASetupResponse, MFAConfirmRequest, RefreshTokenRequest,
    AuthenticationRoutes, create_auth_routes, setup_auth_middleware
)

# Re-export for convenience
__all__ = [
    # Core authentication
    'AuthenticationService',
    'AuthConfig',
    'PasswordValidator',
    'MFAManager',
    'JWTManager',
    'SessionManager',
    'get_auth_service',
    
    # Exceptions
    'AuthenticationError',
    'AuthorizationError',
    
    # Permissions
    'PermissionChecker',
    'require_authentication',
    'require_permissions',
    
    # FastAPI integration
    'AuthenticationMiddleware',
    'RateLimitMiddleware', 
    'SecurityHeadersMiddleware',
    'get_current_user',
    'get_optional_user',
    'require_permissions_dep',
    'require_all_permissions',
    'require_persona_types',
    'AuthenticatedUser',
    
    # Pydantic models
    'LoginRequest',
    'LoginResponse',
    'RegisterRequest',
    'ChangePasswordRequest',
    'MFASetupResponse',
    'MFAConfirmRequest',
    'RefreshTokenRequest',
    
    # Route handlers
    'AuthenticationRoutes',
    'create_auth_routes',
    'setup_auth_middleware'
]

# Version info
__version__ = '1.0.0'
__author__ = 'CollegiumAI Team'