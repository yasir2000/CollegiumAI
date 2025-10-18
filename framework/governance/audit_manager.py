"""
Audit Management System
======================

Comprehensive audit management for governance compliance including
audit planning, execution, tracking, and reporting.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json
import asyncio
from pathlib import Path

from .compliance_engine import AuditFinding, AuditSeverity, ComplianceStatus

class AuditType(Enum):
    """Types of audits"""
    INTERNAL = "internal"
    EXTERNAL = "external"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    OPERATIONAL = "operational"

class AuditStatus(Enum):
    """Audit execution status"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

@dataclass
class AuditScope:
    """Defines the scope of an audit"""
    frameworks: List[str]
    standards: List[str]
    departments: List[str]
    processes: List[str]
    date_range: Optional[Dict[str, datetime]] = None
    exclusions: List[str] = field(default_factory=list)

@dataclass
class AuditChecklistItem:
    """Individual item in an audit checklist"""
    id: str
    category: str
    description: str
    requirement: str
    evidence_required: List[str]
    completed: bool = False
    notes: Optional[str] = None
    completed_by: Optional[str] = None
    completed_date: Optional[datetime] = None

@dataclass
class AuditTeamMember:
    """Member of the audit team"""
    id: str
    name: str
    role: str
    email: str
    qualifications: List[str]
    responsibilities: List[str]
    available_from: datetime
    available_until: datetime

@dataclass
class Audit:
    """Complete audit definition and tracking"""
    id: str
    title: str
    type: AuditType
    status: AuditStatus
    scope: AuditScope
    lead_auditor: str
    team_members: List[AuditTeamMember]
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    checklist: List[AuditChecklistItem] = field(default_factory=list)
    findings: List[AuditFinding] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    report_path: Optional[str] = None
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    created_date: datetime = field(default_factory=datetime.now)
    created_by: str = "system"

@dataclass
class AuditPlan:
    """Annual audit planning and scheduling"""
    year: int
    audits: List[Audit]
    risk_assessment: Dict[str, str]
    resource_allocation: Dict[str, Any]
    compliance_calendar: Dict[str, List[datetime]]
    budget: Optional[float] = None
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None

class AuditManager:
    """Manages all audit activities and processes"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.audits: Dict[str, Audit] = {}
        self.audit_plans: Dict[int, AuditPlan] = {}
        self.templates: Dict[str, List[AuditChecklistItem]] = {}
        
        self._load_templates()
        self._load_audits()
    
    def _load_templates(self) -> None:
        """Load audit checklist templates"""
        self.templates = {
            "aacsb_compliance": [
                AuditChecklistItem(
                    id="aacsb_1_1",
                    category="Strategic Management",
                    description="Review mission statement alignment",
                    requirement="Mission statement clearly articulates institutional purpose",
                    evidence_required=["mission_statement", "strategic_plan", "stakeholder_input"]
                ),
                AuditChecklistItem(
                    id="aacsb_1_2", 
                    category="Strategic Management",
                    description="Assess strategic planning process",
                    requirement="Regular strategic planning with measurable objectives",
                    evidence_required=["strategic_plan", "planning_process", "progress_reports"]
                ),
                AuditChecklistItem(
                    id="aacsb_2_1",
                    category="Learning and Teaching",
                    description="Verify learning goals alignment",
                    requirement="Learning goals support mission and degree programs",
                    evidence_required=["learning_goals", "curriculum_maps", "assessment_data"]
                )
            ],
            "wasc_compliance": [
                AuditChecklistItem(
                    id="wasc_1_1",
                    category="Institutional Purpose",
                    description="Review institutional mission clarity",
                    requirement="Mission clearly defines institutional purpose",
                    evidence_required=["mission_statement", "purpose_documentation"]
                ),
                AuditChecklistItem(
                    id="wasc_2_1",
                    category="Educational Quality",
                    description="Assess learning outcome achievement",
                    requirement="Evidence of student learning outcome achievement",
                    evidence_required=["assessment_reports", "student_work", "outcome_data"]
                )
            ],
            "internal_systems": [
                AuditChecklistItem(
                    id="sys_1_1",
                    category="System Security",
                    description="Review access controls",
                    requirement="Appropriate user access controls implemented",
                    evidence_required=["access_logs", "user_permissions", "security_policies"]
                ),
                AuditChecklistItem(
                    id="sys_1_2",
                    category="Data Management",
                    description="Verify data backup procedures",
                    requirement="Regular data backups with tested recovery",
                    evidence_required=["backup_logs", "recovery_tests", "data_policies"]
                )
            ]
        }
    
    def _load_audits(self) -> None:
        """Load existing audits from storage"""
        audits_file = self.data_dir / "audits.json"
        if audits_file.exists():
            try:
                with open(audits_file, 'r') as f:
                    data = json.load(f)
                    # Convert JSON back to Audit objects (simplified)
                    for audit_data in data:
                        audit = self._deserialize_audit(audit_data)
                        self.audits[audit.id] = audit
            except Exception as e:
                print(f"Error loading audits: {e}")
    
    def _save_audits(self) -> None:
        """Save audits to storage"""
        audits_file = self.data_dir / "audits.json"
        try:
            audit_data = [self._serialize_audit(audit) for audit in self.audits.values()]
            with open(audits_file, 'w') as f:
                json.dump(audit_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving audits: {e}")
    
    def create_audit(self, 
                    title: str,
                    audit_type: AuditType,
                    scope: AuditScope,
                    lead_auditor: str,
                    planned_start: datetime,
                    planned_end: datetime,
                    template_name: Optional[str] = None) -> Audit:
        """Create a new audit"""
        
        audit_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Load checklist from template
        checklist = []
        if template_name and template_name in self.templates:
            checklist = self.templates[template_name].copy()
        
        audit = Audit(
            id=audit_id,
            title=title,
            type=audit_type,
            status=AuditStatus.PLANNED,
            scope=scope,
            lead_auditor=lead_auditor,
            team_members=[],
            planned_start=planned_start,
            planned_end=planned_end,
            checklist=checklist
        )
        
        self.audits[audit_id] = audit
        self._save_audits()
        
        return audit
    
    def add_team_member(self, audit_id: str, team_member: AuditTeamMember) -> None:
        """Add a team member to an audit"""
        if audit_id in self.audits:
            self.audits[audit_id].team_members.append(team_member)
            self._save_audits()
    
    def start_audit(self, audit_id: str) -> bool:
        """Start an audit execution"""
        if audit_id not in self.audits:
            return False
        
        audit = self.audits[audit_id]
        if audit.status != AuditStatus.PLANNED:
            return False
        
        audit.status = AuditStatus.IN_PROGRESS
        audit.actual_start = datetime.now()
        self._save_audits()
        
        return True
    
    def complete_checklist_item(self, 
                               audit_id: str, 
                               item_id: str, 
                               completed_by: str,
                               notes: Optional[str] = None) -> bool:
        """Mark a checklist item as completed"""
        if audit_id not in self.audits:
            return False
        
        audit = self.audits[audit_id]
        for item in audit.checklist:
            if item.id == item_id:
                item.completed = True
                item.completed_by = completed_by
                item.completed_date = datetime.now()
                item.notes = notes
                self._save_audits()
                return True
        
        return False
    
    def add_finding(self, audit_id: str, finding: AuditFinding) -> None:
        """Add a finding to an audit"""
        if audit_id in self.audits:
            finding.audit_id = audit_id
            self.audits[audit_id].findings.append(finding)
            self._save_audits()
    
    def complete_audit(self, audit_id: str, report_path: Optional[str] = None) -> bool:
        """Complete an audit"""
        if audit_id not in self.audits:
            return False
        
        audit = self.audits[audit_id]
        if audit.status != AuditStatus.IN_PROGRESS:
            return False
        
        audit.status = AuditStatus.COMPLETED
        audit.actual_end = datetime.now()
        audit.report_path = report_path
        
        # Determine if follow-up is required based on findings
        critical_findings = [f for f in audit.findings if f.severity == AuditSeverity.CRITICAL]
        high_findings = [f for f in audit.findings if f.severity == AuditSeverity.HIGH]
        
        if critical_findings or len(high_findings) > 2:
            audit.follow_up_required = True
            audit.follow_up_date = datetime.now() + timedelta(days=30)
        
        self._save_audits()
        
        return True
    
    def get_audit_progress(self, audit_id: str) -> Dict[str, Any]:
        """Get audit progress summary"""
        if audit_id not in self.audits:
            return {}
        
        audit = self.audits[audit_id]
        
        total_items = len(audit.checklist)
        completed_items = sum(1 for item in audit.checklist if item.completed)
        
        return {
            "audit_id": audit_id,
            "title": audit.title,
            "status": audit.status.value,
            "progress_percentage": (completed_items / total_items * 100) if total_items > 0 else 0,
            "checklist_completed": completed_items,
            "checklist_total": total_items,
            "findings_count": len(audit.findings),
            "critical_findings": len([f for f in audit.findings if f.severity == AuditSeverity.CRITICAL]),
            "days_remaining": (audit.planned_end - datetime.now()).days if audit.planned_end > datetime.now() else 0,
            "overdue": audit.planned_end < datetime.now() and audit.status != AuditStatus.COMPLETED
        }
    
    def generate_audit_report(self, audit_id: str) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        if audit_id not in self.audits:
            return {}
        
        audit = self.audits[audit_id]
        progress = self.get_audit_progress(audit_id)
        
        # Categorize findings by severity
        findings_by_severity = {}
        for severity in AuditSeverity:
            findings_by_severity[severity.value] = [
                f for f in audit.findings if f.severity == severity
            ]
        
        # Calculate compliance metrics
        total_standards = len(set(f.standard_id for f in audit.findings))
        non_compliant_standards = len(set(f.standard_id for f in audit.findings 
                                        if f.severity in [AuditSeverity.CRITICAL, AuditSeverity.HIGH]))
        
        compliance_rate = ((total_standards - non_compliant_standards) / total_standards * 100) if total_standards > 0 else 100
        
        return {
            "audit_info": {
                "id": audit.id,
                "title": audit.title,
                "type": audit.type.value,
                "scope": {
                    "frameworks": audit.scope.frameworks,
                    "standards": audit.scope.standards,
                    "departments": audit.scope.departments
                },
                "team": {
                    "lead_auditor": audit.lead_auditor,
                    "team_size": len(audit.team_members)
                },
                "timeline": {
                    "planned_start": audit.planned_start.isoformat(),
                    "planned_end": audit.planned_end.isoformat(),
                    "actual_start": audit.actual_start.isoformat() if audit.actual_start else None,
                    "actual_end": audit.actual_end.isoformat() if audit.actual_end else None
                }
            },
            "progress": progress,
            "findings": {
                "total": len(audit.findings),
                "by_severity": {k: len(v) for k, v in findings_by_severity.items()},
                "details": [self._serialize_finding(f) for f in audit.findings]
            },
            "compliance": {
                "standards_reviewed": total_standards,
                "non_compliant_standards": non_compliant_standards,
                "compliance_rate": compliance_rate
            },
            "recommendations": audit.recommendations,
            "follow_up": {
                "required": audit.follow_up_required,
                "date": audit.follow_up_date.isoformat() if audit.follow_up_date else None
            },
            "generated_date": datetime.now().isoformat()
        }
    
    def create_annual_plan(self, year: int, risk_assessment: Dict[str, str]) -> AuditPlan:
        """Create annual audit plan"""
        
        # Generate audit schedule based on risk assessment and compliance requirements
        audits = []
        
        # High-risk areas get quarterly audits
        high_risk_areas = [area for area, risk in risk_assessment.items() if risk == "high"]
        for area in high_risk_areas:
            for quarter in range(1, 5):
                start_date = datetime(year, (quarter - 1) * 3 + 1, 1)
                end_date = start_date + timedelta(days=30)
                
                audit = Audit(
                    id=f"audit_{year}_q{quarter}_{area.lower().replace(' ', '_')}",
                    title=f"Q{quarter} {area} Compliance Audit",
                    type=AuditType.COMPLIANCE,
                    status=AuditStatus.PLANNED,
                    scope=AuditScope(
                        frameworks=["aacsb", "wasc"],
                        standards=[],
                        departments=[area],
                        processes=[]
                    ),
                    lead_auditor="TBD",
                    team_members=[],
                    planned_start=start_date,
                    planned_end=end_date
                )
                audits.append(audit)
        
        # Medium-risk areas get semi-annual audits
        medium_risk_areas = [area for area, risk in risk_assessment.items() if risk == "medium"]
        for area in medium_risk_areas:
            for half in range(1, 3):
                start_date = datetime(year, (half - 1) * 6 + 1, 1)
                end_date = start_date + timedelta(days=45)
                
                audit = Audit(
                    id=f"audit_{year}_h{half}_{area.lower().replace(' ', '_')}",
                    title=f"H{half} {area} Review",
                    type=AuditType.INTERNAL,
                    status=AuditStatus.PLANNED,
                    scope=AuditScope(
                        frameworks=["aacsb", "wasc"],
                        standards=[],
                        departments=[area],
                        processes=[]
                    ),
                    lead_auditor="TBD",
                    team_members=[],
                    planned_start=start_date,
                    planned_end=end_date
                )
                audits.append(audit)
        
        plan = AuditPlan(
            year=year,
            audits=audits,
            risk_assessment=risk_assessment,
            resource_allocation={
                "internal_auditors": 3,
                "external_consultants": 1,
                "budget_hours": sum((audit.planned_end - audit.planned_start).days * 8 for audit in audits)
            },
            compliance_calendar={
                "aacsb": [datetime(year, 6, 1), datetime(year, 12, 1)],
                "wasc": [datetime(year, 3, 1), datetime(year, 9, 1)]
            }
        )
        
        self.audit_plans[year] = plan
        
        return plan
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get audit dashboard data"""
        current_audits = [a for a in self.audits.values() if a.status == AuditStatus.IN_PROGRESS]
        overdue_audits = [a for a in self.audits.values() 
                         if a.planned_end < datetime.now() and a.status != AuditStatus.COMPLETED]
        
        # Upcoming audits in next 30 days
        upcoming_audits = [a for a in self.audits.values() 
                          if a.status == AuditStatus.PLANNED and 
                          datetime.now() <= a.planned_start <= datetime.now() + timedelta(days=30)]
        
        # Recent findings (last 30 days)
        recent_findings = []
        for audit in self.audits.values():
            recent_findings.extend([f for f in audit.findings 
                                  if f.created_date >= datetime.now() - timedelta(days=30)])
        
        return {
            "current_audits": len(current_audits),
            "overdue_audits": len(overdue_audits),
            "upcoming_audits": len(upcoming_audits),
            "recent_findings": len(recent_findings),
            "critical_findings": len([f for f in recent_findings if f.severity == AuditSeverity.CRITICAL]),
            "audit_completion_rate": len([a for a in self.audits.values() if a.status == AuditStatus.COMPLETED]) / len(self.audits) * 100 if self.audits else 0,
            "average_audit_duration": self._calculate_average_duration(),
            "next_scheduled_audit": min([a.planned_start for a in upcoming_audits]) if upcoming_audits else None
        }
    
    def _calculate_average_duration(self) -> float:
        """Calculate average audit duration in days"""
        completed_audits = [a for a in self.audits.values() 
                           if a.status == AuditStatus.COMPLETED and a.actual_start and a.actual_end]
        
        if not completed_audits:
            return 0.0
        
        total_duration = sum((a.actual_end - a.actual_start).days for a in completed_audits)
        return total_duration / len(completed_audits)
    
    def _serialize_audit(self, audit: Audit) -> Dict[str, Any]:
        """Convert Audit object to JSON-serializable dict"""
        return {
            "id": audit.id,
            "title": audit.title,
            "type": audit.type.value,
            "status": audit.status.value,
            # Add other fields as needed
        }
    
    def _deserialize_audit(self, data: Dict[str, Any]) -> Audit:
        """Convert dict back to Audit object"""
        # Simplified deserialization - implement full conversion as needed
        return Audit(
            id=data["id"],
            title=data["title"],
            type=AuditType(data["type"]),
            status=AuditStatus(data["status"]),
            scope=AuditScope(frameworks=[], standards=[], departments=[], processes=[]),
            lead_auditor="",
            team_members=[],
            planned_start=datetime.now(),
            planned_end=datetime.now()
        )
    
    def _serialize_finding(self, finding: AuditFinding) -> Dict[str, Any]:
        """Convert AuditFinding to JSON-serializable dict"""
        return {
            "id": finding.id,
            "standard_id": finding.standard_id,
            "severity": finding.severity.value,
            "title": finding.title,
            "description": finding.description,
            "recommendation": finding.recommendation,
            "status": finding.status,
            "created_date": finding.created_date.isoformat()
        }