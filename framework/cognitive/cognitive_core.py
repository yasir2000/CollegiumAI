"""
CollegiumAI Cognitive Architecture - Core Engine
Advanced cognitive processing inspired by cognitive science and neuroscience
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime
import uuid

class CognitiveStateType(Enum):
    """Types of cognitive states"""
    PERCEIVING = "perceiving"
    REASONING = "reasoning"
    LEARNING = "learning"
    DECIDING = "deciding"
    REFLECTING = "reflecting"
    INTEGRATING = "integrating"

class ActivationLevel(Enum):
    """Cognitive activation levels"""
    LOW = 0.2
    MODERATE = 0.5
    HIGH = 0.8
    CRITICAL = 1.0

@dataclass
class CognitiveState:
    """Represents the current cognitive state of the system"""
    state_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    primary_state: CognitiveStateType = CognitiveStateType.PERCEIVING
    activation_level: ActivationLevel = ActivationLevel.MODERATE
    attention_focus: Dict[str, float] = field(default_factory=dict)
    working_memory_capacity: float = 0.7
    cognitive_load: float = 0.3
    emotional_valence: float = 0.0  # -1 to 1
    confidence_level: float = 0.5
    context_variables: Dict[str, Any] = field(default_factory=dict)
    
    def update_activation(self, new_level: ActivationLevel):
        """Update activation level with temporal smoothing"""
        self.activation_level = new_level
        self.timestamp = datetime.now()
    
    def add_context(self, key: str, value: Any):
        """Add contextual information"""
        self.context_variables[key] = value
    
    def get_cognitive_capacity(self) -> float:
        """Calculate available cognitive capacity"""
        return max(0.0, self.working_memory_capacity - self.cognitive_load)

class CognitiveEngine:
    """
    Core cognitive processing engine that orchestrates all cognitive capabilities
    Inspired by ACT-R, SOAR, and other cognitive architectures
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.cognitive_state = CognitiveState()
        self.logger = logging.getLogger(f"CognitiveEngine-{persona_type}")
        
        # Cognitive modules (to be injected)
        self.perception_module = None
        self.reasoning_engine = None
        self.memory_system = None
        self.learning_system = None
        self.decision_engine = None
        self.attention_mechanism = None
        self.metacognitive_controller = None
        
        # Cognitive cycle parameters
        self.cycle_time = 0.05  # 50ms cognitive cycles
        self.processing_queue = asyncio.Queue()
        self.active_goals = []
        self.cognitive_history = []
        
        # Persona-specific cognitive parameters
        self.cognitive_profile = self._initialize_cognitive_profile()
        
    def _initialize_cognitive_profile(self) -> Dict[str, float]:
        """Initialize persona-specific cognitive parameters"""
        base_profile = {
            "analytical_reasoning": 0.7,
            "creative_thinking": 0.6,
            "social_cognition": 0.5,
            "metacognitive_awareness": 0.6,
            "learning_rate": 0.4,
            "attention_span": 0.7,
            "working_memory_capacity": 0.6,
            "processing_speed": 0.6,
            "emotional_regulation": 0.5
        }
        
        # Adjust based on persona type
        if "student" in self.persona_type.lower():
            base_profile.update({
                "learning_rate": 0.8,
                "creative_thinking": 0.7,
                "metacognitive_awareness": 0.5
            })
        elif "faculty" in self.persona_type.lower() or "professor" in self.persona_type.lower():
            base_profile.update({
                "analytical_reasoning": 0.9,
                "metacognitive_awareness": 0.8,
                "creative_thinking": 0.8,
                "social_cognition": 0.7
            })
        elif "advisor" in self.persona_type.lower() or "counselor" in self.persona_type.lower():
            base_profile.update({
                "social_cognition": 0.9,
                "emotional_regulation": 0.8,
                "metacognitive_awareness": 0.7
            })
        elif "administrator" in self.persona_type.lower():
            base_profile.update({
                "analytical_reasoning": 0.8,
                "social_cognition": 0.8,
                "processing_speed": 0.8,
                "metacognitive_awareness": 0.7
            })
        
        return base_profile
    
    async def initialize_cognitive_modules(self, modules: Dict[str, Any]):
        """Initialize and connect cognitive modules"""
        self.perception_module = modules.get('perception')
        self.reasoning_engine = modules.get('reasoning')
        self.memory_system = modules.get('memory')
        self.learning_system = modules.get('learning')
        self.decision_engine = modules.get('decision')
        self.attention_mechanism = modules.get('attention')
        self.metacognitive_controller = modules.get('metacognition')
        
        # Establish inter-module connections
        await self._establish_cognitive_connections()
        
        self.logger.info(f"Cognitive modules initialized for {self.persona_type}")
    
    async def _establish_cognitive_connections(self):
        """Establish connections between cognitive modules"""
        # Connect perception to working memory
        if self.perception_module and self.memory_system:
            self.perception_module.connect_to_memory(self.memory_system.working_memory)
        
        # Connect reasoning to long-term memory
        if self.reasoning_engine and self.memory_system:
            self.reasoning_engine.connect_to_memory(self.memory_system.long_term_memory)
        
        # Connect metacognition to all modules
        if self.metacognitive_controller:
            await self.metacognitive_controller.connect_to_modules({
                'perception': self.perception_module,
                'reasoning': self.reasoning_engine,
                'memory': self.memory_system,
                'learning': self.learning_system,
                'decision': self.decision_engine,
                'attention': self.attention_mechanism
            })
    
    async def process_cognitive_cycle(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute one complete cognitive cycle
        Based on the cognitive cycle: Perceive -> Reason -> Decide -> Act -> Learn
        """
        cycle_start = datetime.now()
        cycle_id = str(uuid.uuid4())
        
        try:
            # Phase 1: Perception and Attention
            perceived_data = await self._perception_phase(input_data)
            
            # Phase 2: Memory Retrieval and Context Integration
            contextual_data = await self._memory_retrieval_phase(perceived_data)
            
            # Phase 3: Reasoning and Problem Solving
            reasoning_output = await self._reasoning_phase(contextual_data)
            
            # Phase 4: Decision Making
            decision = await self._decision_phase(reasoning_output)
            
            # Phase 5: Action Planning and Execution
            action_plan = await self._action_planning_phase(decision)
            
            # Phase 6: Learning and Memory Consolidation
            await self._learning_phase(input_data, action_plan, cycle_id)
            
            # Phase 7: Metacognitive Monitoring and Control
            await self._metacognitive_phase(cycle_id, cycle_start)
            
            # Update cognitive state
            self._update_cognitive_state(action_plan)
            
            return {
                "cycle_id": cycle_id,
                "cognitive_state": self.cognitive_state,
                "action_plan": action_plan,
                "reasoning_output": reasoning_output,
                "confidence": self.cognitive_state.confidence_level,
                "processing_time": (datetime.now() - cycle_start).total_seconds()
            }
            
        except Exception as e:
            self.logger.error(f"Cognitive cycle error: {e}")
            return {"error": str(e), "cycle_id": cycle_id}
    
    async def _perception_phase(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process perception and attention"""
        if not self.perception_module:
            return input_data
        
        # Apply attention mechanisms
        if self.attention_mechanism:
            focused_input = await self.attention_mechanism.focus_attention(
                input_data, self.cognitive_state.attention_focus
            )
        else:
            focused_input = input_data
        
        # Process through perception
        perceived = await self.perception_module.process_multimodal_input(
            focused_input, self.cognitive_state
        )
        
        return perceived
    
    async def _memory_retrieval_phase(self, perceived_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve relevant memories and context"""
        if not self.memory_system:
            return perceived_data
        
        # Retrieve episodic memories
        episodic_context = await self.memory_system.episodic_memory.retrieve_similar_episodes(
            perceived_data, similarity_threshold=0.7
        )
        
        # Retrieve semantic knowledge
        semantic_context = await self.memory_system.long_term_memory.retrieve_relevant_knowledge(
            perceived_data, activation_threshold=0.5
        )
        
        # Update working memory
        await self.memory_system.working_memory.update(
            perceived_data, episodic_context, semantic_context
        )
        
        return {
            "perceived": perceived_data,
            "episodic_context": episodic_context,
            "semantic_context": semantic_context,
            "working_memory_state": self.memory_system.working_memory.get_state()
        }
    
    async def _reasoning_phase(self, contextual_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply reasoning and problem-solving"""
        if not self.reasoning_engine:
            return contextual_data
        
        # Causal reasoning
        causal_analysis = await self.reasoning_engine.causal_reasoning.analyze_causality(
            contextual_data, self.cognitive_profile["analytical_reasoning"]
        )
        
        # Analogical reasoning
        analogical_insights = await self.reasoning_engine.analogical_reasoning.find_analogies(
            contextual_data, self.memory_system.long_term_memory
        )
        
        # Abstract reasoning
        abstract_patterns = await self.reasoning_engine.identify_abstract_patterns(
            contextual_data, self.cognitive_profile["creative_thinking"]
        )
        
        return {
            "contextual_data": contextual_data,
            "causal_analysis": causal_analysis,
            "analogical_insights": analogical_insights,
            "abstract_patterns": abstract_patterns,
            "reasoning_confidence": self.reasoning_engine.get_confidence()
        }
    
    async def _decision_phase(self, reasoning_output: Dict[str, Any]) -> Dict[str, Any]:
        """Make decisions based on reasoning output"""
        if not self.decision_engine:
            return {"decision": "no_action", "reasoning": reasoning_output}
        
        # Utility-based decision making
        utility_decision = await self.decision_engine.utility_based_decision.evaluate_options(
            reasoning_output, self.active_goals
        )
        
        # Consider emotional factors
        if hasattr(self.decision_engine, 'emotional_decision'):
            emotional_adjustment = await self.decision_engine.emotional_decision.adjust_decision(
                utility_decision, self.cognitive_state.emotional_valence
            )
        else:
            emotional_adjustment = utility_decision
        
        return {
            "primary_decision": emotional_adjustment,
            "utility_analysis": utility_decision,
            "decision_confidence": self.decision_engine.get_confidence(),
            "reasoning_basis": reasoning_output
        }
    
    async def _action_planning_phase(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Plan concrete actions based on decisions"""
        action_plan = {
            "immediate_actions": [],
            "sequential_actions": [],
            "contingency_plans": [],
            "monitoring_points": [],
            "expected_outcomes": []
        }
        
        # Generate action sequence
        primary_decision = decision.get("primary_decision", {})
        
        if primary_decision.get("action_type") == "information_seeking":
            action_plan["immediate_actions"].append({
                "type": "query_knowledge_base",
                "parameters": primary_decision.get("query_parameters", {}),
                "priority": "high"
            })
        elif primary_decision.get("action_type") == "recommendation":
            action_plan["immediate_actions"].append({
                "type": "generate_recommendation",
                "parameters": primary_decision.get("recommendation_parameters", {}),
                "priority": "medium"
            })
        elif primary_decision.get("action_type") == "problem_solving":
            action_plan["sequential_actions"].extend([
                {
                    "type": "analyze_problem",
                    "parameters": primary_decision.get("problem_parameters", {}),
                    "step_order": 1
                },
                {
                    "type": "generate_solutions",
                    "parameters": {},
                    "step_order": 2
                },
                {
                    "type": "evaluate_solutions",
                    "parameters": {},
                    "step_order": 3
                }
            ])
        
        # Add monitoring and contingency planning
        action_plan["monitoring_points"].append({
            "checkpoint": "action_initiation",
            "success_criteria": primary_decision.get("success_criteria", {}),
            "failure_thresholds": primary_decision.get("failure_thresholds", {})
        })
        
        return action_plan
    
    async def _learning_phase(self, input_data: Dict[str, Any], action_plan: Dict[str, Any], cycle_id: str):
        """Learn from the cognitive cycle"""
        if not self.learning_system:
            return
        
        # Create learning episode
        episode = {
            "cycle_id": cycle_id,
            "input_data": input_data,
            "action_plan": action_plan,
            "cognitive_state": self.cognitive_state,
            "timestamp": datetime.now()
        }
        
        # Adaptive learning
        await self.learning_system.adaptive_learning.update_from_episode(episode)
        
        # Meta-learning (learning about learning strategies)
        if hasattr(self.learning_system, 'meta_learning'):
            await self.learning_system.meta_learning.update_learning_strategies(
                episode, self.cognitive_profile
            )
        
        # Memory consolidation
        await self.memory_system.consolidate_episode(episode)
    
    async def _metacognitive_phase(self, cycle_id: str, cycle_start: datetime):
        """Metacognitive monitoring and control"""
        if not self.metacognitive_controller:
            return
        
        processing_time = (datetime.now() - cycle_start).total_seconds()
        
        # Self-monitoring
        performance_metrics = {
            "processing_time": processing_time,
            "cognitive_load": self.cognitive_state.cognitive_load,
            "confidence": self.cognitive_state.confidence_level,
            "working_memory_usage": 1.0 - self.cognitive_state.get_cognitive_capacity()
        }
        
        await self.metacognitive_controller.monitor_performance(
            cycle_id, performance_metrics
        )
        
        # Strategy selection and adjustment
        if processing_time > self.cycle_time * 2:  # If cycle is taking too long
            await self.metacognitive_controller.adjust_processing_strategy(
                "reduce_complexity", self.cognitive_state
            )
    
    def _update_cognitive_state(self, action_plan: Dict[str, Any]):
        """Update the cognitive state based on processing results"""
        # Update cognitive load based on action complexity
        action_complexity = len(action_plan.get("immediate_actions", [])) + \
                           len(action_plan.get("sequential_actions", [])) * 0.5
        
        self.cognitive_state.cognitive_load = min(1.0, action_complexity * 0.2)
        
        # Update confidence based on decision strength
        decision_confidence = action_plan.get("decision_confidence", 0.5)
        self.cognitive_state.confidence_level = decision_confidence
        
        # Update activation level based on task urgency
        if any(action.get("priority") == "high" for action in action_plan.get("immediate_actions", [])):
            self.cognitive_state.activation_level = ActivationLevel.HIGH
        else:
            self.cognitive_state.activation_level = ActivationLevel.MODERATE
        
        # Update timestamp
        self.cognitive_state.timestamp = datetime.now()
    
    async def set_goal(self, goal: Dict[str, Any]):
        """Set a cognitive goal"""
        self.active_goals.append(goal)
        if self.metacognitive_controller:
            await self.metacognitive_controller.update_goal_structure(self.active_goals)
    
    async def get_cognitive_status(self) -> Dict[str, Any]:
        """Get current cognitive status"""
        return {
            "persona_type": self.persona_type,
            "cognitive_state": self.cognitive_state,
            "cognitive_profile": self.cognitive_profile,
            "active_goals": self.active_goals,
            "module_status": {
                "perception": self.perception_module is not None,
                "reasoning": self.reasoning_engine is not None,
                "memory": self.memory_system is not None,
                "learning": self.learning_system is not None,
                "decision": self.decision_engine is not None,
                "attention": self.attention_mechanism is not None,
                "metacognition": self.metacognitive_controller is not None
            }
        }