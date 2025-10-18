"""
CollegiumAI Cognitive Architecture - Attention Mechanism
Advanced attention system with selective focus, task switching, and cognitive load management
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import uuid
import json
from collections import deque

class AttentionType(Enum):
    """Types of attention"""
    SELECTIVE = "selective"      # Focus on specific stimuli
    DIVIDED = "divided"          # Attention to multiple tasks
    SUSTAINED = "sustained"      # Prolonged attention on one task
    EXECUTIVE = "executive"      # Control and coordination of attention
    SPATIAL = "spatial"          # Attention to spatial locations
    TEMPORAL = "temporal"        # Attention to temporal sequences

class FocusState(Enum):
    """States of attentional focus"""
    FOCUSED = "focused"          # High concentration on single task
    MULTITASKING = "multitasking"  # Divided attention across tasks
    SWITCHING = "switching"      # Transitioning between tasks
    DISTRACTED = "distracted"    # Attention captured by irrelevant stimuli
    FATIGUED = "fatigued"        # Reduced attention capacity
    HYPERVIGILANT = "hypervigilant"  # Heightened attention state

@dataclass
class AttentionalResource:
    """Represents attentional capacity and allocation"""
    total_capacity: float = 100.0
    available_capacity: float = 100.0
    allocated_resources: Dict[str, float] = field(default_factory=dict)
    depletion_rate: float = 0.1  # How quickly attention depletes
    recovery_rate: float = 0.05  # How quickly attention recovers
    efficiency: float = 1.0      # How efficiently attention is used

@dataclass
class AttentionTarget:
    """Represents something that can receive attention"""
    target_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    priority: float = 0.5
    salience: float = 0.5        # How attention-grabbing it is
    cognitive_load: float = 0.5   # How much attention it requires
    duration: float = 1.0         # How long it needs attention
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    attention_decay: float = 0.1  # How quickly it loses attention

class AttentionMechanism:
    """
    Advanced attention mechanism that manages focus, task switching, and cognitive load
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"AttentionMechanism-{persona_type}")
        
        # Attention resources
        self.attention_resources = AttentionalResource()
        self.attention_targets = {}
        self.attention_history = deque(maxlen=1000)
        
        # Attention state
        self.current_focus_state = FocusState.FOCUSED
        self.primary_focus = None
        self.secondary_foci = []
        self.distraction_resistance = 0.7
        
        # Persona-specific attention parameters
        self.attention_params = self._initialize_attention_parameters()
        self.task_switching_cost = self._initialize_task_switching_cost()
        
        # Attention control mechanisms
        self.attention_filters = self._initialize_attention_filters()
        self.priority_weights = self._initialize_priority_weights()
        
        # Performance tracking
        self.attention_performance = {
            "focus_duration": [],
            "task_switching_frequency": 0,
            "distraction_episodes": 0,
            "cognitive_load_history": deque(maxlen=100)
        }
        
        # Fatigue and recovery
        self.fatigue_level = 0.0
        self.last_break_time = datetime.now()
        self.attention_burnout_threshold = 0.8
        
    def _initialize_attention_parameters(self) -> Dict[str, float]:
        """Initialize attention parameters based on persona type"""
        
        base_params = {
            "selective_attention_strength": 0.7,
            "divided_attention_capacity": 0.5,
            "sustained_attention_duration": 0.6,
            "executive_control_strength": 0.6,
            "distractibility": 0.4,
            "attention_span": 0.6,
            "focus_stability": 0.7
        }
        
        # Adjust based on persona type
        if "student" in self.persona_type.lower():
            base_params.update({
                "distractibility": 0.6,
                "divided_attention_capacity": 0.7,
                "attention_span": 0.5
            })
        elif "faculty" in self.persona_type.lower() or "researcher" in self.persona_type.lower():
            base_params.update({
                "sustained_attention_duration": 0.9,
                "selective_attention_strength": 0.8,
                "focus_stability": 0.8
            })
        elif "administrator" in self.persona_type.lower():
            base_params.update({
                "divided_attention_capacity": 0.8,
                "executive_control_strength": 0.8,
                "task_switching_efficiency": 0.7
            })
        elif "advisor" in self.persona_type.lower():
            base_params.update({
                "selective_attention_strength": 0.8,
                "executive_control_strength": 0.7,
                "focus_stability": 0.6
            })
        
        return base_params
    
    def _initialize_task_switching_cost(self) -> Dict[str, float]:
        """Initialize task switching costs"""
        
        return {
            "same_domain": 0.1,      # Low cost for similar tasks
            "different_domain": 0.3, # Medium cost for different domains
            "cognitive_mode": 0.4,   # High cost for different cognitive modes
            "interruption_cost": 0.5, # Cost of unexpected interruptions
            "context_switching": 0.2   # Cost of switching contexts
        }
    
    def _initialize_attention_filters(self) -> Dict[str, Dict[str, Any]]:
        """Initialize attention filtering mechanisms"""
        
        return {
            "priority_filter": {
                "enabled": True,
                "threshold": 0.6,
                "adaptation_rate": 0.1
            },
            "relevance_filter": {
                "enabled": True,
                "threshold": 0.5,
                "context_sensitivity": 0.7
            },
            "novelty_filter": {
                "enabled": True,
                "threshold": 0.4,
                "habituation_rate": 0.2
            },
            "urgency_filter": {
                "enabled": True,
                "threshold": 0.7,
                "escalation_rate": 0.3
            }
        }
    
    def _initialize_priority_weights(self) -> Dict[str, float]:
        """Initialize priority weights for different types of attention targets"""
        
        base_weights = {
            "urgent_tasks": 0.9,
            "important_tasks": 0.8,
            "routine_tasks": 0.4,
            "learning_opportunities": 0.6,
            "social_interactions": 0.5,
            "interruptions": 0.3,
            "notifications": 0.2,
            "background_processes": 0.1
        }
        
        # Adjust based on persona type
        if "student" in self.persona_type.lower():
            base_weights.update({
                "learning_opportunities": 0.8,
                "social_interactions": 0.7,
                "notifications": 0.4
            })
        elif "faculty" in self.persona_type.lower():
            base_weights.update({
                "important_tasks": 0.9,
                "learning_opportunities": 0.7,
                "interruptions": 0.2
            })
        
        return base_weights
    
    async def allocate_attention(self, targets: List[AttentionTarget]) -> Dict[str, Any]:
        """Allocate attention across multiple targets"""
        
        if not targets:
            return {"message": "No attention targets provided"}
        
        # Filter targets based on attention filters
        filtered_targets = await self._apply_attention_filters(targets)
        
        # Calculate attention allocation
        allocation = await self._calculate_attention_allocation(filtered_targets)
        
        # Update attention state
        await self._update_attention_state(allocation)
        
        # Monitor cognitive load
        cognitive_load = self._calculate_current_cognitive_load(allocation)
        
        # Update performance metrics
        self._update_attention_performance(allocation, cognitive_load)
        
        return {
            "allocation": allocation,
            "cognitive_load": cognitive_load,
            "focus_state": self.current_focus_state.value,
            "primary_focus": self.primary_focus,
            "attention_efficiency": self._calculate_attention_efficiency(),
            "recommendations": await self._generate_attention_recommendations(allocation, cognitive_load)
        }
    
    async def _apply_attention_filters(self, targets: List[AttentionTarget]) -> List[AttentionTarget]:
        """Apply attention filters to determine which targets merit attention"""
        
        filtered_targets = []
        
        for target in targets:
            should_attend = True
            
            # Priority filter
            if self.attention_filters["priority_filter"]["enabled"]:
                if target.priority < self.attention_filters["priority_filter"]["threshold"]:
                    should_attend = False
            
            # Relevance filter
            if should_attend and self.attention_filters["relevance_filter"]["enabled"]:
                relevance_score = await self._calculate_relevance(target)
                if relevance_score < self.attention_filters["relevance_filter"]["threshold"]:
                    should_attend = False
            
            # Novelty filter
            if should_attend and self.attention_filters["novelty_filter"]["enabled"]:
                novelty_score = await self._calculate_novelty(target)
                if novelty_score < self.attention_filters["novelty_filter"]["threshold"] and target.priority < 0.7:
                    should_attend = False
            
            # Urgency filter
            if should_attend and self.attention_filters["urgency_filter"]["enabled"]:
                urgency_score = await self._calculate_urgency(target)
                if urgency_score > self.attention_filters["urgency_filter"]["threshold"]:
                    should_attend = True  # Override other filters for urgent items
            
            if should_attend:
                filtered_targets.append(target)
        
        return filtered_targets
    
    async def _calculate_relevance(self, target: AttentionTarget) -> float:
        """Calculate relevance of target to current context"""
        
        # Simple relevance calculation based on context overlap
        current_context = self._get_current_context()
        target_context = target.context
        
        if not current_context or not target_context:
            return 0.5  # Default relevance
        
        # Calculate context similarity
        common_keys = set(current_context.keys()).intersection(set(target_context.keys()))
        relevance = len(common_keys) / max(len(current_context), len(target_context))
        
        return min(1.0, max(0.0, relevance))
    
    async def _calculate_novelty(self, target: AttentionTarget) -> float:
        """Calculate novelty of target based on attention history"""
        
        # Check how often similar targets have received attention recently
        recent_targets = [entry for entry in self.attention_history 
                         if (datetime.now() - entry["timestamp"]).total_seconds() < 3600]  # Last hour
        
        similar_count = sum(1 for entry in recent_targets 
                          if self._targets_similar(target, entry.get("target")))
        
        # Higher similarity count = lower novelty
        novelty = 1.0 - min(1.0, similar_count / 10)
        return novelty
    
    def _targets_similar(self, target1: AttentionTarget, target2: Optional[Dict[str, Any]]) -> bool:
        """Check if two targets are similar"""
        
        if not target2:
            return False
        
        # Simple similarity based on name similarity
        name1 = target1.name.lower()
        name2 = target2.get("name", "").lower()
        
        # Check for common words
        words1 = set(name1.split())
        words2 = set(name2.split())
        
        if words1 and words2:
            similarity = len(words1.intersection(words2)) / len(words1.union(words2))
            return similarity > 0.3
        
        return False
    
    async def _calculate_urgency(self, target: AttentionTarget) -> float:
        """Calculate urgency of target"""
        
        # Urgency based on time sensitivity and priority
        base_urgency = target.priority
        
        # Time-based urgency
        time_factor = 1.0
        if "deadline" in target.context:
            deadline = target.context.get("deadline")
            if isinstance(deadline, datetime):
                time_remaining = (deadline - datetime.now()).total_seconds()
                if time_remaining < 3600:  # Less than 1 hour
                    time_factor = 2.0
                elif time_remaining < 86400:  # Less than 1 day
                    time_factor = 1.5
        
        urgency = min(1.0, base_urgency * time_factor)
        return urgency
    
    async def _calculate_attention_allocation(self, targets: List[AttentionTarget]) -> Dict[str, Any]:
        """Calculate optimal attention allocation across filtered targets"""
        
        if not targets:
            return {"allocations": {}, "total_load": 0.0}
        
        # Calculate raw attention scores
        attention_scores = {}
        total_demand = 0.0
        
        for target in targets:
            # Base score from priority and salience
            base_score = (target.priority * 0.6 + target.salience * 0.4)
            
            # Adjust for cognitive load requirements
            load_adjusted_score = base_score * (1.0 + target.cognitive_load * 0.5)
            
            # Apply persona-specific weighting
            persona_weight = self._get_persona_weight(target)
            final_score = load_adjusted_score * persona_weight
            
            attention_scores[target.target_id] = {
                "target": target,
                "score": final_score,
                "demand": target.cognitive_load
            }
            total_demand += target.cognitive_load
        
        # Normalize scores and allocate attention
        available_capacity = self.attention_resources.available_capacity
        
        if total_demand <= available_capacity:
            # Can satisfy all demands
            allocations = {}
            for target_id, score_data in attention_scores.items():
                allocations[target_id] = {
                    "allocated_attention": score_data["demand"],
                    "attention_ratio": score_data["demand"] / available_capacity,
                    "target_info": score_data["target"].__dict__
                }
        else:
            # Need to prioritize and distribute limited attention
            allocations = await self._distribute_limited_attention(attention_scores, available_capacity)
        
        return {
            "allocations": allocations,
            "total_demand": total_demand,
            "available_capacity": available_capacity,
            "capacity_utilization": min(1.0, total_demand / available_capacity)
        }
    
    def _get_persona_weight(self, target: AttentionTarget) -> float:
        """Get persona-specific weighting for target"""
        
        # Determine target category
        target_category = self._categorize_target(target)
        
        # Get weight from priority weights
        weight = self.priority_weights.get(target_category, 0.5)
        
        return weight
    
    def _categorize_target(self, target: AttentionTarget) -> str:
        """Categorize attention target"""
        
        name_lower = target.name.lower()
        
        if any(word in name_lower for word in ["urgent", "emergency", "critical"]):
            return "urgent_tasks"
        elif any(word in name_lower for word in ["important", "priority", "key"]):
            return "important_tasks"
        elif any(word in name_lower for word in ["learn", "study", "education"]):
            return "learning_opportunities"
        elif any(word in name_lower for word in ["social", "meeting", "discussion"]):
            return "social_interactions"
        elif any(word in name_lower for word in ["notification", "alert", "message"]):
            return "notifications"
        elif any(word in name_lower for word in ["routine", "regular", "daily"]):
            return "routine_tasks"
        else:
            return "background_processes"
    
    async def _distribute_limited_attention(self, attention_scores: Dict[str, Dict[str, Any]], 
                                          available_capacity: float) -> Dict[str, Any]:
        """Distribute limited attention capacity optimally"""
        
        # Sort targets by priority score
        sorted_targets = sorted(attention_scores.items(), 
                              key=lambda x: x[1]["score"], 
                              reverse=True)
        
        allocations = {}
        remaining_capacity = available_capacity
        
        for target_id, score_data in sorted_targets:
            target = score_data["target"]
            demanded_attention = score_data["demand"]
            
            if remaining_capacity >= demanded_attention:
                # Can fully satisfy this target
                allocated = demanded_attention
                remaining_capacity -= demanded_attention
            elif remaining_capacity > 0:
                # Partial allocation
                allocated = remaining_capacity
                remaining_capacity = 0
            else:
                # No capacity left
                allocated = 0
            
            if allocated > 0:
                allocations[target_id] = {
                    "allocated_attention": allocated,
                    "attention_ratio": allocated / available_capacity,
                    "satisfaction_ratio": allocated / demanded_attention,
                    "target_info": target.__dict__
                }
        
        return allocations
    
    def _get_current_context(self) -> Dict[str, Any]:
        """Get current attention context"""
        
        context = {
            "focus_state": self.current_focus_state.value,
            "fatigue_level": self.fatigue_level,
            "time_of_day": datetime.now().hour,
            "cognitive_load": self._calculate_current_cognitive_load({})
        }
        
        if self.primary_focus:
            context["primary_focus"] = self.primary_focus
        
        return context
    
    async def _update_attention_state(self, allocation: Dict[str, Any]):
        """Update attention state based on allocation"""
        
        allocations = allocation.get("allocations", {})
        
        if not allocations:
            self.current_focus_state = FocusState.FOCUSED
            self.primary_focus = None
            self.secondary_foci = []
            return
        
        # Determine primary focus (highest allocated attention)
        primary_target = max(allocations.items(), 
                           key=lambda x: x[1]["allocated_attention"])
        self.primary_focus = primary_target[0]
        
        # Determine secondary foci
        self.secondary_foci = [target_id for target_id, alloc in allocations.items()
                              if target_id != self.primary_focus and 
                              alloc["allocated_attention"] > 0.1]
        
        # Determine focus state
        if len(allocations) == 1:
            self.current_focus_state = FocusState.FOCUSED
        elif len(allocations) <= 3:
            self.current_focus_state = FocusState.MULTITASKING
        else:
            self.current_focus_state = FocusState.DISTRACTED
        
        # Update attention resources
        total_allocated = sum(alloc["allocated_attention"] for alloc in allocations.values())
        self.attention_resources.available_capacity = max(0, 
            self.attention_resources.total_capacity - total_allocated)
        
        # Record attention allocation
        self.attention_history.append({
            "timestamp": datetime.now(),
            "allocation": allocation,
            "focus_state": self.current_focus_state.value,
            "primary_focus": self.primary_focus
        })
    
    def _calculate_current_cognitive_load(self, allocation: Dict[str, Any]) -> float:
        """Calculate current cognitive load"""
        
        allocations = allocation.get("allocations", {})
        
        if not allocations:
            return 0.0
        
        # Base load from allocated attention
        base_load = sum(alloc["allocated_attention"] for alloc in allocations.values())
        
        # Task switching penalty
        switching_penalty = 0
        if len(allocations) > 1:
            switching_penalty = len(allocations) * self.task_switching_cost["different_domain"]
        
        # Multitasking penalty
        multitasking_penalty = 0
        if len(allocations) > 2:
            multitasking_penalty = (len(allocations) - 2) * 0.1
        
        # Fatigue effect
        fatigue_multiplier = 1.0 + self.fatigue_level * 0.5
        
        total_load = (base_load + switching_penalty + multitasking_penalty) * fatigue_multiplier
        
        # Normalize to 0-1 scale
        normalized_load = min(1.0, total_load / self.attention_resources.total_capacity)
        
        return normalized_load
    
    def _calculate_attention_efficiency(self) -> float:
        """Calculate current attention efficiency"""
        
        base_efficiency = self.attention_resources.efficiency
        
        # Reduce efficiency based on focus state
        state_penalties = {
            FocusState.FOCUSED: 0.0,
            FocusState.MULTITASKING: 0.2,
            FocusState.SWITCHING: 0.3,
            FocusState.DISTRACTED: 0.5,
            FocusState.FATIGUED: 0.4,
            FocusState.HYPERVIGILANT: 0.1
        }
        
        penalty = state_penalties.get(self.current_focus_state, 0.2)
        
        # Reduce efficiency based on fatigue
        fatigue_penalty = self.fatigue_level * 0.3
        
        # Reduce efficiency based on cognitive load
        current_load = self._calculate_current_cognitive_load({})
        load_penalty = max(0, current_load - 0.7) * 0.5  # Penalty only when overloaded
        
        efficiency = base_efficiency * (1.0 - penalty - fatigue_penalty - load_penalty)
        return max(0.1, min(1.0, efficiency))
    
    def _update_attention_performance(self, allocation: Dict[str, Any], cognitive_load: float):
        """Update attention performance metrics"""
        
        # Update cognitive load history
        self.attention_performance["cognitive_load_history"].append(cognitive_load)
        
        # Track task switching
        if len(allocation.get("allocations", {})) > 1:
            self.attention_performance["task_switching_frequency"] += 1
        
        # Track distractions
        if self.current_focus_state == FocusState.DISTRACTED:
            self.attention_performance["distraction_episodes"] += 1
        
        # Update fatigue level
        self._update_fatigue_level(cognitive_load)
    
    def _update_fatigue_level(self, cognitive_load: float):
        """Update attention fatigue level"""
        
        # Increase fatigue based on cognitive load
        fatigue_increase = cognitive_load * self.attention_resources.depletion_rate
        
        # Recovery based on time since last break
        time_since_break = (datetime.now() - self.last_break_time).total_seconds() / 3600  # hours
        if time_since_break > 2:  # More than 2 hours
            fatigue_increase *= 1.5  # Accelerated fatigue
        
        self.fatigue_level = min(1.0, self.fatigue_level + fatigue_increase)
        
        # Natural recovery (slow)
        recovery = self.attention_resources.recovery_rate * 0.1
        self.fatigue_level = max(0.0, self.fatigue_level - recovery)
        
        # Update focus state based on fatigue
        if self.fatigue_level > self.attention_burnout_threshold:
            self.current_focus_state = FocusState.FATIGUED
    
    async def _generate_attention_recommendations(self, allocation: Dict[str, Any], 
                                                cognitive_load: float) -> List[str]:
        """Generate recommendations for optimizing attention"""
        
        recommendations = []
        
        # Cognitive load recommendations
        if cognitive_load > 0.8:
            recommendations.append("Consider reducing the number of concurrent tasks")
            recommendations.append("Focus on high-priority tasks first")
        elif cognitive_load < 0.3:
            recommendations.append("Consider taking on additional tasks to optimize productivity")
        
        # Fatigue recommendations
        if self.fatigue_level > 0.7:
            recommendations.append("Take a break to restore attention capacity")
            recommendations.append("Consider switching to less demanding tasks")
        
        # Focus state recommendations
        if self.current_focus_state == FocusState.DISTRACTED:
            recommendations.append("Eliminate distractions from your environment")
            recommendations.append("Use attention training techniques to improve focus")
        elif self.current_focus_state == FocusState.MULTITASKING:
            recommendations.append("Consider batching similar tasks together")
            recommendations.append("Schedule focused time blocks for complex tasks")
        
        # Task switching recommendations
        if self.attention_performance["task_switching_frequency"] > 10:
            recommendations.append("Minimize task switching to reduce cognitive overhead")
            recommendations.append("Group similar activities together")
        
        # Efficiency recommendations
        efficiency = self._calculate_attention_efficiency()
        if efficiency < 0.6:
            recommendations.append("Optimize your work environment for better focus")
            recommendations.append("Consider attention training or mindfulness practices")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    async def switch_attention(self, from_target_id: Optional[str], 
                             to_target: AttentionTarget) -> Dict[str, Any]:
        """Handle attention switching between targets"""
        
        switching_start = datetime.now()
        
        # Calculate switching cost
        switching_cost = await self._calculate_switching_cost(from_target_id, to_target)
        
        # Apply switching cost to attention resources
        self.attention_resources.available_capacity -= switching_cost
        
        # Update attention allocation
        new_allocation = await self._allocate_switching_attention(to_target, switching_cost)
        
        # Update state
        await self._update_attention_state(new_allocation)
        
        switching_duration = (datetime.now() - switching_start).total_seconds()
        
        return {
            "switching_successful": True,
            "switching_cost": switching_cost,
            "switching_duration": switching_duration,
            "new_focus": to_target.target_id,
            "new_allocation": new_allocation,
            "recommendations": await self._generate_switching_recommendations(switching_cost)
        }
    
    async def _calculate_switching_cost(self, from_target_id: Optional[str], 
                                      to_target: AttentionTarget) -> float:
        """Calculate cost of switching attention"""
        
        if not from_target_id:
            return 0.1  # Minimal cost for initial attention allocation
        
        # Get previous target info
        from_target = self.attention_targets.get(from_target_id)
        if not from_target:
            return self.task_switching_cost["context_switching"]
        
        # Determine switching cost based on target similarity
        if self._targets_similar(to_target, from_target.__dict__ if hasattr(from_target, '__dict__') else from_target):
            return self.task_switching_cost["same_domain"]
        else:
            return self.task_switching_cost["different_domain"]
    
    async def _allocate_switching_attention(self, target: AttentionTarget, 
                                          switching_cost: float) -> Dict[str, Any]:
        """Allocate attention during switching"""
        
        # Reduce available capacity by switching cost
        adjusted_capacity = max(0, self.attention_resources.available_capacity - switching_cost)
        
        # Allocate to new target
        allocated_attention = min(target.cognitive_load, adjusted_capacity)
        
        allocation = {
            "allocations": {
                target.target_id: {
                    "allocated_attention": allocated_attention,
                    "attention_ratio": allocated_attention / self.attention_resources.total_capacity,
                    "target_info": target.__dict__
                }
            },
            "switching_cost": switching_cost,
            "available_capacity": adjusted_capacity
        }
        
        return allocation
    
    async def _generate_switching_recommendations(self, switching_cost: float) -> List[str]:
        """Generate recommendations for attention switching"""
        
        recommendations = []
        
        if switching_cost > 0.3:
            recommendations.append("High switching cost detected - consider batching similar tasks")
            recommendations.append("Use transition rituals to reduce switching overhead")
        
        if self.attention_performance["task_switching_frequency"] > 15:
            recommendations.append("Frequent task switching detected - consider time blocking")
        
        return recommendations
    
    async def take_attention_break(self, break_duration: float = 0.25) -> Dict[str, Any]:
        """Take a break to restore attention capacity"""
        
        break_start = datetime.now()
        
        # Calculate recovery amount based on break duration (hours)
        recovery_amount = break_duration * self.attention_resources.recovery_rate * 10
        
        # Restore attention capacity
        previous_capacity = self.attention_resources.available_capacity
        self.attention_resources.available_capacity = min(
            self.attention_resources.total_capacity,
            self.attention_resources.available_capacity + recovery_amount
        )
        
        # Reduce fatigue
        fatigue_reduction = break_duration * 0.5
        self.fatigue_level = max(0.0, self.fatigue_level - fatigue_reduction)
        
        # Update last break time
        self.last_break_time = datetime.now()
        
        # Reset focus state if was fatigued
        if self.current_focus_state == FocusState.FATIGUED and self.fatigue_level < 0.5:
            self.current_focus_state = FocusState.FOCUSED
        
        return {
            "break_taken": True,
            "break_duration": break_duration,
            "capacity_recovered": self.attention_resources.available_capacity - previous_capacity,
            "fatigue_reduction": fatigue_reduction,
            "new_capacity": self.attention_resources.available_capacity,
            "new_fatigue_level": self.fatigue_level,
            "recommendations": ["Return to tasks gradually", "Prioritize high-importance tasks first"]
        }
    
    async def get_attention_status(self) -> Dict[str, Any]:
        """Get current attention system status"""
        
        return {
            "attention_resources": {
                "total_capacity": self.attention_resources.total_capacity,
                "available_capacity": self.attention_resources.available_capacity,
                "capacity_utilization": 1.0 - (self.attention_resources.available_capacity / 
                                             self.attention_resources.total_capacity)
            },
            "attention_state": {
                "focus_state": self.current_focus_state.value,
                "primary_focus": self.primary_focus,
                "secondary_foci": self.secondary_foci,
                "fatigue_level": self.fatigue_level
            },
            "performance_metrics": {
                "attention_efficiency": self._calculate_attention_efficiency(),
                "task_switching_frequency": self.attention_performance["task_switching_frequency"],
                "distraction_episodes": self.attention_performance["distraction_episodes"],
                "average_cognitive_load": np.mean(list(self.attention_performance["cognitive_load_history"])) 
                                        if self.attention_performance["cognitive_load_history"] else 0.0
            },
            "recommendations": await self._generate_attention_recommendations({}, 
                                                                           self._calculate_current_cognitive_load({}))
        }
    
    async def optimize_attention_parameters(self, performance_feedback: Dict[str, Any]):
        """Optimize attention parameters based on performance feedback"""
        
        # Adjust attention parameters based on feedback
        if performance_feedback.get("focus_quality", 0.5) < 0.5:
            # Poor focus quality - increase selective attention
            self.attention_params["selective_attention_strength"] = min(1.0, 
                self.attention_params["selective_attention_strength"] * 1.1)
            
            # Increase distraction resistance
            self.distraction_resistance = min(1.0, self.distraction_resistance * 1.05)
        
        if performance_feedback.get("multitasking_effectiveness", 0.5) < 0.5:
            # Poor multitasking - reduce divided attention attempts
            self.attention_params["divided_attention_capacity"] *= 0.95
        
        if performance_feedback.get("fatigue_level", 0.5) > 0.7:
            # High fatigue - improve recovery mechanisms
            self.attention_resources.recovery_rate = min(0.1, 
                self.attention_resources.recovery_rate * 1.1)
        
        # Adapt filter thresholds
        if performance_feedback.get("irrelevant_distractions", 0) > 5:
            # Too many irrelevant distractions - tighten filters
            for filter_name, filter_config in self.attention_filters.items():
                if filter_config["enabled"]:
                    filter_config["threshold"] = min(1.0, filter_config["threshold"] * 1.1)
        
        return {
            "optimization_complete": True,
            "updated_parameters": self.attention_params,
            "updated_filters": self.attention_filters,
            "recommendations": ["Monitor performance for further adjustments"]
        }