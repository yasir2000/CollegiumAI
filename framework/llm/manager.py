"""
LLM Manager
===========

Central manager for coordinating multiple LLM providers with intelligent
model selection, load balancing, fallback mechanisms, and cost optimization.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, AsyncGenerator
from dataclasses import dataclass, field
from pathlib import Path
import yaml

from .providers import (
    BaseLLMProvider, OpenAIProvider, AnthropicProvider, OllamaProvider,
    LLMProvider, LLMRequest, LLMResponse, ModelInfo, ModelCapability
)

logger = logging.getLogger(__name__)

@dataclass
class ProviderConfig:
    """Configuration for an LLM provider"""
    provider_type: LLMProvider
    config: Dict[str, Any]
    priority: int = 1  # Higher number = higher priority
    enabled: bool = True
    max_requests_per_minute: int = 60
    max_tokens_per_minute: int = 40000
    fallback_providers: List[LLMProvider] = field(default_factory=list)

@dataclass
class ModelSelection:
    """Model selection criteria"""
    required_capabilities: List[ModelCapability] = field(default_factory=list)
    max_cost_per_1k_tokens: Optional[float] = None
    min_context_length: Optional[int] = None
    preferred_providers: List[LLMProvider] = field(default_factory=list)
    exclude_providers: List[LLMProvider] = field(default_factory=list)
    prefer_local: bool = False
    require_streaming: bool = False

@dataclass
class UsageStats:
    """Usage statistics for providers and models"""
    provider: LLMProvider
    model: str
    request_count: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    avg_latency: float = 0.0
    error_count: int = 0
    last_used: Optional[datetime] = None

class LLMManager:
    """
    Central manager for multiple LLM providers with intelligent routing,
    load balancing, fallback mechanisms, and cost optimization.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self.provider_configs: Dict[LLMProvider, ProviderConfig] = {}
        self.usage_stats: Dict[str, UsageStats] = {}  # key: f"{provider}:{model}"
        self.rate_limits: Dict[LLMProvider, Dict[str, Any]] = {}
        self._initialized = False
        
        # Load configuration
        if config_path and config_path.exists():
            self._load_config()
        else:
            self._load_default_config()
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.suffix.lower() == '.yaml':
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            self._parse_config(config_data)
            logger.info(f"Loaded LLM configuration from {self.config_path}")
            
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            self._load_default_config()
    
    def _load_default_config(self) -> None:
        """Load default configuration"""
        import os
        
        # Default provider configurations
        default_configs = {}
        
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            default_configs[LLMProvider.OPENAI] = ProviderConfig(
                provider_type=LLMProvider.OPENAI,
                config={"api_key": os.getenv("OPENAI_API_KEY")},
                priority=3,
                enabled=True
            )
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            default_configs[LLMProvider.ANTHROPIC] = ProviderConfig(
                provider_type=LLMProvider.ANTHROPIC,
                config={"api_key": os.getenv("ANTHROPIC_API_KEY")},
                priority=2,
                enabled=True
            )
        
        # Ollama (always try to enable for local models)
        default_configs[LLMProvider.OLLAMA] = ProviderConfig(
            provider_type=LLMProvider.OLLAMA,
            config={"base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")},
            priority=1,
            enabled=True,
            fallback_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
        )
        
        self.provider_configs = default_configs
        logger.info("Loaded default LLM configuration")
    
    def _parse_config(self, config_data: Dict[str, Any]) -> None:
        """Parse configuration data"""
        providers_config = config_data.get("providers", {})
        
        for provider_name, provider_data in providers_config.items():
            try:
                provider_type = LLMProvider(provider_name)
                
                self.provider_configs[provider_type] = ProviderConfig(
                    provider_type=provider_type,
                    config=provider_data.get("config", {}),
                    priority=provider_data.get("priority", 1),
                    enabled=provider_data.get("enabled", True),
                    max_requests_per_minute=provider_data.get("max_requests_per_minute", 60),
                    max_tokens_per_minute=provider_data.get("max_tokens_per_minute", 40000),
                    fallback_providers=[
                        LLMProvider(fp) for fp in provider_data.get("fallback_providers", [])
                    ]
                )
                
            except ValueError as e:
                logger.warning(f"Unknown provider {provider_name}: {e}")
    
    async def initialize(self) -> None:
        """Initialize all configured providers"""
        if self._initialized:
            return
        
        for provider_type, config in self.provider_configs.items():
            if not config.enabled:
                continue
            
            try:
                provider = await self._create_provider(provider_type, config.config)
                if provider:
                    self.providers[provider_type] = provider
                    self.rate_limits[provider_type] = {
                        "requests_count": 0,
                        "tokens_count": 0,
                        "window_start": datetime.now()
                    }
                    logger.info(f"Initialized {provider_type.value} provider")
                    
            except Exception as e:
                logger.error(f"Failed to initialize {provider_type.value} provider: {e}")
        
        if not self.providers:
            raise RuntimeError("No LLM providers could be initialized")
        
        self._initialized = True
        logger.info(f"LLM Manager initialized with {len(self.providers)} providers")
    
    async def _create_provider(self, provider_type: LLMProvider, config: Dict[str, Any]) -> Optional[BaseLLMProvider]:
        """Create and initialize a provider"""
        try:
            if provider_type == LLMProvider.OPENAI:
                provider = OpenAIProvider(config)
            elif provider_type == LLMProvider.ANTHROPIC:
                provider = AnthropicProvider(config)
            elif provider_type == LLMProvider.OLLAMA:
                provider = OllamaProvider(config)
            else:
                logger.warning(f"Provider {provider_type.value} not yet implemented")
                return None
            
            await provider.initialize()
            return provider
            
        except Exception as e:
            logger.error(f"Failed to create {provider_type.value} provider: {e}")
            return None
    
    async def generate_completion(self, 
                                request: LLMRequest, 
                                selection_criteria: Optional[ModelSelection] = None) -> LLMResponse:
        """
        Generate completion with intelligent provider and model selection
        """
        if not self._initialized:
            await self.initialize()
        
        # Select best provider and model
        provider, model_info = await self._select_provider_and_model(request, selection_criteria)
        
        if not provider:
            raise RuntimeError("No suitable provider available")
        
        # Update request with selected model
        request.model = model_info.model_id
        
        try:
            # Check rate limits
            if not await self._check_rate_limits(provider.provider_type, request):
                # Try fallback providers
                fallback_provider = await self._get_fallback_provider(provider.provider_type, request, selection_criteria)
                if fallback_provider:
                    provider, model_info = fallback_provider
                    request.model = model_info.model_id
                else:
                    raise RuntimeError("Rate limit exceeded and no fallback available")
            
            # Generate completion
            start_time = datetime.now()
            response = await provider.generate_completion(request)
            end_time = datetime.now()
            
            # Update usage statistics
            await self._update_usage_stats(
                provider.provider_type, 
                model_info.model_id, 
                response, 
                (end_time - start_time).total_seconds()
            )
            
            # Update rate limits
            await self._update_rate_limits(provider.provider_type, response)
            
            return response
            
        except Exception as e:
            # Try fallback providers
            fallback_provider = await self._get_fallback_provider(provider.provider_type, request, selection_criteria)
            if fallback_provider:
                provider, model_info = fallback_provider
                request.model = model_info.model_id
                
                try:
                    start_time = datetime.now()
                    response = await provider.generate_completion(request)
                    end_time = datetime.now()
                    
                    await self._update_usage_stats(
                        provider.provider_type, 
                        model_info.model_id, 
                        response, 
                        (end_time - start_time).total_seconds()
                    )
                    
                    return response
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback provider also failed: {fallback_error}")
                    raise e
            else:
                raise e
    
    async def generate_streaming_completion(self, 
                                          request: LLMRequest, 
                                          selection_criteria: Optional[ModelSelection] = None) -> AsyncGenerator[str, None]:
        """
        Generate streaming completion with intelligent provider selection
        """
        if not self._initialized:
            await self.initialize()
        
        # Ensure streaming is required
        if not selection_criteria:
            selection_criteria = ModelSelection()
        selection_criteria.require_streaming = True
        
        # Select best provider and model
        provider, model_info = await self._select_provider_and_model(request, selection_criteria)
        
        if not provider:
            raise RuntimeError("No suitable streaming provider available")
        
        request.model = model_info.model_id
        
        try:
            async for chunk in provider.generate_streaming_completion(request):
                yield chunk
                
        except Exception as e:
            # Try fallback providers
            fallback_provider = await self._get_fallback_provider(provider.provider_type, request, selection_criteria)
            if fallback_provider:
                provider, model_info = fallback_provider
                request.model = model_info.model_id
                
                async for chunk in provider.generate_streaming_completion(request):
                    yield chunk
            else:
                raise e
    
    async def _select_provider_and_model(self, 
                                       request: LLMRequest, 
                                       selection_criteria: Optional[ModelSelection]) -> tuple[Optional[BaseLLMProvider], Optional[ModelInfo]]:
        """
        Select the best provider and model based on request and criteria
        """
        if not selection_criteria:
            selection_criteria = ModelSelection()
        
        # Get all available models from all providers
        available_options = []
        
        for provider_type, provider in self.providers.items():
            if provider_type in selection_criteria.exclude_providers:
                continue
            
            try:
                models = await provider.get_available_models()
                for model in models:
                    # Check if model meets criteria
                    if self._model_meets_criteria(model, selection_criteria):
                        priority = self.provider_configs[provider_type].priority
                        
                        # Boost priority for preferred providers
                        if provider_type in selection_criteria.preferred_providers:
                            priority += 2
                        
                        # Boost priority for local models if preferred
                        if selection_criteria.prefer_local and model.is_local:
                            priority += 1
                        
                        available_options.append((priority, provider, model))
                        
            except Exception as e:
                logger.warning(f"Failed to get models from {provider_type.value}: {e}")
        
        if not available_options:
            return None, None
        
        # Sort by priority (highest first), then by cost (lowest first)
        available_options.sort(key=lambda x: (-x[0], x[2].cost_per_1k_tokens.get("input", 0)))
        
        # If a specific model is requested, try to find it
        if request.model:
            for priority, provider, model in available_options:
                if model.model_id == request.model:
                    return provider, model
        
        # Return the best option
        return available_options[0][1], available_options[0][2]
    
    def _model_meets_criteria(self, model: ModelInfo, criteria: ModelSelection) -> bool:
        """Check if a model meets the selection criteria"""
        # Check required capabilities
        if criteria.required_capabilities:
            if not all(cap in model.capabilities for cap in criteria.required_capabilities):
                return False
        
        # Check streaming requirement
        if criteria.require_streaming and ModelCapability.STREAMING not in model.capabilities:
            return False
        
        # Check cost constraint
        if criteria.max_cost_per_1k_tokens is not None:
            input_cost = model.cost_per_1k_tokens.get("input", 0)
            if input_cost > criteria.max_cost_per_1k_tokens:
                return False
        
        # Check context length
        if criteria.min_context_length is not None:
            if model.context_length < criteria.min_context_length:
                return False
        
        return True
    
    async def _check_rate_limits(self, provider_type: LLMProvider, request: LLMRequest) -> bool:
        """Check if request is within rate limits"""
        if provider_type not in self.rate_limits:
            return True
        
        config = self.provider_configs[provider_type]
        limits = self.rate_limits[provider_type]
        
        now = datetime.now()
        window_duration = timedelta(minutes=1)
        
        # Reset window if needed
        if now - limits["window_start"] > window_duration:
            limits["requests_count"] = 0
            limits["tokens_count"] = 0
            limits["window_start"] = now
        
        # Check limits
        if limits["requests_count"] >= config.max_requests_per_minute:
            return False
        
        estimated_tokens = len(str(request.messages)) // 4  # Rough estimation
        if limits["tokens_count"] + estimated_tokens > config.max_tokens_per_minute:
            return False
        
        return True
    
    async def _update_rate_limits(self, provider_type: LLMProvider, response: LLMResponse) -> None:
        """Update rate limit counters"""
        if provider_type in self.rate_limits:
            self.rate_limits[provider_type]["requests_count"] += 1
            self.rate_limits[provider_type]["tokens_count"] += response.usage.get("total_tokens", 0)
    
    async def _get_fallback_provider(self, 
                                   failed_provider: LLMProvider, 
                                   request: LLMRequest, 
                                   selection_criteria: Optional[ModelSelection]) -> Optional[tuple[BaseLLMProvider, ModelInfo]]:
        """Get a fallback provider when the primary fails"""
        config = self.provider_configs.get(failed_provider)
        if not config or not config.fallback_providers:
            return None
        
        for fallback_type in config.fallback_providers:
            if fallback_type in self.providers:
                provider = self.providers[fallback_type]
                models = await provider.get_available_models()
                
                for model in models:
                    if not selection_criteria or self._model_meets_criteria(model, selection_criteria):
                        return provider, model
        
        return None
    
    async def _update_usage_stats(self, 
                                provider_type: LLMProvider, 
                                model: str, 
                                response: LLMResponse, 
                                latency: float) -> None:
        """Update usage statistics"""
        key = f"{provider_type.value}:{model}"
        
        if key not in self.usage_stats:
            self.usage_stats[key] = UsageStats(
                provider=provider_type,
                model=model
            )
        
        stats = self.usage_stats[key]
        stats.request_count += 1
        stats.total_tokens += response.usage.get("total_tokens", 0)
        stats.avg_latency = ((stats.avg_latency * (stats.request_count - 1)) + latency) / stats.request_count
        stats.last_used = datetime.now()
        
        # Estimate cost if available
        provider = self.providers.get(provider_type)
        if provider:
            try:
                # Create a dummy request for cost estimation
                dummy_request = LLMRequest(messages=[], model=model)
                cost = await provider.estimate_cost(dummy_request, response)
                stats.total_cost += cost
            except:
                pass  # Cost estimation failed, skip
    
    async def get_available_models(self, provider_filter: Optional[List[LLMProvider]] = None) -> List[ModelInfo]:
        """Get all available models across providers"""
        if not self._initialized:
            await self.initialize()
        
        all_models = []
        
        for provider_type, provider in self.providers.items():
            if provider_filter and provider_type not in provider_filter:
                continue
            
            try:
                models = await provider.get_available_models()
                all_models.extend(models)
            except Exception as e:
                logger.warning(f"Failed to get models from {provider_type.value}: {e}")
        
        return all_models
    
    async def get_usage_statistics(self) -> Dict[str, UsageStats]:
        """Get usage statistics for all providers and models"""
        return self.usage_stats.copy()
    
    async def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers"""
        status = {}
        
        for provider_type, provider in self.providers.items():
            try:
                models = await provider.get_available_models()
                config = self.provider_configs[provider_type]
                limits = self.rate_limits.get(provider_type, {})
                
                status[provider_type.value] = {
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "available_models": len(models),
                    "requests_this_minute": limits.get("requests_count", 0),
                    "tokens_this_minute": limits.get("tokens_count", 0),
                    "max_requests_per_minute": config.max_requests_per_minute,
                    "max_tokens_per_minute": config.max_tokens_per_minute,
                    "models": [model.name for model in models[:5]]  # First 5 models
                }
                
            except Exception as e:
                status[provider_type.value] = {
                    "enabled": False,
                    "error": str(e)
                }
        
        return status
    
    def add_provider(self, provider_type: LLMProvider, config: ProviderConfig) -> None:
        """Add a new provider configuration"""
        self.provider_configs[provider_type] = config
        self._initialized = False  # Force re-initialization
    
    def remove_provider(self, provider_type: LLMProvider) -> None:
        """Remove a provider"""
        if provider_type in self.providers:
            del self.providers[provider_type]
        if provider_type in self.provider_configs:
            del self.provider_configs[provider_type]
        if provider_type in self.rate_limits:
            del self.rate_limits[provider_type]
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all providers"""
        if not self._initialized:
            await self.initialize()
        
        health_status = {
            "overall_healthy": True,
            "providers": {},
            "total_providers": len(self.providers),
            "healthy_providers": 0
        }
        
        for provider_type, provider in self.providers.items():
            try:
                # Simple health check - try to get available models
                models = await provider.get_available_models()
                
                health_status["providers"][provider_type.value] = {
                    "healthy": True,
                    "available_models": len(models),
                    "last_check": datetime.now().isoformat()
                }
                health_status["healthy_providers"] += 1
                
            except Exception as e:
                health_status["providers"][provider_type.value] = {
                    "healthy": False,
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
                health_status["overall_healthy"] = False
        
        return health_status