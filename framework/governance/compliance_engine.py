"""
Governance Compliance Engine
===========================

Core engine for managing compliance with educational governance frameworks
including AACSB, WASC, HEFCE, and QAA standards.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json
import asyncio
from pathlib import Path

class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    WARNING = "warning"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"

class AuditSeverity(Enum):
    """Audit finding severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class ComplianceStandard:
    """Represents a governance framework standard"""
    id: str
    framework: str
    name: str
    description: str
    requirements: List[str]
    weight: float = 1.0
    mandatory: bool = True
    evidence_types: List[str] = field(default_factory=list)
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None

@dataclass
class ComplianceEvidence:
    """Evidence supporting compliance with a standard"""
    id: str
    standard_id: str
    type: str
    title: str
    description: str
    file_path: Optional[str] = None
    url: Optional[str] = None
    created_date: datetime = field(default_factory=datetime.now)
    expiry_date: Optional[datetime] = None
    verified: bool = False
    verifier: Optional[str] = None

@dataclass
class AuditFinding:
    """Represents an audit finding"""
    id: str
    audit_id: str
    standard_id: str
    severity: AuditSeverity
    title: str
    description: str
    recommendation: str
    status: str = "open"
    assigned_to: Optional[str] = None
    created_date: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None

@dataclass
class ComplianceAssessment:
    """Results of a compliance assessment"""
    id: str
    framework: str
    assessment_date: datetime
    assessor: str
    overall_status: ComplianceStatus
    overall_score: float
    standards_assessed: int
    standards_compliant: int
    findings: List[AuditFinding] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    next_assessment: Optional[datetime] = None

class GovernanceFramework(ABC):
    """Abstract base class for governance frameworks"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.standards: Dict[str, ComplianceStandard] = {}
        self.evidence: Dict[str, List[ComplianceEvidence]] = {}
        
    @abstractmethod
    def load_standards(self) -> None:
        """Load framework standards"""
        pass
    
    @abstractmethod
    async def assess_compliance(self, context: Dict[str, Any]) -> ComplianceAssessment:
        """Assess compliance with framework standards"""
        pass
    
    def add_evidence(self, evidence: ComplianceEvidence) -> None:
        """Add evidence for a standard"""
        if evidence.standard_id not in self.evidence:
            self.evidence[evidence.standard_id] = []
        self.evidence[evidence.standard_id].append(evidence)
    
    def get_evidence(self, standard_id: str) -> List[ComplianceEvidence]:
        """Get evidence for a standard"""
        return self.evidence.get(standard_id, [])
    
    def calculate_compliance_score(self, assessed_standards: Dict[str, float]) -> float:
        """Calculate overall compliance score"""
        if not assessed_standards:
            return 0.0
        
        total_weight = sum(std.weight for std in self.standards.values() 
                          if std.id in assessed_standards)
        
        if total_weight == 0:
            return 0.0
        
        weighted_score = sum(score * self.standards[std_id].weight 
                           for std_id, score in assessed_standards.items())
        
        return weighted_score / total_weight

class AACSBFramework(GovernanceFramework):
    """AACSB International accreditation framework"""
    
    def __init__(self):
        super().__init__("AACSB", "2020")
        self.load_standards()
    
    def load_standards(self) -> None:
        """Load AACSB standards"""
        self.standards = {
            "1": ComplianceStandard(
                id="1",
                framework="AACSB",
                name="Strategic Management",
                description="Mission, strategic planning, and resource allocation",
                requirements=[
                    "Clear mission statement aligned with stakeholder needs",
                    "Strategic plan with measurable objectives",
                    "Resource allocation supporting strategic priorities",
                    "Regular strategic plan review and updates"
                ],
                weight=1.5,
                evidence_types=["policy_document", "strategic_plan", "financial_report"]
            ),
            "2": ComplianceStandard(
                id="2", 
                framework="AACSB",
                name="Learning and Teaching",
                description="Curriculum management and learning assurance",
                requirements=[
                    "Learning goals aligned with mission",
                    "Curriculum management processes",
                    "Assessment of learning outcomes",
                    "Continuous improvement of programs"
                ],
                weight=2.0,
                evidence_types=["curriculum_document", "assessment_report", "learning_outcomes"]
            ),
            "3": ComplianceStandard(
                id="3",
                framework="AACSB", 
                name="Academic and Professional Engagement",
                description="Faculty qualifications and engagement",
                requirements=[
                    "Faculty with academic qualifications",
                    "Faculty with professional qualifications", 
                    "Faculty development programs",
                    "Professional engagement activities"
                ],
                weight=1.5,
                evidence_types=["faculty_cv", "development_record", "engagement_report"]
            ),
            "4": ComplianceStandard(
                id="4",
                framework="AACSB",
                name="Student Academic Achievement",
                description="Student admission, progression, and achievement",
                requirements=[
                    "Student admission standards",
                    "Academic progression policies",
                    "Achievement measurement systems",
                    "Student support services"
                ],
                weight=1.0,
                evidence_types=["admission_policy", "progression_data", "achievement_report"]
            )
        }
    
    async def assess_compliance(self, context: Dict[str, Any]) -> ComplianceAssessment:
        """Assess AACSB compliance"""
        assessment_id = f"aacsb_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        findings = []
        standard_scores = {}
        
        # Assess each standard
        for std_id, standard in self.standards.items():
            score, standard_findings = await self._assess_standard(standard, context)
            standard_scores[std_id] = score
            findings.extend(standard_findings)
        
        # Calculate overall score
        overall_score = self.calculate_compliance_score(standard_scores)
        
        # Determine overall status
        if overall_score >= 85:
            overall_status = ComplianceStatus.COMPLIANT
        elif overall_score >= 70:
            overall_status = ComplianceStatus.WARNING
        else:
            overall_status = ComplianceStatus.NON_COMPLIANT
        
        return ComplianceAssessment(
            id=assessment_id,
            framework="AACSB",
            assessment_date=datetime.now(),
            assessor=context.get("assessor", "System"),
            overall_status=overall_status,
            overall_score=overall_score,
            standards_assessed=len(self.standards),
            standards_compliant=sum(1 for score in standard_scores.values() if score >= 70),
            findings=findings,
            next_assessment=datetime.now() + timedelta(days=365)
        )
    
    async def _assess_standard(self, standard: ComplianceStandard, context: Dict[str, Any]) -> tuple[float, List[AuditFinding]]:
        """Assess a single standard"""
        findings = []
        
        # Check evidence availability
        evidence = self.get_evidence(standard.id)
        evidence_score = min(len(evidence) * 25, 100) if evidence else 0
        
        # Mock compliance checking (replace with actual logic)
        base_score = 75  # Base compliance score
        
        # Adjust score based on evidence
        if evidence_score < 50:
            findings.append(AuditFinding(
                id=f"finding_{standard.id}_{datetime.now().strftime('%H%M%S')}",
                audit_id="system_assessment",
                standard_id=standard.id,
                severity=AuditSeverity.MEDIUM,
                title=f"Insufficient evidence for {standard.name}",
                description=f"Limited evidence available for {standard.name} compliance",
                recommendation="Collect and upload additional supporting evidence"
            ))
            base_score -= 15
        
        # Check for expired evidence
        expired_evidence = [e for e in evidence if e.expiry_date and e.expiry_date < datetime.now()]
        if expired_evidence:
            findings.append(AuditFinding(
                id=f"finding_{standard.id}_expired_{datetime.now().strftime('%H%M%S')}",
                audit_id="system_assessment",
                standard_id=standard.id,
                severity=AuditSeverity.HIGH,
                title=f"Expired evidence for {standard.name}",
                description=f"{len(expired_evidence)} evidence items have expired",
                recommendation="Update expired evidence with current documentation"
            ))
            base_score -= 20
        
        final_score = max(0, min(100, base_score + (evidence_score - 50) * 0.3))
        
        return final_score, findings

class WASCFramework(GovernanceFramework):
    """WASC Senior College accreditation framework"""
    
    def __init__(self):
        super().__init__("WASC", "2013")
        self.load_standards()
    
    def load_standards(self) -> None:
        """Load WASC standards"""
        self.standards = {
            "1": ComplianceStandard(
                id="1",
                framework="WASC",
                name="Institutional Purpose and Objectives",
                description="Mission, purposes, and student learning outcomes",
                requirements=[
                    "Clear institutional mission and purposes",
                    "Defined student learning outcomes",
                    "Mission alignment with actual operations",
                    "Regular mission review and updates"
                ],
                weight=1.0,
                evidence_types=["mission_statement", "learning_outcomes", "strategic_plan"]
            ),
            "2": ComplianceStandard(
                id="2",
                framework="WASC", 
                name="Educational Quality and Institutional Effectiveness",
                description="Assessment and improvement of educational effectiveness",
                requirements=[
                    "Assessment of educational effectiveness",
                    "Use of assessment results for improvement",
                    "Faculty engagement in assessment",
                    "Evidence of institutional learning"
                ],
                weight=2.0,
                evidence_types=["assessment_report", "improvement_plan", "faculty_engagement"]
            ),
            "3": ComplianceStandard(
                id="3",
                framework="WASC",
                name="Resources",
                description="Human, physical, technology, and financial resources",
                requirements=[
                    "Adequate human resources",
                    "Appropriate physical facilities",
                    "Sufficient technology resources",
                    "Sound financial management"
                ],
                weight=1.5,
                evidence_types=["resource_inventory", "budget_report", "facility_assessment"]
            ),
            "4": ComplianceStandard(
                id="4",
                framework="WASC",
                name="Leadership and Governance",
                description="Institutional leadership and governance structures",
                requirements=[
                    "Effective institutional leadership",
                    "Appropriate governance structures",
                    "Board oversight and accountability",
                    "Transparent decision-making processes"
                ],
                weight=1.5,
                evidence_types=["governance_policy", "board_minutes", "leadership_structure"]
            )
        }
    
    async def assess_compliance(self, context: Dict[str, Any]) -> ComplianceAssessment:
        """Assess WASC compliance"""
        assessment_id = f"wasc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        findings = []
        standard_scores = {}
        
        # Assess each standard
        for std_id, standard in self.standards.items():
            score, standard_findings = await self._assess_standard(standard, context)
            standard_scores[std_id] = score
            findings.extend(standard_findings)
        
        # Calculate overall score
        overall_score = self.calculate_compliance_score(standard_scores)
        
        # Determine overall status
        if overall_score >= 80:
            overall_status = ComplianceStatus.COMPLIANT
        elif overall_score >= 65:
            overall_status = ComplianceStatus.WARNING
        else:
            overall_status = ComplianceStatus.NON_COMPLIANT
        
        return ComplianceAssessment(
            id=assessment_id,
            framework="WASC",
            assessment_date=datetime.now(),
            assessor=context.get("assessor", "System"),
            overall_status=overall_status,
            overall_score=overall_score,
            standards_assessed=len(self.standards),
            standards_compliant=sum(1 for score in standard_scores.values() if score >= 65),
            findings=findings,
            next_assessment=datetime.now() + timedelta(days=1095)  # 3 years
        )
    
    async def _assess_standard(self, standard: ComplianceStandard, context: Dict[str, Any]) -> tuple[float, List[AuditFinding]]:
        """Assess a single WASC standard"""
        findings = []
        
        # Check evidence availability
        evidence = self.get_evidence(standard.id)
        evidence_score = min(len(evidence) * 20, 100) if evidence else 0
        
        # Mock compliance checking
        base_score = 70  # Base compliance score for WASC
        
        # Adjust score based on evidence quality
        verified_evidence = [e for e in evidence if e.verified]
        if len(verified_evidence) < len(evidence) * 0.5:
            findings.append(AuditFinding(
                id=f"finding_{standard.id}_verification_{datetime.now().strftime('%H%M%S')}",
                audit_id="system_assessment",
                standard_id=standard.id,
                severity=AuditSeverity.MEDIUM,
                title=f"Unverified evidence for {standard.name}",
                description="Significant amount of evidence lacks verification",
                recommendation="Have evidence reviewed and verified by appropriate personnel"
            ))
            base_score -= 10
        
        final_score = max(0, min(100, base_score + (evidence_score - 60) * 0.5))
        
        return final_score, findings

class ComplianceEngine:
    """Main compliance engine managing all governance frameworks"""
    
    def __init__(self):
        self.frameworks: Dict[str, GovernanceFramework] = {
            "aacsb": AACSBFramework(),
            "wasc": WASCFramework()
            # Additional frameworks can be added here
        }
        self.assessments: List[ComplianceAssessment] = []
        self.audit_schedule: Dict[str, datetime] = {}
    
    async def assess_framework(self, framework_name: str, context: Dict[str, Any]) -> ComplianceAssessment:
        """Assess compliance for a specific framework"""
        if framework_name not in self.frameworks:
            raise ValueError(f"Framework {framework_name} not supported")
        
        framework = self.frameworks[framework_name]
        assessment = await framework.assess_compliance(context)
        self.assessments.append(assessment)
        
        return assessment
    
    async def assess_all_frameworks(self, context: Dict[str, Any]) -> List[ComplianceAssessment]:
        """Assess compliance for all supported frameworks"""
        assessments = []
        
        for framework_name in self.frameworks.keys():
            try:
                assessment = await self.assess_framework(framework_name, context)
                assessments.append(assessment)
            except Exception as e:
                print(f"Error assessing {framework_name}: {e}")
        
        return assessments
    
    def add_evidence(self, framework_name: str, evidence: ComplianceEvidence) -> None:
        """Add evidence for a framework standard"""
        if framework_name in self.frameworks:
            self.frameworks[framework_name].add_evidence(evidence)
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get summary of all compliance assessments"""
        if not self.assessments:
            return {"status": "no_assessments", "frameworks": 0}
        
        recent_assessments = {}
        for assessment in self.assessments:
            if (assessment.framework not in recent_assessments or 
                assessment.assessment_date > recent_assessments[assessment.framework].assessment_date):
                recent_assessments[assessment.framework] = assessment
        
        summary = {
            "frameworks_assessed": len(recent_assessments),
            "overall_compliant": sum(1 for a in recent_assessments.values() 
                                   if a.overall_status == ComplianceStatus.COMPLIANT),
            "frameworks": {}
        }
        
        for framework, assessment in recent_assessments.items():
            summary["frameworks"][framework] = {
                "status": assessment.overall_status.value,
                "score": assessment.overall_score,
                "last_assessment": assessment.assessment_date.isoformat(),
                "findings": len(assessment.findings),
                "standards_compliant": assessment.standards_compliant,
                "standards_total": assessment.standards_assessed
            }
        
        return summary
    
    def schedule_audit(self, framework_name: str, audit_date: datetime) -> None:
        """Schedule an audit for a framework"""
        self.audit_schedule[framework_name] = audit_date
    
    def get_upcoming_audits(self, days_ahead: int = 30) -> Dict[str, datetime]:
        """Get audits scheduled in the next N days"""
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        return {framework: date for framework, date in self.audit_schedule.items() 
                if datetime.now() <= date <= cutoff_date}