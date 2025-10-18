"""
CollegiumAI In-Memory Database Service
Instant database functionality without external dependencies
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import uuid

logger = logging.getLogger(__name__)

class InMemoryDatabaseService:
    """High-performance in-memory database service"""
    
    def __init__(self):
        # Memory stores
        self.memory_store = defaultdict(list)  # cognitive memories
        self.sessions = {}  # user sessions
        self.interactions = []  # interaction logs
        self.cache = {}  # key-value cache
        self.analytics = defaultdict(list)
        
        logger.info("✅ In-memory database service initialized")
    
    async def connect(self):
        """Mock connection (instant)"""
        await asyncio.sleep(0.01)  # Simulate connection time
        logger.info("🚀 In-memory database connected instantly")
    
    async def disconnect(self):
        """Mock disconnection"""
        logger.info("📱 In-memory database disconnected")
    
    # Cognitive Memory Operations
    async def store_memory(self, persona_id: str, memory_type: str, content: Dict[str, Any], importance: float = 0.5):
        """Store cognitive memory in memory"""
        memory_id = str(uuid.uuid4())
        memory = {
            "id": memory_id,
            "persona_id": persona_id,
            "memory_type": memory_type,
            "content": content,
            "importance_score": importance,
            "created_at": datetime.now(),
            "accessed_at": datetime.now(),
            "access_count": 0
        }
        
        self.memory_store[persona_id].append(memory)
        return memory_id
    
    async def retrieve_memories(self, persona_id: str, memory_type: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Retrieve cognitive memories from memory"""
        memories = self.memory_store.get(persona_id, [])
        
        if memory_type:
            memories = [m for m in memories if m["memory_type"] == memory_type]
        
        # Sort by importance and recency
        memories.sort(key=lambda x: (x["importance_score"], x["created_at"]), reverse=True)
        
        return memories[:limit]
    
    # Session Management
    async def create_session(self, session_id: str, persona_id: str, data: Dict[str, Any], ttl: int = 7200):
        """Create user session in memory"""
        session = {
            "session_id": session_id,
            "persona_id": persona_id,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(seconds=ttl),
            "data": data
        }
        
        self.sessions[session_id] = session
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data from memory"""
        session = self.sessions.get(session_id)
        
        if session and session["expires_at"] > datetime.now():
            return session
        elif session:
            # Clean expired session
            del self.sessions[session_id]
        
        return None
    
    async def update_session(self, session_id: str, data: Dict[str, Any]):
        """Update session data in memory"""
        session = await self.get_session(session_id)
        if session:
            session["data"].update(data)
            session["updated_at"] = datetime.now()
    
    # Analytics
    async def log_interaction(self, persona_id: str, session_id: str, request_data: Dict, response_data: Dict, metrics: Dict):
        """Log interaction in memory for analytics"""
        interaction = {
            "id": str(uuid.uuid4()),
            "persona_id": persona_id,
            "session_id": session_id,
            "timestamp": datetime.now(),
            "request": request_data,
            "response": response_data,
            "metrics": metrics
        }
        
        self.interactions.append(interaction)
        self.analytics[persona_id].append(interaction)
        
        return interaction["id"]
    
    async def get_analytics(self, persona_id: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
        """Get analytics data from memory"""
        since_date = datetime.now() - timedelta(days=days)
        
        if persona_id:
            interactions = [i for i in self.analytics[persona_id] if i["timestamp"] >= since_date]
        else:
            interactions = [i for i in self.interactions if i["timestamp"] >= since_date]
        
        if not interactions:
            return {"period_days": days, "total_interactions": 0, "personas": []}
        
        # Calculate statistics
        total_interactions = len(interactions)
        personas = set(i["persona_id"] for i in interactions)
        
        persona_stats = {}
        for p_id in personas:
            p_interactions = [i for i in interactions if i["persona_id"] == p_id]
            
            response_times = [i["metrics"].get("processing_time", 0) for i in p_interactions if "metrics" in i]
            confidences = [i["metrics"].get("confidence", 0) for i in p_interactions if "metrics" in i]
            
            persona_stats[p_id] = {
                "total_interactions": len(p_interactions),
                "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                "avg_confidence": sum(confidences) / len(confidences) if confidences else 0
            }
        
        return {
            "period_days": days,
            "total_interactions": total_interactions,
            "total_personas": len(personas),
            "persona_stats": persona_stats
        }
    
    # Cache operations
    async def cache_set(self, key: str, value: Any, ttl: int = 3600):
        """Set cache value with TTL"""
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = {
            "value": value,
            "expires_at": expires_at
        }
    
    async def cache_get(self, key: str) -> Any:
        """Get cache value"""
        cached = self.cache.get(key)
        
        if cached and cached["expires_at"] > datetime.now():
            return cached["value"]
        elif cached:
            # Clean expired cache
            del self.cache[key]
        
        return None
    
    # Health check
    async def health_check(self) -> Dict[str, bool]:
        """Health check - always healthy for in-memory"""
        return {
            "memory_store": True,
            "sessions": True,
            "cache": True,
            "analytics": True
        }
    
    # Statistics
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        total_memories = sum(len(memories) for memories in self.memory_store.values())
        active_sessions = len([s for s in self.sessions.values() if s["expires_at"] > datetime.now()])
        
        return {
            "total_personas": len(self.memory_store),
            "total_memories": total_memories,
            "active_sessions": active_sessions,
            "total_interactions": len(self.interactions),
            "cache_entries": len(self.cache)
        }

# Global in-memory database service
_db_service = None

async def get_database_service() -> InMemoryDatabaseService:
    """Get or create in-memory database service"""
    global _db_service
    if _db_service is None:
        _db_service = InMemoryDatabaseService()
        await _db_service.connect()
    return _db_service

async def close_database_service():
    """Close database service"""
    global _db_service
    if _db_service:
        await _db_service.disconnect()
        _db_service = None
