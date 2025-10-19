"""
Advanced Database Models for CollegiumAI
========================================

Comprehensive data models for university management, blockchain credentials,
multi-agent coordination, and cognitive architecture monitoring.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, JSON,
    ForeignKey, Table, UniqueConstraint, Index, DECIMAL
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

Base = declarative_base()

# Enums
class UserRole(Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    STAFF = "staff"
    ADMIN = "admin"
    SYSTEM = "system"

class PersonaType(Enum):
    TRADITIONAL_STUDENT = "traditional_student"
    INTERNATIONAL_STUDENT = "international_student"
    GRADUATE_STUDENT = "graduate_student"
    FACULTY_RESEARCHER = "faculty_researcher"
    FACULTY_TEACHER = "faculty_teacher"
    ADMIN_ACADEMIC = "admin_academic"
    ADMIN_TECHNICAL = "admin_technical"
    STAFF_ADVISOR = "staff_advisor"

class CredentialStatus(Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    VERIFIED = "verified"
    REVOKED = "revoked"
    EXPIRED = "expired"

class BolognaProcessStatus(Enum):
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"

class AgentStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"

# Association Tables
user_roles_table = Table(
    'user_roles', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))
)

user_permissions_table = Table(
    'user_permissions', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'))
)

credential_frameworks_table = Table(
    'credential_frameworks', Base.metadata,
    Column('credential_id', UUID(as_uuid=True), ForeignKey('blockchain_credentials.id')),
    Column('framework_id', UUID(as_uuid=True), ForeignKey('governance_frameworks.id'))
)

# Core User Management Models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    student_id = Column(String(50), unique=True, nullable=True)
    employee_id = Column(String(50), unique=True, nullable=True)
    
    # User attributes
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    persona_type = Column(String(50), nullable=False)
    blockchain_address = Column(String(42), unique=True, nullable=True)
    
    # Institutional information
    institution_id = Column(UUID(as_uuid=True), ForeignKey('institutions.id'))
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=True)
    
    # Profile information
    profile_data = Column(JSON, default=dict)
    preferences = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles_table, back_populates="users")
    permissions = relationship("Permission", secondary=user_permissions_table, back_populates="users")
    sessions = relationship("UserSession", back_populates="user")
    credentials = relationship("BlockchainCredential", back_populates="student")
    institution = relationship("Institution", back_populates="users")
    department = relationship("Department", back_populates="users")
    
    # Indexes
    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_username', 'username'),
        Index('idx_users_student_id', 'student_id'),
        Index('idx_users_blockchain_address', 'blockchain_address'),
    )

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", secondary=user_roles_table, back_populates="roles")
    permissions = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    resource = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", secondary=user_permissions_table, back_populates="permissions")
    roles = relationship("RolePermission", back_populates="permission")

class RolePermission(Base):
    __tablename__ = 'role_permissions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
    
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_id'),
    )

# Session Management
class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Session data
    session_data = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Session lifecycle
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    # Indexes
    __table_args__ = (
        Index('idx_sessions_session_id', 'session_id'),
        Index('idx_sessions_user_id', 'user_id'),
        Index('idx_sessions_expires_at', 'expires_at'),
    )

# Institutional Models
class Institution(Base):
    __tablename__ = 'institutions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50), nullable=False)
    type = Column(String(100), nullable=False)  # university, college, institute
    
    # Contact information
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Blockchain information
    blockchain_address = Column(String(42), unique=True, nullable=True)
    
    # Accreditation and compliance
    accreditation_data = Column(JSON, default=dict)
    bologna_process_member = Column(Boolean, default=False)
    
    # Settings
    settings = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="institution")
    departments = relationship("Department", back_populates="institution")
    credentials = relationship("BlockchainCredential", back_populates="institution")

class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    code = Column(String(20), nullable=False)
    institution_id = Column(UUID(as_uuid=True), ForeignKey('institutions.id'), nullable=False)
    
    # Department details
    description = Column(Text, nullable=True)
    head_of_department_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Settings
    settings = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    institution = relationship("Institution", back_populates="departments")
    users = relationship("User", back_populates="department")
    
    __table_args__ = (
        UniqueConstraint('institution_id', 'code'),
    )

# Blockchain Credential Models
class BlockchainCredential(Base):
    __tablename__ = 'blockchain_credentials'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credential_id = Column(Integer, nullable=False)  # Blockchain credential ID
    
    # Basic credential information
    title = Column(String(255), nullable=False)
    program = Column(String(255), nullable=False)
    degree_level = Column(String(100), nullable=False)
    grade = Column(String(10), nullable=True)
    
    # Parties involved
    student_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    institution_id = Column(UUID(as_uuid=True), ForeignKey('institutions.id'), nullable=False)
    issuer_address = Column(String(42), nullable=False)
    
    # Blockchain information
    transaction_hash = Column(String(66), nullable=False)
    block_number = Column(Integer, nullable=True)
    gas_used = Column(String(50), nullable=True)
    
    # IPFS and document storage
    ipfs_hash = Column(String(255), nullable=True)
    document_urls = Column(JSON, default=list)
    
    # Status and lifecycle
    status = Column(String(50), default=CredentialStatus.ISSUED.value)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime(timezone=True), nullable=True)
    
    # Academic information
    issue_date = Column(DateTime(timezone=True), nullable=False)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    credits = Column(Integer, nullable=True)
    
    # Bologna Process compliance
    bologna_data = Column(JSON, default=dict)
    
    # Metadata
    metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("User", back_populates="credentials")
    institution = relationship("Institution", back_populates="credentials")
    governance_frameworks = relationship("GovernanceFramework", 
                                      secondary=credential_frameworks_table, 
                                      back_populates="credentials")
    verification_logs = relationship("CredentialVerificationLog", back_populates="credential")
    
    # Indexes
    __table_args__ = (
        Index('idx_credentials_credential_id', 'credential_id'),
        Index('idx_credentials_student_id', 'student_id'),
        Index('idx_credentials_transaction_hash', 'transaction_hash'),
        Index('idx_credentials_status', 'status'),
        UniqueConstraint('credential_id', 'transaction_hash'),
    )

class GovernanceFramework(Base):
    __tablename__ = 'governance_frameworks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Framework details
    region = Column(String(100), nullable=True)
    framework_type = Column(String(100), nullable=False)  # accreditation, quality_assurance, etc.
    requirements = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    credentials = relationship("BlockchainCredential", 
                             secondary=credential_frameworks_table, 
                             back_populates="governance_frameworks")

class CredentialVerificationLog(Base):
    __tablename__ = 'credential_verification_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credential_id = Column(UUID(as_uuid=True), ForeignKey('blockchain_credentials.id'), nullable=False)
    
    # Verification details
    verifier_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    verification_type = Column(String(100), nullable=False)  # manual, automatic, blockchain
    
    # Results
    is_valid = Column(Boolean, nullable=False)
    verification_data = Column(JSON, default=dict)
    blockchain_verified = Column(Boolean, default=False)
    governance_compliant = Column(Boolean, default=False)
    ipfs_accessible = Column(Boolean, default=False)
    
    # Metadata
    verification_metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    credential = relationship("BlockchainCredential", back_populates="verification_logs")
    verifier = relationship("User")

# Multi-Agent System Models
class Agent(Base):
    __tablename__ = 'agents'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String(100), unique=True, nullable=False)
    agent_type = Column(String(100), nullable=False)
    
    # Agent configuration
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    specialization = Column(String(255), nullable=True)
    
    # Agent state
    status = Column(String(50), default=AgentStatus.IDLE.value)
    capabilities = Column(JSON, default=list)
    configuration = Column(JSON, default=dict)
    
    # Performance metrics
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    average_response_time = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    tasks = relationship("AgentTask", back_populates="agent")
    interactions = relationship("AgentInteraction", back_populates="agent")

class AgentTask(Base):
    __tablename__ = 'agent_tasks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(String(100), unique=True, nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'), nullable=False)
    
    # Task details
    task_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Integer, default=5)  # 1-10 scale
    
    # Task data
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    
    # Task lifecycle
    status = Column(String(50), default='pending')
    assigned_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Performance
    processing_time = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    success = Column(Boolean, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="tasks")
    collaborations = relationship("TaskCollaboration", back_populates="task")

class TaskCollaboration(Base):
    __tablename__ = 'task_collaborations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey('agent_tasks.id'), nullable=False)
    collaborating_agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'), nullable=False)
    
    # Collaboration details
    collaboration_type = Column(String(100), nullable=False)  # consultation, joint_work, handoff
    contribution = Column(Text, nullable=True)
    contribution_data = Column(JSON, default=dict)
    
    # Timing
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    task = relationship("AgentTask", back_populates="collaborations")
    collaborating_agent = relationship("Agent")

class AgentInteraction(Base):
    __tablename__ = 'agent_interactions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    session_id = Column(String(255), nullable=True)
    
    # Interaction details
    interaction_type = Column(String(100), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    
    # Processing details
    thoughts = Column(JSON, default=list)
    actions = Column(JSON, default=list)
    confidence = Column(Float, nullable=True)
    processing_time = Column(Float, nullable=True)
    
    # Context
    context_data = Column(JSON, default=dict)
    metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="interactions")
    user = relationship("User")

# Cognitive Architecture Models
class CognitiveMemory(Base):
    __tablename__ = 'cognitive_memories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(String(100), nullable=False)
    memory_type = Column(String(50), nullable=False)  # episodic, semantic, working, procedural
    
    # Memory content
    content = Column(JSON, nullable=False)
    embedding_vector = Column(ARRAY(Float), nullable=True)  # For semantic search
    
    # Memory attributes
    importance_score = Column(Float, default=0.0)
    confidence = Column(Float, default=1.0)
    emotional_valence = Column(Float, default=0.0)  # -1 to 1
    
    # Access patterns
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Temporal information
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    retention_until = Column(DateTime(timezone=True), nullable=True)
    
    # Context and associations
    context_tags = Column(ARRAY(String), default=list)
    associated_memories = Column(ARRAY(String), default=list)  # UUIDs of related memories
    
    # Indexes
    __table_args__ = (
        Index('idx_memories_persona_id', 'persona_id'),
        Index('idx_memories_type', 'memory_type'),
        Index('idx_memories_importance', 'importance_score'),
        Index('idx_memories_created_at', 'created_at'),
    )

class CognitiveLearning(Base):
    __tablename__ = 'cognitive_learning'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(String(100), nullable=False)
    learning_type = Column(String(50), nullable=False)
    
    # Learning event
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=False)
    
    # Learning metrics
    improvement_score = Column(Float, nullable=True)
    adaptation_rate = Column(Float, nullable=True)
    knowledge_gain = Column(Float, nullable=True)
    
    # Performance tracking
    before_performance = Column(JSON, default=dict)
    after_performance = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_learning_persona_id', 'persona_id'),
        Index('idx_learning_type', 'learning_type'),
        Index('idx_learning_created_at', 'created_at'),
    )

class AttentionPattern(Base):
    __tablename__ = 'attention_patterns'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(String(100), nullable=False)
    
    # Attention allocation
    attention_targets = Column(JSON, nullable=False)
    allocation_weights = Column(JSON, nullable=False)
    focus_duration = Column(Float, nullable=True)
    
    # Context information
    context = Column(JSON, nullable=False)
    trigger_event = Column(String(255), nullable=True)
    
    # Performance metrics
    effectiveness_score = Column(Float, nullable=True)
    distraction_level = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_attention_persona_id', 'persona_id'),
        Index('idx_attention_created_at', 'created_at'),
    )

# Bologna Process Specific Models
class BolognaProcessCompliance(Base):
    __tablename__ = 'bologna_process_compliance'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credential_id = Column(UUID(as_uuid=True), ForeignKey('blockchain_credentials.id'), nullable=False)
    
    # ECTS Information
    ects_credits = Column(Integer, nullable=False)
    eqf_level = Column(Integer, nullable=False)  # European Qualifications Framework level
    
    # Bologna Process compliance
    diploma_supplement_issued = Column(Boolean, default=False)
    quality_assurance_agency = Column(String(255), nullable=True)
    joint_degree_program = Column(Boolean, default=False)
    
    # Learning outcomes and competencies
    learning_outcomes = Column(JSON, default=list)
    competencies = Column(JSON, default=list)
    
    # Mobility and recognition
    mobility_partners = Column(JSON, default=list)
    recognition_status = Column(String(50), default=BolognaProcessStatus.UNDER_REVIEW.value)
    recognition_notes = Column(Text, nullable=True)
    
    # Validation and verification
    is_validated = Column(Boolean, default=False)
    validation_date = Column(DateTime(timezone=True), nullable=True)
    validator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Metadata
    compliance_metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    credential = relationship("BlockchainCredential")
    validator = relationship("User")

# Analytics and Monitoring Models
class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    
    # Categorization
    metric_category = Column(String(100), nullable=False)  # performance, usage, error, etc.
    component = Column(String(100), nullable=True)  # which system component
    
    # Additional data
    metadata = Column(JSON, default=dict)
    tags = Column(ARRAY(String), default=list)
    
    recorded_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_metrics_name', 'metric_name'),
        Index('idx_metrics_category', 'metric_category'),
        Index('idx_metrics_recorded_at', 'recorded_at'),
    )

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Action details
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(255), nullable=True)
    
    # Request information
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Change tracking
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    # Status and results
    success = Column(Boolean, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Additional context
    metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_user_id', 'user_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
        Index('idx_audit_created_at', 'created_at'),
    )