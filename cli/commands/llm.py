"""
LLM Management CLI Commands
==========================

Command-line interface for managing LLM providers, models, and configurations.
"""

import asyncio
import json
import yaml
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from framework.llm import LLMManager, LLMRequest, LLMMessage, ModelSelection, ModelCapability, LLMProvider

console = Console()

@click.group()
def llm():
    """LLM provider management commands"""
    pass

@llm.command()
@click.option('--config-path', '-c', type=click.Path(exists=True), help='Path to LLM configuration file')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), default='table', help='Output format')
def providers(config_path: Optional[str], format: str):
    """List available LLM providers and their status"""
    
    async def _list_providers():
        config_file = Path(config_path) if config_path else None
        llm_manager = LLMManager(config_file)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Initializing LLM providers...", total=None)
            
            try:
                await llm_manager.initialize()
                progress.update(task, description="Getting provider status...")
                
                status = await llm_manager.get_provider_status()
                
                if format == 'json':
                    rprint(json.dumps(status, indent=2))
                elif format == 'yaml':
                    rprint(yaml.dump(status, default_flow_style=False))
                else:
                    # Table format
                    table = Table(title="LLM Provider Status")
                    table.add_column("Provider", style="cyan")
                    table.add_column("Status", style="green")
                    table.add_column("Priority", style="yellow")
                    table.add_column("Models", style="blue")
                    table.add_column("Requests/Min", style="magenta")
                    table.add_column("Tokens/Min", style="red")
                    
                    for provider_name, provider_info in status.items():
                        status_indicator = "✅ Enabled" if provider_info.get('enabled', False) else "❌ Disabled"
                        if 'error' in provider_info:
                            status_indicator = f"⚠️ Error: {provider_info['error']}"
                        
                        table.add_row(
                            provider_name,
                            status_indicator,
                            str(provider_info.get('priority', 'N/A')),
                            str(provider_info.get('available_models', 'N/A')),
                            f"{provider_info.get('requests_this_minute', 0)}/{provider_info.get('max_requests_per_minute', 'N/A')}",
                            f"{provider_info.get('tokens_this_minute', 0)}/{provider_info.get('max_tokens_per_minute', 'N/A')}"
                        )
                    
                    console.print(table)
                    
                    # Show model samples
                    for provider_name, provider_info in status.items():
                        if provider_info.get('models'):
                            panel = Panel(
                                f"Sample models: {', '.join(provider_info['models'])}",
                                title=f"{provider_name} Models",
                                border_style="blue"
                            )
                            console.print(panel)
                
            except Exception as e:
                console.print(f"[red]Error initializing providers: {e}[/red]")
                return 1
    
    return asyncio.run(_list_providers())

@llm.command()
@click.option('--config-path', '-c', type=click.Path(exists=True), help='Path to LLM configuration file')
@click.option('--provider', '-p', type=click.Choice([p.value for p in LLMProvider]), help='Filter by provider')
@click.option('--capability', '-cap', multiple=True, type=click.Choice([c.value for c in ModelCapability]), help='Filter by capability')
@click.option('--local-only', is_flag=True, help='Show only local models')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), default='table', help='Output format')
def models(config_path: Optional[str], provider: Optional[str], capability: List[str], local_only: bool, format: str):
    """List available models across all providers"""
    
    async def _list_models():
        config_file = Path(config_path) if config_path else None
        llm_manager = LLMManager(config_file)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading models...", total=None)
            
            try:
                await llm_manager.initialize()
                
                # Get provider filter
                provider_filter = [LLMProvider(provider)] if provider else None
                
                models = await llm_manager.get_available_models(provider_filter)
                
                # Apply filters
                if capability:
                    capability_enums = [ModelCapability(c) for c in capability]
                    models = [m for m in models if all(cap in m.capabilities for cap in capability_enums)]
                
                if local_only:
                    models = [m for m in models if m.is_local]
                
                if format == 'json':
                    model_data = []
                    for model in models:
                        model_data.append({
                            'name': model.name,
                            'provider': model.provider.value,
                            'model_id': model.model_id,
                            'capabilities': [c.value for c in model.capabilities],
                            'context_length': model.context_length,
                            'max_output_tokens': model.max_output_tokens,
                            'cost_per_1k_tokens': model.cost_per_1k_tokens,
                            'is_local': model.is_local,
                            'description': model.description
                        })
                    rprint(json.dumps(model_data, indent=2))
                    
                elif format == 'yaml':
                    model_data = []
                    for model in models:
                        model_data.append({
                            'name': model.name,
                            'provider': model.provider.value,
                            'model_id': model.model_id,
                            'capabilities': [c.value for c in model.capabilities],
                            'context_length': model.context_length,
                            'max_output_tokens': model.max_output_tokens,
                            'cost_per_1k_tokens': model.cost_per_1k_tokens,
                            'is_local': model.is_local,
                            'description': model.description
                        })
                    rprint(yaml.dump(model_data, default_flow_style=False))
                    
                else:
                    # Table format
                    table = Table(title="Available LLM Models")
                    table.add_column("Model Name", style="cyan")
                    table.add_column("Provider", style="green") 
                    table.add_column("Context", style="yellow")
                    table.add_column("Max Output", style="blue")
                    table.add_column("Cost (Input)", style="magenta")
                    table.add_column("Cost (Output)", style="red")
                    table.add_column("Local", style="white")
                    table.add_column("Capabilities", style="bright_black")
                    
                    for model in models:
                        input_cost = model.cost_per_1k_tokens.get('input', 0)
                        output_cost = model.cost_per_1k_tokens.get('output', 0)
                        
                        capabilities_str = ', '.join([c.value for c in model.capabilities[:3]])
                        if len(model.capabilities) > 3:
                            capabilities_str += f" +{len(model.capabilities) - 3}"
                        
                        table.add_row(
                            model.name,
                            model.provider.value,
                            f"{model.context_length:,}",
                            f"{model.max_output_tokens:,}",
                            f"${input_cost:.4f}" if input_cost > 0 else "Free",
                            f"${output_cost:.4f}" if output_cost > 0 else "Free",
                            "✅" if model.is_local else "❌",
                            capabilities_str
                        )
                    
                    console.print(table)
                    console.print(f"\n[dim]Found {len(models)} models[/dim]")
                
            except Exception as e:
                console.print(f"[red]Error loading models: {e}[/red]")
                return 1
    
    return asyncio.run(_list_models())

@llm.command()
@click.option('--config-path', '-c', type=click.Path(exists=True), help='Path to LLM configuration file')
def health(config_path: Optional[str]):
    """Perform health check on all LLM providers"""
    
    async def _health_check():
        config_file = Path(config_path) if config_path else None
        llm_manager = LLMManager(config_file)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Performing health check...", total=None)
            
            try:
                health_status = await llm_manager.health_check()
                
                # Overall status
                if health_status['overall_healthy']:
                    console.print("🟢 [green]Overall System Health: HEALTHY[/green]")
                else:
                    console.print("🔴 [red]Overall System Health: UNHEALTHY[/red]")
                
                console.print(f"📊 Total Providers: {health_status['total_providers']}")
                console.print(f"✅ Healthy Providers: {health_status['healthy_providers']}")
                
                # Provider details
                table = Table(title="Provider Health Status")
                table.add_column("Provider", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Models", style="yellow")
                table.add_column("Last Check", style="blue")
                table.add_column("Details", style="white")
                
                for provider_name, provider_health in health_status['providers'].items():
                    if provider_health['healthy']:
                        status_icon = "🟢 Healthy"
                        status_style = "green"
                        details = f"{provider_health.get('available_models', 0)} models available"
                    else:
                        status_icon = "🔴 Unhealthy"
                        status_style = "red"
                        details = provider_health.get('error', 'Unknown error')
                    
                    table.add_row(
                        provider_name,
                        f"[{status_style}]{status_icon}[/{status_style}]",
                        str(provider_health.get('available_models', 'N/A')),
                        provider_health.get('last_check', 'Never'),
                        details
                    )
                
                console.print(table)
                
            except Exception as e:
                console.print(f"[red]Error performing health check: {e}[/red]")
                return 1
    
    return asyncio.run(_health_check())

@llm.command()
@click.argument('prompt', required=True)
@click.option('--config-path', '-c', type=click.Path(exists=True), help='Path to LLM configuration file')
@click.option('--model', '-m', help='Specific model to use')
@click.option('--provider', '-p', type=click.Choice([p.value for p in LLMProvider]), help='Specific provider to use')
@click.option('--temperature', '-t', type=float, default=0.7, help='Temperature for generation (0.0-1.0)')
@click.option('--max-tokens', type=int, help='Maximum tokens to generate')
@click.option('--stream', is_flag=True, help='Enable streaming output')
@click.option('--prefer-local', is_flag=True, help='Prefer local models')
@click.option('--max-cost', type=float, help='Maximum cost per 1K tokens')
def chat(prompt: str, config_path: Optional[str], model: Optional[str], provider: Optional[str], 
         temperature: float, max_tokens: Optional[int], stream: bool, prefer_local: bool, max_cost: Optional[float]):
    """Send a chat message to an LLM"""
    
    async def _chat():
        config_file = Path(config_path) if config_path else None
        llm_manager = LLMManager(config_file)
        
        try:
            await llm_manager.initialize()
            
            # Create request
            messages = [LLMMessage(role="user", content=prompt)]
            request = LLMRequest(
                messages=messages,
                model=model or "",
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Create selection criteria
            selection_criteria = ModelSelection(
                prefer_local=prefer_local,
                max_cost_per_1k_tokens=max_cost,
                require_streaming=stream
            )
            
            if provider:
                selection_criteria.preferred_providers = [LLMProvider(provider)]
            
            console.print(f"[dim]Sending prompt to LLM...[/dim]")
            console.print(f"[cyan]Prompt:[/cyan] {prompt}")
            console.print()
            
            if stream:
                console.print("[cyan]Response:[/cyan]")
                response_content = ""
                async for chunk in llm_manager.generate_streaming_completion(request, selection_criteria):
                    console.print(chunk, end="")
                    response_content += chunk
                console.print()
            else:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Generating response...", total=None)
                    
                    response = await llm_manager.generate_completion(request, selection_criteria)
                    
                    console.print(f"[cyan]Response:[/cyan]")
                    console.print(response.content)
                    console.print()
                    console.print(f"[dim]Model: {response.model} | Provider: {response.provider.value}[/dim]")
                    console.print(f"[dim]Tokens: {response.usage.get('total_tokens', 0)} | Finish: {response.finish_reason}[/dim]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return 1
    
    return asyncio.run(_chat())

@llm.command()
@click.option('--config-path', '-c', type=click.Path(exists=True), help='Path to LLM configuration file')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), default='table', help='Output format')
def usage(config_path: Optional[str], format: str):
    """Show LLM usage statistics"""
    
    async def _show_usage():
        config_file = Path(config_path) if config_path else None
        llm_manager = LLMManager(config_file)
        
        try:
            await llm_manager.initialize()
            stats = await llm_manager.get_usage_statistics()
            
            if not stats:
                console.print("[yellow]No usage statistics available[/yellow]")
                return
            
            if format == 'json':
                stats_data = {}
                for key, stat in stats.items():
                    stats_data[key] = {
                        'provider': stat.provider.value,
                        'model': stat.model,
                        'request_count': stat.request_count,
                        'total_tokens': stat.total_tokens,
                        'total_cost': stat.total_cost,
                        'avg_latency': stat.avg_latency,
                        'error_count': stat.error_count,
                        'last_used': stat.last_used.isoformat() if stat.last_used else None
                    }
                rprint(json.dumps(stats_data, indent=2))
                
            elif format == 'yaml':
                stats_data = {}
                for key, stat in stats.items():
                    stats_data[key] = {
                        'provider': stat.provider.value,
                        'model': stat.model,
                        'request_count': stat.request_count,
                        'total_tokens': stat.total_tokens,
                        'total_cost': stat.total_cost,
                        'avg_latency': stat.avg_latency,
                        'error_count': stat.error_count,
                        'last_used': stat.last_used.isoformat() if stat.last_used else None
                    }
                rprint(yaml.dump(stats_data, default_flow_style=False))
                
            else:
                # Table format
                table = Table(title="LLM Usage Statistics")
                table.add_column("Provider:Model", style="cyan")
                table.add_column("Requests", style="green")
                table.add_column("Total Tokens", style="yellow")
                table.add_column("Total Cost", style="red")
                table.add_column("Avg Latency", style="blue")
                table.add_column("Errors", style="magenta")
                table.add_column("Last Used", style="white")
                
                for key, stat in stats.items():
                    last_used = stat.last_used.strftime("%Y-%m-%d %H:%M") if stat.last_used else "Never"
                    
                    table.add_row(
                        f"{stat.provider.value}:{stat.model}",
                        str(stat.request_count),
                        f"{stat.total_tokens:,}",
                        f"${stat.total_cost:.4f}" if stat.total_cost > 0 else "$0.00",
                        f"{stat.avg_latency:.2f}s",
                        str(stat.error_count),
                        last_used
                    )
                
                console.print(table)
                
                # Summary
                total_requests = sum(stat.request_count for stat in stats.values())
                total_tokens = sum(stat.total_tokens for stat in stats.values())
                total_cost = sum(stat.total_cost for stat in stats.values())
                total_errors = sum(stat.error_count for stat in stats.values())
                
                console.print(f"\n[dim]Summary: {total_requests} requests, {total_tokens:,} tokens, ${total_cost:.4f} cost, {total_errors} errors[/dim]")
            
        except Exception as e:
            console.print(f"[red]Error retrieving usage statistics: {e}[/red]")
            return 1
    
    return asyncio.run(_show_usage())

@llm.command()
@click.argument('model_name', required=True)
@click.option('--provider', '-p', type=click.Choice(['ollama']), default='ollama', help='Provider to pull model from')
def pull(model_name: str, provider: str):
    """Pull a model to local provider (Ollama)"""
    
    async def _pull_model():
        if provider == 'ollama':
            from framework.llm.providers import OllamaProvider
            import os
            
            ollama_config = {
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            }
            
            ollama_provider = OllamaProvider(ollama_config)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Pulling model {model_name}...", total=None)
                
                try:
                    await ollama_provider.initialize()
                    success = await ollama_provider.pull_model(model_name)
                    
                    if success:
                        console.print(f"[green]✅ Successfully pulled model: {model_name}[/green]")
                    else:
                        console.print(f"[red]❌ Failed to pull model: {model_name}[/red]")
                        return 1
                        
                except Exception as e:
                    console.print(f"[red]Error pulling model: {e}[/red]")
                    return 1
        else:
            console.print(f"[red]Model pulling not supported for provider: {provider}[/red]")
            return 1
    
    return asyncio.run(_pull_model())

@llm.command()
@click.option('--config-path', '-c', type=click.Path(), help='Path to save configuration file')
def init_config(config_path: Optional[str]):
    """Initialize LLM configuration file"""
    
    if not config_path:
        config_path = "./config/llm-config.yaml"
    
    config_file = Path(config_path)
    
    if config_file.exists():
        if not click.confirm(f"Configuration file {config_path} already exists. Overwrite?"):
            return
    
    # Create directory if it doesn't exist
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy default configuration
    default_config_path = Path(__file__).parent.parent.parent / "config" / "llm-config.yaml"
    
    try:
        if default_config_path.exists():
            import shutil
            shutil.copy(default_config_path, config_file)
        else:
            # Create minimal configuration
            minimal_config = {
                "providers": {
                    "openai": {
                        "config": {"api_key": "${OPENAI_API_KEY}"},
                        "priority": 3,
                        "enabled": True,
                        "max_requests_per_minute": 60,
                        "max_tokens_per_minute": 40000
                    },
                    "ollama": {
                        "config": {"base_url": "${OLLAMA_BASE_URL:http://localhost:11434}"},
                        "priority": 1,
                        "enabled": True,
                        "max_requests_per_minute": 100,
                        "max_tokens_per_minute": 50000
                    }
                }
            }
            
            with open(config_file, 'w') as f:
                yaml.dump(minimal_config, f, default_flow_style=False)
        
        console.print(f"[green]✅ Configuration file created: {config_path}[/green]")
        console.print(f"[dim]Edit the file to configure your API keys and preferences[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error creating configuration file: {e}[/red]")
        return 1

if __name__ == "__main__":
    llm()