"""
Visualization Client for CollegiumAI SDK
Handles multi-agent visualization, dashboards, and real-time monitoring
"""

from typing import Dict, List, Any, Optional, Union, AsyncGenerator
from datetime import datetime
from enum import Enum

class VisualizationType(Enum):
    """Types of visualizations available"""
    NETWORK_TOPOLOGY = "network_topology"
    PERFORMANCE_DASHBOARD = "performance_dashboard"
    COLLABORATION_GRAPH = "collaboration_graph"
    WORKFLOW_DIAGRAM = "workflow_diagram"
    SYSTEM_HEALTH = "system_health"
    USER_ANALYTICS = "user_analytics"
    COGNITIVE_INSIGHTS = "cognitive_insights"
    REAL_TIME_METRICS = "real_time_metrics"

class ChartType(Enum):
    """Chart types for data visualization"""
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    NETWORK_GRAPH = "network_graph"
    TREE_MAP = "tree_map"
    GAUGE = "gauge"
    TIMELINE = "timeline"

class DashboardType(Enum):
    """Dashboard types for different user roles"""
    STUDENT_DASHBOARD = "student_dashboard"
    FACULTY_DASHBOARD = "faculty_dashboard"
    ADMIN_DASHBOARD = "admin_dashboard"
    SYSTEM_DASHBOARD = "system_dashboard"
    ANALYTICS_DASHBOARD = "analytics_dashboard"
    EXECUTIVE_DASHBOARD = "executive_dashboard"

class VisualizationClient:
    """Client for visualization and dashboard operations"""
    
    def __init__(self, client):
        self.client = client
    
    # Multi-Agent Network Visualization
    async def get_agent_network_topology(
        self,
        time_range: str = '1h',
        include_inactive: bool = False,
        layout_algorithm: str = 'force_directed'
    ) -> Dict[str, Any]:
        """
        Get real-time multi-agent network topology
        
        Args:
            time_range: Time range for analysis (1h, 6h, 24h, 7d)
            include_inactive: Include inactive agents in visualization
            layout_algorithm: Graph layout algorithm (force_directed, hierarchical, circular)
            
        Returns:
            Network topology data with nodes, edges, and metadata
        """
        params = {
            'time_range': time_range,
            'include_inactive': include_inactive,
            'layout_algorithm': layout_algorithm
        }
        
        return await self.client.get('/visualization/agent-network', params=params)
    
    async def get_agent_collaboration_graph(
        self,
        collaboration_id: str = None,
        time_range: str = '24h',
        metric: str = 'interactions'
    ) -> Dict[str, Any]:
        """Get agent collaboration visualization"""
        params = {
            'time_range': time_range,
            'metric': metric
        }
        
        if collaboration_id:
            params['collaboration_id'] = collaboration_id
        
        return await self.client.get('/visualization/agent-collaboration', params=params)
    
    async def get_workflow_diagram(
        self,
        workflow_id: str,
        include_performance: bool = True,
        format: str = 'json'
    ) -> Dict[str, Any]:
        """Get workflow visualization diagram"""
        params = {
            'include_performance': include_performance,
            'format': format
        }
        
        return await self.client.get(f'/visualization/workflows/{workflow_id}', params=params)
    
    async def create_custom_network_view(
        self,
        view_config: Dict[str, Any],
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create custom network visualization view"""
        view_data = {
            'view_config': view_config,
            'filters': filters or {}
        }
        
        return await self.client.post('/visualization/network/custom', data=view_data)
    
    # Performance Dashboards
    async def get_performance_dashboard(
        self,
        dashboard_type: Union[str, DashboardType],
        time_range: str = '24h',
        metrics: List[str] = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Get performance dashboard data
        
        Args:
            dashboard_type: Type of dashboard to generate
            time_range: Time range for metrics
            metrics: Specific metrics to include
            user_id: User ID for personalized dashboards
            
        Returns:
            Dashboard configuration and data
        """
        if isinstance(dashboard_type, DashboardType):
            dashboard_type = dashboard_type.value
        
        params = {
            'dashboard_type': dashboard_type,
            'time_range': time_range
        }
        
        if metrics:
            params['metrics'] = ','.join(metrics)
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/visualization/dashboards/performance', params=params)
    
    async def get_system_health_dashboard(
        self,
        include_predictions: bool = True,
        detail_level: str = 'standard'
    ) -> Dict[str, Any]:
        """Get system health monitoring dashboard"""
        params = {
            'include_predictions': include_predictions,
            'detail_level': detail_level
        }
        
        return await self.client.get('/visualization/dashboards/system-health', params=params)
    
    async def create_custom_dashboard(
        self,
        dashboard_config: Dict[str, Any],
        user_id: str = None,
        is_public: bool = False
    ) -> Dict[str, Any]:
        """Create custom dashboard configuration"""
        creation_data = {
            'dashboard_config': dashboard_config,
            'user_id': user_id,
            'is_public': is_public
        }
        
        return await self.client.post('/visualization/dashboards/custom', data=creation_data)
    
    async def get_user_dashboards(
        self,
        user_id: str = None,
        include_public: bool = True
    ) -> List[Dict[str, Any]]:
        """Get user's saved dashboards"""
        params = {'include_public': include_public}
        
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/visualization/dashboards/user', params=params)
    
    # Real-Time Monitoring
    async def subscribe_to_real_time_metrics(
        self,
        metrics: List[str],
        update_interval: int = 5,
        filters: Dict[str, Any] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Subscribe to real-time metric updates
        
        Args:
            metrics: List of metrics to monitor
            update_interval: Update interval in seconds
            filters: Optional filters for metrics
            
        Yields:
            Real-time metric updates
        """
        subscription_data = {
            'type': 'metrics_subscription',
            'metrics': metrics,
            'update_interval': update_interval,
            'filters': filters or {}
        }
        
        # Use the client's WebSocket subscription
        async for message in self.client.subscribe_to_updates(['metrics', 'performance']):
            # Filter for subscribed metrics
            if message.get('type') == 'metrics_update':
                metric_name = message.get('metric')
                if metric_name in metrics:
                    yield message
    
    async def get_real_time_agent_status(self) -> Dict[str, Any]:
        """Get real-time status of all agents"""
        return await self.client.get('/visualization/real-time/agents')
    
    async def get_live_system_metrics(
        self,
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """Get current live system metrics"""
        params = {}
        
        if metrics:
            params['metrics'] = ','.join(metrics)
        
        return await self.client.get('/visualization/real-time/system', params=params)
    
    # Data Visualization and Charts
    async def create_chart(
        self,
        chart_type: Union[str, ChartType],
        data_source: Dict[str, Any],
        chart_config: Dict[str, Any] = None,
        title: str = None
    ) -> Dict[str, Any]:
        """
        Create a data visualization chart
        
        Args:
            chart_type: Type of chart to create
            data_source: Data source configuration
            chart_config: Chart styling and configuration
            title: Chart title
            
        Returns:
            Chart configuration and data
        """
        if isinstance(chart_type, ChartType):
            chart_type = chart_type.value
        
        chart_data = {
            'chart_type': chart_type,
            'data_source': data_source,
            'chart_config': chart_config or {},
            'title': title
        }
        
        return await self.client.post('/visualization/charts', data=chart_data)
    
    async def update_chart_data(
        self,
        chart_id: str,
        new_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update chart with new data"""
        return await self.client.put(f'/visualization/charts/{chart_id}/data', data=new_data)
    
    async def get_chart_data(
        self,
        chart_id: str,
        time_range: str = None
    ) -> Dict[str, Any]:
        """Get chart data"""
        params = {}
        
        if time_range:
            params['time_range'] = time_range
        
        return await self.client.get(f'/visualization/charts/{chart_id}', params=params)
    
    async def export_chart(
        self,
        chart_id: str,
        format: str = 'png',
        width: int = 800,
        height: int = 600
    ) -> Dict[str, Any]:
        """Export chart as image or data"""
        export_data = {
            'format': format,
            'width': width,
            'height': height
        }
        
        return await self.client.post(f'/visualization/charts/{chart_id}/export', data=export_data)
    
    # Analytics Visualization
    async def get_user_analytics_visualization(
        self,
        user_id: str = None,
        time_range: str = '30d',
        visualization_type: Union[str, VisualizationType] = VisualizationType.USER_ANALYTICS
    ) -> Dict[str, Any]:
        """Get user analytics visualization"""
        if isinstance(visualization_type, VisualizationType):
            visualization_type = visualization_type.value
        
        params = {
            'time_range': time_range,
            'visualization_type': visualization_type
        }
        
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/visualization/analytics/user', params=params)
    
    async def get_learning_progress_visualization(
        self,
        student_id: str,
        subject: str = None,
        time_range: str = '90d'
    ) -> Dict[str, Any]:
        """Get learning progress visualization"""
        params = {
            'student_id': student_id,
            'time_range': time_range
        }
        
        if subject:
            params['subject'] = subject
        
        return await self.client.get('/visualization/analytics/learning-progress', params=params)
    
    async def get_engagement_heatmap(
        self,
        time_range: str = '7d',
        granularity: str = 'hour',
        user_type: str = None
    ) -> Dict[str, Any]:
        """Get user engagement heatmap"""
        params = {
            'time_range': time_range,
            'granularity': granularity
        }
        
        if user_type:
            params['user_type'] = user_type
        
        return await self.client.get('/visualization/analytics/engagement-heatmap', params=params)
    
    # Cognitive Visualization
    async def get_cognitive_insights_visualization(
        self,
        user_id: str,
        insight_type: str = 'comprehensive',
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Get cognitive insights visualization"""
        params = {
            'user_id': user_id,
            'insight_type': insight_type,
            'time_range': time_range
        }
        
        return await self.client.get('/visualization/cognitive/insights', params=params)
    
    async def get_memory_pattern_visualization(
        self,
        user_id: str,
        memory_type: str = 'all',
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Get memory pattern visualization"""
        params = {
            'user_id': user_id,
            'memory_type': memory_type,
            'time_range': time_range
        }
        
        return await self.client.get('/visualization/cognitive/memory-patterns', params=params)
    
    async def get_attention_flow_diagram(
        self,
        session_id: str,
        granularity: str = 'minute'
    ) -> Dict[str, Any]:
        """Get attention flow visualization for a session"""
        params = {
            'session_id': session_id,
            'granularity': granularity
        }
        
        return await self.client.get('/visualization/cognitive/attention-flow', params=params)
    
    # Interactive Visualizations
    async def create_interactive_dashboard(
        self,
        dashboard_config: Dict[str, Any],
        widgets: List[Dict[str, Any]],
        layout: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create interactive dashboard with widgets"""
        dashboard_data = {
            'dashboard_config': dashboard_config,
            'widgets': widgets,
            'layout': layout or {'type': 'grid'}
        }
        
        return await self.client.post('/visualization/interactive/dashboard', data=dashboard_data)
    
    async def add_dashboard_widget(
        self,
        dashboard_id: str,
        widget_config: Dict[str, Any],
        position: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Add widget to existing dashboard"""
        widget_data = {
            'widget_config': widget_config,
            'position': position
        }
        
        return await self.client.post(
            f'/visualization/interactive/dashboard/{dashboard_id}/widgets',
            data=widget_data
        )
    
    async def update_dashboard_layout(
        self,
        dashboard_id: str,
        layout: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update dashboard layout"""
        return await self.client.put(
            f'/visualization/interactive/dashboard/{dashboard_id}/layout',
            data=layout
        )
    
    # Export and Sharing
    async def export_visualization(
        self,
        visualization_id: str,
        format: str = 'json',
        include_data: bool = True,
        quality: str = 'high'
    ) -> Dict[str, Any]:
        """Export visualization in various formats"""
        export_data = {
            'format': format,
            'include_data': include_data,
            'quality': quality
        }
        
        return await self.client.post(
            f'/visualization/export/{visualization_id}',
            data=export_data
        )
    
    async def share_dashboard(
        self,
        dashboard_id: str,
        share_config: Dict[str, Any],
        recipients: List[str] = None
    ) -> Dict[str, Any]:
        """Share dashboard with other users"""
        share_data = {
            'share_config': share_config,
            'recipients': recipients or []
        }
        
        return await self.client.post(
            f'/visualization/dashboards/{dashboard_id}/share',
            data=share_data
        )
    
    async def create_public_link(
        self,
        visualization_id: str,
        expiration: datetime = None,
        permissions: List[str] = None
    ) -> Dict[str, Any]:
        """Create public link for visualization"""
        link_data = {
            'permissions': permissions or ['view']
        }
        
        if expiration:
            link_data['expiration'] = expiration.isoformat()
        
        return await self.client.post(
            f'/visualization/{visualization_id}/public-link',
            data=link_data
        )
    
    # Visualization Templates
    async def get_visualization_templates(
        self,
        category: str = None,
        visualization_type: Union[str, VisualizationType] = None
    ) -> List[Dict[str, Any]]:
        """Get available visualization templates"""
        params = {}
        
        if category:
            params['category'] = category
        if visualization_type:
            if isinstance(visualization_type, VisualizationType):
                visualization_type = visualization_type.value
            params['visualization_type'] = visualization_type
        
        return await self.client.get('/visualization/templates', params=params)
    
    async def create_from_template(
        self,
        template_id: str,
        data_source: Dict[str, Any],
        customizations: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create visualization from template"""
        creation_data = {
            'template_id': template_id,
            'data_source': data_source,
            'customizations': customizations or {}
        }
        
        return await self.client.post('/visualization/from-template', data=creation_data)
    
    async def save_as_template(
        self,
        visualization_id: str,
        template_name: str,
        description: str = None,
        is_public: bool = False
    ) -> Dict[str, Any]:
        """Save visualization as template"""
        template_data = {
            'template_name': template_name,
            'description': description,
            'is_public': is_public
        }
        
        return await self.client.post(
            f'/visualization/{visualization_id}/save-template',
            data=template_data
        )