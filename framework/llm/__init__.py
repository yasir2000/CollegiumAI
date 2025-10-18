"""
CollegiumAI LLM Framework
========================

Multi-provider LLM system supporting OpenAI, Anthropic, Google, HuggingFace,
Azure OpenAI, AWS Bedrock, and local models via Ollama with intelligent
routing, load balancing, and cost optimization.

Key Features:
- Multiple LLM provider support (OpenAI, Anthropic, Ollama, etc.)
- Intelligent model selection and routing
- Load balancing and fallback mechanisms
- Cost optimization and usage tracking
- Rate limiting and quota management
- Local model support via Ollama
- Streaming completions
- Function calling capabilities
- Vision model support
- Embeddings generation

Example Usage:
    ```python
    from framework.llm import LLMManager, LLMRequest, LLMMessage, ModelSelection, ModelCapability
    
    # Initialize LLM manager
    llm_manager = LLMManager()
    await llm_manager.initialize()
    
    # Create a request
    request = LLMRequest(
        messages=[
            LLMMessage(role="system", content="You are a helpful academic advisor."),
            LLMMessage(role="user", content="What courses should I take for AI?")
        ],
        temperature=0.7
    )
    
    # Generate completion with automatic provider selection
    response = await llm_manager.generate_completion(request)
    print(response.content)
    
    # Use specific criteria for model selection
    criteria = ModelSelection(
        required_capabilities=[ModelCapability.CHAT_COMPLETION],
        prefer_local=True,
        max_cost_per_1k_tokens=0.01
    )
    
    response = await llm_manager.generate_completion(request, criteria)
    ```

Provider Configuration:
    ```yaml
    providers:
      openai:
        config:
          api_key: "your-openai-key"
        priority: 3
        enabled: true
        max_requests_per_minute: 60
        
      anthropic:
        config:
          api_key: "your-anthropic-key"
        priority: 2
        enabled: true
        
      ollama:
        config:
          base_url: "http://localhost:11434"
        priority: 1
        enabled: true
        fallback_providers: ["openai", "anthropic"]
    ```
"""

from .providers import (
    BaseLLMProvider,
    OpenAIProvider,
    AnthropicProvider,
    OllamaProvider,
    LLMProvider,
    ModelCapability,
    ModelInfo,
    LLMMessage,
    LLMRequest,
    LLMResponse
)

from .manager import (
    LLMManager,
    ProviderConfig,
    ModelSelection,
    UsageStats
)

# Convenience imports for common use cases
from .utils import (
    create_chat_request,
    create_system_message,
    create_user_message,
    create_assistant_message,
    estimate_tokens,
    format_conversation
)

__all__ = [
    # Core classes
    "LLMManager",
    "BaseLLMProvider",
    "LLMRequest",
    "LLMResponse",
    "LLMMessage",
    "ModelInfo",
    
    # Provider implementations
    "OpenAIProvider",
    "AnthropicProvider", 
    "OllamaProvider",
    
    # Configuration classes
    "ProviderConfig",
    "ModelSelection",
    "UsageStats",
    
    # Enums
    "LLMProvider",
    "ModelCapability",
    
    # Utility functions
    "create_chat_request",
    "create_system_message",
    "create_user_message", 
    "create_assistant_message",
    "estimate_tokens",
    "format_conversation"
]

# Version information
__version__ = "1.0.0"
__author__ = "CollegiumAI Team"
__description__ = "Multi-provider LLM framework with intelligent routing and optimization"

# Default configuration
DEFAULT_CONFIG = {
    "providers": {
        "openai": {
            "priority": 3,
            "enabled": True,
            "max_requests_per_minute": 60,
            "max_tokens_per_minute": 40000
        },
        "anthropic": {
            "priority": 2,
            "enabled": True,
            "max_requests_per_minute": 50,
            "max_tokens_per_minute": 30000
        },
        "ollama": {
            "priority": 1,
            "enabled": True,
            "max_requests_per_minute": 100,
            "max_tokens_per_minute": 50000,
            "fallback_providers": ["openai", "anthropic"]
        }
    },
    "default_selection_criteria": {
        "prefer_local": False,
        "max_cost_per_1k_tokens": 0.1,
        "required_capabilities": ["chat_completion"]
    }
}