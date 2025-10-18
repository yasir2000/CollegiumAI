"""
CollegiumAI Cognitive Architecture - Advanced Reasoning Engine
Multi-layered reasoning with causal, analogical, and abstract thinking capabilities
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime
import uuid
import networkx as nx
from collections import defaultdict

class ReasoningType(Enum):
    """Types of reasoning processes"""
    DEDUCTIVE = "deductive"          # General to specific
    INDUCTIVE = "inductive"          # Specific to general
    ABDUCTIVE = "abductive"          # Best explanation
    ANALOGICAL = "analogical"        # Pattern matching across domains
    CAUSAL = "causal"               # Cause-effect relationships
    TEMPORAL = "temporal"           # Time-based reasoning
    SPATIAL = "spatial"             # Spatial relationships
    METACOGNITIVE = "metacognitive"  # Reasoning about reasoning

@dataclass
class ReasoningStep:
    """Represents a single step in reasoning process"""
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reasoning_type: ReasoningType = ReasoningType.DEDUCTIVE
    input_premises: List[Any] = field(default_factory=list)
    reasoning_rule: str = ""
    output_conclusion: Any = None
    confidence: float = 0.5
    justification: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ReasoningChain:
    """Represents a complete reasoning chain"""
    chain_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    steps: List[ReasoningStep] = field(default_factory=list)
    initial_premises: List[Any] = field(default_factory=list)
    final_conclusion: Any = None
    overall_confidence: float = 0.5
    reasoning_strategy: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

class ReasoningEngine:
    """
    Advanced reasoning engine that performs multiple types of reasoning
    Inspired by dual-process theory and cognitive science research
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"ReasoningEngine-{persona_type}")
        
        # Reasoning components
        self.causal_reasoning = CausalReasoning(persona_type)
        self.analogical_reasoning = AnalogicalReasoning(persona_type)
        
        # Knowledge base connection
        self.long_term_memory = None
        
        # Reasoning parameters
        self.reasoning_depth = self._initialize_reasoning_depth()
        self.confidence_threshold = 0.6
        self.max_reasoning_steps = 10
        
        # Reasoning history
        self.reasoning_history = []
        
        # Persona-specific reasoning biases and strengths
        self.reasoning_profile = self._initialize_reasoning_profile()
    
    def _initialize_reasoning_depth(self) -> int:
        """Initialize reasoning depth based on persona type"""
        if "faculty" in self.persona_type.lower() or "researcher" in self.persona_type.lower():
            return 8  # Deep reasoning for academics
        elif "advisor" in self.persona_type.lower():
            return 6  # Moderate-deep reasoning for counseling
        elif "student" in self.persona_type.lower():
            return 5  # Moderate reasoning for learning
        elif "administrator" in self.persona_type.lower():
            return 7  # Deep reasoning for management
        else:
            return 5  # Default moderate reasoning
    
    def _initialize_reasoning_profile(self) -> Dict[str, float]:
        """Initialize persona-specific reasoning preferences and strengths"""
        base_profile = {
            "deductive_strength": 0.7,
            "inductive_strength": 0.6,
            "analogical_strength": 0.5,
            "causal_strength": 0.6,
            "abstract_thinking": 0.6,
            "logical_rigor": 0.7,
            "creative_leaps": 0.4,
            "evidence_weighting": 0.8,
            "uncertainty_tolerance": 0.5
        }
        
        # Adjust based on persona type
        if "faculty" in self.persona_type.lower() or "researcher" in self.persona_type.lower():
            base_profile.update({
                "deductive_strength": 0.9,
                "abstract_thinking": 0.9,
                "logical_rigor": 0.9,
                "evidence_weighting": 0.9,
                "creative_leaps": 0.7
            })
        elif "student" in self.persona_type.lower():
            base_profile.update({
                "inductive_strength": 0.8,
                "analogical_strength": 0.7,
                "creative_leaps": 0.6,
                "uncertainty_tolerance": 0.6
            })
        elif "advisor" in self.persona_type.lower():
            base_profile.update({
                "analogical_strength": 0.8,
                "causal_strength": 0.8,
                "evidence_weighting": 0.8,
                "uncertainty_tolerance": 0.7
            })
        
        return base_profile
    
    def connect_to_memory(self, long_term_memory):
        """Connect to long-term memory system"""
        self.long_term_memory = long_term_memory
        self.causal_reasoning.connect_to_memory(long_term_memory)
        self.analogical_reasoning.connect_to_memory(long_term_memory)
    
    async def reason_about_situation(self, situation: Dict[str, Any], 
                                   reasoning_goals: List[str] = None) -> ReasoningChain:
        """Main reasoning method that coordinates different reasoning types"""
        
        reasoning_chain = ReasoningChain(
            initial_premises=[situation],
            reasoning_strategy="multi_modal_reasoning",
            context={"situation": situation, "goals": reasoning_goals or []}
        )
        
        # Step 1: Analyze the situation and extract key elements
        situation_analysis = await self._analyze_situation_structure(situation)
        reasoning_chain.steps.append(ReasoningStep(
            reasoning_type=ReasoningType.ABDUCTIVE,
            input_premises=[situation],
            reasoning_rule="situation_decomposition",
            output_conclusion=situation_analysis,
            confidence=0.8,
            justification="Breaking down situation into analyzable components"
        ))
        
        # Step 2: Apply causal reasoning to understand relationships
        causal_analysis = await self.causal_reasoning.analyze_causality(
            situation_analysis, self.reasoning_profile["causal_strength"]
        )
        reasoning_chain.steps.append(ReasoningStep(
            reasoning_type=ReasoningType.CAUSAL,
            input_premises=[situation_analysis],
            reasoning_rule="causal_analysis",
            output_conclusion=causal_analysis,
            confidence=causal_analysis.get("confidence", 0.6),
            justification="Identifying causal relationships and dependencies"
        ))
        
        # Step 3: Find analogical patterns from past experience
        analogical_insights = await self.analogical_reasoning.find_analogies(
            situation_analysis, self.long_term_memory
        )
        reasoning_chain.steps.append(ReasoningStep(
            reasoning_type=ReasoningType.ANALOGICAL,
            input_premises=[situation_analysis],
            reasoning_rule="analogical_mapping",
            output_conclusion=analogical_insights,
            confidence=analogical_insights.get("confidence", 0.5),
            justification="Finding similar patterns from past experience"
        ))
        
        # Step 4: Abstract pattern recognition
        abstract_patterns = await self.identify_abstract_patterns(
            {"causal": causal_analysis, "analogical": analogical_insights},
            self.reasoning_profile["abstract_thinking"]
        )
        reasoning_chain.steps.append(ReasoningStep(
            reasoning_type=ReasoningType.INDUCTIVE,
            input_premises=[causal_analysis, analogical_insights],
            reasoning_rule="pattern_abstraction",
            output_conclusion=abstract_patterns,
            confidence=abstract_patterns.get("confidence", 0.6),
            justification="Extracting higher-level patterns and principles"
        ))
        
        # Step 5: Deductive reasoning for specific conclusions
        if reasoning_goals:
            deductive_conclusions = await self._apply_deductive_reasoning(
                abstract_patterns, reasoning_goals
            )
            reasoning_chain.steps.append(ReasoningStep(
                reasoning_type=ReasoningType.DEDUCTIVE,
                input_premises=[abstract_patterns, reasoning_goals],
                reasoning_rule="goal_directed_deduction",
                output_conclusion=deductive_conclusions,
                confidence=deductive_conclusions.get("confidence", 0.7),
                justification="Applying general principles to specific goals"
            ))
            reasoning_chain.final_conclusion = deductive_conclusions
        else:
            reasoning_chain.final_conclusion = abstract_patterns
        
        # Calculate overall confidence
        reasoning_chain.overall_confidence = self._calculate_chain_confidence(reasoning_chain.steps)
        
        # Store reasoning chain
        self.reasoning_history.append(reasoning_chain)
        
        return reasoning_chain
    
    async def _analyze_situation_structure(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and decompose situation structure"""
        structure = {
            "entities": [],
            "relationships": [],
            "constraints": [],
            "goals": [],
            "context_factors": [],
            "temporal_aspects": [],
            "uncertainty_factors": []
        }
        
        # Extract entities (people, objects, concepts)
        if "student_id" in situation or "user_id" in situation:
            structure["entities"].append({
                "type": "person",
                "role": "student" if "student_id" in situation else "user",
                "id": situation.get("student_id") or situation.get("user_id")
            })
        
        # Extract academic entities
        academic_keywords = ["course", "grade", "assignment", "exam", "project", "research"]
        for keyword in academic_keywords:
            if keyword in str(situation).lower():
                structure["entities"].append({
                    "type": "academic_entity",
                    "category": keyword,
                    "mentioned": True
                })
        
        # Extract goals from the situation
        goal_indicators = ["want", "need", "goal", "objective", "aim", "plan"]
        for indicator in goal_indicators:
            if indicator in str(situation).lower():
                structure["goals"].append({
                    "type": "explicit_goal",
                    "indicator": indicator,
                    "context": situation
                })
        
        # Extract temporal aspects
        temporal_keywords = ["deadline", "schedule", "time", "when", "date", "semester"]
        for keyword in temporal_keywords:
            if keyword in str(situation).lower():
                structure["temporal_aspects"].append({
                    "type": "temporal_constraint",
                    "keyword": keyword,
                    "urgency": self._assess_temporal_urgency(keyword, situation)
                })
        
        # Extract constraints
        constraint_keywords = ["can't", "cannot", "unable", "restriction", "limit", "requirement"]
        for keyword in constraint_keywords:
            if keyword in str(situation).lower():
                structure["constraints"].append({
                    "type": "explicit_constraint",
                    "keyword": keyword,
                    "impact": "high"
                })
        
        return structure
    
    def _assess_temporal_urgency(self, keyword: str, situation: Dict[str, Any]) -> str:
        """Assess urgency based on temporal keywords"""
        high_urgency = ["deadline", "asap", "urgent", "immediately"]
        medium_urgency = ["soon", "week", "schedule"]
        
        if any(word in str(situation).lower() for word in high_urgency):
            return "high"
        elif any(word in str(situation).lower() for word in medium_urgency):
            return "medium"
        else:
            return "low"
    
    async def identify_abstract_patterns(self, reasoning_input: Dict[str, Any], 
                                       abstraction_level: float) -> Dict[str, Any]:
        """Identify abstract patterns from reasoning inputs"""
        patterns = {
            "meta_patterns": [],
            "principle_patterns": [],
            "strategic_patterns": [],
            "behavioral_patterns": [],
            "confidence": abstraction_level * 0.8
        }
        
        # Extract meta-patterns (patterns about patterns)
        causal_data = reasoning_input.get("causal", {})
        analogical_data = reasoning_input.get("analogical", {})
        
        # Look for recurring causal structures
        if causal_data.get("causal_chains"):
            patterns["meta_patterns"].append({
                "type": "causal_structure",
                "pattern": "multi_step_causation",
                "description": "Complex causal chains requiring multi-step intervention"
            })
        
        # Look for analogical pattern types
        if analogical_data.get("analogies"):
            analogy_types = [a.get("analogy_type") for a in analogical_data["analogies"]]
            common_types = [t for t in set(analogy_types) if analogy_types.count(t) > 1]
            for analogy_type in common_types:
                patterns["meta_patterns"].append({
                    "type": "analogical_structure",
                    "pattern": f"recurring_{analogy_type}",
                    "description": f"Recurring {analogy_type} pattern in similar situations"
                })
        
        # Extract principle patterns (general rules or guidelines)
        if causal_data.get("root_causes"):
            root_causes = causal_data["root_causes"]
            if any("academic" in str(cause).lower() for cause in root_causes):
                patterns["principle_patterns"].append({
                    "type": "academic_principle",
                    "principle": "academic_performance_multi_factorial",
                    "description": "Academic issues typically have multiple contributing factors"
                })
        
        # Extract strategic patterns (approaches to problem-solving)
        if analogical_data.get("successful_strategies"):
            strategies = analogical_data["successful_strategies"]
            patterns["strategic_patterns"].extend([{
                "type": "solution_strategy",
                "strategy": strategy.get("name", "unknown"),
                "effectiveness": strategy.get("effectiveness", 0.5),
                "description": strategy.get("description", "")
            } for strategy in strategies])
        
        return patterns
    
    async def _apply_deductive_reasoning(self, abstract_patterns: Dict[str, Any], 
                                       goals: List[str]) -> Dict[str, Any]:
        """Apply deductive reasoning to derive specific conclusions"""
        conclusions = {
            "specific_recommendations": [],
            "action_sequences": [],
            "expected_outcomes": [],
            "confidence": 0.7
        }
        
        # Apply principle patterns to specific goals
        principle_patterns = abstract_patterns.get("principle_patterns", [])
        strategic_patterns = abstract_patterns.get("strategic_patterns", [])
        
        for goal in goals:
            goal_lower = goal.lower()
            
            # Match principles to goals
            relevant_principles = [p for p in principle_patterns 
                                 if any(keyword in goal_lower for keyword in 
                                       str(p).lower().split())]
            
            # Match strategies to goals
            relevant_strategies = [s for s in strategic_patterns
                                 if s.get("effectiveness", 0) > 0.6]
            
            # Generate specific recommendations
            if relevant_principles or relevant_strategies:
                recommendation = {
                    "goal": goal,
                    "applicable_principles": relevant_principles,
                    "recommended_strategies": relevant_strategies[:3],  # Top 3 strategies
                    "confidence": min(0.9, len(relevant_strategies) * 0.2 + 0.3)
                }
                conclusions["specific_recommendations"].append(recommendation)
        
        return conclusions
    
    def _calculate_chain_confidence(self, steps: List[ReasoningStep]) -> float:
        """Calculate overall confidence for reasoning chain"""
        if not steps:
            return 0.0
        
        # Weight later steps more heavily (they build on earlier ones)
        weights = [i + 1 for i in range(len(steps))]
        weighted_sum = sum(step.confidence * weight for step, weight in zip(steps, weights))
        total_weight = sum(weights)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def get_confidence(self) -> float:
        """Get current reasoning confidence"""
        if not self.reasoning_history:
            return 0.5
        
        recent_chains = self.reasoning_history[-5:]  # Last 5 reasoning chains
        return np.mean([chain.overall_confidence for chain in recent_chains])
    
    async def explain_reasoning(self, chain_id: str) -> Dict[str, Any]:
        """Provide explanation of reasoning process"""
        chain = next((c for c in self.reasoning_history if c.chain_id == chain_id), None)
        if not chain:
            return {"error": "Reasoning chain not found"}
        
        explanation = {
            "chain_id": chain_id,
            "reasoning_strategy": chain.reasoning_strategy,
            "step_by_step_explanation": [],
            "key_insights": [],
            "confidence_analysis": {},
            "assumptions_made": []
        }
        
        # Explain each step
        for i, step in enumerate(chain.steps):
            step_explanation = {
                "step_number": i + 1,
                "reasoning_type": step.reasoning_type.value,
                "what_happened": step.justification,
                "confidence": step.confidence,
                "key_inputs": len(step.input_premises),
                "conclusion_type": type(step.output_conclusion).__name__
            }
            explanation["step_by_step_explanation"].append(step_explanation)
        
        # Extract key insights
        high_confidence_steps = [s for s in chain.steps if s.confidence > 0.7]
        for step in high_confidence_steps:
            explanation["key_insights"].append({
                "insight": step.justification,
                "confidence": step.confidence,
                "reasoning_type": step.reasoning_type.value
            })
        
        # Analyze confidence
        explanation["confidence_analysis"] = {
            "overall_confidence": chain.overall_confidence,
            "confidence_trend": [s.confidence for s in chain.steps],
            "most_confident_step": max(chain.steps, key=lambda s: s.confidence).reasoning_type.value,
            "least_confident_step": min(chain.steps, key=lambda s: s.confidence).reasoning_type.value
        }
        
        return explanation


class CausalReasoning:
    """
    Specialized causal reasoning component
    Identifies cause-effect relationships and causal chains
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"CausalReasoning-{persona_type}")
        self.long_term_memory = None
        self.causal_knowledge = self._initialize_causal_knowledge()
    
    def _initialize_causal_knowledge(self) -> Dict[str, Any]:
        """Initialize domain-specific causal knowledge"""
        knowledge = {
            "academic_domain": {
                "common_causes": {
                    "poor_performance": ["lack_of_study", "difficulty_understanding", "personal_issues", "time_management"],
                    "stress": ["workload", "deadlines", "social_pressure", "financial_concerns"],
                    "dropout_risk": ["academic_failure", "financial_problems", "lack_of_engagement", "personal_crises"]
                },
                "causal_patterns": [
                    {"cause": "inadequate_preparation", "effect": "poor_test_performance", "strength": 0.8},
                    {"cause": "high_stress", "effect": "reduced_cognitive_function", "strength": 0.7},
                    {"cause": "lack_of_engagement", "effect": "poor_retention", "strength": 0.75}
                ]
            },
            "social_domain": {
                "common_causes": {
                    "isolation": ["introversion", "cultural_barriers", "social_anxiety", "time_constraints"],
                    "conflict": ["miscommunication", "competing_interests", "stress", "cultural_differences"]
                }
            },
            "temporal_domain": {
                "common_causes": {
                    "procrastination": ["anxiety", "perfectionism", "lack_of_motivation", "overwhelm"],
                    "time_pressure": ["poor_planning", "unexpected_events", "overcommitment"]
                }
            }
        }
        
        return knowledge
    
    def connect_to_memory(self, long_term_memory):
        """Connect to long-term memory system"""
        self.long_term_memory = long_term_memory
    
    async def analyze_causality(self, situation_data: Dict[str, Any], 
                              causal_strength: float) -> Dict[str, Any]:
        """Analyze causal relationships in the given situation"""
        
        causal_analysis = {
            "identified_causes": [],
            "causal_chains": [],
            "root_causes": [],
            "contributing_factors": [],
            "causal_confidence": causal_strength,
            "intervention_points": []
        }
        
        # Extract entities and their relationships
        entities = situation_data.get("entities", [])
        constraints = situation_data.get("constraints", [])
        temporal_aspects = situation_data.get("temporal_aspects", [])
        
        # Identify direct causes based on domain knowledge
        direct_causes = await self._identify_direct_causes(entities, constraints, temporal_aspects)
        causal_analysis["identified_causes"] = direct_causes
        
        # Build causal chains
        causal_chains = await self._build_causal_chains(direct_causes)
        causal_analysis["causal_chains"] = causal_chains
        
        # Identify root causes
        root_causes = await self._identify_root_causes(causal_chains)
        causal_analysis["root_causes"] = root_causes
        
        # Identify intervention points
        intervention_points = await self._identify_intervention_points(causal_chains)
        causal_analysis["intervention_points"] = intervention_points
        
        return causal_analysis
    
    async def _identify_direct_causes(self, entities: List[Dict], 
                                    constraints: List[Dict], 
                                    temporal_aspects: List[Dict]) -> List[Dict[str, Any]]:
        """Identify direct causal relationships"""
        direct_causes = []
        
        # Check academic causes
        academic_entities = [e for e in entities if e.get("type") == "academic_entity"]
        for entity in academic_entities:
            category = entity.get("category", "")
            if category in self.causal_knowledge["academic_domain"]["common_causes"]:
                potential_causes = self.causal_knowledge["academic_domain"]["common_causes"][category]
                for cause in potential_causes:
                    direct_causes.append({
                        "cause": cause,
                        "effect": category,
                        "evidence_strength": 0.6,
                        "domain": "academic",
                        "type": "direct"
                    })
        
        # Check temporal causes
        high_urgency_temporal = [t for t in temporal_aspects if t.get("urgency") == "high"]
        if high_urgency_temporal:
            direct_causes.append({
                "cause": "time_pressure",
                "effect": "stress_increase",
                "evidence_strength": 0.8,
                "domain": "temporal",
                "type": "direct"
            })
        
        # Check constraint-based causes
        for constraint in constraints:
            if constraint.get("impact") == "high":
                direct_causes.append({
                    "cause": constraint.get("keyword", "unknown_constraint"),
                    "effect": "limited_options",
                    "evidence_strength": 0.7,
                    "domain": "constraint",
                    "type": "direct"
                })
        
        return direct_causes
    
    async def _build_causal_chains(self, direct_causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build multi-step causal chains"""
        chains = []
        
        # Group causes by domain
        domain_causes = defaultdict(list)
        for cause in direct_causes:
            domain_causes[cause["domain"]].append(cause)
        
        # Build chains within domains
        for domain, causes in domain_causes.items():
            if len(causes) > 1:
                # Create a chain linking related causes
                chain = {
                    "chain_id": str(uuid.uuid4()),
                    "domain": domain,
                    "steps": causes,
                    "chain_strength": min([c["evidence_strength"] for c in causes]),
                    "complexity": len(causes)
                }
                chains.append(chain)
        
        # Look for cross-domain causal relationships
        academic_causes = domain_causes.get("academic", [])
        temporal_causes = domain_causes.get("temporal", [])
        
        if academic_causes and temporal_causes:
            # Time pressure can worsen academic issues
            cross_domain_chain = {
                "chain_id": str(uuid.uuid4()),
                "domain": "cross_domain",
                "steps": temporal_causes + academic_causes,
                "chain_strength": 0.6,
                "complexity": len(temporal_causes) + len(academic_causes),
                "interaction_type": "amplification"
            }
            chains.append(cross_domain_chain)
        
        return chains
    
    async def _identify_root_causes(self, causal_chains: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify root causes from causal chains"""
        root_causes = []
        
        # Find causes that appear early in multiple chains
        cause_frequency = defaultdict(int)
        cause_positions = defaultdict(list)
        
        for chain in causal_chains:
            steps = chain.get("steps", [])
            for i, step in enumerate(steps):
                cause = step.get("cause")
                cause_frequency[cause] += 1
                cause_positions[cause].append(i)
        
        # Root causes are frequent and appear early in chains
        for cause, frequency in cause_frequency.items():
            avg_position = np.mean(cause_positions[cause])
            if frequency > 1 or avg_position < 1:  # Appears multiple times or early
                root_causes.append({
                    "cause": cause,
                    "frequency": frequency,
                    "average_position": avg_position,
                    "root_likelihood": max(0.3, min(0.9, frequency * 0.3 + (2 - avg_position) * 0.2))
                })
        
        # Sort by root likelihood
        root_causes.sort(key=lambda x: x["root_likelihood"], reverse=True)
        
        return root_causes[:5]  # Top 5 root causes
    
    async def _identify_intervention_points(self, causal_chains: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify optimal points for intervention"""
        intervention_points = []
        
        for chain in causal_chains:
            steps = chain.get("steps", [])
            chain_strength = chain.get("chain_strength", 0.5)
            
            # Early intervention is usually more effective
            for i, step in enumerate(steps):
                intervention_effectiveness = max(0.2, (len(steps) - i) / len(steps) * chain_strength)
                
                intervention_points.append({
                    "chain_id": chain["chain_id"],
                    "step_index": i,
                    "cause": step.get("cause"),
                    "effect": step.get("effect"),
                    "intervention_effectiveness": intervention_effectiveness,
                    "intervention_difficulty": self._assess_intervention_difficulty(step.get("cause")),
                    "impact_scope": step.get("domain", "unknown")
                })
        
        # Sort by effectiveness and feasibility
        intervention_points.sort(
            key=lambda x: x["intervention_effectiveness"] / max(0.1, x["intervention_difficulty"]), 
            reverse=True
        )
        
        return intervention_points[:10]  # Top 10 intervention points
    
    def _assess_intervention_difficulty(self, cause: str) -> float:
        """Assess how difficult it would be to intervene on a specific cause"""
        # Some causes are easier to address than others
        easy_interventions = ["study_habits", "time_management", "organization", "scheduling"]
        moderate_interventions = ["stress", "motivation", "engagement", "understanding"]
        difficult_interventions = ["financial_problems", "family_issues", "mental_health", "personal_crises"]
        
        if any(easy in cause.lower() for easy in easy_interventions):
            return 0.3
        elif any(moderate in cause.lower() for moderate in moderate_interventions):
            return 0.6
        elif any(difficult in cause.lower() for difficult in difficult_interventions):
            return 0.9
        else:
            return 0.5  # Default moderate difficulty


class AnalogicalReasoning:
    """
    Specialized analogical reasoning component
    Finds patterns and analogies from past experiences
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"AnalogicalReasoning-{persona_type}")
        self.long_term_memory = None
        self.analogy_templates = self._initialize_analogy_templates()
    
    def _initialize_analogy_templates(self) -> Dict[str, Any]:
        """Initialize templates for analogical matching"""
        templates = {
            "academic_analogies": [
                {
                    "pattern": "skill_building",
                    "structure": {"initial_difficulty": "high", "practice": "required", "outcome": "mastery"},
                    "examples": ["learning_to_drive", "musical_instrument", "foreign_language"]
                },
                {
                    "pattern": "overcoming_obstacles",
                    "structure": {"challenge": "present", "resources": "available", "persistence": "required"},
                    "examples": ["athletic_training", "project_completion", "habit_formation"]
                }
            ],
            "social_analogies": [
                {
                    "pattern": "relationship_building",
                    "structure": {"initial_contact": "awkward", "shared_activities": "bonding", "outcome": "friendship"},
                    "examples": ["workplace_relationships", "neighborhood_connections", "hobby_groups"]
                }
            ],
            "problem_solving_analogies": [
                {
                    "pattern": "systematic_approach",
                    "structure": {"problem_definition": "clear", "step_by_step": "process", "outcome": "solution"},
                    "examples": ["recipe_following", "assembly_instructions", "troubleshooting_guide"]
                }
            ]
        }
        
        return templates
    
    def connect_to_memory(self, long_term_memory):
        """Connect to long-term memory system"""
        self.long_term_memory = long_term_memory
    
    async def find_analogies(self, situation_data: Dict[str, Any], 
                           long_term_memory) -> Dict[str, Any]:
        """Find analogical patterns from past experiences"""
        
        analogical_analysis = {
            "analogies": [],
            "successful_strategies": [],
            "pattern_matches": [],
            "confidence": 0.5,
            "relevance_scores": {}
        }
        
        # Extract key features from current situation
        situation_features = await self._extract_analogical_features(situation_data)
        
        # Search for analogous situations in memory
        analogous_cases = await self._search_analogous_cases(situation_features, long_term_memory)
        analogical_analysis["analogies"] = analogous_cases
        
        # Extract successful strategies from analogous cases
        successful_strategies = await self._extract_successful_strategies(analogous_cases)
        analogical_analysis["successful_strategies"] = successful_strategies
        
        # Match against known patterns
        pattern_matches = await self._match_against_templates(situation_features)
        analogical_analysis["pattern_matches"] = pattern_matches
        
        # Calculate overall confidence
        analogical_analysis["confidence"] = self._calculate_analogical_confidence(
            analogous_cases, pattern_matches
        )
        
        return analogical_analysis
    
    async def _extract_analogical_features(self, situation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features relevant for analogical matching"""
        features = {
            "structural_features": [],
            "functional_features": [],
            "relational_features": [],
            "goal_features": [],
            "constraint_features": []
        }
        
        # Extract structural features (what entities are involved)
        entities = situation_data.get("entities", [])
        for entity in entities:
            features["structural_features"].append({
                "type": entity.get("type"),
                "role": entity.get("role"),
                "category": entity.get("category")
            })
        
        # Extract functional features (what functions/purposes are served)
        goals = situation_data.get("goals", [])
        for goal in goals:
            features["functional_features"].append({
                "type": goal.get("type"),
                "purpose": self._infer_purpose(goal)
            })
        
        # Extract relational features (how entities relate)
        relationships = situation_data.get("relationships", [])
        features["relational_features"] = relationships
        
        # Extract goal features
        features["goal_features"] = goals
        
        # Extract constraint features
        constraints = situation_data.get("constraints", [])
        features["constraint_features"] = constraints
        
        return features
    
    def _infer_purpose(self, goal: Dict[str, Any]) -> str:
        """Infer the purpose/function of a goal"""
        goal_text = str(goal).lower()
        
        if any(word in goal_text for word in ["improve", "better", "enhance"]):
            return "improvement"
        elif any(word in goal_text for word in ["learn", "understand", "study"]):
            return "learning"
        elif any(word in goal_text for word in ["solve", "fix", "resolve"]):
            return "problem_solving"
        elif any(word in goal_text for word in ["connect", "meet", "relationship"]):
            return "social_connection"
        else:
            return "general_achievement"
    
    async def _search_analogous_cases(self, situation_features: Dict[str, Any], 
                                    long_term_memory) -> List[Dict[str, Any]]:
        """Search for analogous cases in long-term memory"""
        analogous_cases = []
        
        # This would typically search episodic memory for similar cases
        # For now, we'll simulate based on feature matching
        
        # Match structural similarity
        structural_features = situation_features.get("structural_features", [])
        if any(f.get("type") == "academic_entity" for f in structural_features):
            analogous_cases.append({
                "case_id": "academic_struggle_case_1",
                "similarity_score": 0.8,
                "analogy_type": "academic_challenge",
                "key_similarities": ["academic_context", "performance_concern", "time_pressure"],
                "successful_outcome": True,
                "strategy_used": "systematic_study_plan"
            })
        
        # Match functional similarity
        functional_features = situation_features.get("functional_features", [])
        learning_purposes = [f for f in functional_features if f.get("purpose") == "learning"]
        if learning_purposes:
            analogous_cases.append({
                "case_id": "skill_acquisition_case_1",
                "similarity_score": 0.7,
                "analogy_type": "skill_building",
                "key_similarities": ["learning_goal", "progressive_difficulty", "practice_required"],
                "successful_outcome": True,
                "strategy_used": "incremental_practice"
            })
        
        # Match relational similarity
        constraint_features = situation_features.get("constraint_features", [])
        if constraint_features:
            analogous_cases.append({
                "case_id": "resource_constraint_case_1",
                "similarity_score": 0.6,
                "analogy_type": "constraint_satisfaction",
                "key_similarities": ["limited_resources", "competing_demands", "priority_setting"],
                "successful_outcome": True,
                "strategy_used": "priority_based_allocation"
            })
        
        return analogous_cases
    
    async def _extract_successful_strategies(self, analogous_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract successful strategies from analogous cases"""
        strategies = []
        
        for case in analogous_cases:
            if case.get("successful_outcome"):
                strategy = {
                    "name": case.get("strategy_used"),
                    "analogy_type": case.get("analogy_type"),
                    "effectiveness": case.get("similarity_score", 0.5),
                    "key_elements": self._extract_strategy_elements(case.get("strategy_used")),
                    "adaptation_needed": self._assess_adaptation_needed(case.get("similarity_score", 0.5))
                }
                strategies.append(strategy)
        
        return strategies
    
    def _extract_strategy_elements(self, strategy_name: str) -> List[str]:
        """Extract key elements of a strategy"""
        strategy_elements = {
            "systematic_study_plan": ["schedule_creation", "goal_setting", "progress_tracking", "regular_review"],
            "incremental_practice": ["small_steps", "consistent_practice", "difficulty_progression", "feedback_integration"],
            "priority_based_allocation": ["priority_identification", "resource_mapping", "trade_off_analysis", "flexible_adjustment"]
        }
        
        return strategy_elements.get(strategy_name, ["structured_approach", "consistent_action", "monitoring"])
    
    def _assess_adaptation_needed(self, similarity_score: float) -> str:
        """Assess how much adaptation is needed for a strategy"""
        if similarity_score > 0.8:
            return "minimal"
        elif similarity_score > 0.6:
            return "moderate"
        else:
            return "significant"
    
    async def _match_against_templates(self, situation_features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Match situation against known analogical templates"""
        pattern_matches = []
        
        # Check each template category
        for category, templates in self.analogy_templates.items():
            for template in templates:
                match_score = self._calculate_template_match(situation_features, template)
                if match_score > 0.4:  # Threshold for meaningful match
                    pattern_matches.append({
                        "template_category": category,
                        "pattern_name": template["pattern"],
                        "match_score": match_score,
                        "template_structure": template["structure"],
                        "example_domains": template["examples"]
                    })
        
        # Sort by match score
        pattern_matches.sort(key=lambda x: x["match_score"], reverse=True)
        
        return pattern_matches
    
    def _calculate_template_match(self, situation_features: Dict[str, Any], 
                                template: Dict[str, Any]) -> float:
        """Calculate how well situation matches a template"""
        match_score = 0.0
        template_structure = template.get("structure", {})
        
        # Check functional feature matches
        functional_features = situation_features.get("functional_features", [])
        functional_match = 0.0
        
        for feature in functional_features:
            purpose = feature.get("purpose", "")
            if purpose in str(template_structure).lower():
                functional_match += 0.3
        
        # Check goal feature matches
        goal_features = situation_features.get("goal_features", [])
        goal_match = 0.0
        
        for goal in goal_features:
            goal_text = str(goal).lower()
            if any(key in goal_text for key in template_structure.keys()):
                goal_match += 0.2
        
        # Check constraint matches
        constraint_features = situation_features.get("constraint_features", [])
        constraint_match = 0.0
        
        if constraint_features and "required" in str(template_structure).lower():
            constraint_match = 0.2
        
        match_score = min(1.0, functional_match + goal_match + constraint_match)
        return match_score
    
    def _calculate_analogical_confidence(self, analogous_cases: List[Dict[str, Any]], 
                                       pattern_matches: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in analogical reasoning"""
        if not analogous_cases and not pattern_matches:
            return 0.2
        
        # Weight case-based and template-based evidence
        case_confidence = 0.0
        if analogous_cases:
            case_scores = [case.get("similarity_score", 0.5) for case in analogous_cases]
            case_confidence = np.mean(case_scores) * 0.6  # Cases are weighted more heavily
        
        template_confidence = 0.0
        if pattern_matches:
            template_scores = [match.get("match_score", 0.5) for match in pattern_matches]
            template_confidence = np.mean(template_scores) * 0.4  # Templates provide structure
        
        overall_confidence = case_confidence + template_confidence
        return min(0.9, max(0.2, overall_confidence))  # Bound between 0.2 and 0.9