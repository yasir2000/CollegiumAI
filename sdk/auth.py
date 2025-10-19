"""
Authentication Client for CollegiumAI SDK
Handles JWT, MFA, RBAC, and user management
"""

import hashlib
import secrets
import qrcode
from io import BytesIO
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pyotp
import jwt

class AuthClient:
    """Client for authentication and authorization operations"""
    
    def __init__(self, client):
        self.client = client
    
    # User Authentication
    async def login(self, username: str, password: str, mfa_token: str = None) -> Dict[str, Any]:
        """
        Authenticate user with username/password and optional MFA
        
        Args:
            username: User's username or email
            password: User's password
            mfa_token: Optional TOTP token for MFA
            
        Returns:
            Authentication response with tokens and user info
        """
        login_data = {
            'username': username,
            'password': password
        }
        
        if mfa_token:
            login_data['mfa_token'] = mfa_token
        
        return await self.client.post('/auth/login', data=login_data)
    
    async def logout(self, token: str = None) -> Dict[str, Any]:
        """
        Logout user and invalidate tokens
        
        Args:
            token: Optional token to invalidate (uses current session if not provided)
        """
        logout_data = {}
        if token:
            logout_data['token'] = token
        
        return await self.client.post('/auth/logout', data=logout_data)
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token and refresh token
        """
        return await self.client.post('/auth/refresh', data={'refresh_token': refresh_token})
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify if a JWT token is valid
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token verification result with user info
        """
        return await self.client.post('/auth/verify', data={'token': token})
    
    # User Management
    async def register_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str = 'student',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            username: Unique username
            email: User's email address
            password: User's password
            first_name: User's first name
            last_name: User's last name
            role: User's role (student, faculty, staff, admin)
            **kwargs: Additional user attributes
        """
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            **kwargs
        }
        
        return await self.client.post('/auth/register', data=user_data)
    
    async def get_user_profile(self, user_id: str = None) -> Dict[str, Any]:
        """
        Get user profile information
        
        Args:
            user_id: User ID (current user if not specified)
        """
        endpoint = '/auth/profile'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.get(endpoint)
    
    async def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            user_id: User ID to update
            updates: Dictionary of fields to update
        """
        return await self.client.put(f'/auth/profile/{user_id}', data=updates)
    
    async def change_password(
        self,
        current_password: str,
        new_password: str,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Change user password
        
        Args:
            current_password: Current password
            new_password: New password
            user_id: User ID (current user if not specified)
        """
        password_data = {
            'current_password': current_password,
            'new_password': new_password
        }
        
        endpoint = '/auth/change-password'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.post(endpoint, data=password_data)
    
    # Multi-Factor Authentication (MFA)
    async def setup_mfa(self, user_id: str = None) -> Dict[str, Any]:
        """
        Setup MFA for user
        
        Args:
            user_id: User ID (current user if not specified)
            
        Returns:
            MFA setup information including QR code
        """
        endpoint = '/auth/mfa/setup'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.post(endpoint)
    
    async def verify_mfa_setup(
        self,
        secret: str,
        token: str,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Verify MFA setup with TOTP token
        
        Args:
            secret: MFA secret from setup
            token: TOTP token from authenticator app
            user_id: User ID (current user if not specified)
        """
        mfa_data = {
            'secret': secret,
            'token': token
        }
        
        endpoint = '/auth/mfa/verify-setup'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.post(endpoint, data=mfa_data)
    
    async def disable_mfa(self, user_id: str = None) -> Dict[str, Any]:
        """
        Disable MFA for user
        
        Args:
            user_id: User ID (current user if not specified)
        """
        endpoint = '/auth/mfa/disable'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.post(endpoint)
    
    async def generate_backup_codes(self, user_id: str = None) -> Dict[str, Any]:
        """
        Generate MFA backup codes
        
        Args:
            user_id: User ID (current user if not specified)
        """
        endpoint = '/auth/mfa/backup-codes'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.post(endpoint)
    
    # Role-Based Access Control (RBAC)
    async def get_user_roles(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all roles assigned to a user"""
        return await self.client.get(f'/auth/users/{user_id}/roles')
    
    async def assign_role(self, user_id: str, role_name: str) -> Dict[str, Any]:
        """Assign a role to a user"""
        return await self.client.post(f'/auth/users/{user_id}/roles', data={'role': role_name})
    
    async def remove_role(self, user_id: str, role_name: str) -> Dict[str, Any]:
        """Remove a role from a user"""
        return await self.client.delete(f'/auth/users/{user_id}/roles/{role_name}')
    
    async def create_role(
        self,
        name: str,
        description: str,
        permissions: List[str]
    ) -> Dict[str, Any]:
        """
        Create a new role
        
        Args:
            name: Role name
            description: Role description
            permissions: List of permission names
        """
        role_data = {
            'name': name,
            'description': description,
            'permissions': permissions
        }
        
        return await self.client.post('/auth/roles', data=role_data)
    
    async def get_roles(self) -> List[Dict[str, Any]]:
        """Get all available roles"""
        return await self.client.get('/auth/roles')
    
    async def get_role(self, role_name: str) -> Dict[str, Any]:
        """Get specific role details"""
        return await self.client.get(f'/auth/roles/{role_name}')
    
    async def update_role(
        self,
        role_name: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update role information"""
        return await self.client.put(f'/auth/roles/{role_name}', data=updates)
    
    async def delete_role(self, role_name: str) -> Dict[str, Any]:
        """Delete a role"""
        return await self.client.delete(f'/auth/roles/{role_name}')
    
    # Permissions
    async def get_permissions(self) -> List[Dict[str, Any]]:
        """Get all available permissions"""
        return await self.client.get('/auth/permissions')
    
    async def check_permission(self, user_id: str, permission: str) -> Dict[str, Any]:
        """Check if user has specific permission"""
        return await self.client.get(
            f'/auth/users/{user_id}/permissions/{permission}'
        )
    
    async def get_user_permissions(self, user_id: str) -> List[str]:
        """Get all permissions for a user"""
        response = await self.client.get(f'/auth/users/{user_id}/permissions')
        return response.get('permissions', [])
    
    # Session Management
    async def get_active_sessions(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get active sessions for user"""
        endpoint = '/auth/sessions'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.get(endpoint)
    
    async def terminate_session(self, session_id: str) -> Dict[str, Any]:
        """Terminate a specific session"""
        return await self.client.delete(f'/auth/sessions/{session_id}')
    
    async def terminate_all_sessions(self, user_id: str = None) -> Dict[str, Any]:
        """Terminate all sessions for user"""
        endpoint = '/auth/sessions/terminate-all'
        if user_id:
            endpoint += f'/{user_id}'
        
        return await self.client.post(endpoint)
    
    # Audit and Security
    async def get_audit_logs(
        self,
        user_id: str = None,
        action_type: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get authentication audit logs
        
        Args:
            user_id: Filter by user ID
            action_type: Filter by action type (login, logout, etc.)
            start_date: Start date for logs
            end_date: End date for logs
            limit: Maximum number of logs to return
        """
        params = {'limit': limit}
        
        if user_id:
            params['user_id'] = user_id
        if action_type:
            params['action_type'] = action_type
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        return await self.client.get('/auth/audit-logs', params=params)
    
    async def get_security_events(
        self,
        event_type: str = None,
        severity: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get security events"""
        params = {'limit': limit}
        
        if event_type:
            params['event_type'] = event_type
        if severity:
            params['severity'] = severity
        
        return await self.client.get('/auth/security-events', params=params)
    
    # Password Security
    async def check_password_strength(self, password: str) -> Dict[str, Any]:
        """Check password strength and compliance"""
        return await self.client.post('/auth/password/check-strength', data={'password': password})
    
    async def get_password_policy(self) -> Dict[str, Any]:
        """Get current password policy"""
        return await self.client.get('/auth/password/policy')
    
    async def update_password_policy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Update password policy (admin only)"""
        return await self.client.put('/auth/password/policy', data=policy)
    
    # Account Security
    async def enable_account_lockout(
        self,
        user_id: str,
        reason: str,
        duration: int = None
    ) -> Dict[str, Any]:
        """
        Lock user account
        
        Args:
            user_id: User ID to lock
            reason: Reason for lockout
            duration: Lockout duration in minutes (permanent if not specified)
        """
        lockout_data = {
            'reason': reason
        }
        
        if duration:
            lockout_data['duration'] = duration
        
        return await self.client.post(f'/auth/users/{user_id}/lockout', data=lockout_data)
    
    async def disable_account_lockout(self, user_id: str) -> Dict[str, Any]:
        """Unlock user account"""
        return await self.client.delete(f'/auth/users/{user_id}/lockout')
    
    async def get_account_status(self, user_id: str) -> Dict[str, Any]:
        """Get account status and security information"""
        return await self.client.get(f'/auth/users/{user_id}/status')
    
    # Utility methods for client-side operations
    def generate_secure_password(self, length: int = 16) -> str:
        """Generate a cryptographically secure password"""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt (client-side utility)"""
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash (client-side utility)"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_totp_qr_code(self, secret: str, user_email: str, issuer: str = "CollegiumAI") -> str:
        """
        Generate TOTP QR code for authenticator apps
        
        Returns:
            Base64 encoded QR code image
        """
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    def verify_totp_token(self, secret: str, token: str) -> bool:
        """Verify TOTP token (client-side utility)"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)