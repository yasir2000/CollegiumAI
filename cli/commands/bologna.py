"""
Bologna Command Module
=====================

CLI commands for Bologna Process compliance, ECTS management,
mobility planning, and European Higher Education Area operations.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.text import Text

console = Console()

@click.group()
def bologna():
    """Bologna Process and ECTS management commands"""
    pass

@bologna.command()
@click.argument('student_id', type=str)
@click.option('--semester', '-s', type=str, help='Semester (e.g., 2024/1)')
@click.option('--institution', '-i', type=str, help='Institution name')
def calculate_ects(student_id, semester, institution):
    """Calculate ECTS credits for a student"""
    asyncio.run(_calculate_ects(student_id, semester, institution))

async def _calculate_ects(student_id: str, semester: str, institution: str):
    """Internal async function for ECTS calculation"""
    from .. import cli
    
    console.print(f"\n🇪🇺 ECTS Credit Calculation", style="bold blue")
    console.print(f"👤 Student ID: {student_id}", style="dim")
    console.print(f"📅 Semester: {semester or 'Current'}", style="dim")
    console.print(f"🏛️ Institution: {institution or 'CollegiumAI University'}", style="dim")
    
    try:
        await cli.initialize_framework()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Calculating ECTS credits...", total=None)
            
            # Mock ECTS calculation (replace with actual database queries)
            await asyncio.sleep(1.5)
            
            # Sample student course data
            courses = [
                {'course_code': 'CS101', 'name': 'Introduction to Computer Science', 'ects': 6, 'grade': 'B+', 'status': 'completed'},
                {'course_code': 'MATH201', 'name': 'Advanced Mathematics', 'ects': 8, 'grade': 'A-', 'status': 'completed'},
                {'course_code': 'ENG102', 'name': 'Academic English', 'ects': 4, 'grade': 'A', 'status': 'completed'},
                {'course_code': 'PHIL150', 'name': 'Ethics in Technology', 'ects': 5, 'grade': 'B', 'status': 'completed'},
                {'course_code': 'CS202', 'name': 'Data Structures', 'ects': 7, 'grade': 'A-', 'status': 'in_progress'},
                {'course_code': 'ECON101', 'name': 'Introduction to Economics', 'ects': 6, 'grade': None, 'status': 'enrolled'}
            ]
            
            progress.update(task, description="ECTS calculation completed")
        
        # Calculate totals
        completed_ects = sum(course['ects'] for course in courses if course['status'] == 'completed')
        in_progress_ects = sum(course['ects'] for course in courses if course['status'] == 'in_progress')
        total_enrolled_ects = sum(course['ects'] for course in courses)
        
        # Calculate GPA equivalent
        grade_points = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3}
        completed_courses = [c for c in courses if c['status'] == 'completed' and c['grade']]
        
        if completed_courses:
            weighted_points = sum(grade_points.get(c['grade'], 0) * c['ects'] for c in completed_courses)
            gpa = weighted_points / completed_ects if completed_ects > 0 else 0
        else:
            gpa = 0
        
        # Display summary
        summary_panel = Panel(
            f"[bold]Student ID:[/bold] {student_id}\n"
            f"[bold]Completed ECTS:[/bold] {completed_ects} credits\n"
            f"[bold]In Progress:[/bold] {in_progress_ects} credits\n"
            f"[bold]Total Enrolled:[/bold] {total_enrolled_ects} credits\n"
            f"[bold]GPA Equivalent:[/bold] {gpa:.2f}/4.0\n"
            f"[bold]Academic Year Progress:[/bold] {completed_ects/60*100:.1f}% (assuming 60 ECTS/year)",
            title="📊 ECTS Credit Summary",
            border_style="green"
        )
        console.print(summary_panel)
        
        # Course details table
        console.print("\n📚 Course Details:", style="bold green")
        
        courses_table = Table(show_header=True, header_style="bold blue")
        courses_table.add_column("Course Code", style="bold")
        courses_table.add_column("Course Name", max_width=30)
        courses_table.add_column("ECTS", justify="center")
        courses_table.add_column("Grade", justify="center")
        courses_table.add_column("Status")
        
        for course in courses:
            status_color = {
                'completed': 'green',
                'in_progress': 'yellow',
                'enrolled': 'blue'
            }.get(course['status'], 'dim')
            
            courses_table.add_row(
                course['course_code'],
                course['name'],
                str(course['ects']),
                course['grade'] or '-',
                f"[{status_color}]{course['status'].replace('_', ' ').title()}[/{status_color}]"
            )
        
        console.print(courses_table)
        
        # Bologna Process compliance
        bologna_compliance = _check_bologna_compliance(completed_ects, total_enrolled_ects, gpa)
        
        compliance_panel = Panel(
            f"[bold]ECTS Range Compliance:[/bold] {bologna_compliance['ects_compliance']}\n"
            f"[bold]Grade Scale Alignment:[/bold] {bologna_compliance['grade_compliance']}\n"
            f"[bold]Recognition Status:[/bold] {bologna_compliance['recognition_status']}\n"
            f"[bold]Mobility Eligible:[/bold] {bologna_compliance['mobility_eligible']}",
            title="🇪🇺 Bologna Process Compliance",
            border_style="blue"
        )
        console.print(compliance_panel)
        
    except Exception as e:
        console.print(f"❌ ECTS calculation failed: {e}", style="red")

def _check_bologna_compliance(completed_ects: int, total_ects: int, gpa: float) -> Dict[str, str]:
    """Check Bologna Process compliance"""
    return {
        'ects_compliance': '✅ Compliant' if 25 <= total_ects <= 30 else '⚠️ Review Needed',
        'grade_compliance': '✅ ECTS Grade Scale' if gpa > 0 else '⏳ Pending',
        'recognition_status': '✅ Recognizable' if completed_ects >= 15 else '⚠️ Minimum Not Met',
        'mobility_eligible': '✅ Eligible' if completed_ects >= 30 and gpa >= 2.0 else '❌ Not Eligible'
    }

@bologna.command()
@click.argument('student_id', type=str)
@click.option('--destination', '-d', type=str, required=True, help='Destination country/institution')
@click.option('--duration', type=click.Choice(['semester', 'academic_year']), 
              default='semester', help='Mobility duration')
@click.option('--program', '-p', type=str, help='Exchange program name')
def plan_mobility(student_id, destination, duration, program):
    """Plan student mobility within Bologna Process"""
    console.print(f"\n🌍 Bologna Process Mobility Planning", style="bold blue")
    console.print(f"👤 Student: {student_id}", style="dim")
    console.print(f"🎯 Destination: {destination}", style="dim")
    console.print(f"📅 Duration: {duration.replace('_', ' ').title()}", style="dim")
    
    try:
        # Mock mobility planning data
        mobility_data = {
            'student_id': student_id,
            'destination': destination,
            'duration': duration,
            'program': program or 'Erasmus+',
            'planning_date': datetime.now().isoformat(),
            'status': 'planning',
            'requirements': _get_mobility_requirements(destination, duration),
            'recommended_courses': _get_recommended_courses(destination),
            'learning_agreement': {
                'home_courses': ['CS301', 'MATH301', 'ENG201'],
                'host_courses': ['INF301', 'MAT301', 'ANG201'],
                'ects_total': 30 if duration == 'academic_year' else 15
            }
        }
        
        # Display mobility plan
        plan_panel = Panel(
            f"[bold]Program:[/bold] {mobility_data['program']}\n"
            f"[bold]Destination:[/bold] {destination}\n" 
            f"[bold]Duration:[/bold] {duration.replace('_', ' ').title()}\n"
            f"[bold]Expected ECTS:[/bold] {mobility_data['learning_agreement']['ects_total']}\n"
            f"[bold]Status:[/bold] Planning Phase\n"
            f"[bold]Planning Date:[/bold] {mobility_data['planning_date'][:10]}",
            title="🌍 Mobility Plan Overview",
            border_style="blue"
        )
        console.print(plan_panel)
        
        # Requirements checklist
        console.print("\n📋 Mobility Requirements:", style="bold green")
        
        req_table = Table(show_header=True, header_style="bold blue")
        req_table.add_column("Requirement", style="bold", ratio=3)
        req_table.add_column("Status", justify="center", ratio=1)
        req_table.add_column("Due Date", ratio=1)
        
        for req in mobility_data['requirements']:
            req_table.add_row(
                req['description'],
                req['status'],
                req['due_date']
            )
        
        console.print(req_table)
        
        # Learning Agreement
        console.print("\n📄 Proposed Learning Agreement:", style="bold green")
        
        la_table = Table(show_header=True, header_style="bold blue")
        la_table.add_column("Home Institution", style="bold")
        la_table.add_column("Host Institution", style="bold")
        la_table.add_column("ECTS")
        
        home_courses = mobility_data['learning_agreement']['home_courses']
        host_courses = mobility_data['learning_agreement']['host_courses']
        
        for i in range(max(len(home_courses), len(host_courses))):
            home = home_courses[i] if i < len(home_courses) else '-'
            host = host_courses[i] if i < len(host_courses) else '-'
            ects = '5' if home != '-' and host != '-' else '-'
            
            la_table.add_row(home, host, ects)
        
        console.print(la_table)
        
        # Next steps
        next_steps_panel = Panel(
            "1. Complete language proficiency assessment\n"
            "2. Submit mobility application by deadline\n"
            "3. Finalize Learning Agreement with host institution\n"
            "4. Arrange accommodation and visa (if required)\n"
            "5. Complete pre-departure orientation",
            title="📝 Next Steps",
            border_style="yellow"
        )
        console.print(next_steps_panel)
        
        # Save mobility plan
        from .. import cli
        mobility_file = cli.config_dir / 'mobility_plans.json'
        
        try:
            if mobility_file.exists():
                with open(mobility_file, 'r') as f:
                    plans = json.load(f)
            else:
                plans = []
            
            plans.append(mobility_data)
            
            with open(mobility_file, 'w') as f:
                json.dump(plans, f, indent=2)
            
            console.print(f"\n💾 Mobility plan saved for student {student_id}", style="green")
            
        except Exception as e:
            console.print(f"⚠️ Warning: Could not save mobility plan: {e}", style="yellow")
        
    except Exception as e:
        console.print(f"❌ Mobility planning failed: {e}", style="red")

def _get_mobility_requirements(destination: str, duration: str) -> List[Dict[str, str]]:
    """Get mobility requirements based on destination and duration"""
    base_requirements = [
        {
            'description': 'Language proficiency certificate',
            'status': '⏳ Pending',
            'due_date': '2024-03-15'
        },
        {
            'description': 'Academic transcript submission',
            'status': '✅ Complete',
            'due_date': '2024-02-01'
        },
        {
            'description': 'Learning Agreement draft',
            'status': '🔄 In Progress',
            'due_date': '2024-03-01'
        },
        {
            'description': 'Mobility application form',
            'status': '⏳ Pending',
            'due_date': '2024-02-15'
        }
    ]
    
    # Add duration-specific requirements
    if duration == 'academic_year':
        base_requirements.extend([
            {
                'description': 'Visa application (if required)',
                'status': '⏳ Pending',
                'due_date': '2024-04-01'
            },
            {
                'description': 'Accommodation arrangement',
                'status': '⏳ Pending',
                'due_date': '2024-05-01'
            }
        ])
    
    return base_requirements

def _get_recommended_courses(destination: str) -> List[Dict[str, str]]:
    """Get recommended courses for destination"""
    # Mock course recommendations
    return [
        {'code': 'INF301', 'name': 'Advanced Programming', 'ects': 6},
        {'code': 'MAT301', 'name': 'Linear Algebra', 'ects': 5},
        {'code': 'ANG201', 'name': 'Academic English', 'ects': 4}
    ]

@bologna.command()
@click.argument('qualification', type=str)
@click.option('--source-country', '-s', type=str, required=True, help='Source country/institution')
@click.option('--target-country', '-t', type=str, required=True, help='Target country/institution')
@click.option('--level', type=click.Choice(['bachelor', 'master', 'doctorate']), help='Qualification level')
def recognize_qualification(qualification, source_country, target_country, level):
    """Process automatic recognition of qualifications"""
    asyncio.run(_recognize_qualification(qualification, source_country, target_country, level))

async def _recognize_qualification(qualification: str, source_country: str, target_country: str, level: str):
    """Internal async function for qualification recognition"""
    console.print(f"\n🎓 Automatic Recognition of Qualifications", style="bold blue")
    console.print(f"📜 Qualification: {qualification}", style="dim")
    console.print(f"🌍 From: {source_country} → To: {target_country}", style="dim")
    
    try:
        # Mock recognition process
        recognition_data = {
            'qualification': qualification,
            'source_country': source_country,
            'target_country': target_country,
            'level': level or 'bachelor',
            'recognition_date': datetime.now().isoformat(),
            'status': 'processing',
            'recognition_type': _determine_recognition_type(source_country, target_country),
            'requirements': _get_recognition_requirements(source_country, target_country),
            'equivalency': _calculate_equivalency(qualification, level or 'bachelor')
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing recognition...", total=None)
            
            # Simulate processing
            await asyncio.sleep(2)
            
            # Determine recognition outcome
            if recognition_data['recognition_type'] == 'automatic':
                recognition_data['status'] = 'recognized'
                recognition_data['outcome'] = 'Full Recognition'
            elif recognition_data['recognition_type'] == 'conditional':
                recognition_data['status'] = 'conditional'
                recognition_data['outcome'] = 'Conditional Recognition'
            else:
                recognition_data['status'] = 'manual_review'
                recognition_data['outcome'] = 'Manual Review Required'
            
            progress.update(task, description="Recognition processing completed")
        
        # Display recognition results
        status_color = {
            'recognized': 'green',
            'conditional': 'yellow',
            'manual_review': 'blue'
        }.get(recognition_data['status'], 'red')
        
        recognition_panel = Panel(
            f"[bold]Qualification:[/bold] {qualification}\n"
            f"[bold]Level:[/bold] {recognition_data['level'].title()}\n"
            f"[bold]Recognition Type:[/bold] {recognition_data['recognition_type'].title()}\n"
            f"[bold]Status:[/bold] [{status_color}]{recognition_data['outcome']}[/{status_color}]\n"
            f"[bold]Processing Date:[/bold] {recognition_data['recognition_date'][:10]}\n"
            f"[bold]Reference ID:[/bold] ARQ_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title="🎓 Recognition Results",
            border_style=status_color
        )
        console.print(recognition_panel)
        
        # Equivalency details
        if recognition_data['equivalency']:
            console.print("\n🔄 Qualification Equivalency:", style="bold green")
            
            equiv_table = Table(show_header=True, header_style="bold blue")
            equiv_table.add_column("Component", style="bold")
            equiv_table.add_column("Source", style="dim")
            equiv_table.add_column("Target Equivalent")
            equiv_table.add_column("ECTS Credits", justify="center")
            
            for equiv in recognition_data['equivalency']:
                equiv_table.add_row(
                    equiv['component'],
                    equiv['source_value'],
                    equiv['target_value'],
                    str(equiv['ects'])
                )
            
            console.print(equiv_table)
        
        # Additional requirements (if any)
        if recognition_data['requirements']:
            console.print("\n📋 Additional Requirements:", style="bold yellow")
            
            for i, req in enumerate(recognition_data['requirements'], 1):
                console.print(f"  {i}. {req}")
        
        # Next steps based on status
        if recognition_data['status'] == 'recognized':
            console.print("\n✅ Your qualification is fully recognized!", style="bold green")
            console.print("No additional steps required for academic recognition.", style="dim")
        elif recognition_data['status'] == 'conditional':
            console.print("\n⚠️ Conditional recognition granted", style="bold yellow")
            console.print("Please complete the additional requirements listed above.", style="dim")
        else:
            console.print("\n🔍 Manual review required", style="bold blue")
            console.print("Your application will be reviewed by recognition experts.", style="dim")
        
    except Exception as e:
        console.print(f"❌ Recognition processing failed: {e}", style="red")

def _determine_recognition_type(source: str, target: str) -> str:
    """Determine type of recognition process"""
    # Mock recognition type determination
    eu_countries = ['germany', 'france', 'spain', 'italy', 'netherlands', 'belgium']
    
    source_lower = source.lower()
    target_lower = target.lower()
    
    if source_lower in eu_countries and target_lower in eu_countries:
        return 'automatic'
    elif 'uk' in source_lower or 'uk' in target_lower:
        return 'conditional'
    else:
        return 'manual_review'

def _get_recognition_requirements(source: str, target: str) -> List[str]:
    """Get additional requirements for recognition"""
    requirements = []
    
    if 'uk' in source.lower() or 'uk' in target.lower():
        requirements.extend([
            'NARIC statement of comparability',
            'English language proficiency certificate'
        ])
    
    if any(country in target.lower() for country in ['germany', 'austria']):
        requirements.append('Apostille certification of documents')
    
    return requirements

def _calculate_equivalency(qualification: str, level: str) -> List[Dict[str, Any]]:
    """Calculate qualification equivalency"""
    # Mock equivalency calculation
    return [
        {
            'component': 'Overall Qualification',
            'source_value': qualification,
            'target_value': f'Recognized {level.title()} Degree',
            'ects': 180 if level == 'bachelor' else 120
        },
        {
            'component': 'Academic Level', 
            'source_value': level.title(),
            'target_value': f'EQF Level {6 if level == "bachelor" else 7}',
            'ects': 0
        }
    ]

@bologna.command()
def quality_framework():
    """Display Bologna Process quality assurance framework"""
    console.print("\n🇪🇺 Bologna Process Quality Assurance Framework", style="bold blue")
    
    # ESG Standards (European Standards and Guidelines)
    esg_tree = Tree("📊 ESG Standards")
    
    # Part 1: Standards for internal quality assurance
    part1 = esg_tree.add("Part 1: Internal Quality Assurance")
    part1.add("1.1 Policy for quality assurance")
    part1.add("1.2 Design and approval of programmes") 
    part1.add("1.3 Student-centred learning, teaching and assessment")
    part1.add("1.4 Student admission, progression, recognition and certification")
    part1.add("1.5 Teaching staff")
    part1.add("1.6 Learning resources and student support")
    part1.add("1.7 Information management")
    part1.add("1.8 Public information")
    part1.add("1.9 On-going monitoring and periodic review of programmes")
    part1.add("1.10 Cyclical external quality assurance")
    
    # Part 2: Standards for external quality assurance
    part2 = esg_tree.add("Part 2: External Quality Assurance")
    part2.add("2.1 Consideration of internal quality assurance")
    part2.add("2.2 Designing methodologies fit for purpose")
    part2.add("2.3 Implementing processes")
    part2.add("2.4 Peer-review experts")
    part2.add("2.5 Criteria for outcomes")
    part2.add("2.6 Reporting")
    part2.add("2.7 Complaints and appeals")
    
    # Part 3: Standards for quality assurance agencies
    part3 = esg_tree.add("Part 3: Quality Assurance Agencies")
    part3.add("3.1 Activities, policy and processes for quality assurance")
    part3.add("3.2 Official status")
    part3.add("3.3 Independence")
    part3.add("3.4 Thematic analysis")
    part3.add("3.5 Resources")
    part3.add("3.6 Internal quality assurance and professional conduct")
    part3.add("3.7 Cyclical external review of agencies")
    
    console.print(esg_tree)
    
    # Key principles
    principles_panel = Panel(
        "• **Student-Centred Learning:** Focus on student needs and learning outcomes\n"
        "• **Stakeholder Involvement:** Engagement of students, employers, and society\n"
        "• **Transparency:** Clear and accessible information about quality processes\n"
        "• **Continuous Improvement:** Regular monitoring and enhancement of quality\n"
        "• **International Cooperation:** Collaboration across European higher education\n"
        "• **Recognition:** Automatic recognition of qualifications and study periods",
        title="🎯 Bologna Process Principles",
        border_style="blue"
    )
    console.print(principles_panel)
    
    # Implementation status
    console.print("\n📈 CollegiumAI Implementation Status:", style="bold green")
    
    implementation_table = Table(show_header=True, header_style="bold blue")
    implementation_table.add_column("ESG Standard", style="bold")
    implementation_table.add_column("Status", justify="center")
    implementation_table.add_column("Implementation Level", justify="center")
    implementation_table.add_column("Last Review")
    
    standards_status = [
        ("1.1 Quality Assurance Policy", "✅ Implemented", "Full", "2023-12-01"),
        ("1.2 Programme Design", "✅ Implemented", "Full", "2023-11-15"),
        ("1.3 Student-Centred Learning", "🔄 In Progress", "Partial", "2024-01-10"),
        ("1.4 Recognition Procedures", "✅ Implemented", "Full", "2023-10-20"),
        ("1.8 Public Information", "✅ Implemented", "Full", "2023-12-15"),
        ("2.1 Internal QA Consideration", "🔄 In Progress", "Partial", "2024-01-05"),
        ("3.1 QA Activities", "⏳ Planned", "Planning", "N/A")
    ]
    
    for standard, status, level, review in standards_status:
        implementation_table.add_row(standard, status, level, review)
    
    console.print(implementation_table)

@bologna.command()
@click.option('--country', '-c', multiple=True, help='Filter by country')
@click.option('--program-type', '-p', type=click.Choice(['bachelor', 'master', 'doctorate']), 
              help='Filter by program type')
def mobility_opportunities(country, program_type):
    """List available mobility opportunities"""
    console.print("\n🌍 Bologna Process Mobility Opportunities", style="bold blue")
    
    # Sample mobility opportunities
    opportunities = [
        {
            'program': 'Erasmus+',
            'country': 'Germany',
            'institution': 'Technical University of Munich',
            'type': 'bachelor',
            'duration': 'semester',
            'language': 'English/German',
            'ects': 30,
            'deadline': '2024-03-15',
            'status': 'Open'
        },
        {
            'program': 'Erasmus+',
            'country': 'France', 
            'institution': 'Sorbonne University',
            'type': 'master',
            'duration': 'academic_year',
            'language': 'French/English',
            'ects': 60,
            'deadline': '2024-02-28',
            'status': 'Open'
        },
        {
            'program': 'Swiss-European Exchange',
            'country': 'Switzerland',
            'institution': 'ETH Zurich',
            'type': 'bachelor',
            'duration': 'semester',
            'language': 'English',
            'ects': 30,
            'deadline': '2024-04-01',
            'status': 'Open'
        },
        {
            'program': 'Nordic Exchange',
            'country': 'Sweden',
            'institution': 'KTH Royal Institute',
            'type': 'master',
            'duration': 'semester',
            'language': 'English',
            'ects': 30,
            'deadline': '2024-03-31',
            'status': 'Limited'
        },
        {
            'program': 'Erasmus+',
            'country': 'Spain',
            'institution': 'University of Barcelona',
            'type': 'bachelor',
            'duration': 'semester',
            'language': 'Spanish/English',
            'ects': 30,
            'deadline': '2024-02-15',
            'status': 'Closed'
        }
    ]
    
    # Apply filters
    filtered_opportunities = opportunities
    
    if country:
        filtered_opportunities = [op for op in filtered_opportunities 
                                 if any(c.lower() in op['country'].lower() for c in country)]
    
    if program_type:
        filtered_opportunities = [op for op in filtered_opportunities 
                                 if op['type'] == program_type]
    
    # Display opportunities
    opportunities_table = Table(show_header=True, header_style="bold blue")
    opportunities_table.add_column("Program", style="bold")
    opportunities_table.add_column("Country/Institution", max_width=25)
    opportunities_table.add_column("Type", justify="center")
    opportunities_table.add_column("Duration", justify="center")
    opportunities_table.add_column("ECTS", justify="center")
    opportunities_table.add_column("Language")
    opportunities_table.add_column("Deadline")
    opportunities_table.add_column("Status")
    
    for op in filtered_opportunities:
        status_color = {
            'Open': 'green',
            'Limited': 'yellow',
            'Closed': 'red'
        }.get(op['status'], 'dim')
        
        opportunities_table.add_row(
            op['program'],
            f"{op['country']}\n{op['institution']}",
            op['type'].title(),
            op['duration'].replace('_', ' ').title(),
            str(op['ects']),
            op['language'],
            op['deadline'],
            f"[{status_color}]{op['status']}[/{status_color}]"
        )
    
    console.print(opportunities_table)
    
    # Summary
    open_count = sum(1 for op in filtered_opportunities if op['status'] == 'Open')
    total_count = len(filtered_opportunities)
    
    summary_panel = Panel(
        f"[bold]Total Opportunities:[/bold] {total_count}\n"
        f"[bold]Currently Open:[/bold] {open_count}\n"
        f"[bold]Countries Available:[/bold] {len(set(op['country'] for op in filtered_opportunities))}\n"
        f"[bold]Average ECTS:[/bold] {sum(op['ects'] for op in filtered_opportunities) / total_count:.1f}" if total_count > 0 else "[bold]No opportunities found[/bold]",
        title="📊 Mobility Summary",
        border_style="blue"
    )
    console.print(summary_panel)

if __name__ == '__main__':
    bologna()