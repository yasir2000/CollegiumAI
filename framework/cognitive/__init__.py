"""
CollegiumAI Cognitive Architecture
Advanced cognitive capabilities for intelligent persona support
"""

from .cognitive_core import CognitiveEngine, CognitiveState
from .perception import PerceptionModule, PerceptualFeature, MultiModalPerception
from .reasoning import ReasoningEngine, CausalReasoning, AnalogicalReasoning, ReasoningChain
from .memory import CognitiveMemory, WorkingMemory, EpisodicMemory, LongTermMemory
from .learning import AdaptiveLearning, MetaLearning, TransferLearning, LearningType, LearningEpisode
from .decision_making import DecisionEngine, DecisionType, DecisionCriteria, DecisionAlternative, DecisionContext
from .attention import AttentionMechanism, AttentionType, FocusState, AttentionTarget, AttentionalResource
from .metacognition import MetacognitiveController, MetacognitiveState, MetacognitiveStrategy, MetacognitiveInsight
from .persona_cognition import PersonaCognitiveAgent, PersonaType, CognitivePersonaFactory

__all__ = [
    # Core cognitive engine
    'CognitiveEngine',
    'CognitiveState',
    
    # Perception system
    'PerceptionModule',
    'PerceptualFeature',
    'MultiModalPerception',
    
    # Reasoning system
    'ReasoningEngine',
    'CausalReasoning',
    'AnalogicalReasoning', 
    'ReasoningChain',
    
    # Memory system
    'CognitiveMemory',
    'WorkingMemory',
    'EpisodicMemory',
    'LongTermMemory',
    
    # Learning system
    'AdaptiveLearning',
    'MetaLearning',
    'TransferLearning',
    'LearningType',
    'LearningEpisode',
    
    # Decision making system
    'DecisionEngine',
    'DecisionType',
    'DecisionCriteria',
    'DecisionAlternative',
    'DecisionContext',
    
    # Attention system
    'AttentionMechanism',
    'AttentionType',
    'FocusState',
    'AttentionTarget',
    'AttentionalResource',
    
    # Metacognitive system
    'MetacognitiveController',
    'MetacognitiveState',
    'MetacognitiveStrategy',
    'MetacognitiveInsight',
    
    # Persona-specific cognitive agents
    'PersonaCognitiveAgent',
    'PersonaType',
    'CognitivePersonaFactory'
]