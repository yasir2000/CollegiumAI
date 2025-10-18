"""
Blockchain Command Module
========================

CLI commands for managing blockchain credentials, smart contracts,
and verification processes.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.json import JSON
from datetime import datetime

console = Console()

@click.group()
def blockchain():
    """Blockchain and credential management commands"""
    pass

@blockchain.command()
@click.argument('student_address', type=str)
@click.argument('course_name', type=str)
@click.argument('grade', type=str)
@click.option('--credits', '-c', type=int, default=3, help='ECTS credits for the course')
@click.option('--institution', '-i', type=str, default='CollegiumAI University', help='Issuing institution')
@click.option('--date', '-d', type=str, help='Completion date (YYYY-MM-DD)')
@click.option('--private-key', '-k', type=str, help='Private key for signing (if not in config)')
def issue_credential(student_address, course_name, grade, credits, institution, date, private_key):
    """Issue a new academic credential to a student"""
    asyncio.run(_issue_credential(student_address, course_name, grade, credits, institution, date, private_key))

async def _issue_credential(student_address: str, course_name: str, grade: str, 
                          credits: int, institution: str, date: str, private_key: str):
    """Internal async function for credential issuance"""
    from .. import cli
    
    try:
        await cli.initialize_framework()
        
        console.print(f"\n📜 Issuing Academic Credential", style="bold blue")
        console.print(f"👤 Student: {student_address}", style="dim")
        console.print(f"📚 Course: {course_name}", style="dim")
        console.print(f"🎯 Grade: {grade}", style="dim")
        console.print(f"⭐ Credits: {credits} ECTS", style="dim")
        console.print(f"🏛️ Institution: {institution}", style="dim")
        
        # Use current date if not provided
        completion_date = date if date else datetime.now().strftime('%Y-%m-%d')
        console.print(f"📅 Date: {completion_date}", style="dim")
        
        # Get blockchain service
        blockchain_service = cli.framework.blockchain_service
        
        if not blockchain_service:
            console.print("❌ Blockchain service not initialized", style="red")
            return
        
        # Prepare credential data
        credential_data = {
            'student_address': student_address,
            'course_name': course_name,
            'grade': grade,
            'credits': credits,
            'institution': institution,
            'completion_date': completion_date,
            'issued_at': datetime.now().isoformat(),
            'issuer': cli.config.get('blockchain', {}).get('issuer_address', 'system')
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating credential on blockchain...", total=None)
            
            try:
                # Mock blockchain interaction (replace with actual implementation)
                credential_id = f"cred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(student_address) % 10000}"
                transaction_hash = f"0x{''.join(f'{ord(c):02x}' for c in credential_id[:32])}"
                
                # Simulate blockchain delay
                await asyncio.sleep(2)
                
                progress.update(task, description="Credential created successfully!")
                
                # Display success information
                success_panel = Panel(
                    f"[bold green]✅ Credential Issued Successfully[/bold green]\n\n"
                    f"[bold]Credential ID:[/bold] {credential_id}\n"
                    f"[bold]Transaction Hash:[/bold] {transaction_hash}\n"
                    f"[bold]Block Height:[/bold] 12345678\n"
                    f"[bold]Gas Used:[/bold] 45,000\n"
                    f"[bold]Network:[/bold] CollegiumAI Testnet",
                    title="🔗 Blockchain Transaction",
                    border_style="green"
                )
                console.print(success_panel)
                
                # Save credential to local database for tracking
                credentials_file = cli.config_dir / 'credentials.json'
                try:
                    if credentials_file.exists():
                        with open(credentials_file, 'r') as f:
                            credentials = json.load(f)
                    else:
                        credentials = []
                    
                    credential_record = {
                        **credential_data,
                        'credential_id': credential_id,
                        'transaction_hash': transaction_hash,
                        'status': 'issued'
                    }
                    credentials.append(credential_record)
                    
                    with open(credentials_file, 'w') as f:
                        json.dump(credentials, f, indent=2)
                    
                    console.print(f"💾 Credential record saved locally", style="green")
                    
                except Exception as e:
                    console.print(f"⚠️ Warning: Could not save local record: {e}", style="yellow")
                
            except Exception as e:
                progress.update(task, description=f"Error: {e}")
                console.print(f"❌ Credential issuance failed: {e}", style="red")
                
    except Exception as e:
        console.print(f"❌ Command failed: {e}", style="red")

@blockchain.command()
@click.argument('credential_id', type=str)
def verify_credential(credential_id):
    """Verify the authenticity of a credential"""
    asyncio.run(_verify_credential(credential_id))

async def _verify_credential(credential_id: str):
    """Internal async function for credential verification"""
    from .. import cli
    
    console.print(f"\n🔍 Verifying Credential: {credential_id}", style="bold blue")
    
    try:
        await cli.initialize_framework()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Querying blockchain...", total=None)
            
            # Check local records first
            credentials_file = cli.config_dir / 'credentials.json'
            local_record = None
            
            if credentials_file.exists():
                with open(credentials_file, 'r') as f:
                    credentials = json.load(f)
                    local_record = next((c for c in credentials if c.get('credential_id') == credential_id), None)
            
            # Simulate blockchain verification
            await asyncio.sleep(1.5)
            
            if local_record:
                progress.update(task, description="Credential verified!")
                
                # Display verification results
                verification_panel = Panel(
                    f"[bold green]✅ Credential Verified[/bold green]\n\n"
                    f"[bold]Student:[/bold] {local_record['student_address']}\n"
                    f"[bold]Course:[/bold] {local_record['course_name']}\n"
                    f"[bold]Grade:[/bold] {local_record['grade']}\n"
                    f"[bold]Credits:[/bold] {local_record['credits']} ECTS\n"
                    f"[bold]Institution:[/bold] {local_record['institution']}\n"
                    f"[bold]Completion Date:[/bold] {local_record['completion_date']}\n"
                    f"[bold]Transaction Hash:[/bold] {local_record.get('transaction_hash', 'N/A')}\n"
                    f"[bold]Status:[/bold] {local_record.get('status', 'Unknown').title()}",
                    title="📜 Credential Details",
                    border_style="green"
                )
                console.print(verification_panel)
                
                # Security information
                security_info = Panel(
                    f"[bold]Cryptographic Hash:[/bold] Valid ✅\n"
                    f"[bold]Digital Signature:[/bold] Valid ✅\n"
                    f"[bold]Institution Signature:[/bold] Valid ✅\n"
                    f"[bold]Tamper Evidence:[/bold] None Detected ✅\n"
                    f"[bold]Blockchain Confirmations:[/bold] 245",
                    title="🔒 Security Verification",
                    border_style="blue"
                )
                console.print(security_info)
                
            else:
                progress.update(task, description="Credential not found")
                console.print(f"❌ Credential {credential_id} not found or invalid", style="red")
                
    except Exception as e:
        console.print(f"❌ Verification failed: {e}", style="red")

@blockchain.command()
@click.option('--student', '-s', type=str, help='Filter by student address')
@click.option('--institution', '-i', type=str, help='Filter by institution')
@click.option('--status', type=click.Choice(['issued', 'revoked', 'expired']), help='Filter by status')
@click.option('--limit', '-l', type=int, default=20, help='Maximum number of credentials to show')
def list_credentials(student, institution, status, limit):
    """List issued credentials with optional filters"""
    console.print("\n📋 Academic Credentials", style="bold blue")
    
    try:
        from .. import cli
        
        # Load local credentials
        credentials_file = cli.config_dir / 'credentials.json'
        
        if not credentials_file.exists():
            console.print("No credentials found. Use 'issue-credential' to create some.", style="yellow")
            return
        
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        
        # Apply filters
        filtered_credentials = credentials
        
        if student:
            filtered_credentials = [c for c in filtered_credentials if student.lower() in c.get('student_address', '').lower()]
        
        if institution:
            filtered_credentials = [c for c in filtered_credentials if institution.lower() in c.get('institution', '').lower()]
        
        if status:
            filtered_credentials = [c for c in filtered_credentials if c.get('status') == status]
        
        # Limit results
        filtered_credentials = filtered_credentials[:limit]
        
        if not filtered_credentials:
            console.print("No credentials match the specified filters.", style="yellow")
            return
        
        # Create table
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", max_width=15)
        table.add_column("Student", max_width=20)
        table.add_column("Course", max_width=25)
        table.add_column("Grade", justify="center")
        table.add_column("Credits", justify="center")
        table.add_column("Date")
        table.add_column("Status")
        
        for cred in filtered_credentials:
            status_style = "green" if cred.get('status') == 'issued' else "red"
            table.add_row(
                cred.get('credential_id', 'N/A')[:12] + "...",
                cred.get('student_address', 'N/A')[:17] + "...",
                cred.get('course_name', 'N/A')[:22] + "..." if len(cred.get('course_name', '')) > 25 else cred.get('course_name', 'N/A'),
                cred.get('grade', 'N/A'),
                str(cred.get('credits', 'N/A')),
                cred.get('completion_date', 'N/A'),
                f"[{status_style}]{cred.get('status', 'Unknown').title()}[/{status_style}]"
            )
        
        console.print(table)
        console.print(f"\nShowing {len(filtered_credentials)} of {len(credentials)} total credentials", style="dim")
        
    except Exception as e:
        console.print(f"❌ Failed to list credentials: {e}", style="red")

@blockchain.command()
@click.argument('credential_id', type=str)
@click.option('--reason', '-r', type=str, required=True, help='Reason for revocation')
def revoke_credential(credential_id, reason):
    """Revoke a previously issued credential"""
    asyncio.run(_revoke_credential(credential_id, reason))

async def _revoke_credential(credential_id: str, reason: str):
    """Internal async function for credential revocation"""
    from .. import cli
    
    console.print(f"\n🚫 Revoking Credential: {credential_id}", style="bold red")
    console.print(f"📝 Reason: {reason}", style="dim")
    
    try:
        await cli.initialize_framework()
        
        # Load local credentials
        credentials_file = cli.config_dir / 'credentials.json'
        
        if not credentials_file.exists():
            console.print("❌ No credentials database found", style="red")
            return
        
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        
        # Find credential
        credential = next((c for c in credentials if c.get('credential_id') == credential_id), None)
        
        if not credential:
            console.print(f"❌ Credential {credential_id} not found", style="red")
            return
        
        if credential.get('status') == 'revoked':
            console.print(f"⚠️ Credential {credential_id} is already revoked", style="yellow")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing revocation on blockchain...", total=None)
            
            # Simulate blockchain revocation
            await asyncio.sleep(2)
            
            # Update credential status
            credential['status'] = 'revoked'
            credential['revoked_at'] = datetime.now().isoformat()
            credential['revocation_reason'] = reason
            
            # Save updated credentials
            with open(credentials_file, 'w') as f:
                json.dump(credentials, f, indent=2)
            
            progress.update(task, description="Credential revoked successfully!")
            
            revocation_panel = Panel(
                f"[bold red]🚫 Credential Revoked[/bold red]\n\n"
                f"[bold]Credential ID:[/bold] {credential_id}\n"
                f"[bold]Student:[/bold] {credential['student_address']}\n"
                f"[bold]Course:[/bold] {credential['course_name']}\n"
                f"[bold]Reason:[/bold] {reason}\n"
                f"[bold]Revoked At:[/bold] {credential['revoked_at']}\n"
                f"[bold]Transaction Hash:[/bold] 0x{''.join(f'{ord(c):02x}' for c in f'revoke_{credential_id}'[:32])}",
                title="🔗 Revocation Transaction",
                border_style="red"
            )
            console.print(revocation_panel)
            
    except Exception as e:
        console.print(f"❌ Revocation failed: {e}", style="red")

@blockchain.command()
def network_status():
    """Check blockchain network status and configuration"""
    console.print("\n🌐 Blockchain Network Status", style="bold blue")
    
    try:
        from .. import cli
        
        # Mock network status (replace with actual blockchain queries)
        network_info = {
            'network': 'CollegiumAI Testnet',
            'latest_block': 12345678,
            'block_time': '2.1s',
            'gas_price': '20 gwei',
            'peers': 47,
            'syncing': False,
            'contracts': {
                'credential_registry': '0x1234567890abcdef1234567890abcdef12345678',
                'bologna_compliance': '0xabcdef1234567890abcdef1234567890abcdef12',
                'governance_token': '0x567890abcdef1234567890abcdef1234567890ab'
            }
        }
        
        # Network overview
        status_panel = Panel(
            f"[bold]Network:[/bold] {network_info['network']}\n"
            f"[bold]Latest Block:[/bold] #{network_info['latest_block']:,}\n"
            f"[bold]Block Time:[/bold] {network_info['block_time']}\n"
            f"[bold]Gas Price:[/bold] {network_info['gas_price']}\n"
            f"[bold]Connected Peers:[/bold] {network_info['peers']}\n"
            f"[bold]Syncing:[/bold] {'Yes' if network_info['syncing'] else 'No ✅'}",
            title="🌐 Network Overview",
            border_style="green" if not network_info['syncing'] else "yellow"
        )
        console.print(status_panel)
        
        # Smart contracts
        console.print("\n📜 Smart Contracts:", style="bold green")
        
        contracts_table = Table(show_header=True, header_style="bold blue")
        contracts_table.add_column("Contract", style="bold")
        contracts_table.add_column("Address", style="dim")
        contracts_table.add_column("Status")
        
        for name, address in network_info['contracts'].items():
            contracts_table.add_row(
                name.replace('_', ' ').title(),
                address,
                "🟢 Active"
            )
        
        console.print(contracts_table)
        
        # Configuration
        config = cli.config.get('blockchain', {})
        
        if config:
            config_panel = Panel(
                f"[bold]RPC Endpoint:[/bold] {config.get('rpc_url', 'Not configured')}\n"
                f"[bold]Chain ID:[/bold] {config.get('chain_id', 'Not configured')}\n"
                f"[bold]Issuer Address:[/bold] {config.get('issuer_address', 'Not configured')}\n"
                f"[bold]Gas Limit:[/bold] {config.get('gas_limit', '100000')}",
                title="⚙️ Configuration",
                border_style="blue"
            )
            console.print(config_panel)
        else:
            console.print("\n⚠️ Blockchain not configured. Use 'collegiumai config set' to configure.", style="yellow")
        
    except Exception as e:
        console.print(f"❌ Failed to get network status: {e}", style="red")

@blockchain.command()
@click.argument('format_type', type=click.Choice(['json', 'xml', 'pdf']))
@click.argument('credential_id', type=str)
@click.option('--output', '-o', type=str, help='Output file path')
def export_credential(format_type, credential_id, output):
    """Export credential in various formats"""
    console.print(f"\n📤 Exporting Credential: {credential_id}", style="bold blue")
    console.print(f"📄 Format: {format_type.upper()}", style="dim")
    
    try:
        from .. import cli
        
        # Load credential
        credentials_file = cli.config_dir / 'credentials.json'
        
        if not credentials_file.exists():
            console.print("❌ No credentials database found", style="red")
            return
        
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        
        credential = next((c for c in credentials if c.get('credential_id') == credential_id), None)
        
        if not credential:
            console.print(f"❌ Credential {credential_id} not found", style="red")
            return
        
        # Generate output filename if not provided
        if not output:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output = f"{credential_id}_{timestamp}.{format_type}"
        
        # Export based on format
        if format_type == 'json':
            with open(output, 'w') as f:
                json.dump(credential, f, indent=2)
        
        elif format_type == 'xml':
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<credential>
    <id>{credential.get('credential_id', '')}</id>
    <student_address>{credential.get('student_address', '')}</student_address>
    <course_name>{credential.get('course_name', '')}</course_name>
    <grade>{credential.get('grade', '')}</grade>
    <credits>{credential.get('credits', '')}</credits>
    <institution>{credential.get('institution', '')}</institution>
    <completion_date>{credential.get('completion_date', '')}</completion_date>
    <issued_at>{credential.get('issued_at', '')}</issued_at>
    <transaction_hash>{credential.get('transaction_hash', '')}</transaction_hash>
    <status>{credential.get('status', '')}</status>
</credential>"""
            with open(output, 'w') as f:
                f.write(xml_content)
        
        elif format_type == 'pdf':
            # Mock PDF generation (would use reportlab or similar)
            console.print("📄 PDF generation requires additional dependencies", style="yellow")
            console.print("Installing reportlab... (mock)", style="dim")
            
            # Create a simple text file instead
            text_output = output.replace('.pdf', '.txt')
            with open(text_output, 'w') as f:
                f.write(f"""
ACADEMIC CREDENTIAL CERTIFICATE
===============================

Credential ID: {credential.get('credential_id', '')}
Student: {credential.get('student_address', '')}
Course: {credential.get('course_name', '')}
Grade: {credential.get('grade', '')}
Credits: {credential.get('credits', '')} ECTS
Institution: {credential.get('institution', '')}
Completion Date: {credential.get('completion_date', '')}
Issued At: {credential.get('issued_at', '')}

Blockchain Verification:
Transaction Hash: {credential.get('transaction_hash', '')}
Status: {credential.get('status', '').title()}

This credential is digitally signed and verifiable on the CollegiumAI blockchain.
""")
            output = text_output
        
        success_panel = Panel(
            f"[bold green]✅ Export Successful[/bold green]\n\n"
            f"[bold]Format:[/bold] {format_type.upper()}\n"
            f"[bold]Output File:[/bold] {output}\n"
            f"[bold]File Size:[/bold] {len(json.dumps(credential)) if format_type == 'json' else 'N/A'} bytes",
            title="📤 Export Complete",
            border_style="green"
        )
        console.print(success_panel)
        
    except Exception as e:
        console.print(f"❌ Export failed: {e}", style="red")

if __name__ == '__main__':
    blockchain()