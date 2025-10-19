"""
CollegiumAI SDK - Enhanced Python Client Library
Enterprise-grade SDK for integrating with the CollegiumAI Framework
"""

import asyncio
import aiohttp
import logging
import json
import uuid
import time
from typing import Dict, List, Any, Optional, Union, Callable, AsyncGenerator
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import websockets
from urllib.parse import urljoin
import jwt
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

class AuthenticationMethod(Enum):
    """Authentication methods supported by the SDK"""
    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    OAUTH2 = "oauth2"
    BASIC_AUTH = "basic_auth"

class ConnectionMode(Enum):
    """Connection modes for different deployment scenarios"""
    LOCAL = "local"
    CLOUD = "cloud"
    ENTERPRISE = "enterprise"
    DEVELOPMENT = "development"

@dataclass
class SDKConfig:
    """Comprehensive SDK configuration"""
    # API Configuration
    api_base_url: str = "http://localhost:4000"
    websocket_url: str = "ws://localhost:4000"
    api_version: str = "v1"
    
    # Authentication
    auth_method: AuthenticationMethod = AuthenticationMethod.API_KEY
    api_key: Optional[str] = None
    jwt_token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    
    # Connection Settings
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    connection_mode: ConnectionMode = ConnectionMode.LOCAL
    
    # Feature Flags
    blockchain_enabled: bool = True
    multi_agent_enabled: bool = True
    cognitive_insights_enabled: bool = True
    real_time_updates: bool = True
    
    # Performance Settings
    connection_pool_size: int = 10
    max_concurrent_requests: int = 100
    cache_enabled: bool = True
    cache_ttl: int = 300
    
    # Debugging and Monitoring
    debug: bool = False
    enable_metrics: bool = True
    log_level: str = "INFO"

class CollegiumAIError(Exception):
    """Base exception for CollegiumAI SDK"""
    pass

class AuthenticationError(CollegiumAIError):
    """Authentication related errors"""
    pass

class APIError(CollegiumAIError):
    """API related errors"""
    def __init__(self, message: str, status_code: int = None, response_data: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class NetworkError(CollegiumAIError):
    """Network related errors"""
    pass

class CollegiumAIClient:
    """
    Enhanced main client class for CollegiumAI Framework
    
    Features:
    - Multiple authentication methods
    - Connection pooling and retry logic
    - Real-time WebSocket communication
    - Comprehensive error handling
    - Performance monitoring
    - Caching capabilities
    """
    
    def __init__(self, config: SDKConfig = None):
        self.config = config or SDKConfig()
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        
        # Sub-clients
        self._auth = None
        self._agents = None
        self._database = None
        self._blockchain = None
        self._bologna = None
        self._visualization = None
        self._cognitive = None
        
        # Internal state
        self._is_initialized = False
        self._connection_pool = None
        self._metrics = {
            'requests_sent': 0,
            'requests_failed': 0,
            'average_response_time': 0.0,
            'last_activity': None
        }
        self._cache = {}
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging based on config"""
        level = getattr(logging, self.config.log_level.upper())
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        if self.config.debug:
            logger.setLevel(logging.DEBUG)
    
    async def __aenter__(self):
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def initialize(self):
        """Initialize the client with enhanced features"""
        if self._is_initialized:
            return
        
        try:
            # Setup HTTP session with connection pooling
            connector = aiohttp.TCPConnector(
                limit=self.config.connection_pool_size,
                limit_per_host=self.config.max_concurrent_requests,
                ttl_dns_cache=300,
                use_dns_cache=True
            )
            
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            
            # Setup headers
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'CollegiumAI-SDK/2.0',
                'Accept': 'application/json'
            }
            
            # Add authentication headers
            await self._setup_authentication(headers)
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                headers=headers,
                timeout=timeout
            )
            
            # Initialize sub-clients
            await self._initialize_subclients()
            
            # Setup WebSocket connection if enabled
            if self.config.real_time_updates:
                await self._setup_websocket()
            
            # Verify connection
            await self._verify_connection()
            
            self._is_initialized = True
            logger.info("CollegiumAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise CollegiumAIError(f"Initialization failed: {e}")
    
    async def _setup_authentication(self, headers: Dict[str, str]):
        """Setup authentication based on method"""
        if self.config.auth_method == AuthenticationMethod.API_KEY:
            if self.config.api_key:
                headers['X-API-Key'] = self.config.api_key
        elif self.config.auth_method == AuthenticationMethod.JWT_TOKEN:
            if self.config.jwt_token:
                headers['Authorization'] = f'Bearer {self.config.jwt_token}'
        elif self.config.auth_method == AuthenticationMethod.BASIC_AUTH:
            if self.config.username and self.config.password:
                import base64
                credentials = base64.b64encode(
                    f"{self.config.username}:{self.config.password}".encode()
                ).decode()
                headers['Authorization'] = f'Basic {credentials}'
    
    async def _initialize_subclients(self):
        """Initialize all sub-clients"""
        from .auth import AuthClient
        from .agents import AgentClient
        from .database import DatabaseClient
        from .blockchain import BlockchainClient
        from .bologna import BolognaClient
        from .visualization import VisualizationClient
        from .cognitive import CognitiveClient
        
        self._auth = AuthClient(self)
        self._agents = AgentClient(self)
        self._database = DatabaseClient(self)
        self._blockchain = BlockchainClient(self)
        self._bologna = BolognaClient(self)
        self._visualization = VisualizationClient(self)
        self._cognitive = CognitiveClient(self)
    
    async def _setup_websocket(self):
        """Setup WebSocket connection for real-time updates"""
        try:
            ws_url = self.config.websocket_url.replace('http', 'ws')
            self.websocket = await websockets.connect(f"{ws_url}/ws")
            logger.info("WebSocket connection established")
        except Exception as e:
            logger.warning(f"Failed to establish WebSocket: {e}")
    
    async def _verify_connection(self):
        """Verify the connection to CollegiumAI services"""
        try:
            health_data = await self.health_check()
            if health_data.get('status') == 'healthy':
                logger.info("Connection verified successfully")
            else:
                raise CollegiumAIError("Service not healthy")
        except Exception as e:
            raise NetworkError(f"Connection verification failed: {e}")
    
    async def close(self):
        """Close all connections and cleanup resources"""
        if self.websocket:
            await self.websocket.close()
        
        if self.session:
            await self.session.close()
        
        self._is_initialized = False
        logger.info("CollegiumAI client closed")
    
    # Properties for accessing sub-clients
    @property
    def auth(self):
        """Access authentication operations"""
        if not self._auth:
            raise RuntimeError("Client not initialized")
        return self._auth
    
    @property
    def agents(self):
        """Access AI agent operations"""
        if not self._agents:
            raise RuntimeError("Client not initialized")
        return self._agents
    
    @property
    def database(self):
        """Access database operations"""
        if not self._database:
            raise RuntimeError("Client not initialized")
        return self._database
    
    @property
    def blockchain(self):
        """Access blockchain operations"""
        if not self._blockchain:
            raise RuntimeError("Client not initialized")
        return self._blockchain
    
    @property
    def bologna(self):
        """Access Bologna Process operations"""
        if not self._bologna:
            raise RuntimeError("Client not initialized")
        return self._bologna
    
    @property
    def visualization(self):
        """Access visualization operations"""
        if not self._visualization:
            raise RuntimeError("Client not initialized")
        return self._visualization
    
    @property
    def cognitive(self):
        """Access cognitive insights operations"""
        if not self._cognitive:
            raise RuntimeError("Client not initialized")
        return self._cognitive
    
    # Core HTTP methods with enhanced error handling and retry logic
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Any = None,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic and error handling"""
        if not self._is_initialized:
            raise RuntimeError("Client not initialized")
        
        url = urljoin(f"{self.config.api_base_url}/api/{self.config.api_version}/", endpoint.lstrip('/'))
        
        # Update metrics
        self._metrics['requests_sent'] += 1
        self._metrics['last_activity'] = datetime.now()
        
        start_time = time.time()
        
        try:
            # Check cache for GET requests
            if method == 'GET' and self.config.cache_enabled:
                cache_key = f"{url}_{json.dumps(params or {})}"
                if cache_key in self._cache:
                    cache_entry = self._cache[cache_key]
                    if datetime.now() - cache_entry['timestamp'] < timedelta(seconds=self.config.cache_ttl):
                        return cache_entry['data']
            
            # Prepare request
            kwargs = {
                'url': url,
                'params': params,
                'headers': headers
            }
            
            if data is not None:
                if isinstance(data, dict):
                    kwargs['json'] = data
                else:
                    kwargs['data'] = data
            
            # Make request
            async with self.session.request(method, **kwargs) as response:
                response_time = time.time() - start_time
                self._update_response_time(response_time)
                
                if response.status >= 400:
                    error_data = None
                    try:
                        error_data = await response.json()
                    except:
                        error_data = await response.text()
                    
                    if response.status == 401:
                        raise AuthenticationError(f"Authentication failed: {error_data}")
                    elif response.status >= 500 and retry_count < self.config.max_retries:
                        await asyncio.sleep(self.config.retry_delay * (retry_count + 1))
                        return await self._make_request(method, endpoint, data, params, headers, retry_count + 1)
                    else:
                        raise APIError(f"API error: {error_data}", response.status, error_data)
                
                try:
                    result = await response.json()
                except:
                    result = await response.text()
                
                # Cache successful GET responses
                if method == 'GET' and self.config.cache_enabled and response.status == 200:
                    cache_key = f"{url}_{json.dumps(params or {})}"
                    self._cache[cache_key] = {
                        'data': result,
                        'timestamp': datetime.now()
                    }
                
                return result
                
        except Exception as e:
            self._metrics['requests_failed'] += 1
            if retry_count < self.config.max_retries and not isinstance(e, AuthenticationError):
                await asyncio.sleep(self.config.retry_delay * (retry_count + 1))
                return await self._make_request(method, endpoint, data, params, headers, retry_count + 1)
            raise
    
    def _update_response_time(self, response_time: float):
        """Update average response time metric"""
        if self._metrics['average_response_time'] == 0:
            self._metrics['average_response_time'] = response_time
        else:
            self._metrics['average_response_time'] = (
                self._metrics['average_response_time'] * 0.9 + response_time * 0.1
            )
    
    async def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make GET request"""
        return await self._make_request('GET', endpoint, params=params, **kwargs)
    
    async def post(self, endpoint: str, data: Any = None, **kwargs) -> Dict[str, Any]:
        """Make POST request"""
        return await self._make_request('POST', endpoint, data=data, **kwargs)
    
    async def put(self, endpoint: str, data: Any = None, **kwargs) -> Dict[str, Any]:
        """Make PUT request"""
        return await self._make_request('PUT', endpoint, data=data, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request"""
        return await self._make_request('DELETE', endpoint, **kwargs)
    
    # Core API methods
    async def health_check(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        return await self.get('/health')
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get client metrics"""
        return {
            'client_metrics': self._metrics,
            'config': {
                'api_base_url': self.config.api_base_url,
                'connection_mode': self.config.connection_mode.value,
                'features_enabled': {
                    'blockchain': self.config.blockchain_enabled,
                    'multi_agent': self.config.multi_agent_enabled,
                    'cognitive_insights': self.config.cognitive_insights_enabled,
                    'real_time': self.config.real_time_updates
                }
            }
        }
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        return await self.get('/system/info')
    
    # Real-time communication
    async def subscribe_to_updates(self, event_types: List[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Subscribe to real-time updates via WebSocket"""
        if not self.websocket:
            raise RuntimeError("WebSocket not connected")
        
        # Send subscription message
        subscription_msg = {
            'type': 'subscribe',
            'event_types': event_types or ['all']
        }
        await self.websocket.send(json.dumps(subscription_msg))
        
        # Yield incoming messages
        async for message in self.websocket:
            try:
                data = json.loads(message)
                yield data
            except json.JSONDecodeError:
                logger.warning(f"Received invalid JSON: {message}")
    
    # Batch operations
    async def batch_request(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple requests in batch"""
        return await self.post('/batch', data={'requests': requests})
    
    # Configuration management
    def update_config(self, **kwargs):
        """Update client configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                logger.warning(f"Unknown config key: {key}")
    
    # Context managers for different connection modes
    @classmethod
    async def development(cls, **kwargs):
        """Create client configured for development"""
        config = SDKConfig(
            connection_mode=ConnectionMode.DEVELOPMENT,
            debug=True,
            log_level="DEBUG",
            **kwargs
        )
        return cls(config)
    
    @classmethod
    async def production(cls, **kwargs):
        """Create client configured for production"""
        config = SDKConfig(
            connection_mode=ConnectionMode.ENTERPRISE,
            debug=False,
            log_level="INFO",
            cache_enabled=True,
            enable_metrics=True,
            **kwargs
        )
        return cls(config)

# Convenience functions
async def create_client(
    api_url: str = "http://localhost:4000",
    api_key: str = None,
    **kwargs
) -> CollegiumAIClient:
    """Create and initialize a CollegiumAI client"""
    config = SDKConfig(
        api_base_url=api_url,
        api_key=api_key,
        **kwargs
    )
    client = CollegiumAIClient(config)
    await client.initialize()
    return client

# Export main classes
__all__ = [
    'CollegiumAIClient',
    'SDKConfig',
    'AuthenticationMethod',
    'ConnectionMode',
    'CollegiumAIError',
    'AuthenticationError',
    'APIError',
    'NetworkError',
    'create_client'
]