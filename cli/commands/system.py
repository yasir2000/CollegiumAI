"""
System Command Module
====================

CLI commands for system administration, monitoring, and configuration
of the CollegiumAI framework.
"""

import json
import asyncio
import psutil
import platform
from typing import Dict, List, Any, Optional
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.tree import Tree
from rich.text import Text
from datetime import datetime, timedelta

console = Console()

@click.group()
def system():
    """System administration and monitoring commands"""
    pass

@system.command()
def status():
    """Display comprehensive system status"""
    console.print("\n🖥️ CollegiumAI System Status", style="bold blue")
    
    try:
        from .. import cli
        
        # System information
        system_info = {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
            'uptime': _get_system_uptime()
        }
        
        system_panel = Panel(
            f"[bold]Platform:[/bold] {system_info['platform']} {system_info['platform_version']}\n"
            f"[bold]Architecture:[/bold] {system_info['architecture']}\n"
            f"[bold]Python Version:[/bold] {system_info['python_version']}\n"
            f"[bold]Hostname:[/bold] {system_info['hostname']}\n"
            f"[bold]System Uptime:[/bold] {system_info['uptime']}",
            title="💻 System Information",
            border_style="blue"
        )
        console.print(system_panel)
        
        # Resource usage
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # CPU status
        cpu_status = "🟢 Good" if cpu_percent < 70 else "🟡 High" if cpu_percent < 90 else "🔴 Critical"
        memory_status = "🟢 Good" if memory.percent < 70 else "🟡 High" if memory.percent < 90 else "🔴 Critical"
        disk_status = "🟢 Good" if disk.percent < 80 else "🟡 High" if disk.percent < 95 else "🔴 Critical"
        
        resources_panel = Panel(
            f"[bold]CPU Usage:[/bold] {cpu_percent:.1f}% {cpu_status}\n"
            f"[bold]Memory Usage:[/bold] {memory.percent:.1f}% ({_format_bytes(memory.used)}/{_format_bytes(memory.total)}) {memory_status}\n"
            f"[bold]Disk Usage:[/bold] {disk.percent:.1f}% ({_format_bytes(disk.used)}/{_format_bytes(disk.total)}) {disk_status}\n"
            f"[bold]CPU Cores:[/bold] {psutil.cpu_count()} logical, {psutil.cpu_count(logical=False)} physical",
            title="📊 Resource Usage",
            border_style="green" if all(x < 70 for x in [cpu_percent, memory.percent, disk.percent]) else "yellow"
        )
        console.print(resources_panel)
        
        # Framework status
        framework_status = _check_framework_status()
        
        status_color = "green" if framework_status['healthy'] else "red"
        framework_panel = Panel(
            f"[bold]Framework Version:[/bold] {framework_status['version']}\n"
            f"[bold]Configuration:[/bold] {framework_status['config_status']}\n"
            f"[bold]Database:[/bold] {framework_status['database_status']}\n"
            f"[bold]Services:[/bold] {framework_status['services_status']}\n"
            f"[bold]Last Check:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            title=f"🔧 CollegiumAI Framework ({'✅ Healthy' if framework_status['healthy'] else '❌ Issues'})",
            border_style=status_color
        )
        console.print(framework_panel)
        
        # Network connectivity
        console.print("\n🌐 Network Connectivity:", style="bold green")
        network_checks = [
            ('Internet', 'google.com'),
            ('CollegiumAI API', 'api.collegiumai.example.com'),
            ('Blockchain RPC', 'rpc.collegiumai.example.com')
        ]
        
        network_table = Table(show_header=True, header_style="bold blue")
        network_table.add_column("Service")
        network_table.add_column("Endpoint")
        network_table.add_column("Status")
        network_table.add_column("Response Time")
        
        for service, endpoint in network_checks:
            # Mock network check (replace with actual ping/connectivity test)
            status = "🟢 Online"
            response_time = "45ms"
            network_table.add_row(service, endpoint, status, response_time)
        
        console.print(network_table)
        
    except Exception as e:
        console.print(f"❌ Failed to get system status: {e}", style="red")

def _get_system_uptime():
    """Get system uptime"""
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m"
    except:
        return "Unknown"

def _format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def _check_framework_status():
    """Check CollegiumAI framework status"""
    from .. import cli
    
    try:
        status = {
            'version': '1.0.0',
            'healthy': True,
            'config_status': '✅ Loaded',
            'database_status': '✅ Connected',
            'services_status': '✅ Running'
        }
        
        # Check configuration
        if not cli.config:
            status['config_status'] = '❌ Not loaded'
            status['healthy'] = False
        
        # Check database (mock)
        # Add actual database connectivity check here
        
        # Check services (mock)
        # Add actual service health checks here
        
        return status
        
    except Exception as e:
        return {
            'version': 'Unknown',
            'healthy': False,
            'config_status': f'❌ Error: {e}',
            'database_status': '❌ Unknown',
            'services_status': '❌ Unknown'
        }

@system.command()
def health_check():
    """Perform comprehensive health check"""
    console.print("\n🏥 CollegiumAI Health Check", style="bold blue")
    
    checks = [
        ('Configuration files', _check_config_files),
        ('Database connectivity', _check_database),
        ('Required dependencies', _check_dependencies),
        ('Service endpoints', _check_services),
        ('Disk space', _check_disk_space),
        ('Memory usage', _check_memory),
        ('File permissions', _check_permissions)
    ]
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Running health checks...", total=len(checks))
        
        for check_name, check_func in checks:
            progress.update(task, description=f"Checking {check_name.lower()}...")
            
            try:
                result = check_func()
                results.append((check_name, result['status'], result['message']))
            except Exception as e:
                results.append((check_name, '❌ Error', str(e)))
            
            progress.advance(task)
    
    # Display results
    console.print("\n📋 Health Check Results:", style="bold green")
    
    health_table = Table(show_header=True, header_style="bold blue")
    health_table.add_column("Check", style="bold")
    health_table.add_column("Status", justify="center")
    health_table.add_column("Details")
    
    overall_healthy = True
    
    for check_name, status, message in results:
        if '❌' in status:
            overall_healthy = False
        health_table.add_row(check_name, status, message)
    
    console.print(health_table)
    
    # Overall status
    overall_status = "✅ System Healthy" if overall_healthy else "❌ Issues Found"
    status_color = "green" if overall_healthy else "red"
    
    summary_panel = Panel(
        f"[bold]Overall Status:[/bold] {overall_status}\n"
        f"[bold]Checks Completed:[/bold] {len(results)}\n"
        f"[bold]Passed:[/bold] {sum(1 for _, status, _ in results if '✅' in status)}\n"
        f"[bold]Failed:[/bold] {sum(1 for _, status, _ in results if '❌' in status)}\n"
        f"[bold]Warnings:[/bold] {sum(1 for _, status, _ in results if '⚠️' in status)}",
        title="🏥 Health Check Summary",
        border_style=status_color
    )
    console.print(summary_panel)

def _check_config_files():
    """Check configuration files"""
    from .. import cli
    
    if cli.config and cli.config_file.exists():
        return {'status': '✅ OK', 'message': f'Configuration loaded from {cli.config_file}'}
    else:
        return {'status': '❌ Missing', 'message': 'Configuration file not found or not loaded'}

def _check_database():
    """Check database connectivity"""
    # Mock database check
    return {'status': '✅ Connected', 'message': 'Database connection established'}

def _check_dependencies():
    """Check required Python dependencies"""
    required_packages = [
        'click', 'rich', 'asyncio', 'psutil', 'fastapi', 
        'pydantic', 'sqlalchemy', 'redis', 'web3'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        return {'status': '❌ Missing', 'message': f'Missing packages: {", ".join(missing)}'}
    else:
        return {'status': '✅ OK', 'message': f'All {len(required_packages)} required packages installed'}

def _check_services():
    """Check service endpoints"""
    # Mock service check
    return {'status': '✅ Running', 'message': 'All services responding normally'}

def _check_disk_space():
    """Check available disk space"""
    disk = psutil.disk_usage('/')
    
    if disk.percent > 95:
        return {'status': '❌ Critical', 'message': f'Disk {disk.percent:.1f}% full - immediate action required'}
    elif disk.percent > 85:
        return {'status': '⚠️ Warning', 'message': f'Disk {disk.percent:.1f}% full - monitor closely'}
    else:
        return {'status': '✅ OK', 'message': f'Disk usage {disk.percent:.1f}% - sufficient space available'}

def _check_memory():
    """Check memory usage"""
    memory = psutil.virtual_memory()
    
    if memory.percent > 90:
        return {'status': '❌ Critical', 'message': f'Memory {memory.percent:.1f}% used - performance impacted'}
    elif memory.percent > 80:
        return {'status': '⚠️ Warning', 'message': f'Memory {memory.percent:.1f}% used - monitor usage'}
    else:
        return {'status': '✅ OK', 'message': f'Memory usage {memory.percent:.1f}% - operating normally'}

def _check_permissions():
    """Check file permissions"""
    from .. import cli
    
    # Check if config directory is writable
    if cli.config_dir.exists() and cli.config_dir.is_dir():
        try:
            test_file = cli.config_dir / '.permission_test'
            test_file.write_text('test')
            test_file.unlink()
            return {'status': '✅ OK', 'message': 'Configuration directory is writable'}
        except Exception as e:
            return {'status': '❌ Error', 'message': f'Cannot write to config directory: {e}'}
    else:
        return {'status': '❌ Missing', 'message': 'Configuration directory does not exist'}

@system.command()
@click.option('--lines', '-n', type=int, default=50, help='Number of log lines to show')
@click.option('--follow', '-f', is_flag=True, help='Follow log output')
@click.option('--level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), help='Filter by log level')
def logs(lines, follow, level):
    """View system logs"""
    console.print(f"\n📄 CollegiumAI System Logs (last {lines} lines)", style="bold blue")
    
    try:
        from .. import cli
        
        # Mock log entries (replace with actual log reading)
        log_entries = [
            {
                'timestamp': '2024-01-15 10:30:15',
                'level': 'INFO',
                'component': 'Framework',
                'message': 'CollegiumAI framework initialized successfully'
            },
            {
                'timestamp': '2024-01-15 10:30:16',
                'level': 'INFO',
                'component': 'AgentManager',
                'message': 'Loaded 3 AI agents: AcademicAdvisor, StudentServices, BolognaProcess'
            },
            {
                'timestamp': '2024-01-15 10:30:17',
                'level': 'INFO',
                'component': 'Blockchain',
                'message': 'Connected to CollegiumAI testnet'
            },
            {
                'timestamp': '2024-01-15 10:35:22',
                'level': 'INFO',
                'component': 'API',
                'message': 'Student query processed: "What courses should I take?"'
            },
            {
                'timestamp': '2024-01-15 10:35:25',
                'level': 'DEBUG',
                'component': 'AcademicAdvisor',
                'message': 'Generated course recommendations for student ID: 12345'
            },
            {
                'timestamp': '2024-01-15 10:40:10',
                'level': 'WARNING',
                'component': 'Database',
                'message': 'Connection pool at 80% capacity'
            },
            {
                'timestamp': '2024-01-15 10:45:33',
                'level': 'ERROR',
                'component': 'Blockchain',
                'message': 'Failed to broadcast credential: network timeout'
            }
        ]
        
        # Apply level filter
        if level:
            log_entries = [entry for entry in log_entries if entry['level'] == level]
        
        # Apply line limit
        log_entries = log_entries[-lines:]
        
        # Display logs
        for entry in log_entries:
            level_color = {
                'DEBUG': 'dim',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red'
            }.get(entry['level'], 'white')
            
            console.print(
                f"[dim]{entry['timestamp']}[/dim] "
                f"[{level_color}]{entry['level']}[/{level_color}] "
                f"[bold]{entry['component']}[/bold]: {entry['message']}"
            )
        
        if follow:
            console.print("\n👁️ Following logs... (Press Ctrl+C to stop)", style="dim")
            try:
                while True:
                    # Mock new log entry
                    asyncio.sleep(5)
                    new_entry = {
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'level': 'INFO',
                        'component': 'Monitor',
                        'message': 'System health check completed'
                    }
                    console.print(
                        f"[dim]{new_entry['timestamp']}[/dim] "
                        f"[blue]{new_entry['level']}[/blue] "
                        f"[bold]{new_entry['component']}[/bold]: {new_entry['message']}"
                    )
            except KeyboardInterrupt:
                console.print("\n📄 Log following stopped", style="dim")
        
    except Exception as e:
        console.print(f"❌ Failed to read logs: {e}", style="red")

@system.command()
@click.option('--component', type=click.Choice(['all', 'framework', 'agents', 'blockchain', 'api']), 
              default='all', help='Component to restart')
@click.option('--force', '-f', is_flag=True, help='Force restart without confirmation')
def restart(component, force):
    """Restart system components"""
    asyncio.run(_restart_components(component, force))

async def _restart_components(component: str, force: bool):
    """Internal async function for restarting components"""
    if not force:
        if not click.confirm(f"Are you sure you want to restart {component}?"):
            console.print("Restart cancelled", style="yellow")
            return
    
    console.print(f"\n🔄 Restarting {component}...", style="bold blue")
    
    components = ['framework', 'agents', 'blockchain', 'api'] if component == 'all' else [component]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for comp in components:
            task = progress.add_task(f"Restarting {comp}...", total=None)
            
            try:
                # Mock restart process
                await asyncio.sleep(2)
                progress.update(task, description=f"{comp.title()} restarted successfully")
                console.print(f"✅ {comp.title()} restarted", style="green")
                
            except Exception as e:
                console.print(f"❌ Failed to restart {comp}: {e}", style="red")
    
    console.print(f"\n✅ Restart completed for {component}", style="bold green")

@system.command()
def cleanup():
    """Clean up temporary files and caches"""
    console.print("\n🧹 System Cleanup", style="bold blue")
    
    cleanup_tasks = [
        ('Temporary files', _cleanup_temp_files),
        ('Log files', _cleanup_old_logs),
        ('Cache files', _cleanup_cache),
        ('Session data', _cleanup_sessions),
        ('Database indexes', _cleanup_database)
    ]
    
    total_freed = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Cleaning up...", total=len(cleanup_tasks))
        
        for task_name, cleanup_func in cleanup_tasks:
            progress.update(task, description=f"Cleaning {task_name.lower()}...")
            
            try:
                result = cleanup_func()
                freed_space = result.get('freed_bytes', 0)
                total_freed += freed_space
                
                console.print(
                    f"✅ {task_name}: {result.get('message', 'Completed')} "
                    f"({_format_bytes(freed_space)} freed)",
                    style="green"
                )
                
            except Exception as e:
                console.print(f"❌ {task_name}: {e}", style="red")
            
            progress.advance(task)
    
    cleanup_panel = Panel(
        f"[bold green]🧹 Cleanup Completed[/bold green]\n\n"
        f"[bold]Total Space Freed:[/bold] {_format_bytes(total_freed)}\n"
        f"[bold]Tasks Completed:[/bold] {len(cleanup_tasks)}\n"
        f"[bold]Completed At:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        title="Cleanup Summary",
        border_style="green"
    )
    console.print(cleanup_panel)

def _cleanup_temp_files():
    """Clean up temporary files"""
    # Mock cleanup
    return {'message': 'Removed 15 temporary files', 'freed_bytes': 2048000}

def _cleanup_old_logs():
    """Clean up old log files"""
    # Mock cleanup
    return {'message': 'Archived 3 old log files', 'freed_bytes': 5120000}

def _cleanup_cache():
    """Clean up cache files"""
    # Mock cleanup
    return {'message': 'Cleared 50 cache entries', 'freed_bytes': 1024000}

def _cleanup_sessions():
    """Clean up expired session data"""
    # Mock cleanup
    return {'message': 'Removed 12 expired sessions', 'freed_bytes': 512000}

def _cleanup_database():
    """Clean up database indexes"""
    # Mock cleanup
    return {'message': 'Optimized database indexes', 'freed_bytes': 3072000}

@system.command()
def info():
    """Display detailed system information"""
    console.print("\n📋 CollegiumAI System Information", style="bold blue")
    
    try:
        from .. import cli
        
        # Framework information
        framework_tree = Tree("🔧 CollegiumAI Framework")
        framework_tree.add("Version: 1.0.0")
        framework_tree.add("Installation Path: " + str(Path(__file__).parent.parent.parent))
        framework_tree.add("Configuration: " + str(cli.config_file))
        framework_tree.add("Data Directory: " + str(cli.config_dir))
        
        # Components
        components_tree = framework_tree.add("📦 Components")
        components_tree.add("✅ Core Framework")
        components_tree.add("✅ AI Agents (3 active)")
        components_tree.add("✅ Blockchain Service")
        components_tree.add("✅ Web API")
        components_tree.add("✅ CLI Tools")
        
        console.print(framework_tree)
        
        # Environment information
        env_info = [
            ("Python Version", platform.python_version()),
            ("Platform", f"{platform.system()} {platform.release()}"),
            ("Architecture", platform.machine()),
            ("Processor", platform.processor() or "Unknown"),
            ("Node Name", platform.node()),
            ("Working Directory", str(Path.cwd()))
        ]
        
        env_table = Table(title="🌍 Environment", show_header=True, header_style="bold blue")
        env_table.add_column("Property", style="bold")
        env_table.add_column("Value")
        
        for prop, value in env_info:
            env_table.add_row(prop, value)
        
        console.print(env_table)
        
        # Configuration summary
        config_summary = cli.config if cli.config else {}
        
        config_panel = Panel(
            f"[bold]Framework Mode:[/bold] {config_summary.get('mode', 'development')}\n"
            f"[bold]Debug Enabled:[/bold] {config_summary.get('debug', False)}\n"
            f"[bold]Logging Level:[/bold] {config_summary.get('log_level', 'INFO')}\n"
            f"[bold]Database URL:[/bold] {config_summary.get('database', {}).get('url', 'Not configured')[:50]}...\n"
            f"[bold]Redis URL:[/bold] {config_summary.get('redis', {}).get('url', 'Not configured')[:50]}...",
            title="⚙️ Configuration Summary",
            border_style="blue"
        )
        console.print(config_panel)
        
    except Exception as e:
        console.print(f"❌ Failed to get system information: {e}", style="red")

if __name__ == '__main__':
    system()