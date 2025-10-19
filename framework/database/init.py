"""
Database Initialization and Migration System
==========================================

Handles database schema creation, migrations, and initial data seeding
for the CollegiumAI platform.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import os
import json
from pathlib import Path

from .service import DatabaseService, DatabaseConfig

logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """Handles database initialization and schema setup"""
    
    def __init__(self, database_service: DatabaseService):
        self.db = database_service
        self.script_dir = Path(__file__).parent / "migrations"
        
    async def initialize_database(self, force_recreate: bool = False) -> bool:
        """Initialize the complete database schema and seed data"""
        try:
            logger.info("Starting database initialization...")
            
            # Check if database is already initialized
            if not force_recreate:
                is_initialized = await self._check_if_initialized()
                if is_initialized:
                    logger.info("Database already initialized")
                    return True
            
            # Create schemas
            await self._create_schemas()
            
            # Create tables
            await self._create_tables()
            
            # Create indexes
            await self._create_indexes()
            
            # Create functions and triggers
            await self._create_functions()
            
            # Seed initial data
            await self._seed_initial_data()
            
            # Mark as initialized
            await self._mark_initialized()
            
            logger.info("Database initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False
    
    async def _check_if_initialized(self) -> bool:
        """Check if database has been initialized"""
        try:
            result = await self.db.fetchval(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users'"
            )
            return result > 0
        except:
            return False
    
    async def _create_schemas(self):
        """Create database schemas"""
        schemas = [
            "CREATE SCHEMA IF NOT EXISTS cognitive",
            "CREATE SCHEMA IF NOT EXISTS agents", 
            "CREATE SCHEMA IF NOT EXISTS analytics",
            "CREATE SCHEMA IF NOT EXISTS bologna"
        ]
        
        for schema_sql in schemas:
            await self.db.execute(schema_sql)
            logger.debug(f"Created schema: {schema_sql}")
    
    async def _create_tables(self):
        """Create all database tables"""
        
        # Extensions first
        await self.db.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        await self.db.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')
        
        # Core tables
        await self._create_core_tables()
        await self._create_auth_tables()
        await self._create_blockchain_tables()
        await self._create_agent_tables()
        await self._create_cognitive_tables()
        await self._create_bologna_tables()
        await self._create_analytics_tables()
    
    async def _create_core_tables(self):
        """Create core institutional tables"""
        
        # Institutions table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS institutions (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                short_name VARCHAR(50) NOT NULL,
                type VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL,
                city VARCHAR(100) NOT NULL,
                address TEXT,
                website VARCHAR(255),
                email VARCHAR(255),
                blockchain_address VARCHAR(42) UNIQUE,
                accreditation_data JSONB DEFAULT '{}',
                bologna_process_member BOOLEAN DEFAULT false,
                settings JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # Departments table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                code VARCHAR(20) NOT NULL,
                institution_id UUID NOT NULL REFERENCES institutions(id),
                description TEXT,
                head_of_department_id UUID,
                settings JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(institution_id, code)
            )
        """)
        
        # Add foreign key for head of department after users table is created
        # We'll do this in a separate step
    
    async def _create_auth_tables(self):
        """Create authentication and authorization tables"""
        
        # Users table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                student_id VARCHAR(50) UNIQUE,
                employee_id VARCHAR(50) UNIQUE,
                is_active BOOLEAN DEFAULT true,
                is_verified BOOLEAN DEFAULT false,
                persona_type VARCHAR(50) NOT NULL,
                blockchain_address VARCHAR(42) UNIQUE,
                institution_id UUID REFERENCES institutions(id),
                department_id UUID REFERENCES departments(id),
                profile_data JSONB DEFAULT '{}',
                preferences JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                last_login TIMESTAMP WITH TIME ZONE
            )
        """)
        
        # Roles table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                is_system BOOLEAN DEFAULT false,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # Permissions table
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS permissions (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                resource VARCHAR(100) NOT NULL,
                action VARCHAR(100) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # User roles association
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS user_roles (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(user_id, role_id)
            )
        """)
        
        # Role permissions association
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS role_permissions (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(role_id, permission_id)
            )
        """)
        
        # User permissions (direct permissions)
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS user_permissions (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(user_id, permission_id)
            )
        """)
        
        # User sessions
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                session_id VARCHAR(255) UNIQUE NOT NULL,
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                session_data JSONB DEFAULT '{}',
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                is_active BOOLEAN DEFAULT true
            )
        """)
    
    async def _create_blockchain_tables(self):
        """Create blockchain and credential tables"""
        
        # Governance frameworks
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS governance_frameworks (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                description TEXT,
                region VARCHAR(100),
                framework_type VARCHAR(100) NOT NULL,
                requirements JSONB DEFAULT '{}',
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # Blockchain credentials
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS blockchain_credentials (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                credential_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                program VARCHAR(255) NOT NULL,
                degree_level VARCHAR(100) NOT NULL,
                grade VARCHAR(10),
                student_id UUID NOT NULL REFERENCES users(id),
                institution_id UUID NOT NULL REFERENCES institutions(id),
                issuer_address VARCHAR(42) NOT NULL,
                transaction_hash VARCHAR(66) NOT NULL,
                block_number INTEGER,
                gas_used VARCHAR(50),
                ipfs_hash VARCHAR(255),
                document_urls JSONB DEFAULT '[]',
                status VARCHAR(50) DEFAULT 'issued',
                is_verified BOOLEAN DEFAULT false,
                verification_date TIMESTAMP WITH TIME ZONE,
                issue_date TIMESTAMP WITH TIME ZONE NOT NULL,
                completion_date TIMESTAMP WITH TIME ZONE,
                credits INTEGER,
                bologna_data JSONB DEFAULT '{}',
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(credential_id, transaction_hash)
            )
        """)
        
        # Credential frameworks association
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS credential_frameworks (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                credential_id UUID NOT NULL REFERENCES blockchain_credentials(id) ON DELETE CASCADE,
                framework_id UUID NOT NULL REFERENCES governance_frameworks(id) ON DELETE CASCADE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(credential_id, framework_id)
            )
        """)
        
        # Credential verification logs
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS credential_verification_logs (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                credential_id UUID NOT NULL REFERENCES blockchain_credentials(id),
                verifier_id UUID REFERENCES users(id),
                verification_type VARCHAR(100) NOT NULL,
                is_valid BOOLEAN NOT NULL,
                verification_data JSONB DEFAULT '{}',
                blockchain_verified BOOLEAN DEFAULT false,
                governance_compliant BOOLEAN DEFAULT false,
                ipfs_accessible BOOLEAN DEFAULT false,
                verification_metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
    
    async def _create_agent_tables(self):
        """Create multi-agent system tables"""
        
        # Agents
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                agent_id VARCHAR(100) UNIQUE NOT NULL,
                agent_type VARCHAR(100) NOT NULL,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                specialization VARCHAR(255),
                status VARCHAR(50) DEFAULT 'idle',
                capabilities JSONB DEFAULT '[]',
                configuration JSONB DEFAULT '{}',
                total_tasks INTEGER DEFAULT 0,
                completed_tasks INTEGER DEFAULT 0,
                success_rate FLOAT DEFAULT 0.0,
                average_response_time FLOAT DEFAULT 0.0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                last_active TIMESTAMP WITH TIME ZONE
            )
        """)
        
        # Agent tasks
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS agent_tasks (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                task_id VARCHAR(100) UNIQUE NOT NULL,
                agent_id UUID NOT NULL REFERENCES agents(id),
                task_type VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                input_data JSONB DEFAULT '{}',
                output_data JSONB DEFAULT '{}',
                status VARCHAR(50) DEFAULT 'pending',
                assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                started_at TIMESTAMP WITH TIME ZONE,
                completed_at TIMESTAMP WITH TIME ZONE,
                processing_time FLOAT,
                confidence_score FLOAT,
                success BOOLEAN,
                error_message TEXT
            )
        """)
        
        # Task collaborations
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS task_collaborations (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                task_id UUID NOT NULL REFERENCES agent_tasks(id),
                collaborating_agent_id UUID NOT NULL REFERENCES agents(id),
                collaboration_type VARCHAR(100) NOT NULL,
                contribution TEXT,
                contribution_data JSONB DEFAULT '{}',
                started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                completed_at TIMESTAMP WITH TIME ZONE
            )
        """)
        
        # Agent interactions
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS agent_interactions (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                agent_id UUID NOT NULL REFERENCES agents(id),
                user_id UUID REFERENCES users(id),
                session_id VARCHAR(255),
                interaction_type VARCHAR(100) NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                thoughts JSONB DEFAULT '[]',
                actions JSONB DEFAULT '[]',
                confidence FLOAT,
                processing_time FLOAT,
                context_data JSONB DEFAULT '{}',
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
    
    async def _create_cognitive_tables(self):
        """Create cognitive architecture tables"""
        
        # Cognitive memories
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS cognitive_memories (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                persona_id VARCHAR(100) NOT NULL,
                memory_type VARCHAR(50) NOT NULL,
                content JSONB NOT NULL,
                embedding_vector FLOAT[],
                importance_score FLOAT DEFAULT 0.0,
                confidence FLOAT DEFAULT 1.0,
                emotional_valence FLOAT DEFAULT 0.0,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                retention_until TIMESTAMP WITH TIME ZONE,
                context_tags TEXT[],
                associated_memories TEXT[]
            )
        """)
        
        # Cognitive learning
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS cognitive_learning (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                persona_id VARCHAR(100) NOT NULL,
                learning_type VARCHAR(50) NOT NULL,
                input_data JSONB NOT NULL,
                output_data JSONB NOT NULL,
                improvement_score FLOAT,
                adaptation_rate FLOAT,
                knowledge_gain FLOAT,
                before_performance JSONB DEFAULT '{}',
                after_performance JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # Attention patterns
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS attention_patterns (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                persona_id VARCHAR(100) NOT NULL,
                attention_targets JSONB NOT NULL,
                allocation_weights JSONB NOT NULL,
                focus_duration FLOAT,
                context JSONB NOT NULL,
                trigger_event VARCHAR(255),
                effectiveness_score FLOAT,
                distraction_level FLOAT DEFAULT 0.0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
    
    async def _create_bologna_tables(self):
        """Create Bologna Process specific tables"""
        
        # Bologna Process compliance
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS bologna_process_compliance (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                credential_id UUID NOT NULL REFERENCES blockchain_credentials(id),
                ects_credits INTEGER NOT NULL,
                eqf_level INTEGER NOT NULL,
                diploma_supplement_issued BOOLEAN DEFAULT false,
                quality_assurance_agency VARCHAR(255),
                joint_degree_program BOOLEAN DEFAULT false,
                learning_outcomes JSONB DEFAULT '[]',
                competencies JSONB DEFAULT '[]',
                mobility_partners JSONB DEFAULT '[]',
                recognition_status VARCHAR(50) DEFAULT 'under_review',
                recognition_notes TEXT,
                is_validated BOOLEAN DEFAULT false,
                validation_date TIMESTAMP WITH TIME ZONE,
                validator_id UUID REFERENCES users(id),
                compliance_metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
    
    async def _create_analytics_tables(self):
        """Create analytics and monitoring tables"""
        
        # System metrics
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                metric_name VARCHAR(100) NOT NULL,
                metric_value FLOAT NOT NULL,
                metric_category VARCHAR(100) NOT NULL,
                component VARCHAR(100),
                metadata JSONB DEFAULT '{}',
                tags TEXT[],
                recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # Audit logs
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID REFERENCES users(id),
                action VARCHAR(100) NOT NULL,
                resource_type VARCHAR(100) NOT NULL,
                resource_id VARCHAR(255),
                ip_address VARCHAR(45),
                user_agent TEXT,
                old_values JSONB,
                new_values JSONB,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
    
    async def _create_indexes(self):
        """Create database indexes for performance"""
        
        indexes = [
            # User indexes
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_student_id ON users(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_users_blockchain_address ON users(blockchain_address)",
            "CREATE INDEX IF NOT EXISTS idx_users_persona_type ON users(persona_type)",
            
            # Session indexes
            "CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON user_sessions(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON user_sessions(expires_at)",
            
            # Credential indexes
            "CREATE INDEX IF NOT EXISTS idx_credentials_credential_id ON blockchain_credentials(credential_id)",
            "CREATE INDEX IF NOT EXISTS idx_credentials_student_id ON blockchain_credentials(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_credentials_transaction_hash ON blockchain_credentials(transaction_hash)",
            "CREATE INDEX IF NOT EXISTS idx_credentials_status ON blockchain_credentials(status)",
            "CREATE INDEX IF NOT EXISTS idx_credentials_issue_date ON blockchain_credentials(issue_date)",
            
            # Agent indexes
            "CREATE INDEX IF NOT EXISTS idx_agents_agent_id ON agents(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(agent_type)",
            "CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status)",
            
            # Task indexes
            "CREATE INDEX IF NOT EXISTS idx_tasks_task_id ON agent_tasks(task_id)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON agent_tasks(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON agent_tasks(status)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_at ON agent_tasks(assigned_at)",
            
            # Interaction indexes
            "CREATE INDEX IF NOT EXISTS idx_interactions_agent_id ON agent_interactions(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_user_id ON agent_interactions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_created_at ON agent_interactions(created_at)",
            
            # Memory indexes
            "CREATE INDEX IF NOT EXISTS idx_memories_persona_id ON cognitive_memories(persona_id)",
            "CREATE INDEX IF NOT EXISTS idx_memories_type ON cognitive_memories(memory_type)",
            "CREATE INDEX IF NOT EXISTS idx_memories_importance ON cognitive_memories(importance_score DESC)",
            "CREATE INDEX IF NOT EXISTS idx_memories_created_at ON cognitive_memories(created_at DESC)",
            
            # Learning indexes
            "CREATE INDEX IF NOT EXISTS idx_learning_persona_id ON cognitive_learning(persona_id)",
            "CREATE INDEX IF NOT EXISTS idx_learning_type ON cognitive_learning(learning_type)",
            "CREATE INDEX IF NOT EXISTS idx_learning_created_at ON cognitive_learning(created_at)",
            
            # Attention indexes
            "CREATE INDEX IF NOT EXISTS idx_attention_persona_id ON attention_patterns(persona_id)",
            "CREATE INDEX IF NOT EXISTS idx_attention_created_at ON attention_patterns(created_at)",
            
            # Analytics indexes
            "CREATE INDEX IF NOT EXISTS idx_metrics_name ON system_metrics(metric_name)",
            "CREATE INDEX IF NOT EXISTS idx_metrics_category ON system_metrics(metric_category)",
            "CREATE INDEX IF NOT EXISTS idx_metrics_recorded_at ON system_metrics(recorded_at)",
            
            # Audit indexes
            "CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_logs(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action)",
            "CREATE INDEX IF NOT EXISTS idx_audit_resource ON audit_logs(resource_type, resource_id)",
            "CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_logs(created_at)",
        ]
        
        for index_sql in indexes:
            try:
                await self.db.execute(index_sql)
                logger.debug(f"Created index: {index_sql}")
            except Exception as e:
                logger.warning(f"Failed to create index: {index_sql} - {e}")
    
    async def _create_functions(self):
        """Create database functions and triggers"""
        
        # Update timestamp function
        await self.db.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ language 'plpgsql'
        """)
        
        # Create triggers for updated_at
        tables_with_updated_at = [
            'users', 'institutions', 'departments', 'roles',
            'blockchain_credentials', 'governance_frameworks',
            'agents', 'cognitive_memories', 'bologna_process_compliance'
        ]
        
        for table in tables_with_updated_at:
            trigger_name = f"update_{table}_updated_at"
            await self.db.execute(f"""
                DROP TRIGGER IF EXISTS {trigger_name} ON {table};
                CREATE TRIGGER {trigger_name}
                    BEFORE UPDATE ON {table}
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column()
            """)
    
    async def _seed_initial_data(self):
        """Seed initial data"""
        logger.info("Seeding initial data...")
        
        # Create default institution
        institution_id = await self._create_default_institution()
        
        # Create system roles and permissions
        await self._create_system_roles()
        await self._create_system_permissions()
        
        # Create default admin user
        await self._create_admin_user(institution_id)
        
        # Create governance frameworks
        await self._create_governance_frameworks()
        
        # Register default agents
        await self._register_default_agents()
        
        logger.info("Initial data seeding completed")
    
    async def _create_default_institution(self) -> str:
        """Create default institution"""
        institution_id = await self.db.fetchval("""
            INSERT INTO institutions (
                name, short_name, type, country, city, 
                bologna_process_member, settings
            ) VALUES (
                'Demo University', 'DEMO_U', 'university', 'United States', 'Demo City',
                true, '{\"demo_mode\": true}'
            )
            ON CONFLICT DO NOTHING
            RETURNING id
        """)
        
        if not institution_id:
            # Get existing institution
            institution_id = await self.db.fetchval(
                "SELECT id FROM institutions WHERE short_name = 'DEMO_U'"
            )
        
        return str(institution_id)
    
    async def _create_system_roles(self):
        """Create system roles"""
        roles = [
            ('admin', 'System Administrator', True),
            ('faculty', 'Faculty Member', False),
            ('staff', 'Staff Member', False), 
            ('student', 'Student', False),
        ]
        
        for role_name, description, is_system in roles:
            await self.db.execute("""
                INSERT INTO roles (name, description, is_system)
                VALUES ($1, $2, $3)
                ON CONFLICT (name) DO NOTHING
            """, role_name, description, is_system)
    
    async def _create_system_permissions(self):
        """Create system permissions"""
        permissions = [
            ('agent_query', 'Query AI agents', 'agents', 'query'),
            ('credential_issue', 'Issue blockchain credentials', 'credentials', 'issue'),
            ('credential_verify', 'Verify blockchain credentials', 'credentials', 'verify'),
            ('governance_audit', 'Create compliance audits', 'governance', 'audit'),
            ('user_manage', 'Manage users', 'users', 'manage'),
            ('system_admin', 'System administration', 'system', 'admin'),
            ('bologna_manage', 'Manage Bologna Process compliance', 'bologna', 'manage'),
            ('analytics_view', 'View analytics and reports', 'analytics', 'view'),
        ]
        
        for name, description, resource, action in permissions:
            await self.db.execute("""
                INSERT INTO permissions (name, description, resource, action)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (name) DO NOTHING
            """, name, description, resource, action)
        
        # Assign permissions to roles
        await self._assign_role_permissions()
    
    async def _assign_role_permissions(self):
        """Assign permissions to roles"""
        role_permissions = {
            'admin': [
                'agent_query', 'credential_issue', 'credential_verify',
                'governance_audit', 'user_manage', 'system_admin',
                'bologna_manage', 'analytics_view'
            ],
            'faculty': [
                'agent_query', 'credential_issue', 'credential_verify',
                'bologna_manage', 'analytics_view'
            ],
            'staff': [
                'agent_query', 'credential_verify', 'analytics_view'
            ],
            'student': [
                'agent_query'
            ]
        }
        
        for role_name, permissions in role_permissions.items():
            role_id = await self.db.fetchval(
                "SELECT id FROM roles WHERE name = $1", role_name
            )
            
            for permission_name in permissions:
                permission_id = await self.db.fetchval(
                    "SELECT id FROM permissions WHERE name = $1", permission_name
                )
                
                if role_id and permission_id:
                    await self.db.execute("""
                        INSERT INTO role_permissions (role_id, permission_id)
                        VALUES ($1, $2)
                        ON CONFLICT (role_id, permission_id) DO NOTHING
                    """, role_id, permission_id)
    
    async def _create_admin_user(self, institution_id: str):
        """Create default admin user"""
        import bcrypt
        
        # Hash default password
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_id = await self.db.fetchval("""
            INSERT INTO users (
                username, email, password_hash, first_name, last_name,
                persona_type, institution_id, is_verified
            ) VALUES (
                'admin', 'admin@collegiumai.com', $1, 'System', 'Administrator',
                'admin_technical', $2, true
            )
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """, password_hash, institution_id)
        
        if user_id:
            # Assign admin role
            admin_role_id = await self.db.fetchval(
                "SELECT id FROM roles WHERE name = 'admin'"
            )
            
            if admin_role_id:
                await self.db.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES ($1, $2)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                """, user_id, admin_role_id)
    
    async def _create_governance_frameworks(self):
        """Create default governance frameworks"""
        frameworks = [
            ('AACSB', 'AACSB', 'Association to Advance Collegiate Schools of Business', 'North America', 'accreditation'),
            ('WASC', 'WASC', 'Western Association of Schools and Colleges', 'North America', 'accreditation'),
            ('QAA', 'QAA', 'Quality Assurance Agency for Higher Education', 'United Kingdom', 'quality_assurance'),
            ('BOLOGNA_PROCESS', 'BOLOGNA', 'Bologna Process - European Higher Education Area', 'Europe', 'compliance'),
            ('ECTS', 'ECTS', 'European Credit Transfer and Accumulation System', 'Europe', 'credit_system'),
        ]
        
        for name, code, description, region, framework_type in frameworks:
            await self.db.execute("""
                INSERT INTO governance_frameworks (name, code, description, region, framework_type)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (code) DO NOTHING
            """, name, code, description, region, framework_type)
    
    async def _register_default_agents(self):
        """Register default system agents"""
        agents = [
            ('academic_advisor_001', 'academic_advisor', 'Academic Advisor', 'Course planning and academic guidance'),
            ('student_services_001', 'student_services', 'Student Services', 'Student enrollment and support services'),
            ('bologna_process_001', 'bologna_process', 'Bologna Process Specialist', 'European Higher Education Area compliance'),
            ('research_coordinator_001', 'research_coordinator', 'Research Coordinator', 'Research project coordination'),
        ]
        
        for agent_id, agent_type, name, description in agents:
            await self.db.execute("""
                INSERT INTO agents (agent_id, agent_type, name, description)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (agent_id) DO NOTHING
            """, agent_id, agent_type, name, description)
    
    async def _mark_initialized(self):
        """Mark database as initialized"""
        await self.db.execute("""
            INSERT INTO system_metrics (
                metric_name, metric_value, metric_category, component, metadata
            ) VALUES (
                'database_initialized', 1.0, 'system', 'database',
                $1
            )
            ON CONFLICT DO NOTHING
        """, json.dumps({
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }))

async def initialize_database(force_recreate: bool = False) -> bool:
    """Initialize the CollegiumAI database"""
    try:
        # Create database service
        db_service = DatabaseService()
        await db_service.initialize()
        
        # Initialize database
        initializer = DatabaseInitializer(db_service)
        success = await initializer.initialize_database(force_recreate)
        
        # Close connection
        await db_service.close()
        
        return success
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    # Run database initialization
    async def main():
        logging.basicConfig(level=logging.INFO)
        success = await initialize_database(force_recreate=False)
        if success:
            print("✅ Database initialization completed successfully")
        else:
            print("❌ Database initialization failed")
    
    asyncio.run(main())