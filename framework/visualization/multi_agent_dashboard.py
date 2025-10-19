"""
Enhanced Multi-Agent Visualization System
========================================

Advanced dashboard for multi-agent coordination providing:
- Real-time agent communication visualization
- Task flow diagrams and dependency tracking
- Performance metrics and analytics
- Collaboration analytics and optimization
- Network topology visualization
- Agent behavior pattern analysis
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid
import numpy as np
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    INITIALIZING = "initializing"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"

class CommunicationType(Enum):
    DIRECT_MESSAGE = "direct_message"
    BROADCAST = "broadcast"
    TASK_ASSIGNMENT = "task_assignment"
    RESOURCE_REQUEST = "resource_request"
    STATUS_UPDATE = "status_update"
    COLLABORATION_INVITE = "collaboration_invite"
    DATA_EXCHANGE = "data_exchange"

class PerformanceMetric(Enum):
    TASK_COMPLETION_TIME = "task_completion_time"
    SUCCESS_RATE = "success_rate"
    COMMUNICATION_EFFICIENCY = "communication_efficiency"
    RESOURCE_UTILIZATION = "resource_utilization"
    COLLABORATION_SCORE = "collaboration_score"
    RELIABILITY_INDEX = "reliability_index"

@dataclass
class AgentNode:
    """Agent representation in the visualization system"""
    agent_id: str
    agent_name: str
    agent_type: str
    status: AgentStatus
    position: Tuple[float, float]  # For graph layout
    capabilities: List[str]
    current_tasks: List[str]
    performance_metrics: Dict[str, float]
    connections: Set[str]  # Connected agent IDs
    last_activity: datetime
    load_factor: float  # 0.0 to 1.0
    health_score: float  # 0.0 to 1.0
    
    def __post_init__(self):
        if isinstance(self.connections, list):
            self.connections = set(self.connections)

@dataclass
class TaskNode:
    """Task representation in the visualization system"""
    task_id: str
    task_name: str
    task_type: str
    status: TaskStatus
    assigned_agents: List[str]
    dependencies: List[str]  # Task IDs this task depends on
    priority: int  # 1-10, 10 being highest
    estimated_duration: float  # in hours
    actual_duration: Optional[float]
    progress: float  # 0.0 to 1.0
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    resource_requirements: Dict[str, Any]
    success_criteria: List[str]

@dataclass
class CommunicationEvent:
    """Communication event between agents"""
    event_id: str
    timestamp: datetime
    sender_id: str
    receiver_id: str
    communication_type: CommunicationType
    message_content: str
    task_context: Optional[str]
    response_time: Optional[float]
    success: bool
    metadata: Dict[str, Any]

@dataclass
class CollaborationPattern:
    """Identified collaboration pattern"""
    pattern_id: str
    pattern_name: str
    participating_agents: List[str]
    pattern_type: str  # "sequential", "parallel", "hierarchical", "peer-to-peer"
    frequency: int
    success_rate: float
    average_duration: float
    efficiency_score: float
    identified_at: datetime

class NetworkTopologyAnalyzer:
    """Analyzes multi-agent network topology and relationships"""
    
    def __init__(self):
        self.agent_graph = {}
        self.communication_patterns = {}
        self.collaboration_clusters = []
        self.influence_scores = {}
    
    def update_network_topology(self, agents: List[AgentNode], communications: List[CommunicationEvent]):
        """Update network topology based on current agent states and communications"""
        
        # Build adjacency graph
        self.agent_graph = {agent.agent_id: set() for agent in agents}
        
        # Add connections based on communications
        for comm in communications:
            if comm.success and comm.timestamp > datetime.utcnow() - timedelta(hours=24):
                self.agent_graph[comm.sender_id].add(comm.receiver_id)
                self.agent_graph[comm.receiver_id].add(comm.sender_id)
        
        # Calculate influence scores
        self._calculate_influence_scores(agents, communications)
        
        # Identify collaboration clusters
        self._identify_collaboration_clusters(agents, communications)
        
        # Analyze communication patterns
        self._analyze_communication_patterns(communications)
    
    def _calculate_influence_scores(self, agents: List[AgentNode], communications: List[CommunicationEvent]):
        """Calculate influence scores for each agent"""
        
        # Initialize scores
        self.influence_scores = {agent.agent_id: 0.0 for agent in agents}
        
        # Communication-based influence
        for comm in communications:
            if comm.success:
                # Sender gets influence for initiating communication
                self.influence_scores[comm.sender_id] += 0.1
                
                # Task assignments give more influence
                if comm.communication_type == CommunicationType.TASK_ASSIGNMENT:
                    self.influence_scores[comm.sender_id] += 0.5
        
        # Network centrality-based influence
        for agent_id, connections in self.agent_graph.items():
            # Degree centrality
            degree_score = len(connections) / max(len(self.agent_graph) - 1, 1)
            self.influence_scores[agent_id] += degree_score * 0.3
        
        # Performance-based influence
        for agent in agents:
            performance_score = agent.performance_metrics.get('success_rate', 0.5)
            self.influence_scores[agent.agent_id] += performance_score * 0.2
        
        # Normalize scores
        max_score = max(self.influence_scores.values()) if self.influence_scores.values() else 1.0
        for agent_id in self.influence_scores:
            self.influence_scores[agent_id] = self.influence_scores[agent_id] / max_score
    
    def _identify_collaboration_clusters(self, agents: List[AgentNode], communications: List[CommunicationEvent]):
        """Identify clusters of frequently collaborating agents"""
        
        # Build collaboration frequency matrix
        collaboration_freq = defaultdict(lambda: defaultdict(int))
        
        for comm in communications:
            if comm.success and comm.timestamp > datetime.utcnow() - timedelta(days=7):
                collaboration_freq[comm.sender_id][comm.receiver_id] += 1
                collaboration_freq[comm.receiver_id][comm.sender_id] += 1
        
        # Simple clustering based on communication frequency
        visited = set()
        self.collaboration_clusters = []
        
        for agent in agents:
            if agent.agent_id not in visited:
                cluster = self._find_cluster(agent.agent_id, collaboration_freq, visited, threshold=5)
                if len(cluster) > 1:
                    self.collaboration_clusters.append(cluster)
    
    def _find_cluster(self, start_agent: str, freq_matrix: Dict, visited: Set, threshold: int) -> List[str]:
        """Find collaboration cluster starting from an agent"""
        cluster = []
        queue = deque([start_agent])
        
        while queue:
            agent_id = queue.popleft()
            if agent_id in visited:
                continue
            
            visited.add(agent_id)
            cluster.append(agent_id)
            
            # Add connected agents that meet frequency threshold
            for connected_agent, freq in freq_matrix[agent_id].items():
                if freq >= threshold and connected_agent not in visited:
                    queue.append(connected_agent)
        
        return cluster
    
    def _analyze_communication_patterns(self, communications: List[CommunicationEvent]):
        """Analyze communication patterns"""
        
        # Group communications by hour to find temporal patterns
        hourly_patterns = defaultdict(int)
        type_patterns = defaultdict(int)
        
        for comm in communications:
            hour = comm.timestamp.hour
            hourly_patterns[hour] += 1
            type_patterns[comm.communication_type.value] += 1
        
        self.communication_patterns = {
            "hourly_distribution": dict(hourly_patterns),
            "type_distribution": dict(type_patterns),
            "peak_hours": sorted(hourly_patterns.items(), key=lambda x: x[1], reverse=True)[:3],
            "most_common_types": sorted(type_patterns.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """Get comprehensive network metrics"""
        
        if not self.agent_graph:
            return {"error": "No network data available"}
        
        total_agents = len(self.agent_graph)
        total_connections = sum(len(connections) for connections in self.agent_graph.values()) // 2
        
        # Calculate network density
        max_connections = total_agents * (total_agents - 1) // 2
        network_density = total_connections / max_connections if max_connections > 0 else 0
        
        # Find most connected agents
        connection_counts = {agent_id: len(connections) for agent_id, connections in self.agent_graph.items()}
        most_connected = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_agents": total_agents,
            "total_connections": total_connections,
            "network_density": network_density,
            "collaboration_clusters": len(self.collaboration_clusters),
            "cluster_details": self.collaboration_clusters,
            "most_connected_agents": most_connected,
            "influence_scores": self.influence_scores,
            "communication_patterns": self.communication_patterns
        }
    
    def analyze_network_topology(self, agents: List[AgentNode], communications: List[CommunicationEvent]) -> Dict[str, Any]:
        """Analyze network topology and return metrics"""
        
        # Update the network topology first
        self.update_network_topology(agents, communications)
        
        # Return the network metrics
        return self.get_network_metrics()

class PerformanceAnalyzer:
    """Analyzes agent and system performance metrics"""
    
    def __init__(self):
        self.performance_history = defaultdict(lambda: defaultdict(list))
        self.system_metrics = {}
        self.benchmark_data = {}
    
    def update_performance_metrics(
        self,
        agents: List[AgentNode],
        tasks: List[TaskNode],
        communications: List[CommunicationEvent]
    ):
        """Update performance metrics for all components"""
        
        current_time = datetime.utcnow()
        
        # Agent performance metrics
        for agent in agents:
            agent_metrics = self._calculate_agent_performance(agent, tasks, communications)
            
            for metric_name, value in agent_metrics.items():
                self.performance_history[agent.agent_id][metric_name].append({
                    "timestamp": current_time,
                    "value": value
                })
        
        # System-wide metrics
        self.system_metrics = self._calculate_system_metrics(agents, tasks, communications)
        
        # Clean old performance data (keep last 30 days)
        self._cleanup_old_metrics(current_time - timedelta(days=30))
    
    def _calculate_agent_performance(
        self,
        agent: AgentNode,
        tasks: List[TaskNode],
        communications: List[CommunicationEvent]
    ) -> Dict[str, float]:
        """Calculate performance metrics for a specific agent"""
        
        # Get agent's tasks
        agent_tasks = [task for task in tasks if agent.agent_id in task.assigned_agents]
        
        # Task completion metrics
        completed_tasks = [task for task in agent_tasks if task.status == TaskStatus.COMPLETED]
        failed_tasks = [task for task in agent_tasks if task.status == TaskStatus.FAILED]
        
        success_rate = len(completed_tasks) / max(len(agent_tasks), 1)
        
        # Average task completion time
        completion_times = []
        for task in completed_tasks:
            if task.started_at and task.completed_at:
                duration = (task.completed_at - task.started_at).total_seconds() / 3600  # hours
                completion_times.append(duration)
        
        avg_completion_time = np.mean(completion_times) if completion_times else 0.0
        
        # Communication efficiency
        agent_communications = [
            comm for comm in communications 
            if comm.sender_id == agent.agent_id or comm.receiver_id == agent.agent_id
        ]
        
        successful_comms = [comm for comm in agent_communications if comm.success]
        communication_efficiency = len(successful_comms) / max(len(agent_communications), 1)
        
        # Response time analysis
        response_times = [
            comm.response_time for comm in successful_comms 
            if comm.response_time is not None
        ]
        avg_response_time = np.mean(response_times) if response_times else 0.0
        
        # Resource utilization
        resource_utilization = agent.load_factor
        
        # Collaboration score (based on number of successful collaborations)
        collaboration_count = len([
            comm for comm in successful_comms 
            if comm.communication_type in [CommunicationType.COLLABORATION_INVITE, CommunicationType.DATA_EXCHANGE]
        ])
        collaboration_score = min(collaboration_count / 10.0, 1.0)  # Normalized to max 10 collaborations
        
        return {
            PerformanceMetric.SUCCESS_RATE.value: success_rate,
            PerformanceMetric.TASK_COMPLETION_TIME.value: avg_completion_time,
            PerformanceMetric.COMMUNICATION_EFFICIENCY.value: communication_efficiency,
            PerformanceMetric.RESOURCE_UTILIZATION.value: resource_utilization,
            PerformanceMetric.COLLABORATION_SCORE.value: collaboration_score,
            PerformanceMetric.RELIABILITY_INDEX.value: agent.health_score,
            "avg_response_time": avg_response_time,
            "total_tasks": len(agent_tasks),
            "completed_tasks": len(completed_tasks),
            "failed_tasks": len(failed_tasks)
        }
    
    def _calculate_system_metrics(
        self,
        agents: List[AgentNode],
        tasks: List[TaskNode],
        communications: List[CommunicationEvent]
    ) -> Dict[str, Any]:
        """Calculate system-wide performance metrics"""
        
        # Overall system health
        active_agents = [agent for agent in agents if agent.status == AgentStatus.ACTIVE]
        system_health = len(active_agents) / max(len(agents), 1)
        
        # Task throughput
        completed_tasks = [task for task in tasks if task.status == TaskStatus.COMPLETED]
        recent_completions = [
            task for task in completed_tasks 
            if task.completed_at and task.completed_at > datetime.utcnow() - timedelta(hours=24)
        ]
        task_throughput = len(recent_completions)  # Tasks completed in last 24 hours
        
        # Average task completion time
        completion_times = []
        for task in completed_tasks:
            if task.started_at and task.completed_at:
                duration = (task.completed_at - task.started_at).total_seconds() / 3600
                completion_times.append(duration)
        
        avg_system_completion_time = np.mean(completion_times) if completion_times else 0.0
        
        # Communication volume and success rate
        recent_communications = [
            comm for comm in communications 
            if comm.timestamp > datetime.utcnow() - timedelta(hours=24)
        ]
        successful_communications = [comm for comm in recent_communications if comm.success]
        
        communication_success_rate = len(successful_communications) / max(len(recent_communications), 1)
        communication_volume = len(recent_communications)
        
        # Load distribution
        load_factors = [agent.load_factor for agent in agents]
        load_std_dev = np.std(load_factors) if load_factors else 0.0
        avg_load = np.mean(load_factors) if load_factors else 0.0
        
        # Error rates
        failed_tasks = [task for task in tasks if task.status == TaskStatus.FAILED]
        task_failure_rate = len(failed_tasks) / max(len(tasks), 1)
        
        return {
            "system_health": system_health,
            "active_agents": len(active_agents),
            "total_agents": len(agents),
            "task_throughput_24h": task_throughput,
            "avg_completion_time": avg_system_completion_time,
            "communication_success_rate": communication_success_rate,
            "communication_volume_24h": communication_volume,
            "avg_system_load": avg_load,
            "load_distribution_std": load_std_dev,
            "task_failure_rate": task_failure_rate,
            "total_tasks": len(tasks),
            "completed_tasks": len(completed_tasks),
            "pending_tasks": len([task for task in tasks if task.status == TaskStatus.PENDING]),
            "in_progress_tasks": len([task for task in tasks if task.status == TaskStatus.IN_PROGRESS])
        }
    
    def _cleanup_old_metrics(self, cutoff_date: datetime):
        """Clean up old performance metrics"""
        for agent_id in self.performance_history:
            for metric_name in self.performance_history[agent_id]:
                self.performance_history[agent_id][metric_name] = [
                    entry for entry in self.performance_history[agent_id][metric_name]
                    if entry["timestamp"] > cutoff_date
                ]
    
    def get_performance_trends(self, agent_id: str = None, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get performance trends for an agent or the entire system"""
        
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        
        if agent_id:
            # Agent-specific trends
            if agent_id not in self.performance_history:
                return {"error": f"No performance data for agent {agent_id}"}
            
            agent_data = {}
            for metric_name, entries in self.performance_history[agent_id].items():
                recent_entries = [
                    entry for entry in entries if entry["timestamp"] > cutoff_time
                ]
                
                if recent_entries:
                    values = [entry["value"] for entry in recent_entries]
                    agent_data[metric_name] = {
                        "current": values[-1] if values else 0,
                        "average": np.mean(values),
                        "trend": "improving" if len(values) > 1 and values[-1] > values[0] else "declining",
                        "data_points": len(values)
                    }
            
            return {"agent_id": agent_id, "metrics": agent_data}
        
        else:
            # System-wide trends
            return {"system_metrics": self.system_metrics}
    
    def identify_performance_anomalies(self) -> List[Dict[str, Any]]:
        """Identify performance anomalies and issues"""
        
        anomalies = []
        
        # Check for agents with low performance
        for agent_id, metrics in self.performance_history.items():
            success_rate_data = metrics.get(PerformanceMetric.SUCCESS_RATE.value, [])
            if success_rate_data:
                recent_success_rate = success_rate_data[-1]["value"] if success_rate_data else 0
                if recent_success_rate < 0.7:  # Less than 70% success rate
                    anomalies.append({
                        "type": "low_performance",
                        "agent_id": agent_id,
                        "metric": "success_rate",
                        "value": recent_success_rate,
                        "severity": "high" if recent_success_rate < 0.5 else "medium"
                    })
            
            # Check for high response times
            response_time_data = metrics.get("avg_response_time", [])
            if response_time_data:
                recent_response_time = response_time_data[-1]["value"] if response_time_data else 0
                if recent_response_time > 5.0:  # More than 5 seconds
                    anomalies.append({
                        "type": "high_response_time",
                        "agent_id": agent_id,
                        "metric": "response_time",
                        "value": recent_response_time,
                        "severity": "medium"
                    })
        
        # System-level anomalies
        if self.system_metrics:
            if self.system_metrics.get("system_health", 1.0) < 0.8:
                anomalies.append({
                    "type": "system_health_degradation",
                    "metric": "system_health",
                    "value": self.system_metrics["system_health"],
                    "severity": "high"
                })
            
            if self.system_metrics.get("communication_success_rate", 1.0) < 0.9:
                anomalies.append({
                    "type": "communication_issues",
                    "metric": "communication_success_rate",
                    "value": self.system_metrics["communication_success_rate"],
                    "severity": "medium"
                })
        
        return anomalies

class TaskFlowVisualizer:
    """Visualizes task dependencies and flows"""
    
    def __init__(self):
        self.task_graph = {}
        self.critical_paths = []
        self.bottlenecks = []
    
    def build_task_flow_graph(self, tasks: List[TaskNode]) -> Dict[str, Any]:
        """Build task flow graph with dependencies"""
        
        # Build adjacency graph for tasks
        self.task_graph = {task.task_id: {
            "task": task,
            "dependencies": set(task.dependencies),
            "dependents": set()
        } for task in tasks}
        
        # Build reverse dependencies (dependents)
        for task_id, task_data in self.task_graph.items():
            for dep_id in task_data["dependencies"]:
                if dep_id in self.task_graph:
                    self.task_graph[dep_id]["dependents"].add(task_id)
        
        # Identify critical paths
        self._identify_critical_paths()
        
        # Identify bottlenecks
        self._identify_bottlenecks()
        
        return {
            "task_graph": self._serialize_task_graph(),
            "critical_paths": self.critical_paths,
            "bottlenecks": self.bottlenecks,
            "flow_metrics": self._calculate_flow_metrics()
        }
    
    def _identify_critical_paths(self):
        """Identify critical paths in task flow"""
        
        # Find tasks with no dependencies (start tasks)
        start_tasks = [
            task_id for task_id, task_data in self.task_graph.items()
            if not task_data["dependencies"]
        ]
        
        # Find tasks with no dependents (end tasks)
        end_tasks = [
            task_id for task_id, task_data in self.task_graph.items()
            if not task_data["dependents"]
        ]
        
        # Calculate longest paths from start to end tasks
        self.critical_paths = []
        for start_task in start_tasks:
            for end_task in end_tasks:
                path = self._find_longest_path(start_task, end_task)
                if path:
                    path_duration = sum(
                        self.task_graph[task_id]["task"].estimated_duration 
                        for task_id in path
                    )
                    self.critical_paths.append({
                        "path": path,
                        "duration": path_duration,
                        "start_task": start_task,
                        "end_task": end_task
                    })
        
        # Sort by duration (longest first)
        self.critical_paths.sort(key=lambda x: x["duration"], reverse=True)
    
    def _find_longest_path(self, start: str, end: str) -> List[str]:
        """Find longest path between two tasks using dynamic programming"""
        
        # Simple DFS approach for longest path (works for DAG)
        def dfs(current, target, visited, path):
            if current == target:
                return path + [current]
            
            visited.add(current)
            longest = []
            
            for dependent in self.task_graph[current]["dependents"]:
                if dependent not in visited:
                    candidate_path = dfs(dependent, target, visited.copy(), path + [current])
                    if len(candidate_path) > len(longest):
                        longest = candidate_path
            
            return longest
        
        return dfs(start, end, set(), [])
    
    def _identify_bottlenecks(self):
        """Identify bottleneck tasks that could delay the entire flow"""
        
        self.bottlenecks = []
        
        for task_id, task_data in self.task_graph.items():
            task = task_data["task"]
            
            # Tasks with many dependents are potential bottlenecks
            dependent_count = len(task_data["dependents"])
            
            # Tasks taking longer than average are bottlenecks
            avg_duration = np.mean([
                t["task"].estimated_duration for t in self.task_graph.values()
            ])
            
            is_bottleneck = (
                dependent_count > 2 or  # Has many dependents
                task.estimated_duration > avg_duration * 1.5 or  # Takes much longer than average
                task.status == TaskStatus.BLOCKED  # Currently blocked
            )
            
            if is_bottleneck:
                self.bottlenecks.append({
                    "task_id": task_id,
                    "task_name": task.task_name,
                    "dependent_count": dependent_count,
                    "estimated_duration": task.estimated_duration,
                    "status": task.status.value,
                    "bottleneck_score": dependent_count + (task.estimated_duration / avg_duration),
                    "reason": self._get_bottleneck_reason(task, dependent_count, avg_duration)
                })
        
        # Sort by bottleneck score
        self.bottlenecks.sort(key=lambda x: x["bottleneck_score"], reverse=True)
    
    def _get_bottleneck_reason(self, task: TaskNode, dependent_count: int, avg_duration: float) -> str:
        """Get reason why task is considered a bottleneck"""
        reasons = []
        
        if dependent_count > 2:
            reasons.append(f"High dependency count ({dependent_count} dependents)")
        
        if task.estimated_duration > avg_duration * 1.5:
            reasons.append(f"Long duration ({task.estimated_duration:.1f}h vs {avg_duration:.1f}h avg)")
        
        if task.status == TaskStatus.BLOCKED:
            reasons.append("Currently blocked")
        
        return "; ".join(reasons)
    
    def _serialize_task_graph(self) -> Dict[str, Any]:
        """Serialize task graph for visualization"""
        serialized = {}
        
        for task_id, task_data in self.task_graph.items():
            task = task_data["task"]
            serialized[task_id] = {
                "task_name": task.task_name,
                "status": task.status.value,
                "progress": task.progress,
                "estimated_duration": task.estimated_duration,
                "assigned_agents": task.assigned_agents,
                "dependencies": list(task_data["dependencies"]),
                "dependents": list(task_data["dependents"]),
                "priority": task.priority
            }
        
        return serialized
    
    def _calculate_flow_metrics(self) -> Dict[str, Any]:
        """Calculate task flow metrics"""
        
        total_tasks = len(self.task_graph)
        completed_tasks = len([
            task_data for task_data in self.task_graph.values()
            if task_data["task"].status == TaskStatus.COMPLETED
        ])
        
        blocked_tasks = len([
            task_data for task_data in self.task_graph.values()
            if task_data["task"].status == TaskStatus.BLOCKED
        ])
        
        # Calculate overall progress
        total_progress = sum(
            task_data["task"].progress for task_data in self.task_graph.values()
        )
        overall_progress = total_progress / max(total_tasks, 1)
        
        # Estimate completion time based on critical path
        estimated_completion = max(
            path["duration"] for path in self.critical_paths
        ) if self.critical_paths else 0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "blocked_tasks": blocked_tasks,
            "overall_progress": overall_progress,
            "completion_rate": completed_tasks / max(total_tasks, 1),
            "estimated_completion_time": estimated_completion,
            "bottleneck_count": len(self.bottlenecks),
            "critical_path_count": len(self.critical_paths)
        }

class MultiAgentVisualizationDashboard:
    """Main dashboard for multi-agent visualization"""
    
    def __init__(self):
        self.topology_analyzer = NetworkTopologyAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.task_flow_visualizer = TaskFlowVisualizer()
        
        # Dashboard state
        self.agents = []
        self.tasks = []
        self.communications = []
        self.last_update = None
    
    async def update_dashboard_data(
        self,
        agents: List[AgentNode],
        tasks: List[TaskNode],
        communications: List[CommunicationEvent]
    ):
        """Update all dashboard data"""
        
        self.agents = agents
        self.tasks = tasks
        self.communications = communications
        self.last_update = datetime.utcnow()
        
        # Update all analyzers
        self.topology_analyzer.update_network_topology(agents, communications)
        self.performance_analyzer.update_performance_metrics(agents, tasks, communications)
        
        logger.info(f"Dashboard updated with {len(agents)} agents, {len(tasks)} tasks, {len(communications)} communications")
    
    async def get_dashboard_overview(self) -> Dict[str, Any]:
        """Get comprehensive dashboard overview"""
        
        if not self.agents:
            return {"error": "No dashboard data available"}
        
        # Network metrics
        network_metrics = self.topology_analyzer.get_network_metrics()
        
        # Performance overview
        system_performance = self.performance_analyzer.system_metrics
        performance_anomalies = self.performance_analyzer.identify_performance_anomalies()
        
        # Task flow analysis
        task_flow_data = self.task_flow_visualizer.build_task_flow_graph(self.tasks)
        
        # Agent status summary
        agent_status_summary = self._get_agent_status_summary()
        
        # Communication summary
        communication_summary = self._get_communication_summary()
        
        return {
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "overview": {
                "total_agents": len(self.agents),
                "active_agents": len([a for a in self.agents if a.status == AgentStatus.ACTIVE]),
                "total_tasks": len(self.tasks),
                "completed_tasks": len([t for t in self.tasks if t.status == TaskStatus.COMPLETED]),
                "total_communications": len(self.communications)
            },
            "network_analysis": network_metrics,
            "performance_analysis": {
                "system_metrics": system_performance,
                "anomalies": performance_anomalies,
                "anomaly_count": len(performance_anomalies)
            },
            "task_flow_analysis": task_flow_data,
            "agent_status": agent_status_summary,
            "communication_analysis": communication_summary
        }
    
    def _get_agent_status_summary(self) -> Dict[str, Any]:
        """Get agent status summary"""
        
        status_counts = defaultdict(int)
        capability_counts = defaultdict(int)
        
        total_load = 0
        total_health = 0
        
        for agent in self.agents:
            status_counts[agent.status.value] += 1
            total_load += agent.load_factor
            total_health += agent.health_score
            
            for capability in agent.capabilities:
                capability_counts[capability] += 1
        
        return {
            "status_distribution": dict(status_counts),
            "capability_distribution": dict(capability_counts),
            "average_load": total_load / len(self.agents),
            "average_health": total_health / len(self.agents),
            "most_common_capabilities": sorted(
                capability_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }
    
    def _get_communication_summary(self) -> Dict[str, Any]:
        """Get communication summary"""
        
        if not self.communications:
            return {"total": 0, "success_rate": 0}
        
        # Recent communications (last 24 hours)
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_comms = [
            comm for comm in self.communications 
            if comm.timestamp > recent_cutoff
        ]
        
        successful_comms = [comm for comm in recent_comms if comm.success]
        
        # Communication types
        type_counts = defaultdict(int)
        for comm in recent_comms:
            type_counts[comm.communication_type.value] += 1
        
        # Response time analysis
        response_times = [
            comm.response_time for comm in successful_comms 
            if comm.response_time is not None
        ]
        
        return {
            "total_24h": len(recent_comms),
            "successful_24h": len(successful_comms),
            "success_rate": len(successful_comms) / max(len(recent_comms), 1),
            "type_distribution": dict(type_counts),
            "average_response_time": np.mean(response_times) if response_times else 0,
            "communication_volume_trend": self._calculate_communication_trend()
        }
    
    def _calculate_communication_trend(self) -> str:
        """Calculate communication volume trend"""
        
        if len(self.communications) < 10:
            return "insufficient_data"
        
        # Compare last 12 hours with previous 12 hours
        now = datetime.utcnow()
        recent_12h = [
            comm for comm in self.communications 
            if now - timedelta(hours=12) <= comm.timestamp <= now
        ]
        previous_12h = [
            comm for comm in self.communications 
            if now - timedelta(hours=24) <= comm.timestamp <= now - timedelta(hours=12)
        ]
        
        recent_count = len(recent_12h)
        previous_count = len(previous_12h)
        
        if previous_count == 0:
            return "increasing" if recent_count > 0 else "stable"
        
        change_ratio = recent_count / previous_count
        
        if change_ratio > 1.2:
            return "increasing"
        elif change_ratio < 0.8:
            return "decreasing"
        else:
            return "stable"
    
    async def get_agent_details(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific agent"""
        
        agent = next((a for a in self.agents if a.agent_id == agent_id), None)
        if not agent:
            return {"error": f"Agent {agent_id} not found"}
        
        # Get agent's tasks
        agent_tasks = [task for task in self.tasks if agent_id in task.assigned_agents]
        
        # Get agent's communications
        agent_communications = [
            comm for comm in self.communications 
            if comm.sender_id == agent_id or comm.receiver_id == agent_id
        ]
        
        # Performance trends
        performance_trends = self.performance_analyzer.get_performance_trends(agent_id)
        
        return {
            "agent_info": asdict(agent),
            "current_tasks": [asdict(task) for task in agent_tasks],
            "recent_communications": [asdict(comm) for comm in agent_communications[-10:]],  # Last 10
            "performance_trends": performance_trends,
            "network_position": {
                "connections": list(agent.connections),
                "influence_score": self.topology_analyzer.influence_scores.get(agent_id, 0),
                "collaboration_clusters": [
                    cluster for cluster in self.topology_analyzer.collaboration_clusters 
                    if agent_id in cluster
                ]
            }
        }
    
    async def get_task_details(self, task_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific task"""
        
        task = next((t for t in self.tasks if t.task_id == task_id), None)
        if not task:
            return {"error": f"Task {task_id} not found"}
        
        # Get task dependencies and dependents
        task_graph_data = self.task_flow_visualizer.task_graph.get(task_id, {})
        
        # Get assigned agents details
        assigned_agents = [
            asdict(agent) for agent in self.agents 
            if agent.agent_id in task.assigned_agents
        ]
        
        return {
            "task_info": asdict(task),
            "assigned_agents": assigned_agents,
            "dependencies": list(task_graph_data.get("dependencies", [])),
            "dependents": list(task_graph_data.get("dependents", [])),
            "is_bottleneck": any(
                bottleneck["task_id"] == task_id 
                for bottleneck in self.task_flow_visualizer.bottlenecks
            ),
            "in_critical_path": any(
                task_id in path["path"] 
                for path in self.task_flow_visualizer.critical_paths
            )
        }

# Utility functions for creating sample data
def create_sample_agents(count: int = 5) -> List[AgentNode]:
    """Create sample agents for testing"""
    
    agents = []
    agent_types = ["academic", "administrative", "research", "analysis", "coordination"]
    capabilities_pool = [
        "data_analysis", "document_processing", "communication", "task_management",
        "research", "content_generation", "quality_assurance", "collaboration"
    ]
    
    for i in range(count):
        agent = AgentNode(
            agent_id=f"agent_{i+1}",
            agent_name=f"Agent {i+1}",
            agent_type=agent_types[i % len(agent_types)],
            status=AgentStatus.ACTIVE,
            position=(np.random.uniform(0, 100), np.random.uniform(0, 100)),
            capabilities=np.random.choice(capabilities_pool, size=3, replace=False).tolist(),
            current_tasks=[f"task_{j}" for j in range(np.random.randint(1, 4))],
            performance_metrics={
                "success_rate": np.random.uniform(0.7, 0.95),
                "avg_completion_time": np.random.uniform(1.0, 8.0)
            },
            connections=set(),
            last_activity=datetime.utcnow() - timedelta(minutes=np.random.randint(0, 60)),
            load_factor=np.random.uniform(0.3, 0.9),
            health_score=np.random.uniform(0.8, 1.0)
        )
        agents.append(agent)
    
    return agents

def create_sample_tasks(count: int = 10) -> List[TaskNode]:
    """Create sample tasks for testing"""
    
    tasks = []
    task_types = ["analysis", "processing", "research", "coordination", "review"]
    
    for i in range(count):
        # Create some dependencies (later tasks depend on earlier ones)
        dependencies = []
        if i > 2:
            dep_count = np.random.randint(0, min(3, i))
            dependencies = [f"task_{j+1}" for j in np.random.choice(i, dep_count, replace=False)]
        
        task = TaskNode(
            task_id=f"task_{i+1}",
            task_name=f"Task {i+1}: {task_types[i % len(task_types)]}",
            task_type=task_types[i % len(task_types)],
            status=np.random.choice(list(TaskStatus)),
            assigned_agents=[f"agent_{np.random.randint(1, 6)}"],
            dependencies=dependencies,
            priority=np.random.randint(1, 11),
            estimated_duration=np.random.uniform(2.0, 12.0),
            actual_duration=np.random.uniform(1.5, 15.0) if np.random.random() > 0.5 else None,
            progress=np.random.uniform(0.0, 1.0),
            created_at=datetime.utcnow() - timedelta(days=np.random.randint(1, 30)),
            started_at=datetime.utcnow() - timedelta(days=np.random.randint(0, 15)) if np.random.random() > 0.3 else None,
            completed_at=datetime.utcnow() - timedelta(days=np.random.randint(0, 10)) if np.random.random() > 0.6 else None,
            resource_requirements={"cpu": np.random.uniform(0.1, 1.0), "memory": np.random.uniform(0.5, 4.0)},
            success_criteria=["criterion_1", "criterion_2"]
        )
        tasks.append(task)
    
    return tasks

def create_sample_communications(agents: List[AgentNode], count: int = 50) -> List[CommunicationEvent]:
    """Create sample communications for testing"""
    
    communications = []
    
    for i in range(count):
        sender = np.random.choice(agents)
        receiver = np.random.choice([a for a in agents if a.agent_id != sender.agent_id])
        
        comm = CommunicationEvent(
            event_id=f"comm_{i+1}",
            timestamp=datetime.utcnow() - timedelta(minutes=np.random.randint(0, 1440)),  # Last 24 hours
            sender_id=sender.agent_id,
            receiver_id=receiver.agent_id,
            communication_type=np.random.choice(list(CommunicationType)),
            message_content=f"Sample message {i+1}",
            task_context=f"task_{np.random.randint(1, 11)}" if np.random.random() > 0.5 else None,
            response_time=np.random.uniform(0.1, 10.0) if np.random.random() > 0.2 else None,
            success=np.random.random() > 0.1,  # 90% success rate
            metadata={"priority": "normal", "category": "operational"}
        )
        communications.append(comm)
    
    return communications

class CollaborationAnalyzer:
    """Analyzes collaboration patterns between agents"""
    
    def analyze_collaboration_patterns(
        self, 
        agents: List[AgentNode], 
        communications: List[CommunicationEvent]
    ) -> Dict[str, Any]:
        """Analyze collaboration patterns between agents"""
        
        # Build collaboration matrix
        agent_ids = [agent.agent_id for agent in agents]
        collaboration_matrix = {}
        
        for agent_id in agent_ids:
            collaboration_matrix[agent_id] = {}
            for other_id in agent_ids:
                collaboration_matrix[agent_id][other_id] = 0
        
        # Count communications
        for comm in communications:
            if comm.sender_id in agent_ids and comm.receiver_id in agent_ids:
                collaboration_matrix[comm.sender_id][comm.receiver_id] += 1
        
        # Find collaboration clusters
        clusters = self._find_collaboration_clusters(agents, communications)
        
        # Calculate communication patterns
        patterns = self._analyze_communication_patterns(communications)
        
        return {
            "collaboration_matrix": collaboration_matrix,
            "collaboration_clusters": clusters,
            "communication_patterns": patterns,
            "total_collaborations": len(communications),
            "unique_collaborators": len(set(
                [comm.sender_id for comm in communications] + 
                [comm.receiver_id for comm in communications]
            ))
        }
    
    def _find_collaboration_clusters(
        self, 
        agents: List[AgentNode], 
        communications: List[CommunicationEvent]
    ) -> List[Dict[str, Any]]:
        """Find clusters of highly collaborating agents"""
        
        # Simple clustering based on communication frequency
        clusters = []
        agent_comm_count = {}
        
        for agent in agents:
            agent_comm_count[agent.agent_id] = sum(
                1 for comm in communications 
                if comm.sender_id == agent.agent_id or comm.receiver_id == agent.agent_id
            )
        
        # Group agents by communication activity level
        high_activity = [aid for aid, count in agent_comm_count.items() if count > 5]
        medium_activity = [aid for aid, count in agent_comm_count.items() if 2 <= count <= 5]
        low_activity = [aid for aid, count in agent_comm_count.items() if count < 2]
        
        if high_activity:
            clusters.append({
                "cluster_id": "high_activity",
                "agents": high_activity,
                "activity_level": "high",
                "size": len(high_activity)
            })
        
        if medium_activity:
            clusters.append({
                "cluster_id": "medium_activity", 
                "agents": medium_activity,
                "activity_level": "medium",
                "size": len(medium_activity)
            })
        
        if low_activity:
            clusters.append({
                "cluster_id": "low_activity",
                "agents": low_activity, 
                "activity_level": "low",
                "size": len(low_activity)
            })
        
        return clusters
    
    def _analyze_communication_patterns(
        self, 
        communications: List[CommunicationEvent]
    ) -> Dict[str, Any]:
        """Analyze communication patterns"""
        
        if not communications:
            return {}
        
        # Communication type distribution
        type_counts = {}
        for comm in communications:
            comm_type = comm.communication_type.value
            type_counts[comm_type] = type_counts.get(comm_type, 0) + 1
        
        # Response time analysis
        response_times = [comm.response_time for comm in communications if comm.response_time is not None]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Success rate
        successful = sum(1 for comm in communications if comm.success)
        success_rate = successful / len(communications) if communications else 0
        
        return {
            "communication_types": type_counts,
            "average_response_time": avg_response_time,
            "success_rate": success_rate,
            "total_communications": len(communications)
        }