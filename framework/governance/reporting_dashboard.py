"""
Governance Reporting Dashboard
=============================

Comprehensive reporting system for governance compliance with
visual dashboards, metrics tracking, and automated report generation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json
from pathlib import Path
import base64
from io import BytesIO

class ReportType(Enum):
    """Types of compliance reports"""
    COMPLIANCE_STATUS = "compliance_status"
    AUDIT_SUMMARY = "audit_summary"
    POLICY_OVERVIEW = "policy_overview"
    RISK_ASSESSMENT = "risk_assessment"
    PERFORMANCE_METRICS = "performance_metrics"
    STAKEHOLDER_REPORT = "stakeholder_report"

class ReportFormat(Enum):
    """Report output formats"""
    JSON = "json"
    HTML = "html"
    PDF = "pdf"
    CSV = "csv"
    DASHBOARD = "dashboard"

class ChartType(Enum):
    """Chart types for visualizations"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    DONUT = "donut"
    GAUGE = "gauge"
    HEATMAP = "heatmap"
    TIMELINE = "timeline"

@dataclass
class MetricValue:
    """Individual metric value with metadata"""
    value: Any
    timestamp: datetime
    unit: Optional[str] = None
    target: Optional[Any] = None
    threshold_low: Optional[Any] = None
    threshold_high: Optional[Any] = None
    status: str = "normal"  # normal, warning, critical
    trend: str = "stable"   # increasing, decreasing, stable

@dataclass
class ChartData:
    """Data structure for chart visualizations"""
    type: ChartType
    title: str
    data: Dict[str, Any]
    labels: List[str] = field(default_factory=list)
    colors: List[str] = field(default_factory=list)
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class DashboardWidget:
    """Individual dashboard widget"""
    id: str
    title: str
    type: str  # metric, chart, table, alert
    position: Tuple[int, int]  # (row, col)
    size: Tuple[int, int]      # (height, width)
    data: Any
    config: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class Report:
    """Generated compliance report"""
    id: str
    type: ReportType
    title: str
    generated_date: datetime
    generated_by: str
    period_start: datetime
    period_end: datetime
    format: ReportFormat
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    recipients: List[str] = field(default_factory=list)

class ReportingEngine:
    """Core reporting and dashboard engine"""
    
    def __init__(self, data_dir: Path, compliance_engine=None, audit_manager=None, policy_engine=None):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.compliance_engine = compliance_engine
        self.audit_manager = audit_manager
        self.policy_engine = policy_engine
        
        self.reports: Dict[str, Report] = {}
        self.dashboards: Dict[str, List[DashboardWidget]] = {}
        self.metrics_history: Dict[str, List[MetricValue]] = {}
        
        self._load_reports()
        self._setup_default_dashboards()
    
    def _load_reports(self) -> None:
        """Load saved reports"""
        reports_file = self.data_dir / "reports.json"
        if reports_file.exists():
            try:
                with open(reports_file, 'r') as f:
                    data = json.load(f)
                    for report_data in data:
                        report = self._deserialize_report(report_data)
                        self.reports[report.id] = report
            except Exception as e:
                print(f"Error loading reports: {e}")
    
    def _save_reports(self) -> None:
        """Save reports to storage"""
        reports_file = self.data_dir / "reports.json"
        try:
            report_data = [self._serialize_report(report) for report in self.reports.values()]
            with open(reports_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving reports: {e}")
    
    def _setup_default_dashboards(self) -> None:
        """Setup default dashboard layouts"""
        
        # Executive Dashboard
        self.dashboards["executive"] = [
            DashboardWidget(
                id="compliance_overview",
                title="Compliance Overview",
                type="metric",
                position=(0, 0),
                size=(1, 2),
                data={"value": "85%", "trend": "up", "status": "good"}
            ),
            DashboardWidget(
                id="active_audits",
                title="Active Audits",
                type="metric", 
                position=(0, 2),
                size=(1, 1),
                data={"value": 3, "trend": "stable"}
            ),
            DashboardWidget(
                id="policy_status",
                title="Policy Status",
                type="chart",
                position=(1, 0),
                size=(2, 2),
                data={}
            ),
            DashboardWidget(
                id="compliance_trends",
                title="Compliance Trends",
                type="chart",
                position=(1, 2),
                size=(2, 2),
                data={}
            ),
            DashboardWidget(
                id="recent_findings",
                title="Recent Findings",
                type="table",
                position=(3, 0),
                size=(2, 4),
                data={}
            )
        ]
        
        # Operational Dashboard
        self.dashboards["operational"] = [
            DashboardWidget(
                id="audit_pipeline",
                title="Audit Pipeline",
                type="chart",
                position=(0, 0),
                size=(2, 2),
                data={}
            ),
            DashboardWidget(
                id="policy_reviews",
                title="Policy Reviews Due",
                type="table",
                position=(0, 2),
                size=(2, 2),
                data={}
            ),
            DashboardWidget(
                id="compliance_heatmap",
                title="Compliance Heatmap",
                type="chart",
                position=(2, 0),
                size=(2, 4),
                data={}
            )
        ]
    
    def generate_compliance_status_report(self,
                                        period_start: datetime,
                                        period_end: datetime,
                                        frameworks: List[str] = None) -> Report:
        """Generate comprehensive compliance status report"""
        
        report_id = f"compliance_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        content = {
            "executive_summary": self._generate_executive_summary(frameworks),
            "compliance_metrics": self._generate_compliance_metrics(frameworks),
            "framework_analysis": {},
            "risk_areas": self._identify_risk_areas(frameworks),
            "recommendations": self._generate_recommendations(frameworks),
            "charts": []
        }
        
        # Framework-specific analysis
        if frameworks:
            for framework in frameworks:
                content["framework_analysis"][framework] = self._analyze_framework_compliance(framework)
        
        # Generate visualizations
        content["charts"] = [
            self._create_compliance_overview_chart(frameworks),
            self._create_trend_analysis_chart(frameworks, period_start, period_end),
            self._create_framework_comparison_chart(frameworks)
        ]
        
        report = Report(
            id=report_id,
            type=ReportType.COMPLIANCE_STATUS,
            title="Compliance Status Report",
            generated_date=datetime.now(),
            generated_by="system",
            period_start=period_start,
            period_end=period_end,
            format=ReportFormat.JSON,
            content=content,
            metadata={
                "frameworks_included": frameworks or [],
                "data_sources": ["compliance_engine", "audit_manager", "policy_engine"]
            }
        )
        
        self.reports[report_id] = report
        self._save_reports()
        
        return report
    
    def generate_audit_summary_report(self, audit_ids: List[str] = None) -> Report:
        """Generate audit summary report"""
        
        report_id = f"audit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not self.audit_manager:
            raise ValueError("Audit manager not available")
        
        # Get audit data
        if audit_ids:
            audits = [self.audit_manager.audits.get(aid) for aid in audit_ids if aid in self.audit_manager.audits]
        else:
            audits = list(self.audit_manager.audits.values())
        
        content = {
            "summary": {
                "total_audits": len(audits),
                "completed_audits": len([a for a in audits if a.status == "completed"]),
                "in_progress_audits": len([a for a in audits if a.status == "in_progress"]),
                "planned_audits": len([a for a in audits if a.status == "planned"])
            },
            "findings_summary": self._summarize_audit_findings(audits),
            "performance_metrics": self._calculate_audit_performance(audits),
            "recommendations": self._extract_audit_recommendations(audits),
            "charts": [
                self._create_audit_status_chart(audits),
                self._create_findings_severity_chart(audits),
                self._create_audit_timeline_chart(audits)
            ]
        }
        
        report = Report(
            id=report_id,
            type=ReportType.AUDIT_SUMMARY,
            title="Audit Summary Report",
            generated_date=datetime.now(),
            generated_by="system",
            period_start=min(a.created_date for a in audits) if audits else datetime.now(),
            period_end=datetime.now(),
            format=ReportFormat.JSON,
            content=content
        )
        
        self.reports[report_id] = report
        self._save_reports()
        
        return report
    
    def generate_policy_overview_report(self) -> Report:
        """Generate policy management overview report"""
        
        report_id = f"policy_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not self.policy_engine:
            raise ValueError("Policy engine not available")
        
        analytics = self.policy_engine.get_policy_analytics()
        due_for_review = self.policy_engine.get_policies_for_review()
        
        content = {
            "policy_statistics": analytics,
            "review_status": {
                "due_for_review": len(due_for_review),
                "policies_by_status": analytics["status_distribution"],
                "policies_by_type": analytics["type_distribution"]
            },
            "compliance_coverage": self._analyze_policy_compliance_coverage(),
            "recommendations": self._generate_policy_recommendations(due_for_review),
            "charts": [
                self._create_policy_status_chart(analytics),
                self._create_policy_type_distribution_chart(analytics),
                self._create_compliance_coverage_chart()
            ]
        }
        
        report = Report(
            id=report_id,
            type=ReportType.POLICY_OVERVIEW,
            title="Policy Overview Report",
            generated_date=datetime.now(),
            generated_by="system",
            period_start=datetime.now() - timedelta(days=365),
            period_end=datetime.now(),
            format=ReportFormat.JSON,
            content=content
        )
        
        self.reports[report_id] = report
        self._save_reports()
        
        return report
    
    def get_dashboard_data(self, dashboard_name: str) -> Dict[str, Any]:
        """Get current data for dashboard widgets"""
        
        if dashboard_name not in self.dashboards:
            raise ValueError(f"Dashboard {dashboard_name} not found")
        
        dashboard_data = {
            "name": dashboard_name,
            "widgets": [],
            "last_updated": datetime.now().isoformat()
        }
        
        for widget in self.dashboards[dashboard_name]:
            widget_data = {
                "id": widget.id,
                "title": widget.title,
                "type": widget.type,
                "position": widget.position,
                "size": widget.size,
                "config": widget.config,
                "data": self._get_widget_data(widget)
            }
            dashboard_data["widgets"].append(widget_data)
        
        return dashboard_data
    
    def _get_widget_data(self, widget: DashboardWidget) -> Any:
        """Get current data for a specific widget"""
        
        if widget.id == "compliance_overview":
            return self._get_compliance_overview_data()
        elif widget.id == "active_audits":
            return self._get_active_audits_data()
        elif widget.id == "policy_status":
            return self._get_policy_status_chart_data()
        elif widget.id == "compliance_trends":
            return self._get_compliance_trends_data()
        elif widget.id == "recent_findings":
            return self._get_recent_findings_data()
        elif widget.id == "audit_pipeline":
            return self._get_audit_pipeline_data()
        elif widget.id == "policy_reviews":
            return self._get_policy_reviews_data()
        elif widget.id == "compliance_heatmap":
            return self._get_compliance_heatmap_data()
        else:
            return widget.data
    
    def create_custom_report(self, 
                           report_type: ReportType,
                           title: str,
                           parameters: Dict[str, Any],
                           generated_by: str) -> Report:
        """Create a custom report with specified parameters"""
        
        report_id = f"custom_{report_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        content = {}
        
        if report_type == ReportType.RISK_ASSESSMENT:
            content = self._generate_risk_assessment_content(parameters)
        elif report_type == ReportType.PERFORMANCE_METRICS:
            content = self._generate_performance_metrics_content(parameters)
        elif report_type == ReportType.STAKEHOLDER_REPORT:
            content = self._generate_stakeholder_report_content(parameters)
        
        report = Report(
            id=report_id,
            type=report_type,
            title=title,
            generated_date=datetime.now(),
            generated_by=generated_by,
            period_start=parameters.get("period_start", datetime.now() - timedelta(days=30)),
            period_end=parameters.get("period_end", datetime.now()),
            format=ReportFormat.JSON,
            content=content,
            metadata=parameters
        )
        
        self.reports[report_id] = report
        self._save_reports()
        
        return report
    
    def export_report(self, report_id: str, format: ReportFormat) -> str:
        """Export report in specified format"""
        
        if report_id not in self.reports:
            raise ValueError(f"Report {report_id} not found")
        
        report = self.reports[report_id]
        
        if format == ReportFormat.JSON:
            return json.dumps(self._serialize_report(report), indent=2, default=str)
        elif format == ReportFormat.HTML:
            return self._generate_html_report(report)
        elif format == ReportFormat.CSV:
            return self._generate_csv_report(report)
        else:
            raise ValueError(f"Format {format} not supported")
    
    def _generate_executive_summary(self, frameworks: List[str]) -> Dict[str, Any]:
        """Generate executive summary of compliance status"""
        return {
            "overall_score": 85,
            "trend": "improving",
            "key_achievements": [
                "AACSB compliance maintained at 90%",
                "Zero critical audit findings this quarter",
                "All policies updated within review cycle"
            ],
            "areas_of_concern": [
                "Minor documentation gaps in WASC standards",
                "Two policies due for review next month"
            ],
            "next_actions": [
                "Complete WASC documentation review",
                "Schedule policy review meetings",
                "Plan annual compliance assessment"
            ]
        }
    
    def _generate_compliance_metrics(self, frameworks: List[str]) -> Dict[str, Any]:
        """Generate compliance metrics"""
        return {
            "overall_compliance_score": 85,
            "framework_scores": {
                "aacsb": 90,
                "wasc": 82,
                "qaa": 88
            },
            "trend_direction": "improving",
            "last_assessment_date": datetime.now() - timedelta(days=30),
            "next_assessment_date": datetime.now() + timedelta(days=90)
        }
    
    def _create_compliance_overview_chart(self, frameworks: List[str]) -> ChartData:
        """Create compliance overview chart"""
        return ChartData(
            type=ChartType.GAUGE,
            title="Overall Compliance Score",
            data={
                "value": 85,
                "target": 90,
                "ranges": [
                    {"min": 0, "max": 60, "color": "#ff4444"},
                    {"min": 60, "max": 80, "color": "#ffaa00"},
                    {"min": 80, "max": 100, "color": "#44ff44"}
                ]
            }
        )
    
    def _serialize_report(self, report: Report) -> Dict[str, Any]:
        """Convert Report object to JSON-serializable dict"""
        return {
            "id": report.id,
            "type": report.type.value,
            "title": report.title,
            "generated_date": report.generated_date.isoformat(),
            "generated_by": report.generated_by,
            "period_start": report.period_start.isoformat(),
            "period_end": report.period_end.isoformat(),
            "format": report.format.value,
            "content": report.content,
            "metadata": report.metadata
        }
    
    def _deserialize_report(self, data: Dict[str, Any]) -> Report:
        """Convert dict back to Report object"""
        return Report(
            id=data["id"],
            type=ReportType(data["type"]),
            title=data["title"],
            generated_date=datetime.fromisoformat(data["generated_date"]),
            generated_by=data["generated_by"],
            period_start=datetime.fromisoformat(data["period_start"]),
            period_end=datetime.fromisoformat(data["period_end"]),
            format=ReportFormat(data["format"]),
            content=data["content"],
            metadata=data.get("metadata", {})
        )
    
    # Additional helper methods for data generation
    def _get_compliance_overview_data(self) -> Dict[str, Any]:
        """Get compliance overview widget data"""
        return {
            "value": "85%",
            "trend": "up",
            "status": "good",
            "change": "+3%",
            "period": "vs last month"
        }
    
    def _get_active_audits_data(self) -> Dict[str, Any]:
        """Get active audits widget data"""
        return {
            "value": 3,
            "trend": "stable",
            "breakdown": {
                "in_progress": 2,
                "planned": 1,
                "overdue": 0
            }
        }
    
    def _generate_html_report(self, report: Report) -> str:
        """Generate HTML version of report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .section {{ margin: 30px 0; }}
                .metric {{ background: #f5f5f5; padding: 15px; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report.title}</h1>
                <p>Generated: {report.generated_date.strftime('%Y-%m-%d %H:%M')}</p>
                <p>Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}</p>
            </div>
            <div class="section">
                <h2>Summary</h2>
                <pre>{json.dumps(report.content, indent=2, default=str)}</pre>
            </div>
        </body>
        </html>
        """
        return html
    
    # Placeholder methods for additional functionality
    def _identify_risk_areas(self, frameworks): return []
    def _generate_recommendations(self, frameworks): return []
    def _analyze_framework_compliance(self, framework): return {}
    def _create_trend_analysis_chart(self, frameworks, start, end): return ChartData(ChartType.LINE, "Trends", {})
    def _create_framework_comparison_chart(self, frameworks): return ChartData(ChartType.BAR, "Comparison", {})
    def _summarize_audit_findings(self, audits): return {}
    def _calculate_audit_performance(self, audits): return {}
    def _extract_audit_recommendations(self, audits): return []
    def _create_audit_status_chart(self, audits): return ChartData(ChartType.PIE, "Status", {})
    def _create_findings_severity_chart(self, audits): return ChartData(ChartType.BAR, "Findings", {})
    def _create_audit_timeline_chart(self, audits): return ChartData(ChartType.TIMELINE, "Timeline", {})
    def _analyze_policy_compliance_coverage(self): return {}
    def _generate_policy_recommendations(self, policies): return []
    def _create_policy_status_chart(self, analytics): return ChartData(ChartType.PIE, "Policy Status", {})
    def _create_policy_type_distribution_chart(self, analytics): return ChartData(ChartType.DONUT, "Types", {})
    def _create_compliance_coverage_chart(self): return ChartData(ChartType.HEATMAP, "Coverage", {})
    def _get_policy_status_chart_data(self): return {}
    def _get_compliance_trends_data(self): return {}
    def _get_recent_findings_data(self): return {}
    def _get_audit_pipeline_data(self): return {}
    def _get_policy_reviews_data(self): return {}
    def _get_compliance_heatmap_data(self): return {}
    def _generate_risk_assessment_content(self, params): return {}
    def _generate_performance_metrics_content(self, params): return {}
    def _generate_stakeholder_report_content(self, params): return {}
    def _generate_csv_report(self, report): return ""