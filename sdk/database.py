"""
Database Client for CollegiumAI SDK
Handles database operations, queries, and data management
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
from enum import Enum

class QueryType(Enum):
    """Database query types"""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    AGGREGATE = "aggregate"
    ANALYTICS = "analytics"

class DatabaseClient:
    """Client for database operations and data management"""
    
    def __init__(self, client):
        self.client = client
    
    # User Data Management
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user information by ID"""
        return await self.client.get(f'/database/users/{user_id}')
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user record"""
        return await self.client.post('/database/users', data=user_data)
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        return await self.client.put(f'/database/users/{user_id}', data=updates)
    
    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user record"""
        return await self.client.delete(f'/database/users/{user_id}')
    
    async def search_users(
        self,
        query: str = None,
        filters: Dict[str, Any] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search users with filters
        
        Args:
            query: Search query string
            filters: Filter criteria (role, department, etc.)
            limit: Maximum results to return
            offset: Results offset for pagination
            
        Returns:
            Search results with users and metadata
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if query:
            params['query'] = query
        if filters:
            params.update(filters)
        
        return await self.client.get('/database/users/search', params=params)
    
    # Agent Data Management
    async def get_agent_sessions(
        self,
        user_id: str = None,
        agent_type: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get agent session data"""
        params = {'limit': limit}
        
        if user_id:
            params['user_id'] = user_id
        if agent_type:
            params['agent_type'] = agent_type
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        return await self.client.get('/database/agent-sessions', params=params)
    
    async def get_conversation_history(
        self,
        session_id: str,
        include_metadata: bool = True
    ) -> List[Dict[str, Any]]:
        """Get complete conversation history for a session"""
        params = {'include_metadata': include_metadata}
        
        return await self.client.get(
            f'/database/conversations/{session_id}',
            params=params
        )
    
    async def save_conversation_message(
        self,
        session_id: str,
        message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save a conversation message to database"""
        return await self.client.post(
            f'/database/conversations/{session_id}/messages',
            data=message_data
        )
    
    async def get_agent_performance_data(
        self,
        agent_type: str = None,
        time_period: str = '30d'
    ) -> Dict[str, Any]:
        """Get agent performance metrics from database"""
        params = {'time_period': time_period}
        
        if agent_type:
            params['agent_type'] = agent_type
        
        return await self.client.get('/database/analytics/agent-performance', params=params)
    
    # Credential and Academic Data
    async def get_user_credentials(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's digital credentials"""
        return await self.client.get(f'/database/credentials/{user_id}')
    
    async def create_credential(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new digital credential"""
        return await self.client.post('/database/credentials', data=credential_data)
    
    async def verify_credential(self, credential_id: str) -> Dict[str, Any]:
        """Verify a digital credential"""
        return await self.client.get(f'/database/credentials/{credential_id}/verify')
    
    async def get_academic_records(
        self,
        user_id: str,
        record_type: str = None
    ) -> List[Dict[str, Any]]:
        """Get user's academic records"""
        params = {}
        if record_type:
            params['type'] = record_type
        
        return await self.client.get(
            f'/database/academic-records/{user_id}',
            params=params
        )
    
    async def create_academic_record(
        self,
        user_id: str,
        record_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new academic record"""
        return await self.client.post(
            f'/database/academic-records/{user_id}',
            data=record_data
        )
    
    # Cognitive Data Management
    async def get_cognitive_data(
        self,
        user_id: str,
        data_type: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[Dict[str, Any]]:
        """Get user's cognitive performance data"""
        params = {}
        
        if data_type:
            params['type'] = data_type
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        return await self.client.get(
            f'/database/cognitive-data/{user_id}',
            params=params
        )
    
    async def save_cognitive_metrics(
        self,
        user_id: str,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save cognitive performance metrics"""
        return await self.client.post(
            f'/database/cognitive-data/{user_id}',
            data=metrics
        )
    
    async def get_learning_analytics(
        self,
        user_id: str,
        subject: str = None,
        time_period: str = '30d'
    ) -> Dict[str, Any]:
        """Get learning analytics for a user"""
        params = {'time_period': time_period}
        
        if subject:
            params['subject'] = subject
        
        return await self.client.get(
            f'/database/learning-analytics/{user_id}',
            params=params
        )
    
    # System Data and Configuration
    async def get_system_configuration(self) -> Dict[str, Any]:
        """Get system configuration from database"""
        return await self.client.get('/database/system/configuration')
    
    async def update_system_configuration(
        self,
        config_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update system configuration"""
        return await self.client.put('/database/system/configuration', data=config_updates)
    
    async def get_audit_logs(
        self,
        table_name: str = None,
        action_type: str = None,
        user_id: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get database audit logs"""
        params = {'limit': limit}
        
        if table_name:
            params['table'] = table_name
        if action_type:
            params['action'] = action_type
        if user_id:
            params['user_id'] = user_id
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        return await self.client.get('/database/audit-logs', params=params)
    
    # Analytics and Reporting
    async def execute_analytics_query(
        self,
        query_name: str,
        parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute a predefined analytics query"""
        query_data = {
            'query_name': query_name,
            'parameters': parameters or {}
        }
        
        return await self.client.post('/database/analytics/query', data=query_data)
    
    async def get_user_engagement_metrics(
        self,
        time_period: str = '30d',
        user_type: str = None
    ) -> Dict[str, Any]:
        """Get user engagement metrics"""
        params = {'time_period': time_period}
        
        if user_type:
            params['user_type'] = user_type
        
        return await self.client.get('/database/analytics/user-engagement', params=params)
    
    async def get_system_usage_statistics(
        self,
        time_period: str = '30d',
        breakdown_by: str = 'day'
    ) -> Dict[str, Any]:
        """Get system usage statistics"""
        params = {
            'time_period': time_period,
            'breakdown_by': breakdown_by
        }
        
        return await self.client.get('/database/analytics/system-usage', params=params)
    
    async def generate_report(
        self,
        report_type: str,
        parameters: Dict[str, Any] = None,
        format: str = 'json'
    ) -> Dict[str, Any]:
        """Generate a data report"""
        report_data = {
            'report_type': report_type,
            'parameters': parameters or {},
            'format': format
        }
        
        return await self.client.post('/database/reports/generate', data=report_data)
    
    # Data Import/Export
    async def export_data(
        self,
        tables: List[str],
        format: str = 'json',
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Export data from specified tables"""
        export_data = {
            'tables': tables,
            'format': format,
            'filters': filters or {}
        }
        
        return await self.client.post('/database/export', data=export_data)
    
    async def import_data(
        self,
        table: str,
        data: List[Dict[str, Any]],
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Import data into a table"""
        import_data = {
            'table': table,
            'data': data,
            'options': options or {}
        }
        
        return await self.client.post('/database/import', data=import_data)
    
    async def backup_database(
        self,
        backup_name: str = None,
        include_tables: List[str] = None,
        exclude_tables: List[str] = None
    ) -> Dict[str, Any]:
        """Create a database backup"""
        backup_data = {
            'backup_name': backup_name,
            'include_tables': include_tables,
            'exclude_tables': exclude_tables
        }
        
        return await self.client.post('/database/backup', data=backup_data)
    
    async def restore_database(
        self,
        backup_id: str,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Restore database from backup"""
        restore_data = {
            'backup_id': backup_id,
            'options': options or {}
        }
        
        return await self.client.post('/database/restore', data=restore_data)
    
    # Database Health and Monitoring
    async def get_database_status(self) -> Dict[str, Any]:
        """Get database health status"""
        return await self.client.get('/database/status')
    
    async def get_database_metrics(self) -> Dict[str, Any]:
        """Get database performance metrics"""
        return await self.client.get('/database/metrics')
    
    async def get_connection_pool_status(self) -> Dict[str, Any]:
        """Get database connection pool status"""
        return await self.client.get('/database/connection-pool')
    
    async def optimize_database(
        self,
        tables: List[str] = None,
        operation: str = 'analyze'
    ) -> Dict[str, Any]:
        """
        Optimize database performance
        
        Args:
            tables: Specific tables to optimize (all if not specified)
            operation: Type of optimization (analyze, vacuum, reindex)
            
        Returns:
            Optimization results
        """
        optimization_data = {
            'tables': tables,
            'operation': operation
        }
        
        return await self.client.post('/database/optimize', data=optimization_data)
    
    # Custom Queries (with safety checks)
    async def execute_safe_query(
        self,
        query: str,
        parameters: Dict[str, Any] = None,
        read_only: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a custom SQL query with safety checks
        
        Args:
            query: SQL query to execute
            parameters: Query parameters for prepared statements
            read_only: Whether query is read-only (enforced on server)
            
        Returns:
            Query results
        """
        query_data = {
            'query': query,
            'parameters': parameters or {},
            'read_only': read_only
        }
        
        return await self.client.post('/database/query/execute', data=query_data)
    
    async def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate SQL query syntax without executing"""
        return await self.client.post('/database/query/validate', data={'query': query})
    
    async def explain_query(self, query: str) -> Dict[str, Any]:
        """Get query execution plan"""
        return await self.client.post('/database/query/explain', data={'query': query})
    
    # Schema Management
    async def get_schema_info(self, table_name: str = None) -> Dict[str, Any]:
        """Get database schema information"""
        params = {}
        if table_name:
            params['table'] = table_name
        
        return await self.client.get('/database/schema', params=params)
    
    async def get_table_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """Get indexes for a specific table"""
        return await self.client.get(f'/database/schema/{table_name}/indexes')
    
    async def get_table_constraints(self, table_name: str) -> List[Dict[str, Any]]:
        """Get constraints for a specific table"""
        return await self.client.get(f'/database/schema/{table_name}/constraints')
    
    # Data Validation and Quality
    async def validate_data_integrity(
        self,
        table_name: str = None
    ) -> Dict[str, Any]:
        """Validate data integrity across tables"""
        params = {}
        if table_name:
            params['table'] = table_name
        
        return await self.client.get('/database/validate/integrity', params=params)
    
    async def check_data_quality(
        self,
        table_name: str,
        quality_rules: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Check data quality against rules"""
        check_data = {
            'table': table_name,
            'quality_rules': quality_rules or []
        }
        
        return await self.client.post('/database/validate/quality', data=check_data)
    
    async def get_data_statistics(
        self,
        table_name: str,
        columns: List[str] = None
    ) -> Dict[str, Any]:
        """Get statistical analysis of table data"""
        params = {'table': table_name}
        
        if columns:
            params['columns'] = ','.join(columns)
        
        return await self.client.get('/database/statistics', params=params)