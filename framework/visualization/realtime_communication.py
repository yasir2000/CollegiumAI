"""
Real-time Agent Communication Visualizer
=======================================

WebSocket-based real-time visualization of agent communications
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import asdict
import websockets
import uuid

from .multi_agent_dashboard import (
    AgentNode, CommunicationEvent, CommunicationType,
    MultiAgentVisualizationDashboard
)

logger = logging.getLogger(__name__)

class RealTimeVisualizationServer:
    """WebSocket server for real-time visualization"""
    
    def __init__(self, dashboard: MultiAgentVisualizationDashboard, port: int = 8765):
        self.dashboard = dashboard
        self.port = port
        self.connected_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.is_running = False
        self.communication_buffer = []
        self.update_interval = 1.0  # seconds
    
    async def start_server(self):
        """Start the WebSocket server"""
        self.is_running = True
        logger.info(f"Starting real-time visualization server on port {self.port}")
        
        # Start WebSocket server
        server = await websockets.serve(
            self.handle_client_connection,
            "localhost",
            self.port
        )
        
        # Start background update task
        update_task = asyncio.create_task(self.broadcast_updates())
        
        try:
            await server.wait_closed()
        finally:
            self.is_running = False
            update_task.cancel()
    
    async def handle_client_connection(self, websocket, path):
        """Handle new client connections"""
        client_id = str(uuid.uuid4())
        self.connected_clients.add(websocket)
        logger.info(f"Client {client_id} connected. Total clients: {len(self.connected_clients)}")
        
        try:
            # Send initial dashboard data
            await self.send_initial_data(websocket)
            
            # Handle incoming messages
            async for message in websocket:
                await self.handle_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            self.connected_clients.discard(websocket)
    
    async def send_initial_data(self, websocket):
        """Send initial dashboard data to new client"""
        try:
            overview = await self.dashboard.get_dashboard_overview()
            
            initial_data = {
                "type": "initial_data",
                "timestamp": datetime.utcnow().isoformat(),
                "data": overview
            }
            
            await websocket.send(json.dumps(initial_data))
            
        except Exception as e:
            logger.error(f"Error sending initial data: {e}")
    
    async def handle_client_message(self, websocket, message):
        """Handle messages from clients"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "get_agent_details":
                agent_id = data.get("agent_id")
                if agent_id:
                    agent_details = await self.dashboard.get_agent_details(agent_id)
                    response = {
                        "type": "agent_details",
                        "agent_id": agent_id,
                        "data": agent_details
                    }
                    await websocket.send(json.dumps(response))
            
            elif message_type == "get_task_details":
                task_id = data.get("task_id")
                if task_id:
                    task_details = await self.dashboard.get_task_details(task_id)
                    response = {
                        "type": "task_details",
                        "task_id": task_id,
                        "data": task_details
                    }
                    await websocket.send(json.dumps(response))
            
            elif message_type == "subscribe_to_agent":
                # Client wants to subscribe to specific agent updates
                agent_id = data.get("agent_id")
                # Store subscription info (implementation depends on requirements)
                logger.info(f"Client subscribed to agent {agent_id}")
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from client")
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    async def broadcast_updates(self):
        """Broadcast updates to all connected clients"""
        while self.is_running:
            try:
                if self.connected_clients:
                    # Get latest dashboard data
                    overview = await self.dashboard.get_dashboard_overview()
                    
                    # Prepare update message
                    update_message = {
                        "type": "dashboard_update",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": overview
                    }
                    
                    # Broadcast to all clients
                    if self.connected_clients:
                        await asyncio.gather(
                            *[client.send(json.dumps(update_message)) for client in self.connected_clients],
                            return_exceptions=True
                        )
                
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error in broadcast updates: {e}")
                await asyncio.sleep(self.update_interval)
    
    async def broadcast_communication_event(self, communication: CommunicationEvent):
        """Broadcast new communication event to all clients"""
        if self.connected_clients:
            event_message = {
                "type": "new_communication",
                "timestamp": datetime.utcnow().isoformat(),
                "data": asdict(communication)
            }
            
            await asyncio.gather(
                *[client.send(json.dumps(event_message)) for client in self.connected_clients],
                return_exceptions=True
            )
    
    async def broadcast_agent_status_change(self, agent: AgentNode):
        """Broadcast agent status change to all clients"""
        if self.connected_clients:
            status_message = {
                "type": "agent_status_change",
                "timestamp": datetime.utcnow().isoformat(),
                "agent_id": agent.agent_id,
                "data": asdict(agent)
            }
            
            await asyncio.gather(
                *[client.send(json.dumps(status_message)) for client in self.connected_clients],
                return_exceptions=True
            )

class NetworkGraphGenerator:
    """Generates network graph data for visualization"""
    
    @staticmethod
    def generate_network_graph(
        agents: List[AgentNode],
        communications: List[CommunicationEvent],
        time_window_hours: int = 24
    ) -> Dict[str, Any]:
        """Generate network graph data for D3.js or similar visualization libraries"""
        
        # Filter recent communications
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        recent_comms = [
            comm for comm in communications
            if comm.timestamp > cutoff_time
        ]
        
        # Create nodes
        nodes = []
        for agent in agents:
            node = {
                "id": agent.agent_id,
                "name": agent.agent_name,
                "type": agent.agent_type,
                "status": agent.status.value,
                "load": agent.load_factor,
                "health": agent.health_score,
                "capabilities": agent.capabilities,
                "position": {"x": agent.position[0], "y": agent.position[1]},
                "size": len(agent.current_tasks) * 5 + 10,  # Size based on task count
                "color": NetworkGraphGenerator._get_status_color(agent.status.value)
            }
            nodes.append(node)
        
        # Create links (edges)
        links = []
        link_strength = {}  # Track communication frequency between agents
        
        for comm in recent_comms:
            if comm.success:
                link_key = f"{comm.sender_id}-{comm.receiver_id}"
                reverse_key = f"{comm.receiver_id}-{comm.sender_id}"
                
                # Use undirected links (combine both directions)
                if reverse_key in link_strength:
                    link_strength[reverse_key] += 1
                else:
                    link_strength[link_key] = link_strength.get(link_key, 0) + 1
        
        # Convert to links format
        processed_pairs = set()
        for link_key, strength in link_strength.items():
            if strength < 2:  # Only show links with multiple communications
                continue
                
            parts = link_key.split('-')
            if len(parts) == 2:
                source, target = parts
                pair = tuple(sorted([source, target]))
                
                if pair not in processed_pairs:
                    processed_pairs.add(pair)
                    
                    link = {
                        "source": source,
                        "target": target,
                        "strength": strength,
                        "width": min(strength / 2, 10),  # Visual width
                        "color": NetworkGraphGenerator._get_link_color(strength)
                    }
                    links.append(link)
        
        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_agents": len(agents),
                "total_communications": len(recent_comms),
                "time_window_hours": time_window_hours,
                "generated_at": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def _get_status_color(status: str) -> str:
        """Get color for agent status"""
        color_map = {
            "active": "#4CAF50",      # Green
            "idle": "#FFC107",        # Amber
            "busy": "#FF9800",        # Orange
            "error": "#F44336",       # Red
            "offline": "#9E9E9E",     # Grey
            "initializing": "#2196F3"  # Blue
        }
        return color_map.get(status, "#9E9E9E")
    
    @staticmethod
    def _get_link_color(strength: int) -> str:
        """Get color for link based on communication strength"""
        if strength >= 10:
            return "#1976D2"  # Strong blue
        elif strength >= 5:
            return "#42A5F5"  # Medium blue
        else:
            return "#90CAF9"  # Light blue

class TaskFlowDiagramGenerator:
    """Generates task flow diagrams"""
    
    @staticmethod
    def generate_task_flow_diagram(task_flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate task flow diagram data"""
        
        task_graph = task_flow_data.get("task_graph", {})
        critical_paths = task_flow_data.get("critical_paths", [])
        bottlenecks = task_flow_data.get("bottlenecks", [])
        
        # Create nodes for tasks
        nodes = []
        for task_id, task_data in task_graph.items():
            
            # Check if task is in critical path
            in_critical_path = any(
                task_id in path["path"] for path in critical_paths
            )
            
            # Check if task is a bottleneck
            is_bottleneck = any(
                bottleneck["task_id"] == task_id for bottleneck in bottlenecks
            )
            
            node = {
                "id": task_id,
                "name": task_data["task_name"],
                "status": task_data["status"],
                "progress": task_data["progress"],
                "priority": task_data["priority"],
                "estimated_duration": task_data["estimated_duration"],
                "assigned_agents": task_data["assigned_agents"],
                "in_critical_path": in_critical_path,
                "is_bottleneck": is_bottleneck,
                "color": TaskFlowDiagramGenerator._get_task_color(
                    task_data["status"], in_critical_path, is_bottleneck
                ),
                "size": task_data["priority"] * 2 + 10,  # Size based on priority
                "shape": "diamond" if is_bottleneck else "circle"
            }
            nodes.append(node)
        
        # Create links for dependencies
        links = []
        for task_id, task_data in task_graph.items():
            for dependency in task_data["dependencies"]:
                link = {
                    "source": dependency,
                    "target": task_id,
                    "type": "dependency",
                    "color": "#757575"
                }
                links.append(link)
        
        # Add critical path highlighting
        critical_path_links = []
        for path_data in critical_paths[:1]:  # Show only the most critical path
            path = path_data["path"]
            for i in range(len(path) - 1):
                critical_path_links.append({
                    "source": path[i],
                    "target": path[i + 1],
                    "type": "critical_path",
                    "color": "#F44336",
                    "width": 3
                })
        
        return {
            "nodes": nodes,
            "dependency_links": links,
            "critical_path_links": critical_path_links,
            "layout_config": {
                "type": "hierarchical",
                "direction": "top-to-bottom",
                "level_separation": 100,
                "node_separation": 80
            },
            "metadata": {
                "total_tasks": len(nodes),
                "critical_paths": len(critical_paths),
                "bottlenecks": len(bottlenecks),
                "completion_rate": task_flow_data.get("flow_metrics", {}).get("completion_rate", 0)
            }
        }
    
    @staticmethod
    def _get_task_color(status: str, in_critical_path: bool, is_bottleneck: bool) -> str:
        """Get color for task based on status and properties"""
        
        if is_bottleneck:
            return "#FF5722"  # Deep Orange for bottlenecks
        elif in_critical_path:
            return "#F44336"  # Red for critical path
        else:
            # Status-based colors
            color_map = {
                "pending": "#9E9E9E",      # Grey
                "in_progress": "#2196F3",  # Blue
                "completed": "#4CAF50",    # Green
                "failed": "#F44336",       # Red
                "cancelled": "#757575",    # Dark Grey
                "blocked": "#FF9800"       # Orange
            }
            return color_map.get(status, "#9E9E9E")

class PerformanceChartGenerator:
    """Generates performance charts and metrics"""
    
    @staticmethod
    def generate_performance_charts(performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance chart data"""
        
        system_metrics = performance_data.get("system_metrics", {})
        
        # System health over time chart
        health_chart = {
            "type": "line",
            "title": "System Health Over Time",
            "data": {
                "labels": ["1h ago", "45m ago", "30m ago", "15m ago", "Now"],
                "datasets": [{
                    "label": "System Health",
                    "data": [0.95, 0.92, 0.88, 0.91, system_metrics.get("system_health", 0.9)],
                    "borderColor": "#4CAF50",
                    "backgroundColor": "rgba(76, 175, 80, 0.1)"
                }]
            }
        }
        
        # Task throughput chart
        throughput_chart = {
            "type": "bar",
            "title": "Task Throughput (24h)",
            "data": {
                "labels": ["Completed", "In Progress", "Pending", "Failed"],
                "datasets": [{
                    "label": "Tasks",
                    "data": [
                        system_metrics.get("completed_tasks", 0),
                        system_metrics.get("in_progress_tasks", 0),
                        system_metrics.get("pending_tasks", 0),
                        system_metrics.get("total_tasks", 0) - system_metrics.get("completed_tasks", 0) - 
                        system_metrics.get("in_progress_tasks", 0) - system_metrics.get("pending_tasks", 0)
                    ],
                    "backgroundColor": ["#4CAF50", "#2196F3", "#FF9800", "#F44336"]
                }]
            }
        }
        
        # Communication success rate
        comm_chart = {
            "type": "doughnut",
            "title": "Communication Success Rate",
            "data": {
                "labels": ["Successful", "Failed"],
                "datasets": [{
                    "data": [
                        system_metrics.get("communication_success_rate", 0.9) * 100,
                        (1 - system_metrics.get("communication_success_rate", 0.9)) * 100
                    ],
                    "backgroundColor": ["#4CAF50", "#F44336"]
                }]
            }
        }
        
        # Agent load distribution
        load_chart = {
            "type": "histogram",
            "title": "Agent Load Distribution",
            "data": {
                "bins": [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                "values": [2, 5, 8, 3, 2],  # Sample distribution
                "backgroundColor": "#2196F3"
            }
        }
        
        return {
            "charts": {
                "system_health": health_chart,
                "task_throughput": throughput_chart,
                "communication_success": comm_chart,
                "load_distribution": load_chart
            },
            "key_metrics": {
                "system_health": system_metrics.get("system_health", 0),
                "active_agents": system_metrics.get("active_agents", 0),
                "task_completion_rate": system_metrics.get("completed_tasks", 0) / max(system_metrics.get("total_tasks", 1), 1),
                "avg_response_time": system_metrics.get("avg_response_time", 0),
                "communication_volume": system_metrics.get("communication_volume_24h", 0)
            }
        }

# Integration function
async def create_visualization_server(
    dashboard: MultiAgentVisualizationDashboard,
    port: int = 8765
) -> RealTimeVisualizationServer:
    """Create and return a configured visualization server"""
    
    server = RealTimeVisualizationServer(dashboard, port)
    return server

# Example usage and testing functions
async def demo_visualization_system():
    """Demonstrate the visualization system with sample data"""
    
    # Import sample data creators
    from .multi_agent_dashboard import (
        create_sample_agents,
        create_sample_tasks,
        create_sample_communications,
        MultiAgentVisualizationDashboard
    )
    
    # Create sample data
    agents = create_sample_agents(8)
    tasks = create_sample_tasks(15)
    communications = create_sample_communications(agents, 100)
    
    # Create dashboard
    dashboard = MultiAgentVisualizationDashboard()
    await dashboard.update_dashboard_data(agents, tasks, communications)
    
    # Generate visualization data
    network_graph = NetworkGraphGenerator.generate_network_graph(agents, communications)
    task_flow_data = dashboard.task_flow_visualizer.build_task_flow_graph(tasks)
    task_flow_diagram = TaskFlowDiagramGenerator.generate_task_flow_diagram(task_flow_data)
    
    performance_data = {"system_metrics": dashboard.performance_analyzer.system_metrics}
    performance_charts = PerformanceChartGenerator.generate_performance_charts(performance_data)
    
    print("=== Multi-Agent Visualization Demo ===")
    print(f"Network Graph: {len(network_graph['nodes'])} nodes, {len(network_graph['links'])} links")
    print(f"Task Flow: {len(task_flow_diagram['nodes'])} tasks, {len(task_flow_diagram['dependency_links'])} dependencies")
    print(f"Performance Charts: {len(performance_charts['charts'])} charts generated")
    
    return {
        "network_graph": network_graph,
        "task_flow_diagram": task_flow_diagram,
        "performance_charts": performance_charts,
        "dashboard_overview": await dashboard.get_dashboard_overview()
    }

if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demo_visualization_system())