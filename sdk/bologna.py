"""
Bologna Process Client for CollegiumAI SDK
Handles European higher education compliance and standards
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime, date
from enum import Enum

class QualificationLevel(Enum):
    """European Qualifications Framework levels"""
    EQF_1 = "eqf_1"  # Basic knowledge and skills
    EQF_2 = "eqf_2"  # Basic factual knowledge
    EQF_3 = "eqf_3"  # Knowledge of facts, principles
    EQF_4 = "eqf_4"  # Factual and theoretical knowledge
    EQF_5 = "eqf_5"  # Comprehensive knowledge
    EQF_6 = "eqf_6"  # Advanced knowledge (Bachelor)
    EQF_7 = "eqf_7"  # Highly specialized knowledge (Master)
    EQF_8 = "eqf_8"  # Most advanced knowledge (PhD)

class QualificationFramework(Enum):
    """Quality assurance frameworks"""
    ECTS = "ects"  # European Credit Transfer System
    QAA = "qaa"    # Quality Assurance Agency
    AACSB = "aacsb"  # Association to Advance Collegiate Schools of Business
    EQUIS = "equis"  # European Quality Improvement System
    AMBA = "amba"   # Association of MBAs
    ENQA = "enqa"   # European Association for Quality Assurance

class MobilityType(Enum):
    """Types of student mobility"""
    ERASMUS = "erasmus"
    EXCHANGE = "exchange"
    DOUBLE_DEGREE = "double_degree"
    JOINT_DEGREE = "joint_degree"
    STUDY_ABROAD = "study_abroad"
    INTERNSHIP = "internship"
    RESEARCH = "research"

class BolognaClient:
    """Client for Bologna Process compliance and European higher education standards"""
    
    def __init__(self, client):
        self.client = client
    
    # ECTS Credit System
    async def validate_ects_credits(
        self,
        course_data: Dict[str, Any],
        institution_id: str = None
    ) -> Dict[str, Any]:
        """
        Validate ECTS credit allocation for a course
        
        Args:
            course_data: Course information including workload, learning outcomes
            institution_id: Institution ID for specific validation rules
            
        Returns:
            ECTS validation results and recommendations
        """
        validation_data = {
            'course_data': course_data,
            'institution_id': institution_id
        }
        
        return await self.client.post('/bologna/ects/validate', data=validation_data)
    
    async def calculate_ects_credits(
        self,
        workload_hours: int,
        learning_outcomes: List[str],
        assessment_methods: List[str],
        contact_hours: int = None
    ) -> Dict[str, Any]:
        """
        Calculate appropriate ECTS credits for a course
        
        Args:
            workload_hours: Total student workload in hours
            learning_outcomes: List of learning outcomes
            assessment_methods: Assessment methods used
            contact_hours: Direct contact/teaching hours
            
        Returns:
            Calculated ECTS credits and breakdown
        """
        calculation_data = {
            'workload_hours': workload_hours,
            'learning_outcomes': learning_outcomes,
            'assessment_methods': assessment_methods,
            'contact_hours': contact_hours
        }
        
        return await self.client.post('/bologna/ects/calculate', data=calculation_data)
    
    async def convert_credits_to_ects(
        self,
        credits: float,
        source_system: str,
        source_country: str,
        institution_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Convert credits from other systems to ECTS"""
        conversion_data = {
            'credits': credits,
            'source_system': source_system,
            'source_country': source_country,
            'institution_context': institution_context or {}
        }
        
        return await self.client.post('/bologna/ects/convert', data=conversion_data)
    
    async def get_ects_grade_scale(
        self,
        institution_id: str = None,
        country: str = None
    ) -> Dict[str, Any]:
        """Get ECTS grading scale information"""
        params = {}
        
        if institution_id:
            params['institution_id'] = institution_id
        if country:
            params['country'] = country
        
        return await self.client.get('/bologna/ects/grades', params=params)
    
    # Degree Recognition
    async def assess_degree_recognition(
        self,
        degree_data: Dict[str, Any],
        target_country: str,
        target_institution: str = None,
        profession: str = None
    ) -> Dict[str, Any]:
        """
        Assess probability of degree recognition
        
        Args:
            degree_data: Degree information including institution, qualifications
            target_country: Country where recognition is sought
            target_institution: Specific target institution
            profession: Target profession for professional recognition
            
        Returns:
            Recognition assessment and probability
        """
        assessment_data = {
            'degree_data': degree_data,
            'target_country': target_country,
            'target_institution': target_institution,
            'profession': profession
        }
        
        return await self.client.post('/bologna/recognition/assess', data=assessment_data)
    
    async def get_recognition_requirements(
        self,
        source_country: str,
        target_country: str,
        qualification_level: Union[str, QualificationLevel],
        field_of_study: str = None
    ) -> Dict[str, Any]:
        """Get degree recognition requirements"""
        if isinstance(qualification_level, QualificationLevel):
            qualification_level = qualification_level.value
        
        params = {
            'source_country': source_country,
            'target_country': target_country,
            'qualification_level': qualification_level
        }
        
        if field_of_study:
            params['field_of_study'] = field_of_study
        
        return await self.client.get('/bologna/recognition/requirements', params=params)
    
    async def submit_recognition_application(
        self,
        application_data: Dict[str, Any],
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Submit degree recognition application"""
        submission_data = {
            'application_data': application_data,
            'documents': documents
        }
        
        return await self.client.post('/bologna/recognition/apply', data=submission_data)
    
    async def track_recognition_application(
        self,
        application_id: str
    ) -> Dict[str, Any]:
        """Track status of recognition application"""
        return await self.client.get(f'/bologna/recognition/applications/{application_id}')
    
    # Quality Assurance
    async def check_quality_compliance(
        self,
        institution_data: Dict[str, Any],
        frameworks: List[Union[str, QualificationFramework]],
        assessment_type: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """
        Check institutional quality assurance compliance
        
        Args:
            institution_data: Institution information and programs
            frameworks: Quality assurance frameworks to check against
            assessment_type: Type of assessment (basic, comprehensive, detailed)
            
        Returns:
            Compliance assessment results
        """
        # Convert enums to strings
        framework_strs = []
        for framework in frameworks:
            if isinstance(framework, QualificationFramework):
                framework_strs.append(framework.value)
            else:
                framework_strs.append(framework)
        
        compliance_data = {
            'institution_data': institution_data,
            'frameworks': framework_strs,
            'assessment_type': assessment_type
        }
        
        return await self.client.post('/bologna/quality/check', data=compliance_data)
    
    async def get_quality_standards(
        self,
        framework: Union[str, QualificationFramework],
        country: str = None,
        field_of_study: str = None
    ) -> Dict[str, Any]:
        """Get quality assurance standards"""
        if isinstance(framework, QualificationFramework):
            framework = framework.value
        
        params = {'framework': framework}
        
        if country:
            params['country'] = country
        if field_of_study:
            params['field_of_study'] = field_of_study
        
        return await self.client.get('/bologna/quality/standards', params=params)
    
    async def generate_quality_report(
        self,
        institution_id: str,
        report_type: str = 'annual',
        frameworks: List[Union[str, QualificationFramework]] = None
    ) -> Dict[str, Any]:
        """Generate quality assurance report"""
        if frameworks:
            framework_strs = []
            for framework in frameworks:
                if isinstance(framework, QualificationFramework):
                    framework_strs.append(framework.value)
                else:
                    framework_strs.append(framework)
        else:
            framework_strs = []
        
        report_data = {
            'institution_id': institution_id,
            'report_type': report_type,
            'frameworks': framework_strs
        }
        
        return await self.client.post('/bologna/quality/report', data=report_data)
    
    # Student Mobility
    async def create_mobility_record(
        self,
        student_id: str,
        mobility_data: Dict[str, Any],
        mobility_type: Union[str, MobilityType]
    ) -> Dict[str, Any]:
        """Create student mobility record"""
        if isinstance(mobility_type, MobilityType):
            mobility_type = mobility_type.value
        
        record_data = {
            'student_id': student_id,
            'mobility_data': mobility_data,
            'mobility_type': mobility_type
        }
        
        return await self.client.post('/bologna/mobility/records', data=record_data)
    
    async def get_mobility_opportunities(
        self,
        student_profile: Dict[str, Any],
        target_countries: List[str] = None,
        field_of_study: str = None,
        mobility_type: Union[str, MobilityType] = None
    ) -> List[Dict[str, Any]]:
        """Get available mobility opportunities"""
        params = {}
        
        if target_countries:
            params['countries'] = ','.join(target_countries)
        if field_of_study:
            params['field_of_study'] = field_of_study
        if mobility_type:
            if isinstance(mobility_type, MobilityType):
                mobility_type = mobility_type.value
            params['mobility_type'] = mobility_type
        
        # Include student profile in request body
        return await self.client.post('/bologna/mobility/opportunities', 
                                    data={'student_profile': student_profile},
                                    params=params)
    
    async def validate_mobility_requirements(
        self,
        student_id: str,
        target_program: Dict[str, Any],
        mobility_type: Union[str, MobilityType]
    ) -> Dict[str, Any]:
        """Validate if student meets mobility requirements"""
        if isinstance(mobility_type, MobilityType):
            mobility_type = mobility_type.value
        
        validation_data = {
            'student_id': student_id,
            'target_program': target_program,
            'mobility_type': mobility_type
        }
        
        return await self.client.post('/bologna/mobility/validate', data=validation_data)
    
    async def generate_learning_agreement(
        self,
        mobility_record_id: str,
        courses: List[Dict[str, Any]],
        learning_outcomes: List[str]
    ) -> Dict[str, Any]:
        """Generate learning agreement for mobility"""
        agreement_data = {
            'mobility_record_id': mobility_record_id,
            'courses': courses,
            'learning_outcomes': learning_outcomes
        }
        
        return await self.client.post('/bologna/mobility/learning-agreement', data=agreement_data)
    
    # Learning Outcomes and Competencies
    async def validate_learning_outcomes(
        self,
        outcomes: List[str],
        qualification_level: Union[str, QualificationLevel],
        field_of_study: str,
        framework: Union[str, QualificationFramework] = QualificationFramework.ECTS
    ) -> Dict[str, Any]:
        """Validate learning outcomes against standards"""
        if isinstance(qualification_level, QualificationLevel):
            qualification_level = qualification_level.value
        if isinstance(framework, QualificationFramework):
            framework = framework.value
        
        validation_data = {
            'outcomes': outcomes,
            'qualification_level': qualification_level,
            'field_of_study': field_of_study,
            'framework': framework
        }
        
        return await self.client.post('/bologna/outcomes/validate', data=validation_data)
    
    async def map_competencies(
        self,
        source_competencies: List[str],
        target_framework: Union[str, QualificationFramework],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Map competencies between different frameworks"""
        if isinstance(target_framework, QualificationFramework):
            target_framework = target_framework.value
        
        mapping_data = {
            'source_competencies': source_competencies,
            'target_framework': target_framework,
            'context': context or {}
        }
        
        return await self.client.post('/bologna/competencies/map', data=mapping_data)
    
    async def generate_competency_profile(
        self,
        student_id: str,
        completed_courses: List[Dict[str, Any]],
        framework: Union[str, QualificationFramework] = QualificationFramework.ECTS
    ) -> Dict[str, Any]:
        """Generate student competency profile"""
        if isinstance(framework, QualificationFramework):
            framework = framework.value
        
        profile_data = {
            'student_id': student_id,
            'completed_courses': completed_courses,
            'framework': framework
        }
        
        return await self.client.post('/bologna/competencies/profile', data=profile_data)
    
    # Institutional Cooperation
    async def register_bilateral_agreement(
        self,
        institution1_id: str,
        institution2_id: str,
        agreement_data: Dict[str, Any],
        agreement_type: str = 'mobility'
    ) -> Dict[str, Any]:
        """Register bilateral institutional agreement"""
        registration_data = {
            'institution1_id': institution1_id,
            'institution2_id': institution2_id,
            'agreement_data': agreement_data,
            'agreement_type': agreement_type
        }
        
        return await self.client.post('/bologna/agreements/bilateral', data=registration_data)
    
    async def get_partner_institutions(
        self,
        institution_id: str,
        country: str = None,
        field_of_study: str = None,
        agreement_type: str = None
    ) -> List[Dict[str, Any]]:
        """Get partner institutions"""
        params = {'institution_id': institution_id}
        
        if country:
            params['country'] = country
        if field_of_study:
            params['field_of_study'] = field_of_study
        if agreement_type:
            params['agreement_type'] = agreement_type
        
        return await self.client.get('/bologna/agreements/partners', params=params)
    
    async def validate_joint_program(
        self,
        program_data: Dict[str, Any],
        participating_institutions: List[str]
    ) -> Dict[str, Any]:
        """Validate joint/double degree program compliance"""
        validation_data = {
            'program_data': program_data,
            'participating_institutions': participating_institutions
        }
        
        return await self.client.post('/bologna/programs/joint/validate', data=validation_data)
    
    # Bologna Process Compliance Monitoring
    async def get_compliance_dashboard(
        self,
        institution_id: str,
        time_period: str = '12m'
    ) -> Dict[str, Any]:
        """Get Bologna Process compliance dashboard"""
        params = {
            'institution_id': institution_id,
            'time_period': time_period
        }
        
        return await self.client.get('/bologna/compliance/dashboard', params=params)
    
    async def generate_compliance_report(
        self,
        institution_id: str,
        report_type: str = 'comprehensive',
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """Generate Bologna Process compliance report"""
        report_data = {
            'institution_id': institution_id,
            'report_type': report_type,
            'include_recommendations': include_recommendations
        }
        
        return await self.client.post('/bologna/compliance/report', data=report_data)
    
    async def get_non_compliance_issues(
        self,
        institution_id: str,
        severity: str = None
    ) -> List[Dict[str, Any]]:
        """Get identified non-compliance issues"""
        params = {'institution_id': institution_id}
        
        if severity:
            params['severity'] = severity
        
        return await self.client.get('/bologna/compliance/issues', params=params)
    
    async def create_compliance_action_plan(
        self,
        institution_id: str,
        issues: List[str],
        timeline: int = 12
    ) -> Dict[str, Any]:
        """Create action plan to address compliance issues"""
        action_plan_data = {
            'institution_id': institution_id,
            'issues': issues,
            'timeline': timeline
        }
        
        return await self.client.post('/bologna/compliance/action-plan', data=action_plan_data)
    
    # Analytics and Reporting
    async def get_bologna_analytics(
        self,
        metric_type: str,
        time_period: str = '12m',
        country: str = None,
        institution_type: str = None
    ) -> Dict[str, Any]:
        """Get Bologna Process analytics"""
        params = {
            'metric_type': metric_type,
            'time_period': time_period
        }
        
        if country:
            params['country'] = country
        if institution_type:
            params['institution_type'] = institution_type
        
        return await self.client.get('/bologna/analytics', params=params)
    
    async def get_mobility_statistics(
        self,
        country: str = None,
        time_period: str = '12m',
        mobility_type: Union[str, MobilityType] = None
    ) -> Dict[str, Any]:
        """Get student mobility statistics"""
        params = {'time_period': time_period}
        
        if country:
            params['country'] = country
        if mobility_type:
            if isinstance(mobility_type, MobilityType):
                mobility_type = mobility_type.value
            params['mobility_type'] = mobility_type
        
        return await self.client.get('/bologna/analytics/mobility', params=params)