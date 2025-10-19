# CollegiumAI SDK - Enhanced Version
"""
CollegiumAI Enhanced SDK - Python Client Library

A comprehensive SDK for integrating with the CollegiumAI enterprise platform.
Provides access to all advanced features including authentication, AI agents,
blockchain credentials, and real-time monitoring.

Quick Start:
    from collegiumai_sdk import CollegiumAIClient
    
    client = CollegiumAIClient(api_url="http://localhost:4000")
    await client.authenticate("username", "password")
    
    # Use AI agents
    response = await client.agents.chat("research_assistant", "Help with my thesis")
    
    # Access database  
    users = await client.database.get_users()
    
    # Blockchain credentials
    credential = await client.blockchain.issue_credential(user_id, data)
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import aiohttp

__version__ = "2.0.0"
__author__ = "CollegiumAI Team"

logger = logging.getLogger(__name__)

@dataclass
class SDKConfig:
    """Enhanced SDK Configuration"""
    api_base_url: str = "http://localhost:4000"
    api_key: Optional[str] = None
    jwt_token: Optional[str] = None
    timeout: int = 30

class APIException(Exception):
    """Custom exception for API errors"""
    pass

class BaseClient:
    """Base client with common HTTP functionality"""
    
    def __init__(self, config: SDKConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {"Content-Type": "application/json"}
        
    async def _ensure_session(self):
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request with error handling"""
        await self._ensure_session()
        url = f"{self.config.api_base_url}{endpoint}"
        
        if self.config.jwt_token:
            self.headers["Authorization"] = f"Bearer {self.config.jwt_token}"
            
        try:
            async with self.session.request(method, url, headers=self.headers, **kwargs) as response:
                if response.content_type == 'application/json':
                    return await response.json()
                else:
                    return {"response": await response.text()}
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise APIException(f"Request failed: {str(e)}")

class AuthClient(BaseClient):
    """Authentication and Authorization Client"""
    
    async def authenticate(self, username: str, password: str) -> dict:
        """Authenticate user with username/password"""
        data = {"username": username, "password": password}
        response = await self._request("POST", "/auth/login", json=data)
        
        if "access_token" in response:
            self.config.jwt_token = response["access_token"]
            logger.info("Authentication successful")
        return response
    
    async def setup_mfa(self, user_id: int) -> dict:
        """Setup Multi-Factor Authentication"""
        return await self._request("POST", f"/auth/mfa/setup/{user_id}")

class AgentsClient(BaseClient):
    """Multi-Agent System Client"""
    
    async def list_agents(self) -> List[dict]:
        """Get list of available agents"""
        response = await self._request("GET", "/agents")
        return response.get("agents", [])
    
    async def chat(self, agent_type: str, message: str, context: dict = None) -> dict:
        """Chat with a specific agent"""
        data = {
            "agent_type": agent_type,
            "message": message,
            "context": context or {}
        }
        return await self._request("POST", "/agents/chat", json=data)

class DatabaseClient(BaseClient):
    """Database Operations Client"""
    
    async def get_users(self, limit: int = 100) -> List[dict]:
        """Get users from database"""
        params = {"limit": limit}
        response = await self._request("GET", "/database/users", params=params)
        return response.get("users", [])
    
    async def create_user(self, user_data: dict) -> dict:
        """Create new user"""
        return await self._request("POST", "/database/users", json=user_data)

class BlockchainClient(BaseClient):
    """Blockchain Credentials Client"""
    
    async def issue_credential(self, user_id: int, credential_data: dict) -> dict:
        """Issue blockchain credential"""
        data = {"user_id": user_id, "credential_data": credential_data}
        return await self._request("POST", "/blockchain/credentials/issue", json=data)
    
    async def verify_credential(self, credential_id: str) -> dict:
        """Verify blockchain credential"""
        return await self._request("GET", f"/blockchain/credentials/verify/{credential_id}")

class BolognaClient(BaseClient):
    """Bologna Process Compliance Client"""
    
    async def validate_ects(self, course_data: dict) -> dict:
        """Validate ECTS credits"""
        return await self._request("POST", "/bologna/ects/validate", json=course_data)

class VisualizationClient(BaseClient):
    """Multi-Agent Visualization Client"""
    
    async def get_network_topology(self) -> dict:
        """Get current network topology"""
        return await self._request("GET", "/visualization/network")

class CognitiveClient(BaseClient):
    """Cognitive Insights Client"""
    
    async def get_memory_analysis(self, agent_id: str) -> dict:
        """Get cognitive memory analysis"""
        return await self._request("GET", f"/cognitive/memory/{agent_id}")

class CollegiumAIClient:
    """
    Main CollegiumAI SDK Client
    
    Provides unified access to all CollegiumAI services including:
    - Authentication & Authorization
    - Multi-Agent AI System  
    - Database Operations
    - Blockchain Credentials
    - Bologna Process Compliance
    - Real-time Visualization
    - Cognitive Insights
    """
    
    def __init__(self, api_url: str = "http://localhost:4000", **kwargs):
        """Initialize CollegiumAI client"""
        self.config = SDKConfig(api_base_url=api_url, **kwargs)
        
        # Initialize all service clients
        self.auth = AuthClient(self.config)
        self.agents = AgentsClient(self.config)
        self.database = DatabaseClient(self.config)
        self.blockchain = BlockchainClient(self.config)
        self.bologna = BolognaClient(self.config)
        self.visualization = VisualizationClient(self.config)
        self.cognitive = CognitiveClient(self.config)
        
        logger.info(f"CollegiumAI SDK v{__version__} initialized")
    
    async def authenticate(self, username: str, password: str) -> dict:
        """Quick authentication method"""
        return await self.auth.authenticate(username, password)
    
    async def health_check(self) -> dict:
        """Check API health status"""
        try:
            return await self.auth._request("GET", "/health")
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def close(self):
        """Close all connections"""
        for client in [self.auth, self.agents, self.database, self.blockchain, 
                      self.bologna, self.visualization, self.cognitive]:
            if hasattr(client, 'session') and client.session:
                await client.session.close()

# Convenience functions
async def quick_chat(message: str, agent_type: str = "general_assistant", 
                    api_url: str = "http://localhost:4000") -> str:
    """Quick chat function for simple use cases"""
    client = CollegiumAIClient(api_url)
    try:
        response = await client.agents.chat(agent_type, message)
        return response.get("response", "")
    finally:
        await client.close()

# Export main classes
__all__ = [
    "CollegiumAIClient",
    "SDKConfig", 
    "AuthClient",
    "AgentsClient",
    "DatabaseClient",
    "BlockchainClient",
    "BolognaClient", 
    "VisualizationClient",
    "CognitiveClient",
    "quick_chat"
]
