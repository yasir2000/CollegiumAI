"""
Core Framework Classes
=====================

Core classes for the CollegiumAI framework.
"""

from typing import Dict, List, Any
from datetime import datetime

class CollegiumFramework:
    """Main CollegiumAI framework class"""
    
    def __init__(self):
        self.agents = {}
        self.students = {}
        self.courses = {}
        self.initialized = True
        self.created_at = datetime.now()
    
    def get_status(self) -> Dict[str, Any]:
        """Get framework status"""
        return {
            "initialized": self.initialized,
            "agents": len(self.agents),
            "students": len(self.students),
            "courses": len(self.courses),
            "created_at": self.created_at.isoformat()
        }