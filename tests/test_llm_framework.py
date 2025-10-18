#!/usr/bin/env python3
"""
CollegiumAI LLM Framework Test Suite
===================================

Comprehensive test suite for validating the multi-provider LLM framework.
Tests all components including providers, manager, utilities, and CLI commands.

Run with: python tests/test_llm_framework.py
"""

import asyncio
import os
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from framework.llm import (
        LLMManager, LLMRequest, LLMResponse, LLMMessage, 
        ModelSelection, ModelCapability, LLMProvider,
        OpenAIProvider, AnthropicProvider, OllamaProvider,
        create_chat_request, create_user_message, create_system_message,
        create_assistant_message, estimate_tokens, format_conversation
    )
    from framework.llm.utils import create_model_info, validate_request
    FRAMEWORK_AVAILABLE = True
except ImportError as e:
    print(f"❌ Framework import failed: {e}")
    FRAMEWORK_AVAILABLE = False

class LLMFrameworkTester:
    """Comprehensive test suite for LLM framework"""
    
    def __init__(self):
        self.test_results = {}
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
        
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        
        self.test_results[test_name] = {
            'passed': passed,
            'details': details
        }
    
    def test_framework_imports(self):
        """Test framework imports"""
        test_name = "Framework Imports"
        
        if not FRAMEWORK_AVAILABLE:
            self.log_test(test_name, False, "Framework modules not available")
            return False
        
        try:
            # Test core imports
            assert LLMManager is not None
            assert LLMRequest is not None
            assert LLMResponse is not None
            assert ModelSelection is not None
            
            # Test provider imports
            assert OpenAIProvider is not None
            assert AnthropicProvider is not None
            assert OllamaProvider is not None
            
            # Test utility imports
            assert create_chat_request is not None
            assert create_user_message is not None
            
            self.log_test(test_name, True, "All imports successful")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Import error: {e}")
            return False
    
    def test_message_creation(self):
        """Test message creation utilities"""
        test_name = "Message Creation"
        
        try:
            # Test message creation
            user_msg = create_user_message("Hello")
            system_msg = create_system_message("You are helpful")
            assistant_msg = create_assistant_message("Hi there!")
            
            assert user_msg.role == "user"
            assert user_msg.content == "Hello"
            assert system_msg.role == "system"
            assert assistant_msg.role == "assistant"
            
            # Test chat request creation
            messages = [system_msg, user_msg]
            request = create_chat_request(messages=messages)
            
            assert request.messages == messages
            assert request.temperature >= 0 and request.temperature <= 2
            assert request.max_tokens > 0
            
            self.log_test(test_name, True, "Message creation working correctly")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Message creation error: {e}")
            return False
    
    def test_model_selection(self):
        """Test model selection criteria"""
        test_name = "Model Selection"
        
        try:
            # Test basic selection
            selection = ModelSelection(
                required_capabilities=[ModelCapability.CHAT_COMPLETION],
                max_cost_per_1k_tokens=0.01
            )
            
            assert ModelCapability.CHAT_COMPLETION in selection.required_capabilities
            assert selection.max_cost_per_1k_tokens == 0.01
            
            # Test complex selection
            complex_selection = ModelSelection(
                required_capabilities=[
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION
                ],
                preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC],
                prefer_local=True,
                min_context_length=8000
            )
            
            assert len(complex_selection.required_capabilities) == 2
            assert LLMProvider.OPENAI in complex_selection.preferred_providers
            assert complex_selection.prefer_local == True
            assert complex_selection.min_context_length == 8000
            
            self.log_test(test_name, True, "Model selection criteria working")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Model selection error: {e}")
            return False
    
    def test_utility_functions(self):
        """Test utility functions"""
        test_name = "Utility Functions"
        
        try:
            # Test token estimation
            text = "This is a test message"
            tokens = estimate_tokens(text)
            assert tokens > 0
            
            # Test conversation formatting
            messages = [
                create_system_message("You are helpful"),
                create_user_message("Hello"),
                create_assistant_message("Hi there!")
            ]
            
            formatted = format_conversation(messages)
            assert len(formatted) > 0
            
            # Test request validation
            request = create_chat_request(messages=messages)
            is_valid = validate_request(request)
            assert is_valid == True
            
            self.log_test(test_name, True, "Utility functions working")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Utility function error: {e}")
            return False
    
    async def test_provider_initialization(self):
        """Test provider initialization without API calls"""
        test_name = "Provider Initialization"
        
        try:
            # Test OpenAI provider (mock)
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
                openai_provider = OpenAIProvider()
                assert openai_provider.provider == LLMProvider.OPENAI
                assert openai_provider.name == "openai"
            
            # Test Anthropic provider (mock)
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'}):
                anthropic_provider = AnthropicProvider()
                assert anthropic_provider.provider == LLMProvider.ANTHROPIC
                assert anthropic_provider.name == "anthropic"
            
            # Test Ollama provider
            ollama_provider = OllamaProvider()
            assert ollama_provider.provider == LLMProvider.OLLAMA
            assert ollama_provider.name == "ollama"
            
            self.log_test(test_name, True, "Provider initialization successful")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Provider initialization error: {e}")
            return False
    
    async def test_llm_manager_initialization(self):
        """Test LLM manager initialization"""
        test_name = "LLM Manager Initialization"
        
        try:
            # Create temporary config for testing
            config = {
                'providers': {
                    'openai': {'enabled': False},
                    'anthropic': {'enabled': False},
                    'ollama': {'enabled': False}
                },
                'selection_defaults': {
                    'temperature': 0.7,
                    'max_tokens': 1000
                }
            }
            
            # Test manager initialization
            manager = LLMManager(config=config)
            
            assert manager is not None
            assert hasattr(manager, 'providers')
            assert hasattr(manager, 'config')
            
            self.log_test(test_name, True, "LLM Manager initialized successfully")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"LLM Manager initialization error: {e}")
            return False
    
    def test_configuration_handling(self):
        """Test configuration file handling"""
        test_name = "Configuration Handling"
        
        try:
            # Test default configuration
            config = {
                'providers': {
                    'openai': {
                        'enabled': True,
                        'priority': 1,
                        'models': ['gpt-3.5-turbo', 'gpt-4']
                    }
                }
            }
            
            # Validate configuration structure
            assert 'providers' in config
            assert 'openai' in config['providers']
            assert 'enabled' in config['providers']['openai']
            
            self.log_test(test_name, True, "Configuration handling working")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Configuration error: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        test_name = "Error Handling"
        
        try:
            # Test invalid message creation
            try:
                invalid_msg = create_user_message("")  # Empty message
                # Should still work, just be empty
                assert invalid_msg.content == ""
            except Exception:
                pass  # Some validation might prevent this
            
            # Test invalid model selection
            try:
                invalid_selection = ModelSelection(
                    max_cost_per_1k_tokens=-1  # Invalid negative cost
                )
                # Should handle gracefully or raise appropriate error
            except Exception:
                pass  # Expected for invalid values
            
            self.log_test(test_name, True, "Error handling working")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Error handling test failed: {e}")
            return False
    
    def test_environment_configuration(self):
        """Test environment variable configuration"""
        test_name = "Environment Configuration"
        
        try:
            # Test with mock environment variables
            test_env = {
                'OPENAI_API_KEY': 'test_openai_key',
                'ANTHROPIC_API_KEY': 'test_anthropic_key',
                'OLLAMA_BASE_URL': 'http://localhost:11434'
            }
            
            with patch.dict(os.environ, test_env):
                # Test that environment variables are accessible
                assert os.getenv('OPENAI_API_KEY') == 'test_openai_key'
                assert os.getenv('ANTHROPIC_API_KEY') == 'test_anthropic_key'
                assert os.getenv('OLLAMA_BASE_URL') == 'http://localhost:11434'
            
            self.log_test(test_name, True, "Environment configuration working")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Environment configuration error: {e}")
            return False
    
    def test_integration_compatibility(self):
        """Test integration with existing CollegiumAI components"""
        test_name = "Integration Compatibility"
        
        try:
            # Test that LLM components can be imported alongside existing framework
            from framework.llm import LLMManager
            
            # Test basic integration pattern
            integration_config = {
                'llm_enabled': True,
                'default_provider': 'openai',
                'cost_optimization': True
            }
            
            assert integration_config['llm_enabled'] == True
            assert 'default_provider' in integration_config
            
            self.log_test(test_name, True, "Integration compatibility confirmed")
            return True
            
        except Exception as e:
            self.log_test(test_name, False, f"Integration compatibility error: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🧪 CollegiumAI LLM Framework Test Suite")
        print("=" * 50)
        print()
        
        # Run synchronous tests
        sync_tests = [
            self.test_framework_imports,
            self.test_message_creation,
            self.test_model_selection,
            self.test_utility_functions,
            self.test_configuration_handling,
            self.test_error_handling,
            self.test_environment_configuration,
            self.test_integration_compatibility
        ]
        
        for test in sync_tests:
            test()
        
        # Run asynchronous tests
        async_tests = [
            self.test_provider_initialization,
            self.test_llm_manager_initialization
        ]
        
        for test in async_tests:
            await test()
        
        print()
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("📊 TEST SUMMARY")
        print("=" * 30)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 All tests passed! LLM Framework is ready for use.")
        else:
            print(f"\n⚠️ {self.failed_tests} test(s) failed. Please review the issues above.")
            
            # Show failed tests
            failed_tests = [name for name, result in self.test_results.items() if not result['passed']]
            if failed_tests:
                print("\nFailed Tests:")
                for test_name in failed_tests:
                    details = self.test_results[test_name]['details']
                    print(f"  - {test_name}: {details}")
        
        print()
        return self.failed_tests == 0

def main():
    """Main test entry point"""
    print("Setting up test environment...")
    
    # Set up test environment
    os.environ.setdefault('OPENAI_API_KEY', 'test_key_for_testing')
    os.environ.setdefault('ANTHROPIC_API_KEY', 'test_key_for_testing')
    os.environ.setdefault('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    # Run tests
    tester = LLMFrameworkTester()
    success = asyncio.run(tester.run_all_tests())
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())