"""
LLM Provider Framework
=====================

Comprehensive multi-provider LLM system supporting OpenAI, Anthropic, 
Google, HuggingFace, Azure OpenAI, AWS Bedrock, and local models via Ollama.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Union, AsyncGenerator, Callable
import asyncio
import json
import logging
from pathlib import Path
import aiohttp
import openai
from anthropic import AsyncAnthropic
import google.generativeai as genai
from transformers import pipeline
import ollama
import boto3
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"
    AZURE_OPENAI = "azure_openai"
    AWS_BEDROCK = "aws_bedrock"
    OLLAMA = "ollama"
    COHERE = "cohere"
    MISTRAL = "mistral"

class ModelCapability(Enum):
    """Model capabilities"""
    TEXT_GENERATION = "text_generation"
    CHAT_COMPLETION = "chat_completion"
    CODE_GENERATION = "code_generation"
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"
    EMBEDDINGS = "embeddings"
    FINE_TUNING = "fine_tuning"
    STREAMING = "streaming"

@dataclass
class ModelInfo:
    """Information about an LLM model"""
    name: str
    provider: LLMProvider
    model_id: str
    capabilities: List[ModelCapability]
    context_length: int
    max_output_tokens: int
    cost_per_1k_tokens: Dict[str, float]  # {"input": 0.0015, "output": 0.002}
    description: str
    is_local: bool = False
    requires_gpu: bool = False
    model_size: Optional[str] = None  # e.g., "7B", "13B", "70B"
    quantization: Optional[str] = None  # e.g., "4bit", "8bit"

@dataclass
class LLMMessage:
    """Standardized message format"""
    role: str  # "system", "user", "assistant", "function"
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LLMRequest:
    """Standardized LLM request"""
    messages: List[LLMMessage]
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[List[str]] = None
    stream: bool = False
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[str, Dict[str, str]]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LLMResponse:
    """Standardized LLM response"""
    content: str
    model: str
    provider: LLMProvider
    usage: Dict[str, int]  # {"prompt_tokens": x, "completion_tokens": y, "total_tokens": z}
    finish_reason: str
    function_call: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseLLMProvider(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider_type = None
        self.available_models: List[ModelInfo] = []
        self._initialized = False
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the provider"""
        pass
    
    @abstractmethod
    async def generate_completion(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion"""
        pass
    
    @abstractmethod
    async def generate_streaming_completion(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Generate a streaming completion"""
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[ModelInfo]:
        """Get list of available models"""
        pass
    
    @abstractmethod
    async def validate_model(self, model_name: str) -> bool:
        """Validate if model is available"""
        pass
    
    async def estimate_cost(self, request: LLMRequest, response: LLMResponse) -> float:
        """Estimate the cost of the request/response"""
        model_info = next((m for m in self.available_models if m.model_id == request.model), None)
        if not model_info or not model_info.cost_per_1k_tokens:
            return 0.0
        
        input_cost = (response.usage.get("prompt_tokens", 0) / 1000) * model_info.cost_per_1k_tokens.get("input", 0)
        output_cost = (response.usage.get("completion_tokens", 0) / 1000) * model_info.cost_per_1k_tokens.get("output", 0)
        
        return input_cost + output_cost

class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider_type = LLMProvider.OPENAI
        self.client = None
    
    async def initialize(self) -> None:
        """Initialize OpenAI client"""
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        
        # Define available models
        self.available_models = [
            ModelInfo(
                name="GPT-4 Turbo",
                provider=LLMProvider.OPENAI,
                model_id="gpt-4-turbo-preview",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING
                ],
                context_length=128000,
                max_output_tokens=4096,
                cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                description="Most capable GPT-4 model with 128K context window"
            ),
            ModelInfo(
                name="GPT-4",
                provider=LLMProvider.OPENAI,
                model_id="gpt-4",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING
                ],
                context_length=8192,
                max_output_tokens=4096,
                cost_per_1k_tokens={"input": 0.03, "output": 0.06},
                description="High-intelligence flagship model for complex tasks"
            ),
            ModelInfo(
                name="GPT-3.5 Turbo",
                provider=LLMProvider.OPENAI,
                model_id="gpt-3.5-turbo",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING
                ],
                context_length=16385,
                max_output_tokens=4096,
                cost_per_1k_tokens={"input": 0.0015, "output": 0.002},
                description="Fast, inexpensive model for simple tasks"
            )
        ]
        
        self._initialized = True
        logger.info("OpenAI provider initialized successfully")
    
    async def generate_completion(self, request: LLMRequest) -> LLMResponse:
        """Generate completion using OpenAI"""
        if not self._initialized:
            await self.initialize()
        
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=request.model,
                messages=openai_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                frequency_penalty=request.frequency_penalty,
                presence_penalty=request.presence_penalty,
                stop=request.stop,
                functions=request.functions,
                function_call=request.function_call
            )
            
            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=response.model,
                provider=LLMProvider.OPENAI,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                finish_reason=response.choices[0].finish_reason,
                function_call=response.choices[0].message.function_call.dict() if response.choices[0].message.function_call else None
            )
            
        except Exception as e:
            logger.error(f"OpenAI completion error: {e}")
            raise
    
    async def generate_streaming_completion(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Generate streaming completion using OpenAI"""
        if not self._initialized:
            await self.initialize()
        
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        try:
            stream = await self.client.chat.completions.create(
                model=request.model,
                messages=openai_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            raise
    
    async def get_available_models(self) -> List[ModelInfo]:
        """Get available OpenAI models"""
        return self.available_models
    
    async def validate_model(self, model_name: str) -> bool:
        """Validate OpenAI model availability"""
        return any(model.model_id == model_name for model in self.available_models)

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider_type = LLMProvider.ANTHROPIC
        self.client = None
    
    async def initialize(self) -> None:
        """Initialize Anthropic client"""
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = AsyncAnthropic(api_key=api_key)
        
        # Define available models
        self.available_models = [
            ModelInfo(
                name="Claude-3 Opus",
                provider=LLMProvider.ANTHROPIC,
                model_id="claude-3-opus-20240229",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.VISION,
                    ModelCapability.STREAMING
                ],
                context_length=200000,
                max_output_tokens=4096,
                cost_per_1k_tokens={"input": 0.015, "output": 0.075},
                description="Most powerful Claude model for highly complex tasks"
            ),
            ModelInfo(
                name="Claude-3 Sonnet",
                provider=LLMProvider.ANTHROPIC,
                model_id="claude-3-sonnet-20240229",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.VISION,
                    ModelCapability.STREAMING
                ],
                context_length=200000,
                max_output_tokens=4096,
                cost_per_1k_tokens={"input": 0.003, "output": 0.015},
                description="Balanced performance and speed for a wide range of tasks"
            ),
            ModelInfo(
                name="Claude-3 Haiku",
                provider=LLMProvider.ANTHROPIC,
                model_id="claude-3-haiku-20240307",
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.STREAMING
                ],
                context_length=200000,
                max_output_tokens=4096,
                cost_per_1k_tokens={"input": 0.00025, "output": 0.00125},
                description="Fastest and most compact model for simple tasks"
            )
        ]
        
        self._initialized = True
        logger.info("Anthropic provider initialized successfully")
    
    async def generate_completion(self, request: LLMRequest) -> LLMResponse:
        """Generate completion using Anthropic"""
        if not self._initialized:
            await self.initialize()
        
        # Convert messages to Anthropic format
        system_message = ""
        messages = []
        
        for msg in request.messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = await self.client.messages.create(
                model=request.model,
                max_tokens=request.max_tokens or 4096,
                temperature=request.temperature,
                system=system_message if system_message else None,
                messages=messages
            )
            
            return LLMResponse(
                content=response.content[0].text,
                model=request.model,
                provider=LLMProvider.ANTHROPIC,
                usage={
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                },
                finish_reason=response.stop_reason
            )
            
        except Exception as e:
            logger.error(f"Anthropic completion error: {e}")
            raise
    
    async def generate_streaming_completion(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Generate streaming completion using Anthropic"""
        if not self._initialized:
            await self.initialize()
        
        system_message = ""
        messages = []
        
        for msg in request.messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                messages.append({"role": msg.role, "content": msg.content})
        
        try:
            async with self.client.messages.stream(
                model=request.model,
                max_tokens=request.max_tokens or 4096,
                temperature=request.temperature,
                system=system_message if system_message else None,
                messages=messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Anthropic streaming error: {e}")
            raise
    
    async def get_available_models(self) -> List[ModelInfo]:
        """Get available Anthropic models"""
        return self.available_models
    
    async def validate_model(self, model_name: str) -> bool:
        """Validate Anthropic model availability"""
        return any(model.model_id == model_name for model in self.available_models)

class OllamaProvider(BaseLLMProvider):
    """Ollama local model provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.provider_type = LLMProvider.OLLAMA
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.client = None
    
    async def initialize(self) -> None:
        """Initialize Ollama client"""
        try:
            # Test connection to Ollama
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status != 200:
                        raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}")
            
            # Initialize Ollama client
            self.client = ollama.AsyncClient(host=self.base_url)
            
            # Get available models from Ollama
            await self._load_available_models()
            
            self._initialized = True
            logger.info(f"Ollama provider initialized successfully at {self.base_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Ollama provider: {e}")
            raise
    
    async def _load_available_models(self) -> None:
        """Load available models from Ollama"""
        try:
            models_response = await self.client.list()
            self.available_models = []
            
            for model in models_response.get('models', []):
                model_name = model['name']
                
                # Extract model size from name if available
                model_size = None
                if ':' in model_name:
                    base_name, tag = model_name.split(':', 1)
                    if any(size in tag for size in ['7b', '13b', '30b', '70b']):
                        model_size = tag.upper()
                
                # Determine capabilities based on model name
                capabilities = [
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT_COMPLETION,
                    ModelCapability.STREAMING
                ]
                
                if 'code' in model_name.lower():
                    capabilities.append(ModelCapability.CODE_GENERATION)
                
                model_info = ModelInfo(
                    name=model_name,
                    provider=LLMProvider.OLLAMA,
                    model_id=model_name,
                    capabilities=capabilities,
                    context_length=4096,  # Default, can be model-specific
                    max_output_tokens=2048,
                    cost_per_1k_tokens={"input": 0.0, "output": 0.0},  # Free for local models
                    description=f"Local model running via Ollama: {model_name}",
                    is_local=True,
                    requires_gpu=True,  # Most local models benefit from GPU
                    model_size=model_size
                )
                
                self.available_models.append(model_info)
                
        except Exception as e:
            logger.error(f"Failed to load Ollama models: {e}")
            # Provide some default models that are commonly available
            self.available_models = [
                ModelInfo(
                    name="llama2",
                    provider=LLMProvider.OLLAMA,
                    model_id="llama2",
                    capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.CHAT_COMPLETION],
                    context_length=4096,
                    max_output_tokens=2048,
                    cost_per_1k_tokens={"input": 0.0, "output": 0.0},
                    description="Llama 2 model running locally via Ollama",
                    is_local=True,
                    requires_gpu=True,
                    model_size="7B"
                )
            ]
    
    async def generate_completion(self, request: LLMRequest) -> LLMResponse:
        """Generate completion using Ollama"""
        if not self._initialized:
            await self.initialize()
        
        # Convert messages to a single prompt for Ollama
        prompt = self._convert_messages_to_prompt(request.messages)
        
        try:
            response = await self.client.generate(
                model=request.model,
                prompt=prompt,
                options={
                    'temperature': request.temperature,
                    'top_p': request.top_p,
                    'num_predict': request.max_tokens or -1,
                    'stop': request.stop or []
                }
            )
            
            return LLMResponse(
                content=response['response'],
                model=request.model,
                provider=LLMProvider.OLLAMA,
                usage={
                    "prompt_tokens": response.get('prompt_eval_count', 0),
                    "completion_tokens": response.get('eval_count', 0),
                    "total_tokens": response.get('prompt_eval_count', 0) + response.get('eval_count', 0)
                },
                finish_reason="stop"
            )
            
        except Exception as e:
            logger.error(f"Ollama completion error: {e}")
            raise
    
    async def generate_streaming_completion(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Generate streaming completion using Ollama"""
        if not self._initialized:
            await self.initialize()
        
        prompt = self._convert_messages_to_prompt(request.messages)
        
        try:
            stream = await self.client.generate(
                model=request.model,
                prompt=prompt,
                stream=True,
                options={
                    'temperature': request.temperature,
                    'top_p': request.top_p,
                    'num_predict': request.max_tokens or -1
                }
            )
            
            async for chunk in stream:
                if 'response' in chunk:
                    yield chunk['response']
                    
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            raise
    
    def _convert_messages_to_prompt(self, messages: List[LLMMessage]) -> str:
        """Convert messages to a single prompt for Ollama"""
        prompt_parts = []
        
        for message in messages:
            if message.role == "system":
                prompt_parts.append(f"System: {message.content}")
            elif message.role == "user":
                prompt_parts.append(f"Human: {message.content}")
            elif message.role == "assistant":
                prompt_parts.append(f"Assistant: {message.content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    async def get_available_models(self) -> List[ModelInfo]:
        """Get available Ollama models"""
        if not self._initialized:
            await self.initialize()
        return self.available_models
    
    async def validate_model(self, model_name: str) -> bool:
        """Validate Ollama model availability"""
        try:
            # Try to check if model exists
            models = await self.client.list()
            return any(model['name'] == model_name for model in models.get('models', []))
        except:
            return False
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull a model to Ollama"""
        try:
            await self.client.pull(model_name)
            await self._load_available_models()  # Refresh available models
            return True
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False