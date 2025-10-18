# CollegiumAI Cognitive Architecture
# Advanced cognitive capabilities for persona-specific AI support

from .cognitive_core import CognitiveEngine, CognitiveState
from .perception import PerceptionModule, MultiModalPerception
from .reasoning import ReasoningEngine, CausalReasoning, AnalogicalReasoning
from .memory import CognitiveMemory, WorkingMemory, LongTermMemory, EpisodicMemory
from .learning import AdaptiveLearning, MetaLearning, TransferLearning
from .decision_making import DecisionEngine, UtilityBasedDecision, EmotionalDecision
from .attention import AttentionMechanism, SelectiveAttention, DividedAttention
from .metacognition import MetacognitiveController, SelfMonitoring, StrategySelection
from .persona_cognition import PersonaCognitiveAgent, CognitivePersonaFactory

__all__ = [
    'CognitiveEngine',
    'CognitiveState', 
    'PerceptionModule',
    'MultiModalPerception',
    'ReasoningEngine',
    'CausalReasoning',
    'AnalogicalReasoning',
    'CognitiveMemory',
    'WorkingMemory',
    'LongTermMemory',
    'EpisodicMemory',
    'AdaptiveLearning',
    'MetaLearning',
    'TransferLearning',
    'DecisionEngine',
    'UtilityBasedDecision',
    'EmotionalDecision',
    'AttentionMechanism',
    'SelectiveAttention',
    'DividedAttention',
    'MetacognitiveController',
    'SelfMonitoring',
    'StrategySelection',
    'PersonaCognitiveAgent',
    'CognitivePersonaFactory'
]