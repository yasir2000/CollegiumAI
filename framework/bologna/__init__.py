"""
Bologna Process Framework Package
===============================

Bologna Process compliance and automation components
"""

from .compliance_automation import (
    BolognaProcessAutomation,
    ECTSValidator,
    DegreeRecognitionSystem,
    MobilityTracker,
    QualityAssuranceSystem,
    BolognaComplianceLevel,
    QualificationLevel,
    MobilityType,
    ECTSCredit,
    QualificationFrameworkMapping,
    MobilityRecord
)

__all__ = [
    'BolognaProcessAutomation',
    'ECTSValidator',
    'DegreeRecognitionSystem',
    'MobilityTracker',
    'QualityAssuranceSystem',
    'BolognaComplianceLevel',
    'QualificationLevel',
    'MobilityType',
    'ECTSCredit',
    'QualificationFrameworkMapping',
    'MobilityRecord'
]

# Version info
__version__ = '1.0.0'
__author__ = 'CollegiumAI Team'
__description__ = 'Bologna Process compliance automation and validation system'