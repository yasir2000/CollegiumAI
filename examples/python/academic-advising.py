#!/usr/bin/env python3
"""
CollegiumAI SDK Example: Academic Advising
==========================================

This example demonstrates comprehensive academic advising scenarios using the
CollegiumAI Framework. It shows how to interact with the Academic Advisor agent
for various student personas and academic situations.

Features demonstrated:
- Course selection assistance
- Degree planning and progression tracking
- Academic policy compliance checking
- GPA impact analysis
- Multi-semester planning
- Prerequisites verification
- Graduation requirements checking
"""

import asyncio
import os
import sys
import json
from datetime import datetime, date
from typing import Dict, List, Any, Optional
import argparse
import logging

# Add the parent directory to the path to import the SDK
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk import (
    CollegiumAIClient, SDKConfig, PersonaType, GovernanceFramework,
    PersonaHelper, ResponseBuilder
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AcademicAdvisingDemo:
    """
    Comprehensive academic advising demonstration class
    """
    
    def __init__(self, config: SDKConfig):
        self.config = config
        self.client: Optional[CollegiumAIClient] = None
        self.sample_students = self._create_sample_students()
        self.sample_courses = self._create_sample_courses()
        
    async def __aenter__(self):
        self.client = CollegiumAIClient(self.config)
        await self.client.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.close()
    
    def _create_sample_students(self) -> Dict[str, Dict[str, Any]]:
        """Create sample student data for different personas"""
        return {
            'traditional_student': {
                'student_id': 'STU001',
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@university.edu',
                'persona': PersonaType.TRADITIONAL_STUDENT,
                'year': 'sophomore',
                'major': 'Computer Science',
                'minor': 'Mathematics',
                'gpa': 3.2,
                'completed_credits': 45,
                'enrolled_credits': 15,
                'academic_standing': 'good',
                'interests': ['artificial intelligence', 'web development', 'data science'],
                'career_goals': 'Software Engineer at tech company',
                'completed_courses': [
                    'CS101 - Introduction to Programming',
                    'CS102 - Data Structures',
                    'MATH151 - Calculus I',
                    'MATH152 - Calculus II',
                    'ENG101 - English Composition',
                    'HIST101 - World History'
                ]
            },
            'transfer_student': {
                'student_id': 'STU002',
                'name': 'Michael Chen',
                'email': 'michael.chen@university.edu',
                'persona': PersonaType.TRANSFER_STUDENT,
                'year': 'junior',
                'major': 'Business Administration',
                'gpa': 3.7,
                'completed_credits': 72,
                'transfer_credits': 45,
                'enrolled_credits': 12,
                'academic_standing': 'dean_list',
                'previous_institution': 'Community College of Technology',
                'interests': ['entrepreneurship', 'finance', 'international business'],
                'career_goals': 'Start own consulting business',
                'transfer_concerns': [
                    'Credit transfer evaluation',
                    'Graduation timeline',
                    'Prerequisites alignment'
                ]
            },
            'graduate_student': {
                'student_id': 'STU003',
                'name': 'Dr. Emily Rodriguez',
                'email': 'emily.rodriguez@university.edu',
                'persona': PersonaType.GRADUATE_STUDENT,
                'degree_level': 'PhD',
                'program': 'Educational Psychology',
                'year': 'third_year',
                'gpa': 3.9,
                'completed_credits': 54,
                'dissertation_stage': 'proposal_approved',
                'advisor': 'Dr. James Wilson',
                'research_area': 'AI in Educational Assessment',
                'interests': ['machine learning', 'educational technology', 'assessment design'],
                'career_goals': 'University professor and researcher',
                'research_progress': {
                    'literature_review': 'completed',
                    'methodology': 'in_progress',
                    'data_collection': 'planned',
                    'analysis': 'planned'
                }
            },
            'international_student': {
                'student_id': 'STU004',
                'name': 'Raj Patel',
                'email': 'raj.patel@university.edu',
                'persona': PersonaType.INTERNATIONAL_STUDENT,
                'year': 'freshman',
                'major': 'Engineering',
                'country_of_origin': 'India',
                'visa_status': 'F-1',
                'gpa': 3.5,
                'completed_credits': 15,
                'enrolled_credits': 18,
                'english_proficiency': 'advanced',
                'interests': ['robotics', 'renewable energy', 'sustainable technology'],
                'career_goals': 'Renewable energy engineer',
                'cultural_considerations': [
                    'Academic calendar differences',
                    'Grading system adaptation',
                    'Cultural integration'
                ],
                'visa_requirements': {
                    'minimum_credits': 12,
                    'academic_progress': 'satisfactory',
                    'program_completion': 'on_track'
                }
            }
        }
    
    def _create_sample_courses(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create sample course catalogs for different departments"""
        return {
            'computer_science': [
                {
                    'course_code': 'CS201',
                    'title': 'Advanced Programming',
                    'credits': 3,
                    'prerequisites': ['CS102'],
                    'description': 'Advanced programming concepts and software development practices',
                    'offered': ['fall', 'spring'],
                    'difficulty': 'intermediate',
                    'workload': 'heavy'
                },
                {
                    'course_code': 'CS301',
                    'title': 'Algorithms and Data Structures',
                    'credits': 3,
                    'prerequisites': ['CS201', 'MATH152'],
                    'description': 'Analysis and design of efficient algorithms and data structures',
                    'offered': ['fall', 'spring'],
                    'difficulty': 'advanced',
                    'workload': 'heavy'
                },
                {
                    'course_code': 'CS350',
                    'title': 'Artificial Intelligence',
                    'credits': 3,
                    'prerequisites': ['CS301', 'MATH251'],
                    'description': 'Introduction to AI concepts, machine learning, and neural networks',
                    'offered': ['spring'],
                    'difficulty': 'advanced',
                    'workload': 'heavy'
                },
                {
                    'course_code': 'CS280',
                    'title': 'Web Development',
                    'credits': 3,
                    'prerequisites': ['CS201'],
                    'description': 'Full-stack web development with modern frameworks',
                    'offered': ['fall', 'spring', 'summer'],
                    'difficulty': 'intermediate',
                    'workload': 'moderate'
                }
            ],
            'mathematics': [
                {
                    'course_code': 'MATH251',
                    'title': 'Linear Algebra',
                    'credits': 3,
                    'prerequisites': ['MATH152'],
                    'description': 'Vector spaces, matrices, linear transformations',
                    'offered': ['fall', 'spring'],
                    'difficulty': 'intermediate',
                    'workload': 'moderate'
                },
                {
                    'course_code': 'MATH301',
                    'title': 'Statistics and Probability',
                    'credits': 3,
                    'prerequisites': ['MATH152'],
                    'description': 'Statistical analysis and probability theory',
                    'offered': ['fall', 'spring'],
                    'difficulty': 'intermediate',
                    'workload': 'moderate'
                }
            ],
            'business': [
                {
                    'course_code': 'BUS201',
                    'title': 'Principles of Management',
                    'credits': 3,
                    'prerequisites': ['BUS101'],
                    'description': 'Fundamental management concepts and practices',
                    'offered': ['fall', 'spring'],
                    'difficulty': 'beginner',
                    'workload': 'light'
                },
                {
                    'course_code': 'BUS301',
                    'title': 'Strategic Management',
                    'credits': 3,
                    'prerequisites': ['BUS201', 'BUS220'],
                    'description': 'Strategic planning and competitive analysis',
                    'offered': ['fall', 'spring'],
                    'difficulty': 'advanced',
                    'workload': 'moderate'
                }
            ]
        }
    
    async def demonstrate_course_selection(self, student_key: str = 'traditional_student'):
        """
        Demonstrate course selection assistance for different student scenarios
        """
        print(f"\n{'='*60}")
        print("COURSE SELECTION ASSISTANCE DEMO")
        print(f"{'='*60}")
        
        student = self.sample_students[student_key]
        print(f"Student: {student['name']} ({student['persona'].value})")
        print(f"Major: {student['major']}")
        print(f"Current GPA: {student['gpa']}")
        print(f"Completed Credits: {student['completed_credits']}")
        
        advisor = self.client.agent('academic_advisor')
        
        # Course selection query
        query = f"""
        I need help selecting courses for next semester. I'm a {student['year']} {student['major']} major 
        with a {student['gpa']} GPA. I've completed {student['completed_credits']} credits so far.
        
        My interests include: {', '.join(student['interests'])}
        My career goal is: {student['career_goals']}
        
        I'm particularly interested in courses that will help me with my career goals while 
        maintaining a good balance for my GPA.
        """
        
        try:
            response = await advisor.query(
                message=query,
                context={
                    'student_profile': student,
                    'available_courses': self.sample_courses,
                    'current_semester': 'spring_2024',
                    'graduation_requirements': {
                        'total_credits': 120,
                        'major_credits': 60,
                        'core_requirements': 30,
                        'electives': 30
                    }
                },
                user_type=student['persona'],
                collaborative=True
            )
            
            self._print_agent_response(response, "Course Selection Advice")
            
        except Exception as e:
            logger.error(f"Error in course selection demo: {e}")
            print(f"❌ Error: {e}")
    
    async def demonstrate_degree_planning(self, student_key: str = 'transfer_student'):
        """
        Demonstrate comprehensive degree planning assistance
        """
        print(f"\n{'='*60}")
        print("DEGREE PLANNING ASSISTANCE DEMO")
        print(f"{'='*60}")
        
        student = self.sample_students[student_key]
        print(f"Student: {student['name']} ({student['persona'].value})")
        
        advisor = self.client.agent('academic_advisor')
        
        query = """
        I need help creating a comprehensive degree plan that accounts for my transfer credits
        and ensures I can graduate on time. I want to understand:
        
        1. How my transfer credits apply to degree requirements
        2. What courses I still need to take
        3. A semester-by-semester plan to graduation
        4. Any potential issues or bottlenecks
        5. Opportunities for accelerated completion
        """
        
        try:
            response = await advisor.query(
                message=query,
                context={
                    'student_profile': student,
                    'transfer_evaluation': {
                        'total_transfer_credits': student.get('transfer_credits', 0),
                        'applicable_credits': 42,
                        'general_education_completed': 18,
                        'major_prerequisites_completed': 15,
                        'electives_completed': 9
                    },
                    'degree_requirements': {
                        'total_credits': 120,
                        'residency_requirement': 30,  # Minimum credits at current institution
                        'major_core': 45,
                        'major_electives': 15,
                        'general_education': 30,
                        'free_electives': 30
                    },
                    'graduation_timeline': 'may_2025'
                },
                user_type=student['persona']
            )
            
            self._print_agent_response(response, "Degree Planning Advice")
            
        except Exception as e:
            logger.error(f"Error in degree planning demo: {e}")
            print(f"❌ Error: {e}")
    
    async def demonstrate_academic_recovery(self):
        """
        Demonstrate academic recovery planning for at-risk students
        """
        print(f"\n{'='*60}")
        print("ACADEMIC RECOVERY ASSISTANCE DEMO")
        print(f"{'='*60}")
        
        # Create at-risk student scenario
        at_risk_student = {
            'student_id': 'STU005',
            'name': 'Alex Thompson',
            'email': 'alex.thompson@university.edu',
            'persona': PersonaType.NON_TRADITIONAL_STUDENT,
            'year': 'junior',
            'major': 'Psychology',
            'gpa': 2.1,  # Below good standing
            'completed_credits': 75,
            'academic_standing': 'probation',
            'challenges': [
                'Work-life balance (full-time job)',
                'Family responsibilities (single parent)',
                'Financial stress',
                'Time management difficulties'
            ],
            'recent_grades': ['D+', 'C-', 'F', 'B-'],
            'support_services_used': ['tutoring', 'counseling']
        }
        
        print(f"Student: {at_risk_student['name']} ({at_risk_student['persona'].value})")
        print(f"Current GPA: {at_risk_student['gpa']} (Academic Probation)")
        print(f"Challenges: {', '.join(at_risk_student['challenges'])}")
        
        advisor = self.client.agent('academic_advisor')
        
        query = """
        I'm struggling academically and on academic probation. I need help creating a recovery plan
        that addresses my specific challenges while helping me get back to good academic standing.
        
        My main challenges are balancing work, family, and school. I need practical strategies that
        account for my limited time and resources.
        
        Can you help me with:
        1. A realistic course load for next semester
        2. Study strategies that work with my schedule
        3. Campus resources that can provide additional support
        4. A timeline for getting back to good standing
        5. Strategies to prevent future academic difficulties
        """
        
        try:
            response = await advisor.query(
                message=query,
                context={
                    'student_profile': at_risk_student,
                    'academic_policies': {
                        'probation_requirements': {
                            'minimum_semester_gpa': 2.5,
                            'maximum_courses': 12,  # Credit hour limit
                            'mandatory_advising': True,
                            'progress_monitoring': 'bi_weekly'
                        },
                        'dismissal_threshold': 2.0,
                        'recovery_timeline': '2_semesters'
                    },
                    'support_services': [
                        'Academic Success Center',
                        'Tutoring Services',
                        'Financial Aid Counseling',
                        'Student Parent Support Group',
                        'Career Counseling',
                        'Mental Health Services'
                    ]
                },
                user_type=at_risk_student['persona'],
                collaborative=True
            )
            
            self._print_agent_response(response, "Academic Recovery Plan")
            
        except Exception as e:
            logger.error(f"Error in academic recovery demo: {e}")
            print(f"❌ Error: {e}")
    
    async def demonstrate_graduate_research_planning(self):
        """
        Demonstrate graduate research and dissertation planning
        """
        print(f"\n{'='*60}")
        print("GRADUATE RESEARCH PLANNING DEMO")
        print(f"{'='*60}")
        
        grad_student = self.sample_students['graduate_student']
        print(f"Student: {grad_student['name']} ({grad_student['persona'].value})")
        print(f"Program: {grad_student['program']}")
        print(f"Research Area: {grad_student['research_area']}")
        print(f"Dissertation Stage: {grad_student['dissertation_stage']}")
        
        advisor = self.client.agent('academic_advisor')
        
        query = """
        I'm a PhD student in Educational Psychology working on AI applications in educational assessment.
        My dissertation proposal has been approved, and I need guidance on:
        
        1. Planning my research methodology and data collection
        2. Selecting appropriate courses to support my research
        3. Timeline management for dissertation completion
        4. Preparing for comprehensive exams
        5. Building my academic portfolio for future faculty positions
        6. Balancing research, coursework, and teaching responsibilities
        """
        
        try:
            response = await advisor.query(
                message=query,
                context={
                    'student_profile': grad_student,
                    'program_requirements': {
                        'total_credits': 72,
                        'coursework_credits': 42,
                        'dissertation_credits': 30,
                        'comprehensive_exam': 'third_year',
                        'dissertation_defense': 'fifth_year',
                        'teaching_requirement': 'two_semesters'
                    },
                    'research_resources': [
                        'Statistical Analysis Software',
                        'Research Participant Pool',
                        'Grant Funding Opportunities',
                        'Conference Presentation Opportunities',
                        'Publication Support',
                        'Research Ethics Board'
                    ],
                    'career_preparation': {
                        'academic_job_market': 'competitive',
                        'preparation_timeline': '18_months',
                        'required_portfolio': [
                            'dissertation',
                            'publications',
                            'teaching_portfolio',
                            'research_statement',
                            'conference_presentations'
                        ]
                    }
                },
                user_type=grad_student['persona']
            )
            
            self._print_agent_response(response, "Graduate Research Planning")
            
        except Exception as e:
            logger.error(f"Error in graduate research planning demo: {e}")
            print(f"❌ Error: {e}")
    
    async def demonstrate_international_student_advising(self):
        """
        Demonstrate specialized advising for international students
        """
        print(f"\n{'='*60}")
        print("INTERNATIONAL STUDENT ADVISING DEMO")
        print(f"{'='*60}")
        
        intl_student = self.sample_students['international_student']
        print(f"Student: {intl_student['name']} ({intl_student['persona'].value})")
        print(f"Country: {intl_student['country_of_origin']}")
        print(f"Visa Status: {intl_student['visa_status']}")
        
        advisor = self.client.agent('academic_advisor')
        
        query = """
        As an international student on an F-1 visa, I need guidance on academic planning that
        ensures I maintain my visa status while succeeding academically. I need help with:
        
        1. Understanding minimum credit hour requirements for visa compliance
        2. Academic calendar and cultural differences in education systems
        3. Course selection that balances difficulty with success
        4. Opportunities for practical training (CPT/OPT) in my field
        5. Building connections for future career opportunities
        6. Resources for academic and cultural adjustment
        """
        
        try:
            response = await advisor.query(
                message=query,
                context={
                    'student_profile': intl_student,
                    'visa_requirements': intl_student['visa_requirements'],
                    'international_services': [
                        'International Student Orientation',
                        'Visa Compliance Workshops',
                        'Cultural Adjustment Programs',
                        'English Language Support',
                        'International Student Association',
                        'Career Services for International Students'
                    ],
                    'practical_training': {
                        'cpt_eligibility': 'after_one_year',
                        'opt_eligibility': 'after_degree_completion',
                        'stem_extension': 'available',
                        'work_authorization_process': 'requires_advance_planning'
                    },
                    'cultural_considerations': intl_student['cultural_considerations']
                },
                user_type=intl_student['persona']
            )
            
            self._print_agent_response(response, "International Student Advising")
            
        except Exception as e:
            logger.error(f"Error in international student advising demo: {e}")
            print(f"❌ Error: {e}")
    
    async def demonstrate_collaborative_advising(self):
        """
        Demonstrate multi-agent collaboration between advisor and student services
        """
        print(f"\n{'='*60}")
        print("COLLABORATIVE ADVISING DEMO")
        print(f"{'='*60}")
        
        student = self.sample_students['traditional_student']
        print(f"Student: {student['name']} needs comprehensive support")
        print("Collaborating Agents: Academic Advisor + Student Services")
        
        # Get both agents
        advisor = self.client.agent('academic_advisor')
        student_services = self.client.agent('student_services')
        
        # Complex scenario requiring both academic and support services
        complex_query = """
        I'm struggling with both academic performance and personal challenges. My GPA has dropped
        from 3.2 to 2.8 this semester, and I'm feeling overwhelmed. I think I need both academic
        support and personal counseling, but I'm not sure how to coordinate everything.
        
        Academic concerns:
        - Difficulty with advanced math courses
        - Time management issues
        - Study skills need improvement
        
        Personal concerns:
        - Anxiety about academic performance
        - Financial stress from part-time work
        - Relationship issues affecting focus
        
        Can you help me create a comprehensive plan that addresses both my academic and personal needs?
        """
        
        try:
            # First, get academic advisor perspective
            print("\n🎓 Academic Advisor Analysis:")
            academic_response = await advisor.query(
                message=complex_query,
                context={
                    'student_profile': student,
                    'recent_performance': {
                        'current_gpa': 2.8,
                        'previous_gpa': 3.2,
                        'struggling_courses': ['MATH251', 'CS301'],
                        'successful_courses': ['ENG201', 'HIST220']
                    }
                },
                user_type=student['persona'],
                collaborative=True
            )
            
            self._print_agent_response(academic_response, "Academic Perspective")
            
            # Then get student services perspective
            print("\n🏥 Student Services Analysis:")
            services_response = await student_services.query(
                message=complex_query,
                context={
                    'student_profile': student,
                    'academic_context': academic_response.get('context', {}),
                    'support_needs': [
                        'academic_support',
                        'mental_health',
                        'financial_counseling',
                        'time_management'
                    ]
                },
                user_type=student['persona'],
                collaborative=True
            )
            
            self._print_agent_response(services_response, "Student Services Perspective")
            
            # Create integrated plan
            print("\n🤝 Integrated Support Plan:")
            print("Academic Advisor + Student Services have collaborated to create a comprehensive plan.")
            
        except Exception as e:
            logger.error(f"Error in collaborative advising demo: {e}")
            print(f"❌ Error: {e}")
    
    def _print_agent_response(self, response: Dict[str, Any], title: str):
        """Helper method to format and print agent responses"""
        print(f"\n📋 {title}")
        print("-" * 50)
        
        if response.get('success'):
            # Print thinking process
            if response.get('thoughts'):
                print("🧠 Agent Reasoning:")
                for i, thought in enumerate(response['thoughts'][-2:], 1):  # Show last 2 thoughts
                    print(f"  {i}. {thought.get('observation', 'N/A')}")
                    print(f"     Reasoning: {thought.get('reasoning', 'N/A')}")
                    print(f"     Action Plan: {thought.get('actionPlan', 'N/A')}")
                    print()
            
            # Print final response
            print("💡 Recommendation:")
            print(response.get('finalResponse', 'No response available'))
            
            # Print confidence level
            confidence = response.get('confidence', 0)
            confidence_emoji = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.6 else "🔴"
            print(f"\n{confidence_emoji} Confidence: {confidence:.1%}")
            
            # Print collaborating agents if any
            if response.get('collaboratingAgents'):
                print(f"🤝 Collaborating Agents: {', '.join(response['collaboratingAgents'])}")
            
            # Print additional recommendations
            if response.get('recommendations'):
                print("\n📌 Additional Recommendations:")
                for rec in response['recommendations']:
                    print(f"  • {rec}")
        else:
            print("❌ Error in agent response")
            print(response.get('error', 'Unknown error'))
    
    async def run_all_demos(self):
        """Run all demonstration scenarios"""
        print("🎓 CollegiumAI Academic Advising SDK Demo")
        print("=" * 60)
        
        try:
            # Check system health first
            health = await self.client.health_check()
            print(f"✅ System Health: {health.get('status', 'Unknown')}")
            
            # Run all demonstration scenarios
            await self.demonstrate_course_selection('traditional_student')
            await self.demonstrate_degree_planning('transfer_student')
            await self.demonstrate_academic_recovery()
            await self.demonstrate_graduate_research_planning()
            await self.demonstrate_international_student_advising()
            await self.demonstrate_collaborative_advising()
            
            print(f"\n{'='*60}")
            print("🎉 All Academic Advising Demos Completed Successfully!")
            print("="*60)
            
        except Exception as e:
            logger.error(f"Error running demos: {e}")
            print(f"❌ Demo failed: {e}")

async def main():
    """Main function to run the academic advising examples"""
    parser = argparse.ArgumentParser(description='CollegiumAI Academic Advising SDK Examples')
    parser.add_argument('--api-key', help='API key for CollegiumAI')
    parser.add_argument('--base-url', default='http://localhost:4000/api/v1', help='Base URL for API')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--demo', choices=[
        'course-selection', 'degree-planning', 'academic-recovery', 
        'graduate-research', 'international-student', 'collaborative', 'all'
    ], default='all', help='Specific demo to run')
    
    args = parser.parse_args()
    
    # Get API key from environment or command line
    api_key = args.api_key or os.getenv('COLLEGIUMAI_API_KEY')
    if not api_key:
        print("❌ Error: API key required. Set COLLEGIUMAI_API_KEY environment variable or use --api-key")
        return
    
    # Create SDK configuration
    config = SDKConfig(
        api_base_url=args.base_url,
        api_key=api_key,
        debug=args.debug,
        timeout=60  # Longer timeout for complex queries
    )
    
    # Run the demonstration
    async with AcademicAdvisingDemo(config) as demo:
        if args.demo == 'all':
            await demo.run_all_demos()
        elif args.demo == 'course-selection':
            await demo.demonstrate_course_selection()
        elif args.demo == 'degree-planning':
            await demo.demonstrate_degree_planning()
        elif args.demo == 'academic-recovery':
            await demo.demonstrate_academic_recovery()
        elif args.demo == 'graduate-research':
            await demo.demonstrate_graduate_research_planning()
        elif args.demo == 'international-student':
            await demo.demonstrate_international_student_advising()
        elif args.demo == 'collaborative':
            await demo.demonstrate_collaborative_advising()

if __name__ == "__main__":
    asyncio.run(main())