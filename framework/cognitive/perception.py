"""
CollegiumAI Cognitive Architecture - Advanced Perception Module
Multi-modal perception with cognitive filtering and interpretation
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import json
import re

class PerceptionModality(Enum):
    """Different types of perceptual input"""
    TEXTUAL = "textual"
    VISUAL = "visual"
    AUDITORY = "auditory"
    NUMERICAL = "numerical"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    SOCIAL = "social"
    EMOTIONAL = "emotional"

class PerceptionLevel(Enum):
    """Levels of perceptual processing"""
    SENSORY = "sensory"           # Raw input detection
    PATTERN = "pattern"           # Pattern recognition
    SEMANTIC = "semantic"         # Meaning extraction
    PRAGMATIC = "pragmatic"       # Context-aware interpretation

@dataclass
class PerceptualFeature:
    """Represents a perceived feature"""
    modality: PerceptionModality
    level: PerceptionLevel
    content: Any
    confidence: float
    salience: float  # How attention-grabbing this feature is
    timestamp: datetime
    context: Dict[str, Any]

class PerceptionModule:
    """
    Advanced perception module that processes multi-modal input
    with cognitive filtering and contextual interpretation
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"Perception-{persona_type}")
        
        # Perception parameters
        self.perception_threshold = 0.3
        self.salience_weights = self._initialize_salience_weights()
        self.pattern_templates = self._load_pattern_templates()
        self.semantic_networks = {}
        
        # Working memory connection
        self.working_memory = None
        
        # Perceptual history for context
        self.perceptual_history = []
        
    def _initialize_salience_weights(self) -> Dict[PerceptionModality, float]:
        """Initialize salience weights based on persona type"""
        base_weights = {
            PerceptionModality.TEXTUAL: 0.8,
            PerceptionModality.NUMERICAL: 0.6,
            PerceptionModality.TEMPORAL: 0.5,
            PerceptionModality.SPATIAL: 0.4,
            PerceptionModality.SOCIAL: 0.6,
            PerceptionModality.EMOTIONAL: 0.5,
            PerceptionModality.VISUAL: 0.3,
            PerceptionModality.AUDITORY: 0.3
        }
        
        # Adjust based on persona
        if "student" in self.persona_type.lower():
            base_weights[PerceptionModality.TEXTUAL] = 0.9
            base_weights[PerceptionModality.TEMPORAL] = 0.7
            base_weights[PerceptionModality.EMOTIONAL] = 0.6
        elif "faculty" in self.persona_type.lower():
            base_weights[PerceptionModality.TEXTUAL] = 0.9
            base_weights[PerceptionModality.NUMERICAL] = 0.8
            base_weights[PerceptionModality.SOCIAL] = 0.7
        elif "advisor" in self.persona_type.lower():
            base_weights[PerceptionModality.SOCIAL] = 0.9
            base_weights[PerceptionModality.EMOTIONAL] = 0.8
            base_weights[PerceptionModality.TEXTUAL] = 0.8
        elif "administrator" in self.persona_type.lower():
            base_weights[PerceptionModality.NUMERICAL] = 0.9
            base_weights[PerceptionModality.TEMPORAL] = 0.8
            base_weights[PerceptionModality.SOCIAL] = 0.7
        
        return base_weights
    
    def _load_pattern_templates(self) -> Dict[str, Any]:
        """Load persona-specific pattern templates"""
        templates = {
            "academic_patterns": [
                r"(?i)(gpa|grade|score|performance|academic)",
                r"(?i)(course|class|subject|curriculum|syllabus)",
                r"(?i)(assignment|homework|project|exam|test)",
                r"(?i)(research|study|paper|thesis|dissertation)"
            ],
            "emotional_patterns": [
                r"(?i)(stress|anxiety|worry|concern|fear)",
                r"(?i)(happy|excited|confident|motivated)",
                r"(?i)(frustrated|confused|lost|overwhelmed)",
                r"(?i)(help|support|assistance|guidance)"
            ],
            "temporal_patterns": [
                r"(?i)(deadline|due date|schedule|timeline)",
                r"(?i)(urgent|asap|immediately|soon)",
                r"(?i)(semester|quarter|year|month|week)",
                r"(?i)(before|after|during|while)"
            ],
            "social_patterns": [
                r"(?i)(team|group|collaboration|partner)",
                r"(?i)(meeting|discussion|conference|seminar)",
                r"(?i)(professor|advisor|counselor|peer)",
                r"(?i)(community|network|relationship)"
            ]
        }
        
        return templates
    
    def connect_to_memory(self, working_memory):
        """Connect to working memory system"""
        self.working_memory = working_memory
    
    async def process_multimodal_input(self, input_data: Dict[str, Any], cognitive_state) -> Dict[str, Any]:
        """Process multi-modal input through all perception levels"""
        
        perceived_features = []
        
        # Level 1: Sensory Processing
        sensory_features = await self._sensory_processing(input_data)
        perceived_features.extend(sensory_features)
        
        # Level 2: Pattern Recognition
        pattern_features = await self._pattern_recognition(sensory_features)
        perceived_features.extend(pattern_features)
        
        # Level 3: Semantic Processing
        semantic_features = await self._semantic_processing(pattern_features, cognitive_state)
        perceived_features.extend(semantic_features)
        
        # Level 4: Pragmatic Interpretation
        pragmatic_features = await self._pragmatic_interpretation(semantic_features, cognitive_state)
        perceived_features.extend(pragmatic_features)
        
        # Filter by salience and attention
        salient_features = await self._salience_filtering(perceived_features, cognitive_state)
        
        # Update perceptual history
        self.perceptual_history.append({
            "timestamp": datetime.now(),
            "input_data": input_data,
            "perceived_features": salient_features,
            "cognitive_state": cognitive_state
        })
        
        # Keep only recent history
        if len(self.perceptual_history) > 100:
            self.perceptual_history = self.perceptual_history[-100:]
        
        return {
            "perceived_features": salient_features,
            "feature_count": len(salient_features),
            "processing_summary": self._generate_processing_summary(salient_features),
            "contextual_cues": await self._extract_contextual_cues(salient_features)
        }
    
    async def _sensory_processing(self, input_data: Dict[str, Any]) -> List[PerceptualFeature]:
        """Basic sensory-level processing"""
        features = []
        
        # Process textual input
        if "text" in input_data or "message" in input_data or "query" in input_data:
            text_content = input_data.get("text") or input_data.get("message") or input_data.get("query", "")
            if text_content:
                features.append(PerceptualFeature(
                    modality=PerceptionModality.TEXTUAL,
                    level=PerceptionLevel.SENSORY,
                    content=text_content,
                    confidence=0.9,
                    salience=self._calculate_text_salience(text_content),
                    timestamp=datetime.now(),
                    context={"input_type": "textual", "length": len(text_content)}
                ))
        
        # Process numerical data
        numerical_data = self._extract_numerical_data(input_data)
        if numerical_data:
            features.append(PerceptualFeature(
                modality=PerceptionModality.NUMERICAL,
                level=PerceptionLevel.SENSORY,
                content=numerical_data,
                confidence=0.8,
                salience=self._calculate_numerical_salience(numerical_data),
                timestamp=datetime.now(),
                context={"data_type": "numerical", "count": len(numerical_data)}
            ))
        
        # Process temporal information
        temporal_data = self._extract_temporal_data(input_data)
        if temporal_data:
            features.append(PerceptualFeature(
                modality=PerceptionModality.TEMPORAL,
                level=PerceptionLevel.SENSORY,
                content=temporal_data,
                confidence=0.7,
                salience=self._calculate_temporal_salience(temporal_data),
                timestamp=datetime.now(),
                context={"temporal_type": "timestamp_or_duration"}
            ))
        
        # Process social cues
        social_data = self._extract_social_cues(input_data)
        if social_data:
            features.append(PerceptualFeature(
                modality=PerceptionModality.SOCIAL,
                level=PerceptionLevel.SENSORY,
                content=social_data,
                confidence=0.6,
                salience=self._calculate_social_salience(social_data),
                timestamp=datetime.now(),
                context={"social_type": "interpersonal_or_collaborative"}
            ))
        
        return features
    
    async def _pattern_recognition(self, sensory_features: List[PerceptualFeature]) -> List[PerceptualFeature]:
        """Pattern-level processing"""
        pattern_features = []
        
        for feature in sensory_features:
            if feature.modality == PerceptionModality.TEXTUAL:
                # Recognize academic patterns
                academic_patterns = self._recognize_academic_patterns(feature.content)
                if academic_patterns:
                    pattern_features.append(PerceptualFeature(
                        modality=PerceptionModality.TEXTUAL,
                        level=PerceptionLevel.PATTERN,
                        content=academic_patterns,
                        confidence=0.8,
                        salience=feature.salience * 1.2,
                        timestamp=datetime.now(),
                        context={"pattern_type": "academic", "source_feature": feature}
                    ))
                
                # Recognize emotional patterns
                emotional_patterns = self._recognize_emotional_patterns(feature.content)
                if emotional_patterns:
                    pattern_features.append(PerceptualFeature(
                        modality=PerceptionModality.EMOTIONAL,
                        level=PerceptionLevel.PATTERN,
                        content=emotional_patterns,
                        confidence=0.7,
                        salience=feature.salience * 1.1,
                        timestamp=datetime.now(),
                        context={"pattern_type": "emotional", "source_feature": feature}
                    ))
                
                # Recognize temporal patterns
                temporal_patterns = self._recognize_temporal_patterns(feature.content)
                if temporal_patterns:
                    pattern_features.append(PerceptualFeature(
                        modality=PerceptionModality.TEMPORAL,
                        level=PerceptionLevel.PATTERN,
                        content=temporal_patterns,
                        confidence=0.7,
                        salience=feature.salience * 1.1,
                        timestamp=datetime.now(),
                        context={"pattern_type": "temporal", "source_feature": feature}
                    ))
            
            elif feature.modality == PerceptionModality.NUMERICAL:
                # Recognize numerical patterns (trends, outliers, distributions)
                numerical_patterns = self._recognize_numerical_patterns(feature.content)
                if numerical_patterns:
                    pattern_features.append(PerceptualFeature(
                        modality=PerceptionModality.NUMERICAL,
                        level=PerceptionLevel.PATTERN,
                        content=numerical_patterns,
                        confidence=0.8,
                        salience=feature.salience * 1.2,
                        timestamp=datetime.now(),
                        context={"pattern_type": "numerical", "source_feature": feature}
                    ))
        
        return pattern_features
    
    async def _semantic_processing(self, pattern_features: List[PerceptualFeature], cognitive_state) -> List[PerceptualFeature]:
        """Semantic-level processing - extract meaning"""
        semantic_features = []
        
        for feature in pattern_features:
            if feature.level == PerceptionLevel.PATTERN:
                # Extract semantic meaning based on pattern type
                if feature.context.get("pattern_type") == "academic":
                    semantic_meaning = await self._extract_academic_semantics(feature.content, cognitive_state)
                    if semantic_meaning:
                        semantic_features.append(PerceptualFeature(
                            modality=feature.modality,
                            level=PerceptionLevel.SEMANTIC,
                            content=semantic_meaning,
                            confidence=feature.confidence * 0.9,
                            salience=feature.salience * 1.3,
                            timestamp=datetime.now(),
                            context={"semantic_type": "academic_meaning", "source_pattern": feature}
                        ))
                
                elif feature.context.get("pattern_type") == "emotional":
                    emotional_semantics = await self._extract_emotional_semantics(feature.content, cognitive_state)
                    if emotional_semantics:
                        semantic_features.append(PerceptualFeature(
                            modality=PerceptionModality.EMOTIONAL,
                            level=PerceptionLevel.SEMANTIC,
                            content=emotional_semantics,
                            confidence=feature.confidence * 0.8,
                            salience=feature.salience * 1.4,  # Emotional semantics are highly salient
                            timestamp=datetime.now(),
                            context={"semantic_type": "emotional_meaning", "source_pattern": feature}
                        ))
                
                elif feature.context.get("pattern_type") == "temporal":
                    temporal_semantics = await self._extract_temporal_semantics(feature.content, cognitive_state)
                    if temporal_semantics:
                        semantic_features.append(PerceptualFeature(
                            modality=PerceptionModality.TEMPORAL,
                            level=PerceptionLevel.SEMANTIC,
                            content=temporal_semantics,
                            confidence=feature.confidence * 0.9,
                            salience=feature.salience * 1.2,
                            timestamp=datetime.now(),
                            context={"semantic_type": "temporal_meaning", "source_pattern": feature}
                        ))
        
        return semantic_features
    
    async def _pragmatic_interpretation(self, semantic_features: List[PerceptualFeature], cognitive_state) -> List[PerceptualFeature]:
        """Pragmatic-level processing - contextual interpretation"""
        pragmatic_features = []
        
        # Combine semantic features for pragmatic interpretation
        combined_semantics = {}
        for feature in semantic_features:
            modality_key = feature.modality.value
            if modality_key not in combined_semantics:
                combined_semantics[modality_key] = []
            combined_semantics[modality_key].append(feature)
        
        # Generate pragmatic interpretations
        if "textual" in combined_semantics or "emotional" in combined_semantics:
            # Interpret intent and goals
            intent_interpretation = await self._interpret_user_intent(combined_semantics, cognitive_state)
            if intent_interpretation:
                pragmatic_features.append(PerceptualFeature(
                    modality=PerceptionModality.SOCIAL,  # Intent is fundamentally social
                    level=PerceptionLevel.PRAGMATIC,
                    content=intent_interpretation,
                    confidence=0.7,
                    salience=1.0,  # User intent is always highly salient
                    timestamp=datetime.now(),
                    context={"pragmatic_type": "user_intent", "source_semantics": combined_semantics}
                ))
        
        # Interpret urgency and priority
        if "temporal" in combined_semantics or "emotional" in combined_semantics:
            urgency_interpretation = await self._interpret_urgency(combined_semantics, cognitive_state)
            if urgency_interpretation:
                pragmatic_features.append(PerceptualFeature(
                    modality=PerceptionModality.TEMPORAL,
                    level=PerceptionLevel.PRAGMATIC,
                    content=urgency_interpretation,
                    confidence=0.8,
                    salience=urgency_interpretation.get("urgency_level", 0.5),
                    timestamp=datetime.now(),
                    context={"pragmatic_type": "urgency_assessment", "source_semantics": combined_semantics}
                ))
        
        # Interpret support needs
        if any(modality in combined_semantics for modality in ["textual", "emotional", "social"]):
            support_interpretation = await self._interpret_support_needs(combined_semantics, cognitive_state)
            if support_interpretation:
                pragmatic_features.append(PerceptualFeature(
                    modality=PerceptionModality.SOCIAL,
                    level=PerceptionLevel.PRAGMATIC,
                    content=support_interpretation,
                    confidence=0.8,
                    salience=support_interpretation.get("support_urgency", 0.6),
                    timestamp=datetime.now(),
                    context={"pragmatic_type": "support_needs", "source_semantics": combined_semantics}
                ))
        
        return pragmatic_features
    
    async def _salience_filtering(self, all_features: List[PerceptualFeature], cognitive_state) -> List[PerceptualFeature]:
        """Filter features by salience and attention capacity"""
        
        # Calculate attention capacity
        attention_capacity = cognitive_state.get_cognitive_capacity()
        max_features = int(attention_capacity * 10)  # Scale to reasonable number
        
        # Weight salience by modality preferences
        weighted_features = []
        for feature in all_features:
            modality_weight = self.salience_weights.get(feature.modality, 0.5)
            weighted_salience = feature.salience * modality_weight
            
            # Boost salience for pragmatic-level features
            if feature.level == PerceptionLevel.PRAGMATIC:
                weighted_salience *= 1.5
            
            weighted_features.append((feature, weighted_salience))
        
        # Sort by weighted salience and take top features
        weighted_features.sort(key=lambda x: x[1], reverse=True)
        selected_features = [f[0] for f in weighted_features[:max_features]]
        
        return selected_features
    
    # Helper methods for pattern recognition and semantic extraction
    
    def _calculate_text_salience(self, text: str) -> float:
        """Calculate salience of text content"""
        # Factors: length, emotional words, question marks, urgency indicators
        base_salience = min(1.0, len(text) / 100)  # Longer text is more salient up to a point
        
        # Boost for emotional indicators
        emotional_words = ["urgent", "help", "problem", "issue", "concern", "worried", "excited", "happy", "frustrated"]
        emotional_count = sum(1 for word in emotional_words if word.lower() in text.lower())
        emotional_boost = min(0.3, emotional_count * 0.1)
        
        # Boost for questions
        question_boost = 0.2 if "?" in text else 0.0
        
        # Boost for urgency indicators
        urgency_words = ["asap", "immediately", "urgent", "deadline", "due"]
        urgency_boost = 0.3 if any(word.lower() in text.lower() for word in urgency_words) else 0.0
        
        return min(1.0, base_salience + emotional_boost + question_boost + urgency_boost)
    
    def _calculate_numerical_salience(self, numerical_data: Dict[str, Any]) -> float:
        """Calculate salience of numerical data"""
        # Factors: outliers, trends, significant values
        values = numerical_data.get("values", [])
        if not values:
            return 0.3
        
        # Check for outliers or extreme values
        if len(values) > 1:
            mean_val = np.mean(values)
            std_val = np.std(values)
            outlier_count = sum(1 for v in values if abs(v - mean_val) > 2 * std_val)
            outlier_salience = min(0.4, outlier_count * 0.2)
        else:
            outlier_salience = 0.0
        
        return min(1.0, 0.5 + outlier_salience)
    
    def _calculate_temporal_salience(self, temporal_data: Dict[str, Any]) -> float:
        """Calculate salience of temporal information"""
        # Factors: proximity to now, deadlines, duration
        base_salience = 0.5
        
        # Boost for near-term deadlines
        if "deadline" in temporal_data:
            deadline_boost = 0.4
        else:
            deadline_boost = 0.0
        
        # Boost for current/immediate timeframes
        current_boost = 0.3 if any(word in str(temporal_data).lower() for word in ["now", "today", "immediately"]) else 0.0
        
        return min(1.0, base_salience + deadline_boost + current_boost)
    
    def _calculate_social_salience(self, social_data: Dict[str, Any]) -> float:
        """Calculate salience of social information"""
        # Factors: collaboration indicators, interpersonal relationships, authority figures
        base_salience = 0.4
        
        # Boost for authority figures
        authority_boost = 0.3 if any(word in str(social_data).lower() for word in ["professor", "advisor", "dean", "boss"]) else 0.0
        
        # Boost for collaboration
        collab_boost = 0.2 if any(word in str(social_data).lower() for word in ["team", "group", "together", "collaboration"]) else 0.0
        
        return min(1.0, base_salience + authority_boost + collab_boost)
    
    def _extract_numerical_data(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract numerical data from input"""
        numerical_data = {}
        
        # Look for explicit numerical fields
        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                if "values" not in numerical_data:
                    numerical_data["values"] = []
                numerical_data["values"].append(value)
                numerical_data[key] = value
        
        # Extract numbers from text
        if "text" in input_data or "message" in input_data:
            text = input_data.get("text") or input_data.get("message", "")
            numbers = re.findall(r'\d+\.?\d*', text)
            if numbers:
                numerical_data["extracted_numbers"] = [float(n) for n in numbers]
                if "values" not in numerical_data:
                    numerical_data["values"] = []
                numerical_data["values"].extend([float(n) for n in numbers])
        
        return numerical_data if numerical_data else None
    
    def _extract_temporal_data(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract temporal information from input"""
        temporal_data = {}
        
        # Look for explicit temporal fields
        temporal_fields = ["timestamp", "deadline", "due_date", "schedule", "time", "date"]
        for field in temporal_fields:
            if field in input_data:
                temporal_data[field] = input_data[field]
        
        # Extract temporal expressions from text
        if "text" in input_data or "message" in input_data:
            text = input_data.get("text") or input_data.get("message", "")
            
            # Look for temporal keywords
            temporal_keywords = ["today", "tomorrow", "yesterday", "week", "month", "year", "deadline", "due", "schedule"]
            found_keywords = [word for word in temporal_keywords if word.lower() in text.lower()]
            if found_keywords:
                temporal_data["temporal_keywords"] = found_keywords
        
        return temporal_data if temporal_data else None
    
    def _extract_social_cues(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract social cues from input"""
        social_data = {}
        
        # Look for explicit social fields
        social_fields = ["user_id", "sender", "recipient", "team", "group", "collaboration"]
        for field in social_fields:
            if field in input_data:
                social_data[field] = input_data[field]
        
        # Extract social cues from text
        if "text" in input_data or "message" in input_data:
            text = input_data.get("text") or input_data.get("message", "")
            
            # Look for social keywords
            social_keywords = ["we", "us", "team", "group", "together", "collaborate", "professor", "advisor", "peer"]
            found_keywords = [word for word in social_keywords if word.lower() in text.lower()]
            if found_keywords:
                social_data["social_keywords"] = found_keywords
        
        return social_data if social_data else None
    
    def _recognize_academic_patterns(self, text: str) -> Optional[Dict[str, Any]]:
        """Recognize academic patterns in text"""
        patterns = {}
        
        for pattern in self.pattern_templates["academic_patterns"]:
            matches = re.findall(pattern, text)
            if matches:
                patterns[pattern] = matches
        
        return patterns if patterns else None
    
    def _recognize_emotional_patterns(self, text: str) -> Optional[Dict[str, Any]]:
        """Recognize emotional patterns in text"""
        patterns = {}
        
        for pattern in self.pattern_templates["emotional_patterns"]:
            matches = re.findall(pattern, text)
            if matches:
                patterns[pattern] = matches
        
        return patterns if patterns else None
    
    def _recognize_temporal_patterns(self, text: str) -> Optional[Dict[str, Any]]:
        """Recognize temporal patterns in text"""
        patterns = {}
        
        for pattern in self.pattern_templates["temporal_patterns"]:
            matches = re.findall(pattern, text)
            if matches:
                patterns[pattern] = matches
        
        return patterns if patterns else None
    
    def _recognize_numerical_patterns(self, numerical_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Recognize patterns in numerical data"""
        patterns = {}
        values = numerical_data.get("values", [])
        
        if len(values) < 2:
            return None
        
        # Trend analysis
        if len(values) >= 3:
            diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
            if all(d > 0 for d in diffs):
                patterns["trend"] = "increasing"
            elif all(d < 0 for d in diffs):
                patterns["trend"] = "decreasing"
            else:
                patterns["trend"] = "mixed"
        
        # Outlier detection
        mean_val = np.mean(values)
        std_val = np.std(values)
        outliers = [v for v in values if abs(v - mean_val) > 2 * std_val]
        if outliers:
            patterns["outliers"] = outliers
        
        return patterns if patterns else None
    
    async def _extract_academic_semantics(self, patterns: Dict[str, Any], cognitive_state) -> Optional[Dict[str, Any]]:
        """Extract semantic meaning from academic patterns"""
        semantics = {}
        
        # Determine academic domain
        if any("gpa" in str(p).lower() or "grade" in str(p).lower() for p in patterns.values()):
            semantics["domain"] = "academic_performance"
            semantics["concern_level"] = "high"
        elif any("course" in str(p).lower() or "class" in str(p).lower() for p in patterns.values()):
            semantics["domain"] = "curriculum"
            semantics["concern_level"] = "medium"
        elif any("research" in str(p).lower() or "thesis" in str(p).lower() for p in patterns.values()):
            semantics["domain"] = "research"
            semantics["concern_level"] = "medium"
        
        return semantics if semantics else None
    
    async def _extract_emotional_semantics(self, patterns: Dict[str, Any], cognitive_state) -> Optional[Dict[str, Any]]:
        """Extract semantic meaning from emotional patterns"""
        semantics = {}
        
        # Determine emotional valence
        positive_emotions = ["happy", "excited", "confident", "motivated"]
        negative_emotions = ["stress", "anxiety", "worry", "frustrated", "confused", "overwhelmed"]
        
        pattern_text = str(patterns).lower()
        
        positive_count = sum(1 for emotion in positive_emotions if emotion in pattern_text)
        negative_count = sum(1 for emotion in negative_emotions if emotion in pattern_text)
        
        if negative_count > positive_count:
            semantics["valence"] = "negative"
            semantics["intensity"] = min(1.0, negative_count * 0.3)
            semantics["support_needed"] = True
        elif positive_count > negative_count:
            semantics["valence"] = "positive"
            semantics["intensity"] = min(1.0, positive_count * 0.3)
            semantics["support_needed"] = False
        
        return semantics if semantics else None
    
    async def _extract_temporal_semantics(self, patterns: Dict[str, Any], cognitive_state) -> Optional[Dict[str, Any]]:
        """Extract semantic meaning from temporal patterns"""
        semantics = {}
        
        pattern_text = str(patterns).lower()
        
        # Determine urgency
        if any(word in pattern_text for word in ["urgent", "asap", "immediately", "deadline"]):
            semantics["urgency"] = "high"
            semantics["time_pressure"] = True
        elif any(word in pattern_text for word in ["soon", "week", "month"]):
            semantics["urgency"] = "medium"
            semantics["time_pressure"] = False
        else:
            semantics["urgency"] = "low"
            semantics["time_pressure"] = False
        
        return semantics if semantics else None
    
    async def _interpret_user_intent(self, combined_semantics: Dict[str, List], cognitive_state) -> Optional[Dict[str, Any]]:
        """Interpret user's intent from combined semantic features"""
        intent = {}
        
        # Check for help-seeking intent
        if "emotional" in combined_semantics:
            for feature in combined_semantics["emotional"]:
                if feature.content.get("support_needed"):
                    intent["type"] = "help_seeking"
                    intent["domain"] = "emotional_support"
                    intent["urgency"] = feature.content.get("intensity", 0.5)
                    break
        
        # Check for information-seeking intent
        if "textual" in combined_semantics:
            for feature in combined_semantics["textual"]:
                if "academic" in str(feature.content).lower():
                    intent["type"] = "information_seeking"
                    intent["domain"] = "academic"
                    break
        
        return intent if intent else None
    
    async def _interpret_urgency(self, combined_semantics: Dict[str, List], cognitive_state) -> Optional[Dict[str, Any]]:
        """Interpret urgency level from combined semantic features"""
        urgency = {"urgency_level": 0.3}  # Default low urgency
        
        # Check temporal urgency
        if "temporal" in combined_semantics:
            for feature in combined_semantics["temporal"]:
                temporal_urgency = feature.content.get("urgency", "low")
                if temporal_urgency == "high":
                    urgency["urgency_level"] = 0.9
                    urgency["source"] = "temporal"
                elif temporal_urgency == "medium":
                    urgency["urgency_level"] = max(urgency["urgency_level"], 0.6)
                    urgency["source"] = "temporal"
        
        # Check emotional urgency
        if "emotional" in combined_semantics:
            for feature in combined_semantics["emotional"]:
                emotional_intensity = feature.content.get("intensity", 0.3)
                if emotional_intensity > 0.7:
                    urgency["urgency_level"] = max(urgency["urgency_level"], 0.8)
                    urgency["source"] = "emotional"
        
        return urgency
    
    async def _interpret_support_needs(self, combined_semantics: Dict[str, List], cognitive_state) -> Optional[Dict[str, Any]]:
        """Interpret what kind of support is needed"""
        support = {}
        
        # Determine support type
        if "emotional" in combined_semantics:
            for feature in combined_semantics["emotional"]:
                if feature.content.get("support_needed"):
                    support["type"] = "emotional_support"
                    support["support_urgency"] = feature.content.get("intensity", 0.5)
        
        if "textual" in combined_semantics:
            for feature in combined_semantics["textual"]:
                content_str = str(feature.content).lower()
                if "academic" in content_str:
                    support["type"] = "academic_support"
                    support["support_urgency"] = 0.6
                elif "career" in content_str:
                    support["type"] = "career_support"
                    support["support_urgency"] = 0.5
        
        return support if support else None
    
    def _generate_processing_summary(self, features: List[PerceptualFeature]) -> Dict[str, Any]:
        """Generate a summary of perceptual processing"""
        summary = {
            "total_features": len(features),
            "modalities": {},
            "levels": {},
            "average_confidence": 0.0,
            "average_salience": 0.0
        }
        
        if not features:
            return summary
        
        # Count by modality and level
        for feature in features:
            modality = feature.modality.value
            level = feature.level.value
            
            summary["modalities"][modality] = summary["modalities"].get(modality, 0) + 1
            summary["levels"][level] = summary["levels"].get(level, 0) + 1
        
        # Calculate averages
        summary["average_confidence"] = np.mean([f.confidence for f in features])
        summary["average_salience"] = np.mean([f.salience for f in features])
        
        return summary
    
    async def _extract_contextual_cues(self, features: List[PerceptualFeature]) -> Dict[str, Any]:
        """Extract contextual cues for downstream processing"""
        cues = {
            "dominant_modality": None,
            "processing_complexity": "low",
            "attention_demands": "moderate",
            "emotional_state": "neutral",
            "temporal_pressure": False,
            "social_context": False
        }
        
        if not features:
            return cues
        
        # Determine dominant modality
        modality_counts = {}
        for feature in features:
            modality = feature.modality.value
            modality_counts[modality] = modality_counts.get(modality, 0) + 1
        
        if modality_counts:
            cues["dominant_modality"] = max(modality_counts, key=modality_counts.get)
        
        # Assess processing complexity
        pragmatic_features = [f for f in features if f.level == PerceptionLevel.PRAGMATIC]
        if len(pragmatic_features) > 2:
            cues["processing_complexity"] = "high"
        elif len(pragmatic_features) > 0:
            cues["processing_complexity"] = "medium"
        
        # Assess attention demands
        high_salience_features = [f for f in features if f.salience > 0.7]
        if len(high_salience_features) > 3:
            cues["attention_demands"] = "high"
        elif len(high_salience_features) > 1:
            cues["attention_demands"] = "moderate"
        
        # Detect emotional state
        emotional_features = [f for f in features if f.modality == PerceptionModality.EMOTIONAL]
        if emotional_features:
            negative_emotions = sum(1 for f in emotional_features 
                                  if f.content and f.content.get("valence") == "negative")
            positive_emotions = sum(1 for f in emotional_features 
                                  if f.content and f.content.get("valence") == "positive")
            
            if negative_emotions > positive_emotions:
                cues["emotional_state"] = "negative"
            elif positive_emotions > negative_emotions:
                cues["emotional_state"] = "positive"
        
        # Detect temporal pressure
        temporal_features = [f for f in features if f.modality == PerceptionModality.TEMPORAL]
        if any(f.content and f.content.get("urgency") == "high" for f in temporal_features):
            cues["temporal_pressure"] = True
        
        # Detect social context
        social_features = [f for f in features if f.modality == PerceptionModality.SOCIAL]
        if social_features:
            cues["social_context"] = True
        
        return cues


class MultiModalPerception:
    """
    Advanced multi-modal perception system that integrates multiple
    perception modules for comprehensive environmental understanding
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.primary_perception = PerceptionModule(persona_type)
        self.specialized_modules = {}
        self.integration_weights = {}
        
    async def add_specialized_module(self, modality: PerceptionModality, module: PerceptionModule, weight: float = 1.0):
        """Add a specialized perception module for a specific modality"""
        self.specialized_modules[modality] = module
        self.integration_weights[modality] = weight
    
    async def process_integrated_perception(self, input_data: Dict[str, Any], cognitive_state) -> Dict[str, Any]:
        """Process input through all perception modules and integrate results"""
        
        # Primary perception processing
        primary_result = await self.primary_perception.process_multimodal_input(input_data, cognitive_state)
        
        # Specialized module processing
        specialized_results = {}
        for modality, module in self.specialized_modules.items():
            try:
                result = await module.process_multimodal_input(input_data, cognitive_state)
                specialized_results[modality.value] = result
            except Exception as e:
                logging.error(f"Specialized perception module {modality} error: {e}")
        
        # Integrate results
        integrated_result = await self._integrate_perception_results(
            primary_result, specialized_results, cognitive_state
        )
        
        return integrated_result
    
    async def _integrate_perception_results(self, primary: Dict[str, Any], 
                                         specialized: Dict[str, Any], 
                                         cognitive_state) -> Dict[str, Any]:
        """Integrate results from multiple perception modules"""
        
        # Start with primary results
        integrated_features = primary.get("perceived_features", [])
        
        # Add specialized features with appropriate weighting
        for modality_name, result in specialized.items():
            weight = self.integration_weights.get(PerceptionModality(modality_name), 1.0)
            specialized_features = result.get("perceived_features", [])
            
            # Apply weight to salience
            for feature in specialized_features:
                feature.salience *= weight
            
            integrated_features.extend(specialized_features)
        
        # Remove duplicates and apply final filtering
        unique_features = await self._remove_duplicate_features(integrated_features)
        final_features = await self.primary_perception._salience_filtering(unique_features, cognitive_state)
        
        return {
            "perceived_features": final_features,
            "integration_summary": {
                "primary_features": len(primary.get("perceived_features", [])),
                "specialized_features": {k: len(v.get("perceived_features", [])) for k, v in specialized.items()},
                "final_features": len(final_features)
            },
            "processing_summary": self.primary_perception._generate_processing_summary(final_features),
            "contextual_cues": await self.primary_perception._extract_contextual_cues(final_features)
        }
    
    async def _remove_duplicate_features(self, features: List[PerceptualFeature]) -> List[PerceptualFeature]:
        """Remove duplicate or highly similar features"""
        unique_features = []
        
        for feature in features:
            is_duplicate = False
            for existing in unique_features:
                if (feature.modality == existing.modality and 
                    feature.level == existing.level and
                    self._calculate_feature_similarity(feature, existing) > 0.8):
                    is_duplicate = True
                    # Keep the feature with higher salience
                    if feature.salience > existing.salience:
                        unique_features.remove(existing)
                        unique_features.append(feature)
                    break
            
            if not is_duplicate:
                unique_features.append(feature)
        
        return unique_features
    
    def _calculate_feature_similarity(self, feature1: PerceptualFeature, feature2: PerceptualFeature) -> float:
        """Calculate similarity between two perceptual features"""
        # Simple similarity based on content overlap
        content1_str = str(feature1.content).lower()
        content2_str = str(feature2.content).lower()
        
        # Jaccard similarity for basic comparison
        words1 = set(content1_str.split())
        words2 = set(content2_str.split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0