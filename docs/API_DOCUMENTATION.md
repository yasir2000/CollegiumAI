# CollegiumAI API Documentation

Version: 1.0.0  
Last Updated: October 19, 2025

## 📋 Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Core APIs](#core-apis)
- [Cognitive Engine API](#cognitive-engine-api)
- [Persona System API](#persona-system-api)
- [Multi-Agent API](#multi-agent-api)
- [Configuration API](#configuration-api)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [SDK and Client Libraries](#sdk-and-client-libraries)

---

## Overview

The CollegiumAI API provides programmatic access to the advanced cognitive architecture and university intelligence capabilities. The API is designed for developers who want to integrate CollegiumAI's capabilities into their applications, services, or research projects.

### Key Features
- **Cognitive Processing**: Advanced multi-modal cognitive processing
- **Persona Intelligence**: Access to 51+ university personas
- **Multi-Agent Coordination**: Collaborative AI agent orchestration
- **Real-time Processing**: Async/await support for responsive applications
- **Comprehensive Testing**: Built-in validation and testing frameworks

### API Principles
- **Async-First**: All operations are asynchronous for optimal performance
- **Type-Safe**: Full type hints and validation for reliable development
- **Modular**: Clean separation of cognitive modules and capabilities
- **Extensible**: Easy integration of custom personas and cognitive modules

---

## Getting Started

### Installation

```python
# Clone the repository
git clone https://github.com/yasir2000/CollegiumAI.git
cd CollegiumAI

# Install dependencies (when available)
pip install -r requirements.txt
```

### Basic Setup

```python
import asyncio
from framework.cognitive import (
    CognitiveEngine, 
    CognitivePersonaFactory, 
    PersonaType
)

# Initialize the persona factory
factory = CognitivePersonaFactory()

# Create a cognitive agent
student_agent = factory.create_agent(PersonaType.TRADITIONAL_STUDENT)

# Process a request
async def example():
    result = await student_agent.process_intelligent_request({
        "text": "I need help with my studies",
        "context": {"domain": "academic", "urgency": "medium"}
    })
    return result

# Run the example
result = asyncio.run(example())
print(f"Response confidence: {result.get('confidence', 0):.2f}")
```

### Quick Validation

```python
# Validate your setup
import subprocess
result = subprocess.run(["python", "quick_test.py"], capture_output=True, text=True)
print(result.stdout)
```

---

## Core APIs

### CognitiveEngine

The core cognitive processing engine that orchestrates all cognitive modules.

#### Constructor

```python
class CognitiveEngine:
    def __init__(self, persona_id: str):
        """
        Initialize cognitive engine for a specific persona
        
        Args:
            persona_id: Unique identifier for the persona
        """
```

#### Methods

##### process_cognitive_cycle()

```python
async def process_cognitive_cycle(
    self, 
    input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process input through complete cognitive cycle
    
    Args:
        input_data: Dictionary containing:
            - text: Input text to process
            - context: Contextual information
            - metadata: Additional processing hints
    
    Returns:
        Dictionary containing:
            - confidence: Processing confidence (0.0-1.0)
            - cognitive_state: Current cognitive state
            - action_plan: Recommended actions
            - processing_time: Time taken for processing
    
    Example:
        result = await engine.process_cognitive_cycle({
            "text": "Help me understand calculus",
            "context": {
                "domain": "mathematics",
                "difficulty": "intermediate",
                "urgency": "medium"
            }
        })
    """
```

### CognitivePersonaFactory

Factory class for creating persona-specific cognitive agents.

#### Methods

##### create_agent()

```python
def create_agent(
    persona_type: PersonaType, 
    individual_context: Dict[str, Any] = None
) -> PersonaCognitiveAgent:
    """
    Create a cognitive agent for specific persona type
    
    Args:
        persona_type: Type of persona (enum value)
        individual_context: Optional individual customization
    
    Returns:
        PersonaCognitiveAgent instance
    
    Example:
        factory = CognitivePersonaFactory()
        student = factory.create_agent(
            PersonaType.GRADUATE_STUDENT,
            {"research_area": "machine_learning"}
        )
    """
```

##### create_student_agent()

```python
def create_student_agent(
    student_type: str, 
    individual_context: Dict[str, Any] = None
) -> PersonaCognitiveAgent:
    """
    Create student-specific agent with string identifier
    
    Args:
        student_type: String identifier for student type
        individual_context: Individual customization options
    
    Returns:
        PersonaCognitiveAgent for student
    
    Example:
        student = factory.create_student_agent(
            "international_graduate",
            {"home_country": "Germany", "field": "physics"}
        )
    """
```

### PersonaCognitiveAgent

Individual cognitive agent with persona-specific capabilities.

#### Methods

##### process_intelligent_request()

```python
async def process_intelligent_request(
    self, 
    request: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process request with persona-specific intelligence
    
    Args:
        request: Dictionary containing:
            - text: Request text
            - context: Contextual information
            - preferences: User preferences
    
    Returns:
        Dictionary containing:
            - response: Generated response text
            - confidence: Response confidence
            - support_assessment: Identified support needs
            - cognitive_insights: Processing insights
            - recommendations: Action recommendations
    
    Example:
        result = await agent.process_intelligent_request({
            "text": "I'm struggling with time management",
            "context": {
                "domain": "personal_development",
                "urgency": "high",
                "current_stress": 0.8
            }
        })
    """
```

---

## Cognitive Engine API

### Perception Module

Access to multi-modal perception capabilities.

```python
# Access perception module
perception = engine.perception_module

# Process multi-modal input
result = await perception.process_multi_modal_input({
    "text": "I'm excited but worried about my presentation",
    "context": {
        "emotional_cues": ["excitement", "anxiety"],
        "domain": "academic_presentation"
    }
})

# Result structure
{
    "salience_score": 0.85,
    "emotional_patterns": {...},
    "academic_patterns": {...},
    "attention_targets": [...]
}
```

### Reasoning Engine

Advanced reasoning capabilities for complex problem solving.

```python
# Access reasoning engine
reasoning = engine.reasoning_engine

# Causal relationship analysis
causal_result = await reasoning.analyze_causal_relationships(
    problem="Student grades declining",
    context={
        "factors": ["attendance", "engagement", "difficulty"],
        "domain": "academic_performance"
    }
)

# Analogical reasoning
analogical_result = await reasoning.apply_analogical_reasoning(
    scenario={
        "problem": "Research methodology confusion",
        "context": {"field": "psychology", "level": "graduate"}
    },
    domain_context={"related_fields": ["statistics", "experimental_design"]}
)
```

### Memory System

Comprehensive memory storage and retrieval.

```python
# Access memory system
memory = engine.memory_system

# Store episodic memory
await memory.store_episodic_memory({
    "content": "Successful tutoring session on linear algebra",
    "context": {
        "domain": "mathematics",
        "importance": 0.8,
        "emotional_valence": 0.7
    },
    "timestamp": datetime.now()
})

# Retrieve relevant memories
memories = await memory.retrieve_relevant_memories({
    "query": "mathematics tutoring",
    "context": {"similarity_threshold": 0.6}
})
```

### Learning System

Adaptive learning and optimization capabilities.

```python
# Access learning systems
adaptive_learning = engine.learning_systems["adaptive"]

# Update from learning episode
await adaptive_learning.update_from_episode({
    "input_data": "Complex calculus problem",
    "cognitive_state": {"motivation": 0.8, "cognitive_load": 0.6},
    "processing_time": 2.1,
    "confidence": 0.75,
    "success": True
})

# Get optimal learning strategy
strategy = await adaptive_learning.get_optimal_learning_strategy({
    "topic": "differential_equations",
    "difficulty": 0.8,
    "user_profile": {"learning_style": "visual"}
})
```

### Decision Making Engine

Strategic decision making with multiple approaches.

```python
from framework.cognitive.decision_making import (
    DecisionContext, DecisionType, DecisionCriteria, DecisionAlternative
)

# Create decision context
context = DecisionContext(
    decision_type=DecisionType.ANALYTICAL,
    urgency_level=0.7,
    importance_level=0.9
)

# Define criteria
criteria = [
    DecisionCriteria(name="effectiveness", weight=0.4),
    DecisionCriteria(name="feasibility", weight=0.3),
    DecisionCriteria(name="cost", weight=0.3)
]

# Define alternatives
alternatives = [
    DecisionAlternative(
        name="Option A: Individual Tutoring",
        criteria_scores={
            "effectiveness": 0.9,
            "feasibility": 0.6,
            "cost": 0.3
        }
    ),
    DecisionAlternative(
        name="Option B: Study Group",
        criteria_scores={
            "effectiveness": 0.7,
            "feasibility": 0.9,
            "cost": 0.8
        }
    )
]

# Make decision
decision = await engine.decision_engine.make_decision(
    context, criteria, alternatives
)
```

### Attention Mechanism

Dynamic attention allocation and management.

```python
from framework.cognitive.attention import AttentionTarget

# Create attention targets
targets = [
    AttentionTarget(
        name="High Priority Assignment",
        priority=0.9,
        cognitive_load=0.6,
        deadline_pressure=0.8
    ),
    AttentionTarget(
        name="Reading Assignment",
        priority=0.5,
        cognitive_load=0.3,
        deadline_pressure=0.2
    )
]

# Allocate attention
allocation = await engine.attention_mechanism.allocate_attention(targets)
```

### Metacognitive Controller

Self-monitoring and performance regulation.

```python
# Monitor cognitive process
monitoring = await engine.metacognitive_controller.monitor_cognitive_process(
    process_name="problem_solving",
    process_data={
        "performance_metrics": {"accuracy": 0.85, "speed": 0.7},
        "resource_usage": {"attention": 0.8, "working_memory": 0.6},
        "duration": 3.2,
        "strategy_used": "analytical"
    }
)
```

---

## Persona System API

### PersonaType Enumeration

```python
from framework.cognitive import PersonaType

# Student personas
PersonaType.TRADITIONAL_STUDENT
PersonaType.INTERNATIONAL_STUDENT
PersonaType.GRADUATE_STUDENT
PersonaType.TRANSFER_STUDENT
PersonaType.NON_TRADITIONAL_STUDENT
PersonaType.STUDENT_WITH_DISABILITIES
PersonaType.ONLINE_STUDENT
PersonaType.PART_TIME_STUDENT

# Faculty personas
PersonaType.PROFESSOR
PersonaType.LECTURER
PersonaType.RESEARCHER
PersonaType.DEPARTMENT_HEAD
PersonaType.ADJUNCT_FACULTY
PersonaType.POSTDOCTORAL_FELLOW

# Staff personas
PersonaType.ACADEMIC_ADVISOR
PersonaType.REGISTRAR
PersonaType.STUDENT_AFFAIRS_OFFICER
PersonaType.IT_SUPPORT_SPECIALIST
PersonaType.FINANCIAL_AID_COUNSELOR
PersonaType.CAREER_COUNSELOR
PersonaType.LIBRARIAN
```

### Persona Cognitive Profiles

Each persona has unique cognitive parameters:

```python
# Example: Graduate student profile
{
    "attention_params": {
        "focus_depth": 0.85,
        "task_switching_cost": 0.3,
        "sustained_attention": 0.9
    },
    "learning_params": {
        "learning_rate": 0.02,
        "preferred_modality": "analytical",
        "complexity_tolerance": 0.8
    },
    "decision_params": {
        "risk_tolerance": 0.6,
        "analysis_depth": 0.9,
        "decision_speed": 0.4
    },
    "communication_style": {
        "formality": 0.7,
        "detail_level": 0.8,
        "empathy": 0.6
    }
}
```

### Custom Persona Creation

```python
# Create custom persona profile
custom_profile = {
    "attention_params": {"focus_depth": 0.7},
    "learning_params": {"learning_rate": 0.03},
    "decision_params": {"risk_tolerance": 0.8},
    "individual_context": {
        "field_of_study": "computer_science",
        "year": "senior",
        "interests": ["AI", "machine_learning"]
    }
}

# Create agent with custom profile
agent = factory.create_agent(
    PersonaType.TRADITIONAL_STUDENT,
    custom_profile
)
```

---

## Multi-Agent API

### MultiAgentOrchestrator

Coordination of multiple AI agents for complex tasks.

```python
from multi_agent_system import MultiAgentOrchestrator

# Mock client for development/testing
class MockOllamaClient:
    async def generate_response(self, prompt, **kwargs):
        return {"response": f"Response to: {prompt}", "done": True}
    
    async def chat(self, messages, **kwargs):
        return {
            "message": {"content": f"Chat response to {len(messages)} messages"},
            "done": True
        }

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator(MockOllamaClient())

# Coordinate task
task = {
    "type": "academic_support",
    "description": "Help with research methodology design",
    "complexity": "high",
    "required_expertise": ["research", "statistics", "writing"]
}

result = await orchestrator.coordinate_task(task)
```

### Available Agents

The multi-agent system includes specialized agents:

```python
# Agent types and specializations
agents = {
    "research_specialist": {
        "specialization": "Academic research and methodology",
        "expertise": ["research_design", "literature_review", "data_analysis"]
    },
    "academic_advisor": {
        "specialization": "Academic planning and guidance", 
        "expertise": ["course_planning", "degree_requirements", "career_advice"]
    },
    "wellness_counselor": {
        "specialization": "Student wellness and support",
        "expertise": ["stress_management", "time_management", "mental_health"]
    },
    "technical_assistant": {
        "specialization": "Technical and IT support",
        "expertise": ["software_help", "platform_navigation", "troubleshooting"]
    }
}
```

---

## Configuration API

### System Configuration

```python
# Default configuration structure
config = {
    "max_concurrent_requests": 15,
    "session_timeout": 7200,
    "logging_level": "INFO",
    "enable_learning": True,
    "enable_multi_agent": True,
    
    "cognitive_parameters": {
        "default_confidence_threshold": 0.6,
        "learning_rate": 0.01,
        "attention_decay_rate": 0.95,
        "memory_consolidation_threshold": 0.7
    },
    
    "persona_preferences": {
        "traditional_student": {
            "response_style": "supportive",
            "complexity_level": "intermediate",
            "interaction_frequency": "high"
        }
    },
    
    "multi_agent_settings": {
        "collaboration_threshold": 0.7,
        "max_agents_per_task": 5,
        "consensus_requirement": 0.8
    },
    
    "performance_settings": {
        "response_timeout": 5.0,
        "max_memory_size": 1000,
        "cache_expiry": 3600
    }
}
```

### Loading Configuration

```python
import json

# Load from file
with open("config/default_config.json", "r") as f:
    config = json.load(f)

# Apply to system
collegium_ai = CollegiumAI()
collegium_ai.config.update(config)
```

---

## Error Handling

### Exception Types

```python
class CollegiumAIException(Exception):
    """Base exception for CollegiumAI"""
    pass

class CognitiveProcessingError(CollegiumAIException):
    """Error in cognitive processing pipeline"""
    pass

class PersonaNotFoundError(CollegiumAIException):
    """Requested persona type not available"""
    pass

class MultiAgentCoordinationError(CollegiumAIException):
    """Error in multi-agent coordination"""
    pass

class ConfigurationError(CollegiumAIException):
    """Invalid configuration provided"""
    pass
```

### Error Handling Patterns

```python
import logging
from typing import Optional

async def safe_cognitive_processing(
    engine: CognitiveEngine,
    input_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Safely process cognitive input with error handling
    """
    try:
        result = await engine.process_cognitive_cycle(input_data)
        return result
        
    except CognitiveProcessingError as e:
        logging.error(f"Cognitive processing failed: {e}")
        return {
            "error": "processing_failed",
            "message": "Unable to process request",
            "confidence": 0.0
        }
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {
            "error": "system_error",
            "message": "System error occurred",
            "confidence": 0.0
        }
```

### Graceful Degradation

```python
async def robust_request_processing(
    agent: PersonaCognitiveAgent,
    request: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process request with fallback mechanisms
    """
    try:
        # Try full cognitive processing
        return await agent.process_intelligent_request(request)
        
    except Exception as e:
        logging.warning(f"Full processing failed: {e}")
        
        # Fallback to basic response
        return {
            "response": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
            "confidence": 0.1,
            "error_mode": True,
            "fallback_used": True
        }
```

---

## Examples

### Basic Student Assistance

```python
async def student_help_example():
    """Example: Basic student academic assistance"""
    
    # Create student agent
    factory = CognitivePersonaFactory()
    student = factory.create_agent(PersonaType.TRADITIONAL_STUDENT)
    
    # Process help request
    result = await student.process_intelligent_request({
        "text": "I'm having trouble understanding derivatives in calculus",
        "context": {
            "subject": "mathematics",
            "topic": "calculus",
            "difficulty_level": "beginner",
            "urgency": "medium"
        }
    })
    
    print(f"Response: {result.get('response', 'No response')}")
    print(f"Confidence: {result.get('confidence', 0):.2f}")
    print(f"Support types: {result.get('support_assessment', {}).get('support_types', [])}")

# Run example
asyncio.run(student_help_example())
```

### Multi-Agent Research Support

```python
async def research_support_example():
    """Example: Complex research support with multiple agents"""
    
    # Initialize multi-agent system
    class MockClient:
        async def generate_response(self, prompt, **kwargs):
            return {"response": f"Research guidance for: {prompt[:50]}...", "done": True}
        async def chat(self, messages, **kwargs):
            return {"message": {"content": "Research methodology advice"}, "done": True}
    
    orchestrator = MultiAgentOrchestrator(MockClient())
    
    # Coordinate research task
    task = {
        "type": "research_support",
        "description": "Need help designing experiment for psychology research on learning",
        "complexity": "high",
        "required_expertise": ["research_methodology", "psychology", "statistics"],
        "context": {
            "field": "cognitive_psychology",
            "study_type": "experimental",
            "sample_size": 100
        }
    }
    
    result = await orchestrator.coordinate_task(task)
    
    print(f"Coordination result: {result}")
    print(f"Participating agents: {len(orchestrator.agents)}")

# Run example
asyncio.run(research_support_example())
```

### Custom Persona Development

```python
async def custom_persona_example():
    """Example: Creating and using custom persona"""
    
    # Define custom persona profile
    custom_profile = {
        "attention_params": {
            "focus_depth": 0.9,  # High focus for research
            "multitasking_ability": 0.4  # Low multitasking
        },
        "learning_params": {
            "learning_rate": 0.015,  # Slower, more thorough learning
            "preferred_modality": "analytical",
            "complexity_tolerance": 0.95  # Very high complexity tolerance
        },
        "decision_params": {
            "risk_tolerance": 0.3,  # Conservative decisions
            "analysis_depth": 0.95,  # Very thorough analysis
            "decision_speed": 0.2  # Slow, careful decisions
        },
        "individual_context": {
            "field": "theoretical_physics",
            "career_stage": "postdoc",
            "research_focus": "quantum_mechanics"
        }
    }
    
    # Create custom agent
    factory = CognitivePersonaFactory()
    physicist = factory.create_agent(
        PersonaType.POSTDOCTORAL_FELLOW,
        custom_profile
    )
    
    # Test with domain-specific request
    result = await physicist.process_intelligent_request({
        "text": "I need help with grant writing for my quantum computing research proposal",
        "context": {
            "domain": "research",
            "subdomain": "quantum_physics",
            "task_type": "grant_writing",
            "deadline_pressure": 0.8
        }
    })
    
    print(f"Custom persona response confidence: {result.get('confidence', 0):.2f}")

# Run example
asyncio.run(custom_persona_example())
```

### Performance Monitoring

```python
async def performance_monitoring_example():
    """Example: Monitoring system performance and health"""
    
    import time
    
    # Initialize system
    factory = CognitivePersonaFactory()
    agent = factory.create_agent(PersonaType.GRADUATE_STUDENT)
    
    # Performance testing
    response_times = []
    confidences = []
    
    test_requests = [
        "Help with statistical analysis",
        "Research methodology questions",
        "Time management strategies",
        "Writing assistance needed",
        "Career planning guidance"
    ]
    
    for i, request_text in enumerate(test_requests):
        start_time = time.time()
        
        result = await agent.process_intelligent_request({
            "text": request_text,
            "context": {"test_id": i, "domain": "academic"}
        })
        
        response_time = time.time() - start_time
        response_times.append(response_time)
        confidences.append(result.get("confidence", 0))
        
        print(f"Request {i+1}: {response_time:.2f}s, confidence: {result.get('confidence', 0):.2f}")
    
    # Calculate performance metrics
    avg_response_time = sum(response_times) / len(response_times)
    avg_confidence = sum(confidences) / len(confidences)
    
    print(f"\nPerformance Summary:")
    print(f"Average response time: {avg_response_time:.2f} seconds")
    print(f"Average confidence: {avg_confidence:.2f}")
    print(f"Requests processed: {len(test_requests)}")

# Run example
asyncio.run(performance_monitoring_example())
```

---

## SDK and Client Libraries

### Python SDK (Native)

The main Python SDK provides full access to all CollegiumAI capabilities:

```python
# Installation
pip install collegium-ai  # When available

# Usage
from collegium_ai import CollegiumAI, PersonaType

async def main():
    ai = CollegiumAI()
    await ai.initialize_system()
    
    result = await ai.process_request(
        "Help with my research",
        persona_type="graduate_student"
    )
    return result
```

### REST API Wrapper (Planned)

Future REST API for language-agnostic integration:

```python
# FastAPI server wrapper (planned for v1.1.0)
from fastapi import FastAPI
from collegium_ai import CollegiumAI

app = FastAPI()
ai_system = CollegiumAI()

@app.post("/api/v1/process")
async def process_request(request: ProcessRequest):
    result = await ai_system.process_request(
        request.text,
        request.persona_type,
        request.context
    )
    return result
```

### JavaScript/TypeScript Client (Planned)

```javascript
// JavaScript client (planned for v1.2.0)
import { CollegiumAI } from 'collegium-ai-js';

const ai = new CollegiumAI({
    apiKey: 'your-api-key',
    baseUrl: 'https://api.collegium-ai.org'
});

const result = await ai.processRequest({
    text: "Help with my studies",
    personaType: "traditional_student",
    context: { domain: "academic" }
});
```

---

## Rate Limits and Quotas

### Current Limitations (v1.0.0)
- **Concurrent Requests**: 15 per system instance
- **Session Duration**: 2 hours default timeout
- **Memory Usage**: 1000 items max per session
- **Processing Timeout**: 5 seconds per request

### Planned Scaling (v1.1.0+)
- **Concurrent Requests**: 100+ with load balancing
- **Multi-tenancy**: Isolated instances per institution
- **Caching**: Intelligent response caching
- **Auto-scaling**: Dynamic resource allocation

---

## Versioning and Compatibility

### Semantic Versioning
CollegiumAI follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes to API
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### API Compatibility
- **v1.0.x**: Stable API, no breaking changes
- **v1.1.x**: New features, maintaining v1.0 compatibility
- **v2.0.x**: Next major release with potential breaking changes

### Migration Guides
Migration guides will be provided for major version updates, including:
- API changes and deprecations
- New feature adoption patterns
- Backward compatibility considerations
- Automated migration tools

---

## Support and Community

### Documentation
- **API Reference**: This document
- **User Guides**: README.md and tutorials
- **Examples**: examples/ directory
- **Video Tutorials**: Coming in v1.1.0

### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community Q&A and sharing
- **Stack Overflow**: `collegium-ai` tag
- **Academic Forums**: Research and education discussions

### Professional Support
- **Consulting**: Custom implementation assistance
- **Training**: Workshops and educational programs
- **Enterprise**: Dedicated support for institutions
- **Research**: Collaboration opportunities

---

**For more information, examples, and the latest updates, visit our [GitHub repository](https://github.com/yasir2000/CollegiumAI) or check out the comprehensive [README](README.md).**

*API Documentation v1.0.0 - Last updated October 19, 2025*