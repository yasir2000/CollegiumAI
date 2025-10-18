"""
Bologna Process Agent - European Higher Education Area Framework
===============================================================

This agent provides specialized support for Bologna Process compliance,
ECTS credit management, mobility programs, and European qualification
framework alignment for universities in the European Higher Education Area.

Key Bologna Process Features:
- Three-cycle degree structure (Bachelor/Master/Doctorate)
- ECTS credit system and transfer
- Quality assurance and accreditation
- Recognition of qualifications and study periods
- Promotion of mobility and international cooperation
- European Qualifications Framework (EQF) alignment
- Diploma Supplement issuance
- Joint and double degree programs
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import logging

from ..core import (
    BaseAgent, AgentResponse, AgentThought, AgentAction,
    UniversityContext, PersonaType, GovernanceFramework,
    BolognaProcessData
)

logger = logging.getLogger(__name__)

class BolognaProcessAgent(BaseAgent):
    """
    Specialized agent for Bologna Process compliance and European Higher Education Area integration
    """
    
    def __init__(self, agent_id: str, university_context: UniversityContext):
        super().__init__(agent_id, university_context)
        self.agent_type = "bologna_process"
        self.description = "European Higher Education Area compliance and mobility specialist"
        
        # Bologna Process specific knowledge base
        self.bologna_knowledge = {
            "ects_system": {
                "bachelor_credits": 180,  # Typically 3 years * 60 ECTS
                "master_credits": 120,   # Typically 2 years * 60 ECTS
                "annual_credits": 60,    # Standard full-time academic year
                "workload_hours_per_credit": 25,  # 25-30 hours per ECTS credit
                "grading_scale": {
                    "A": "Excellent (90-100%)",
                    "B": "Very Good (80-89%)",
                    "C": "Good (70-79%)",
                    "D": "Satisfactory (60-69%)",
                    "E": "Sufficient (50-59%)",
                    "F": "Fail (<50%)"
                }
            },
            "qualification_levels": {
                1: "Basic general knowledge",
                2: "Basic factual knowledge of a field of work or study",
                3: "Knowledge of facts, principles, processes and general concepts",
                4: "Factual and theoretical knowledge in broad contexts",
                5: "Comprehensive, specialised factual and theoretical knowledge",
                6: "Advanced knowledge demonstrating mastery (Bachelor level)",
                7: "Highly specialised knowledge building on bachelor (Master level)",
                8: "Knowledge at most advanced frontier (Doctoral level)"
            },
            "mobility_programs": [
                "Erasmus+",
                "CEEPUS",
                "NORDPLUS",
                "Fulbright",
                "Marie Skłodowska-Curie Actions"
            ],
            "recognition_tools": [
                "ENIC-NARIC networks",
                "European Credit Transfer System (ECTS)",
                "Diploma Supplement",
                "Europass",
                "European Qualifications Framework (EQF)"
            ]
        }
    
    async def process_query(
        self,
        message: str,
        context: Dict[str, Any],
        user_id: str,
        user_type: PersonaType,
        collaborative: bool = True
    ) -> AgentResponse:
        """Process Bologna Process related queries"""
        
        thoughts = []
        actions = []
        
        # Initial thought and assessment
        initial_thought = AgentThought(
            thought="Analyzing Bologna Process query and user context",
            reasoning=f"User ({user_type.value}) needs Bologna Process assistance: {message}",
            confidence=0.9,
            relevant_context=["bologna_process", "ects", "mobility", "recognition"]
        )
        thoughts.append(initial_thought)
        
        # Determine query type and appropriate response
        query_analysis = await self._analyze_bologna_query(message, context, user_type)
        thoughts.extend(query_analysis["thoughts"])
        actions.extend(query_analysis["actions"])
        
        # Generate specialized response based on query type
        if query_analysis["query_type"] == "ects_management":
            response_data = await self._handle_ects_query(message, context, user_type)
        elif query_analysis["query_type"] == "mobility_planning":
            response_data = await self._handle_mobility_query(message, context, user_type)
        elif query_analysis["query_type"] == "recognition_procedures":
            response_data = await self._handle_recognition_query(message, context, user_type)
        elif query_analysis["query_type"] == "quality_assurance":
            response_data = await self._handle_quality_assurance_query(message, context, user_type)
        elif query_analysis["query_type"] == "degree_structure":
            response_data = await self._handle_degree_structure_query(message, context, user_type)
        else:
            response_data = await self._handle_general_bologna_query(message, context, user_type)
        
        thoughts.extend(response_data["thoughts"])
        actions.extend(response_data["actions"])
        
        # Collaborative input if requested
        collaborating_agents = []
        if collaborative:
            if user_type in [PersonaType.TRADITIONAL_STUDENT, PersonaType.INTERNATIONAL_STUDENT]:
                # Collaborate with academic advisor for academic planning
                collaboration = await self._collaborate_with_academic_advisor(message, context)
                if collaboration:
                    collaborating_agents.append("academic_advisor")
                    thoughts.append(AgentThought(
                        thought="Collaborated with academic advisor for comprehensive planning",
                        reasoning="Bologna Process decisions impact overall academic planning",
                        confidence=0.8,
                        relevant_context=["academic_planning", "course_selection"]
                    ))
        
        # Final recommendation compilation
        final_response = response_data["response"]
        recommendations = response_data.get("recommendations", [])
        
        # Add Bologna Process specific recommendations
        recommendations.extend([
            "Ensure ECTS credits align with European standards",
            "Consider mobility opportunities for international experience",
            "Maintain documentation for qualification recognition"
        ])
        
        return AgentResponse(
            success=True,
            thoughts=[asdict(t) for t in thoughts],
            actions=[asdict(a) for a in actions],
            final_response=final_response,
            confidence=response_data["confidence"],
            collaborating_agents=collaborating_agents,
            recommendations=recommendations,
            metadata={
                "query_type": query_analysis["query_type"],
                "bologna_frameworks_applied": ["ECTS", "EQF", "Diploma_Supplement"],
                "user_type": user_type.value,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    async def _analyze_bologna_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Analyze the type of Bologna Process query"""
        
        message_lower = message.lower()
        thoughts = []
        actions = []
        
        # Query classification logic
        if any(keyword in message_lower for keyword in ["ects", "credits", "transfer", "recognition"]):
            query_type = "ects_management"
        elif any(keyword in message_lower for keyword in ["mobility", "erasmus", "exchange", "study abroad"]):
            query_type = "mobility_planning"
        elif any(keyword in message_lower for keyword in ["recognition", "diploma", "qualification", "equivalent"]):
            query_type = "recognition_procedures"
        elif any(keyword in message_lower for keyword in ["quality", "assurance", "accreditation", "standards"]):
            query_type = "quality_assurance"
        elif any(keyword in message_lower for keyword in ["bachelor", "master", "doctorate", "degree", "cycle"]):
            query_type = "degree_structure"
        else:
            query_type = "general_bologna"
        
        analysis_thought = AgentThought(
            thought=f"Classified query as {query_type} based on keywords and context",
            reasoning=f"Message contains Bologna Process indicators: {message_lower[:100]}...",
            confidence=0.85,
            relevant_context=[query_type, "bologna_process"]
        )
        thoughts.append(analysis_thought)
        
        # Log analysis action
        analysis_action = AgentAction(
            action_type="query_analysis",
            parameters={"query_type": query_type, "keywords_found": True},
            success=True,
            result={"classification": query_type}
        )
        actions.append(analysis_action)
        
        return {
            "query_type": query_type,
            "thoughts": thoughts,
            "actions": actions
        }
    
    async def _handle_ects_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Handle ECTS credit system queries"""
        
        thoughts = []
        actions = []
        
        # Get user's academic context
        current_credits = context.get("completed_credits", 0)
        program_type = context.get("degree_level", "bachelor")
        target_credits = self.bologna_knowledge["ects_system"].get(f"{program_type}_credits", 180)
        
        ects_thought = AgentThought(
            thought="Analyzing ECTS credit requirements and transfer possibilities",
            reasoning=f"Student has {current_credits} credits, needs {target_credits} for {program_type}",
            confidence=0.9,
            relevant_context=["ects_system", "credit_transfer"]
        )
        thoughts.append(ects_thought)
        
        # Calculate ECTS equivalency if needed
        ects_calculation = await self._calculate_ects_equivalency(context)
        actions.append(AgentAction(
            action_type="ects_calculation",
            parameters={"current_credits": current_credits, "target_credits": target_credits},
            success=True,
            result=ects_calculation
        ))
        
        # Generate ECTS-specific response
        response = f"""
        **ECTS Credit System Analysis**
        
        Based on your current status:
        - Current ECTS Credits: {current_credits}
        - Required for {program_type.title()}: {target_credits} ECTS
        - Remaining Credits Needed: {max(0, target_credits - current_credits)} ECTS
        
        **ECTS System Overview:**
        - 1 ECTS credit = 25-30 hours of student workload
        - Full academic year = 60 ECTS credits
        - Bachelor's degree = 180-240 ECTS (typically 180)
        - Master's degree = 90-120 ECTS (typically 120)
        
        **Credit Transfer Information:**
        Your credits can be transferred between European institutions through:
        - ECTS Learning Agreements
        - Transcript of Records
        - Bilateral agreements between institutions
        
        **Grade Conversion:**
        ECTS grading scale ensures fair recognition across institutions:
        {json.dumps(self.bologna_knowledge["ects_system"]["grading_scale"], indent=2)}
        """
        
        recommendations = [
            "Request official ECTS transcript for mobility applications",
            "Verify credit transfer agreements with target institutions",
            "Plan coursework to meet annual 60 ECTS requirement",
            "Consider Recognition of Prior Learning (RPL) for non-formal qualifications"
        ]
        
        return {
            "response": response,
            "confidence": 0.92,
            "thoughts": thoughts,
            "actions": actions,
            "recommendations": recommendations
        }
    
    async def _handle_mobility_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Handle student/staff mobility program queries"""
        
        thoughts = []
        actions = []
        
        mobility_thought = AgentThought(
            thought="Analyzing mobility opportunities and requirements within EHEA",
            reasoning="Student/staff seeks mobility options under Bologna Process framework",
            confidence=0.88,
            relevant_context=["mobility_programs", "erasmus", "recognition"]
        )
        thoughts.append(mobility_thought)
        
        # Get mobility recommendations
        mobility_options = await self._get_mobility_recommendations(context, user_type)
        actions.append(AgentAction(
            action_type="mobility_analysis",
            parameters={"user_type": user_type.value, "context": context},
            success=True,
            result=mobility_options
        ))
        
        response = f"""
        **European Mobility Opportunities**
        
        **Available Programs:**
        {chr(10).join([f"• {program}" for program in self.bologna_knowledge["mobility_programs"]])}
        
        **Mobility Benefits:**
        - ECTS credit recognition across European institutions
        - Enhanced language skills and cultural competency
        - Expanded academic and professional networks
        - Improved employability in European job market
        
        **Requirements for Mobility:**
        - Learning Agreement signed before departure
        - Minimum academic standing maintained
        - ECTS credit pre-approval from home institution
        - Language proficiency certification (if required)
        
        **Recognition Guarantees:**
        - Credits earned abroad automatically recognized
        - No additional fees for credit recognition
        - Grades converted using ECTS grading scale
        - Academic progress maintained in degree timeline
        
        **Application Process:**
        1. Consult with Bologna Process coordinator
        2. Select partner institution and courses
        3. Complete Learning Agreement
        4. Submit mobility application
        5. Prepare required documentation
        """
        
        recommendations = [
            "Start mobility planning at least 6 months in advance",
            "Research language requirements for target countries",
            "Connect with Bologna Process office for guidance",
            "Consider joint/double degree programs for extended mobility"
        ]
        
        return {
            "response": response,
            "confidence": 0.89,
            "thoughts": thoughts,
            "actions": actions,
            "recommendations": recommendations
        }
    
    async def _handle_recognition_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Handle qualification recognition queries"""
        
        thoughts = []
        actions = []
        
        recognition_thought = AgentThought(
            thought="Analyzing qualification recognition procedures and requirements",
            reasoning="User needs guidance on European qualification recognition processes",
            confidence=0.87,
            relevant_context=["enic_naric", "diploma_supplement", "recognition"]
        )
        thoughts.append(recognition_thought)
        
        # Check recognition requirements
        recognition_analysis = await self._analyze_recognition_requirements(context)
        actions.append(AgentAction(
            action_type="recognition_analysis",
            parameters={"qualification_data": context},
            success=True,
            result=recognition_analysis
        ))
        
        response = f"""
        **Qualification Recognition in European Higher Education Area**
        
        **Recognition Tools Available:**
        {chr(10).join([f"• {tool}" for tool in self.bologna_knowledge["recognition_tools"]])}
        
        **Automatic Recognition:**
        Under Bologna Process, qualifications are automatically recognized for:
        - Access to next cycle of studies
        - Employment purposes (where applicable)
        - Credit transfer between institutions
        
        **Diploma Supplement:**
        - Standardized description of qualification
        - Available in major European languages
        - Enhances international transparency
        - Facilitates recognition procedures
        
        **ENIC-NARIC Network:**
        - National Academic Recognition Information Centres
        - Provide official recognition decisions
        - Offer information on qualification systems
        - Support fair recognition practices
        
        **European Qualifications Framework (EQF) Levels:**
        {chr(10).join([f"Level {level}: {desc}" for level, desc in self.bologna_knowledge["qualification_levels"].items()])}
        
        **Recognition Process:**
        1. Submit application to relevant NARIC centre
        2. Provide original qualification documents
        3. Include official translations if required
        4. Pay applicable recognition fees
        5. Await recognition decision (typically 2-4 months)
        """
        
        recommendations = [
            "Request Diploma Supplement from awarding institution",
            "Contact NARIC centre in target country early",
            "Prepare certified translations of documents",
            "Keep detailed records of all academic achievements"
        ]
        
        return {
            "response": response,
            "confidence": 0.91,
            "thoughts": thoughts,
            "actions": actions,
            "recommendations": recommendations
        }
    
    async def _handle_quality_assurance_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Handle quality assurance and accreditation queries"""
        
        thoughts = []
        actions = []
        
        qa_thought = AgentThought(
            thought="Analyzing Bologna Process quality assurance requirements",
            reasoning="Query relates to European quality standards and accreditation",
            confidence=0.86,
            relevant_context=["quality_assurance", "esg", "accreditation"]
        )
        thoughts.append(qa_thought)
        
        response = """
        **Bologna Process Quality Assurance Framework**
        
        **Standards and Guidelines for Quality Assurance (ESG):**
        
        **Part 1 - Internal Quality Assurance:**
        • Policy for quality assurance
        • Design and approval of programmes
        • Student-centred learning and assessment
        • Student admission, progression, and certification
        • Teaching staff qualifications and development
        • Learning resources and student support
        • Information management systems
        • Public information transparency
        • Ongoing monitoring and review processes
        
        **Part 2 - External Quality Assurance:**
        • Consideration of internal quality assurance
        • Designing methodologies fit for purpose
        • Implementing processes consistently
        • Peer review procedures
        • Criteria for outcomes and decisions
        • Reporting transparency and completeness
        • Complaints and appeals procedures
        
        **Part 3 - Quality Assurance Agencies:**
        • Activities, policy, and processes for quality assurance
        • Official status and formal recognition
        • Independence and stakeholder involvement
        • Thematic analysis and system-wide overview
        • Resources allocation and management
        • Internal quality assurance and professional conduct
        • Cyclical external review of agencies
        
        **European Quality Assurance Register (EQAR):**
        - Lists quality assurance agencies that comply with ESG
        - Enhances trust in European higher education
        - Supports recognition of quality assurance decisions
        - Facilitates mobility and cooperation
        
        **Institutional Accreditation Benefits:**
        - Enhanced institutional reputation
        - Improved student mobility opportunities
        - Greater employer confidence in graduates
        - Access to European funding programmes
        - Participation in joint programme initiatives
        """
        
        recommendations = [
            "Ensure institutional compliance with ESG standards",
            "Engage with recognized quality assurance agencies",
            "Implement continuous improvement processes",
            "Maintain transparent quality information systems"
        ]
        
        return {
            "response": response,
            "confidence": 0.88,
            "thoughts": thoughts,
            "actions": actions,
            "recommendations": recommendations
        }
    
    async def _handle_degree_structure_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Handle three-cycle degree structure queries"""
        
        thoughts = []
        actions = []
        
        structure_thought = AgentThought(
            thought="Explaining Bologna Process three-cycle degree structure",
            reasoning="User needs clarification on European degree framework",
            confidence=0.93,
            relevant_context=["degree_cycles", "ects", "qualification_levels"]
        )
        thoughts.append(structure_thought)
        
        response = """
        **Bologna Process Three-Cycle Degree Structure**
        
        **First Cycle - Bachelor's Degree:**
        • Duration: Typically 3-4 years (180-240 ECTS)
        • Purpose: Broad foundation in chosen field
        • Outcomes: Employment qualification or access to second cycle
        • EQF Level: 6 (Advanced knowledge demonstrating mastery)
        • Key Features: Core subject knowledge, transferable skills
        
        **Second Cycle - Master's Degree:**
        • Duration: 1-2 years (90-120 ECTS)
        • Purpose: Specialization and advanced competencies
        • Access: First cycle degree or equivalent qualification
        • EQF Level: 7 (Highly specialised knowledge)
        • Types: Academic masters, professional masters, integrated programmes
        
        **Third Cycle - Doctoral Degree:**
        • Duration: 3-4+ years (no fixed ECTS requirement)
        • Purpose: Original research and knowledge creation
        • Access: Second cycle degree (Master's level)
        • EQF Level: 8 (Knowledge at most advanced frontier)
        • Requirements: Original thesis, public defense, research training
        
        **Integrated Programmes:**
        • Long first cycle (300-360 ECTS) leading directly to Master's level
        • Common in: Medicine, Dentistry, Veterinary Medicine, Engineering
        • Maintain competency equivalent to standard two-cycle route
        
        **Short Cycle Qualifications:**
        • Duration: 2-3 years (120 ECTS)
        • EQF Level: 5 (Comprehensive, specialised knowledge)
        • Purpose: Technical and professional qualifications
        • Integration: Can provide access to first cycle programmes
        
        **Quality Assurance Across Cycles:**
        • Dublin Descriptors define learning outcomes for each cycle
        • ECTS ensures credit comparability and transfer
        • National qualification frameworks align with EQF
        • Regular programme reviews ensure standards maintenance
        """
        
        recommendations = [
            "Plan academic progression across Bologna cycles",
            "Understand ECTS requirements for each degree level",
            "Consider integrated programmes where appropriate",
            "Align career goals with qualification levels"
        ]
        
        return {
            "response": response,
            "confidence": 0.94,
            "thoughts": thoughts,
            "actions": actions,
            "recommendations": recommendations
        }
    
    async def _handle_general_bologna_query(
        self, 
        message: str, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Handle general Bologna Process queries"""
        
        thoughts = []
        actions = []
        
        general_thought = AgentThought(
            thought="Providing comprehensive Bologna Process overview",
            reasoning="User needs general information about European Higher Education Area",
            confidence=0.85,
            relevant_context=["bologna_process", "ehea", "reforms"]
        )
        thoughts.append(general_thought)
        
        response = """
        **Bologna Process Overview - European Higher Education Area**
        
        **What is the Bologna Process?**
        The Bologna Process is a series of ministerial meetings and agreements between European countries designed to ensure comparability in the standards and quality of higher education qualifications across Europe.
        
        **Key Objectives:**
        • Adoption of easily readable and comparable degrees
        • Introduction of the three-cycle system (Bachelor/Master/Doctorate)
        • Establishment of the ECTS credit system
        • Promotion of mobility among students, teachers, and researchers
        • Enhancement of quality assurance cooperation
        • Promotion of the European dimension in higher education
        
        **Bologna Process Action Lines:**
        1. **Degree Structure:** Three-cycle system implementation
        2. **Quality Assurance:** ESG standards adoption
        3. **Recognition:** Qualifications and study periods
        4. **Mobility:** Student and staff exchange programs
        5. **ECTS:** European Credit Transfer and Accumulation System
        6. **Diploma Supplement:** Standardized qualification description
        7. **Lifelong Learning:** Recognition of prior learning
        8. **Employability:** Labour market relevant skills
        9. **Student Involvement:** Partnership in governance
        10. **Social Dimension:** Widening access and participation
        
        **Participating Countries:** 49 countries across Europe
        
        **Benefits for Students:**
        • Enhanced mobility opportunities across Europe
        • Automatic recognition of qualifications
        • Transparent academic progression
        • Improved employability in European job market
        • Access to diverse educational opportunities
        
        **Benefits for Institutions:**
        • Increased international cooperation
        • Enhanced reputation and competitiveness
        • Access to European funding programmes
        • Simplified partnership agreements
        • Quality improvement through peer review
        """
        
        recommendations = [
            "Familiarize yourself with Bologna Process principles",
            "Leverage EHEA opportunities for academic and career development",
            "Engage with international mobility programmes",
            "Stay informed about Bologna Process developments"
        ]
        
        return {
            "response": response,
            "confidence": 0.87,
            "thoughts": thoughts,
            "actions": actions,
            "recommendations": recommendations
        }
    
    async def _calculate_ects_equivalency(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ECTS credit equivalency for transfer/recognition"""
        
        current_credits = context.get("completed_credits", 0)
        credit_system = context.get("credit_system", "ects")
        
        if credit_system == "ects":
            return {"ects_credits": current_credits, "conversion_rate": 1.0}
        
        # Common credit system conversions
        conversion_rates = {
            "us_credits": 2.0,      # 1 US credit ≈ 2 ECTS
            "uk_credits": 0.5,      # 2 UK credits ≈ 1 ECTS
            "german_cp": 1.0,       # German CP = ECTS
            "french_credits": 1.0   # French credits aligned with ECTS
        }
        
        rate = conversion_rates.get(credit_system, 1.0)
        ects_equivalent = current_credits * rate
        
        return {
            "original_credits": current_credits,
            "original_system": credit_system,
            "ects_credits": ects_equivalent,
            "conversion_rate": rate
        }
    
    async def _get_mobility_recommendations(
        self, 
        context: Dict[str, Any], 
        user_type: PersonaType
    ) -> Dict[str, Any]:
        """Get personalized mobility programme recommendations"""
        
        recommendations = []
        
        if user_type in [PersonaType.TRADITIONAL_STUDENT, PersonaType.INTERNATIONAL_STUDENT]:
            recommendations.extend([
                "Erasmus+ student mobility for studies",
                "Erasmus+ student mobility for traineeships",
                "Joint Master's programmes",
                "Summer/winter schools"
            ])
        
        if user_type in [PersonaType.GRADUATE_STUDENT, PersonaType.RESEARCHER]:
            recommendations.extend([
                "Marie Skłodowska-Curie Individual Fellowships",
                "Erasmus+ doctoral programmes",
                "Research collaboration networks"
            ])
        
        if user_type in [PersonaType.PROFESSOR, PersonaType.LECTURER]:
            recommendations.extend([
                "Erasmus+ staff mobility for teaching",
                "Erasmus+ staff mobility for training",
                "European University Alliance participation"
            ])
        
        return {"recommended_programmes": recommendations}
    
    async def _analyze_recognition_requirements(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specific recognition requirements based on qualification"""
        
        qualification_type = context.get("qualification_type", "bachelor")
        origin_country = context.get("origin_country", "unknown")
        target_country = context.get("target_country", "unknown")
        
        requirements = {
            "documents_needed": [
                "Original qualification certificate",
                "Academic transcript",
                "Diploma Supplement (if available)",
                "Official translations"
            ],
            "processing_time": "2-4 months",
            "fees": "Varies by country (€50-200 typical)",
            "success_likelihood": "High for Bologna Process qualifications"
        }
        
        return requirements
    
    async def _collaborate_with_academic_advisor(
        self, 
        message: str, 
        context: Dict[str, Any]
    ) -> bool:
        """Collaborate with academic advisor for comprehensive planning"""
        
        # Simulate collaboration check
        academic_keywords = ["course", "degree", "planning", "graduation", "requirements"]
        
        return any(keyword in message.lower() for keyword in academic_keywords)

def asdict(obj):
    """Convert dataclass to dictionary"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return obj