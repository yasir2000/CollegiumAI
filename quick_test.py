#!/usr/bin/env python3
"""
CollegiumAI - Quick Integration Test
Simple test to validate core components are working
"""

import asyncio
import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

print("🧪 CollegiumAI Quick Integration Test")
print("=" * 50)

async def test_cognitive_core():
    """Test core cognitive engine"""
    print("\n1. Testing Cognitive Engine Import...")
    try:
        from framework.cognitive import CognitiveEngine
        engine = CognitiveEngine("test_persona")
        print("   ✅ Cognitive Engine: PASS")
        return True
    except Exception as e:
        print(f"   ❌ Cognitive Engine: FAIL - {e}")
        return False

async def test_persona_system():
    """Test persona system"""
    print("\n2. Testing Persona System...")
    try:
        from framework.cognitive import CognitivePersonaFactory, PersonaType
        factory = CognitivePersonaFactory()
        print("   ✅ Persona Factory: PASS")
        
        # Test persona creation
        persona = factory.create_agent(PersonaType.TRADITIONAL_STUDENT)
        print("   ✅ Persona Creation: PASS")
        return True
    except Exception as e:
        print(f"   ❌ Persona System: FAIL - {e}")
        return False

async def test_cognitive_processing():
    """Test basic cognitive processing"""
    print("\n3. Testing Cognitive Processing...")
    try:
        from framework.cognitive import CognitivePersonaFactory, PersonaType
        factory = CognitivePersonaFactory()
        student = factory.create_agent(PersonaType.TRADITIONAL_STUDENT)
        
        # Test basic request processing
        request_data = {
            "text": "I need help with my studies",
            "context": {"domain": "academic", "urgency": "medium"}
        }
        result = await student.process_intelligent_request(request_data)
        
        if result and isinstance(result, dict):
            confidence = result.get("confidence", 0)
            print(f"   ✅ Request Processing: PASS (confidence: {confidence:.2f})")
            return True
        else:
            print("   ❌ Request Processing: FAIL - Invalid result")
            return False
    except Exception as e:
        print(f"   ❌ Cognitive Processing: FAIL - {e}")
        return False

async def test_multi_agent_basic():
    """Test basic multi-agent system"""
    print("\n4. Testing Multi-Agent System...")
    try:
        from multi_agent_system import MultiAgentOrchestrator
        
        # Create mock ollama client
        class MockOllama:
            async def generate_response(self, prompt, **kwargs):
                return {"response": "Mock response", "done": True}
            async def chat(self, messages, **kwargs):
                return {"message": {"content": "Mock chat"}, "done": True}
        
        orchestrator = MultiAgentOrchestrator(MockOllama())
        # Initialization happens in constructor
        print(f"   ✅ Multi-Agent Initialization: PASS ({len(orchestrator.agents)} agents)")
        return True
    except Exception as e:
        print(f"   ❌ Multi-Agent System: FAIL - {e}")
        return False

async def test_demo_availability():
    """Test demo system availability"""
    print("\n5. Testing Demo System...")
    try:
        from cognitive_architecture_demo import CognitiveArchitectureDemo
        demo = CognitiveArchitectureDemo()
        print("   ✅ Demo System: PASS")
        return True
    except Exception as e:
        print(f"   ❌ Demo System: FAIL - {e}")
        return False

async def run_quick_tests():
    """Run all quick tests"""
    
    tests = [
        test_cognitive_core(),
        test_persona_system(),
        test_cognitive_processing(),
        test_multi_agent_basic(),
        test_demo_availability()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    passed = sum(1 for r in results if r is True)
    total = len(results)
    
    print(f"\n" + "=" * 50)
    print(f"🎯 QUICK TEST RESULTS")
    print(f"   Tests Passed: {passed}/{total}")
    print(f"   Success Rate: {(passed/total)*100:.1f}%")
    
    if passed >= 4:
        print(f"   Status: 🟢 READY FOR FULL TESTING")
        print(f"\n🚀 System is ready! Try:")
        print(f"   python main.py --mode interactive")
        print(f"   python main.py --mode demo")
        print(f"   python cognitive_architecture_demo.py")
    elif passed >= 2:
        print(f"   Status: 🟡 PARTIALLY READY")
        print(f"   Some components need attention")
    else:
        print(f"   Status: 🔴 NEEDS WORK")
        print(f"   Major components failing")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(run_quick_tests())