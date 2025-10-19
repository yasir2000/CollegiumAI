"""
Advanced Cognitive Insights Dashboard
====================================

Comprehensive cognitive architecture monitoring system providing:
- Memory system visualization and analysis
- Attention pattern tracking and optimization
- Learning progression monitoring
- Decision-making process transparency
- Cognitive load assessment
- Knowledge graph visualization
- Metacognitive insights and recommendations
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict, field
from enum import Enum
import json
import numpy as np
import uuid
from collections import defaultdict, deque
import math

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    WORKING = "working"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    METACOGNITIVE = "metacognitive"

class AttentionType(Enum):
    FOCUSED = "focused"
    SELECTIVE = "selective"
    DIVIDED = "divided"
    SUSTAINED = "sustained"
    EXECUTIVE = "executive"

class CognitiveState(Enum):
    OPTIMAL = "optimal"
    MODERATE_LOAD = "moderate_load"
    HIGH_LOAD = "high_load"
    OVERLOADED = "overloaded"
    FATIGUED = "fatigued"
    LEARNING = "learning"
    CONSOLIDATING = "consolidating"

class DecisionType(Enum):
    ANALYTICAL = "analytical"
    INTUITIVE = "intuitive"
    HEURISTIC = "heuristic"
    COLLABORATIVE = "collaborative"
    AUTOMATED = "automated"

@dataclass
class MemoryItem:
    """Individual memory item in the cognitive system"""
    memory_id: str
    content: Dict[str, Any]
    memory_type: MemoryType
    strength: float  # 0.0 to 1.0
    access_count: int
    last_accessed: datetime
    created_at: datetime
    associated_concepts: List[str]
    emotional_valence: float  # -1.0 to 1.0
    importance_score: float  # 0.0 to 1.0
    decay_rate: float
    consolidation_status: str  # "unconsolidated", "consolidating", "consolidated"
    
    def __post_init__(self):
        if self.associated_concepts is None:
            self.associated_concepts = []

@dataclass
class AttentionFocus:
    """Attention focus tracking"""
    focus_id: str
    target_object: str
    attention_type: AttentionType
    intensity: float  # 0.0 to 1.0
    duration: float  # in seconds
    start_time: datetime
    end_time: Optional[datetime]
    context: Dict[str, Any]
    distractors: List[str]
    performance_impact: float  # -1.0 to 1.0

@dataclass
class LearningEvent:
    """Learning event tracking"""
    event_id: str
    learning_content: str
    learning_type: str  # "acquisition", "refinement", "adaptation", "correction"
    pre_knowledge_level: float
    post_knowledge_level: float
    learning_efficiency: float
    timestamp: datetime
    duration: float
    cognitive_load: float
    success_indicators: List[str]
    failure_indicators: List[str]
    
    def __post_init__(self):
        if self.success_indicators is None:
            self.success_indicators = []
        if self.failure_indicators is None:
            self.failure_indicators = []

@dataclass
class DecisionEvent:
    """Decision-making event tracking"""
    decision_id: str
    decision_context: str
    decision_type: DecisionType
    options_considered: List[str]
    chosen_option: str
    confidence_level: float  # 0.0 to 1.0
    decision_time: float  # time taken to decide
    information_used: List[str]
    cognitive_processes: List[str]
    outcome_prediction: str
    actual_outcome: Optional[str]
    timestamp: datetime
    decision_quality_score: Optional[float]

@dataclass
class CognitiveLoad:
    """Cognitive load measurement"""
    load_id: str
    timestamp: datetime
    working_memory_load: float  # 0.0 to 1.0
    attention_demand: float
    processing_complexity: float
    emotional_load: float
    overall_load: float
    performance_impact: float
    fatigue_indicators: List[str]
    optimization_suggestions: List[str]
    
    def __post_init__(self):
        if self.fatigue_indicators is None:
            self.fatigue_indicators = []
        if self.optimization_suggestions is None:
            self.optimization_suggestions = []

class MemorySystemAnalyzer:
    """Analyzes memory system patterns and performance"""
    
    def __init__(self):
        self.memory_stores = {memory_type: [] for memory_type in MemoryType}
        self.memory_network = {}  # Associative connections
        self.consolidation_queue = deque()
        self.forgetting_curve_params = {}
    
    def add_memory_item(self, memory_item: MemoryItem):
        """Add new memory item to the system"""
        self.memory_stores[memory_item.memory_type].append(memory_item)
        self._update_memory_network(memory_item)
        
        # Queue for consolidation if needed
        if memory_item.consolidation_status == "unconsolidated":
            self.consolidation_queue.append(memory_item.memory_id)
    
    def _update_memory_network(self, memory_item: MemoryItem):
        """Update associative memory network"""
        if memory_item.memory_id not in self.memory_network:
            self.memory_network[memory_item.memory_id] = set()
        
        # Create associations based on concepts
        for concept in memory_item.associated_concepts:
            for other_memory_id, other_connections in self.memory_network.items():
                if other_memory_id != memory_item.memory_id:
                    # Check for concept overlap
                    other_memory = self._find_memory_by_id(other_memory_id)
                    if other_memory and concept in other_memory.associated_concepts:
                        self.memory_network[memory_item.memory_id].add(other_memory_id)
                        self.memory_network[other_memory_id].add(memory_item.memory_id)
    
    def _find_memory_by_id(self, memory_id: str) -> Optional[MemoryItem]:
        """Find memory item by ID"""
        for memory_type, memories in self.memory_stores.items():
            for memory in memories:
                if memory.memory_id == memory_id:
                    return memory
        return None
    
    def analyze_memory_patterns(self) -> Dict[str, Any]:
        """Analyze memory system patterns"""
        
        analysis = {
            "memory_distribution": {},
            "memory_strength_analysis": {},
            "access_patterns": {},
            "consolidation_status": {},
            "memory_network_analysis": {},
            "forgetting_analysis": {}
        }
        
        # Memory distribution by type
        for memory_type, memories in self.memory_stores.items():
            analysis["memory_distribution"][memory_type.value] = len(memories)
        
        # Memory strength analysis
        all_memories = []
        for memories in self.memory_stores.values():
            all_memories.extend(memories)
        
        if all_memories:
            strengths = [mem.strength for mem in all_memories]
            analysis["memory_strength_analysis"] = {
                "average_strength": np.mean(strengths),
                "strength_std": np.std(strengths),
                "strong_memories": len([s for s in strengths if s > 0.8]),
                "weak_memories": len([s for s in strengths if s < 0.3])
            }
            
            # Access patterns
            access_counts = [mem.access_count for mem in all_memories]
            analysis["access_patterns"] = {
                "total_accesses": sum(access_counts),
                "average_accesses": np.mean(access_counts),
                "most_accessed": max(access_counts) if access_counts else 0,
                "least_accessed": min(access_counts) if access_counts else 0
            }
            
            # Consolidation status
            consolidation_counts = defaultdict(int)
            for memory in all_memories:
                consolidation_counts[memory.consolidation_status] += 1
            analysis["consolidation_status"] = dict(consolidation_counts)
        
        # Memory network analysis
        if self.memory_network:
            connection_counts = [len(connections) for connections in self.memory_network.values()]
            analysis["memory_network_analysis"] = {
                "total_connections": sum(connection_counts),
                "average_connections": np.mean(connection_counts),
                "most_connected_memory": max(connection_counts) if connection_counts else 0,
                "network_density": self._calculate_network_density()
            }
        
        return analysis
    
    def _calculate_network_density(self) -> float:
        """Calculate memory network density"""
        if len(self.memory_network) < 2:
            return 0.0
        
        actual_connections = sum(len(connections) for connections in self.memory_network.values()) // 2
        max_connections = len(self.memory_network) * (len(self.memory_network) - 1) // 2
        
        return actual_connections / max_connections if max_connections > 0 else 0.0
    
    def get_memory_visualization_data(self) -> Dict[str, Any]:
        """Get data for memory visualization"""
        
        # Create nodes for memories
        nodes = []
        for memory_type, memories in self.memory_stores.items():
            for memory in memories:
                node = {
                    "id": memory.memory_id,
                    "type": memory_type.value,
                    "strength": memory.strength,
                    "importance": memory.importance_score,
                    "access_count": memory.access_count,
                    "age_days": (datetime.utcnow() - memory.created_at).days,
                    "consolidation": memory.consolidation_status,
                    "concepts": memory.associated_concepts,
                    "size": memory.strength * 20 + 5,  # Visual size
                    "color": self._get_memory_color(memory_type, memory.strength)
                }
                nodes.append(node)
        
        # Create links for associations
        links = []
        for memory_id, connections in self.memory_network.items():
            for connected_id in connections:
                if memory_id < connected_id:  # Avoid duplicates
                    link = {
                        "source": memory_id,
                        "target": connected_id,
                        "strength": self._calculate_association_strength(memory_id, connected_id)
                    }
                    links.append(link)
        
        return {
            "nodes": nodes,
            "links": links,
            "layout_config": {
                "type": "force_directed",
                "cluster_by": "type",
                "strength_factor": 0.8
            }
        }
    
    def _get_memory_color(self, memory_type: MemoryType, strength: float) -> str:
        """Get color for memory visualization"""
        base_colors = {
            MemoryType.WORKING: "#FF5722",      # Deep Orange
            MemoryType.SHORT_TERM: "#FF9800",   # Orange
            MemoryType.LONG_TERM: "#4CAF50",    # Green
            MemoryType.EPISODIC: "#2196F3",     # Blue
            MemoryType.SEMANTIC: "#9C27B0",     # Purple
            MemoryType.PROCEDURAL: "#607D8B",   # Blue Grey
            MemoryType.METACOGNITIVE: "#795548"  # Brown
        }
        
        base_color = base_colors.get(memory_type, "#9E9E9E")
        
        # Adjust opacity based on strength
        opacity = 0.3 + (strength * 0.7)  # 0.3 to 1.0
        
        return base_color  # In a real implementation, would adjust opacity
    
    def _calculate_association_strength(self, memory_id1: str, memory_id2: str) -> float:
        """Calculate association strength between two memories"""
        memory1 = self._find_memory_by_id(memory_id1)
        memory2 = self._find_memory_by_id(memory_id2)
        
        if not memory1 or not memory2:
            return 0.0
        
        # Calculate based on concept overlap and access patterns
        concept_overlap = len(set(memory1.associated_concepts) & set(memory2.associated_concepts))
        max_concepts = max(len(memory1.associated_concepts), len(memory2.associated_concepts))
        
        concept_similarity = concept_overlap / max_concepts if max_concepts > 0 else 0.0
        
        # Time-based association (memories accessed around the same time)
        time_diff = abs((memory1.last_accessed - memory2.last_accessed).total_seconds())
        time_factor = math.exp(-time_diff / 3600)  # Decay over hours
        
        return (concept_similarity * 0.7 + time_factor * 0.3)

class AttentionAnalyzer:
    """Analyzes attention patterns and focus dynamics"""
    
    def __init__(self):
        self.attention_history = []
        self.focus_switches = []
        self.distraction_events = []
        self.attention_capacity = 1.0  # Normalized capacity
    
    def track_attention_focus(self, attention_focus: AttentionFocus):
        """Track attention focus event"""
        self.attention_history.append(attention_focus)
        
        # Detect focus switches
        if len(self.attention_history) > 1:
            prev_focus = self.attention_history[-2]
            if prev_focus.target_object != attention_focus.target_object:
                switch_event = {
                    "timestamp": attention_focus.start_time,
                    "from_target": prev_focus.target_object,
                    "to_target": attention_focus.target_object,
                    "switch_time": (attention_focus.start_time - prev_focus.end_time).total_seconds() if prev_focus.end_time else 0
                }
                self.focus_switches.append(switch_event)
    
    def analyze_attention_patterns(self) -> Dict[str, Any]:
        """Analyze attention patterns"""
        
        if not self.attention_history:
            return {"error": "No attention data available"}
        
        analysis = {
            "attention_metrics": {},
            "focus_patterns": {},
            "distraction_analysis": {},
            "attention_efficiency": {},
            "temporal_patterns": {}
        }
        
        # Attention metrics
        total_duration = sum(
            (focus.end_time - focus.start_time).total_seconds() if focus.end_time else 0
            for focus in self.attention_history
        )
        
        intensities = [focus.intensity for focus in self.attention_history]
        analysis["attention_metrics"] = {
            "total_focus_time": total_duration,
            "average_intensity": np.mean(intensities),
            "max_intensity": max(intensities),
            "focus_sessions": len(self.attention_history),
            "total_switches": len(self.focus_switches)
        }
        
        # Focus patterns by type
        type_distribution = defaultdict(list)
        for focus in self.attention_history:
            type_distribution[focus.attention_type.value].append(focus.intensity)
        
        analysis["focus_patterns"] = {
            attention_type: {
                "count": len(intensities),
                "average_intensity": np.mean(intensities),
                "total_time": sum(
                    (f.end_time - f.start_time).total_seconds() if f.end_time else 0
                    for f in self.attention_history
                    if f.attention_type.value == attention_type
                )
            }
            for attention_type, intensities in type_distribution.items()
        }
        
        # Distraction analysis
        distraction_counts = defaultdict(int)
        for focus in self.attention_history:
            for distractor in focus.distractors:
                distraction_counts[distractor] += 1
        
        analysis["distraction_analysis"] = {
            "total_distractions": sum(distraction_counts.values()),
            "unique_distractors": len(distraction_counts),
            "most_common_distractors": sorted(
                distraction_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }
        
        # Attention efficiency
        performance_impacts = [focus.performance_impact for focus in self.attention_history]
        positive_impacts = [p for p in performance_impacts if p > 0]
        negative_impacts = [p for p in performance_impacts if p < 0]
        
        analysis["attention_efficiency"] = {
            "overall_performance_impact": np.mean(performance_impacts),
            "positive_focus_sessions": len(positive_impacts),
            "negative_focus_sessions": len(negative_impacts),
            "efficiency_score": len(positive_impacts) / max(len(performance_impacts), 1)
        }
        
        # Temporal patterns (hourly distribution)
        hourly_focus = defaultdict(list)
        for focus in self.attention_history:
            hour = focus.start_time.hour
            hourly_focus[hour].append(focus.intensity)
        
        analysis["temporal_patterns"] = {
            "peak_hours": sorted(
                [(hour, np.mean(intensities)) for hour, intensities in hourly_focus.items()],
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "hourly_distribution": {
                hour: {
                    "session_count": len(intensities),
                    "average_intensity": np.mean(intensities)
                }
                for hour, intensities in hourly_focus.items()
            }
        }
        
        return analysis
    
    def get_attention_heatmap_data(self) -> Dict[str, Any]:
        """Get attention heatmap data for visualization"""
        
        # Create hourly heatmap data
        heatmap_data = {}
        
        for focus in self.attention_history:
            hour = focus.start_time.hour
            day = focus.start_time.strftime("%Y-%m-%d")
            
            if day not in heatmap_data:
                heatmap_data[day] = {h: 0 for h in range(24)}
            
            heatmap_data[day][hour] += focus.intensity
        
        # Normalize data
        max_value = max(
            max(day_data.values()) for day_data in heatmap_data.values()
        ) if heatmap_data else 1
        
        normalized_data = {}
        for day, day_data in heatmap_data.items():
            normalized_data[day] = {
                hour: value / max_value for hour, value in day_data.items()
            }
        
        return {
            "heatmap_data": normalized_data,
            "max_intensity": max_value,
            "time_range": {
                "start": min(focus.start_time for focus in self.attention_history).strftime("%Y-%m-%d") if self.attention_history else None,
                "end": max(focus.start_time for focus in self.attention_history).strftime("%Y-%m-%d") if self.attention_history else None
            }
        }

class LearningProgressAnalyzer:
    """Analyzes learning progression and patterns"""
    
    def __init__(self):
        self.learning_events = []
        self.knowledge_domains = {}
        self.learning_curves = {}
        self.mastery_thresholds = {}
    
    def track_learning_event(self, learning_event: LearningEvent):
        """Track learning event"""
        self.learning_events.append(learning_event)
        
        # Update knowledge domain tracking
        content = learning_event.learning_content
        if content not in self.knowledge_domains:
            self.knowledge_domains[content] = []
        
        self.knowledge_domains[content].append({
            "timestamp": learning_event.timestamp,
            "knowledge_level": learning_event.post_knowledge_level,
            "learning_efficiency": learning_event.learning_efficiency
        })
    
    def analyze_learning_progression(self) -> Dict[str, Any]:
        """Analyze learning progression"""
        
        if not self.learning_events:
            return {"error": "No learning data available"}
        
        analysis = {
            "overall_progress": {},
            "learning_efficiency": {},
            "domain_analysis": {},
            "learning_patterns": {},
            "mastery_analysis": {}
        }
        
        # Overall progress
        pre_levels = [event.pre_knowledge_level for event in self.learning_events]
        post_levels = [event.post_knowledge_level for event in self.learning_events]
        efficiencies = [event.learning_efficiency for event in self.learning_events]
        
        analysis["overall_progress"] = {
            "total_learning_events": len(self.learning_events),
            "average_pre_level": np.mean(pre_levels),
            "average_post_level": np.mean(post_levels),
            "average_improvement": np.mean([post - pre for pre, post in zip(pre_levels, post_levels)]),
            "total_learning_time": sum(event.duration for event in self.learning_events)
        }
        
        # Learning efficiency
        analysis["learning_efficiency"] = {
            "average_efficiency": np.mean(efficiencies),
            "efficiency_trend": self._calculate_efficiency_trend(),
            "high_efficiency_sessions": len([e for e in efficiencies if e > 0.8]),
            "low_efficiency_sessions": len([e for e in efficiencies if e < 0.4])
        }
        
        # Domain analysis
        domain_stats = {}
        for domain, progress_list in self.knowledge_domains.items():
            if progress_list:
                levels = [p["knowledge_level"] for p in progress_list]
                efficiencies = [p["learning_efficiency"] for p in progress_list]
                
                domain_stats[domain] = {
                    "current_level": levels[-1],
                    "progress_rate": (levels[-1] - levels[0]) / max(len(levels), 1),
                    "average_efficiency": np.mean(efficiencies),
                    "learning_sessions": len(progress_list),
                    "mastery_status": "mastered" if levels[-1] > 0.9 else "learning"
                }
        
        analysis["domain_analysis"] = domain_stats
        
        # Learning patterns
        learning_types = defaultdict(list)
        for event in self.learning_events:
            learning_types[event.learning_type].append(event.learning_efficiency)
        
        analysis["learning_patterns"] = {
            "type_distribution": {
                learning_type: {
                    "count": len(efficiencies),
                    "average_efficiency": np.mean(efficiencies)
                }
                for learning_type, efficiencies in learning_types.items()
            },
            "most_effective_type": max(
                learning_types.items(), 
                key=lambda x: np.mean(x[1])
            )[0] if learning_types else None
        }
        
        # Mastery analysis
        mastered_domains = [
            domain for domain, stats in domain_stats.items()
            if stats["mastery_status"] == "mastered"
        ]
        
        analysis["mastery_analysis"] = {
            "mastered_domains": len(mastered_domains),
            "total_domains": len(domain_stats),
            "mastery_rate": len(mastered_domains) / max(len(domain_stats), 1),
            "domains_near_mastery": [
                domain for domain, stats in domain_stats.items()
                if 0.8 <= stats["current_level"] < 0.9
            ]
        }
        
        return analysis
    
    def _calculate_efficiency_trend(self) -> str:
        """Calculate learning efficiency trend"""
        if len(self.learning_events) < 5:
            return "insufficient_data"
        
        # Compare recent efficiency with earlier efficiency
        recent_events = self.learning_events[-5:]
        early_events = self.learning_events[:5]
        
        recent_efficiency = np.mean([e.learning_efficiency for e in recent_events])
        early_efficiency = np.mean([e.learning_efficiency for e in early_events])
        
        if recent_efficiency > early_efficiency * 1.1:
            return "improving"
        elif recent_efficiency < early_efficiency * 0.9:
            return "declining"
        else:
            return "stable"
    
    def get_learning_curve_data(self) -> Dict[str, Any]:
        """Get learning curve visualization data"""
        
        curves = {}
        
        for domain, progress_list in self.knowledge_domains.items():
            if len(progress_list) > 1:
                timestamps = [p["timestamp"] for p in progress_list]
                levels = [p["knowledge_level"] for p in progress_list]
                
                # Create time series data
                curve_data = []
                for i, (timestamp, level) in enumerate(zip(timestamps, levels)):
                    curve_data.append({
                        "x": timestamp.isoformat(),
                        "y": level,
                        "session": i + 1
                    })
                
                curves[domain] = {
                    "data": curve_data,
                    "start_level": levels[0],
                    "current_level": levels[-1],
                    "improvement": levels[-1] - levels[0],
                    "sessions": len(levels)
                }
        
        return {
            "learning_curves": curves,
            "summary": {
                "total_domains": len(curves),
                "average_improvement": np.mean([
                    curve["improvement"] for curve in curves.values()
                ]) if curves else 0
            }
        }

class DecisionAnalyzer:
    """Analyzes decision-making processes and patterns"""
    
    def __init__(self):
        self.decision_history = []
        self.decision_outcomes = {}
        self.decision_patterns = {}
    
    def track_decision_event(self, decision_event: DecisionEvent):
        """Track decision-making event"""
        self.decision_history.append(decision_event)
        
        # Update outcome tracking when available
        if decision_event.actual_outcome:
            self.decision_outcomes[decision_event.decision_id] = {
                "predicted": decision_event.outcome_prediction,
                "actual": decision_event.actual_outcome,
                "confidence": decision_event.confidence_level
            }
    
    def analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision-making patterns"""
        
        if not self.decision_history:
            return {"error": "No decision data available"}
        
        analysis = {
            "decision_metrics": {},
            "decision_types": {},
            "confidence_analysis": {},
            "outcome_analysis": {},
            "decision_quality": {},
            "temporal_patterns": {}
        }
        
        # Decision metrics
        decision_times = [d.decision_time for d in self.decision_history]
        confidence_levels = [d.confidence_level for d in self.decision_history]
        
        analysis["decision_metrics"] = {
            "total_decisions": len(self.decision_history),
            "average_decision_time": np.mean(decision_times),
            "fastest_decision": min(decision_times),
            "slowest_decision": max(decision_times),
            "average_confidence": np.mean(confidence_levels)
        }
        
        # Decision types analysis
        type_distribution = defaultdict(list)
        for decision in self.decision_history:
            type_distribution[decision.decision_type.value].append({
                "confidence": decision.confidence_level,
                "time": decision.decision_time,
                "options": len(decision.options_considered)
            })
        
        analysis["decision_types"] = {
            decision_type: {
                "count": len(decisions),
                "average_confidence": np.mean([d["confidence"] for d in decisions]),
                "average_time": np.mean([d["time"] for d in decisions]),
                "average_options": np.mean([d["options"] for d in decisions])
            }
            for decision_type, decisions in type_distribution.items()
        }
        
        # Confidence analysis
        high_confidence = [d for d in self.decision_history if d.confidence_level > 0.8]
        low_confidence = [d for d in self.decision_history if d.confidence_level < 0.4]
        
        analysis["confidence_analysis"] = {
            "high_confidence_decisions": len(high_confidence),
            "low_confidence_decisions": len(low_confidence),
            "confidence_distribution": self._calculate_confidence_distribution(),
            "confidence_vs_time_correlation": self._calculate_confidence_time_correlation()
        }
        
        # Outcome analysis
        if self.decision_outcomes:
            correct_predictions = 0
            total_with_outcomes = len(self.decision_outcomes)
            
            for outcome_data in self.decision_outcomes.values():
                if outcome_data["predicted"] == outcome_data["actual"]:
                    correct_predictions += 1
            
            analysis["outcome_analysis"] = {
                "prediction_accuracy": correct_predictions / total_with_outcomes,
                "total_outcomes_tracked": total_with_outcomes,
                "correct_predictions": correct_predictions,
                "overconfidence_instances": self._calculate_overconfidence_instances()
            }
        
        # Decision quality (based on various factors)
        quality_scores = []
        for decision in self.decision_history:
            if decision.decision_quality_score:
                quality_scores.append(decision.decision_quality_score)
        
        if quality_scores:
            analysis["decision_quality"] = {
                "average_quality": np.mean(quality_scores),
                "quality_trend": self._calculate_quality_trend(quality_scores),
                "high_quality_decisions": len([q for q in quality_scores if q > 0.8]),
                "low_quality_decisions": len([q for q in quality_scores if q < 0.4])
            }
        
        return analysis
    
    def _calculate_confidence_distribution(self) -> Dict[str, int]:
        """Calculate confidence level distribution"""
        bins = {"very_low": 0, "low": 0, "medium": 0, "high": 0, "very_high": 0}
        
        for decision in self.decision_history:
            conf = decision.confidence_level
            if conf < 0.2:
                bins["very_low"] += 1
            elif conf < 0.4:
                bins["low"] += 1
            elif conf < 0.6:
                bins["medium"] += 1
            elif conf < 0.8:
                bins["high"] += 1
            else:
                bins["very_high"] += 1
        
        return bins
    
    def _calculate_confidence_time_correlation(self) -> float:
        """Calculate correlation between confidence and decision time"""
        if len(self.decision_history) < 3:
            return 0.0
        
        confidences = [d.confidence_level for d in self.decision_history]
        times = [d.decision_time for d in self.decision_history]
        
        return np.corrcoef(confidences, times)[0, 1] if len(confidences) > 1 else 0.0
    
    def _calculate_overconfidence_instances(self) -> int:
        """Calculate instances of overconfidence"""
        overconfident = 0
        
        for outcome_data in self.decision_outcomes.values():
            # High confidence but wrong prediction
            if (outcome_data["confidence"] > 0.8 and 
                outcome_data["predicted"] != outcome_data["actual"]):
                overconfident += 1
        
        return overconfident
    
    def _calculate_quality_trend(self, quality_scores: List[float]) -> str:
        """Calculate decision quality trend"""
        if len(quality_scores) < 5:
            return "insufficient_data"
        
        # Compare recent vs. early quality
        recent_quality = np.mean(quality_scores[-5:])
        early_quality = np.mean(quality_scores[:5])
        
        if recent_quality > early_quality * 1.1:
            return "improving"
        elif recent_quality < early_quality * 0.9:
            return "declining"
        else:
            return "stable"

class CognitiveLoadMonitor:
    """Monitors and analyzes cognitive load"""
    
    def __init__(self):
        self.load_history = []
        self.load_thresholds = {
            "optimal": 0.7,
            "moderate": 0.8,
            "high": 0.9,
            "overload": 1.0
        }
    
    def track_cognitive_load(self, cognitive_load: CognitiveLoad):
        """Track cognitive load measurement"""
        self.load_history.append(cognitive_load)
    
    def analyze_cognitive_load(self) -> Dict[str, Any]:
        """Analyze cognitive load patterns"""
        
        if not self.load_history:
            return {"error": "No cognitive load data available"}
        
        analysis = {
            "load_metrics": {},
            "load_distribution": {},
            "performance_correlation": {},
            "overload_analysis": {},
            "optimization_insights": {}
        }
        
        # Load metrics
        overall_loads = [load.overall_load for load in self.load_history]
        working_memory_loads = [load.working_memory_load for load in self.load_history]
        attention_demands = [load.attention_demand for load in self.load_history]
        emotional_loads = [load.emotional_load for load in self.load_history]
        
        analysis["load_metrics"] = {
            "average_overall_load": np.mean(overall_loads),
            "max_load": max(overall_loads),
            "min_load": min(overall_loads),
            "load_variability": np.std(overall_loads),
            "average_working_memory_load": np.mean(working_memory_loads),
            "average_attention_demand": np.mean(attention_demands),
            "average_emotional_load": np.mean(emotional_loads)
        }
        
        # Load distribution
        load_categories = {"optimal": 0, "moderate": 0, "high": 0, "overload": 0}
        
        for load in overall_loads:
            if load <= self.load_thresholds["optimal"]:
                load_categories["optimal"] += 1
            elif load <= self.load_thresholds["moderate"]:
                load_categories["moderate"] += 1
            elif load <= self.load_thresholds["high"]:
                load_categories["high"] += 1
            else:
                load_categories["overload"] += 1
        
        analysis["load_distribution"] = load_categories
        
        # Performance correlation
        performance_impacts = [load.performance_impact for load in self.load_history]
        load_performance_correlation = np.corrcoef(overall_loads, performance_impacts)[0, 1] if len(overall_loads) > 1 else 0.0
        
        analysis["performance_correlation"] = {
            "load_performance_correlation": load_performance_correlation,
            "optimal_performance_load": self._find_optimal_performance_load(),
            "average_performance_impact": np.mean(performance_impacts)
        }
        
        # Overload analysis
        overload_instances = [load for load in self.load_history if load.overall_load > self.load_thresholds["high"]]
        
        analysis["overload_analysis"] = {
            "overload_frequency": len(overload_instances),
            "overload_percentage": len(overload_instances) / len(self.load_history) * 100,
            "common_overload_causes": self._analyze_overload_causes(overload_instances),
            "average_overload_duration": self._calculate_average_overload_duration()
        }
        
        # Optimization insights
        all_suggestions = []
        for load in self.load_history:
            all_suggestions.extend(load.optimization_suggestions)
        
        suggestion_counts = defaultdict(int)
        for suggestion in all_suggestions:
            suggestion_counts[suggestion] += 1
        
        analysis["optimization_insights"] = {
            "most_common_suggestions": sorted(
                suggestion_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "total_suggestions": len(all_suggestions),
            "unique_suggestions": len(suggestion_counts)
        }
        
        return analysis
    
    def _find_optimal_performance_load(self) -> float:
        """Find the load level that correlates with best performance"""
        if len(self.load_history) < 5:
            return 0.7  # Default optimal load
        
        # Find load level with highest average performance impact
        load_performance_pairs = [
            (load.overall_load, load.performance_impact) 
            for load in self.load_history
        ]
        
        # Group by load ranges and find average performance
        load_ranges = np.arange(0, 1.1, 0.1)
        best_load = 0.7
        best_performance = -1
        
        for i in range(len(load_ranges) - 1):
            range_performances = [
                perf for load, perf in load_performance_pairs
                if load_ranges[i] <= load < load_ranges[i + 1]
            ]
            
            if range_performances:
                avg_performance = np.mean(range_performances)
                if avg_performance > best_performance:
                    best_performance = avg_performance
                    best_load = (load_ranges[i] + load_ranges[i + 1]) / 2
        
        return best_load
    
    def _analyze_overload_causes(self, overload_instances: List[CognitiveLoad]) -> List[str]:
        """Analyze common causes of cognitive overload"""
        all_fatigue_indicators = []
        for load in overload_instances:
            all_fatigue_indicators.extend(load.fatigue_indicators)
        
        cause_counts = defaultdict(int)
        for cause in all_fatigue_indicators:
            cause_counts[cause] += 1
        
        return sorted(cause_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _calculate_average_overload_duration(self) -> float:
        """Calculate average duration of overload periods"""
        # This would require temporal analysis of consecutive overload instances
        # Simplified for demonstration
        return 15.0  # Average 15 minutes

class CognitiveInsightsDashboard:
    """Main dashboard for cognitive insights"""
    
    def __init__(self):
        self.memory_analyzer = MemorySystemAnalyzer()
        self.attention_analyzer = AttentionAnalyzer()
        self.learning_analyzer = LearningProgressAnalyzer()
        self.decision_analyzer = DecisionAnalyzer()
        self.load_monitor = CognitiveLoadMonitor()
        
        self.current_cognitive_state = CognitiveState.OPTIMAL
        self.insights_history = []
        self.recommendations = []
    
    async def update_cognitive_data(
        self,
        memory_items: List[MemoryItem] = None,
        attention_focuses: List[AttentionFocus] = None,
        learning_events: List[LearningEvent] = None,
        decision_events: List[DecisionEvent] = None,
        cognitive_loads: List[CognitiveLoad] = None
    ):
        """Update cognitive dashboard with new data"""
        
        # Update memory system
        if memory_items:
            for memory_item in memory_items:
                self.memory_analyzer.add_memory_item(memory_item)
        
        # Update attention tracking
        if attention_focuses:
            for attention_focus in attention_focuses:
                self.attention_analyzer.track_attention_focus(attention_focus)
        
        # Update learning tracking  
        if learning_events:
            for learning_event in learning_events:
                self.learning_analyzer.track_learning_event(learning_event)
        
        # Update decision tracking
        if decision_events:
            for decision_event in decision_events:
                self.decision_analyzer.track_decision_event(decision_event)
        
        # Update cognitive load monitoring
        if cognitive_loads:
            for cognitive_load in cognitive_loads:
                self.load_monitor.track_cognitive_load(cognitive_load)
        
        # Update cognitive state assessment
        await self._assess_current_cognitive_state()
        
        # Generate new insights and recommendations
        await self._generate_insights_and_recommendations()
    
    async def get_comprehensive_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive cognitive insights dashboard"""
        
        dashboard = {
            "overview": await self._get_cognitive_overview(),
            "memory_analysis": self.memory_analyzer.analyze_memory_patterns(),
            "attention_analysis": self.attention_analyzer.analyze_attention_patterns(),
            "learning_analysis": self.learning_analyzer.analyze_learning_progression(),
            "decision_analysis": self.decision_analyzer.analyze_decision_patterns(),
            "cognitive_load_analysis": self.load_monitor.analyze_cognitive_load(),
            "visualizations": await self._get_visualization_data(),
            "insights": self.insights_history[-10:],  # Last 10 insights
            "recommendations": self.recommendations,
            "current_state": self.current_cognitive_state.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return dashboard
    
    async def _get_cognitive_overview(self) -> Dict[str, Any]:
        """Get cognitive system overview"""
        
        return {
            "cognitive_state": self.current_cognitive_state.value,
            "memory_system_health": self._calculate_memory_health(),
            "attention_efficiency": self._calculate_attention_efficiency(),
            "learning_velocity": self._calculate_learning_velocity(),
            "decision_quality": self._calculate_decision_quality(),
            "cognitive_load_status": self._get_current_load_status(),
            "overall_performance_score": self._calculate_overall_performance()
        }
    
    def _calculate_memory_health(self) -> float:
        """Calculate memory system health score"""
        analysis = self.memory_analyzer.analyze_memory_patterns()
        
        if "memory_strength_analysis" not in analysis:
            return 0.5
        
        strength_data = analysis["memory_strength_analysis"]
        avg_strength = strength_data.get("average_strength", 0.5)
        strong_ratio = strength_data.get("strong_memories", 0) / max(
            strength_data.get("strong_memories", 0) + strength_data.get("weak_memories", 1), 1
        )
        
        return (avg_strength * 0.6 + strong_ratio * 0.4)
    
    def _calculate_attention_efficiency(self) -> float:
        """Calculate attention efficiency score"""
        analysis = self.attention_analyzer.analyze_attention_patterns()
        
        if "attention_efficiency" not in analysis:
            return 0.5
        
        return analysis["attention_efficiency"].get("efficiency_score", 0.5)
    
    def _calculate_learning_velocity(self) -> float:
        """Calculate learning velocity score"""
        analysis = self.learning_analyzer.analyze_learning_progression()
        
        if "learning_efficiency" not in analysis:
            return 0.5
        
        return analysis["learning_efficiency"].get("average_efficiency", 0.5)
    
    def _calculate_decision_quality(self) -> float:
        """Calculate decision quality score"""
        analysis = self.decision_analyzer.analyze_decision_patterns()
        
        if "decision_quality" not in analysis:
            return 0.5
        
        return analysis["decision_quality"].get("average_quality", 0.5)
    
    def _get_current_load_status(self) -> str:
        """Get current cognitive load status"""
        if not self.load_monitor.load_history:
            return "unknown"
        
        latest_load = self.load_monitor.load_history[-1].overall_load
        
        if latest_load <= 0.7:
            return "optimal"
        elif latest_load <= 0.8:
            return "moderate"
        elif latest_load <= 0.9:
            return "high"
        else:
            return "overloaded"
    
    def _calculate_overall_performance(self) -> float:
        """Calculate overall cognitive performance score"""
        scores = [
            self._calculate_memory_health(),
            self._calculate_attention_efficiency(),
            self._calculate_learning_velocity(),
            self._calculate_decision_quality()
        ]
        
        return np.mean(scores)
    
    async def _assess_current_cognitive_state(self):
        """Assess current cognitive state"""
        
        performance_score = self._calculate_overall_performance()
        load_status = self._get_current_load_status()
        
        # Determine cognitive state based on performance and load
        if performance_score > 0.8 and load_status in ["optimal", "moderate"]:
            self.current_cognitive_state = CognitiveState.OPTIMAL
        elif load_status == "high":
            self.current_cognitive_state = CognitiveState.HIGH_LOAD
        elif load_status == "overloaded":
            self.current_cognitive_state = CognitiveState.OVERLOADED
        elif performance_score < 0.4:
            self.current_cognitive_state = CognitiveState.FATIGUED
        else:
            self.current_cognitive_state = CognitiveState.MODERATE_LOAD
    
    async def _generate_insights_and_recommendations(self):
        """Generate cognitive insights and recommendations"""
        
        insights = []
        recommendations = []
        
        # Memory insights
        memory_analysis = self.memory_analyzer.analyze_memory_patterns()
        if "memory_strength_analysis" in memory_analysis:
            strength_data = memory_analysis["memory_strength_analysis"]
            if strength_data.get("weak_memories", 0) > strength_data.get("strong_memories", 0):
                insights.append({
                    "type": "memory",
                    "insight": "Memory consolidation may need attention - more weak memories than strong ones",
                    "timestamp": datetime.utcnow().isoformat()
                })
                recommendations.append("Consider memory consolidation exercises and spaced repetition")
        
        # Attention insights
        attention_analysis = self.attention_analyzer.analyze_attention_patterns()
        if "distraction_analysis" in attention_analysis:
            distraction_data = attention_analysis["distraction_analysis"]
            if distraction_data.get("total_distractions", 0) > 10:
                insights.append({
                    "type": "attention",
                    "insight": f"High distraction count detected: {distraction_data['total_distractions']} distractions",
                    "timestamp": datetime.utcnow().isoformat()
                })
                recommendations.append("Implement distraction management strategies")
        
        # Learning insights
        learning_analysis = self.learning_analyzer.analyze_learning_progression()
        if "learning_efficiency" in learning_analysis:
            efficiency_data = learning_analysis["learning_efficiency"]
            if efficiency_data.get("efficiency_trend") == "declining":
                insights.append({
                    "type": "learning",
                    "insight": "Learning efficiency shows declining trend",
                    "timestamp": datetime.utcnow().isoformat()
                })
                recommendations.append("Review learning strategies and consider rest periods")
        
        # Update history
        self.insights_history.extend(insights)
        self.recommendations = recommendations[:10]  # Keep top 10 recommendations
    
    async def _get_visualization_data(self) -> Dict[str, Any]:
        """Get data for cognitive visualizations"""
        
        return {
            "memory_network": self.memory_analyzer.get_memory_visualization_data(),
            "attention_heatmap": self.attention_analyzer.get_attention_heatmap_data(),
            "learning_curves": self.learning_analyzer.get_learning_curve_data(),
            "cognitive_load_timeline": self._get_load_timeline_data()
        }
    
    def _get_load_timeline_data(self) -> Dict[str, Any]:
        """Get cognitive load timeline data"""
        
        if not self.load_monitor.load_history:
            return {"data": [], "summary": {}}
        
        timeline_data = []
        for load in self.load_monitor.load_history:
            timeline_data.append({
                "timestamp": load.timestamp.isoformat(),
                "overall_load": load.overall_load,
                "working_memory": load.working_memory_load,
                "attention_demand": load.attention_demand,
                "emotional_load": load.emotional_load,
                "performance_impact": load.performance_impact
            })
        
        return {
            "data": timeline_data,
            "summary": {
                "average_load": np.mean([d["overall_load"] for d in timeline_data]),
                "peak_load": max([d["overall_load"] for d in timeline_data]),
                "data_points": len(timeline_data)
            }
        }

# Utility functions for creating sample data
def create_sample_cognitive_data():
    """Create sample cognitive data for testing"""
    
    # Sample memory items
    memory_items = [
        MemoryItem(
            memory_id=f"mem_{i}",
            content={"topic": f"Topic {i}", "details": f"Details about topic {i}"},
            memory_type=np.random.choice(list(MemoryType)),
            strength=np.random.uniform(0.3, 1.0),
            access_count=np.random.randint(1, 20),
            last_accessed=datetime.utcnow() - timedelta(hours=np.random.randint(1, 72)),
            created_at=datetime.utcnow() - timedelta(days=np.random.randint(1, 30)),
            associated_concepts=[f"concept_{j}" for j in range(np.random.randint(1, 5))],
            emotional_valence=np.random.uniform(-1, 1),
            importance_score=np.random.uniform(0.2, 1.0),
            decay_rate=np.random.uniform(0.01, 0.1),
            consolidation_status=np.random.choice(["unconsolidated", "consolidating", "consolidated"])
        )
        for i in range(20)
    ]
    
    # Sample attention focuses
    attention_focuses = [
        AttentionFocus(
            focus_id=f"att_{i}",
            target_object=f"target_{i}",
            attention_type=np.random.choice(list(AttentionType)),
            intensity=np.random.uniform(0.3, 1.0),
            duration=np.random.uniform(30, 300),  # 30 seconds to 5 minutes
            start_time=datetime.utcnow() - timedelta(minutes=np.random.randint(0, 1440)),
            end_time=datetime.utcnow() - timedelta(minutes=np.random.randint(0, 720)),
            context={"task": f"task_{i}", "environment": "office"},
            distractors=[f"distractor_{j}" for j in range(np.random.randint(0, 3))],
            performance_impact=np.random.uniform(-0.5, 1.0)
        )
        for i in range(30)
    ]
    
    # Sample learning events
    learning_events = [
        LearningEvent(
            event_id=f"learn_{i}",
            learning_content=f"Content {i}",
            learning_type=np.random.choice(["acquisition", "refinement", "adaptation", "correction"]),
            pre_knowledge_level=np.random.uniform(0.1, 0.7),
            post_knowledge_level=np.random.uniform(0.3, 1.0),
            learning_efficiency=np.random.uniform(0.3, 1.0),
            timestamp=datetime.utcnow() - timedelta(hours=np.random.randint(1, 168)),
            duration=np.random.uniform(10, 120),  # 10 minutes to 2 hours
            cognitive_load=np.random.uniform(0.3, 0.9),
            success_indicators=["indicator_1", "indicator_2"],
            failure_indicators=[]
        )
        for i in range(15)
    ]
    
    return {
        "memory_items": memory_items,
        "attention_focuses": attention_focuses,
        "learning_events": learning_events
    }