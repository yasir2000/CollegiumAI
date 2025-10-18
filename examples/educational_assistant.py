#!/usr/bin/env python3
"""
CollegiumAI Educational Assistant with Multi-Provider LLM
=========================================================

This example demonstrates a practical educational assistant that leverages
the multi-provider LLM framework to provide intelligent academic support
with cost optimization and local model support.

Features:
- Academic advising with cost-optimized models
- Research assistance with high-capability models
- Student support with local/private models
- Content generation with streaming responses
- Intelligent provider selection based on task requirements
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent))

from framework.llm import (
    LLMManager, LLMRequest, LLMMessage, ModelSelection, 
    ModelCapability, LLMProvider, create_chat_request,
    create_system_message, create_user_message, create_assistant_message
)

class TaskType(Enum):
    """Types of educational tasks"""
    ACADEMIC_ADVISING = "academic_advising"
    RESEARCH_ASSISTANCE = "research_assistance"
    TUTORING = "tutoring"
    CONTENT_CREATION = "content_creation"
    CODE_REVIEW = "code_review"
    STUDENT_SUPPORT = "student_support"

class EducationalAssistant:
    """Intelligent educational assistant with multi-provider LLM support"""
    
    def __init__(self):
        self.llm_manager = None
        self.conversation_history = {}
        self.task_preferences = self._setup_task_preferences()
    
    def _setup_task_preferences(self) -> Dict[TaskType, ModelSelection]:
        """Configure model selection preferences for different educational tasks"""
        return {
            # Academic advising - cost-optimized for high volume
            TaskType.ACADEMIC_ADVISING: ModelSelection(
                required_capabilities=[ModelCapability.CHAT_COMPLETION],
                max_cost_per_1k_tokens=0.01,  # Budget-friendly
                preferred_providers=[LLMProvider.OPENAI, LLMProvider.OLLAMA],
                temperature_range=(0.3, 0.7)  # Balanced but leaning factual
            ),
            
            # Research assistance - high capability models
            TaskType.RESEARCH_ASSISTANCE: ModelSelection(
                required_capabilities=[
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.REASONING
                ],
                preferred_providers=[LLMProvider.ANTHROPIC, LLMProvider.OPENAI],
                min_context_length=8000,  # Need longer context for research
                temperature_range=(0.2, 0.5)  # More factual
            ),
            
            # Tutoring - prefer local models for privacy
            TaskType.TUTORING: ModelSelection(
                required_capabilities=[ModelCapability.CHAT_COMPLETION],
                prefer_local=True,  # Student privacy
                preferred_providers=[LLMProvider.OLLAMA, LLMProvider.OPENAI],
                temperature_range=(0.4, 0.8)  # Engaging but accurate
            ),
            
            # Content creation - streaming capable models
            TaskType.CONTENT_CREATION: ModelSelection(
                required_capabilities=[
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CREATIVE_WRITING
                ],
                require_streaming=True,
                preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
                temperature_range=(0.7, 0.9)  # More creative
            ),
            
            # Code review - programming-focused models
            TaskType.CODE_REVIEW: ModelSelection(
                required_capabilities=[
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.CHAT_COMPLETION
                ],
                preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
                temperature_range=(0.2, 0.4)  # Precise and accurate
            ),
            
            # Student support - local/private models preferred
            TaskType.STUDENT_SUPPORT: ModelSelection(
                required_capabilities=[ModelCapability.CHAT_COMPLETION],
                prefer_local=True,
                max_cost_per_1k_tokens=0.005,  # Very cost-effective
                preferred_providers=[LLMProvider.OLLAMA],
                temperature_range=(0.5, 0.8)  # Warm and supportive
            )
        }
    
    async def initialize(self):
        """Initialize the educational assistant"""
        print("🎓 Initializing CollegiumAI Educational Assistant...")
        
        self.llm_manager = LLMManager()
        await self.llm_manager.initialize()
        
        print("✅ Educational Assistant ready!")
        return self
    
    async def provide_academic_advice(self, student_query: str, student_context: Dict[str, Any] = None) -> str:
        """Provide academic advising with cost optimization"""
        
        # Build context-aware system prompt
        context_info = ""
        if student_context:
            major = student_context.get('major', 'undeclared')
            year = student_context.get('year', 'unknown')
            interests = student_context.get('interests', [])
            context_info = f" The student is a {year} majoring in {major}"
            if interests:
                context_info += f" with interests in {', '.join(interests)}"
        
        system_prompt = f"""You are an expert academic advisor at CollegiumAI.{context_info}
        
        Provide personalized, actionable academic advice that:
        - Considers the student's current academic standing
        - Suggests relevant courses and opportunities
        - Explains the reasoning behind recommendations
        - Encourages academic growth and exploration
        - Is supportive and encouraging
        
        Keep responses concise but comprehensive."""
        
        messages = [
            create_system_message(system_prompt),
            create_user_message(student_query)
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.6,
            max_tokens=400
        )
        
        # Use cost-optimized selection for academic advising
        response = await self.llm_manager.generate_completion(
            request, 
            self.task_preferences[TaskType.ACADEMIC_ADVISING]
        )
        
        return response.content
    
    async def assist_with_research(self, research_query: str, domain: str = None) -> str:
        """Provide research assistance with high-capability models"""
        
        domain_context = f" in the field of {domain}" if domain else ""
        
        system_prompt = f"""You are a research assistant specializing in academic research{domain_context}.
        
        Your role is to:
        - Help analyze research questions and methodologies
        - Suggest relevant literature and resources
        - Explain complex concepts clearly
        - Provide structured research guidance
        - Identify potential research gaps or opportunities
        
        Provide thorough, well-reasoned responses with academic rigor."""
        
        messages = [
            create_system_message(system_prompt),
            create_user_message(research_query)
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.4,
            max_tokens=600
        )
        
        # Use high-capability models for research
        response = await self.llm_manager.generate_completion(
            request,
            self.task_preferences[TaskType.RESEARCH_ASSISTANCE]
        )
        
        return response.content
    
    async def provide_tutoring(self, subject: str, student_question: str, difficulty_level: str = "intermediate") -> str:
        """Provide tutoring with privacy-focused local models"""
        
        system_prompt = f"""You are an expert tutor for {subject} at the {difficulty_level} level.
        
        Your teaching approach:
        - Break down complex concepts into digestible parts
        - Use analogies and examples to explain difficult topics
        - Encourage student thinking with guiding questions
        - Provide step-by-step explanations
        - Be patient, supportive, and encouraging
        - Adapt explanations to the student's level
        
        Focus on helping the student understand, not just providing answers."""
        
        messages = [
            create_system_message(system_prompt),
            create_user_message(student_question)
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # Prefer local models for tutoring (privacy)
        response = await self.llm_manager.generate_completion(
            request,
            self.task_preferences[TaskType.TUTORING]
        )
        
        return response.content
    
    async def create_educational_content(self, content_type: str, topic: str, audience: str = "college students") -> str:
        """Create educational content with streaming for real-time generation"""
        
        system_prompt = f"""You are an educational content creator specializing in {content_type} for {audience}.
        
        Create engaging, informative content that:
        - Is appropriate for the target audience
        - Uses clear, accessible language
        - Includes relevant examples and applications
        - Maintains academic accuracy
        - Encourages further learning and exploration
        
        Make the content interesting and memorable."""
        
        content_request = f"Create a {content_type} about {topic} for {audience}."
        
        messages = [
            create_system_message(system_prompt),
            create_user_message(content_request)
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.8,
            max_tokens=800
        )
        
        # Use streaming for content creation
        print(f"🎨 Creating {content_type} about {topic}...")
        print("-" * 50)
        
        full_content = ""
        async for chunk in self.llm_manager.generate_streaming_completion(
            request, 
            self.task_preferences[TaskType.CONTENT_CREATION]
        ):
            print(chunk, end="", flush=True)
            full_content += chunk
        
        print("\n" + "-" * 50)
        return full_content
    
    async def review_student_code(self, code: str, language: str, assignment_context: str = None) -> str:
        """Provide code review with programming-focused models"""
        
        context_info = f" for a {assignment_context} assignment" if assignment_context else ""
        
        system_prompt = f"""You are a programming instructor reviewing {language} code{context_info}.
        
        Provide constructive code review feedback that:
        - Identifies strengths in the code
        - Points out areas for improvement
        - Suggests specific fixes or enhancements
        - Explains best practices and coding standards
        - Considers code readability, efficiency, and maintainability
        - Encourages good programming habits
        
        Be supportive and educational in your feedback."""
        
        messages = [
            create_system_message(system_prompt),
            create_user_message(f"Please review this {language} code:\n\n```{language}\n{code}\n```")
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.3,
            max_tokens=600
        )
        
        # Use programming-capable models
        response = await self.llm_manager.generate_completion(
            request,
            self.task_preferences[TaskType.CODE_REVIEW]
        )
        
        return response.content
    
    async def provide_student_support(self, concern: str, support_type: str = "general") -> str:
        """Provide student support with privacy-focused approach"""
        
        system_prompt = f"""You are a supportive student counselor at CollegiumAI providing {support_type} support.
        
        Your approach is:
        - Empathetic and understanding
        - Non-judgmental and supportive
        - Practical and solution-oriented
        - Encouraging and motivating
        - Respectful of student privacy and autonomy
        
        Provide helpful guidance while recognizing when professional help might be needed."""
        
        messages = [
            create_system_message(system_prompt),
            create_user_message(concern)
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        
        # Use local/private models for sensitive support
        response = await self.llm_manager.generate_completion(
            request,
            self.task_preferences[TaskType.STUDENT_SUPPORT]
        )
        
        return response.content
    
    async def interactive_session(self):
        """Run an interactive session demonstrating different capabilities"""
        
        print("🎓 CollegiumAI Educational Assistant - Interactive Demo")
        print("=" * 60)
        print()
        print("Available services:")
        print("1. Academic Advising")
        print("2. Research Assistance") 
        print("3. Tutoring")
        print("4. Content Creation")
        print("5. Code Review")
        print("6. Student Support")
        print("7. Exit")
        print()
        
        while True:
            try:
                choice = input("Select a service (1-7): ").strip()
                
                if choice == "7":
                    break
                elif choice == "1":
                    await self._demo_academic_advising()
                elif choice == "2":
                    await self._demo_research_assistance()
                elif choice == "3":
                    await self._demo_tutoring()
                elif choice == "4":
                    await self._demo_content_creation()
                elif choice == "5":
                    await self._demo_code_review()
                elif choice == "6":
                    await self._demo_student_support()
                else:
                    print("Invalid choice. Please select 1-7.")
                
                print("\n" + "="*60 + "\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("Thank you for using CollegiumAI Educational Assistant!")
    
    async def _demo_academic_advising(self):
        """Demo academic advising functionality"""
        print("📚 Academic Advising Demo")
        print("-" * 30)
        
        # Sample student context
        student_context = {
            'major': 'Computer Science',
            'year': 'sophomore',
            'interests': ['artificial intelligence', 'web development']
        }
        
        query = "I'm interested in both AI and web development. Should I focus on one area or can I pursue both? What courses would help me with both interests?"
        
        print(f"Student Query: {query}")
        print(f"Student Context: {student_context}")
        print("\nAdvice:")
        
        advice = await self.provide_academic_advice(query, student_context)
        print(advice)
    
    async def _demo_research_assistance(self):
        """Demo research assistance functionality"""
        print("🔬 Research Assistance Demo")
        print("-" * 30)
        
        query = "I want to research the impact of AI on personalized learning in higher education. What methodology should I use and what existing literature should I review?"
        domain = "Educational Technology"
        
        print(f"Research Query: {query}")
        print(f"Domain: {domain}")
        print("\nResearch Guidance:")
        
        guidance = await self.assist_with_research(query, domain)
        print(guidance)
    
    async def _demo_tutoring(self):
        """Demo tutoring functionality"""
        print("👨‍🏫 Tutoring Demo")
        print("-" * 30)
        
        subject = "Data Structures"
        question = "I'm confused about when to use a hash table versus a binary search tree. Can you explain the differences and when each is most appropriate?"
        level = "intermediate"
        
        print(f"Subject: {subject}")
        print(f"Student Question: {question}")
        print(f"Level: {level}")
        print("\nTutoring Response:")
        
        response = await self.provide_tutoring(subject, question, level)
        print(response)
    
    async def _demo_content_creation(self):
        """Demo content creation with streaming"""
        print("🎨 Content Creation Demo")
        print("-" * 30)
        
        content_type = "lesson plan"
        topic = "Introduction to Machine Learning"
        audience = "undergraduate students"
        
        print(f"Content Type: {content_type}")
        print(f"Topic: {topic}")
        print(f"Audience: {audience}")
        print()
        
        content = await self.create_educational_content(content_type, topic, audience)
    
    async def _demo_code_review(self):
        """Demo code review functionality"""
        print("💻 Code Review Demo")
        print("-" * 30)
        
        code = """
def calculate_grade(scores):
    total = 0
    for score in scores:
        total = total + score
    average = total / len(scores)
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'
"""
        
        language = "Python"
        context = "intro programming course"
        
        print(f"Language: {language}")
        print(f"Assignment Context: {context}")
        print(f"Code to Review:\n{code}")
        print("\nCode Review:")
        
        review = await self.review_student_code(code, language, context)
        print(review)
    
    async def _demo_student_support(self):
        """Demo student support functionality"""
        print("🤝 Student Support Demo")
        print("-" * 30)
        
        concern = "I'm feeling overwhelmed with my course load this semester. I have three major projects due in the same week and I'm not sure how to manage my time effectively."
        support_type = "academic stress"
        
        print(f"Student Concern: {concern}")
        print(f"Support Type: {support_type}")
        print("\nSupport Response:")
        
        support = await self.provide_student_support(concern, support_type)
        print(support)

async def main():
    """Main application entry point"""
    
    # Initialize the educational assistant
    assistant = await EducationalAssistant().initialize()
    
    # Show system status
    print("\n📊 System Status:")
    status = await assistant.llm_manager.get_provider_status()
    active_providers = [name for name, info in status.items() if info.get('enabled', False)]
    print(f"Active Providers: {', '.join(active_providers) if active_providers else 'None'}")
    
    models = await assistant.llm_manager.get_available_models()
    print(f"Available Models: {len(models)}")
    print()
    
    # Run interactive session
    await assistant.interactive_session()
    
    # Show usage statistics
    print("\n📈 Session Statistics:")
    stats = await assistant.llm_manager.get_usage_statistics()
    if stats:
        total_requests = sum(stat.request_count for stat in stats.values())
        total_tokens = sum(stat.total_tokens for stat in stats.values())
        total_cost = sum(stat.total_cost for stat in stats.values())
        
        print(f"Total Requests: {total_requests}")
        print(f"Total Tokens: {total_tokens:,}")
        print(f"Total Cost: ${total_cost:.4f}")
    else:
        print("No usage data available")

if __name__ == "__main__":
    asyncio.run(main())