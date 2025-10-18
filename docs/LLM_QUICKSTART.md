# CollegiumAI LLM Framework - Quick Start Guide

Welcome to the CollegiumAI Multi-Provider LLM Framework! This guide will help you get started with using multiple AI providers including OpenAI, Anthropic, and local models via Ollama.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install openai anthropic ollama tiktoken pyyaml rich aiofiles
```

### 2. Configure Environment

Create a `.env` file in your project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_ORG_ID=your_org_id_here  # Optional

# Anthropic Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Ollama Configuration (for local models)
OLLAMA_BASE_URL=http://localhost:11434  # Default Ollama URL
OLLAMA_TIMEOUT=120

# Optional: Custom configuration file path
LLM_CONFIG_PATH=config/llm-config.yaml
```

### 3. Basic Usage

```python
import asyncio
from framework.llm import LLMManager, create_chat_request, create_user_message

async def main():
    # Initialize the LLM manager
    llm_manager = LLMManager()
    await llm_manager.initialize()
    
    # Create a simple request
    messages = [create_user_message("What is artificial intelligence?")]
    request = create_chat_request(messages=messages)
    
    # Generate response (automatically selects best provider)
    response = await llm_manager.generate_completion(request)
    print(f"Response from {response.provider.value}: {response.content}")

# Run the example
asyncio.run(main())
```

## 📋 Provider Setup

### OpenAI Setup
1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Set `OPENAI_API_KEY` in your environment
3. Models available: GPT-4, GPT-3.5, etc.

### Anthropic Setup
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Set `ANTHROPIC_API_KEY` in your environment  
3. Models available: Claude-3, Claude-2, etc.

### Ollama Setup (Local Models)
1. Install Ollama: [https://ollama.ai/](https://ollama.ai/)
2. Pull models: `ollama pull llama2` or `ollama pull codellama`
3. Start Ollama service: `ollama serve`
4. Set `OLLAMA_BASE_URL` to your Ollama instance

## 🎯 Intelligent Model Selection

The framework automatically selects the best model based on your criteria:

```python
from framework.llm import ModelSelection, ModelCapability, LLMProvider

# Cost-optimized selection
cost_optimized = ModelSelection(
    max_cost_per_1k_tokens=0.01,
    required_capabilities=[ModelCapability.CHAT_COMPLETION]
)

# Privacy-focused (local models)
private_selection = ModelSelection(
    prefer_local=True,
    required_capabilities=[ModelCapability.CHAT_COMPLETION]
)

# High-performance selection
high_performance = ModelSelection(
    required_capabilities=[
        ModelCapability.CHAT_COMPLETION,
        ModelCapability.CODE_GENERATION
    ],
    preferred_providers=[LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
)

# Use with specific selection criteria
response = await llm_manager.generate_completion(request, cost_optimized)
```

## 🌊 Streaming Responses

For real-time content generation:

```python
async for chunk in llm_manager.generate_streaming_completion(request):
    print(chunk, end="", flush=True)
```

## 🛠️ CLI Management

The framework includes powerful CLI tools:

```bash
# Check provider status
python -m cli.commands.llm status

# List available models
python -m cli.commands.llm models

# Test a provider
python -m cli.commands.llm test "Hello, world!"

# Interactive chat
python -m cli.commands.llm chat

# Pull Ollama models
python -m cli.commands.llm pull llama2
```

## 📊 Usage Monitoring

Track your usage and costs:

```python
# Get usage statistics
stats = await llm_manager.get_usage_statistics()
for provider_model, stat in stats.items():
    print(f"{provider_model}: {stat.request_count} requests, ${stat.total_cost:.4f}")

# Health check
health = await llm_manager.health_check()
print(f"System healthy: {health['overall_healthy']}")
```

## 🎓 Educational Use Cases

The framework is optimized for educational applications:

```python
from examples.educational_assistant import EducationalAssistant

# Initialize educational assistant
assistant = await EducationalAssistant().initialize()

# Academic advising (cost-optimized)
advice = await assistant.provide_academic_advice(
    "What courses should I take for AI specialization?",
    {'major': 'Computer Science', 'year': 'junior'}
)

# Research assistance (high-capability models)
research_help = await assistant.assist_with_research(
    "How to analyze student learning outcomes?",
    domain="Educational Research"
)

# Tutoring (privacy-focused local models)
tutoring = await assistant.provide_tutoring(
    "Mathematics",
    "Explain calculus derivatives",
    difficulty_level="beginner"
)
```

## ⚙️ Configuration Options

Customize behavior with `config/llm-config.yaml`:

```yaml
providers:
  openai:
    enabled: true
    priority: 1
    models:
      - gpt-4
      - gpt-3.5-turbo
    rate_limits:
      requests_per_minute: 60
      
  anthropic:
    enabled: true
    priority: 2
    models:
      - claude-3-opus
      - claude-3-sonnet
      
  ollama:
    enabled: true
    priority: 3
    base_url: "http://localhost:11434"
    
selection_defaults:
  temperature: 0.7
  max_tokens: 1000
  prefer_local: false
  max_cost_per_1k_tokens: 1.0
```

## 📈 Performance Tips

1. **Cost Optimization**: Use `max_cost_per_1k_tokens` for budget control
2. **Privacy**: Set `prefer_local=True` for sensitive data
3. **Speed**: Use streaming for long responses
4. **Reliability**: Configure multiple providers for fallback
5. **Caching**: Enable response caching for repeated queries

## 🔍 Troubleshooting

### Common Issues

**Provider Not Available**
```python
# Check provider status
status = await llm_manager.get_provider_status()
print(status)
```

**API Key Issues**
- Verify environment variables are set
- Check API key validity and permissions
- Ensure proper .env file loading

**Ollama Connection Issues**
- Verify Ollama is running: `ollama serve`
- Check URL: `curl http://localhost:11434/api/tags`
- Pull required models: `ollama pull llama2`

**Rate Limits**
- Configure rate limits in config file
- Use multiple providers for load distribution
- Implement request queuing for high-volume apps

## 📚 Examples

- `examples/llm_demo.py` - Comprehensive framework demonstration
- `examples/educational_assistant.py` - Educational use cases
- `examples/comprehensive_integration_demo.py` - Full system integration

## 🆘 Getting Help

1. Check the configuration with CLI: `python -m cli.commands.llm status`
2. Run health check: `python -m cli.commands.llm health`
3. Test providers individually: `python -m cli.commands.llm test`
4. Review logs for detailed error information

## 🚀 Next Steps

1. Run the comprehensive demo: `python examples/llm_demo.py`
2. Try the educational assistant: `python examples/educational_assistant.py`
3. Explore CLI commands: `python -m cli.commands.llm --help`
4. Customize configuration for your use case
5. Integrate into your CollegiumAI applications

Happy building with CollegiumAI's Multi-Provider LLM Framework! 🎓✨