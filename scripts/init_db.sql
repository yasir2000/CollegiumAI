-- CollegiumAI Database Initialization Script
-- Version: 1.0.0

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS cognitive;
CREATE SCHEMA IF NOT EXISTS personas;
CREATE SCHEMA IF NOT EXISTS sessions;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Create tables for cognitive engine
CREATE TABLE IF NOT EXISTS cognitive.memory_store (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    persona_id VARCHAR(100) NOT NULL,
    memory_type VARCHAR(50) NOT NULL, -- episodic, semantic, working
    content JSONB NOT NULL,
    importance_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cognitive.learning_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    persona_id VARCHAR(100) NOT NULL,
    learning_type VARCHAR(50) NOT NULL,
    input_data JSONB NOT NULL,
    output_data JSONB NOT NULL,
    performance_metrics JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cognitive.attention_patterns (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    persona_id VARCHAR(100) NOT NULL,
    attention_targets JSONB NOT NULL,
    allocation_weights JSONB NOT NULL,
    context JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tables for personas
CREATE TABLE IF NOT EXISTS personas.persona_profiles (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    persona_id VARCHAR(100) UNIQUE NOT NULL,
    persona_type VARCHAR(100) NOT NULL,
    cognitive_params JSONB NOT NULL,
    individual_context JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS personas.interaction_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    persona_id VARCHAR(100) NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    request_data JSONB NOT NULL,
    response_data JSONB NOT NULL,
    processing_time FLOAT NOT NULL,
    confidence_score FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tables for sessions
CREATE TABLE IF NOT EXISTS sessions.user_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    persona_id VARCHAR(100) NOT NULL,
    session_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions.multi_agent_tasks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    task_id VARCHAR(100) UNIQUE NOT NULL,
    task_description TEXT NOT NULL,
    participating_agents JSONB NOT NULL,
    task_status VARCHAR(50) DEFAULT 'pending',
    result_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Create tables for analytics
CREATE TABLE IF NOT EXISTS analytics.system_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metadata JSONB DEFAULT '{}',
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics.performance_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    operation_type VARCHAR(100) NOT NULL,
    execution_time FLOAT NOT NULL,
    memory_usage FLOAT,
    cpu_usage FLOAT,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_memory_store_persona_id ON cognitive.memory_store(persona_id);
CREATE INDEX IF NOT EXISTS idx_memory_store_type ON cognitive.memory_store(memory_type);
CREATE INDEX IF NOT EXISTS idx_memory_store_importance ON cognitive.memory_store(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_memory_store_created_at ON cognitive.memory_store(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_learning_history_persona_id ON cognitive.learning_history(persona_id);
CREATE INDEX IF NOT EXISTS idx_learning_history_type ON cognitive.learning_history(learning_type);
CREATE INDEX IF NOT EXISTS idx_learning_history_created_at ON cognitive.learning_history(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_attention_patterns_persona_id ON cognitive.attention_patterns(persona_id);
CREATE INDEX IF NOT EXISTS idx_attention_patterns_created_at ON cognitive.attention_patterns(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_persona_profiles_persona_id ON personas.persona_profiles(persona_id);
CREATE INDEX IF NOT EXISTS idx_persona_profiles_type ON personas.persona_profiles(persona_type);

CREATE INDEX IF NOT EXISTS idx_interaction_history_persona_id ON personas.interaction_history(persona_id);
CREATE INDEX IF NOT EXISTS idx_interaction_history_session_id ON personas.interaction_history(session_id);
CREATE INDEX IF NOT EXISTS idx_interaction_history_created_at ON personas.interaction_history(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON sessions.user_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_persona_id ON sessions.user_sessions(persona_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON sessions.user_sessions(expires_at);

CREATE INDEX IF NOT EXISTS idx_multi_agent_tasks_task_id ON sessions.multi_agent_tasks(task_id);
CREATE INDEX IF NOT EXISTS idx_multi_agent_tasks_status ON sessions.multi_agent_tasks(task_status);
CREATE INDEX IF NOT EXISTS idx_multi_agent_tasks_created_at ON sessions.multi_agent_tasks(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_system_metrics_name ON analytics.system_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_system_metrics_recorded_at ON analytics.system_metrics(recorded_at DESC);

CREATE INDEX IF NOT EXISTS idx_performance_logs_operation_type ON analytics.performance_logs(operation_type);
CREATE INDEX IF NOT EXISTS idx_performance_logs_created_at ON analytics.performance_logs(created_at DESC);

-- Create functions for maintenance
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM sessions.user_sessions WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cleanup_old_logs(days_to_keep INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM analytics.performance_logs WHERE created_at < NOW() - INTERVAL '%s days' % days_to_keep;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_persona_profiles_updated_at
    BEFORE UPDATE ON personas.persona_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_sessions_updated_at
    BEFORE UPDATE ON sessions.user_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert initial system configuration
INSERT INTO analytics.system_metrics (metric_name, metric_value, metadata) VALUES
    ('system_initialization', 1.0, '{"version": "1.0.0", "timestamp": "' || NOW() || '"}'),
    ('database_schema_version', 1.0, '{"schema_version": "1.0.0"}')
ON CONFLICT DO NOTHING;

-- Grant permissions (adjust as needed for your setup)
GRANT USAGE ON SCHEMA cognitive TO collegiumai;
GRANT USAGE ON SCHEMA personas TO collegiumai;
GRANT USAGE ON SCHEMA sessions TO collegiumai;
GRANT USAGE ON SCHEMA analytics TO collegiumai;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cognitive TO collegiumai;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA personas TO collegiumai;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sessions TO collegiumai;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO collegiumai;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA cognitive TO collegiumai;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA personas TO collegiumai;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sessions TO collegiumai;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO collegiumai;

-- Log successful initialization
INSERT INTO analytics.performance_logs (operation_type, execution_time, success, created_at) VALUES
    ('database_initialization', 0.0, true, NOW());

COMMIT;