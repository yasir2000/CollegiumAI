"""
Governance Integration Module
============================

Integrated governance system that combines compliance monitoring,
audit management, policy control, and reporting into a unified platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import asyncio
from enum import Enum

from .compliance_engine import ComplianceEngine, ComplianceStandard, ComplianceEvidence
from .audit_manager import AuditManager, Audit, AuditStatus
from .policy_engine import PolicyEngine, Policy, PolicyStatus
from .reporting_dashboard import ReportingEngine, ReportType, DashboardWidget

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    URGENT = "urgent"

class MonitoringFrequency(Enum):
    """Monitoring frequency options"""
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class GovernanceAlert:
    """Governance compliance alert"""
    id: str
    level: AlertLevel
    title: str
    description: str
    source: str  # compliance, audit, policy
    created_date: datetime
    due_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GovernanceMetric:
    """Key governance performance metric"""
    name: str
    value: float
    unit: str
    target: Optional[float] = None
    trend: str = "stable"  # increasing, decreasing, stable
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class IntegrationConfig:
    """Configuration for governance integration"""
    auto_compliance_check: bool = True
    auto_audit_scheduling: bool = True
    auto_policy_reminders: bool = True
    notification_enabled: bool = True
    monitoring_frequency: MonitoringFrequency = MonitoringFrequency.DAILY
    alert_thresholds: Dict[str, float] = field(default_factory=dict)
    dashboard_refresh_interval: int = 300  # seconds

class GovernanceIntegration:
    """
    Integrated governance management system combining all components
    """
    
    def __init__(self, data_dir: Path, config: IntegrationConfig = None):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = config or IntegrationConfig()
        
        # Initialize core components
        self.compliance_engine = ComplianceEngine(data_dir / "compliance")
        self.audit_manager = AuditManager(data_dir / "audits")
        self.policy_engine = PolicyEngine(data_dir / "policies")
        self.reporting_engine = ReportingEngine(
            data_dir / "reports",
            compliance_engine=self.compliance_engine,
            audit_manager=self.audit_manager,
            policy_engine=self.policy_engine
        )
        
        # Integration state
        self.alerts: Dict[str, GovernanceAlert] = {}
        self.metrics: Dict[str, GovernanceMetric] = {}
        self.monitoring_tasks: Dict[str, Any] = {}
        
        # Load integration data
        self._load_alerts()
        self._load_metrics()
        
        # Start monitoring if configured
        if self.config.auto_compliance_check:
            self._start_monitoring()
    
    def _load_alerts(self) -> None:
        """Load saved alerts"""
        alerts_file = self.data_dir / "alerts.json"
        if alerts_file.exists():
            try:
                with open(alerts_file, 'r') as f:
                    data = json.load(f)
                    for alert_data in data:
                        alert = self._deserialize_alert(alert_data)
                        self.alerts[alert.id] = alert
            except Exception as e:
                print(f"Error loading alerts: {e}")
    
    def _save_alerts(self) -> None:
        """Save alerts to storage"""
        alerts_file = self.data_dir / "alerts.json"
        try:
            alert_data = [self._serialize_alert(alert) for alert in self.alerts.values()]
            with open(alerts_file, 'w') as f:
                json.dump(alert_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving alerts: {e}")
    
    def _load_metrics(self) -> None:
        """Load governance metrics"""
        metrics_file = self.data_dir / "metrics.json"
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    data = json.load(f)
                    for metric_data in data:
                        metric = self._deserialize_metric(metric_data)
                        self.metrics[metric.name] = metric
            except Exception as e:
                print(f"Error loading metrics: {e}")
    
    def _save_metrics(self) -> None:
        """Save metrics to storage"""
        metrics_file = self.data_dir / "metrics.json"
        try:
            metric_data = [self._serialize_metric(metric) for metric in self.metrics.values()]
            with open(metrics_file, 'w') as f:
                json.dump(metric_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def run_comprehensive_compliance_check(self, frameworks: List[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive compliance check across all frameworks
        """
        print("🔍 Running comprehensive compliance check...")
        
        results = {
            "timestamp": datetime.now(),
            "frameworks_checked": frameworks or ["aacsb", "wasc", "qaa", "hefce"],
            "compliance_results": {},
            "alerts_generated": [],
            "recommendations": [],
            "overall_score": 0
        }
        
        total_score = 0
        framework_count = 0
        
        # Check each framework
        for framework in results["frameworks_checked"]:
            try:
                compliance_result = self.compliance_engine.assess_compliance(framework)
                results["compliance_results"][framework] = compliance_result
                
                # Calculate score
                if compliance_result["findings"]:
                    framework_score = sum(f["score"] for f in compliance_result["findings"]) / len(compliance_result["findings"])
                    total_score += framework_score
                    framework_count += 1
                
                # Generate alerts for low scores
                if compliance_result.get("overall_score", 0) < 80:
                    alert = self._create_alert(
                        level=AlertLevel.WARNING if compliance_result["overall_score"] > 60 else AlertLevel.CRITICAL,
                        title=f"Low compliance score for {framework.upper()}",
                        description=f"Compliance score of {compliance_result['overall_score']}% is below threshold",
                        source="compliance",
                        metadata={"framework": framework, "score": compliance_result["overall_score"]}
                    )
                    results["alerts_generated"].append(alert.id)
                
            except Exception as e:
                print(f"Error checking {framework}: {e}")
                continue
        
        # Calculate overall score
        if framework_count > 0:
            results["overall_score"] = total_score / framework_count
        
        # Update metrics
        self._update_metric("overall_compliance_score", results["overall_score"], "%")
        
        # Generate recommendations
        results["recommendations"] = self._generate_compliance_recommendations(results["compliance_results"])
        
        print(f"✅ Compliance check complete. Overall score: {results['overall_score']:.1f}%")
        return results
    
    def schedule_automated_audits(self) -> Dict[str, Any]:
        """
        Schedule audits based on compliance results and policies
        """
        print("📋 Scheduling automated audits...")
        
        scheduling_result = {
            "timestamp": datetime.now(),
            "audits_scheduled": [],
            "next_audit_dates": {},
            "recommendations": []
        }
        
        # Get compliance results to identify areas needing audits
        compliance_check = self.run_comprehensive_compliance_check()
        
        for framework, result in compliance_check["compliance_results"].items():
            # Schedule audits for frameworks with low scores
            if result.get("overall_score", 100) < 85:
                audit_id = self.audit_manager.create_audit(
                    title=f"Compliance Audit - {framework.upper()}",
                    description=f"Focused audit based on low compliance score ({result['overall_score']}%)",
                    audit_type="compliance",
                    scope=f"Review {framework} compliance standards and evidence",
                    start_date=datetime.now() + timedelta(days=7),
                    end_date=datetime.now() + timedelta(days=21)
                )
                scheduling_result["audits_scheduled"].append(audit_id)
        
        # Schedule routine audits based on policy requirements
        for policy in self.policy_engine.policies.values():
            if policy.status == PolicyStatus.ACTIVE and policy.next_review_date:
                if policy.next_review_date <= datetime.now() + timedelta(days=30):
                    audit_id = self.audit_manager.create_audit(
                        title=f"Policy Review Audit - {policy.title}",
                        description=f"Scheduled review of policy: {policy.title}",
                        audit_type="policy_review",
                        scope=f"Review and validate policy {policy.id}",
                        start_date=policy.next_review_date - timedelta(days=7),
                        end_date=policy.next_review_date + timedelta(days=7)
                    )
                    scheduling_result["audits_scheduled"].append(audit_id)
        
        print(f"✅ Scheduled {len(scheduling_result['audits_scheduled'])} audits")
        return scheduling_result
    
    def generate_integrated_dashboard(self, dashboard_type: str = "executive") -> Dict[str, Any]:
        """
        Generate integrated governance dashboard
        """
        print(f"📊 Generating {dashboard_type} dashboard...")
        
        dashboard_data = self.reporting_engine.get_dashboard_data(dashboard_type)
        
        # Add integration-specific widgets
        integration_widgets = self._get_integration_widgets()
        dashboard_data["widgets"].extend(integration_widgets)
        
        # Add real-time metrics
        dashboard_data["metrics"] = {
            name: {
                "value": metric.value,
                "unit": metric.unit,
                "target": metric.target,
                "trend": metric.trend,
                "last_updated": metric.last_updated.isoformat()
            }
            for name, metric in self.metrics.items()
        }
        
        # Add alerts summary
        active_alerts = [a for a in self.alerts.values() if not a.resolved_date]
        dashboard_data["alerts"] = {
            "total": len(active_alerts),
            "critical": len([a for a in active_alerts if a.level == AlertLevel.CRITICAL]),
            "warning": len([a for a in active_alerts if a.level == AlertLevel.WARNING]),
            "recent": [self._serialize_alert(a) for a in sorted(active_alerts, key=lambda x: x.created_date, reverse=True)[:5]]
        }
        
        return dashboard_data
    
    def perform_policy_lifecycle_management(self) -> Dict[str, Any]:
        """
        Automated policy lifecycle management
        """
        print("📋 Performing policy lifecycle management...")
        
        management_result = {
            "timestamp": datetime.now(),
            "policies_reviewed": 0,
            "policies_updated": 0,
            "alerts_generated": [],
            "recommendations": []
        }
        
        # Check for policies due for review
        due_policies = self.policy_engine.get_policies_for_review()
        management_result["policies_reviewed"] = len(due_policies)
        
        for policy in due_policies:
            # Generate alert for overdue policy
            alert = self._create_alert(
                level=AlertLevel.WARNING,
                title=f"Policy Review Due: {policy.title}",
                description=f"Policy {policy.id} is due for review",
                source="policy",
                due_date=policy.next_review_date,
                metadata={"policy_id": policy.id, "policy_title": policy.title}
            )
            management_result["alerts_generated"].append(alert.id)
        
        # Auto-update policy review dates for active policies
        for policy in self.policy_engine.policies.values():
            if policy.status == PolicyStatus.ACTIVE and not policy.next_review_date:
                policy.next_review_date = datetime.now() + timedelta(days=policy.review_frequency)
                management_result["policies_updated"] += 1
        
        print(f"✅ Policy lifecycle management complete. Reviewed {management_result['policies_reviewed']} policies")
        return management_result
    
    def generate_compliance_report(self, 
                                 report_type: str = "comprehensive",
                                 period_days: int = 30,
                                 frameworks: List[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report
        """
        print(f"📄 Generating {report_type} compliance report...")
        
        period_start = datetime.now() - timedelta(days=period_days)
        period_end = datetime.now()
        
        if report_type == "comprehensive":
            report = self.reporting_engine.generate_compliance_status_report(
                period_start=period_start,
                period_end=period_end,
                frameworks=frameworks
            )
        elif report_type == "audit":
            report = self.reporting_engine.generate_audit_summary_report()
        elif report_type == "policy":
            report = self.reporting_engine.generate_policy_overview_report()
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Add integration insights
        report.content["integration_insights"] = {
            "active_alerts": len([a for a in self.alerts.values() if not a.resolved_date]),
            "governance_score": self.metrics.get("overall_compliance_score", GovernanceMetric("overall_compliance_score", 0, "%")).value,
            "system_health": self._assess_system_health()
        }
        
        print(f"✅ Report generated: {report.id}")
        return {
            "report_id": report.id,
            "report": report,
            "export_formats": ["json", "html", "pdf"]
        }
    
    def get_governance_health_status(self) -> Dict[str, Any]:
        """
        Get overall governance health status
        """
        active_alerts = [a for a in self.alerts.values() if not a.resolved_date]
        critical_alerts = [a for a in active_alerts if a.level == AlertLevel.CRITICAL]
        
        # Calculate health score
        base_score = 100
        base_score -= len(critical_alerts) * 10  # -10 for each critical alert
        base_score -= len([a for a in active_alerts if a.level == AlertLevel.WARNING]) * 5  # -5 for warnings
        
        # Factor in compliance score
        compliance_score = self.metrics.get("overall_compliance_score", GovernanceMetric("overall_compliance_score", 85, "%")).value
        health_score = (base_score + compliance_score) / 2
        
        status = "excellent" if health_score >= 90 else "good" if health_score >= 80 else "fair" if health_score >= 70 else "poor"
        
        return {
            "health_score": max(0, min(100, health_score)),
            "status": status,
            "active_alerts": len(active_alerts),
            "critical_issues": len(critical_alerts),
            "compliance_score": compliance_score,
            "last_assessment": datetime.now(),
            "recommendations": self._get_health_recommendations(health_score, active_alerts)
        }
    
    def _create_alert(self, 
                     level: AlertLevel,
                     title: str,
                     description: str,
                     source: str,
                     due_date: datetime = None,
                     metadata: Dict[str, Any] = None) -> GovernanceAlert:
        """Create and store a new governance alert"""
        
        alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        alert = GovernanceAlert(
            id=alert_id,
            level=level,
            title=title,
            description=description,
            source=source,
            created_date=datetime.now(),
            due_date=due_date,
            metadata=metadata or {}
        )
        
        self.alerts[alert_id] = alert
        self._save_alerts()
        
        return alert
    
    def resolve_alert(self, alert_id: str, resolved_by: str = None) -> bool:
        """Resolve a governance alert"""
        if alert_id not in self.alerts:
            return False
        
        alert = self.alerts[alert_id]
        alert.resolved_date = datetime.now()
        if resolved_by:
            alert.metadata["resolved_by"] = resolved_by
        
        self._save_alerts()
        return True
    
    def _update_metric(self, name: str, value: float, unit: str, target: float = None) -> None:
        """Update or create a governance metric"""
        
        # Calculate trend if metric exists
        trend = "stable"
        if name in self.metrics:
            old_value = self.metrics[name].value
            if value > old_value * 1.05:
                trend = "increasing"
            elif value < old_value * 0.95:
                trend = "decreasing"
        
        metric = GovernanceMetric(
            name=name,
            value=value,
            unit=unit,
            target=target,
            trend=trend,
            last_updated=datetime.now()
        )
        
        self.metrics[name] = metric
        self._save_metrics()
    
    def _start_monitoring(self) -> None:
        """Start automated monitoring tasks"""
        print("🔄 Starting governance monitoring...")
        
        # This would typically use asyncio or background tasks
        # Simplified implementation for demonstration
        pass
    
    def _get_integration_widgets(self) -> List[Dict[str, Any]]:
        """Get integration-specific dashboard widgets"""
        return [
            {
                "id": "governance_health",
                "title": "Governance Health",
                "type": "metric",
                "position": (0, 3),
                "size": (1, 1),
                "data": self.get_governance_health_status()
            },
            {
                "id": "active_alerts",
                "title": "Active Alerts",
                "type": "alert_list",
                "position": (1, 3),
                "size": (2, 1),
                "data": {
                    "alerts": [self._serialize_alert(a) for a in self.alerts.values() if not a.resolved_date]
                }
            }
        ]
    
    def _assess_system_health(self) -> str:
        """Assess overall system health"""
        health_status = self.get_governance_health_status()
        return health_status["status"]
    
    def _generate_compliance_recommendations(self, compliance_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on compliance results"""
        recommendations = []
        
        for framework, result in compliance_results.items():
            if result.get("overall_score", 100) < 80:
                recommendations.append(f"Improve {framework.upper()} compliance through targeted policy updates")
            
            if result.get("findings"):
                low_scoring = [f for f in result["findings"] if f.get("score", 100) < 70]
                if low_scoring:
                    recommendations.append(f"Address low-scoring standards in {framework.upper()}: {[f['standard'].name for f in low_scoring]}")
        
        return recommendations
    
    def _get_health_recommendations(self, health_score: float, active_alerts: List[GovernanceAlert]) -> List[str]:
        """Get recommendations for improving governance health"""
        recommendations = []
        
        if health_score < 80:
            recommendations.append("Schedule comprehensive compliance review")
        
        if len(active_alerts) > 5:
            recommendations.append("Prioritize resolution of active alerts")
        
        critical_alerts = [a for a in active_alerts if a.level == AlertLevel.CRITICAL]
        if critical_alerts:
            recommendations.append(f"Immediately address {len(critical_alerts)} critical issues")
        
        return recommendations
    
    def _serialize_alert(self, alert: GovernanceAlert) -> Dict[str, Any]:
        """Convert alert to JSON-serializable format"""
        return {
            "id": alert.id,
            "level": alert.level.value,
            "title": alert.title,
            "description": alert.description,
            "source": alert.source,
            "created_date": alert.created_date.isoformat(),
            "due_date": alert.due_date.isoformat() if alert.due_date else None,
            "resolved_date": alert.resolved_date.isoformat() if alert.resolved_date else None,
            "assigned_to": alert.assigned_to,
            "metadata": alert.metadata
        }
    
    def _deserialize_alert(self, data: Dict[str, Any]) -> GovernanceAlert:
        """Convert dict back to alert object"""
        return GovernanceAlert(
            id=data["id"],
            level=AlertLevel(data["level"]),
            title=data["title"],
            description=data["description"],
            source=data["source"],
            created_date=datetime.fromisoformat(data["created_date"]),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            resolved_date=datetime.fromisoformat(data["resolved_date"]) if data.get("resolved_date") else None,
            assigned_to=data.get("assigned_to"),
            metadata=data.get("metadata", {})
        )
    
    def _serialize_metric(self, metric: GovernanceMetric) -> Dict[str, Any]:
        """Convert metric to JSON-serializable format"""
        return {
            "name": metric.name,
            "value": metric.value,
            "unit": metric.unit,
            "target": metric.target,
            "trend": metric.trend,
            "last_updated": metric.last_updated.isoformat()
        }
    
    def _deserialize_metric(self, data: Dict[str, Any]) -> GovernanceMetric:
        """Convert dict back to metric object"""
        return GovernanceMetric(
            name=data["name"],
            value=data["value"],
            unit=data["unit"],
            target=data.get("target"),
            trend=data.get("trend", "stable"),
            last_updated=datetime.fromisoformat(data["last_updated"])
        )