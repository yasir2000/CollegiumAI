"""
CollegiumAI Cognitive Architecture - Advanced Memory Systems
Multi-layered memory with working, episodic, and semantic components
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
from collections import defaultdict, deque
import heapq

class MemoryType(Enum):
    """Types of memory systems"""
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    SENSORY = "sensory"

class MemoryStrength(Enum):
    """Memory consolidation strength levels"""
    WEAK = 0.2
    MODERATE = 0.5
    STRONG = 0.8
    PERMANENT = 1.0

@dataclass
class MemoryTrace:
    """Individual memory trace"""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Any = None
    memory_type: MemoryType = MemoryType.WORKING
    strength: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    associations: List[str] = field(default_factory=list)  # IDs of related memories
    context: Dict[str, Any] = field(default_factory=dict)
    decay_rate: float = 0.1  # How fast this memory decays
    
    def access(self):
        """Record memory access"""
        self.last_accessed = datetime.now()
        self.access_count += 1
        # Accessing strengthens memory slightly
        self.strength = min(1.0, self.strength + 0.05)
    
    def decay(self, time_passed: float):
        """Apply memory decay over time"""
        decay_factor = np.exp(-self.decay_rate * time_passed)
        self.strength *= decay_factor
        self.strength = max(0.01, self.strength)  # Minimum strength

@dataclass
class Episode:
    """Episodic memory episode"""
    episode_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    outcome: Optional[Dict[str, Any]] = None
    emotional_valence: float = 0.0  # -1 to 1
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    participants: List[str] = field(default_factory=list)
    location: Optional[str] = None
    success_indicator: Optional[bool] = None

class CognitiveMemory:
    """
    Unified cognitive memory system managing all memory types
    Inspired by Atkinson-Shiffrin model and Baddeley's working memory model
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.logger = logging.getLogger(f"CognitiveMemory-{persona_type}")
        
        # Memory subsystems
        self.working_memory = WorkingMemory(persona_type)
        self.episodic_memory = EpisodicMemory(persona_type)
        self.long_term_memory = LongTermMemory(persona_type)
        
        # Memory management parameters
        self.consolidation_threshold = 0.7
        self.decay_update_interval = 3600  # Update decay every hour
        self.last_decay_update = datetime.now()
        
        # Cross-memory associations
        self.memory_associations = defaultdict(list)  # trace_id -> [associated_trace_ids]
        
    async def store_memory(self, content: Any, memory_type: MemoryType, 
                         context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """Store memory in appropriate subsystem"""
        
        if memory_type == MemoryType.WORKING:
            return await self.working_memory.store(content, context, tags)
        elif memory_type == MemoryType.EPISODIC:
            return await self.episodic_memory.store_episode(content, context, tags)
        elif memory_type == MemoryType.SEMANTIC:
            return await self.long_term_memory.store_semantic(content, context, tags)
        else:
            # Default to working memory
            return await self.working_memory.store(content, context, tags)
    
    async def retrieve_memory(self, query: Dict[str, Any], 
                            memory_types: List[MemoryType] = None,
                            similarity_threshold: float = 0.6) -> List[MemoryTrace]:
        """Retrieve memories across subsystems"""
        
        all_memories = []
        target_types = memory_types or [MemoryType.WORKING, MemoryType.EPISODIC, MemoryType.SEMANTIC]
        
        # Search each requested memory type
        for mem_type in target_types:
            if mem_type == MemoryType.WORKING:
                memories = await self.working_memory.retrieve(query, similarity_threshold)
            elif mem_type == MemoryType.EPISODIC:
                memories = await self.episodic_memory.retrieve_similar_episodes(query, similarity_threshold)
            elif mem_type == MemoryType.SEMANTIC:
                memories = await self.long_term_memory.retrieve_relevant_knowledge(query, similarity_threshold)
            else:
                continue
            
            all_memories.extend(memories)
        
        # Sort by relevance and recency
        all_memories.sort(key=lambda m: (m.strength, m.access_count), reverse=True)
        
        return all_memories
    
    async def consolidate_episode(self, episode_data: Dict[str, Any]):
        """Consolidate episode from working memory to long-term memory"""
        
        # Create episode
        episode = Episode(
            context=episode_data.get("context", {}),
            events=episode_data.get("events", []),
            outcome=episode_data.get("outcome"),
            importance=episode_data.get("importance", 0.5),
            tags=episode_data.get("tags", [])
        )
        
        # Store in episodic memory
        episode_id = await self.episodic_memory.store_episode(episode)
        
        # Extract semantic knowledge from episode
        semantic_knowledge = await self._extract_semantic_knowledge(episode)
        if semantic_knowledge:
            await self.long_term_memory.store_semantic(semantic_knowledge, episode.context)
        
        # Clear related items from working memory if successfully consolidated
        if episode.importance > self.consolidation_threshold:
            await self.working_memory.clear_related_items(episode.tags)
        
        return episode_id
    
    async def _extract_semantic_knowledge(self, episode: Episode) -> Optional[Dict[str, Any]]:
        """Extract generalizable knowledge from specific episodes"""
        
        semantic_knowledge = {
            "patterns": [],
            "rules": [],
            "concepts": [],
            "relationships": []
        }
        
        # Extract patterns from successful episodes
        if episode.success_indicator:
            for event in episode.events:
                if event.get("type") == "action" and event.get("outcome") == "positive":
                    semantic_knowledge["patterns"].append({
                        "pattern_type": "successful_action",
                        "action": event.get("action"),
                        "context": event.get("context", {}),
                        "effectiveness": 0.7
                    })
        
        # Extract rules from repeated patterns
        context_type = episode.context.get("type", "general")
        if context_type == "academic":
            semantic_knowledge["rules"].append({
                "rule_type": "academic_guideline",
                "condition": episode.context.get("situation"),
                "action": "systematic_approach",
                "confidence": episode.importance
            })
        
        return semantic_knowledge if any(semantic_knowledge.values()) else None
    
    async def update_memory_strengths(self):
        """Update memory strengths and apply decay"""
        current_time = datetime.now()
        time_since_update = (current_time - self.last_decay_update).total_seconds() / 3600  # hours
        
        if time_since_update >= 1.0:  # Update at least every hour
            await self.working_memory.apply_decay(time_since_update)
            await self.episodic_memory.apply_decay(time_since_update)
            await self.long_term_memory.apply_decay(time_since_update)
            
            self.last_decay_update = current_time
    
    async def create_association(self, trace_id1: str, trace_id2: str, association_strength: float = 0.5):
        """Create association between memory traces"""
        self.memory_associations[trace_id1].append({
            "target_id": trace_id2,
            "strength": association_strength,
            "created_at": datetime.now()
        })
        self.memory_associations[trace_id2].append({
            "target_id": trace_id1,
            "strength": association_strength,
            "created_at": datetime.now()
        })
    
    async def get_memory_status(self) -> Dict[str, Any]:
        """Get overall memory system status"""
        return {
            "working_memory": await self.working_memory.get_status(),
            "episodic_memory": await self.episodic_memory.get_status(),
            "long_term_memory": await self.long_term_memory.get_status(),
            "total_associations": len(self.memory_associations),
            "last_consolidation": self.last_decay_update.isoformat()
        }


class WorkingMemory:
    """
    Working memory system with limited capacity and rapid decay
    Based on Baddeley's model with central executive, phonological loop, and visuospatial sketchpad
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.capacity = self._initialize_capacity()
        self.memories = {}  # trace_id -> MemoryTrace
        self.active_chunk_ids = deque(maxlen=self.capacity)  # Most recently used
        
        # Working memory components
        self.central_executive = []  # Control and coordination
        self.phonological_loop = []  # Verbal/linguistic information
        self.visuospatial_sketchpad = []  # Visual and spatial information
        self.episodic_buffer = []  # Integration of information
        
    def _initialize_capacity(self) -> int:
        """Initialize working memory capacity based on persona type"""
        base_capacity = 7  # Miller's magic number ±2
        
        if "faculty" in self.persona_type.lower() or "researcher" in self.persona_type.lower():
            return base_capacity + 2  # Higher capacity for academics
        elif "student" in self.persona_type.lower():
            return base_capacity  # Standard capacity
        elif "administrator" in self.persona_type.lower():
            return base_capacity + 1  # Slightly higher for complex admin tasks
        else:
            return base_capacity
    
    async def store(self, content: Any, context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """Store item in working memory"""
        
        # Create memory trace
        trace = MemoryTrace(
            content=content,
            memory_type=MemoryType.WORKING,
            strength=0.8,  # Working memory starts strong
            tags=tags or [],
            context=context or {},
            decay_rate=0.3  # Working memory decays faster
        )
        
        # Check capacity and evict if necessary
        if len(self.active_chunk_ids) >= self.capacity:
            await self._evict_oldest()
        
        # Store in appropriate component
        content_type = self._classify_content_type(content)
        if content_type == "verbal":
            self.phonological_loop.append(trace.trace_id)
        elif content_type == "spatial":
            self.visuospatial_sketchpad.append(trace.trace_id)
        elif content_type == "integrated":
            self.episodic_buffer.append(trace.trace_id)
        else:
            self.central_executive.append(trace.trace_id)
        
        # Store memory and update active chunks
        self.memories[trace.trace_id] = trace
        self.active_chunk_ids.append(trace.trace_id)
        
        return trace.trace_id
    
    def _classify_content_type(self, content: Any) -> str:
        """Classify content for appropriate working memory component"""
        content_str = str(content).lower()
        
        if any(word in content_str for word in ["text", "word", "language", "verbal", "speech"]):
            return "verbal"
        elif any(word in content_str for word in ["image", "visual", "spatial", "location", "diagram"]):
            return "spatial"
        elif isinstance(content, dict) and len(content) > 3:
            return "integrated"  # Complex integrated information
        else:
            return "executive"  # Control and coordination
    
    async def retrieve(self, query: Dict[str, Any], similarity_threshold: float = 0.6) -> List[MemoryTrace]:
        """Retrieve items from working memory"""
        
        matching_traces = []
        query_str = str(query).lower()
        
        for trace_id, trace in self.memories.items():
            # Calculate similarity
            similarity = self._calculate_similarity(query, trace)
            
            if similarity >= similarity_threshold:
                trace.access()  # Record access
                matching_traces.append(trace)
                
                # Move to front of active chunks (LRU)
                if trace_id in self.active_chunk_ids:
                    self.active_chunk_ids.remove(trace_id)
                    self.active_chunk_ids.append(trace_id)
        
        # Sort by strength and recency
        matching_traces.sort(key=lambda t: (t.strength, t.access_count), reverse=True)
        
        return matching_traces
    
    def _calculate_similarity(self, query: Dict[str, Any], trace: MemoryTrace) -> float:
        """Calculate similarity between query and memory trace"""
        query_str = str(query).lower()
        content_str = str(trace.content).lower()
        context_str = str(trace.context).lower()
        tags_str = " ".join(trace.tags).lower()
        
        # Simple keyword-based similarity
        query_words = set(query_str.split())
        content_words = set(content_str.split())
        context_words = set(context_str.split())
        tag_words = set(tags_str.split())
        
        all_trace_words = content_words.union(context_words).union(tag_words)
        
        if not query_words or not all_trace_words:
            return 0.0
        
        intersection = len(query_words.intersection(all_trace_words))
        union = len(query_words.union(all_trace_words))
        
        return intersection / union if union > 0 else 0.0
    
    async def update(self, perceived_data: Dict[str, Any], episodic_context: List[Any], semantic_context: List[Any]):
        """Update working memory with new information"""
        
        # Store new perceived data
        await self.store(perceived_data, {"type": "perception"}, ["current", "perception"])
        
        # Store episodic context if relevant
        if episodic_context:
            await self.store(episodic_context, {"type": "episodic_context"}, ["context", "episodic"])
        
        # Store semantic context if relevant  
        if semantic_context:
            await self.store(semantic_context, {"type": "semantic_context"}, ["context", "semantic"])
    
    async def _evict_oldest(self):
        """Evict oldest item from working memory"""
        if self.active_chunk_ids:
            oldest_id = self.active_chunk_ids.popleft()
            if oldest_id in self.memories:
                del self.memories[oldest_id]
                
                # Remove from components
                for component in [self.central_executive, self.phonological_loop, 
                                self.visuospatial_sketchpad, self.episodic_buffer]:
                    if oldest_id in component:
                        component.remove(oldest_id)
    
    async def apply_decay(self, time_hours: float):
        """Apply memory decay to working memory contents"""
        to_remove = []
        
        for trace_id, trace in self.memories.items():
            trace.decay(time_hours)
            
            # Remove very weak memories
            if trace.strength < 0.1:
                to_remove.append(trace_id)
        
        # Remove weak memories
        for trace_id in to_remove:
            if trace_id in self.memories:
                del self.memories[trace_id]
            if trace_id in self.active_chunk_ids:
                self.active_chunk_ids.remove(trace_id)
    
    async def clear_related_items(self, tags: List[str]):
        """Clear items with specific tags (for consolidation)"""
        to_remove = []
        
        for trace_id, trace in self.memories.items():
            if any(tag in trace.tags for tag in tags):
                to_remove.append(trace_id)
        
        for trace_id in to_remove:
            if trace_id in self.memories:
                del self.memories[trace_id]
            if trace_id in self.active_chunk_ids:
                self.active_chunk_ids.remove(trace_id)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current working memory state"""
        return {
            "capacity": self.capacity,
            "current_load": len(self.memories),
            "utilization": len(self.memories) / self.capacity,
            "component_loads": {
                "central_executive": len(self.central_executive),
                "phonological_loop": len(self.phonological_loop),
                "visuospatial_sketchpad": len(self.visuospatial_sketchpad),
                "episodic_buffer": len(self.episodic_buffer)
            },
            "average_strength": np.mean([t.strength for t in self.memories.values()]) if self.memories else 0.0
        }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get working memory status"""
        return {
            "total_items": len(self.memories),
            "capacity_utilization": len(self.memories) / self.capacity,
            "average_strength": np.mean([t.strength for t in self.memories.values()]) if self.memories else 0.0,
            "oldest_item_age": (datetime.now() - min(t.created_at for t in self.memories.values())).total_seconds() / 3600 if self.memories else 0
        }


class EpisodicMemory:
    """
    Episodic memory system for storing and retrieving specific experiences
    Includes temporal organization and contextual retrieval
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.episodes = {}  # episode_id -> Episode
        self.temporal_index = []  # [(timestamp, episode_id), ...] sorted by time
        self.context_index = defaultdict(list)  # context_type -> [episode_ids]
        self.tag_index = defaultdict(list)  # tag -> [episode_ids]
        
        # Episodic memory parameters
        self.max_episodes = 10000  # Maximum episodes to store
        self.importance_threshold = 0.3  # Minimum importance to retain
        
    async def store_episode(self, episode_data: Union[Episode, Dict[str, Any]], 
                          context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """Store an episode in episodic memory"""
        
        if isinstance(episode_data, Episode):
            episode = episode_data
        else:
            episode = Episode(
                context=context or episode_data.get("context", {}),
                events=episode_data.get("events", []),
                outcome=episode_data.get("outcome"),
                importance=episode_data.get("importance", 0.5),
                tags=tags or episode_data.get("tags", [])
            )
        
        # Store episode
        self.episodes[episode.episode_id] = episode
        
        # Update indices
        heapq.heappush(self.temporal_index, (episode.timestamp, episode.episode_id))
        
        context_type = episode.context.get("type", "general")
        self.context_index[context_type].append(episode.episode_id)
        
        for tag in episode.tags:
            self.tag_index[tag].append(episode.episode_id)
        
        # Manage memory capacity
        await self._manage_capacity()
        
        return episode.episode_id
    
    async def retrieve_similar_episodes(self, query: Dict[str, Any], 
                                      similarity_threshold: float = 0.7) -> List[Episode]:
        """Retrieve episodes similar to the query"""
        
        matching_episodes = []
        
        # Extract query features
        query_context = query.get("context", {})
        query_tags = query.get("tags", [])
        query_content = str(query).lower()
        
        for episode in self.episodes.values():
            similarity = await self._calculate_episode_similarity(query, episode)
            
            if similarity >= similarity_threshold:
                matching_episodes.append(episode)
        
        # Sort by similarity and recency
        matching_episodes.sort(key=lambda e: (
            self._calculate_episode_similarity_sync(query, e), 
            e.timestamp
        ), reverse=True)
        
        return matching_episodes
    
    async def _calculate_episode_similarity(self, query: Dict[str, Any], episode: Episode) -> float:
        """Calculate similarity between query and episode"""
        return self._calculate_episode_similarity_sync(query, episode)
    
    def _calculate_episode_similarity_sync(self, query: Dict[str, Any], episode: Episode) -> float:
        """Synchronous version of episode similarity calculation"""
        similarity_score = 0.0
        
        # Context similarity
        query_context = query.get("context", {})
        if query_context and episode.context:
            context_match = sum(1 for k, v in query_context.items() 
                              if k in episode.context and episode.context[k] == v)
            context_total = max(len(query_context), len(episode.context))
            if context_total > 0:
                similarity_score += (context_match / context_total) * 0.4
        
        # Tag similarity
        query_tags = set(query.get("tags", []))
        episode_tags = set(episode.tags)
        if query_tags or episode_tags:
            tag_intersection = len(query_tags.intersection(episode_tags))
            tag_union = len(query_tags.union(episode_tags))
            if tag_union > 0:
                similarity_score += (tag_intersection / tag_union) * 0.3
        
        # Content similarity
        query_str = str(query).lower()
        episode_str = str(episode.events).lower()
        query_words = set(query_str.split())
        episode_words = set(episode_str.split())
        
        if query_words or episode_words:
            word_intersection = len(query_words.intersection(episode_words))
            word_union = len(query_words.union(episode_words))
            if word_union > 0:
                similarity_score += (word_intersection / word_union) * 0.3
        
        return similarity_score
    
    async def retrieve_by_timeframe(self, start_time: datetime, end_time: datetime) -> List[Episode]:
        """Retrieve episodes within a specific timeframe"""
        matching_episodes = []
        
        for timestamp, episode_id in self.temporal_index:
            if start_time <= timestamp <= end_time:
                if episode_id in self.episodes:
                    matching_episodes.append(self.episodes[episode_id])
        
        return matching_episodes
    
    async def retrieve_by_context(self, context_type: str) -> List[Episode]:
        """Retrieve episodes by context type"""
        episode_ids = self.context_index.get(context_type, [])
        return [self.episodes[eid] for eid in episode_ids if eid in self.episodes]
    
    async def retrieve_by_tags(self, tags: List[str]) -> List[Episode]:
        """Retrieve episodes that have any of the specified tags"""
        episode_ids = set()
        for tag in tags:
            episode_ids.update(self.tag_index.get(tag, []))
        
        return [self.episodes[eid] for eid in episode_ids if eid in self.episodes]
    
    async def _manage_capacity(self):
        """Manage episodic memory capacity by removing less important episodes"""
        if len(self.episodes) > self.max_episodes:
            # Sort episodes by importance and recency
            episodes_by_importance = sorted(
                self.episodes.values(),
                key=lambda e: (e.importance, e.timestamp),
                reverse=True
            )
            
            # Keep the most important and recent episodes
            episodes_to_keep = episodes_by_importance[:self.max_episodes]
            episodes_to_remove = set(self.episodes.keys()) - {e.episode_id for e in episodes_to_keep}
            
            # Remove less important episodes
            for episode_id in episodes_to_remove:
                await self._remove_episode(episode_id)
    
    async def _remove_episode(self, episode_id: str):
        """Remove an episode and update all indices"""
        if episode_id not in self.episodes:
            return
        
        episode = self.episodes[episode_id]
        
        # Remove from main storage
        del self.episodes[episode_id]
        
        # Remove from temporal index
        self.temporal_index = [(t, eid) for t, eid in self.temporal_index if eid != episode_id]
        heapq.heapify(self.temporal_index)
        
        # Remove from context index
        context_type = episode.context.get("type", "general")
        if episode_id in self.context_index[context_type]:
            self.context_index[context_type].remove(episode_id)
        
        # Remove from tag index
        for tag in episode.tags:
            if episode_id in self.tag_index[tag]:
                self.tag_index[tag].remove(episode_id)
    
    async def apply_decay(self, time_hours: float):
        """Apply decay to episodic memories based on time and access patterns"""
        decay_factor = 0.95 ** (time_hours / 24)  # Slower decay than working memory
        
        episodes_to_remove = []
        
        for episode in self.episodes.values():
            # Reduce importance over time (unless frequently accessed)
            episode.importance *= decay_factor
            
            # Remove episodes that have decayed below threshold
            if episode.importance < self.importance_threshold:
                episodes_to_remove.append(episode.episode_id)
        
        # Remove decayed episodes
        for episode_id in episodes_to_remove:
            await self._remove_episode(episode_id)
    
    async def get_status(self) -> Dict[str, Any]:
        """Get episodic memory status"""
        if not self.episodes:
            return {
                "total_episodes": 0,
                "average_importance": 0.0,
                "oldest_episode_age": 0,
                "context_types": 0
            }
        
        return {
            "total_episodes": len(self.episodes),
            "average_importance": np.mean([e.importance for e in self.episodes.values()]),
            "oldest_episode_age": (datetime.now() - min(e.timestamp for e in self.episodes.values())).total_seconds() / 3600,
            "context_types": len(self.context_index)
        }


class LongTermMemory:
    """
    Long-term semantic memory system for storing factual knowledge and procedures
    Organized as semantic networks with associative retrieval
    """
    
    def __init__(self, persona_type: str):
        self.persona_type = persona_type
        self.semantic_network = {}  # concept_id -> {content, associations, strength}
        self.concept_index = defaultdict(list)  # keyword -> [concept_ids]
        self.category_index = defaultdict(list)  # category -> [concept_ids]
        
        # Initialize with domain-specific knowledge
        self.domain_knowledge = self._initialize_domain_knowledge()
        
    def _initialize_domain_knowledge(self) -> Dict[str, Any]:
        """Initialize persona-specific domain knowledge"""
        knowledge = {
            "academic_concepts": {
                "gpa": {"definition": "Grade Point Average", "importance": 0.9, "category": "academic_metric"},
                "credit_hours": {"definition": "Academic unit of measurement", "importance": 0.8, "category": "academic_unit"},
                "prerequisite": {"definition": "Required prior course", "importance": 0.8, "category": "academic_requirement"}
            },
            "procedural_knowledge": {
                "course_registration": {
                    "steps": ["check_prerequisites", "verify_schedule", "submit_registration"],
                    "importance": 0.9
                },
                "study_planning": {
                    "steps": ["assess_workload", "create_schedule", "allocate_time", "review_progress"],
                    "importance": 0.8
                }
            }
        }
        
        # Add persona-specific knowledge
        if "student" in self.persona_type.lower():
            knowledge["academic_concepts"].update({
                "study_techniques": {"definition": "Methods for effective learning", "importance": 0.9},
                "time_management": {"definition": "Effective use of available time", "importance": 0.8}
            })
        elif "faculty" in self.persona_type.lower():
            knowledge["academic_concepts"].update({
                "curriculum_design": {"definition": "Process of creating educational programs", "importance": 0.9},
                "assessment_methods": {"definition": "Techniques for evaluating student learning", "importance": 0.8}
            })
        
        return knowledge
    
    async def store_semantic(self, content: Any, context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """Store semantic knowledge in long-term memory"""
        
        concept_id = str(uuid.uuid4())
        
        # Extract keywords for indexing
        keywords = self._extract_keywords(content)
        category = context.get("category", "general") if context else "general"
        
        # Store in semantic network
        self.semantic_network[concept_id] = {
            "content": content,
            "context": context or {},
            "tags": tags or [],
            "keywords": keywords,
            "category": category,
            "strength": 0.8,  # Start with strong long-term memory
            "created_at": datetime.now(),
            "access_count": 0,
            "associations": []
        }
        
        # Update indices
        for keyword in keywords:
            self.concept_index[keyword].append(concept_id)
        
        self.category_index[category].append(concept_id)
        
        # Create associations with existing concepts
        await self._create_semantic_associations(concept_id)
        
        return concept_id
    
    def _extract_keywords(self, content: Any) -> List[str]:
        """Extract keywords from content for indexing"""
        content_str = str(content).lower()
        
        # Simple keyword extraction (in practice, could use NLP techniques)
        words = content_str.split()
        
        # Filter out common words and keep significant terms
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return unique keywords
        return list(set(keywords))
    
    async def _create_semantic_associations(self, concept_id: str):
        """Create associations between the new concept and existing ones"""
        new_concept = self.semantic_network[concept_id]
        new_keywords = set(new_concept["keywords"])
        
        # Find concepts with overlapping keywords
        for existing_id, existing_concept in self.semantic_network.items():
            if existing_id == concept_id:
                continue
            
            existing_keywords = set(existing_concept["keywords"])
            overlap = len(new_keywords.intersection(existing_keywords))
            
            if overlap > 0:
                # Calculate association strength
                association_strength = overlap / len(new_keywords.union(existing_keywords))
                
                if association_strength > 0.2:  # Minimum threshold for association
                    # Create bidirectional association
                    new_concept["associations"].append({
                        "target_id": existing_id,
                        "strength": association_strength,
                        "type": "semantic_similarity"
                    })
                    existing_concept["associations"].append({
                        "target_id": concept_id,
                        "strength": association_strength,
                        "type": "semantic_similarity"
                    })
    
    async def retrieve_relevant_knowledge(self, query: Dict[str, Any], 
                                        activation_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Retrieve relevant knowledge based on spreading activation"""
        
        # Extract query keywords
        query_keywords = self._extract_keywords(str(query))
        
        # Initial activation based on keyword matches
        activated_concepts = {}
        
        for keyword in query_keywords:
            concept_ids = self.concept_index.get(keyword, [])
            for concept_id in concept_ids:
                if concept_id not in activated_concepts:
                    activated_concepts[concept_id] = 0.0
                activated_concepts[concept_id] += 0.3  # Base activation per keyword match
        
        # Spreading activation through associations
        for _ in range(3):  # 3 levels of spreading
            new_activations = activated_concepts.copy()
            
            for concept_id, activation in activated_concepts.items():
                if activation > 0.1:  # Only spread from sufficiently activated concepts
                    concept = self.semantic_network.get(concept_id, {})
                    
                    for association in concept.get("associations", []):
                        target_id = association["target_id"]
                        spread_amount = activation * association["strength"] * 0.5
                        
                        if target_id not in new_activations:
                            new_activations[target_id] = 0.0
                        new_activations[target_id] += spread_amount
            
            activated_concepts = new_activations
        
        # Filter by activation threshold and create result list
        relevant_knowledge = []
        
        for concept_id, activation in activated_concepts.items():
            if activation >= activation_threshold:
                concept = self.semantic_network.get(concept_id, {})
                concept["activation"] = activation
                concept["concept_id"] = concept_id
                
                # Record access
                concept["access_count"] = concept.get("access_count", 0) + 1
                
                relevant_knowledge.append(concept)
        
        # Sort by activation level
        relevant_knowledge.sort(key=lambda c: c["activation"], reverse=True)
        
        return relevant_knowledge
    
    async def retrieve_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retrieve all knowledge in a specific category"""
        concept_ids = self.category_index.get(category, [])
        return [self.semantic_network[cid] for cid in concept_ids if cid in self.semantic_network]
    
    async def strengthen_concept(self, concept_id: str, strength_increase: float = 0.1):
        """Strengthen a concept through use"""
        if concept_id in self.semantic_network:
            concept = self.semantic_network[concept_id]
            concept["strength"] = min(1.0, concept["strength"] + strength_increase)
            concept["access_count"] = concept.get("access_count", 0) + 1
    
    async def apply_decay(self, time_hours: float):
        """Apply very slow decay to long-term memory"""
        decay_factor = 0.999 ** (time_hours / 24)  # Very slow decay
        
        concepts_to_remove = []
        
        for concept_id, concept in self.semantic_network.items():
            # Apply decay, but less for frequently accessed concepts
            access_protection = min(0.5, concept.get("access_count", 0) * 0.01)
            effective_decay = decay_factor + access_protection
            
            concept["strength"] *= effective_decay
            
            # Remove concepts that have decayed significantly
            if concept["strength"] < 0.1:
                concepts_to_remove.append(concept_id)
        
        # Remove decayed concepts
        for concept_id in concepts_to_remove:
            await self._remove_concept(concept_id)
    
    async def _remove_concept(self, concept_id: str):
        """Remove a concept and update indices"""
        if concept_id not in self.semantic_network:
            return
        
        concept = self.semantic_network[concept_id]
        
        # Remove from main storage
        del self.semantic_network[concept_id]
        
        # Remove from keyword index
        for keyword in concept.get("keywords", []):
            if concept_id in self.concept_index[keyword]:
                self.concept_index[keyword].remove(concept_id)
        
        # Remove from category index
        category = concept.get("category", "general")
        if concept_id in self.category_index[category]:
            self.category_index[category].remove(concept_id)
        
        # Remove associations
        for association in concept.get("associations", []):
            target_id = association["target_id"]
            if target_id in self.semantic_network:
                target_concept = self.semantic_network[target_id]
                target_concept["associations"] = [
                    a for a in target_concept["associations"] 
                    if a["target_id"] != concept_id
                ]
    
    async def get_status(self) -> Dict[str, Any]:
        """Get long-term memory status"""
        if not self.semantic_network:
            return {
                "total_concepts": 0,
                "average_strength": 0.0,
                "total_associations": 0,
                "categories": 0
            }
        
        total_associations = sum(len(c.get("associations", [])) for c in self.semantic_network.values())
        
        return {
            "total_concepts": len(self.semantic_network),
            "average_strength": np.mean([c.get("strength", 0.5) for c in self.semantic_network.values()]),
            "total_associations": total_associations,
            "categories": len(self.category_index)
        }