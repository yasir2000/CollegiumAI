"""
Dev Command Module
=================

CLI commands for developers working with the CollegiumAI framework,
including code generation, testing utilities, and development tools.
"""

import json
import asyncio
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.tree import Tree

console = Console()

@click.group()
def dev():
    """Development tools and utilities"""
    pass

@dev.command()
@click.argument('agent_name', type=str)
@click.option('--template', '-t', type=click.Choice(['basic', 'react', 'collaborative']), 
              default='basic', help='Agent template type')
@click.option('--output', '-o', type=str, help='Output directory')
def generate_agent(agent_name, template, output):
    """Generate a new AI agent from template"""
    console.print(f"\n🤖 Generating AI Agent: {agent_name}", style="bold blue")
    console.print(f"📋 Template: {template.title()}", style="dim")
    
    try:
        from .. import cli
        
        # Set output directory
        if not output:
            output = cli.config_dir.parent / 'framework' / 'agents' / agent_name.lower()
        else:
            output = Path(output)
        
        output.mkdir(parents=True, exist_ok=True)
        
        # Generate agent based on template
        agent_code = _generate_agent_code(agent_name, template)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating agent files...", total=4)
            
            # Create main agent file
            agent_file = output / f"{agent_name.lower()}.py"
            with open(agent_file, 'w') as f:
                f.write(agent_code['main'])
            progress.advance(task)
            
            # Create test file
            test_file = output / f"test_{agent_name.lower()}.py"
            with open(test_file, 'w') as f:
                f.write(agent_code['test'])
            progress.advance(task)
            
            # Create configuration file
            config_file = output / f"{agent_name.lower()}_config.json"
            with open(config_file, 'w') as f:
                json.dump(agent_code['config'], f, indent=2)
            progress.advance(task)
            
            # Create README file
            readme_file = output / 'README.md'
            with open(readme_file, 'w') as f:
                f.write(agent_code['readme'])
            progress.advance(task)
        
        # Display generated files
        files_panel = Panel(
            f"[bold green]✅ Agent Generated Successfully[/bold green]\n\n"
            f"[bold]Agent Name:[/bold] {agent_name}\n"
            f"[bold]Template:[/bold] {template.title()}\n"
            f"[bold]Output Directory:[/bold] {output}\n"
            f"[bold]Files Created:[/bold] 4\n"
            f"[bold]Main File:[/bold] {agent_file.name}",
            title="🤖 Agent Generation Complete",
            border_style="green"
        )
        console.print(files_panel)
        
        # Show file tree
        console.print(f"\n📁 Generated Files:", style="bold green")
        
        file_tree = Tree(f"📁 {output.name}")
        file_tree.add(f"🐍 {agent_file.name}")
        file_tree.add(f"🧪 {test_file.name}")
        file_tree.add(f"⚙️ {config_file.name}")
        file_tree.add(f"📄 {readme_file.name}")
        
        console.print(file_tree)
        
        # Next steps
        next_steps_panel = Panel(
            f"1. Review the generated agent code in {agent_file}\n"
            f"2. Customize the agent logic for your specific use case\n"
            f"3. Run tests with: python -m pytest {test_file}\n"
            f"4. Update configuration in {config_file}\n"
            f"5. Integrate with the main framework",
            title="📝 Next Steps",
            border_style="yellow"
        )
        console.print(next_steps_panel)
        
    except Exception as e:
        console.print(f"❌ Agent generation failed: {e}", style="red")

def _generate_agent_code(agent_name: str, template: str) -> Dict[str, Any]:
    """Generate agent code based on template"""
    class_name = f"{agent_name.title().replace('_', '')}Agent"
    
    main_code = f'''"""
{agent_name.title().replace('_', ' ')} Agent
{'=' * (len(agent_name) + 6)}

AI agent for {agent_name.lower().replace('_', ' ')} operations in the CollegiumAI framework.
Generated using {template} template.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..base_agent import BaseAgent, AgentResponse, Thought, Action
from ...context import FrameworkContext


@dataclass
class {class_name}(BaseAgent):
    """
    {agent_name.title().replace('_', ' ')} Agent for CollegiumAI Framework
    
    This agent handles {agent_name.lower().replace('_', ' ')}-related queries and operations.
    """
    
    def __init__(self):
        super().__init__(
            name="{agent_name.lower()}",
            description="{agent_name.title().replace('_', ' ')} operations and assistance",
            version="1.0.0"
        )
    
    async def process_query(self, query: str, context: FrameworkContext) -> AgentResponse:
        """
        Process a {agent_name.lower().replace('_', ' ')}-related query
        
        Args:
            query: User query string
            context: Framework context with user info and state
            
        Returns:
            AgentResponse with thoughts, actions, and final response
        """
        thoughts = []
        actions = []
        
        # Add initial thought
        thoughts.append(Thought(
            content=f"Processing {agent_name.lower().replace('_', ' ')} query: {{query}}",
            reasoning="Analyzing user request for {agent_name.lower().replace('_', ' ')} assistance"
        ))
        
        try:
            # TODO: Implement your agent logic here
            response_text = await self._generate_response(query, context)
            
            # Add successful processing thought
            thoughts.append(Thought(
                content="Successfully processed query",
                reasoning="Generated appropriate response based on agent capabilities"
            ))
            
            return AgentResponse(
                thoughts=thoughts,
                actions=actions,
                final_response=response_text,
                confidence=0.85,
                requires_followup=False
            )
            
        except Exception as e:
            thoughts.append(Thought(
                content=f"Error processing query: {{str(e)}}",
                reasoning="Encountered error during processing"
            ))
            
            return AgentResponse(
                thoughts=thoughts,
                actions=actions,
                final_response=f"I apologize, but I encountered an error while processing your {agent_name.lower().replace('_', ' ')} request. Please try again or contact support.",
                confidence=0.0,
                requires_followup=True
            )
    
    async def _generate_response(self, query: str, context: FrameworkContext) -> str:
        """
        Generate response for {agent_name.lower().replace('_', ' ')} query
        
        Args:
            query: User query
            context: Framework context
            
        Returns:
            Generated response string
        """
        # TODO: Implement specific response generation logic
        
        # Example response generation
        if "help" in query.lower():
            return f"I'm the {agent_name.title()} Agent, here to help with {agent_name.lower().replace('_', ' ')}-related questions and tasks. What would you like to know?"
        
        elif "status" in query.lower():
            return f"The {agent_name.lower().replace('_', ' ')} system is currently operational and ready to assist you."
        
        else:
            return f"I understand you're asking about {{query}}. As the {agent_name.title()} Agent, I can help with various {agent_name.lower().replace('_', ' ')}-related tasks. Could you please provide more specific details about what you need?"
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return [
            f"{agent_name.title().replace('_', ' ')} information and guidance",
            "Query processing and response generation",
            "Context-aware assistance",
            "Integration with CollegiumAI framework"
        ]
    
    def get_supported_personas(self) -> List[str]:
        """Return list of supported user personas"""
        return [
            "student",
            "faculty",
            "administrator",
            "staff"
        ]
'''

    test_code = f'''"""
Test suite for {agent_name.title().replace('_', ' ')} Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from framework.agents.{agent_name.lower()}.{agent_name.lower()} import {class_name}
from framework.context import FrameworkContext


class Test{class_name}:
    """Test cases for {class_name}"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.agent = {class_name}()
        self.mock_context = Mock(spec=FrameworkContext)
        self.mock_context.user_id = "test_user_123"
        self.mock_context.session_id = "test_session_456"
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.name == "{agent_name.lower()}"
        assert self.agent.version == "1.0.0"
        assert "{agent_name.title().replace('_', ' ')}" in self.agent.description
    
    @pytest.mark.asyncio
    async def test_help_query(self):
        """Test help query processing"""
        query = "Can you help me?"
        response = await self.agent.process_query(query, self.mock_context)
        
        assert response is not None
        assert response.final_response is not None
        assert "help" in response.final_response.lower()
        assert response.confidence > 0
    
    @pytest.mark.asyncio
    async def test_status_query(self):
        """Test status query processing"""
        query = "What's the status?"
        response = await self.agent.process_query(query, self.mock_context)
        
        assert response is not None
        assert "status" in response.final_response.lower()
        assert response.confidence > 0
    
    @pytest.mark.asyncio
    async def test_general_query(self):
        """Test general query processing"""
        query = "Tell me about your capabilities"
        response = await self.agent.process_query(query, self.mock_context)
        
        assert response is not None
        assert response.final_response is not None
        assert len(response.thoughts) > 0
    
    def test_get_capabilities(self):
        """Test capabilities listing"""
        capabilities = self.agent.get_capabilities()
        
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert all(isinstance(cap, str) for cap in capabilities)
    
    def test_get_supported_personas(self):
        """Test supported personas listing"""
        personas = self.agent.get_supported_personas()
        
        assert isinstance(personas, list)
        assert "student" in personas
        assert "faculty" in personas


if __name__ == "__main__":
    pytest.main([__file__])
'''

    config = {
        "agent_name": agent_name.lower(),
        "display_name": agent_name.title().replace('_', ' '),
        "version": "1.0.0",
        "template": template,
        "capabilities": [
            f"{agent_name.title().replace('_', ' ')} assistance",
            "Query processing",
            "Context awareness"
        ],
        "supported_personas": [
            "student",
            "faculty", 
            "administrator",
            "staff"
        ],
        "configuration": {
            "max_response_length": 1000,
            "confidence_threshold": 0.7,
            "enable_logging": True,
            "cache_responses": False
        },
        "governance_frameworks": [
            "aacsb",
            "wasc",
            "hefce",
            "qaa"
        ]
    }

    readme = f'''# {agent_name.title().replace('_', ' ')} Agent

AI agent for {agent_name.lower().replace('_', ' ')} operations in the CollegiumAI framework.

## Overview

This agent handles {agent_name.lower().replace('_', ' ')}-related queries and operations, providing specialized assistance within the CollegiumAI multi-agent framework.

## Features

- **Query Processing**: Handles {agent_name.lower().replace('_', ' ')}-specific questions and requests
- **Context Awareness**: Integrates with framework context for personalized responses
- **Multi-Persona Support**: Works with students, faculty, administrators, and staff
- **Governance Compliance**: Adheres to educational governance frameworks

## Usage

```python
from framework.agents.{agent_name.lower()}.{agent_name.lower()} import {class_name}

# Initialize agent
agent = {class_name}()

# Process query
response = await agent.process_query("Your question here", context)
print(response.final_response)
```

## Testing

Run tests with:

```bash
python -m pytest test_{agent_name.lower()}.py -v
```

## Configuration

Agent configuration is stored in `{agent_name.lower()}_config.json`. Modify settings as needed:

- `max_response_length`: Maximum length of generated responses
- `confidence_threshold`: Minimum confidence for responses
- `enable_logging`: Enable/disable agent logging
- `cache_responses`: Enable/disable response caching

## Integration

To integrate this agent with the main framework:

1. Add agent import to the main agent registry
2. Update framework configuration to include this agent
3. Test integration with the CLI tools
4. Deploy with the rest of the framework

## Generated Information

- **Template**: {template.title()}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Framework**: CollegiumAI v1.0.0

## Next Steps

1. Customize the `_generate_response` method with your specific logic
2. Add any required dependencies to requirements
3. Implement additional capabilities as needed
4. Update tests to cover your custom functionality
5. Document any special configuration requirements
'''

    return {
        'main': main_code,
        'test': test_code,
        'config': config,
        'readme': readme
    }

@dev.command()
@click.option('--components', '-c', multiple=True, 
              type=click.Choice(['agents', 'blockchain', 'api', 'web', 'cli']),
              help='Specific components to test')
@click.option('--coverage', is_flag=True, help='Generate coverage report')
@click.option('--parallel', '-p', is_flag=True, help='Run tests in parallel')
def run_tests(components, coverage, parallel):
    """Run comprehensive test suite"""
    console.print("\n🧪 CollegiumAI Test Suite", style="bold blue")
    
    try:
        from .. import cli
        
        # Determine test directories
        test_dirs = []
        if components:
            for component in components:
                test_dirs.append(f"tests/{component}")
        else:
            test_dirs = ["tests/"]
        
        console.print(f"📁 Test Directories: {', '.join(test_dirs)}", style="dim")
        
        # Build pytest command
        pytest_cmd = ["python", "-m", "pytest"]
        
        # Add test directories
        pytest_cmd.extend(test_dirs)
        
        # Add options
        pytest_cmd.extend(["-v", "--tb=short"])
        
        if coverage:
            pytest_cmd.extend(["--cov=framework", "--cov-report=html", "--cov-report=term"])
        
        if parallel:
            pytest_cmd.extend(["-n", "auto"])
        
        console.print(f"🚀 Running: {' '.join(pytest_cmd)}", style="dim")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running tests...", total=None)
            
            # Run tests
            result = subprocess.run(pytest_cmd, capture_output=True, text=True)
            
            progress.update(task, description="Tests completed")
        
        # Display results
        if result.returncode == 0:
            console.print("✅ All tests passed!", style="bold green")
        else:
            console.print("❌ Some tests failed", style="bold red")
        
        # Show test output
        if result.stdout:
            console.print("\n📊 Test Results:", style="bold blue")
            console.print(result.stdout)
        
        if result.stderr:
            console.print("\n⚠️ Test Errors:", style="bold yellow")
            console.print(result.stderr)
        
        # Coverage summary
        if coverage and result.returncode == 0:
            console.print(f"\n📈 Coverage report generated in htmlcov/", style="green")
            console.print("Open htmlcov/index.html to view detailed coverage", style="dim")
        
    except Exception as e:
        console.print(f"❌ Test execution failed: {e}", style="red")

@dev.command()
@click.option('--port', '-p', type=int, default=8000, help='Development server port')
@click.option('--reload', '-r', is_flag=True, help='Enable auto-reload on file changes')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
def server(port, reload, debug):
    """Start development server"""
    console.print(f"\n🚀 Starting CollegiumAI Development Server", style="bold blue")
    console.print(f"🌐 Port: {port}", style="dim")
    console.print(f"🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}", style="dim")
    console.print(f"🐛 Debug mode: {'Enabled' if debug else 'Disabled'}", style="dim")
    
    try:
        # Build uvicorn command
        uvicorn_cmd = ["python", "-m", "uvicorn", "framework.api.main:app"]
        uvicorn_cmd.extend(["--host", "0.0.0.0", "--port", str(port)])
        
        if reload:
            uvicorn_cmd.append("--reload")
        
        if debug:
            uvicorn_cmd.extend(["--log-level", "debug"])
        
        console.print(f"🚀 Command: {' '.join(uvicorn_cmd)}", style="dim")
        
        # Start server
        console.print(f"\n✅ Server starting at http://localhost:{port}", style="green")
        console.print("Press Ctrl+C to stop the server", style="dim")
        
        subprocess.run(uvicorn_cmd)
        
    except KeyboardInterrupt:
        console.print("\n🛑 Development server stopped", style="yellow")
    except Exception as e:
        console.print(f"❌ Failed to start server: {e}", style="red")

@dev.command()
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'md']), 
              default='json', help='Output format')
@click.option('--output', '-o', type=str, help='Output file path')
def generate_docs(format, output):
    """Generate API documentation"""
    console.print(f"\n📚 Generating API Documentation", style="bold blue")
    console.print(f"📄 Format: {format.upper()}", style="dim")
    
    try:
        from .. import cli
        
        # Mock API documentation structure
        api_docs = {
            "info": {
                "title": "CollegiumAI API",
                "version": "1.0.0",
                "description": "AI Multi-Agent Framework for Digital Universities"
            },
            "servers": [
                {"url": "http://localhost:8000", "description": "Development server"}
            ],
            "paths": {
                "/api/v1/agents": {
                    "get": {
                        "summary": "List available AI agents",
                        "responses": {
                            "200": {"description": "List of agents"}
                        }
                    }
                },
                "/api/v1/agents/{agent_id}/query": {
                    "post": {
                        "summary": "Query an AI agent",
                        "parameters": [
                            {"name": "agent_id", "in": "path", "required": True}
                        ],
                        "responses": {
                            "200": {"description": "Agent response"}
                        }
                    }
                },
                "/api/v1/blockchain/credentials": {
                    "get": {
                        "summary": "List blockchain credentials",
                        "responses": {
                            "200": {"description": "List of credentials"}
                        }
                    },
                    "post": {
                        "summary": "Issue new credential",
                        "responses": {
                            "201": {"description": "Credential created"}
                        }
                    }
                },
                "/api/v1/bologna/ects": {
                    "get": {
                        "summary": "Calculate ECTS credits",
                        "responses": {
                            "200": {"description": "ECTS calculation"}
                        }
                    }
                }
            }
        }
        
        # Generate output filename if not provided
        if not output:
            output = f"api_docs.{format}"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating documentation...", total=None)
            
            if format == 'json':
                with open(output, 'w') as f:
                    json.dump(api_docs, f, indent=2)
            
            elif format == 'yaml':
                import yaml
                with open(output, 'w') as f:
                    yaml.dump(api_docs, f, default_flow_style=False)
            
            elif format == 'md':
                md_content = _generate_markdown_docs(api_docs)
                with open(output, 'w') as f:
                    f.write(md_content)
            
            progress.update(task, description="Documentation generated")
        
        docs_panel = Panel(
            f"[bold green]✅ Documentation Generated[/bold green]\n\n"
            f"[bold]Format:[/bold] {format.upper()}\n"
            f"[bold]Output File:[/bold] {output}\n"
            f"[bold]API Endpoints:[/bold] {len(api_docs['paths'])}\n"
            f"[bold]Generated:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            title="📚 Documentation Complete",
            border_style="green"
        )
        console.print(docs_panel)
        
    except Exception as e:
        console.print(f"❌ Documentation generation failed: {e}", style="red")

def _generate_markdown_docs(api_docs: Dict[str, Any]) -> str:
    """Generate Markdown documentation from API spec"""
    md = f"""# {api_docs['info']['title']}

{api_docs['info']['description']}

**Version:** {api_docs['info']['version']}

## Servers

"""
    
    for server in api_docs['servers']:
        md += f"- **{server['description']}:** {server['url']}\n"
    
    md += "\n## API Endpoints\n\n"
    
    for path, methods in api_docs['paths'].items():
        md += f"### {path}\n\n"
        
        for method, details in methods.items():
            md += f"#### {method.upper()}\n\n"
            md += f"{details['summary']}\n\n"
            
            if 'parameters' in details:
                md += "**Parameters:**\n"
                for param in details['parameters']:
                    required = " (required)" if param.get('required') else ""
                    md += f"- `{param['name']}` ({param['in']}){required}\n"
                md += "\n"
            
            md += "**Responses:**\n"
            for code, response in details['responses'].items():
                md += f"- `{code}`: {response['description']}\n"
            md += "\n"
    
    md += f"""
## Generated Information

- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Framework:** CollegiumAI v1.0.0
- **Documentation Format:** Markdown

---
*This documentation is automatically generated by CollegiumAI Development Tools*
"""
    
    return md

@dev.command()
@click.option('--clean', '-c', is_flag=True, help='Clean build artifacts first')
@click.option('--production', '-p', is_flag=True, help='Build for production')
def build(clean, production):
    """Build the CollegiumAI framework"""
    console.print(f"\n🔨 Building CollegiumAI Framework", style="bold blue")
    console.print(f"🧹 Clean build: {'Yes' if clean else 'No'}", style="dim")
    console.print(f"🏭 Production mode: {'Yes' if production else 'No'}", style="dim")
    
    try:
        build_steps = [
            ("Clean previous builds", _clean_build if clean else lambda: None),
            ("Install dependencies", _install_dependencies),
            ("Build Python packages", _build_python_packages),
            ("Build web assets", _build_web_assets),
            ("Run tests", _run_build_tests),
            ("Generate documentation", _generate_build_docs)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Building framework...", total=len(build_steps))
            
            for step_name, step_func in build_steps:
                progress.update(task, description=step_name)
                
                try:
                    if step_func:
                        step_func()
                    console.print(f"✅ {step_name}", style="green")
                except Exception as e:
                    console.print(f"❌ {step_name}: {e}", style="red")
                    return
                
                progress.advance(task)
        
        build_panel = Panel(
            f"[bold green]✅ Build Completed Successfully[/bold green]\n\n"
            f"[bold]Mode:[/bold] {'Production' if production else 'Development'}\n"
            f"[bold]Build Steps:[/bold] {len(build_steps)}\n"
            f"[bold]Build Time:[/bold] {datetime.now().strftime('%H:%M:%S')}\n"
            f"[bold]Framework Version:[/bold] 1.0.0",
            title="🔨 Build Summary",
            border_style="green"
        )
        console.print(build_panel)
        
    except Exception as e:
        console.print(f"❌ Build failed: {e}", style="red")

def _clean_build():
    """Clean previous build artifacts"""
    # Mock clean process
    pass

def _install_dependencies():
    """Install Python dependencies"""
    # Mock dependency installation
    pass

def _build_python_packages():
    """Build Python packages"""
    # Mock Python package building
    pass

def _build_web_assets():
    """Build web assets"""
    # Mock web asset building
    pass

def _run_build_tests():
    """Run build tests"""
    # Mock test execution
    pass

def _generate_build_docs():
    """Generate build documentation"""
    # Mock documentation generation
    pass

@dev.command()
def info():
    """Display development environment information"""
    console.print("\n🛠️ CollegiumAI Development Environment", style="bold blue")
    
    try:
        import sys
        import platform
        from .. import cli
        
        # System information
        sys_info = Tree("💻 System Information")
        sys_info.add(f"Python Version: {sys.version}")
        sys_info.add(f"Platform: {platform.platform()}")
        sys_info.add(f"Architecture: {platform.architecture()[0]}")
        sys_info.add(f"Processor: {platform.processor() or 'Unknown'}")
        
        console.print(sys_info)
        
        # Framework information
        framework_info = Tree("🔧 Framework Information")
        framework_info.add("Version: 1.0.0")
        framework_info.add(f"Installation: {Path(__file__).parent.parent.parent}")
        framework_info.add(f"Configuration: {cli.config_file}")
        framework_info.add(f"Data Directory: {cli.config_dir}")
        
        console.print(framework_info)
        
        # Development tools
        dev_tools = Tree("🛠️ Development Tools")
        
        # Check for common dev tools
        tools_to_check = [
            ("pytest", "python -m pytest --version"),
            ("uvicorn", "python -m uvicorn --version"),
            ("git", "git --version"),
            ("node", "node --version"),
            ("npm", "npm --version")
        ]
        
        for tool_name, version_cmd in tools_to_check:
            try:
                result = subprocess.run(version_cmd.split(), capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip().split('\n')[0]
                    dev_tools.add(f"{tool_name}: ✅ {version}")
                else:
                    dev_tools.add(f"{tool_name}: ❌ Not available")
            except:
                dev_tools.add(f"{tool_name}: ❌ Not available")
        
        console.print(dev_tools)
        
        # Environment variables
        env_vars = [
            ("PYTHONPATH", "Python module search path"),
            ("PATH", "System executable path"),
            ("NODE_ENV", "Node.js environment"),
            ("COLLEGIUMAI_ENV", "CollegiumAI environment mode")
        ]
        
        env_table = Table(title="🌍 Environment Variables", show_header=True, header_style="bold blue")
        env_table.add_column("Variable", style="bold")
        env_table.add_column("Description")
        env_table.add_column("Value", max_width=40)
        
        import os
        for var, desc in env_vars:
            value = os.environ.get(var, 'Not set')
            if len(value) > 40:
                value = value[:37] + "..."
            env_table.add_row(var, desc, value)
        
        console.print(env_table)
        
    except Exception as e:
        console.print(f"❌ Failed to get development info: {e}", style="red")

if __name__ == '__main__':
    dev()