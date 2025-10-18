"""
Agent Command Module
==================

CLI commands for interacting with AI agents, testing agent responses,
and managing agent configurations.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown

console = Console()

@click.group()
def agent():
    """AI Agent management and testing commands"""
    pass

@agent.command()
@click.argument('agent_type', type=click.Choice([
    'academic_advisor', 'student_services', 'bologna_process', 
    'admissions', 'financial_aid', 'career_services'
]))
@click.argument('query', type=str)
@click.option('--persona', '-p', type=click.Choice([
    'traditional_student', 'non_traditional_student', 'international_student',
    'graduate_student', 'faculty_member', 'staff_member'
]), default='traditional_student', help='User persona for context')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive session')
@click.option('--save', '-s', help='Save conversation to file')
def test(agent_type, query, persona, interactive, save):
    """Test AI agent with a query"""
    asyncio.run(_test_agent(agent_type, query, persona, interactive, save))

async def _test_agent(agent_type: str, query: str, persona: str, interactive: bool, save: str):
    """Internal async function for agent testing"""
    from .. import cli
    
    try:
        await cli.initialize_framework()
        
        # Get the appropriate agent
        agent_map = {
            'academic_advisor': 'AcademicAdvisorAgent',
            'student_services': 'StudentServicesAgent', 
            'bologna_process': 'BolognaProcessAgent'
        }
        
        if agent_type not in agent_map:
            console.print(f"❌ Agent type '{agent_type}' not implemented yet", style="red")
            return
        
        console.print(f"\n🤖 Testing {agent_type.replace('_', ' ').title()} Agent", style="bold blue")
        console.print(f"👤 Persona: {persona.replace('_', ' ').title()}", style="dim")
        console.print(f"❓ Query: {query}", style="dim")
        console.print()
        
        # Import and initialize the specific agent
        if agent_type == 'academic_advisor':
            from ...framework.agents.academic_advisor import AcademicAdvisorAgent
            agent = AcademicAdvisorAgent()
        elif agent_type == 'student_services':
            from ...framework.agents.student_services import StudentServicesAgent
            agent = StudentServicesAgent()
        elif agent_type == 'bologna_process':
            from ...framework.agents.bologna_process import BolognaProcessAgent
            agent = BolognaProcessAgent()
        
        conversation = []
        
        # Process the query
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing query...", total=None)
            
            try:
                response = await agent.process_query(query, cli.framework.context)
                progress.update(task, completed=True)
                
                conversation.append({
                    'timestamp': response.final_response,  # Using final_response as placeholder
                    'query': query,
                    'response': response.final_response,
                    'thoughts': [thought.__dict__ if hasattr(thought, '__dict__') else str(thought) 
                               for thought in response.thoughts],
                    'actions': [action.__dict__ if hasattr(action, '__dict__') else str(action) 
                              for action in response.actions]
                })
                
            except Exception as e:
                progress.update(task, description=f"Error: {e}")
                console.print(f"❌ Agent processing failed: {e}", style="red")
                return
        
        # Display response
        response_panel = Panel(
            response.final_response,
            title=f"🤖 {agent_type.replace('_', ' ').title()} Response",
            border_style="green"
        )
        console.print(response_panel)
        
        # Show thinking process if debug mode
        if cli.config.get('debug') and response.thoughts:
            console.print("\n🧠 Agent Thinking Process:", style="bold yellow")
            for i, thought in enumerate(response.thoughts, 1):
                thought_str = thought.__dict__ if hasattr(thought, '__dict__') else str(thought)
                console.print(f"{i}. {thought_str}", style="dim")
        
        # Interactive mode
        if interactive:
            console.print("\n💬 Interactive mode - Type 'quit' to exit")
            while True:
                try:
                    new_query = click.prompt("\nYour question", type=str)
                    if new_query.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console,
                    ) as progress:
                        task = progress.add_task("Processing...", total=None)
                        
                        response = await agent.process_query(new_query, cli.framework.context)
                        conversation.append({
                            'query': new_query,
                            'response': response.final_response
                        })
                        
                        response_panel = Panel(
                            response.final_response,
                            title="🤖 Response",
                            border_style="green"
                        )
                        console.print(response_panel)
                        
                except KeyboardInterrupt:
                    break
        
        # Save conversation if requested
        if save:
            try:
                with open(save, 'w') as f:
                    json.dump(conversation, f, indent=2, default=str)
                console.print(f"\n💾 Conversation saved to {save}", style="green")
            except Exception as e:
                console.print(f"❌ Failed to save conversation: {e}", style="red")
                
    except Exception as e:
        console.print(f"❌ Agent test failed: {e}", style="red")

@agent.command()
def list():
    """List available AI agents"""
    agents_info = [
        {
            'name': 'Academic Advisor',
            'type': 'academic_advisor',
            'description': 'Course planning, degree requirements, academic guidance',
            'status': '✅ Available'
        },
        {
            'name': 'Student Services',
            'type': 'student_services', 
            'description': 'Campus life, housing, dining, activities, support',
            'status': '✅ Available'
        },
        {
            'name': 'Bologna Process',
            'type': 'bologna_process',
            'description': 'ECTS credits, mobility programs, European qualifications',
            'status': '✅ Available'
        },
        {
            'name': 'Admissions',
            'type': 'admissions',
            'description': 'Application process, requirements, enrollment',
            'status': '🚧 Coming Soon'
        },
        {
            'name': 'Financial Aid', 
            'type': 'financial_aid',
            'description': 'Scholarships, grants, student loans, budgeting',
            'status': '🚧 Coming Soon'
        },
        {
            'name': 'Career Services',
            'type': 'career_services', 
            'description': 'Job search, internships, career guidance, networking',
            'status': '🚧 Coming Soon'
        }
    ]
    
    table = Table(title="Available AI Agents", show_header=True, header_style="bold blue")
    table.add_column("Agent Name", style="bold")
    table.add_column("Type", style="dim")
    table.add_column("Description")
    table.add_column("Status")
    
    for agent in agents_info:
        table.add_row(
            agent['name'],
            agent['type'],
            agent['description'],
            agent['status']
        )
    
    console.print(table)

@agent.command()
@click.argument('agent_type')
@click.option('--output', '-o', help='Output file for performance report') 
def benchmark(agent_type, output):
    """Benchmark agent performance with test queries"""
    asyncio.run(_benchmark_agent(agent_type, output))

async def _benchmark_agent(agent_type: str, output: str):
    """Internal async function for agent benchmarking"""
    from .. import cli
    
    test_queries = [
        "What courses should I take next semester?",
        "I'm struggling with my math class, what resources are available?", 
        "How do I apply for graduate school?",
        "What are the degree requirements for Computer Science?",
        "Can you help me plan my course schedule?"
    ]
    
    console.print(f"\n🏁 Benchmarking {agent_type} Agent", style="bold blue")
    console.print(f"📊 Running {len(test_queries)} test queries", style="dim")
    
    try:
        await cli.initialize_framework()
        
        # Import agent
        if agent_type == 'academic_advisor':
            from ...framework.agents.academic_advisor import AcademicAdvisorAgent
            agent = AcademicAdvisorAgent()
        else:
            console.print(f"❌ Benchmarking not implemented for {agent_type}", style="red")
            return
        
        results = []
        
        with Progress(console=console) as progress:
            task = progress.add_task("Benchmarking...", total=len(test_queries))
            
            for i, query in enumerate(test_queries):
                start_time = asyncio.get_event_loop().time()
                
                try:
                    response = await agent.process_query(query, cli.framework.context)
                    end_time = asyncio.get_event_loop().time()
                    
                    results.append({
                        'query': query,
                        'response_time': end_time - start_time,
                        'response_length': len(response.final_response),
                        'thoughts_count': len(response.thoughts),
                        'actions_count': len(response.actions),
                        'success': True
                    })
                    
                except Exception as e:
                    end_time = asyncio.get_event_loop().time()
                    results.append({
                        'query': query, 
                        'response_time': end_time - start_time,
                        'error': str(e),
                        'success': False
                    })
                
                progress.update(task, advance=1)
        
        # Calculate statistics
        successful = [r for r in results if r['success']]
        avg_response_time = sum(r['response_time'] for r in successful) / len(successful) if successful else 0
        success_rate = len(successful) / len(results) * 100
        
        # Display results
        console.print(f"\n📈 Benchmark Results for {agent_type}", style="bold green")
        
        stats_table = Table(show_header=False)
        stats_table.add_column("Metric", style="bold")
        stats_table.add_column("Value")
        
        stats_table.add_row("Total Queries", str(len(test_queries)))
        stats_table.add_row("Successful", str(len(successful)))
        stats_table.add_row("Success Rate", f"{success_rate:.1f}%")
        stats_table.add_row("Avg Response Time", f"{avg_response_time:.2f}s")
        
        console.print(stats_table)
        
        # Detailed results table
        if cli.config.get('debug'):
            console.print("\n📋 Detailed Results:", style="bold")
            
            results_table = Table(show_header=True, header_style="bold blue")
            results_table.add_column("Query", max_width=40)
            results_table.add_column("Time (s)")
            results_table.add_column("Status")
            
            for result in results:
                status = "✅ Success" if result['success'] else f"❌ {result.get('error', 'Failed')}"
                results_table.add_row(
                    result['query'][:37] + "..." if len(result['query']) > 40 else result['query'],
                    f"{result['response_time']:.2f}",
                    status
                )
            
            console.print(results_table)
        
        # Save results if requested
        if output:
            try:
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                console.print(f"\n💾 Benchmark results saved to {output}", style="green")
            except Exception as e:
                console.print(f"❌ Failed to save results: {e}", style="red")
                
    except Exception as e:
        console.print(f"❌ Benchmark failed: {e}", style="red")

@agent.command()
@click.argument('agent_type')
def inspect(agent_type):
    """Inspect agent configuration and capabilities"""
    console.print(f"\n🔍 Inspecting {agent_type} Agent", style="bold blue")
    
    agent_specs = {
        'academic_advisor': {
            'class': 'AcademicAdvisorAgent',
            'personas': ['traditional_student', 'non_traditional_student', 'graduate_student'],
            'capabilities': [
                'Course planning and scheduling',
                'Degree requirement analysis', 
                'Academic progress tracking',
                'Study abroad guidance',
                'Graduate school preparation'
            ],
            'governance_frameworks': ['AACSB', 'WASC', 'HEFCE'],
            'collaboration': ['student_services', 'bologna_process']
        },
        'student_services': {
            'class': 'StudentServicesAgent',
            'personas': ['traditional_student', 'non_traditional_student', 'international_student'],
            'capabilities': [
                'Campus life guidance',
                'Housing and dining support',
                'Student activities coordination',
                'Wellness and counseling referrals',
                'Emergency assistance'
            ],
            'governance_frameworks': ['HEFCE', 'QAA'],
            'collaboration': ['academic_advisor', 'financial_aid']
        },
        'bologna_process': {
            'class': 'BolognaProcessAgent',
            'personas': ['international_student', 'exchange_student'],
            'capabilities': [
                'ECTS credit calculation',
                'Mobility program planning',
                'Automatic recognition procedures',
                'Quality assurance compliance',
                'European qualification mapping'
            ],
            'governance_frameworks': ['BOLOGNA_PROCESS'],
            'collaboration': ['academic_advisor', 'admissions']
        }
    }
    
    if agent_type not in agent_specs:
        console.print(f"❌ Agent type '{agent_type}' not found", style="red")
        return
    
    spec = agent_specs[agent_type]
    
    # Agent overview
    overview_panel = Panel(
        f"[bold]Class:[/bold] {spec['class']}\n"
        f"[bold]Supported Personas:[/bold] {', '.join(spec['personas'])}\n"
        f"[bold]Governance Frameworks:[/bold] {', '.join(spec['governance_frameworks'])}\n"
        f"[bold]Collaborates With:[/bold] {', '.join(spec['collaboration'])}",
        title=f"🤖 {agent_type.replace('_', ' ').title()} Overview",
        border_style="blue"
    )
    console.print(overview_panel)
    
    # Capabilities
    console.print("\n🚀 Capabilities:", style="bold green")
    for i, capability in enumerate(spec['capabilities'], 1):
        console.print(f"  {i}. {capability}")
    
    console.print()

if __name__ == '__main__':
    agent()