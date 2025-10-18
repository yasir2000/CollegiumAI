// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title CollegiumAI Governance Compliance Contract
 * @dev Smart contract for tracking and enforcing higher education governance compliance
 * Supports AACSB, HEFCE, Middle States, WASC, AAC&U, SPHEIR, and QAA standards
 */
contract GovernanceCompliance is Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    Counters.Counter private _auditIds;
    Counters.Counter private _policyIds;
    
    // Governance frameworks
    enum GovernanceFramework {
        AACSB,      // Association to Advance Collegiate Schools of Business
        HEFCE,      // Higher Education Funding Council for England
        MIDDLE_STATES, // Middle States Commission on Higher Education
        WASC,       // Western Association of Schools and Colleges
        AACSU,      // American Association of Colleges and Universities
        SPHEIR,     // Strategic Partnerships for Higher Education Innovation and Reform
        QAA         // Quality Assurance Agency for Higher Education
    }
    
    // Compliance status levels
    enum ComplianceStatus {
        COMPLIANT,
        NON_COMPLIANT,
        UNDER_REVIEW,
        PENDING_REVIEW,
        CONDITIONALLY_COMPLIANT
    }
    
    // Policy types
    enum PolicyType {
        ACADEMIC,
        ADMINISTRATIVE,
        STUDENT_AFFAIRS,
        FACULTY,
        FINANCIAL,
        GOVERNANCE,
        QUALITY_ASSURANCE
    }
    
    // Compliance audit structure
    struct ComplianceAudit {
        uint256 id;
        GovernanceFramework framework;
        string institution;
        PolicyType policyType;
        string auditArea;
        ComplianceStatus status;
        uint256 auditDate;
        uint256 nextReviewDate;
        string findings;
        string recommendations;
        address auditor;
        string evidenceHash; // IPFS hash for supporting evidence
        bool isActive;
    }
    
    // Policy structure
    struct Policy {
        uint256 id;
        string title;
        string description;
        PolicyType policyType;
        GovernanceFramework[] applicableFrameworks;
        string institution;
        uint256 effectiveDate;
        uint256 reviewDate;
        address creator;
        string documentHash; // IPFS hash for policy document
        bool isActive;
        mapping(GovernanceFramework => ComplianceStatus) frameworkCompliance;
    }
    
    // Institution compliance tracking
    struct InstitutionCompliance {
        string name;
        mapping(GovernanceFramework => ComplianceStatus) overallCompliance;
        mapping(GovernanceFramework => uint256) lastAuditDate;
        mapping(GovernanceFramework => uint256) nextAuditDate;
        uint256[] auditHistory;
        bool isActive;
    }
    
    // Mappings
    mapping(uint256 => ComplianceAudit) public audits;
    mapping(uint256 => Policy) public policies;
    mapping(string => InstitutionCompliance) public institutionCompliance;
    mapping(address => bool) public authorizedAuditors;
    mapping(GovernanceFramework => mapping(string => uint256[])) public frameworkAudits;
    
    // Events
    event AuditCreated(
        uint256 indexed auditId,
        GovernanceFramework indexed framework,
        string indexed institution,
        address auditor
    );
    
    event ComplianceStatusUpdated(
        uint256 indexed auditId,
        GovernanceFramework indexed framework,
        ComplianceStatus status
    );
    
    event PolicyCreated(
        uint256 indexed policyId,
        string title,
        PolicyType policyType,
        string institution
    );
    
    event PolicyUpdated(
        uint256 indexed policyId,
        GovernanceFramework framework,
        ComplianceStatus complianceStatus
    );
    
    event AuditorAuthorized(address indexed auditor, bool authorized);
    
    // Modifiers
    modifier onlyAuthorizedAuditor() {
        require(authorizedAuditors[msg.sender] || msg.sender == owner(), "Not authorized auditor");
        _;
    }
    
    modifier validAudit(uint256 _auditId) {
        require(_auditId > 0 && _auditId <= _auditIds.current(), "Invalid audit ID");
        require(audits[_auditId].isActive, "Audit is not active");
        _;
    }
    
    modifier validPolicy(uint256 _policyId) {
        require(_policyId > 0 && _policyId <= _policyIds.current(), "Invalid policy ID");
        require(policies[_policyId].isActive, "Policy is not active");
        _;
    }
    
    /**
     * @dev Create a new compliance audit
     */
    function createComplianceAudit(
        GovernanceFramework _framework,
        string memory _institution,
        PolicyType _policyType,
        string memory _auditArea,
        ComplianceStatus _status,
        uint256 _nextReviewDate,
        string memory _findings,
        string memory _recommendations,
        string memory _evidenceHash
    ) external onlyAuthorizedAuditor returns (uint256) {
        require(bytes(_institution).length > 0, "Institution name cannot be empty");
        require(bytes(_auditArea).length > 0, "Audit area cannot be empty");
        require(_nextReviewDate > block.timestamp, "Next review date must be in the future");
        
        _auditIds.increment();
        uint256 newAuditId = _auditIds.current();
        
        audits[newAuditId] = ComplianceAudit({
            id: newAuditId,
            framework: _framework,
            institution: _institution,
            policyType: _policyType,
            auditArea: _auditArea,
            status: _status,
            auditDate: block.timestamp,
            nextReviewDate: _nextReviewDate,
            findings: _findings,
            recommendations: _recommendations,
            auditor: msg.sender,
            evidenceHash: _evidenceHash,
            isActive: true
        });
        
        // Update institution compliance tracking
        InstitutionCompliance storage instCompliance = institutionCompliance[_institution];
        if (bytes(instCompliance.name).length == 0) {
            instCompliance.name = _institution;
            instCompliance.isActive = true;
        }
        
        instCompliance.overallCompliance[_framework] = _status;
        instCompliance.lastAuditDate[_framework] = block.timestamp;
        instCompliance.nextAuditDate[_framework] = _nextReviewDate;
        instCompliance.auditHistory.push(newAuditId);
        
        // Track audits by framework
        frameworkAudits[_framework][_institution].push(newAuditId);
        
        emit AuditCreated(newAuditId, _framework, _institution, msg.sender);
        
        return newAuditId;
    }
    
    /**
     * @dev Update compliance status for an audit
     */
    function updateComplianceStatus(
        uint256 _auditId,
        ComplianceStatus _newStatus,
        string memory _updatedFindings,
        string memory _updatedRecommendations
    ) external onlyAuthorizedAuditor validAudit(_auditId) {
        ComplianceAudit storage audit = audits[_auditId];
        
        audit.status = _newStatus;
        if (bytes(_updatedFindings).length > 0) {
            audit.findings = _updatedFindings;
        }
        if (bytes(_updatedRecommendations).length > 0) {
            audit.recommendations = _updatedRecommendations;
        }
        
        // Update institution overall compliance
        institutionCompliance[audit.institution].overallCompliance[audit.framework] = _newStatus;
        
        emit ComplianceStatusUpdated(_auditId, audit.framework, _newStatus);
    }
    
    /**
     * @dev Create a new institutional policy
     */
    function createPolicy(
        string memory _title,
        string memory _description,
        PolicyType _policyType,
        GovernanceFramework[] memory _applicableFrameworks,
        string memory _institution,
        uint256 _effectiveDate,
        uint256 _reviewDate,
        string memory _documentHash
    ) external returns (uint256) {
        require(bytes(_title).length > 0, "Policy title cannot be empty");
        require(bytes(_institution).length > 0, "Institution name cannot be empty");
        require(_effectiveDate > 0 && _reviewDate > _effectiveDate, "Invalid dates");
        
        _policyIds.increment();
        uint256 newPolicyId = _policyIds.current();
        
        Policy storage newPolicy = policies[newPolicyId];
        newPolicy.id = newPolicyId;
        newPolicy.title = _title;
        newPolicy.description = _description;
        newPolicy.policyType = _policyType;
        newPolicy.applicableFrameworks = _applicableFrameworks;
        newPolicy.institution = _institution;
        newPolicy.effectiveDate = _effectiveDate;
        newPolicy.reviewDate = _reviewDate;
        newPolicy.creator = msg.sender;
        newPolicy.documentHash = _documentHash;
        newPolicy.isActive = true;
        
        // Initialize compliance status for all applicable frameworks
        for (uint i = 0; i < _applicableFrameworks.length; i++) {
            newPolicy.frameworkCompliance[_applicableFrameworks[i]] = ComplianceStatus.PENDING_REVIEW;
        }
        
        emit PolicyCreated(newPolicyId, _title, _policyType, _institution);
        
        return newPolicyId;
    }
    
    /**
     * @dev Update policy compliance status for a specific framework
     */
    function updatePolicyCompliance(
        uint256 _policyId,
        GovernanceFramework _framework,
        ComplianceStatus _complianceStatus
    ) external onlyAuthorizedAuditor validPolicy(_policyId) {
        policies[_policyId].frameworkCompliance[_framework] = _complianceStatus;
        
        emit PolicyUpdated(_policyId, _framework, _complianceStatus);
    }
    
    /**
     * @dev Get audit details
     */
    function getAuditDetails(uint256 _auditId)
        external
        view
        validAudit(_auditId)
        returns (
            GovernanceFramework framework,
            string memory institution,
            PolicyType policyType,
            string memory auditArea,
            ComplianceStatus status,
            uint256 auditDate,
            uint256 nextReviewDate,
            string memory findings,
            address auditor
        )
    {
        ComplianceAudit storage audit = audits[_auditId];
        
        return (
            audit.framework,
            audit.institution,
            audit.policyType,
            audit.auditArea,
            audit.status,
            audit.auditDate,
            audit.nextReviewDate,
            audit.findings,
            audit.auditor
        );
    }
    
    /**
     * @dev Get policy details
     */
    function getPolicyDetails(uint256 _policyId)
        external
        view
        validPolicy(_policyId)
        returns (
            string memory title,
            string memory description,
            PolicyType policyType,
            string memory institution,
            uint256 effectiveDate,
            uint256 reviewDate,
            address creator,
            string memory documentHash
        )
    {
        Policy storage policy = policies[_policyId];
        
        return (
            policy.title,
            policy.description,
            policy.policyType,
            policy.institution,
            policy.effectiveDate,
            policy.reviewDate,
            policy.creator,
            policy.documentHash
        );
    }
    
    /**
     * @dev Get institution compliance status for a specific framework
     */
    function getInstitutionComplianceStatus(
        string memory _institution,
        GovernanceFramework _framework
    ) external view returns (
        ComplianceStatus status,
        uint256 lastAuditDate,
        uint256 nextAuditDate
    ) {
        InstitutionCompliance storage compliance = institutionCompliance[_institution];
        
        return (
            compliance.overallCompliance[_framework],
            compliance.lastAuditDate[_framework],
            compliance.nextAuditDate[_framework]
        );
    }
    
    /**
     * @dev Get policy compliance status for a specific framework
     */
    function getPolicyComplianceStatus(
        uint256 _policyId,
        GovernanceFramework _framework
    ) external view validPolicy(_policyId) returns (ComplianceStatus) {
        return policies[_policyId].frameworkCompliance[_framework];
    }
    
    /**
     * @dev Get all audits for an institution and framework
     */
    function getFrameworkAudits(
        GovernanceFramework _framework,
        string memory _institution
    ) external view returns (uint256[] memory) {
        return frameworkAudits[_framework][_institution];
    }
    
    /**
     * @dev Get institution audit history
     */
    function getInstitutionAuditHistory(string memory _institution)
        external
        view
        returns (uint256[] memory)
    {
        return institutionCompliance[_institution].auditHistory;
    }
    
    /**
     * @dev Authorize/deauthorize an auditor
     */
    function setAuditorAuthorization(address _auditor, bool _authorized) 
        external 
        onlyOwner 
    {
        authorizedAuditors[_auditor] = _authorized;
        emit AuditorAuthorized(_auditor, _authorized);
    }
    
    /**
     * @dev Check if an address is an authorized auditor
     */
    function isAuthorizedAuditor(address _auditor) external view returns (bool) {
        return authorizedAuditors[_auditor] || _auditor == owner();
    }
    
    /**
     * @dev Get upcoming audits that need review
     */
    function getUpcomingAudits(uint256 _daysAhead) 
        external 
        view 
        returns (uint256[] memory) 
    {
        uint256 cutoffDate = block.timestamp + (_daysAhead * 1 days);
        uint256[] memory upcomingAudits = new uint256[](_auditIds.current());
        uint256 count = 0;
        
        for (uint256 i = 1; i <= _auditIds.current(); i++) {
            if (audits[i].isActive && 
                audits[i].nextReviewDate <= cutoffDate && 
                audits[i].nextReviewDate > block.timestamp) {
                upcomingAudits[count] = i;
                count++;
            }
        }
        
        // Resize array to actual count
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = upcomingAudits[i];
        }
        
        return result;
    }
    
    /**
     * @dev Get compliance summary for an institution
     */
    function getInstitutionComplianceSummary(string memory _institution)
        external
        view
        returns (
            uint256 totalAudits,
            uint256 compliantFrameworks,
            uint256 nonCompliantFrameworks,
            uint256 underReviewFrameworks
        )
    {
        InstitutionCompliance storage compliance = institutionCompliance[_institution];
        totalAudits = compliance.auditHistory.length;
        
        // Count compliance status across all frameworks
        for (uint i = 0; i <= uint(GovernanceFramework.QAA); i++) {
            GovernanceFramework framework = GovernanceFramework(i);
            ComplianceStatus status = compliance.overallCompliance[framework];
            
            if (status == ComplianceStatus.COMPLIANT || 
                status == ComplianceStatus.CONDITIONALLY_COMPLIANT) {
                compliantFrameworks++;
            } else if (status == ComplianceStatus.NON_COMPLIANT) {
                nonCompliantFrameworks++;
            } else if (status == ComplianceStatus.UNDER_REVIEW || 
                      status == ComplianceStatus.PENDING_REVIEW) {
                underReviewFrameworks++;
            }
        }
    }
    
    /**
     * @dev Deactivate an audit (for corrections or updates)
     */
    function deactivateAudit(uint256 _auditId) 
        external 
        onlyAuthorizedAuditor 
        validAudit(_auditId) 
    {
        audits[_auditId].isActive = false;
    }
    
    /**
     * @dev Deactivate a policy
     */
    function deactivatePolicy(uint256 _policyId) 
        external 
        validPolicy(_policyId) 
    {
        require(
            policies[_policyId].creator == msg.sender || msg.sender == owner(),
            "Not authorized to deactivate this policy"
        );
        policies[_policyId].isActive = false;
    }
    
    /**
     * @dev Get total counts
     */
    function getTotalCounts() 
        external 
        view 
        returns (
            uint256 totalAudits,
            uint256 totalPolicies,
            uint256 totalAuthorizedAuditors
        ) 
    {
        totalAudits = _auditIds.current();
        totalPolicies = _policyIds.current();
        
        // This is a simplified count - in practice, you'd maintain a counter
        totalAuthorizedAuditors = 0;
    }
}