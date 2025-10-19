"""
Cognitive Client for CollegiumAI SDK
Handles cognitive insights, memory analysis, and learning analytics
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
from enum import Enum

class CognitiveMetric(Enum):
    """Types of cognitive metrics"""
    ATTENTION_FOCUS = "attention_focus"
    MEMORY_RETENTION = "memory_retention"
    LEARNING_SPEED = "learning_speed"
    COMPREHENSION_LEVEL = "comprehension_level"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVITY_INDEX = "creativity_index"
    COGNITIVE_LOAD = "cognitive_load"
    DECISION_MAKING = "decision_making"
    METACOGNITION = "metacognition"
    KNOWLEDGE_TRANSFER = "knowledge_transfer"

class MemoryType(Enum):
    """Types of memory systems"""
    WORKING_MEMORY = "working_memory"
    EPISODIC_MEMORY = "episodic_memory"
    SEMANTIC_MEMORY = "semantic_memory"
    PROCEDURAL_MEMORY = "procedural_memory"
    LONG_TERM_MEMORY = "long_term_memory"
    SHORT_TERM_MEMORY = "short_term_memory"

class LearningType(Enum):
    """Types of learning patterns"""
    ADAPTIVE_LEARNING = "adaptive_learning"
    META_LEARNING = "meta_learning"
    TRANSFER_LEARNING = "transfer_learning"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    COLLABORATIVE_LEARNING = "collaborative_learning"
    SELF_DIRECTED_LEARNING = "self_directed_learning"

class CognitiveState(Enum):
    """Cognitive states"""
    FOCUSED = "focused"
    DISTRACTED = "distracted"
    OVERLOADED = "overloaded"
    OPTIMAL = "optimal"
    FATIGUED = "fatigued"
    ENGAGED = "engaged"
    STRESSED = "stressed"
    RELAXED = "relaxed"

class CognitiveClient:
    """Client for cognitive insights and analysis operations"""
    
    def __init__(self, client):
        self.client = client
    
    # Cognitive Insights Dashboard
    async def get_cognitive_dashboard(
        self,
        user_id: str,
        time_range: str = '30d',
        include_predictions: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive cognitive insights dashboard
        
        Args:
            user_id: User ID for cognitive analysis
            time_range: Time range for analysis (7d, 30d, 90d)
            include_predictions: Include cognitive performance predictions
            
        Returns:
            Complete cognitive dashboard with insights and metrics
        """
        params = {
            'user_id': user_id,
            'time_range': time_range,
            'include_predictions': include_predictions
        }
        
        return await self.client.get('/cognitive/dashboard', params=params)
    
    async def get_cognitive_overview(
        self,
        user_id: str,
        metrics: List[Union[str, CognitiveMetric]] = None
    ) -> Dict[str, Any]:
        """Get cognitive performance overview"""
        params = {'user_id': user_id}
        
        if metrics:
            metric_strs = []
            for metric in metrics:
                if isinstance(metric, CognitiveMetric):
                    metric_strs.append(metric.value)
                else:
                    metric_strs.append(metric)
            params['metrics'] = ','.join(metric_strs)
        
        return await self.client.get('/cognitive/overview', params=params)
    
    async def get_cognitive_trends(
        self,
        user_id: str,
        metric: Union[str, CognitiveMetric],
        time_range: str = '90d',
        granularity: str = 'day'
    ) -> Dict[str, Any]:
        """Get cognitive performance trends over time"""
        if isinstance(metric, CognitiveMetric):
            metric = metric.value
        
        params = {
            'user_id': user_id,
            'metric': metric,
            'time_range': time_range,
            'granularity': granularity
        }
        
        return await self.client.get('/cognitive/trends', params=params)
    
    # Memory System Analysis
    async def analyze_memory_patterns(
        self,
        user_id: str,
        memory_type: Union[str, MemoryType] = None,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """
        Analyze user's memory patterns and performance
        
        Args:
            user_id: User ID for memory analysis
            memory_type: Specific memory type to analyze
            time_range: Time range for analysis
            
        Returns:
            Memory pattern analysis and insights
        """
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if memory_type:
            if isinstance(memory_type, MemoryType):
                memory_type = memory_type.value
            params['memory_type'] = memory_type
        
        return await self.client.get('/cognitive/memory/patterns', params=params)
    
    async def get_memory_consolidation_metrics(
        self,
        user_id: str,
        learning_session_id: str = None,
        time_range: str = '7d'
    ) -> Dict[str, Any]:
        """Get memory consolidation effectiveness metrics"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if learning_session_id:
            params['session_id'] = learning_session_id
        
        return await self.client.get('/cognitive/memory/consolidation', params=params)
    
    async def analyze_memory_retrieval(
        self,
        user_id: str,
        content_id: str,
        retrieval_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Analyze memory retrieval patterns for specific content"""
        analysis_data = {
            'user_id': user_id,
            'content_id': content_id,
            'retrieval_context': retrieval_context or {}
        }
        
        return await self.client.post('/cognitive/memory/retrieval-analysis', data=analysis_data)
    
    async def get_memory_interference_analysis(
        self,
        user_id: str,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Analyze memory interference patterns"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        return await self.client.get('/cognitive/memory/interference', params=params)
    
    # Attention Pattern Analysis
    async def track_attention_patterns(
        self,
        user_id: str,
        session_id: str,
        attention_events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Track and analyze attention patterns during learning"""
        tracking_data = {
            'user_id': user_id,
            'session_id': session_id,
            'attention_events': attention_events
        }
        
        return await self.client.post('/cognitive/attention/track', data=tracking_data)
    
    async def get_attention_heatmap(
        self,
        user_id: str,
        content_id: str = None,
        time_range: str = '7d'
    ) -> Dict[str, Any]:
        """Get attention heatmap for content or time period"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if content_id:
            params['content_id'] = content_id
        
        return await self.client.get('/cognitive/attention/heatmap', params=params)
    
    async def analyze_attention_span(
        self,
        user_id: str,
        activity_type: str = None,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Analyze attention span patterns"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if activity_type:
            params['activity_type'] = activity_type
        
        return await self.client.get('/cognitive/attention/span-analysis', params=params)
    
    async def get_distraction_analysis(
        self,
        user_id: str,
        time_range: str = '7d',
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """Analyze distraction patterns and provide recommendations"""
        params = {
            'user_id': user_id,
            'time_range': time_range,
            'include_recommendations': include_recommendations
        }
        
        return await self.client.get('/cognitive/attention/distraction-analysis', params=params)
    
    # Learning Progression Analysis
    async def analyze_learning_progression(
        self,
        user_id: str,
        subject: str = None,
        learning_type: Union[str, LearningType] = None,
        time_range: str = '90d'
    ) -> Dict[str, Any]:
        """
        Analyze learning progression and effectiveness
        
        Args:
            user_id: User ID for learning analysis
            subject: Specific subject to analyze
            learning_type: Type of learning to focus on
            time_range: Time range for analysis
            
        Returns:
            Learning progression analysis and insights
        """
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if subject:
            params['subject'] = subject
        if learning_type:
            if isinstance(learning_type, LearningType):
                learning_type = learning_type.value
            params['learning_type'] = learning_type
        
        return await self.client.get('/cognitive/learning/progression', params=params)
    
    async def get_learning_velocity(
        self,
        user_id: str,
        subject: str = None,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Get learning velocity metrics"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if subject:
            params['subject'] = subject
        
        return await self.client.get('/cognitive/learning/velocity', params=params)
    
    async def analyze_knowledge_gaps(
        self,
        user_id: str,
        subject: str,
        target_competencies: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze knowledge gaps and learning opportunities"""
        analysis_data = {
            'user_id': user_id,
            'subject': subject,
            'target_competencies': target_competencies or []
        }
        
        return await self.client.post('/cognitive/learning/knowledge-gaps', data=analysis_data)
    
    async def get_learning_efficiency_metrics(
        self,
        user_id: str,
        time_range: str = '30d',
        breakdown_by: str = 'subject'
    ) -> Dict[str, Any]:
        """Get learning efficiency metrics"""
        params = {
            'user_id': user_id,
            'time_range': time_range,
            'breakdown_by': breakdown_by
        }
        
        return await self.client.get('/cognitive/learning/efficiency', params=params)
    
    # Decision-Making Analysis
    async def analyze_decision_patterns(
        self,
        user_id: str,
        decision_context: str = None,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Analyze decision-making patterns and quality"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if decision_context:
            params['context'] = decision_context
        
        return await self.client.get('/cognitive/decision-making/patterns', params=params)
    
    async def track_decision_process(
        self,
        user_id: str,
        decision_id: str,
        process_steps: List[Dict[str, Any]],
        outcome: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Track decision-making process for analysis"""
        tracking_data = {
            'user_id': user_id,
            'decision_id': decision_id,
            'process_steps': process_steps,
            'outcome': outcome
        }
        
        return await self.client.post('/cognitive/decision-making/track', data=tracking_data)
    
    async def get_decision_quality_metrics(
        self,
        user_id: str,
        time_range: str = '30d',
        decision_type: str = None
    ) -> Dict[str, Any]:
        """Get decision quality metrics and trends"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if decision_type:
            params['decision_type'] = decision_type
        
        return await self.client.get('/cognitive/decision-making/quality', params=params)
    
    # Cognitive State Monitoring
    async def detect_cognitive_state(
        self,
        user_id: str,
        session_data: Dict[str, Any],
        real_time: bool = True
    ) -> Dict[str, Any]:
        """
        Detect current cognitive state
        
        Args:
            user_id: User ID for state detection
            session_data: Current session data and indicators
            real_time: Whether to use real-time detection
            
        Returns:
            Detected cognitive state and confidence level
        """
        detection_data = {
            'user_id': user_id,
            'session_data': session_data,
            'real_time': real_time
        }
        
        return await self.client.post('/cognitive/state/detect', data=detection_data)
    
    async def get_cognitive_state_history(
        self,
        user_id: str,
        time_range: str = '7d',
        states: List[Union[str, CognitiveState]] = None
    ) -> List[Dict[str, Any]]:
        """Get cognitive state history"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if states:
            state_strs = []
            for state in states:
                if isinstance(state, CognitiveState):
                    state_strs.append(state.value)
                else:
                    state_strs.append(state)
            params['states'] = ','.join(state_strs)
        
        return await self.client.get('/cognitive/state/history', params=params)
    
    async def predict_cognitive_state(
        self,
        user_id: str,
        context_factors: Dict[str, Any],
        prediction_horizon: str = '1h'
    ) -> Dict[str, Any]:
        """Predict future cognitive state"""
        prediction_data = {
            'user_id': user_id,
            'context_factors': context_factors,
            'prediction_horizon': prediction_horizon
        }
        
        return await self.client.post('/cognitive/state/predict', data=prediction_data)
    
    # Cognitive Load Assessment
    async def assess_cognitive_load(
        self,
        user_id: str,
        task_data: Dict[str, Any],
        performance_indicators: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Assess cognitive load for a task or session"""
        assessment_data = {
            'user_id': user_id,
            'task_data': task_data,
            'performance_indicators': performance_indicators or {}
        }
        
        return await self.client.post('/cognitive/load/assess', data=assessment_data)
    
    async def get_cognitive_load_trends(
        self,
        user_id: str,
        time_range: str = '30d',
        activity_type: str = None
    ) -> Dict[str, Any]:
        """Get cognitive load trends over time"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        if activity_type:
            params['activity_type'] = activity_type
        
        return await self.client.get('/cognitive/load/trends', params=params)
    
    async def optimize_cognitive_load(
        self,
        user_id: str,
        current_tasks: List[Dict[str, Any]],
        constraints: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Get recommendations to optimize cognitive load"""
        optimization_data = {
            'user_id': user_id,
            'current_tasks': current_tasks,
            'constraints': constraints or {}
        }
        
        return await self.client.post('/cognitive/load/optimize', data=optimization_data)
    
    # Metacognitive Analysis
    async def analyze_metacognitive_awareness(
        self,
        user_id: str,
        self_assessment_data: Dict[str, Any],
        actual_performance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze metacognitive awareness accuracy"""
        analysis_data = {
            'user_id': user_id,
            'self_assessment_data': self_assessment_data,
            'actual_performance_data': actual_performance_data
        }
        
        return await self.client.post('/cognitive/metacognition/awareness', data=analysis_data)
    
    async def get_self_regulation_metrics(
        self,
        user_id: str,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Get self-regulation effectiveness metrics"""
        params = {
            'user_id': user_id,
            'time_range': time_range
        }
        
        return await self.client.get('/cognitive/metacognition/self-regulation', params=params)
    
    async def track_strategy_usage(
        self,
        user_id: str,
        learning_strategies: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Track learning strategy usage and effectiveness"""
        tracking_data = {
            'user_id': user_id,
            'learning_strategies': learning_strategies,
            'context': context or {}
        }
        
        return await self.client.post('/cognitive/metacognition/strategy-tracking', data=tracking_data)
    
    # Cognitive Insights and Recommendations
    async def generate_cognitive_insights(
        self,
        user_id: str,
        focus_areas: List[str] = None,
        time_range: str = '30d',
        include_predictions: bool = True
    ) -> Dict[str, Any]:
        """
        Generate comprehensive cognitive insights
        
        Args:
            user_id: User ID for insights generation
            focus_areas: Specific cognitive areas to focus on
            time_range: Time range for analysis
            include_predictions: Include predictive insights
            
        Returns:
            Comprehensive cognitive insights and recommendations
        """
        insights_data = {
            'user_id': user_id,
            'focus_areas': focus_areas or [],
            'time_range': time_range,
            'include_predictions': include_predictions
        }
        
        return await self.client.post('/cognitive/insights/generate', data=insights_data)
    
    async def get_personalized_recommendations(
        self,
        user_id: str,
        goal_type: str = 'learning_optimization',
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Get personalized cognitive enhancement recommendations"""
        recommendation_data = {
            'user_id': user_id,
            'goal_type': goal_type,
            'context': context or {}
        }
        
        return await self.client.post('/cognitive/recommendations', data=recommendation_data)
    
    async def create_cognitive_improvement_plan(
        self,
        user_id: str,
        target_areas: List[str],
        timeline: str = '30d',
        constraints: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create personalized cognitive improvement plan"""
        plan_data = {
            'user_id': user_id,
            'target_areas': target_areas,
            'timeline': timeline,
            'constraints': constraints or {}
        }
        
        return await self.client.post('/cognitive/improvement-plan', data=plan_data)
    
    # Comparative Analysis
    async def compare_cognitive_performance(
        self,
        user_id: str,
        comparison_type: str = 'peer_group',
        comparison_context: Dict[str, Any] = None,
        time_range: str = '30d'
    ) -> Dict[str, Any]:
        """Compare cognitive performance with peer groups or benchmarks"""
        comparison_data = {
            'user_id': user_id,
            'comparison_type': comparison_type,
            'comparison_context': comparison_context or {},
            'time_range': time_range
        }
        
        return await self.client.post('/cognitive/analysis/compare', data=comparison_data)
    
    async def get_cognitive_benchmarks(
        self,
        benchmark_type: str,
        demographic_filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Get cognitive performance benchmarks"""
        params = {'benchmark_type': benchmark_type}
        
        if demographic_filters:
            params.update(demographic_filters)
        
        return await self.client.get('/cognitive/benchmarks', params=params)
    
    # Data Export and Integration
    async def export_cognitive_data(
        self,
        user_id: str,
        data_types: List[str],
        time_range: str = '90d',
        format: str = 'json'
    ) -> Dict[str, Any]:
        """Export cognitive data for external analysis"""
        export_data = {
            'user_id': user_id,
            'data_types': data_types,
            'time_range': time_range,
            'format': format
        }
        
        return await self.client.post('/cognitive/export', data=export_data)
    
    async def import_external_cognitive_data(
        self,
        user_id: str,
        data_source: str,
        cognitive_data: Dict[str, Any],
        validation_level: str = 'standard'
    ) -> Dict[str, Any]:
        """Import cognitive data from external sources"""
        import_data = {
            'user_id': user_id,
            'data_source': data_source,
            'cognitive_data': cognitive_data,
            'validation_level': validation_level
        }
        
        return await self.client.post('/cognitive/import', data=import_data)