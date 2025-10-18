#!/usr/bin/env python3
"""
CollegiumAI CLI - Main Entry Point
=================================

Professional command-line interface for CollegiumAI Multi-Agent Educational Framework.
Provides comprehensive university management, agent coordination, and AI-powered operations.

Based on advanced CLI patterns from Feriq framework, specialized for higher education.
"""

import click
import asyncio
from typing import Dict, Any, Optional
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.commands.agent_commands import agent_commands
from cli.commands.student_commands import student_commands  
from cli.commands.academic_commands import academic_commands
from cli.commands.research_commands import research_commands
from cli.commands.governance_commands import governance_commands
from cli.commands.compliance_commands import compliance_commands
from cli.commands.blockchain_commands import blockchain_commands
from cli.commands.team_commands import team_commands
from cli.commands.system_commands import system_commands

# CLI Context and Configuration
class CLIContext:
    """Global CLI context and configuration"""
    def __init__(self):
        self.config = {}
        self.workspace_path = os.getcwd()
        self.verbose = False
        self.framework = None
        
    def load_config(self):
        """Load configuration from collegium.yaml"""
        config_path = Path(self.workspace_path) / "collegium.yaml"
        if config_path.exists():
            import yaml
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        
    def get_framework(self):
        """Get or initialize the CollegiumAI framework"""
        if not self.framework:
            # Import here to avoid circular imports
            from framework.core.collegium_framework import CollegiumFramework
            self.framework = CollegiumFramework()
        return self.framework

# Main CLI Group
@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--workspace', '-w', default='.', help='Workspace directory')
@click.version_option(version='1.0.0', prog_name='CollegiumAI')
@click.pass_context
def cli(ctx, verbose, workspace):
    """
    🎓 CollegiumAI - AI Multi-Agent Collaborative Framework for Digital Universities
    
    Professional command-line interface for managing AI-powered university operations,
    student services, academic planning, research coordination, and governance compliance.
    
    Examples:
        collegium agent list                    # List all agents
        collegium student enroll --help         # Student enrollment help
        collegium academic plan-degree          # Create degree plan
        collegium research collaborate          # Start research collaboration
        collegium governance check-compliance   # Check compliance status
        collegium blockchain verify-credential # Verify credentials
    """
    
    # Initialize CLI context
    cli_context = CLIContext()
    cli_context.verbose = verbose
    cli_context.workspace_path = os.path.abspath(workspace)
    cli_context.load_config()
    
    ctx.ensure_object(dict)
    ctx.obj['cli_context'] = cli_context
    
    # If no command provided, show help
    if ctx.invoked_subcommand is None:
        show_welcome()
        click.echo(ctx.get_help())

def show_welcome():
    """Display welcome message and system status"""
    click.echo("🎓✨ " + click.style("CollegiumAI", fg='blue', bold=True) + " - AI Multi-Agent Educational Framework")
    click.echo("=" * 80)
    click.echo("🤖 " + click.style("AI Agents:", fg='green') + " ReACT Multi-Agent System with Educational Specialization")
    click.echo("🧠 " + click.style("LLM Support:", fg='yellow') + " OpenAI, Anthropic, Ollama with Intelligent Routing")
    click.echo("🇪🇺 " + click.style("Bologna Process:", fg='blue') + " European Higher Education Area Compliance")
    click.echo("🔗 " + click.style("Blockchain:", fg='purple') + " Credential Verification & Governance")
    click.echo("📋 " + click.style("Compliance:", fg='red') + " AACSB, HEFCE, Middle States, WASC, QAA")
    click.echo("=" * 80)
    click.echo()

# Add command groups
cli.add_command(agent_commands, name='agent')
cli.add_command(student_commands, name='student')
cli.add_command(academic_commands, name='academic')
cli.add_command(research_commands, name='research')
cli.add_command(governance_commands, name='governance')
cli.add_command(compliance_commands, name='compliance')
cli.add_command(blockchain_commands, name='blockchain')
cli.add_command(team_commands, name='team')
cli.add_command(system_commands, name='system')

# Quick Actions
@cli.command()
@click.pass_context
def init(ctx):
    """🚀 Initialize a new CollegiumAI workspace"""
    cli_context = ctx.obj['cli_context']
    
    click.echo("🎓 " + click.style("Initializing CollegiumAI Workspace", fg='blue', bold=True))
    click.echo("=" * 50)
    
    # Create workspace structure
    workspace_path = Path(cli_context.workspace_path)
    
    directories = [
        'config',
        'data/students',
        'data/faculty', 
        'data/courses',
        'data/research',
        'agents',
        'workflows',
        'reports',
        'compliance',
        'blockchain'
    ]
    
    for dir_name in directories:
        dir_path = workspace_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        click.echo(f"  ✅ Created: {dir_name}/")
    
    # Create configuration file
    config_content = """# CollegiumAI Configuration
project:
  name: "My University"
  type: "digital_university"
  version: "1.0.0"

# AI Agent Configuration
agents:
  academic_advisor:
    enabled: true
    llm_provider: "anthropic"
    specialization: "Academic Planning"
  
  student_services:
    enabled: true
    llm_provider: "ollama"
    specialization: "Student Support"
    
  bologna_process:
    enabled: true
    llm_provider: "openai"
    specialization: "European Standards"
    
  research_coordinator:
    enabled: true
    llm_provider: "openai"
    specialization: "Research Collaboration"

# LLM Configuration
llm:
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"
    
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-sonnet"
    
  ollama:
    host: "http://localhost:11434"
    model: "llama2"

# Bologna Process Configuration
bologna:
  country: "Generic EU Member"
  ects_system: true
  quality_framework: "ESG 2015"
  
# Compliance Frameworks
compliance:
  enabled_frameworks:
    - "AACSB"
    - "Bologna Process"
    - "QAA"
  
# Blockchain Configuration  
blockchain:
  network: "ethereum_testnet"
  smart_contracts:
    credentials: true
    governance: true
"""
    
    config_path = workspace_path / "collegium.yaml"
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    click.echo(f"  ✅ Created: collegium.yaml")
    click.echo()
    click.echo("🎉 " + click.style("CollegiumAI workspace initialized successfully!", fg='green', bold=True))
    click.echo()
    click.echo("Next steps:")
    click.echo("  1. Configure your LLM API keys in collegium.yaml")
    click.echo("  2. Run: collegium system status")
    click.echo("  3. Run: collegium agent list")
    click.echo("  4. Run: collegium student enroll --help")

@cli.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed status')
@click.pass_context
def status(ctx, detailed):
    """📊 Show CollegiumAI system status"""
    cli_context = ctx.obj['cli_context']
    
    click.echo("📊 " + click.style("CollegiumAI System Status", fg='blue', bold=True))
    click.echo("=" * 50)
    
    # Check configuration
    config_path = Path(cli_context.workspace_path) / "collegium.yaml"
    if config_path.exists():
        click.echo("✅ Configuration: " + click.style("Found", fg='green'))
    else:
        click.echo("❌ Configuration: " + click.style("Missing", fg='red'))
        click.echo("   Run: collegium init")
        return
    
    # Check LLM providers
    click.echo("\n🧠 LLM Provider Status:")
    llm_providers = cli_context.config.get('llm', {})
    
    for provider in ['openai', 'anthropic', 'ollama']:
        if provider in llm_providers:
            # Check if API key is configured
            config = llm_providers[provider]
            if provider == 'ollama':
                status = "Configured" if config.get('host') else "Not Configured"
            else:
                api_key = config.get('api_key', '').replace('${', '').replace('}', '')
                env_var = os.getenv(api_key.split('_API_KEY')[0] + '_API_KEY') if '_API_KEY' in api_key else None
                status = "Ready" if env_var else "API Key Missing"
            
            color = 'green' if 'Ready' in status or 'Configured' in status else 'yellow'
            click.echo(f"  {provider}: " + click.style(status, fg=color))
        else:
            click.echo(f"  {provider}: " + click.style("Not Configured", fg='red'))
    
    # Check agents
    click.echo("\n🤖 Agent Status:")
    agents = cli_context.config.get('agents', {})
    for agent_name, agent_config in agents.items():
        enabled = agent_config.get('enabled', False)
        status = "Active" if enabled else "Disabled"
        color = 'green' if enabled else 'red'
        specialization = agent_config.get('specialization', '')
        click.echo(f"  {agent_name}: " + click.style(status, fg=color) + f" ({specialization})")
    
    if detailed:
        # Show workspace structure
        click.echo("\n📁 Workspace Structure:")
        workspace_path = Path(cli_context.workspace_path)
        for item in sorted(workspace_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                click.echo(f"  📁 {item.name}/")
            elif item.suffix in ['.yaml', '.yml', '.json']:
                click.echo(f"  📄 {item.name}")

# Demo Command
@cli.command()
@click.option('--scenario', '-s', 
              type=click.Choice(['student_transfer', 'research_collaboration', 'compliance_check']),
              default='student_transfer',
              help='Demo scenario to run')
@click.pass_context
def demo(ctx, scenario):
    """🎭 Run CollegiumAI demonstration scenarios"""
    click.echo("🎭 " + click.style("CollegiumAI Demo", fg='blue', bold=True))
    click.echo("=" * 50)
    
    if scenario == 'student_transfer':
        click.echo("🎯 Running: International Student Transfer Demo")
        click.echo("📋 Scenario: European student transferring 150 ECTS credits")
        click.echo()
        
        # Run the ReACT demo
        import subprocess
        result = subprocess.run([
            sys.executable, 
            str(project_root / "working_react_demo.py")
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            click.echo(result.stdout)
        else:
            click.echo("❌ Demo failed: " + result.stderr, err=True)
    
    elif scenario == 'research_collaboration':
        click.echo("🎯 Running: Research Collaboration Demo")
        click.echo("📋 Scenario: Multi-disciplinary AI research project")
        click.echo("⚠️  This demo is not yet implemented")
        
    elif scenario == 'compliance_check':
        click.echo("🎯 Running: Compliance Check Demo")
        click.echo("📋 Scenario: Bologna Process compliance verification")
        click.echo("⚠️  This demo is not yet implemented")

if __name__ == '__main__':
    cli()