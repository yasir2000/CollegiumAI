#!/usr/bin/env python3
"""
CollegiumAI CLI - Command Line Interface
=======================================

Comprehensive command-line utilities for developers and administrators
to interact with the CollegiumAI AI Multi-Agent Framework.

Features:
- Agent testing and interaction
- Blockchain credential management
- System administration and monitoring
- Governance compliance checking
- Bologna Process management
- Development utilities

Usage:
    collegiumai --help
    collegiumai agent test academic_advisor "Help me plan my courses"
    collegiumai blockchain issue-credential --student-id S123456
    collegiumai system status
    collegiumai governance audit --framework AACSB
    collegiumai bologna ects-calculator --credits 180
"""

import asyncio
import sys
import os
import argparse
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import colorama
from colorama import Fore, Back, Style
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown

# Add the parent directories to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from framework.core import UniversityFramework, PersonaType, GovernanceFramework, UniversityContext
from framework.agents.academic_advisor import AcademicAdvisorAgent
from framework.agents.student_services import StudentServicesAgent
from framework.agents.bologna_process import BolognaProcessAgent
from framework.blockchain.integration import BlockchainIntegration
from sdk import CollegiumAIClient, SDKConfig

# Initialize colorama and rich console
colorama.init(autoreset=True)
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('collegiumai-cli.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CollegiumAICLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.framework = None
        self.blockchain = None
        self.client = None
        self.config = {
            'api_url': 'http://localhost:4000/api/v1',
            'debug': False,
            'output_format': 'table'  # table, json, yaml
        }
    
    def load_config(self, config_path: str = None):
        """Load CLI configuration from file"""
        if config_path is None:
            config_path = os.path.expanduser('~/.collegiumai/config.json')
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                    console.print(f"✅ Loaded configuration from {config_path}", style="green")
            except Exception as e:
                console.print(f"⚠️ Failed to load config: {e}", style="yellow")
    
    def save_config(self, config_path: str = None):
        """Save CLI configuration to file"""
        if config_path is None:
            config_path = os.path.expanduser('~/.collegiumai/config.json')
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            console.print(f"✅ Configuration saved to {config_path}", style="green")
        except Exception as e:
            console.print(f"❌ Failed to save config: {e}", style="red")
    
    async def initialize_framework(self):
        """Initialize the CollegiumAI framework"""
        try:
            # Sample university context for CLI operations
            university_context = UniversityContext(
                institution_name="CollegiumAI CLI Test University",
                establishment_date=datetime(2020, 1, 1),
                location={
                    "city": "Vienna",
                    "state": "Vienna",
                    "country": "Austria"
                },
                accreditations=["AACSB", "WASC", "QAA"],
                total_students=10000,
                total_faculty=500,
                total_staff=200,
                departments=["Computer Science", "Business", "Engineering"],
                academic_programs=["Bachelor CS", "Master Business", "PhD Engineering"],
                governance_frameworks=[
                    GovernanceFramework.AACSB,
                    GovernanceFramework.WASC,
                    GovernanceFramework.BOLOGNA_PROCESS
                ]
            )
            
            self.framework = UniversityFramework(university_context)
            
            # Initialize blockchain if enabled
            if self.config.get('blockchain_enabled', True):
                try:
                    self.blockchain = BlockchainIntegration()
                    await self.blockchain.initialize()
                    console.print("✅ Blockchain integration initialized", style="green")
                except Exception as e:
                    console.print(f"⚠️ Blockchain initialization failed: {e}", style="yellow")
            
            # Initialize SDK client
            sdk_config = SDKConfig(
                api_base_url=self.config['api_url'],
                debug=self.config['debug']
            )
            self.client = CollegiumAIClient(sdk_config)
            
            console.print("✅ CollegiumAI framework initialized", style="green")
            
        except Exception as e:
            console.print(f"❌ Framework initialization failed: {e}", style="red")
            raise
    
    def print_header(self):
        """Print CLI header with branding"""
        header = Panel.fit(
            "[bold blue]CollegiumAI CLI[/bold blue]\n"
            "[dim]AI Multi-Agent Framework for Digital Universities[/dim]\n"
            f"[dim]Version 1.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
            border_style="blue"
        )
        console.print(header)
        console.print()

# Global CLI instance
cli = CollegiumAICLI()

@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.option('--api-url', '-u', help='API base URL')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'yaml']), help='Output format')
@click.pass_context
def main(ctx, config, debug, api_url, format):
    """CollegiumAI CLI - AI Multi-Agent Framework for Digital Universities"""
    ctx.ensure_object(dict)
    
    # Load configuration
    if config:
        cli.load_config(config)
    else:
        cli.load_config()
    
    # Override config with command line options
    if debug:
        cli.config['debug'] = True
    if api_url:
        cli.config['api_url'] = api_url
    if format:
        cli.config['output_format'] = format
    
    # Set up logging level
    if cli.config['debug']:
        logging.getLogger().setLevel(logging.DEBUG)
    
    cli.print_header()

# Import command modules
from .commands.agent import agent
from .commands.blockchain import blockchain
from .commands.system import system
from .commands.governance import governance
from .commands.bologna import bologna
from .commands.dev import dev
from .commands.llm import llm

# Register command groups
main.add_command(agent)
main.add_command(blockchain)
main.add_command(system)
main.add_command(governance)
main.add_command(bologna)
main.add_command(dev)
main.add_command(llm)

@main.command()
@click.option('--key', help='Configuration key to set')
@click.option('--value', help='Configuration value to set')
@click.option('--show', is_flag=True, help='Show current configuration')
def config(key, value, show):
    """Manage CLI configuration"""
    if show:
        console.print("\n[bold]Current Configuration:[/bold]")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Key")
        table.add_column("Value")
        
        for k, v in cli.config.items():
            table.add_row(str(k), str(v))
        
        console.print(table)
    
    elif key and value:
        # Convert string values to appropriate types
        if value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        
        cli.config[key] = value
        cli.save_config()
        console.print(f"✅ Set {key} = {value}", style="green")
    
    else:
        console.print("Use --show to view config or --key/--value to set values", style="yellow")

@main.command()
def version():
    """Show version information"""
    version_info = {
        "version": "1.0.0",
        "framework_version": "1.0.0",
        "python_version": sys.version,
        "platform": sys.platform,
        "build_date": "2025-10-18"
    }
    
    if cli.config['output_format'] == 'json':
        console.print(json.dumps(version_info, indent=2))
    else:
        table = Table(title="Version Information", show_header=True, header_style="bold blue")
        table.add_column("Component")
        table.add_column("Version")
        
        for key, value in version_info.items():
            if key == "python_version":
                value = value.split()[0]  # Just version number
            table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(table)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="yellow")
    except Exception as e:
        console.print(f"\n❌ Fatal error: {e}", style="red")
        if cli.config.get('debug'):
            import traceback
            console.print(traceback.format_exc())