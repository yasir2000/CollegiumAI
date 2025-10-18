#!/usr/bin/env python3
"""
CollegiumAI - Main Integration Wrapper
Comprehensive university AI assistant with advanced cognitive architecture
"""

import asyncio
import argparse
import logging
from pathlib import Path
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

# Import CollegiumAI components
from framework.cognitive import (
    CognitivePersonaFactory, PersonaType, 
    CognitiveEngine, PersonaCognitiveAgent
)
from multi_agent_system import MultiAgentOrchestrator, AutonomousAgent
from cognitive_architecture_demo import CognitiveArchitectureDemo
from comprehensive_test_suite import CollegiumAITestSuite

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Mock OllamaClient for main system
class MockOllamaClient:
    """Mock Ollama client for main system"""
    
    async def generate_response(self, prompt: str, model: str = "llama2", **kwargs):
        return {
            "response": f"I understand you're asking about: {prompt[:100]}... Let me help you with that.",
            "model": model,
            "done": True
        }
    
    async def chat(self, messages: list, model: str = "llama2", **kwargs):
        last_message = messages[-1] if messages else {"content": "Hello"}
        return {
            "message": {
                "role": "assistant",
                "content": f"I can help you with: {last_message.get('content', 'your request')}"
            },
            "done": True
        }


class CollegiumAI:
    """
    Main CollegiumAI system integrating cognitive architecture,
    multi-agent collaboration, and persona-specific intelligence
    """
    
    def __init__(self):
        self.persona_factory = CognitivePersonaFactory()
        # Create mock client for the main system
        mock_client = MockOllamaClient()
        self.multi_agent_system = MultiAgentOrchestrator(mock_client)
        self.cognitive_demo = CognitiveArchitectureDemo()
        self.active_personas = {}
        self.session_history = []
        self.system_initialized = False
        
        # System configuration
        self.config = {
            "max_concurrent_requests": 10,
            "session_timeout": 3600,  # 1 hour
            "logging_level": "INFO",
            "enable_learning": True,
            "enable_multi_agent": True
        }
    
    async def initialize_system(self):
        """Initialize the complete CollegiumAI system"""
        
        logger.info("🚀 Initializing CollegiumAI System...")
        
        try:
            # Initialize multi-agent system
            if self.config["enable_multi_agent"]:
                await self.multi_agent_system.initialize()
                logger.info("✅ Multi-agent system initialized")
            
            # Pre-create common personas for faster response
            common_personas = [
                PersonaType.UNDERGRAD_STUDENT,
                PersonaType.GRAD_STUDENT,
                PersonaType.PROFESSOR,
                PersonaType.ACADEMIC_ADVISOR,
                PersonaType.TEACHING_ASSISTANT
            ]
            
            for persona_type in common_personas:
                persona = await self.persona_factory.create_persona_agent(persona_type)
                self.active_personas[persona_type.value] = persona
                logger.info(f"✅ {persona_type.value} persona ready")
            
            self.system_initialized = True
            logger.info("🎉 CollegiumAI system fully initialized")
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            raise
    
    async def get_persona_agent(self, persona_type: str) -> PersonaCognitiveAgent:
        """Get or create a persona agent"""
        
        if persona_type in self.active_personas:
            return self.active_personas[persona_type]
        
        # Create new persona if not cached
        try:
            persona_enum = PersonaType(persona_type)
            persona = await self.persona_factory.create_persona_agent(persona_enum)
            self.active_personas[persona_type] = persona
            return persona
        except ValueError:
            logger.error(f"Unknown persona type: {persona_type}")
            # Default to undergraduate student
            return self.active_personas.get("undergrad_student")
    
    async def process_request(
        self,
        request: str,
        persona_type: str = "undergrad_student",
        context: Optional[Dict[str, Any]] = None,
        use_multi_agent: bool = False
    ) -> Dict[str, Any]:
        """Process a user request through the cognitive system"""
        
        if not self.system_initialized:
            await self.initialize_system()
        
        logger.info(f"Processing request for {persona_type}: {request[:100]}...")
        
        try:
            # Record session data
            session_data = {
                "timestamp": datetime.now().isoformat(),
                "request": request,
                "persona_type": persona_type,
                "context": context or {},
                "use_multi_agent": use_multi_agent
            }
            
            if use_multi_agent and self.config["enable_multi_agent"]:
                # Use multi-agent collaboration
                task = {
                    "type": "user_support",
                    "description": request,
                    "persona_context": persona_type,
                    "context": context or {}
                }
                
                result = await self.multi_agent_system.coordinate_task(task)
                response = {
                    "response": result.get("results", "Multi-agent processing completed"),
                    "confidence": result.get("confidence", 0.8),
                    "processing_type": "multi_agent",
                    "agents_involved": result.get("participating_agents", []),
                    "workflow_status": result.get("workflow_status", "completed")
                }
                
            else:
                # Use single persona agent
                persona = await self.get_persona_agent(persona_type)
                result = await persona.process_request(request)
                
                response = {
                    "response": result.get("response", "Request processed successfully"),
                    "confidence": result.get("confidence", 0.7),
                    "processing_type": "single_agent",
                    "persona_used": persona_type,
                    "cognitive_insights": result.get("cognitive_insights", {}),
                    "support_assessment": result.get("support_assessment", {})
                }
            
            # Add session data to response
            session_data["result"] = response
            session_data["success"] = True
            self.session_history.append(session_data)
            
            logger.info(f"✅ Request processed successfully with confidence {response['confidence']:.2f}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Request processing failed: {e}")
            
            error_response = {
                "response": f"I apologize, but I encountered an error processing your request: {str(e)}",
                "confidence": 0.0,
                "processing_type": "error",
                "error": str(e)
            }
            
            session_data["result"] = error_response
            session_data["success"] = False
            self.session_history.append(session_data)
            
            return error_response
    
    async def run_interactive_session(self):
        """Run an interactive session with the user"""
        
        print("🎓 Welcome to CollegiumAI - Your Intelligent University Assistant")
        print("=" * 60)
        print("I provide personalized academic support using advanced cognitive AI.")
        print("Type 'help' for available commands or 'quit' to exit.\n")
        
        # Initialize system
        await self.initialize_system()
        
        # Available persona types
        available_personas = list(self.active_personas.keys())
        current_persona = "undergrad_student"
        
        while True:
            try:
                print(f"\n[{current_persona}] Enter your request:")
                user_input = input("> ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'quit':
                    print("👋 Thank you for using CollegiumAI!")
                    break
                
                elif user_input.lower() == 'help':
                    await self._show_help(available_personas)
                    continue
                
                elif user_input.lower().startswith('persona '):
                    new_persona = user_input[8:].strip()
                    if new_persona in available_personas:
                        current_persona = new_persona
                        print(f"✅ Switched to {current_persona} persona")
                    else:
                        print(f"❌ Unknown persona. Available: {', '.join(available_personas)}")
                    continue
                
                elif user_input.lower() == 'multi-agent':
                    print("🤖 Switching to multi-agent mode for complex request...")
                    print("Enter your complex request:")
                    complex_request = input("> ").strip()
                    if complex_request:
                        result = await self.process_request(
                            complex_request,
                            current_persona,
                            use_multi_agent=True
                        )
                        self._display_response(result)
                    continue
                
                elif user_input.lower() == 'demo':
                    print("🎮 Running cognitive architecture demonstration...")
                    await self.cognitive_demo.run_comprehensive_demo()
                    continue
                
                elif user_input.lower() == 'stats':
                    self._show_session_stats()
                    continue
                
                # Process regular request
                result = await self.process_request(user_input, current_persona)
                self._display_response(result)
                
            except KeyboardInterrupt:
                print("\n👋 Session interrupted. Thank you for using CollegiumAI!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Interactive session error: {e}")
    
    async def _show_help(self, available_personas: List[str]):
        """Show help information"""
        
        print("\n📚 CollegiumAI Help")
        print("-" * 30)
        print("Commands:")
        print("  help          - Show this help message")
        print("  quit          - Exit the system")
        print("  demo          - Run cognitive architecture demo")
        print("  multi-agent   - Use multi-agent collaboration")
        print("  stats         - Show session statistics")
        print("  persona <type> - Switch persona")
        print("\nAvailable Personas:")
        for persona in available_personas:
            print(f"  • {persona}")
        print("\nExample requests:")
        print("  • I need help with my calculus homework")
        print("  • How do I write a research proposal?")
        print("  • I'm feeling overwhelmed with my coursework")
        print("  • Can you help me plan my thesis research?")
    
    def _display_response(self, result: Dict[str, Any]):
        """Display a formatted response"""
        
        print("\n" + "="*50)
        print("🤖 CollegiumAI Response:")
        print("-" * 25)
        print(result.get("response", "No response generated"))
        
        # Show additional details
        confidence = result.get("confidence", 0)
        print(f"\n📊 Confidence: {confidence:.1%}")
        
        if result.get("processing_type") == "multi_agent":
            agents = result.get("agents_involved", [])
            if agents:
                print(f"🤝 Agents involved: {', '.join(agents)}")
        
        # Show cognitive insights if available
        insights = result.get("cognitive_insights", {})
        if insights:
            print(f"🧠 Cognitive insights: {len(insights)} insights generated")
        
        # Show support assessment if available
        assessment = result.get("support_assessment", {})
        if assessment and "support_types" in assessment:
            support_types = assessment["support_types"]
            print(f"🎯 Support types identified: {', '.join(support_types)}")
    
    def _show_session_stats(self):
        """Show session statistics"""
        
        if not self.session_history:
            print("📊 No session data available")
            return
        
        total_requests = len(self.session_history)
        successful_requests = sum(1 for s in self.session_history if s.get("success", False))
        
        # Calculate average confidence
        confidences = [
            s["result"].get("confidence", 0) 
            for s in self.session_history 
            if s.get("success", False)
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Count persona usage
        persona_counts = {}
        for session in self.session_history:
            persona = session.get("persona_type", "unknown")
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
        
        print("\n📊 Session Statistics")
        print("-" * 25)
        print(f"Total requests: {total_requests}")
        print(f"Successful requests: {successful_requests}")
        print(f"Success rate: {(successful_requests/total_requests)*100:.1f}%")
        print(f"Average confidence: {avg_confidence:.1%}")
        print("\nPersona usage:")
        for persona, count in persona_counts.items():
            print(f"  • {persona}: {count} requests")
    
    async def run_batch_processing(self, requests_file: str):
        """Process requests from a file"""
        
        try:
            with open(requests_file, 'r') as f:
                batch_data = json.load(f)
            
            print(f"📁 Processing {len(batch_data)} requests from {requests_file}")
            
            await self.initialize_system()
            
            results = []
            for i, request_data in enumerate(batch_data, 1):
                print(f"Processing request {i}/{len(batch_data)}...")
                
                result = await self.process_request(
                    request_data.get("request", ""),
                    request_data.get("persona_type", "undergrad_student"),
                    request_data.get("context"),
                    request_data.get("use_multi_agent", False)
                )
                
                results.append({
                    "request_id": i,
                    "original_request": request_data,
                    "result": result
                })
            
            # Save results
            output_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"✅ Batch processing completed. Results saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            print(f"❌ Batch processing error: {e}")


async def main():
    """Main entry point for CollegiumAI"""
    
    parser = argparse.ArgumentParser(description="CollegiumAI - Intelligent University Assistant")
    parser.add_argument("--mode", choices=["interactive", "demo", "test", "batch"], 
                       default="interactive", help="Operation mode")
    parser.add_argument("--persona", default="undergrad_student", 
                       help="Default persona type")
    parser.add_argument("--batch-file", help="File containing batch requests (JSON)")
    parser.add_argument("--config", help="Configuration file (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize CollegiumAI
    collegium_ai = CollegiumAI()
    
    # Load configuration if provided
    if args.config:
        try:
            with open(args.config, 'r') as f:
                collegium_ai.config.update(json.load(f))
            print(f"✅ Configuration loaded from {args.config}")
        except Exception as e:
            print(f"⚠️ Failed to load configuration: {e}")
    
    try:
        if args.mode == "interactive":
            await collegium_ai.run_interactive_session()
        
        elif args.mode == "demo":
            print("🎮 Running CollegiumAI Cognitive Architecture Demo")
            demo = CognitiveArchitectureDemo()
            await demo.run_comprehensive_demo()
        
        elif args.mode == "test":
            print("🧪 Running CollegiumAI Comprehensive Test Suite")
            test_suite = CollegiumAITestSuite()
            await test_suite.run_all_tests()
        
        elif args.mode == "batch":
            if not args.batch_file:
                print("❌ Batch mode requires --batch-file argument")
                return
            await collegium_ai.run_batch_processing(args.batch_file)
        
    except KeyboardInterrupt:
        print("\n👋 CollegiumAI session ended by user")
    except Exception as e:
        logger.error(f"CollegiumAI error: {e}")
        print(f"❌ System error: {e}")


if __name__ == "__main__":
    asyncio.run(main())