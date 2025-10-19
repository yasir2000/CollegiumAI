"""
Visualization Framework Package
==============================

Multi-agent visualization and dashboard components
"""

from .multi_agent_dashboard import (
    MultiAgentVisualizationDashboard,
    NetworkTopologyAnalyzer,
    PerformanceAnalyzer,
    TaskFlowVisualizer,
    AgentNode,
    TaskNode,
    CommunicationEvent,
    CollaborationPattern,
    AgentStatus,
    TaskStatus,
    CommunicationType,
    PerformanceMetric,
    create_sample_agents,
    create_sample_tasks,
    create_sample_communications
)

# Optional real-time components (requires websockets)
try:
    from .realtime_communication import (
        RealTimeVisualizationServer,
        NetworkGraphGenerator,
        TaskFlowDiagramGenerator,
        PerformanceChartGenerator,
        create_visualization_server
    )
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False
    
    # Provide fallback classes
    class RealTimeVisualizationServer:
        def __init__(self, *args, **kwargs):
            raise ImportError("websockets package required for real-time visualization")
    
    class NetworkGraphGenerator:
        @staticmethod
        def generate_network_graph(*args, **kwargs):
            raise ImportError("websockets package required for network graph generation")
    
    class TaskFlowDiagramGenerator:
        @staticmethod
        def generate_task_flow_diagram(*args, **kwargs):
            raise ImportError("websockets package required for task flow diagrams")
    
    class PerformanceChartGenerator:
        @staticmethod
        def generate_performance_charts(*args, **kwargs):
            raise ImportError("websockets package required for performance charts")
    
    def create_visualization_server(*args, **kwargs):
        raise ImportError("websockets package required for visualization server")

__all__ = [
    # Core dashboard components
    'MultiAgentVisualizationDashboard',
    'NetworkTopologyAnalyzer',
    'PerformanceAnalyzer',
    'TaskFlowVisualizer',
    
    # Data structures
    'AgentNode',
    'TaskNode',
    'CommunicationEvent',
    'CollaborationPattern',
    
    # Enums
    'AgentStatus',
    'TaskStatus',
    'CommunicationType',
    'PerformanceMetric',
    
    # Real-time components (optional)
    'RealTimeVisualizationServer',
    'NetworkGraphGenerator',
    'TaskFlowDiagramGenerator',
    'PerformanceChartGenerator',
    'create_visualization_server',
    
    # Utilities
    'create_sample_agents',
    'create_sample_tasks',
    'create_sample_communications',
    
    # Feature availability
    'REALTIME_AVAILABLE'
]

# Version info
__version__ = '1.0.0'
__author__ = 'CollegiumAI Team'
__description__ = 'Multi-agent visualization and dashboard system'