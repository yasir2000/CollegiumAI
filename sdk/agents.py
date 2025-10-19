"""
Multi-Agent Client for CollegiumAI SDK
Handles AI agent interactions, collaboration, and management
"""

from typing import Dict, List, Any, Optional, Union, AsyncGenerator
from datetime import datetime
from enum import Enum

class AgentType(Enum):
    """Available agent types in CollegiumAI"""
    ACADEMIC_ADVISOR = "academic_advisor"
    RESEARCH_ASSISTANT = "research_assistant"
    STUDY_BUDDY = "study_buddy"
    CAREER_COUNSELOR = "career_counselor"
    WRITING_TUTOR = "writing_tutor"
    MATH_TUTOR = "math_tutor"
    LANGUAGE_TUTOR = "language_tutor"
    ADMINISTRATIVE_ASSISTANT = "administrative_assistant"
    FACULTY_SUPPORT = "faculty_support"
    CURRICULUM_DESIGNER = "curriculum_designer"
    DEPARTMENT_CHAIR = "department_chair"
    DEAN = "dean"
    REGISTRAR = "registrar"
    FINANCIAL_AID = "financial_aid"
    LIBRARIAN = "librarian"
    IT_SUPPORT = "it_support"
    CAMPUS_GUIDE = "campus_guide"
    WELLNESS_COUNSELOR = "wellness_counselor"
    INTERNATIONAL_STUDENT_ADVISOR = "international_student_advisor"
    CUSTOM = "custom"

class PersonaType(Enum):
    """University persona types"""
    UNDERGRADUATE_STUDENT = "undergraduate_student"
    GRADUATE_STUDENT = "graduate_student"
    PHD_CANDIDATE = "phd_candidate"
    FACULTY_MEMBER = "faculty_member"
    PROFESSOR = "professor"
    DEPARTMENT_CHAIR = "department_chair"
    DEAN = "dean"
    STAFF_MEMBER = "staff_member"
    ADMINISTRATOR = "administrator"
    RESEARCHER = "researcher"
    VISITING_SCHOLAR = "visiting_scholar"
    ALUMNI = "alumni"

class CollaborationMode(Enum):
    """Agent collaboration modes"""
    INDEPENDENT = "independent"
    COLLABORATIVE = "collaborative"
    HIERARCHICAL = "hierarchical"
    DEMOCRATIC = "democratic"
    EXPERT_CONSENSUS = "expert_consensus"

class AgentClient:
    """Client for AI agent operations and multi-agent collaboration"""
    
    def __init__(self, client):
        self.client = client
        self._active_sessions = {}
    
    # Single Agent Interactions
    async def create_agent_session(
        self,
        agent_type: Union[str, AgentType],
        persona: Union[str, PersonaType] = None,
        context: Dict[str, Any] = None,
        session_id: str = None
    ) -> Dict[str, Any]:
        """
        Create a new agent session
        
        Args:
            agent_type: Type of agent to create
            persona: User persona for personalized responses
            context: Initial context for the session
            session_id: Optional session ID (auto-generated if not provided)
            
        Returns:
            Agent session information
        """
        if isinstance(agent_type, AgentType):
            agent_type = agent_type.value
        if isinstance(persona, PersonaType):
            persona = persona.value
        
        session_data = {
            'agent_type': agent_type,
            'persona': persona,
            'context': context or {},
            'session_id': session_id
        }
        
        response = await self.client.post('/agents/sessions', data=session_data)
        
        # Store session locally for management
        session_id = response.get('session_id')
        if session_id:
            self._active_sessions[session_id] = {
                'agent_type': agent_type,
                'persona': persona,
                'created_at': datetime.now(),
                'last_activity': datetime.now()
            }
        
        return response
    
    async def send_message(
        self,
        session_id: str,
        message: str,
        context: Dict[str, Any] = None,
        attachments: List[Dict[str, Any]] = None,
        collaboration_mode: CollaborationMode = CollaborationMode.INDEPENDENT
    ) -> Dict[str, Any]:
        """
        Send a message to an agent
        
        Args:
            session_id: Agent session ID
            message: Message to send
            context: Additional context for the message
            attachments: File attachments or additional data
            collaboration_mode: How other agents should be involved
            
        Returns:
            Agent response with reasoning and actions
        """
        message_data = {
            'message': message,
            'context': context or {},
            'attachments': attachments or [],
            'collaboration_mode': collaboration_mode.value
        }
        
        response = await self.client.post(
            f'/agents/sessions/{session_id}/messages',
            data=message_data
        )
        
        # Update session activity
        if session_id in self._active_sessions:
            self._active_sessions[session_id]['last_activity'] = datetime.now()
        
        return response
    
    async def get_session_history(
        self,
        session_id: str,
        limit: int = 50,
        include_reasoning: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Agent session ID
            limit: Maximum number of messages to return
            include_reasoning: Include agent reasoning in response
            
        Returns:
            List of messages in chronological order
        """
        params = {
            'limit': limit,
            'include_reasoning': include_reasoning
        }
        
        return await self.client.get(
            f'/agents/sessions/{session_id}/history',
            params=params
        )
    
    async def close_agent_session(self, session_id: str) -> Dict[str, Any]:
        """Close an agent session"""
        response = await self.client.delete(f'/agents/sessions/{session_id}')
        
        # Remove from local tracking
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]
        
        return response
    
    # Multi-Agent Collaboration
    async def create_collaboration_session(
        self,
        agent_types: List[Union[str, AgentType]],
        task_description: str,
        collaboration_mode: CollaborationMode = CollaborationMode.COLLABORATIVE,
        persona: Union[str, PersonaType] = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a multi-agent collaboration session
        
        Args:
            agent_types: List of agent types to include
            task_description: Description of the collaborative task
            collaboration_mode: How agents should collaborate
            persona: User persona for context
            context: Additional context for all agents
            
        Returns:
            Collaboration session information
        """
        # Convert enums to strings
        agent_types_str = []
        for agent_type in agent_types:
            if isinstance(agent_type, AgentType):
                agent_types_str.append(agent_type.value)
            else:
                agent_types_str.append(agent_type)
        
        if isinstance(persona, PersonaType):
            persona = persona.value
        
        collaboration_data = {
            'agent_types': agent_types_str,
            'task_description': task_description,
            'collaboration_mode': collaboration_mode.value,
            'persona': persona,
            'context': context or {}
        }
        
        return await self.client.post('/agents/collaborations', data=collaboration_data)
    
    async def send_collaboration_message(
        self,
        collaboration_id: str,
        message: str,
        target_agent: str = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Send a message to a collaboration session
        
        Args:
            collaboration_id: Collaboration session ID
            message: Message to send
            target_agent: Specific agent to address (all agents if not specified)
            context: Additional context
            
        Returns:
            Collaborative response from multiple agents
        """
        message_data = {
            'message': message,
            'target_agent': target_agent,
            'context': context or {}
        }
        
        return await self.client.post(
            f'/agents/collaborations/{collaboration_id}/messages',
            data=message_data
        )
    
    async def get_collaboration_status(self, collaboration_id: str) -> Dict[str, Any]:
        """Get status of a collaboration session"""
        return await self.client.get(f'/agents/collaborations/{collaboration_id}/status')
    
    async def get_collaboration_agents(self, collaboration_id: str) -> List[Dict[str, Any]]:
        """Get information about agents in a collaboration"""
        return await self.client.get(f'/agents/collaborations/{collaboration_id}/agents')
    
    async def add_agent_to_collaboration(
        self,
        collaboration_id: str,
        agent_type: Union[str, AgentType],
        role: str = None
    ) -> Dict[str, Any]:
        """Add an agent to an existing collaboration"""
        if isinstance(agent_type, AgentType):
            agent_type = agent_type.value
        
        agent_data = {
            'agent_type': agent_type,
            'role': role
        }
        
        return await self.client.post(
            f'/agents/collaborations/{collaboration_id}/agents',
            data=agent_data
        )
    
    async def remove_agent_from_collaboration(
        self,
        collaboration_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """Remove an agent from a collaboration"""
        return await self.client.delete(
            f'/agents/collaborations/{collaboration_id}/agents/{agent_id}'
        )
    
    # Agent Management
    async def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get list of all available agent types"""
        return await self.client.get('/agents/types')
    
    async def get_agent_capabilities(self, agent_type: Union[str, AgentType]) -> Dict[str, Any]:
        """Get capabilities and expertise of a specific agent type"""
        if isinstance(agent_type, AgentType):
            agent_type = agent_type.value
        
        return await self.client.get(f'/agents/types/{agent_type}/capabilities')
    
    async def get_active_sessions(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get all active agent sessions"""
        params = {}
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/agents/sessions', params=params)
    
    async def get_collaboration_sessions(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get all active collaboration sessions"""
        params = {}
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/agents/collaborations', params=params)
    
    # Agent Configuration and Customization
    async def create_custom_agent(
        self,
        name: str,
        description: str,
        capabilities: List[str],
        personality_traits: Dict[str, Any],
        knowledge_domains: List[str],
        base_agent_type: Union[str, AgentType] = AgentType.CUSTOM
    ) -> Dict[str, Any]:
        """
        Create a custom agent with specific capabilities
        
        Args:
            name: Agent name
            description: Agent description
            capabilities: List of agent capabilities
            personality_traits: Agent personality configuration
            knowledge_domains: Areas of expertise
            base_agent_type: Base agent type to extend from
            
        Returns:
            Custom agent configuration
        """
        if isinstance(base_agent_type, AgentType):
            base_agent_type = base_agent_type.value
        
        agent_config = {
            'name': name,
            'description': description,
            'capabilities': capabilities,
            'personality_traits': personality_traits,
            'knowledge_domains': knowledge_domains,
            'base_agent_type': base_agent_type
        }
        
        return await self.client.post('/agents/custom', data=agent_config)
    
    async def update_agent_configuration(
        self,
        agent_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update configuration of a custom agent"""
        return await self.client.put(f'/agents/custom/{agent_id}', data=updates)
    
    async def delete_custom_agent(self, agent_id: str) -> Dict[str, Any]:
        """Delete a custom agent"""
        return await self.client.delete(f'/agents/custom/{agent_id}')
    
    async def get_custom_agents(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get list of custom agents"""
        params = {}
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/agents/custom', params=params)
    
    # Agent Performance and Analytics
    async def get_agent_performance(
        self,
        agent_type: Union[str, AgentType] = None,
        session_id: str = None,
        time_period: str = '7d'
    ) -> Dict[str, Any]:
        """
        Get agent performance metrics
        
        Args:
            agent_type: Specific agent type to analyze
            session_id: Specific session to analyze
            time_period: Time period for analysis (1d, 7d, 30d)
            
        Returns:
            Performance metrics and analytics
        """
        params = {'time_period': time_period}
        
        if agent_type:
            if isinstance(agent_type, AgentType):
                agent_type = agent_type.value
            params['agent_type'] = agent_type
        
        if session_id:
            params['session_id'] = session_id
        
        return await self.client.get('/agents/analytics/performance', params=params)
    
    async def get_collaboration_analytics(
        self,
        collaboration_id: str = None,
        time_period: str = '7d'
    ) -> Dict[str, Any]:
        """Get multi-agent collaboration analytics"""
        params = {'time_period': time_period}
        
        if collaboration_id:
            params['collaboration_id'] = collaboration_id
        
        return await self.client.get('/agents/analytics/collaboration', params=params)
    
    async def get_user_interaction_patterns(
        self,
        user_id: str = None,
        time_period: str = '30d'
    ) -> Dict[str, Any]:
        """Get user interaction patterns with agents"""
        params = {'time_period': time_period}
        
        if user_id:
            params['user_id'] = user_id
        
        return await self.client.get('/agents/analytics/user-patterns', params=params)
    
    # Real-time Agent Communication
    async def subscribe_to_agent_updates(
        self,
        session_id: str = None,
        collaboration_id: str = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Subscribe to real-time agent updates
        
        Args:
            session_id: Subscribe to specific session updates
            collaboration_id: Subscribe to collaboration updates
            
        Yields:
            Real-time agent messages and status updates
        """
        subscription_data = {}
        
        if session_id:
            subscription_data['session_id'] = session_id
        if collaboration_id:
            subscription_data['collaboration_id'] = collaboration_id
        
        # Use the client's WebSocket subscription
        async for message in self.client.subscribe_to_updates(['agent_messages', 'agent_status']):
            # Filter messages based on subscription criteria
            if session_id and message.get('session_id') != session_id:
                continue
            if collaboration_id and message.get('collaboration_id') != collaboration_id:
                continue
            
            yield message
    
    # Agent Learning and Adaptation
    async def provide_feedback(
        self,
        session_id: str,
        message_id: str,
        feedback_type: str,
        rating: int,
        comments: str = None
    ) -> Dict[str, Any]:
        """
        Provide feedback on agent responses for learning
        
        Args:
            session_id: Agent session ID
            message_id: Specific message ID to rate
            feedback_type: Type of feedback (helpful, accurate, relevant, etc.)
            rating: Rating from 1-5
            comments: Optional detailed feedback
            
        Returns:
            Feedback submission confirmation
        """
        feedback_data = {
            'message_id': message_id,
            'feedback_type': feedback_type,
            'rating': rating,
            'comments': comments
        }
        
        return await self.client.post(
            f'/agents/sessions/{session_id}/feedback',
            data=feedback_data
        )
    
    async def get_agent_learning_progress(
        self,
        agent_type: Union[str, AgentType]
    ) -> Dict[str, Any]:
        """Get learning progress for a specific agent type"""
        if isinstance(agent_type, AgentType):
            agent_type = agent_type.value
        
        return await self.client.get(f'/agents/types/{agent_type}/learning-progress')
    
    # Batch Operations
    async def batch_message_agents(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Send multiple messages to different agents in batch
        
        Args:
            messages: List of message objects with session_id, message, etc.
            
        Returns:
            List of agent responses
        """
        return await self.client.post('/agents/batch/messages', data={'messages': messages})
    
    async def bulk_create_sessions(
        self,
        session_configs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Bulk create multiple agent sessions"""
        return await self.client.post('/agents/bulk/sessions', data={'sessions': session_configs})
    
    # Utility Methods
    def get_local_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get locally tracked active sessions"""
        return self._active_sessions.copy()
    
    def clear_local_session_cache(self):
        """Clear locally cached session information"""
        self._active_sessions.clear()
    
    async def validate_session(self, session_id: str) -> bool:
        """Validate if a session is still active on the server"""
        try:
            response = await self.client.get(f'/agents/sessions/{session_id}/status')
            return response.get('status') == 'active'
        except:
            return False