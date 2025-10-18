"""
CollegiumAI Cognitive Architecture - Metacognitive Controller
Advanced metacognitive awareness and control of cognitive processes
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

class MetacognitiveState(Enum):
    """States of metacognitive awareness"""
    MONITORING = "monitoring"        # Actively monitoring cognitive processes
    EVALUATING = "evaluating"       # Evaluating cognitive performance
    PLANNING = "planning"           # Planning cognitive strategies
    REGULATING = "regulating"       # Regulating cognitive processes
    REFLECTING = "reflecting"       # Reflecting on cognitive experiences
    ADAPTING = "adapting"          # Adapting cognitive strategies

class MetacognitiveStrategy(Enum):
    """Types of metacognitive strategies"""
    SELF_MONITORING = "self_monitoring"
    STRATEGY_SELECTION = "strategy_selection"
    RESOURCE_ALLOCATION = "resource_allocation"
    ERROR_DETECTION = "error_detection"
    PERFORMANCE_EVALUATION = "performance_evaluation"
    STRATEGY_ADAPTATION = "strategy_adaptation"

@dataclass
class CognitiveProcessMonitor:
    """Monitor for individual cognitive processes"""
    process_name: str
    process_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = field(default_factory=datetime.now)
    current_state: str = "active"
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    resource_usage: Dict[str, float] = field(default_factory=dict)
    error_count: int = 0
    efficiency_score: float = 0.5
    quality_indicators: Dict[str, float] = field(default_factory=dict)
    strategy_effectiveness: float = 0.5

@dataclass
class MetacognitiveInsight:
    """Represents metacognitive insights about cognitive processes"""
    insight_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    insight_type: str = "performance"
    description: str = ""
    confidence: float = 0.5
    actionable_recommendations: List[str] = field(default_factory=list)
    affected_processes: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)

class MetacognitiveController:
    """
    Advanced metacognitive controller that monitors, evaluates, and regulates
    cognitive processes for optimal performance
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"MetacognitiveController-{persona_type}")
        
        # Metacognitive state
        self.current_state = MetacognitiveState.MONITORING
        self.metacognitive_awareness_level = 0.7
        self.self_regulation_strength = 0.6
        
        # Process monitoring
        self.active_monitors = {}
        self.monitoring_history = deque(maxlen=1000)
        self.performance_trends = {}
        
        # Metacognitive knowledge
        self.strategy_knowledge = self._initialize_strategy_knowledge()
        self.process_knowledge = self._initialize_process_knowledge()
        self.conditional_knowledge = self._initialize_conditional_knowledge()
        
        # Insights and reflections
        self.insights = deque(maxlen=500)
        self.reflection_cycles = []
        self.adaptation_history = []
        
        # Performance tracking
        self.metacognitive_performance = {
            "monitoring_accuracy": 0.7,
            "strategy_effectiveness": 0.6,
            "adaptation_success_rate": 0.5,
            "error_detection_rate": 0.6
        }
        
        # Persona-specific metacognitive parameters
        self.metacognitive_style = self._initialize_metacognitive_style()
        
    def _initialize_strategy_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Initialize knowledge about cognitive strategies"""
        
        return {
            "attention_strategies": {
                "selective_focus": {
                    "effectiveness": 0.8,
                    "cognitive_cost": 0.3,
                    "suitable_contexts": ["complex_tasks", "noisy_environments"],
                    "prerequisites": ["adequate_motivation", "clear_goals"]
                },
                "divided_attention": {
                    "effectiveness": 0.6,
                    "cognitive_cost": 0.7,
                    "suitable_contexts": ["routine_tasks", "multitasking"],
                    "prerequisites": ["well_practiced_skills", "low_complexity"]
                }
            },
            "memory_strategies": {
                "elaborative_rehearsal": {
                    "effectiveness": 0.9,
                    "cognitive_cost": 0.6,
                    "suitable_contexts": ["learning", "understanding"],
                    "prerequisites": ["relevant_knowledge", "sufficient_time"]
                },
                "spaced_repetition": {
                    "effectiveness": 0.8,
                    "cognitive_cost": 0.4,
                    "suitable_contexts": ["memorization", "retention"],
                    "prerequisites": ["scheduling_capability", "consistency"]
                }
            },
            "reasoning_strategies": {
                "analytical_reasoning": {
                    "effectiveness": 0.7,
                    "cognitive_cost": 0.8,
                    "suitable_contexts": ["complex_problems", "logical_tasks"],
                    "prerequisites": ["domain_knowledge", "cognitive_capacity"]
                },
                "intuitive_reasoning": {
                    "effectiveness": 0.6,
                    "cognitive_cost": 0.3,
                    "suitable_contexts": ["familiar_domains", "time_pressure"],
                    "prerequisites": ["domain_expertise", "pattern_recognition"]
                }
            }
        }
    
    def _initialize_process_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Initialize knowledge about cognitive processes"""
        
        return {
            "perception": {
                "typical_duration": 0.1,  # seconds
                "resource_requirements": {"attention": 0.3, "working_memory": 0.2},
                "error_indicators": ["misperception", "attention_lapses"],
                "quality_metrics": ["accuracy", "completeness", "speed"]
            },
            "memory_retrieval": {
                "typical_duration": 0.5,
                "resource_requirements": {"attention": 0.4, "working_memory": 0.6},
                "error_indicators": ["retrieval_failures", "false_memories"],
                "quality_metrics": ["accuracy", "completeness", "relevance"]
            },
            "reasoning": {
                "typical_duration": 2.0,
                "resource_requirements": {"attention": 0.8, "working_memory": 0.9},
                "error_indicators": ["logical_errors", "biased_reasoning"],
                "quality_metrics": ["logical_consistency", "conclusion_validity", "efficiency"]
            },
            "decision_making": {
                "typical_duration": 1.5,
                "resource_requirements": {"attention": 0.7, "working_memory": 0.7},
                "error_indicators": ["poor_outcomes", "decision_regret"],
                "quality_metrics": ["outcome_satisfaction", "decision_confidence", "process_efficiency"]
            }
        }
    
    def _initialize_conditional_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Initialize conditional knowledge about when to use strategies"""
        
        return {
            "high_cognitive_load": {
                "recommended_strategies": ["simplification", "chunking", "external_aids"],
                "avoid_strategies": ["multitasking", "complex_reasoning"]
            },
            "time_pressure": {
                "recommended_strategies": ["satisficing", "heuristics", "intuitive_reasoning"],
                "avoid_strategies": ["exhaustive_search", "detailed_analysis"]
            },
            "unfamiliar_domain": {
                "recommended_strategies": ["systematic_exploration", "analogy_use", "help_seeking"],
                "avoid_strategies": ["intuitive_reasoning", "rapid_decisions"]
            },
            "high_stakes": {
                "recommended_strategies": ["careful_analysis", "verification", "consultation"],
                "avoid_strategies": ["quick_decisions", "minimal_processing"]
            }
        }
    
    def _initialize_metacognitive_style(self) -> Dict[str, float]:
        """Initialize metacognitive style based on persona type"""
        
        base_style = {
            "self_monitoring_frequency": 0.6,
            "strategy_flexibility": 0.5,
            "reflection_depth": 0.6,
            "error_sensitivity": 0.5,
            "confidence_calibration": 0.5,
            "help_seeking_tendency": 0.4
        }
        
        # Adjust based on persona type
        if "student" in self.persona_type.lower():
            base_style.update({
                "self_monitoring_frequency": 0.7,
                "help_seeking_tendency": 0.7,
                "strategy_flexibility": 0.6
            })
        elif "faculty" in self.persona_type.lower() or "researcher" in self.persona_type.lower():
            base_style.update({
                "reflection_depth": 0.8,
                "strategy_flexibility": 0.7,
                "error_sensitivity": 0.7
            })
        elif "administrator" in self.persona_type.lower():
            base_style.update({
                "self_monitoring_frequency": 0.8,
                "confidence_calibration": 0.7,
                "strategy_flexibility": 0.6
            })
        
        return base_style
    
    async def monitor_cognitive_process(self, process_name: str, 
                                      process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor a cognitive process and track its performance"""
        
        # Create or update process monitor
        if process_name not in self.active_monitors:
            self.active_monitors[process_name] = CognitiveProcessMonitor(
                process_name=process_name
            )
        
        monitor = self.active_monitors[process_name]
        
        # Update monitoring data
        await self._update_process_monitor(monitor, process_data)
        
        # Detect anomalies or issues
        issues = await self._detect_process_issues(monitor, process_data)
        
        # Generate monitoring insights
        insights = await self._generate_monitoring_insights(monitor, issues)
        
        # Update metacognitive state
        self._update_metacognitive_state(issues, insights)
        
        # Record monitoring data
        monitoring_record = {
            "timestamp": datetime.now(),
            "process_name": process_name,
            "monitor_data": monitor.__dict__,
            "issues_detected": issues,
            "insights_generated": len(insights)
        }
        self.monitoring_history.append(monitoring_record)
        
        return {
            "monitor_status": "active",
            "process_performance": {
                "efficiency_score": monitor.efficiency_score,
                "error_count": monitor.error_count,
                "strategy_effectiveness": monitor.strategy_effectiveness
            },
            "issues_detected": issues,
            "insights": [insight.__dict__ for insight in insights],
            "recommendations": await self._generate_process_recommendations(monitor, issues)
        }
    
    async def _update_process_monitor(self, monitor: CognitiveProcessMonitor, 
                                    process_data: Dict[str, Any]):
        """Update process monitor with new data"""
        
        # Update performance metrics
        if "performance_metrics" in process_data:
            monitor.performance_metrics.update(process_data["performance_metrics"])
        
        # Update resource usage
        if "resource_usage" in process_data:
            monitor.resource_usage.update(process_data["resource_usage"])
        
        # Calculate efficiency score
        monitor.efficiency_score = await self._calculate_process_efficiency(monitor, process_data)
        
        # Update quality indicators
        monitor.quality_indicators = await self._assess_process_quality(monitor, process_data)
        
        # Track errors
        if process_data.get("errors_detected", 0) > 0:
            monitor.error_count += process_data["errors_detected"]
        
        # Update strategy effectiveness
        if "strategy_used" in process_data:
            monitor.strategy_effectiveness = await self._evaluate_strategy_effectiveness(
                process_data["strategy_used"], process_data
            )
    
    async def _calculate_process_efficiency(self, monitor: CognitiveProcessMonitor, 
                                          process_data: Dict[str, Any]) -> float:
        """Calculate efficiency of cognitive process"""
        
        # Base efficiency from performance metrics
        performance_score = np.mean(list(monitor.performance_metrics.values())) if monitor.performance_metrics else 0.5
        
        # Resource efficiency
        expected_resources = self.process_knowledge.get(monitor.process_name, {}).get("resource_requirements", {})
        actual_resources = monitor.resource_usage
        
        resource_efficiency = 1.0
        for resource, expected in expected_resources.items():
            actual = actual_resources.get(resource, expected)
            if actual > 0:
                resource_efficiency *= min(1.0, expected / actual)
        
        # Time efficiency
        process_duration = process_data.get("duration", 1.0)
        expected_duration = self.process_knowledge.get(monitor.process_name, {}).get("typical_duration", 1.0)
        time_efficiency = min(1.0, expected_duration / process_duration) if process_duration > 0 else 0.5
        
        # Error penalty
        error_penalty = min(0.5, monitor.error_count * 0.1)
        
        # Combined efficiency
        efficiency = (performance_score * 0.4 + resource_efficiency * 0.3 + time_efficiency * 0.3) * (1.0 - error_penalty)
        
        return max(0.0, min(1.0, efficiency))
    
    async def _assess_process_quality(self, monitor: CognitiveProcessMonitor, 
                                    process_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess quality of cognitive process"""
        
        quality_metrics = self.process_knowledge.get(monitor.process_name, {}).get("quality_metrics", [])
        quality_scores = {}
        
        for metric in quality_metrics:
            if metric in process_data:
                quality_scores[metric] = process_data[metric]
            else:
                # Estimate based on available data
                if metric == "accuracy":
                    accuracy = 1.0 - (monitor.error_count / max(1, process_data.get("attempts", 1)))
                    quality_scores[metric] = max(0.0, accuracy)
                elif metric == "speed":
                    duration = process_data.get("duration", 1.0)
                    expected_duration = self.process_knowledge.get(monitor.process_name, {}).get("typical_duration", 1.0)
                    speed_score = min(1.0, expected_duration / duration) if duration > 0 else 0.5
                    quality_scores[metric] = speed_score
                else:
                    quality_scores[metric] = 0.5  # Default neutral score
        
        return quality_scores
    
    async def _evaluate_strategy_effectiveness(self, strategy_used: str, 
                                             process_data: Dict[str, Any]) -> float:
        """Evaluate effectiveness of strategy used"""
        
        # Get strategy information
        strategy_info = None
        for category, strategies in self.strategy_knowledge.items():
            if strategy_used in strategies:
                strategy_info = strategies[strategy_used]
                break
        
        if not strategy_info:
            return 0.5  # Default effectiveness for unknown strategies
        
        # Base effectiveness
        base_effectiveness = strategy_info["effectiveness"]
        
        # Context suitability
        current_context = process_data.get("context", {})
        suitable_contexts = strategy_info.get("suitable_contexts", [])
        
        context_match = 0.5
        if suitable_contexts:
            context_matches = sum(1 for context in suitable_contexts 
                                if context in str(current_context).lower())
            context_match = min(1.0, context_matches / len(suitable_contexts))
        
        # Prerequisites satisfaction
        prerequisites = strategy_info.get("prerequisites", [])
        prerequisite_satisfaction = 1.0
        
        for prereq in prerequisites:
            if prereq == "adequate_motivation":
                prerequisite_satisfaction *= current_context.get("motivation", 0.7)
            elif prereq == "clear_goals":
                prerequisite_satisfaction *= current_context.get("goal_clarity", 0.7)
            elif prereq == "sufficient_time":
                time_pressure = current_context.get("time_pressure", 0.5)
                prerequisite_satisfaction *= (1.0 - time_pressure)
            # Add more prerequisite evaluations as needed
        
        # Combined effectiveness
        effectiveness = base_effectiveness * context_match * prerequisite_satisfaction
        
        return max(0.1, min(1.0, effectiveness))
    
    async def _detect_process_issues(self, monitor: CognitiveProcessMonitor, 
                                   process_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect issues in cognitive process"""
        
        issues = []
        
        # Low efficiency detection
        if monitor.efficiency_score < 0.4:
            issues.append({
                "type": "low_efficiency",
                "severity": "high" if monitor.efficiency_score < 0.2 else "medium",
                "description": f"Process efficiency is low ({monitor.efficiency_score:.2f})",
                "potential_causes": ["inadequate_strategy", "resource_constraints", "fatigue"]
            })
        
        # High error rate detection
        attempts = process_data.get("attempts", 1)
        error_rate = monitor.error_count / attempts if attempts > 0 else 0
        if error_rate > 0.2:
            issues.append({
                "type": "high_error_rate",
                "severity": "high" if error_rate > 0.4 else "medium",
                "description": f"High error rate detected ({error_rate:.2f})",
                "potential_causes": ["attention_lapses", "inadequate_knowledge", "poor_strategy"]
            })
        
        # Resource overconsumption
        for resource, usage in monitor.resource_usage.items():
            expected_usage = self.process_knowledge.get(monitor.process_name, {}).get("resource_requirements", {}).get(resource, 0.5)
            if usage > expected_usage * 1.5:
                issues.append({
                    "type": "resource_overconsumption",
                    "severity": "medium",
                    "description": f"High {resource} usage ({usage:.2f} vs expected {expected_usage:.2f})",
                    "potential_causes": ["inefficient_strategy", "task_complexity", "lack_of_automation"]
                })
        
        # Duration issues
        duration = process_data.get("duration", 1.0)
        expected_duration = self.process_knowledge.get(monitor.process_name, {}).get("typical_duration", 1.0)
        if duration > expected_duration * 2:
            issues.append({
                "type": "slow_processing",
                "severity": "medium",
                "description": f"Process taking longer than expected ({duration:.2f}s vs {expected_duration:.2f}s)",
                "potential_causes": ["cognitive_overload", "unfamiliarity", "poor_strategy"]
            })
        
        return issues
    
    async def _generate_monitoring_insights(self, monitor: CognitiveProcessMonitor, 
                                          issues: List[Dict[str, Any]]) -> List[MetacognitiveInsight]:
        """Generate insights from process monitoring"""
        
        insights = []
        
        # Performance trend insights
        if monitor.process_name in self.performance_trends:
            trend_data = self.performance_trends[monitor.process_name]
            trend_direction = self._calculate_performance_trend(trend_data)
            
            if abs(trend_direction) > 0.1:  # Significant trend
                insight = MetacognitiveInsight(
                    insight_type="performance_trend",
                    description=f"Performance trend detected: {'improving' if trend_direction > 0 else 'declining'}",
                    confidence=min(1.0, abs(trend_direction)),
                    actionable_recommendations=self._get_trend_recommendations(trend_direction),
                    affected_processes=[monitor.process_name],
                    evidence={"trend_direction": trend_direction, "data_points": len(trend_data)}
                )
                insights.append(insight)
        
        # Strategy effectiveness insights
        if monitor.strategy_effectiveness < 0.4:
            insight = MetacognitiveInsight(
                insight_type="strategy_ineffectiveness",
                description="Current strategy appears to be ineffective",
                confidence=1.0 - monitor.strategy_effectiveness,
                actionable_recommendations=[
                    "Consider alternative strategies",
                    "Analyze strategy-context mismatch",
                    "Seek additional resources or support"
                ],
                affected_processes=[monitor.process_name],
                evidence={"strategy_effectiveness": monitor.strategy_effectiveness}
            )
            insights.append(insight)
        
        # Resource utilization insights
        high_resource_usage = [resource for resource, usage in monitor.resource_usage.items() 
                              if usage > 0.8]
        if high_resource_usage:
            insight = MetacognitiveInsight(
                insight_type="resource_strain",
                description=f"High resource utilization detected: {', '.join(high_resource_usage)}",
                confidence=0.8,
                actionable_recommendations=[
                    "Consider resource-efficient strategies",
                    "Take breaks to restore resources",
                    "Simplify task approach"
                ],
                affected_processes=[monitor.process_name],
                evidence={"high_resource_usage": high_resource_usage}
            )
            insights.append(insight)
        
        # Store insights
        for insight in insights:
            self.insights.append(insight)
        
        return insights
    
    def _calculate_performance_trend(self, trend_data: List[float]) -> float:
        """Calculate performance trend direction"""
        
        if len(trend_data) < 3:
            return 0.0
        
        # Simple linear trend calculation
        x = np.arange(len(trend_data))
        y = np.array(trend_data)
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        return slope
    
    def _get_trend_recommendations(self, trend_direction: float) -> List[str]:
        """Get recommendations based on performance trend"""
        
        if trend_direction > 0:
            return [
                "Continue current approach - performance is improving",
                "Consider applying successful strategies to other areas",
                "Document what's working well"
            ]
        else:
            return [
                "Analyze what might be causing performance decline",
                "Consider strategy changes or modifications",
                "Take breaks if fatigue might be a factor",
                "Seek feedback or assistance"
            ]
    
    def _update_metacognitive_state(self, issues: List[Dict[str, Any]], 
                                   insights: List[MetacognitiveInsight]):
        """Update metacognitive state based on monitoring results"""
        
        # Determine appropriate metacognitive state
        if issues:
            high_severity_issues = [issue for issue in issues if issue.get("severity") == "high"]
            if high_severity_issues:
                self.current_state = MetacognitiveState.REGULATING
            else:
                self.current_state = MetacognitiveState.EVALUATING
        elif insights:
            self.current_state = MetacognitiveState.REFLECTING
        else:
            self.current_state = MetacognitiveState.MONITORING
        
        # Update metacognitive awareness
        issue_count = len(issues)
        insight_count = len(insights)
        
        # Higher awareness if detecting more issues and generating insights
        awareness_boost = min(0.1, (issue_count + insight_count) * 0.02)
        self.metacognitive_awareness_level = min(1.0, self.metacognitive_awareness_level + awareness_boost)
    
    async def _generate_process_recommendations(self, monitor: CognitiveProcessMonitor, 
                                              issues: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations for process improvement"""
        
        recommendations = []
        
        # Issue-specific recommendations
        for issue in issues:
            if issue["type"] == "low_efficiency":
                recommendations.extend([
                    "Consider switching to a more efficient strategy",
                    "Break down complex tasks into smaller components",
                    "Eliminate distractions from your environment"
                ])
            elif issue["type"] == "high_error_rate":
                recommendations.extend([
                    "Slow down and focus on accuracy",
                    "Use verification strategies",
                    "Seek additional knowledge or training"
                ])
            elif issue["type"] == "resource_overconsumption":
                recommendations.extend([
                    "Use external aids to reduce cognitive load",
                    "Practice to improve automaticity",
                    "Consider simpler approaches"
                ])
        
        # General process improvement recommendations
        if monitor.efficiency_score < 0.6:
            recommendations.append("Consider metacognitive strategy training")
        
        if monitor.error_count > 3:
            recommendations.append("Implement error-checking routines")
        
        # Remove duplicates and limit
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:5]
    
    async def evaluate_cognitive_performance(self, time_window: int = 3600) -> Dict[str, Any]:
        """Evaluate overall cognitive performance over a time window"""
        
        self.current_state = MetacognitiveState.EVALUATING
        
        # Get recent monitoring data
        cutoff_time = datetime.now() - timedelta(seconds=time_window)
        recent_data = [record for record in self.monitoring_history 
                      if record["timestamp"] > cutoff_time]
        
        if not recent_data:
            return {"message": "No recent performance data available"}
        
        # Aggregate performance metrics
        performance_summary = await self._aggregate_performance_metrics(recent_data)
        
        # Identify patterns and trends
        patterns = await self._identify_performance_patterns(recent_data)
        
        # Generate performance insights
        performance_insights = await self._generate_performance_insights(performance_summary, patterns)
        
        # Update performance trends
        self._update_performance_trends(performance_summary)
        
        evaluation_result = {
            "evaluation_timestamp": datetime.now().isoformat(),
            "time_window_hours": time_window / 3600,
            "performance_summary": performance_summary,
            "patterns_identified": patterns,
            "insights": [insight.__dict__ for insight in performance_insights],
            "overall_rating": self._calculate_overall_performance_rating(performance_summary),
            "improvement_areas": self._identify_improvement_areas(performance_summary),
            "strengths": self._identify_cognitive_strengths(performance_summary)
        }
        
        return evaluation_result
    
    async def _aggregate_performance_metrics(self, recent_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate performance metrics from recent data"""
        
        metrics_by_process = {}
        
        for record in recent_data:
            process_name = record["process_name"]
            monitor_data = record["monitor_data"]
            
            if process_name not in metrics_by_process:
                metrics_by_process[process_name] = {
                    "efficiency_scores": [],
                    "error_counts": [],
                    "strategy_effectiveness": [],
                    "quality_scores": []
                }
            
            metrics_by_process[process_name]["efficiency_scores"].append(monitor_data["efficiency_score"])
            metrics_by_process[process_name]["error_counts"].append(monitor_data["error_count"])
            metrics_by_process[process_name]["strategy_effectiveness"].append(monitor_data["strategy_effectiveness"])
            
            # Aggregate quality indicators
            quality_scores = list(monitor_data.get("quality_indicators", {}).values())
            if quality_scores:
                metrics_by_process[process_name]["quality_scores"].extend(quality_scores)
        
        # Calculate summary statistics
        summary = {}
        for process_name, metrics in metrics_by_process.items():
            summary[process_name] = {
                "average_efficiency": np.mean(metrics["efficiency_scores"]),
                "efficiency_std": np.std(metrics["efficiency_scores"]),
                "total_errors": sum(metrics["error_counts"]),
                "average_strategy_effectiveness": np.mean(metrics["strategy_effectiveness"]),
                "average_quality": np.mean(metrics["quality_scores"]) if metrics["quality_scores"] else 0.5,
                "sample_count": len(metrics["efficiency_scores"])
            }
        
        # Overall summary
        all_efficiency_scores = [score for metrics in metrics_by_process.values() 
                               for score in metrics["efficiency_scores"]]
        all_quality_scores = [score for metrics in metrics_by_process.values() 
                            for score in metrics["quality_scores"]]
        
        summary["overall"] = {
            "average_efficiency": np.mean(all_efficiency_scores) if all_efficiency_scores else 0.5,
            "efficiency_consistency": 1.0 - np.std(all_efficiency_scores) if len(all_efficiency_scores) > 1 else 0.5,
            "average_quality": np.mean(all_quality_scores) if all_quality_scores else 0.5,
            "total_processes_monitored": len(metrics_by_process)
        }
        
        return summary
    
    async def _identify_performance_patterns(self, recent_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify patterns in performance data"""
        
        patterns = []
        
        # Time-based patterns
        hourly_performance = {}
        for record in recent_data:
            hour = record["timestamp"].hour
            efficiency = record["monitor_data"]["efficiency_score"]
            
            if hour not in hourly_performance:
                hourly_performance[hour] = []
            hourly_performance[hour].append(efficiency)
        
        # Find peak performance hours
        if len(hourly_performance) > 2:
            avg_hourly_performance = {hour: np.mean(scores) for hour, scores in hourly_performance.items()}
            best_hour = max(avg_hourly_performance.items(), key=lambda x: x[1])
            worst_hour = min(avg_hourly_performance.items(), key=lambda x: x[1])
            
            if best_hour[1] - worst_hour[1] > 0.2:  # Significant difference
                patterns.append({
                    "type": "time_based_performance",
                    "description": f"Performance peaks at hour {best_hour[0]} and dips at hour {worst_hour[0]}",
                    "confidence": min(1.0, (best_hour[1] - worst_hour[1]) * 2),
                    "data": {"best_hour": best_hour, "worst_hour": worst_hour}
                })
        
        # Process-specific patterns
        process_performance = {}
        for record in recent_data:
            process = record["process_name"]
            efficiency = record["monitor_data"]["efficiency_score"]
            
            if process not in process_performance:
                process_performance[process] = []
            process_performance[process].append(efficiency)
        
        if len(process_performance) > 1:
            avg_process_performance = {process: np.mean(scores) for process, scores in process_performance.items()}
            strongest_process = max(avg_process_performance.items(), key=lambda x: x[1])
            weakest_process = min(avg_process_performance.items(), key=lambda x: x[1])
            
            patterns.append({
                "type": "process_performance_variation",
                "description": f"Strongest performance in {strongest_process[0]}, weakest in {weakest_process[0]}",
                "confidence": 0.8,
                "data": {"strongest": strongest_process, "weakest": weakest_process}
            })
        
        return patterns
    
    async def _generate_performance_insights(self, performance_summary: Dict[str, Any], 
                                           patterns: List[Dict[str, Any]]) -> List[MetacognitiveInsight]:
        """Generate insights from performance evaluation"""
        
        insights = []
        
        # Overall performance insight
        overall_efficiency = performance_summary["overall"]["average_efficiency"]
        if overall_efficiency < 0.5:
            insight = MetacognitiveInsight(
                insight_type="low_overall_performance",
                description=f"Overall cognitive performance is below optimal ({overall_efficiency:.2f})",
                confidence=1.0 - overall_efficiency,
                actionable_recommendations=[
                    "Consider comprehensive strategy review",
                    "Assess for fatigue or stress factors",
                    "Implement systematic performance improvement plan"
                ],
                evidence={"overall_efficiency": overall_efficiency}
            )
            insights.append(insight)
        elif overall_efficiency > 0.8:
            insight = MetacognitiveInsight(
                insight_type="high_performance",
                description=f"Cognitive performance is excellent ({overall_efficiency:.2f})",
                confidence=overall_efficiency,
                actionable_recommendations=[
                    "Document successful strategies for future use",
                    "Consider sharing effective approaches with others",
                    "Maintain current approach while staying adaptable"
                ],
                evidence={"overall_efficiency": overall_efficiency}
            )
            insights.append(insight)
        
        # Pattern-based insights
        for pattern in patterns:
            if pattern["type"] == "time_based_performance":
                insight = MetacognitiveInsight(
                    insight_type="time_optimization",
                    description="Identified optimal performance times",
                    confidence=pattern["confidence"],
                    actionable_recommendations=[
                        f"Schedule demanding tasks during peak hours ({pattern['data']['best_hour'][0]})",
                        f"Use low-performance hours ({pattern['data']['worst_hour'][0]}) for routine tasks",
                        "Consider energy management strategies"
                    ],
                    evidence=pattern["data"]
                )
                insights.append(insight)
        
        # Store insights
        for insight in insights:
            self.insights.append(insight)
        
        return insights
    
    def _update_performance_trends(self, performance_summary: Dict[str, Any]):
        """Update performance trends with new data"""
        
        for process_name, metrics in performance_summary.items():
            if process_name != "overall":
                if process_name not in self.performance_trends:
                    self.performance_trends[process_name] = []
                
                self.performance_trends[process_name].append(metrics["average_efficiency"])
                
                # Keep only recent trend data
                if len(self.performance_trends[process_name]) > 20:
                    self.performance_trends[process_name] = self.performance_trends[process_name][-20:]
    
    def _calculate_overall_performance_rating(self, performance_summary: Dict[str, Any]) -> str:
        """Calculate overall performance rating"""
        
        overall_efficiency = performance_summary["overall"]["average_efficiency"]
        
        if overall_efficiency >= 0.8:
            return "Excellent"
        elif overall_efficiency >= 0.7:
            return "Good"
        elif overall_efficiency >= 0.5:
            return "Satisfactory"
        elif overall_efficiency >= 0.3:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _identify_improvement_areas(self, performance_summary: Dict[str, Any]) -> List[str]:
        """Identify areas needing improvement"""
        
        improvement_areas = []
        
        for process_name, metrics in performance_summary.items():
            if process_name != "overall":
                if metrics["average_efficiency"] < 0.5:
                    improvement_areas.append(f"{process_name.replace('_', ' ').title()} efficiency")
                
                if metrics["total_errors"] > 5:
                    improvement_areas.append(f"{process_name.replace('_', ' ').title()} accuracy")
                
                if metrics["average_strategy_effectiveness"] < 0.5:
                    improvement_areas.append(f"{process_name.replace('_', ' ').title()} strategy selection")
        
        # Overall improvement areas
        overall_metrics = performance_summary["overall"]
        if overall_metrics["efficiency_consistency"] < 0.6:
            improvement_areas.append("Performance consistency")
        
        return improvement_areas[:5]  # Limit to top 5
    
    def _identify_cognitive_strengths(self, performance_summary: Dict[str, Any]) -> List[str]:
        """Identify cognitive strengths"""
        
        strengths = []
        
        for process_name, metrics in performance_summary.items():
            if process_name != "overall":
                if metrics["average_efficiency"] > 0.7:
                    strengths.append(f"Strong {process_name.replace('_', ' ')} performance")
                
                if metrics["average_strategy_effectiveness"] > 0.7:
                    strengths.append(f"Effective {process_name.replace('_', ' ')} strategies")
                
                if metrics["total_errors"] < 2:
                    strengths.append(f"High {process_name.replace('_', ' ')} accuracy")
        
        # Overall strengths
        overall_metrics = performance_summary["overall"]
        if overall_metrics["efficiency_consistency"] > 0.8:
            strengths.append("Consistent performance across tasks")
        
        return strengths[:5]  # Limit to top 5
    
    async def regulate_cognitive_processes(self, regulation_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Regulate cognitive processes to achieve specified goals"""
        
        self.current_state = MetacognitiveState.REGULATING
        
        regulation_actions = []
        
        # Process-specific regulation
        for process_name, goal in regulation_goals.items():
            if process_name in self.active_monitors:
                monitor = self.active_monitors[process_name]
                actions = await self._regulate_single_process(monitor, goal)
                regulation_actions.extend(actions)
        
        # Global regulation actions
        global_actions = await self._apply_global_regulation(regulation_goals)
        regulation_actions.extend(global_actions)
        
        return {
            "regulation_complete": True,
            "actions_taken": regulation_actions,
            "predicted_outcomes": await self._predict_regulation_outcomes(regulation_actions),
            "monitoring_adjustments": await self._adjust_monitoring_parameters(regulation_goals)
        }
    
    async def _regulate_single_process(self, monitor: CognitiveProcessMonitor, 
                                     goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Regulate a single cognitive process"""
        
        actions = []
        
        # Efficiency regulation
        target_efficiency = goal.get("target_efficiency", 0.7)
        if monitor.efficiency_score < target_efficiency:
            # Suggest strategy change
            actions.append({
                "type": "strategy_change",
                "process": monitor.process_name,
                "current_efficiency": monitor.efficiency_score,
                "target_efficiency": target_efficiency,
                "recommendation": "Consider switching to a more efficient strategy"
            })
            
            # Resource optimization
            actions.append({
                "type": "resource_optimization",
                "process": monitor.process_name,
                "recommendation": "Optimize resource usage for better efficiency"
            })
        
        # Error reduction
        max_errors = goal.get("max_errors", 2)
        if monitor.error_count > max_errors:
            actions.append({
                "type": "error_reduction",
                "process": monitor.process_name,
                "current_errors": monitor.error_count,
                "target_errors": max_errors,
                "recommendation": "Implement error-checking and verification strategies"
            })
        
        return actions
    
    async def _apply_global_regulation(self, regulation_goals: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply global cognitive regulation"""
        
        actions = []
        
        # Overall performance regulation
        if "overall_performance" in regulation_goals:
            target_performance = regulation_goals["overall_performance"]
            current_performance = np.mean([monitor.efficiency_score for monitor in self.active_monitors.values()])
            
            if current_performance < target_performance:
                actions.append({
                    "type": "global_performance_boost",
                    "current_performance": current_performance,
                    "target_performance": target_performance,
                    "recommendations": [
                        "Take a cognitive break to restore resources",
                        "Reassess and optimize current strategies",
                        "Consider environmental modifications"
                    ]
                })
        
        # Cognitive load regulation
        if "cognitive_load_limit" in regulation_goals:
            load_limit = regulation_goals["cognitive_load_limit"]
            total_load = sum(sum(monitor.resource_usage.values()) for monitor in self.active_monitors.values())
            
            if total_load > load_limit:
                actions.append({
                    "type": "cognitive_load_reduction",
                    "current_load": total_load,
                    "load_limit": load_limit,
                    "recommendations": [
                        "Reduce number of concurrent tasks",
                        "Use external aids to reduce cognitive burden",
                        "Prioritize and defer non-essential tasks"
                    ]
                })
        
        return actions
    
    async def _predict_regulation_outcomes(self, regulation_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict outcomes of regulation actions"""
        
        predicted_improvements = {}
        
        for action in regulation_actions:
            if action["type"] == "strategy_change":
                predicted_improvements[action["process"]] = {
                    "efficiency_improvement": 0.2,
                    "confidence": 0.6
                }
            elif action["type"] == "error_reduction":
                predicted_improvements[action["process"]] = {
                    "error_reduction": 0.5,
                    "confidence": 0.7
                }
            elif action["type"] == "global_performance_boost":
                predicted_improvements["overall"] = {
                    "performance_improvement": 0.15,
                    "confidence": 0.5
                }
        
        return predicted_improvements
    
    async def _adjust_monitoring_parameters(self, regulation_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust monitoring parameters based on regulation goals"""
        
        adjustments = {}
        
        # Increase monitoring frequency for processes with improvement goals
        for process_name in regulation_goals:
            if process_name in self.active_monitors:
                adjustments[process_name] = {
                    "monitoring_frequency": "increased",
                    "focus_areas": ["efficiency", "errors", "strategy_effectiveness"]
                }
        
        return adjustments
    
    async def get_metacognitive_status(self) -> Dict[str, Any]:
        """Get current metacognitive system status"""
        
        return {
            "metacognitive_state": self.current_state.value,
            "awareness_level": self.metacognitive_awareness_level,
            "self_regulation_strength": self.self_regulation_strength,
            "active_monitors": len(self.active_monitors),
            "recent_insights": len([insight for insight in self.insights 
                                  if (datetime.now() - insight.timestamp).total_seconds() < 3600]),
            "performance_summary": {
                "monitoring_accuracy": self.metacognitive_performance["monitoring_accuracy"],
                "strategy_effectiveness": self.metacognitive_performance["strategy_effectiveness"],
                "adaptation_success_rate": self.metacognitive_performance["adaptation_success_rate"]
            },
            "metacognitive_style": self.metacognitive_style,
            "recent_regulation_actions": len(self.adaptation_history)
        }