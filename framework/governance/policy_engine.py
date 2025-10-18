"""
Policy Management System
=======================

Comprehensive policy management for governance compliance including
policy creation, versioning, approval workflows, and automated enforcement.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json
import re
from pathlib import Path

class PolicyStatus(Enum):
    """Policy lifecycle status"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class PolicyType(Enum):
    """Types of policies"""
    GOVERNANCE = "governance"
    ACADEMIC = "academic"
    ADMINISTRATIVE = "administrative"
    TECHNICAL = "technical"
    COMPLIANCE = "compliance"
    SECURITY = "security"

class ApprovalLevel(Enum):
    """Policy approval levels"""
    DEPARTMENT = "department"
    FACULTY = "faculty"
    ADMINISTRATION = "administration"
    BOARD = "board"

@dataclass
class PolicySection:
    """Section within a policy document"""
    id: str
    title: str
    content: str
    order: int
    subsections: List['PolicySection'] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    compliance_frameworks: List[str] = field(default_factory=list)

@dataclass
class PolicyApproval:
    """Policy approval record"""
    approver_id: str
    approver_name: str
    approval_level: ApprovalLevel
    approved_date: datetime
    comments: Optional[str] = None
    conditions: List[str] = field(default_factory=list)

@dataclass
class PolicyReview:
    """Policy review record"""
    reviewer_id: str
    reviewer_name: str
    review_date: datetime
    status: str  # "approved", "needs_revision", "rejected"
    comments: str
    suggestions: List[str] = field(default_factory=list)

@dataclass
class PolicyVersion:
    """Version of a policy document"""
    version: str
    content: str
    sections: List[PolicySection]
    created_date: datetime
    created_by: str
    change_summary: str
    approved_by: List[PolicyApproval] = field(default_factory=list)
    reviewed_by: List[PolicyReview] = field(default_factory=list)

@dataclass
class Policy:
    """Complete policy document with versioning"""
    id: str
    title: str
    type: PolicyType
    status: PolicyStatus
    description: str
    owner: str
    current_version: str
    versions: Dict[str, PolicyVersion]
    created_date: datetime
    last_modified: datetime
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    review_frequency: int = 365  # days
    next_review_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    compliance_frameworks: List[str] = field(default_factory=list)
    related_policies: List[str] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)

@dataclass
class PolicyTemplate:
    """Template for creating new policies"""
    id: str
    name: str
    type: PolicyType
    description: str
    sections: List[PolicySection]
    required_approvals: List[ApprovalLevel]
    compliance_frameworks: List[str]
    stakeholder_groups: List[str]

class PolicyEngine:
    """Core policy management engine"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.policies: Dict[str, Policy] = {}
        self.templates: Dict[str, PolicyTemplate] = {}
        self.approval_workflows: Dict[str, List[ApprovalLevel]] = {}
        
        self._load_templates()
        self._load_policies()
        self._setup_workflows()
    
    def _load_templates(self) -> None:
        """Load policy templates"""
        self.templates = {
            "aacsb_governance": PolicyTemplate(
                id="aacsb_governance",
                name="AACSB Governance Policy Template",
                type=PolicyType.GOVERNANCE,
                description="Template for AACSB governance compliance policies",
                sections=[
                    PolicySection(
                        id="purpose",
                        title="Purpose and Scope",
                        content="This policy establishes governance frameworks in accordance with AACSB standards...",
                        order=1,
                        compliance_frameworks=["aacsb"]
                    ),
                    PolicySection(
                        id="governance_structure",
                        title="Governance Structure",
                        content="The institution maintains a governance structure that...",
                        order=2,
                        requirements=[
                            "Clear governance hierarchy",
                            "Defined roles and responsibilities",
                            "Regular governance reviews"
                        ],
                        compliance_frameworks=["aacsb"]
                    ),
                    PolicySection(
                        id="strategic_planning",
                        title="Strategic Planning Process",
                        content="Strategic planning follows a systematic process that...",
                        order=3,
                        requirements=[
                            "Annual strategic planning cycle",
                            "Stakeholder engagement",
                            "Performance measurement"
                        ],
                        compliance_frameworks=["aacsb"]
                    )
                ],
                required_approvals=[ApprovalLevel.ADMINISTRATION, ApprovalLevel.BOARD],
                compliance_frameworks=["aacsb"],
                stakeholder_groups=["faculty", "administration", "board"]
            ),
            "wasc_quality": PolicyTemplate(
                id="wasc_quality",
                name="WASC Quality Assurance Policy Template",
                type=PolicyType.ACADEMIC,
                description="Template for WASC quality assurance policies",
                sections=[
                    PolicySection(
                        id="quality_framework",
                        title="Quality Assurance Framework",
                        content="The institution maintains a comprehensive quality assurance framework...",
                        order=1,
                        compliance_frameworks=["wasc"]
                    ),
                    PolicySection(
                        id="assessment_procedures",
                        title="Assessment Procedures",
                        content="Assessment procedures ensure systematic evaluation of...",
                        order=2,
                        requirements=[
                            "Regular assessment cycles",
                            "Multiple assessment methods",
                            "Stakeholder involvement"
                        ],
                        compliance_frameworks=["wasc"]
                    )
                ],
                required_approvals=[ApprovalLevel.FACULTY, ApprovalLevel.ADMINISTRATION],
                compliance_frameworks=["wasc"],
                stakeholder_groups=["faculty", "students", "administration"]
            )
        }
    
    def _load_policies(self) -> None:
        """Load existing policies from storage"""
        policies_file = self.data_dir / "policies.json"
        if policies_file.exists():
            try:
                with open(policies_file, 'r') as f:
                    data = json.load(f)
                    for policy_data in data:
                        policy = self._deserialize_policy(policy_data)
                        self.policies[policy.id] = policy
            except Exception as e:
                print(f"Error loading policies: {e}")
    
    def _save_policies(self) -> None:
        """Save policies to storage"""
        policies_file = self.data_dir / "policies.json"
        try:
            policy_data = [self._serialize_policy(policy) for policy in self.policies.values()]
            with open(policies_file, 'w') as f:
                json.dump(policy_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving policies: {e}")
    
    def _setup_workflows(self) -> None:
        """Setup approval workflows for different policy types"""
        self.approval_workflows = {
            PolicyType.GOVERNANCE.value: [ApprovalLevel.ADMINISTRATION, ApprovalLevel.BOARD],
            PolicyType.ACADEMIC.value: [ApprovalLevel.FACULTY, ApprovalLevel.ADMINISTRATION],
            PolicyType.ADMINISTRATIVE.value: [ApprovalLevel.ADMINISTRATION],
            PolicyType.TECHNICAL.value: [ApprovalLevel.DEPARTMENT, ApprovalLevel.ADMINISTRATION],
            PolicyType.COMPLIANCE.value: [ApprovalLevel.ADMINISTRATION, ApprovalLevel.BOARD],
            PolicyType.SECURITY.value: [ApprovalLevel.DEPARTMENT, ApprovalLevel.ADMINISTRATION]
        }
    
    def create_policy_from_template(self, 
                                   template_id: str,
                                   title: str,
                                   owner: str,
                                   description: str,
                                   customizations: Dict[str, Any] = None) -> Policy:
        """Create a new policy from a template"""
        
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]
        policy_id = f"policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create initial version
        initial_version = PolicyVersion(
            version="1.0",
            content=self._generate_policy_content(template, customizations or {}),
            sections=template.sections.copy(),
            created_date=datetime.now(),
            created_by=owner,
            change_summary="Initial policy creation from template"
        )
        
        policy = Policy(
            id=policy_id,
            title=title,
            type=template.type,
            status=PolicyStatus.DRAFT,
            description=description,
            owner=owner,
            current_version="1.0",
            versions={"1.0": initial_version},
            created_date=datetime.now(),
            last_modified=datetime.now(),
            compliance_frameworks=template.compliance_frameworks.copy(),
            stakeholders=template.stakeholder_groups.copy()
        )
        
        # Set review schedule
        policy.next_review_date = datetime.now() + timedelta(days=policy.review_frequency)
        
        self.policies[policy_id] = policy
        self._save_policies()
        
        return policy
    
    def _generate_policy_content(self, template: PolicyTemplate, customizations: Dict[str, Any]) -> str:
        """Generate policy content from template with customizations"""
        content = f"# {customizations.get('title', 'Policy Title')}\n\n"
        content += f"**Policy Type:** {template.type.value.title()}\n"
        content += f"**Effective Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
        content += f"**Owner:** {customizations.get('owner', 'TBD')}\n\n"
        
        for section in template.sections:
            content += f"## {section.title}\n\n"
            content += f"{section.content}\n\n"
            
            if section.requirements:
                content += "### Requirements:\n"
                for req in section.requirements:
                    content += f"- {req}\n"
                content += "\n"
        
        content += "## Compliance\n\n"
        content += f"This policy ensures compliance with: {', '.join(template.compliance_frameworks)}\n\n"
        
        content += "## Review and Updates\n\n"
        content += f"This policy will be reviewed annually or as needed to ensure continued compliance and effectiveness.\n\n"
        
        return content
    
    def submit_for_review(self, policy_id: str, reviewer_id: str) -> bool:
        """Submit policy for review"""
        if policy_id not in self.policies:
            return False
        
        policy = self.policies[policy_id]
        if policy.status != PolicyStatus.DRAFT:
            return False
        
        policy.status = PolicyStatus.REVIEW
        policy.last_modified = datetime.now()
        self._save_policies()
        
        return True
    
    def add_review(self, policy_id: str, review: PolicyReview) -> bool:
        """Add a review to a policy"""
        if policy_id not in self.policies:
            return False
        
        policy = self.policies[policy_id]
        current_version = policy.versions[policy.current_version]
        current_version.reviewed_by.append(review)
        
        self._save_policies()
        return True
    
    def approve_policy(self, policy_id: str, approval: PolicyApproval) -> bool:
        """Add approval to a policy"""
        if policy_id not in self.policies:
            return False
        
        policy = self.policies[policy_id]
        current_version = policy.versions[policy.current_version]
        current_version.approved_by.append(approval)
        
        # Check if all required approvals are received
        required_levels = self.approval_workflows.get(policy.type.value, [])
        approved_levels = [a.approval_level for a in current_version.approved_by]
        
        if all(level in approved_levels for level in required_levels):
            policy.status = PolicyStatus.APPROVED
            policy.effective_date = datetime.now()
        
        self._save_policies()
        return True
    
    def activate_policy(self, policy_id: str) -> bool:
        """Activate an approved policy"""
        if policy_id not in self.policies:
            return False
        
        policy = self.policies[policy_id]
        if policy.status != PolicyStatus.APPROVED:
            return False
        
        policy.status = PolicyStatus.ACTIVE
        if not policy.effective_date:
            policy.effective_date = datetime.now()
        
        self._save_policies()
        return True
    
    def create_new_version(self, policy_id: str, change_summary: str, created_by: str) -> str:
        """Create a new version of a policy"""
        if policy_id not in self.policies:
            raise ValueError(f"Policy {policy_id} not found")
        
        policy = self.policies[policy_id]
        current_version_num = float(policy.current_version)
        new_version_num = f"{current_version_num + 0.1:.1f}"
        
        # Copy current version as base for new version
        current_version = policy.versions[policy.current_version]
        new_version = PolicyVersion(
            version=new_version_num,
            content=current_version.content,
            sections=current_version.sections.copy(),
            created_date=datetime.now(),
            created_by=created_by,
            change_summary=change_summary
        )
        
        policy.versions[new_version_num] = new_version
        policy.current_version = new_version_num
        policy.status = PolicyStatus.DRAFT
        policy.last_modified = datetime.now()
        
        self._save_policies()
        return new_version_num
    
    def get_policies_for_review(self) -> List[Policy]:
        """Get policies due for review"""
        due_for_review = []
        current_date = datetime.now()
        
        for policy in self.policies.values():
            if (policy.next_review_date and 
                policy.next_review_date <= current_date and 
                policy.status == PolicyStatus.ACTIVE):
                due_for_review.append(policy)
        
        return due_for_review
    
    def search_policies(self, query: str, filters: Dict[str, Any] = None) -> List[Policy]:
        """Search policies by content and metadata"""
        results = []
        query_lower = query.lower()
        
        for policy in self.policies.values():
            # Apply filters
            if filters:
                if 'type' in filters and policy.type.value != filters['type']:
                    continue
                if 'status' in filters and policy.status.value != filters['status']:
                    continue
                if 'framework' in filters and filters['framework'] not in policy.compliance_frameworks:
                    continue
            
            # Text search
            if (query_lower in policy.title.lower() or 
                query_lower in policy.description.lower() or
                any(query_lower in tag.lower() for tag in policy.tags)):
                results.append(policy)
                continue
            
            # Search in current version content
            current_version = policy.versions[policy.current_version]
            if query_lower in current_version.content.lower():
                results.append(policy)
        
        return results
    
    def get_compliance_report(self, framework: str) -> Dict[str, Any]:
        """Generate compliance report for a specific framework"""
        framework_policies = [p for p in self.policies.values() 
                            if framework in p.compliance_frameworks]
        
        active_policies = [p for p in framework_policies if p.status == PolicyStatus.ACTIVE]
        draft_policies = [p for p in framework_policies if p.status == PolicyStatus.DRAFT]
        expired_policies = [p for p in framework_policies 
                          if p.expiry_date and p.expiry_date < datetime.now()]
        
        due_for_review = [p for p in active_policies 
                         if p.next_review_date and p.next_review_date <= datetime.now()]
        
        return {
            "framework": framework,
            "total_policies": len(framework_policies),
            "active_policies": len(active_policies),
            "draft_policies": len(draft_policies),
            "expired_policies": len(expired_policies),
            "due_for_review": len(due_for_review),
            "coverage_percentage": (len(active_policies) / len(framework_policies) * 100) if framework_policies else 0,
            "policies": [self._policy_summary(p) for p in framework_policies]
        }
    
    def get_policy_analytics(self) -> Dict[str, Any]:
        """Get policy management analytics"""
        total_policies = len(self.policies)
        
        status_counts = {}
        type_counts = {}
        
        for policy in self.policies.values():
            status_counts[policy.status.value] = status_counts.get(policy.status.value, 0) + 1
            type_counts[policy.type.value] = type_counts.get(policy.type.value, 0) + 1
        
        # Calculate average review cycle
        active_policies = [p for p in self.policies.values() if p.status == PolicyStatus.ACTIVE]
        avg_review_frequency = sum(p.review_frequency for p in active_policies) / len(active_policies) if active_policies else 0
        
        # Policies by creation year
        creation_years = {}
        for policy in self.policies.values():
            year = policy.created_date.year
            creation_years[year] = creation_years.get(year, 0) + 1
        
        return {
            "total_policies": total_policies,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "average_review_frequency_days": avg_review_frequency,
            "policies_by_year": creation_years,
            "frameworks_covered": list(set(fw for p in self.policies.values() for fw in p.compliance_frameworks)),
            "templates_available": len(self.templates)
        }
    
    def _policy_summary(self, policy: Policy) -> Dict[str, Any]:
        """Create summary of policy for reports"""
        return {
            "id": policy.id,
            "title": policy.title,
            "type": policy.type.value,
            "status": policy.status.value,
            "owner": policy.owner,
            "version": policy.current_version,
            "effective_date": policy.effective_date.isoformat() if policy.effective_date else None,
            "next_review": policy.next_review_date.isoformat() if policy.next_review_date else None,
            "compliance_frameworks": policy.compliance_frameworks
        }
    
    def _serialize_policy(self, policy: Policy) -> Dict[str, Any]:
        """Convert Policy object to JSON-serializable dict"""
        return {
            "id": policy.id,
            "title": policy.title,
            "type": policy.type.value,
            "status": policy.status.value,
            "description": policy.description,
            "owner": policy.owner,
            "current_version": policy.current_version,
            "created_date": policy.created_date.isoformat(),
            "last_modified": policy.last_modified.isoformat(),
            "effective_date": policy.effective_date.isoformat() if policy.effective_date else None,
            "compliance_frameworks": policy.compliance_frameworks,
            "tags": policy.tags
        }
    
    def _deserialize_policy(self, data: Dict[str, Any]) -> Policy:
        """Convert dict back to Policy object"""
        # Simplified deserialization - implement full conversion as needed
        return Policy(
            id=data["id"],
            title=data["title"],
            type=PolicyType(data["type"]),
            status=PolicyStatus(data["status"]),
            description=data["description"],
            owner=data["owner"],
            current_version=data["current_version"],
            versions={},  # Would need to deserialize versions
            created_date=datetime.fromisoformat(data["created_date"]),
            last_modified=datetime.fromisoformat(data["last_modified"]),
            effective_date=datetime.fromisoformat(data["effective_date"]) if data.get("effective_date") else None,
            compliance_frameworks=data.get("compliance_frameworks", []),
            tags=data.get("tags", [])
        )