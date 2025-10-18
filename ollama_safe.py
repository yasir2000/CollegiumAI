#!/usr/bin/env python3
"""
CollegiumAI Ollama Integration - Unicode Safe
============================================

Enhanced CLI with real Ollama LLM integration for Windows testing.
"""

import click
import requests
import json
import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows
if os.name == 'nt':
    import locale
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Ollama API configuration
OLLAMA_API_BASE = "http://localhost:11434"
DEFAULT_MODEL = "deepseek-r1:1.5b"

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url=OLLAMA_API_BASE):
        self.base_url = base_url
    
    def is_available(self):
        """Check if Ollama service is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def list_models(self):
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get('models', [])
        except requests.RequestException:
            return []
    
    def generate(self, model, prompt, system_prompt=None):
        """Generate response using Ollama"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            else:
                return f"Error: HTTP {response.status_code}"
                
        except requests.RequestException as e:
            return f"Connection error: {str(e)}"

@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.version_option(version='1.0.0', prog_name='CollegiumAI-Ollama')
@click.pass_context
def main(ctx, verbose):
    """
    CollegiumAI with Ollama Integration
    
    AI Multi-Agent Educational Framework with Local LLM Support
    """
    
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['ollama'] = OllamaClient()
    
    if ctx.invoked_subcommand is None:
        ollama_status = "[Connected]" if ctx.obj['ollama'].is_available() else "[Disconnected]"
        
        click.echo("=== " + click.style("CollegiumAI", fg='blue', bold=True) + " - Local LLM Edition ===")
        click.echo("=" * 80)
        click.echo("* " + click.style("AI Agents:", fg='green') + " ReACT Multi-Agent System")
        click.echo("* " + click.style("Local LLM:", fg='yellow') + f" Ollama {ollama_status}")
        click.echo("* " + click.style("Bologna Process:", fg='blue') + " European Higher Education")
        click.echo("* " + click.style("Blockchain:", fg='magenta') + " Credential Verification")
        click.echo("=" * 80)
        click.echo()
        click.echo(ctx.get_help())

@main.group()
@click.pass_context
def ollama(ctx):
    """Ollama Local LLM commands"""
    pass

@ollama.command('status')
@click.pass_context
def ollama_status(ctx):
    """Check Ollama service status"""
    client = ctx.obj['ollama']
    
    click.echo("=== " + click.style("Ollama Service Status", fg='blue', bold=True) + " ===")
    click.echo("=" * 50)
    
    if client.is_available():
        click.echo("Status: " + click.style("Connected", fg='green', bold=True))
        click.echo(f"Endpoint: {client.base_url}")
        
        models = client.list_models()
        if models:
            click.echo(f"\nAvailable Models ({len(models)}):")
            for model in models:
                name = model.get('name', 'Unknown')
                size = model.get('size', 0)
                size_gb = size / (1024**3) if size > 0 else 0
                click.echo(f"  - {name} ({size_gb:.1f} GB)")
        else:
            click.echo("\nNo models found")
    else:
        click.echo("Status: " + click.style("Disconnected", fg='red', bold=True))
        click.echo("Make sure Ollama is running: ollama serve")

@ollama.command('models')
@click.pass_context
def list_models(ctx):
    """List available Ollama models"""
    client = ctx.obj['ollama']
    
    click.echo("=== " + click.style("Ollama Models", fg='blue', bold=True) + " ===")
    click.echo("=" * 50)
    
    if not client.is_available():
        click.echo(click.style("Ollama service not available", fg='red'))
        return
    
    models = client.list_models()
    if models:
        click.echo(f"{'Model Name':<30} {'Size':<15} {'Modified':<20}")
        click.echo("-" * 65)
        
        for model in models:
            name = model.get('name', 'Unknown')
            size = model.get('size', 0)
            modified = model.get('modified_at', 'Unknown')
            
            size_gb = f"{size / (1024**3):.1f} GB" if size > 0 else "Unknown"
            modified_str = modified[:19] if modified != 'Unknown' else 'Unknown'
            
            click.echo(f"{name:<30} {size_gb:<15} {modified_str:<20}")
        
        click.echo(f"\nTotal models: {len(models)}")
    else:
        click.echo("No models available")

@main.group()
@click.pass_context
def agent(ctx):
    """AI Agent management with Ollama"""
    pass

@agent.command('chat')
@click.option('--agent', '-a', default='student_services', help='Agent to chat with')
@click.option('--message', '-m', required=True, help='Message to send')
@click.option('--model', default=DEFAULT_MODEL, help='Ollama model to use')
@click.pass_context
def chat_with_agent(ctx, agent, message, model):
    """Chat with an AI agent using Ollama"""
    client = ctx.obj['ollama']
    
    if not client.is_available():
        click.echo(click.style("Ollama service not available", fg='red'))
        return
    
    # Agent-specific system prompts
    system_prompts = {
        'student_services': """You are a Student Services AI agent for CollegiumAI university. 
                             You help students with enrollment, transfers, course registration, and academic support.
                             Be helpful, professional, and knowledgeable about university processes.""",
        
        'academic_advisor': """You are an Academic Advisor AI agent for CollegiumAI university.
                             You provide academic guidance, course planning, and career advice to students.
                             Be supportive and focus on student success.""",
        
        'bologna_process': """You are a Bologna Process AI agent specializing in European Higher Education.
                             You handle ECTS credit conversions, international transfers, and European standards compliance.
                             Be precise with academic regulations and credit calculations.""",
        
        'research_coordinator': """You are a Research Coordinator AI agent for CollegiumAI university.
                                 You assist with research projects, grant applications, and academic collaborations.
                                 Be knowledgeable about research methodologies and academic publishing."""
    }
    
    system_prompt = system_prompts.get(agent, "You are a helpful AI assistant for CollegiumAI university.")
    
    click.echo("=== " + click.style(f"Chat with {agent.replace('_', ' ').title()}", fg='blue', bold=True) + " ===")
    click.echo("=" * 60)
    click.echo(f"Model: {model}")
    click.echo(f"Message: {message}")
    click.echo("Thinking...")
    click.echo()
    
    response = client.generate(model, message, system_prompt)
    
    click.echo(click.style("Agent Response:", fg='green', bold=True))
    click.echo("-" * 40)
    click.echo(response)

@main.group()
def student():
    """Student services with AI assistance"""
    pass

@student.command('advise')
@click.option('--student-name', '-n', required=True, help='Student name')
@click.option('--question', '-q', required=True, help='Academic question')
@click.option('--model', default=DEFAULT_MODEL, help='Ollama model to use')
@click.pass_context
def student_advise(ctx, student_name, question, model):
    """Get AI-powered academic advice"""
    client = ctx.obj['ollama']
    
    if not client.is_available():
        click.echo(click.style("Ollama service not available", fg='red'))
        return
    
    system_prompt = f"""You are an Academic Advisor AI for CollegiumAI university helping {student_name}.
                       Provide personalized, constructive academic advice. Be supportive and specific.
                       Focus on actionable recommendations for student success."""
    
    prompt = f"Student {student_name} asks: {question}"
    
    click.echo("=== " + click.style("Academic Advising Session", fg='blue', bold=True) + " ===")
    click.echo("=" * 50)
    click.echo(f"Student: {student_name}")
    click.echo(f"Question: {question}")
    click.echo(f"AI Model: {model}")
    click.echo("Generating advice...")
    click.echo()
    
    response = client.generate(model, prompt, system_prompt)
    
    click.echo(click.style("Academic Advice:", fg='green', bold=True))
    click.echo("-" * 40)
    click.echo(response)

@main.command()
@click.option('--model', default=DEFAULT_MODEL, help='Ollama model to use')
@click.pass_context
def demo(ctx, model):
    """Run interactive Ollama demo"""
    client = ctx.obj['ollama']
    
    click.echo("=== " + click.style("CollegiumAI Ollama Demo", fg='blue', bold=True) + " ===")
    click.echo("=" * 60)
    
    if not client.is_available():
        click.echo(click.style("Ollama service not available", fg='red'))
        click.echo("Start Ollama: ollama serve")
        return
    
    click.echo("Ollama service: Connected")
    click.echo(f"Using model: {model}")
    click.echo()
    
    # Demo scenarios
    scenarios = [
        ("Student Enrollment", "I'm a new international student. How do I enroll for Computer Science?"),
        ("ECTS Conversion", "I have 120 ECTS credits from Germany. How many US credits is that?"),
        ("Course Planning", "What courses should I take in my first semester for AI and Machine Learning?")
    ]
    
    for title, question in scenarios:
        click.echo("=== " + click.style(f"Demo: {title}", fg='cyan', bold=True) + " ===")
        click.echo(f"Question: {question}")
        click.echo("AI thinking...")
        
        system_prompt = "You are a helpful university AI assistant. Provide concise, accurate information."
        response = client.generate(model, question, system_prompt)
        
        click.echo(click.style("Response:", fg='green'))
        # Limit response length for demo
        response_lines = response.split('\n')[:3]
        for line in response_lines:
            if line.strip():
                click.echo(f"   {line.strip()}")
        click.echo()
    
    click.echo(click.style("Demo completed!", fg='green', bold=True))

if __name__ == '__main__':
    main()