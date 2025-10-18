#!/usr/bin/env python3
"""
LLM Multi-Provider Demo
======================

Comprehensive demonstration of the CollegiumAI LLM framework with multiple
providers including OpenAI, Anthropic, and local models via Ollama.

This demo showcases:
- Multi-provider setup and configuration
- Intelligent model selection
- Fallback mechanisms
- Cost optimization
- Local model integration
- Real-world use cases
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent))

from framework.llm import (
    LLMManager, LLMRequest, LLMMessage, ModelSelection, 
    ModelCapability, LLMProvider, create_chat_request,
    create_system_message, create_user_message
)

class LLMDemo:
    """Comprehensive LLM framework demonstration"""
    
    def __init__(self):
        self.llm_manager = None
        self.demo_results = {}
    
    async def initialize(self):
        """Initialize the LLM manager"""
        print("🚀 Initializing LLM Manager...")
        
        # Use default configuration (environment variables)
        self.llm_manager = LLMManager()
        await self.llm_manager.initialize()
        
        print("✅ LLM Manager initialized successfully!")
        print()
    
    async def demo_provider_status(self):
        """Demonstrate provider status checking"""
        print("📊 PROVIDER STATUS DEMONSTRATION")
        print("=" * 50)
        
        # Get provider status
        status = await self.llm_manager.get_provider_status()
        
        for provider_name, provider_info in status.items():
            print(f"🔧 {provider_name.upper()}:")
            if provider_info.get('enabled', False):
                print(f"   Status: ✅ Enabled (Priority: {provider_info.get('priority', 'N/A')})")
                print(f"   Models: {provider_info.get('available_models', 0)}")
                print(f"   Rate Limits: {provider_info.get('requests_this_minute', 0)}/{provider_info.get('max_requests_per_minute', 'N/A')} req/min")
                if provider_info.get('models'):
                    print(f"   Sample Models: {', '.join(provider_info['models'][:3])}")
            else:
                error_msg = provider_info.get('error', 'Disabled')
                print(f"   Status: ❌ {error_msg}")
            print()
        
        self.demo_results['provider_status'] = status
    
    async def demo_model_listing(self):
        """Demonstrate model listing across providers"""
        print("🤖 MODEL LISTING DEMONSTRATION")
        print("=" * 50)
        
        # Get all available models
        models = await self.llm_manager.get_available_models()
        
        print(f"Found {len(models)} models across all providers:")
        print()
        
        # Group by provider
        by_provider = {}
        for model in models:
            provider = model.provider.value
            if provider not in by_provider:
                by_provider[provider] = []
            by_provider[provider].append(model)
        
        for provider, provider_models in by_provider.items():
            print(f"📡 {provider.upper()} ({len(provider_models)} models):")
            for model in provider_models[:3]:  # Show first 3
                cost_info = f"${model.cost_per_1k_tokens.get('input', 0):.4f}/1K" if model.cost_per_1k_tokens.get('input', 0) > 0 else "Free"
                local_indicator = "🏠" if model.is_local else "☁️"
                print(f"   {local_indicator} {model.name} - {model.context_length:,} tokens - {cost_info}")
            
            if len(provider_models) > 3:
                print(f"   ... and {len(provider_models) - 3} more models")
            print()
        
        self.demo_results['available_models'] = len(models)
    
    async def demo_intelligent_selection(self):
        """Demonstrate intelligent model selection"""
        print("🧠 INTELLIGENT MODEL SELECTION DEMONSTRATION")
        print("=" * 50)
        
        # Test different selection criteria
        test_cases = [
            {
                "name": "Cost-Optimized Selection",
                "criteria": ModelSelection(
                    max_cost_per_1k_tokens=0.01,
                    required_capabilities=[ModelCapability.CHAT_COMPLETION]
                ),
                "prompt": "What is artificial intelligence?"
            },
            {
                "name": "Local Model Preference",
                "criteria": ModelSelection(
                    prefer_local=True,
                    required_capabilities=[ModelCapability.CHAT_COMPLETION]
                ),
                "prompt": "Explain machine learning in simple terms."
            },
            {
                "name": "High-Capability Model",
                "criteria": ModelSelection(
                    required_capabilities=[
                        ModelCapability.CHAT_COMPLETION,
                        ModelCapability.CODE_GENERATION
                    ],
                    preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
                ),
                "prompt": "Write a Python function to calculate fibonacci numbers."
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. {test_case['name']}:")
            
            try:
                # Create request
                messages = [
                    create_system_message("You are a helpful AI assistant."),
                    create_user_message(test_case['prompt'])
                ]
                
                request = create_chat_request(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=150
                )
                
                # Generate response with selection criteria
                start_time = datetime.now()
                response = await self.llm_manager.generate_completion(
                    request, test_case['criteria']
                )
                end_time = datetime.now()
                
                latency = (end_time - start_time).total_seconds()
                
                print(f"   Model Selected: {response.model} ({response.provider.value})")
                print(f"   Response Time: {latency:.2f}s")
                print(f"   Tokens Used: {response.usage.get('total_tokens', 0)}")
                print(f"   Response Preview: {response.content[:100]}...")
                print()
                
                # Store results
                self.demo_results[f'test_case_{i}'] = {
                    'model': response.model,
                    'provider': response.provider.value,
                    'latency': latency,
                    'tokens': response.usage.get('total_tokens', 0)
                }
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
    
    async def demo_streaming_completion(self):
        """Demonstrate streaming completion"""
        print("📡 STREAMING COMPLETION DEMONSTRATION")
        print("=" * 50)
        
        # Create streaming request
        messages = [
            create_system_message("You are a creative writing assistant."),
            create_user_message("Write a short story about a robot learning to paint.")
        ]
        
        request = create_chat_request(
            messages=messages,
            temperature=0.8,
            max_tokens=300
        )
        
        # Selection criteria for streaming
        criteria = ModelSelection(
            require_streaming=True,
            preferred_providers=[LLMProvider.OPENAI, LLMProvider.OLLAMA]
        )
        
        print("🎨 Creative Story Generation (Streaming):")
        print("-" * 40)
        
        try:
            start_time = datetime.now()
            full_response = ""
            
            async for chunk in self.llm_manager.generate_streaming_completion(request, criteria):
                print(chunk, end="", flush=True)
                full_response += chunk
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds()
            
            print(f"\n\n⏱️ Streaming completed in {latency:.2f}s")
            print(f"📊 Generated {len(full_response)} characters")
            
            self.demo_results['streaming_demo'] = {
                'latency': latency,
                'characters': len(full_response)
            }
            
        except Exception as e:
            print(f"❌ Streaming error: {e}")
        
        print("\n")
    
    async def demo_fallback_mechanism(self):
        """Demonstrate fallback mechanisms"""
        print("🔄 FALLBACK MECHANISM DEMONSTRATION")
        print("=" * 50)
        
        # Create a request that might fail on primary provider
        messages = [
            create_system_message("You are a helpful assistant."),
            create_user_message("What's the weather like today?")
        ]
        
        request = create_chat_request(messages=messages)
        
        # Try with different providers to test fallback
        print("Testing fallback behavior:")
        
        try:
            response = await self.llm_manager.generate_completion(request)
            print(f"✅ Primary provider succeeded: {response.provider.value} - {response.model}")
            
            self.demo_results['fallback_test'] = {
                'success': True,
                'provider': response.provider.value,
                'model': response.model
            }
            
        except Exception as e:
            print(f"❌ All providers failed: {e}")
            self.demo_results['fallback_test'] = {'success': False, 'error': str(e)}
        
        print()
    
    async def demo_usage_statistics(self):
        """Demonstrate usage statistics"""
        print("📈 USAGE STATISTICS DEMONSTRATION")
        print("=" * 50)
        
        stats = await self.llm_manager.get_usage_statistics()
        
        if stats:
            print("Usage Statistics:")
            total_requests = 0
            total_tokens = 0
            total_cost = 0
            
            for key, stat in stats.items():
                print(f"🔧 {stat.provider.value}:{stat.model}")
                print(f"   Requests: {stat.request_count}")
                print(f"   Tokens: {stat.total_tokens:,}")
                print(f"   Cost: ${stat.total_cost:.4f}")
                print(f"   Avg Latency: {stat.avg_latency:.2f}s")
                print(f"   Errors: {stat.error_count}")
                print()
                
                total_requests += stat.request_count
                total_tokens += stat.total_tokens
                total_cost += stat.total_cost
            
            print(f"📊 TOTALS:")
            print(f"   Total Requests: {total_requests}")
            print(f"   Total Tokens: {total_tokens:,}")
            print(f"   Total Cost: ${total_cost:.4f}")
            
            self.demo_results['usage_stats'] = {
                'total_requests': total_requests,
                'total_tokens': total_tokens,
                'total_cost': total_cost
            }
        else:
            print("No usage statistics available yet.")
        
        print()
    
    async def demo_health_check(self):
        """Demonstrate health checking"""
        print("🏥 HEALTH CHECK DEMONSTRATION")
        print("=" * 50)
        
        health = await self.llm_manager.health_check()
        
        if health['overall_healthy']:
            print("🟢 Overall System Health: HEALTHY")
        else:
            print("🔴 Overall System Health: UNHEALTHY")
        
        print(f"📊 Total Providers: {health['total_providers']}")
        print(f"✅ Healthy Providers: {health['healthy_providers']}")
        print()
        
        print("Provider Health Details:")
        for provider_name, provider_health in health['providers'].items():
            status_icon = "🟢" if provider_health['healthy'] else "🔴"
            print(f"{status_icon} {provider_name}:")
            
            if provider_health['healthy']:
                print(f"   Models Available: {provider_health.get('available_models', 0)}")
            else:
                print(f"   Error: {provider_health.get('error', 'Unknown')}")
            
            print(f"   Last Check: {provider_health.get('last_check', 'Never')}")
            print()
        
        self.demo_results['health_check'] = health
    
    async def demo_educational_use_cases(self):
        """Demonstrate educational AI use cases"""
        print("🎓 EDUCATIONAL USE CASES DEMONSTRATION")
        print("=" * 50)
        
        use_cases = [
            {
                "name": "Academic Advising",
                "system_prompt": "You are an expert academic advisor helping students plan their academic journey.",
                "user_prompt": "I'm a sophomore computer science student interested in AI. What courses should I take next semester?",
                "criteria": ModelSelection(
                    required_capabilities=[ModelCapability.CHAT_COMPLETION],
                    max_cost_per_1k_tokens=0.05
                )
            },
            {
                "name": "Research Paper Analysis",
                "system_prompt": "You are a research assistant specializing in academic literature analysis.",
                "user_prompt": "Summarize the key findings and methodology of a paper on 'Machine Learning in Educational Assessment'.",
                "criteria": ModelSelection(
                    required_capabilities=[ModelCapability.CHAT_COMPLETION],
                    preferred_providers=[LLMProvider.ANTHROPIC, LLMProvider.OPENAI]
                )
            },
            {
                "name": "Code Review for Students",
                "system_prompt": "You are a programming instructor providing constructive code review feedback.",
                "user_prompt": "Review this Python function for calculating GPA: def calculate_gpa(grades): return sum(grades) / len(grades)",
                "criteria": ModelSelection(
                    required_capabilities=[ModelCapability.CODE_GENERATION, ModelCapability.CHAT_COMPLETION],
                    prefer_local=False
                )
            }
        ]
        
        for i, use_case in enumerate(use_cases, 1):
            print(f"{i}. {use_case['name']}:")
            
            try:
                messages = [
                    create_system_message(use_case['system_prompt']),
                    create_user_message(use_case['user_prompt'])
                ]
                
                request = create_chat_request(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=200
                )
                
                response = await self.llm_manager.generate_completion(
                    request, use_case['criteria']
                )
                
                print(f"   Model: {response.model} ({response.provider.value})")
                print(f"   Response: {response.content[:150]}...")
                print()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
    
    async def run_comprehensive_demo(self):
        """Run the complete demonstration"""
        print("🎯 COLLEGIUMAI LLM FRAMEWORK COMPREHENSIVE DEMO")
        print("=" * 60)
        print("Multi-Provider AI with Intelligent Routing & Local Model Support")
        print("=" * 60)
        print()
        
        try:
            # Initialize
            await self.initialize()
            
            # Run all demonstrations
            await self.demo_provider_status()
            await self.demo_model_listing()
            await self.demo_intelligent_selection()
            await self.demo_streaming_completion()
            await self.demo_fallback_mechanism()
            await self.demo_educational_use_cases()
            await self.demo_usage_statistics()
            await self.demo_health_check()
            
            # Generate summary report
            await self.generate_summary_report()
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()
    
    async def generate_summary_report(self):
        """Generate a summary report of the demo"""
        print("📋 DEMO SUMMARY REPORT")
        print("=" * 50)
        
        print(f"Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Provider summary
        provider_status = self.demo_results.get('provider_status', {})
        active_providers = [name for name, info in provider_status.items() if info.get('enabled', False)]
        print(f"🔧 Active Providers: {len(active_providers)} ({', '.join(active_providers)})")
        
        # Model summary
        total_models = self.demo_results.get('available_models', 0)
        print(f"🤖 Available Models: {total_models}")
        
        # Usage summary
        usage_stats = self.demo_results.get('usage_stats', {})
        if usage_stats:
            print(f"📊 Demo Usage:")
            print(f"   Requests Made: {usage_stats.get('total_requests', 0)}")
            print(f"   Tokens Processed: {usage_stats.get('total_tokens', 0):,}")
            print(f"   Total Cost: ${usage_stats.get('total_cost', 0):.4f}")
        
        # Health summary
        health_check = self.demo_results.get('health_check', {})
        if health_check:
            print(f"🏥 System Health: {'✅ Healthy' if health_check.get('overall_healthy') else '❌ Issues Detected'}")
        
        print()
        print("🎉 Demo completed successfully!")
        print("🔍 Check the detailed output above for comprehensive results.")

def main():
    """Main demo entry point"""
    print("Setting up environment...")
    
    # Check for required environment variables
    required_vars = []
    optional_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'OLLAMA_BASE_URL']
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or environment.")
        return 1
    
    # Show available optional configurations
    available_configs = []
    for var in optional_vars:
        if os.getenv(var):
            available_configs.append(var)
    
    if available_configs:
        print(f"✅ Available configurations: {', '.join(available_configs)}")
    else:
        print("ℹ️ No API keys configured. The demo will use mock responses or show configuration examples.")
    
    print()
    
    # Run the demo
    demo = LLMDemo()
    return asyncio.run(demo.run_comprehensive_demo())

if __name__ == "__main__":
    exit(main())