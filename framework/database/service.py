"""
Database Service Layer for CollegiumAI
=====================================

Provides high-level database operations and connection management
for the CollegiumAI platform with PostgreSQL backend.
"""

import os
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager
import asyncpg
import json
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration settings"""
    
    def __init__(self):
        # Default to environment variables or local development settings
        self.database_url = os.getenv(
            'DATABASE_URL', 
            'postgresql://collegiumai:password@localhost:5432/collegiumai'
        )
        self.min_pool_size = int(os.getenv('DB_MIN_POOL_SIZE', '5'))
        self.max_pool_size = int(os.getenv('DB_MAX_POOL_SIZE', '20'))
        self.command_timeout = int(os.getenv('DB_COMMAND_TIMEOUT', '60'))
        self.pool_recycle = int(os.getenv('DB_POOL_RECYCLE', '3600'))  # 1 hour
        
        # Parse database URL for components
        parsed = urlparse(self.database_url)
        self.host = parsed.hostname or 'localhost'
        self.port = parsed.port or 5432
        self.database = parsed.path.lstrip('/') or 'collegiumai'
        self.username = parsed.username or 'collegiumai'
        self.password = parsed.password or 'password'
        
    def get_connection_params(self) -> Dict[str, Any]:
        """Get connection parameters for asyncpg"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.username,
            'password': self.password,
            'command_timeout': self.command_timeout,
            'min_size': self.min_pool_size,
            'max_size': self.max_pool_size,
        }

class DatabaseService:
    """
    Advanced database service providing high-level operations
    for CollegiumAI with connection pooling and transaction management
    """
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self.pool: Optional[asyncpg.Pool] = None
        self._initialized = False
        
    async def initialize(self) -> bool:
        """Initialize database connection pool"""
        try:
            logger.info("Initializing database connection pool...")
            self.pool = await asyncpg.create_pool(**self.config.get_connection_params())
            
            # Test connection
            async with self.pool.acquire() as conn:
                await conn.execute('SELECT 1')
                
            self._initialized = True
            logger.info(f"Database pool initialized successfully with {self.config.max_pool_size} max connections")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            return False
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self._initialized = False
            logger.info("Database pool closed")
    
    @asynccontextmanager
    async def transaction(self):
        """Database transaction context manager"""
        if not self._initialized:
            raise RuntimeError("Database service not initialized")
            
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query and return status"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Fetch multiple rows as dictionaries"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def fetchrow(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Fetch single row as dictionary"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    
    async def fetchval(self, query: str, *args) -> Any:
        """Fetch single value"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    # User Management Methods
    async def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        persona_type: str,
        institution_id: str,
        **kwargs
    ) -> str:
        """Create a new user and return user ID"""
        query = """
            INSERT INTO users (
                username, email, password_hash, first_name, last_name,
                persona_type, institution_id, student_id, employee_id,
                blockchain_address, profile_data, preferences
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id
        """
        user_id = await self.fetchval(
            query, username, email, password_hash, first_name, last_name,
            persona_type, institution_id, kwargs.get('student_id'),
            kwargs.get('employee_id'), kwargs.get('blockchain_address'),
            json.dumps(kwargs.get('profile_data', {})),
            json.dumps(kwargs.get('preferences', {}))
        )
        return str(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email address"""
        query = """
            SELECT u.*, i.name as institution_name, d.name as department_name
            FROM users u
            LEFT JOIN institutions i ON u.institution_id = i.id
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.email = $1 AND u.is_active = true
        """
        return await self.fetchrow(query, email)
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        query = """
            SELECT u.*, i.name as institution_name, d.name as department_name
            FROM users u
            LEFT JOIN institutions i ON u.institution_id = i.id
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = $1 AND u.is_active = true
        """
        return await self.fetchrow(query, user_id)
    
    async def update_user_login(self, user_id: str, ip_address: str = None):
        """Update user's last login timestamp"""
        query = "UPDATE users SET last_login = $1 WHERE id = $2"
        await self.execute(query, datetime.utcnow(), user_id)
    
    async def get_user_permissions(self, user_id: str) -> List[str]:
        """Get user's permissions (both direct and via roles)"""
        query = """
            SELECT DISTINCT p.name
            FROM permissions p
            WHERE p.id IN (
                -- Direct permissions
                SELECT permission_id FROM user_permissions WHERE user_id = $1
                UNION
                -- Role-based permissions
                SELECT rp.permission_id 
                FROM role_permissions rp
                JOIN user_roles ur ON rp.role_id = ur.role_id
                WHERE ur.user_id = $1
            )
        """
        rows = await self.fetch(query, user_id)
        return [row['name'] for row in rows]

    # Session Management
    async def create_session(
        self,
        session_id: str,
        user_id: str,
        session_data: Dict[str, Any] = None,
        expires_in_hours: int = 24,
        ip_address: str = None,
        user_agent: str = None
    ) -> str:
        """Create a new user session"""
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        
        query = """
            INSERT INTO user_sessions (
                session_id, user_id, session_data, expires_at, ip_address, user_agent
            ) VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
        """
        
        session_uuid = await self.fetchval(
            query, session_id, user_id, json.dumps(session_data or {}),
            expires_at, ip_address, user_agent
        )
        return str(session_uuid)
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by session ID"""
        query = """
            SELECT s.*, u.username, u.email, u.persona_type
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_id = $1 AND s.is_active = true AND s.expires_at > $2
        """
        return await self.fetchrow(query, session_id, datetime.utcnow())
    
    async def update_session(self, session_id: str, session_data: Dict[str, Any]):
        """Update session data"""
        query = """
            UPDATE user_sessions 
            SET session_data = $1, updated_at = $2
            WHERE session_id = $3
        """
        await self.execute(query, json.dumps(session_data), datetime.utcnow(), session_id)
    
    async def expire_session(self, session_id: str):
        """Mark session as inactive"""
        query = "UPDATE user_sessions SET is_active = false WHERE session_id = $1"
        await self.execute(query, session_id)

    # Blockchain Credential Management
    async def store_credential(
        self,
        credential_id: int,
        transaction_hash: str,
        student_id: str,
        institution_id: str,
        credential_data: Dict[str, Any]
    ) -> str:
        """Store blockchain credential information"""
        query = """
            INSERT INTO blockchain_credentials (
                credential_id, transaction_hash, student_id, institution_id,
                title, program, degree_level, grade, issuer_address,
                issue_date, completion_date, credits, ipfs_hash,
                document_urls, bologna_data, metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
            RETURNING id
        """
        
        cred_uuid = await self.fetchval(
            query,
            credential_id, transaction_hash, student_id, institution_id,
            credential_data['title'], credential_data['program'],
            credential_data['degree_level'], credential_data.get('grade'),
            credential_data['issuer_address'],
            credential_data.get('issue_date', datetime.utcnow()),
            credential_data.get('completion_date'),
            credential_data.get('credits'),
            credential_data.get('ipfs_hash'),
            json.dumps(credential_data.get('document_urls', [])),
            json.dumps(credential_data.get('bologna_data', {})),
            json.dumps(credential_data.get('metadata', {}))
        )
        return str(cred_uuid)
    
    async def get_user_credentials(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all credentials for a user"""
        query = """
            SELECT c.*, i.name as institution_name
            FROM blockchain_credentials c
            JOIN institutions i ON c.institution_id = i.id
            WHERE c.student_id = $1
            ORDER BY c.issue_date DESC
        """
        return await self.fetch(query, user_id)
    
    async def verify_credential(
        self,
        credential_id: str,
        verifier_id: str = None,
        verification_data: Dict[str, Any] = None
    ) -> str:
        """Log credential verification"""
        query = """
            INSERT INTO credential_verification_logs (
                credential_id, verifier_id, verification_type, is_valid,
                verification_data, blockchain_verified, governance_compliant, ipfs_accessible
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """
        
        log_id = await self.fetchval(
            query,
            credential_id, verifier_id, verification_data.get('verification_type', 'automatic'),
            verification_data.get('is_valid', False), json.dumps(verification_data or {}),
            verification_data.get('blockchain_verified', False),
            verification_data.get('governance_compliant', False),
            verification_data.get('ipfs_accessible', False)
        )
        return str(log_id)

    # Agent Management
    async def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        name: str,
        description: str = None,
        specialization: str = None,
        capabilities: List[str] = None,
        configuration: Dict[str, Any] = None
    ) -> str:
        """Register a new agent"""
        query = """
            INSERT INTO agents (
                agent_id, agent_type, name, description, specialization,
                capabilities, configuration
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        """
        
        uuid = await self.fetchval(
            query, agent_id, agent_type, name, description, specialization,
            json.dumps(capabilities or []), json.dumps(configuration or {})
        )
        return str(uuid)
    
    async def update_agent_status(self, agent_id: str, status: str):
        """Update agent status"""
        query = """
            UPDATE agents 
            SET status = $1, last_active = $2, updated_at = $2
            WHERE agent_id = $3
        """
        await self.execute(query, status, datetime.utcnow(), agent_id)
    
    async def log_agent_task(
        self,
        task_id: str,
        agent_id: str,
        task_type: str,
        description: str,
        input_data: Dict[str, Any],
        priority: int = 5
    ) -> str:
        """Log a new agent task"""
        # Get agent UUID
        agent_uuid = await self.fetchval(
            "SELECT id FROM agents WHERE agent_id = $1", agent_id
        )
        
        if not agent_uuid:
            raise ValueError(f"Agent {agent_id} not found")
        
        query = """
            INSERT INTO agent_tasks (
                task_id, agent_id, task_type, description, input_data, priority
            ) VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
        """
        
        task_uuid = await self.fetchval(
            query, task_id, agent_uuid, task_type, description,
            json.dumps(input_data), priority
        )
        return str(task_uuid)
    
    async def complete_agent_task(
        self,
        task_id: str,
        output_data: Dict[str, Any],
        success: bool = True,
        processing_time: float = None,
        confidence_score: float = None,
        error_message: str = None
    ):
        """Mark agent task as completed"""
        query = """
            UPDATE agent_tasks 
            SET status = 'completed', completed_at = $1, output_data = $2,
                success = $3, processing_time = $4, confidence_score = $5,
                error_message = $6
            WHERE task_id = $7
        """
        await self.execute(
            query, datetime.utcnow(), json.dumps(output_data), success,
            processing_time, confidence_score, error_message, task_id
        )
    
    async def log_agent_interaction(
        self,
        agent_id: str,
        user_id: str,
        query: str,
        response: str,
        thoughts: List[Dict[str, Any]] = None,
        actions: List[Dict[str, Any]] = None,
        confidence: float = None,
        processing_time: float = None,
        context_data: Dict[str, Any] = None,
        session_id: str = None
    ) -> str:
        """Log agent-user interaction"""
        # Get agent UUID
        agent_uuid = await self.fetchval(
            "SELECT id FROM agents WHERE agent_id = $1", agent_id
        )
        
        if not agent_uuid:
            raise ValueError(f"Agent {agent_id} not found")
        
        query_sql = """
            INSERT INTO agent_interactions (
                agent_id, user_id, session_id, interaction_type, query, response,
                thoughts, actions, confidence, processing_time, context_data
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id
        """
        
        interaction_id = await self.fetchval(
            query_sql, agent_uuid, user_id, session_id, 'chat', query, response,
            json.dumps(thoughts or []), json.dumps(actions or []),
            confidence, processing_time, json.dumps(context_data or {})
        )
        return str(interaction_id)

    # Cognitive Architecture Support
    async def store_memory(
        self,
        persona_id: str,
        memory_type: str,
        content: Dict[str, Any],
        importance_score: float = 0.0,
        confidence: float = 1.0,
        context_tags: List[str] = None,
        retention_hours: int = None
    ) -> str:
        """Store cognitive memory"""
        retention_until = None
        if retention_hours:
            retention_until = datetime.utcnow() + timedelta(hours=retention_hours)
        
        query = """
            INSERT INTO cognitive_memories (
                persona_id, memory_type, content, importance_score, confidence,
                context_tags, retention_until
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        """
        
        memory_id = await self.fetchval(
            query, persona_id, memory_type, json.dumps(content),
            importance_score, confidence, context_tags or [], retention_until
        )
        return str(memory_id)
    
    async def retrieve_memories(
        self,
        persona_id: str,
        memory_type: str = None,
        limit: int = 100,
        min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Retrieve cognitive memories"""
        conditions = ["persona_id = $1", "importance_score >= $2"]
        params = [persona_id, min_importance]
        
        if memory_type:
            conditions.append("memory_type = $3")
            params.append(memory_type)
        
        query = f"""
            SELECT * FROM cognitive_memories
            WHERE {' AND '.join(conditions)}
                AND (retention_until IS NULL OR retention_until > NOW())
            ORDER BY importance_score DESC, created_at DESC
            LIMIT ${len(params) + 1}
        """
        params.append(limit)
        
        return await self.fetch(query, *params)
    
    async def log_learning_event(
        self,
        persona_id: str,
        learning_type: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        improvement_score: float = None
    ) -> str:
        """Log cognitive learning event"""
        query = """
            INSERT INTO cognitive_learning (
                persona_id, learning_type, input_data, output_data, improvement_score
            ) VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """
        
        learning_id = await self.fetchval(
            query, persona_id, learning_type, json.dumps(input_data),
            json.dumps(output_data), improvement_score
        )
        return str(learning_id)

    # Bologna Process Support
    async def store_bologna_compliance(
        self,
        credential_id: str,
        ects_credits: int,
        eqf_level: int,
        compliance_data: Dict[str, Any]
    ) -> str:
        """Store Bologna Process compliance data"""
        query = """
            INSERT INTO bologna_process_compliance (
                credential_id, ects_credits, eqf_level, diploma_supplement_issued,
                quality_assurance_agency, joint_degree_program, learning_outcomes,
                competencies, mobility_partners, recognition_status, compliance_metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id
        """
        
        compliance_id = await self.fetchval(
            query, credential_id, ects_credits, eqf_level,
            compliance_data.get('diploma_supplement_issued', False),
            compliance_data.get('quality_assurance_agency'),
            compliance_data.get('joint_degree_program', False),
            json.dumps(compliance_data.get('learning_outcomes', [])),
            json.dumps(compliance_data.get('competencies', [])),
            json.dumps(compliance_data.get('mobility_partners', [])),
            compliance_data.get('recognition_status', 'under_review'),
            json.dumps(compliance_data.get('metadata', {}))
        )
        return str(compliance_id)

    # Analytics and Monitoring
    async def log_system_metric(
        self,
        metric_name: str,
        metric_value: float,
        metric_category: str = 'general',
        component: str = None,
        metadata: Dict[str, Any] = None,
        tags: List[str] = None
    ):
        """Log system metric"""
        query = """
            INSERT INTO system_metrics (
                metric_name, metric_value, metric_category, component, metadata, tags
            ) VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self.execute(
            query, metric_name, metric_value, metric_category, component,
            json.dumps(metadata or {}), tags or []
        )
    
    async def get_system_metrics(
        self,
        metric_name: str = None,
        category: str = None,
        hours_back: int = 24
    ) -> List[Dict[str, Any]]:
        """Get system metrics"""
        conditions = ["recorded_at >= $1"]
        params = [datetime.utcnow() - timedelta(hours=hours_back)]
        
        if metric_name:
            conditions.append("metric_name = $2")
            params.append(metric_name)
        
        if category:
            conditions.append("metric_category = $" + str(len(params) + 1))
            params.append(category)
        
        query = f"""
            SELECT * FROM system_metrics
            WHERE {' AND '.join(conditions)}
            ORDER BY recorded_at DESC
        """
        
        return await self.fetch(query, *params)
    
    async def log_audit_event(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str = None,
        success: bool = True,
        old_values: Dict[str, Any] = None,
        new_values: Dict[str, Any] = None,
        ip_address: str = None,
        user_agent: str = None,
        metadata: Dict[str, Any] = None
    ):
        """Log audit event"""
        query = """
            INSERT INTO audit_logs (
                user_id, action, resource_type, resource_id, success,
                old_values, new_values, ip_address, user_agent, metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """
        await self.execute(
            query, user_id, action, resource_type, resource_id, success,
            json.dumps(old_values) if old_values else None,
            json.dumps(new_values) if new_values else None,
            ip_address, user_agent, json.dumps(metadata or {})
        )

    # Health and Status
    async def health_check(self) -> Dict[str, Any]:
        """Perform database health check"""
        try:
            # Basic connectivity test
            start_time = datetime.utcnow()
            await self.fetchval("SELECT 1")
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Pool status
            pool_stats = {
                'size': self.pool.get_size(),
                'min_size': self.pool.get_min_size(),
                'max_size': self.pool.get_max_size(),
                'idle_size': self.pool.get_idle_size(),
            }
            
            # Recent metrics
            recent_errors = await self.fetchval(
                "SELECT COUNT(*) FROM audit_logs WHERE success = false AND created_at >= $1",
                datetime.utcnow() - timedelta(hours=1)
            )
            
            return {
                'status': 'healthy',
                'response_time_ms': response_time * 1000,
                'pool_stats': pool_stats,
                'recent_errors': recent_errors,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

# Global database service instance
_database_service: Optional[DatabaseService] = None

async def get_database_service() -> DatabaseService:
    """Get or create the global database service instance"""
    global _database_service
    if _database_service is None:
        _database_service = DatabaseService()
        await _database_service.initialize()
    return _database_service

async def close_database_service():
    """Close the global database service"""
    global _database_service
    if _database_service:
        await _database_service.close()
        _database_service = None