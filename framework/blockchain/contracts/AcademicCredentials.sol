// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title CollegiumAI Academic Credentials Contract
 * @dev Smart contract for managing academic credentials, degrees, and certificates
 * Supports multiple governance frameworks (AACSB, HEFCE, WASC, QAA, etc.)
 */
contract AcademicCredentials is Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    Counters.Counter private _credentialIds;
    
    // Governance frameworks supported
    enum GovernanceFramework {
        AACSB,      // Association to Advance Collegiate Schools of Business
        HEFCE,      // Higher Education Funding Council for England
        MIDDLE_STATES, // Middle States Commission on Higher Education
        WASC,       // Western Association of Schools and Colleges
        AACSU,      // American Association of Colleges and Universities
        SPHEIR,     // Strategic Partnerships for Higher Education Innovation and Reform
        QAA,        // Quality Assurance Agency for Higher Education
        BOLOGNA_PROCESS // European Higher Education Area framework
    }
    
    // Credential types
    enum CredentialType {
        DEGREE,
        CERTIFICATE,
        DIPLOMA,
        BADGE,
        TRANSCRIPT,
        COURSE_COMPLETION
    }
    
    // Academic credential structure
    struct Credential {
        uint256 id;
        address student;
        string studentId;
        CredentialType credentialType;
        string title;
        string institution;
        string program;
        string grade;
        uint256 credits;
        uint256 issueDate;
        uint256 completionDate;
        bool isActive;
        string ipfsHash; // For storing detailed credential data
        GovernanceFramework[] applicableFrameworks;
        mapping(GovernanceFramework => bool) frameworkCompliance;
    }
    
    // Institution information
    struct Institution {
        string name;
        string accreditation;
        address admin;
        GovernanceFramework[] supportedFrameworks;
        bool isActive;
    }
    
    // Bologna Process specific data structure
    struct BolognaData {
        uint256 ectsCredits;        // ECTS credits for the credential
        uint8 eqfLevel;             // European Qualifications Framework level (1-8)
        bool diplomaSupplementIssued; // Whether diploma supplement was issued
        string[] learningOutcomes;   // Defined learning outcomes
        string qualityAssuranceAgency; // Responsible QA agency
        bool jointDegreeProgram;     // Is this a joint/double degree program
        string[] mobilityPartners;   // Partner institutions for mobility
        bool automaticRecognition;   // Eligible for automatic recognition
    }
    
    // Mappings
    mapping(uint256 => Credential) public credentials;
    mapping(address => uint256[]) public studentCredentials;
    mapping(string => Institution) public institutions;
    mapping(address => bool) public authorizedIssuers;
    mapping(uint256 => BolognaData) public credentialBolognaData;
    
    // Events
    event CredentialIssued(
        uint256 indexed credentialId,
        address indexed student,
        string studentId,
        CredentialType credentialType,
        string title,
        string institution
    );
    
    event CredentialVerified(
        uint256 indexed credentialId,
        address indexed verifier,
        bool isValid
    );
    
    event ComplianceUpdated(
        uint256 indexed credentialId,
        GovernanceFramework framework,
        bool compliant
    );
    
    event InstitutionRegistered(
        string indexed institutionName,
        address indexed admin,
        GovernanceFramework[] frameworks
    );
    
    event BolognaComplianceSet(
        uint256 indexed credentialId,
        uint256 ectsCredits,
        uint8 eqfLevel,
        bool automaticRecognition
    );
    
    event ECTSCreditsUpdated(
        uint256 indexed credentialId,
        uint256 oldCredits,
        uint256 newCredits
    );
    
    // Modifiers
    modifier onlyAuthorizedIssuer() {
        require(authorizedIssuers[msg.sender] || msg.sender == owner(), "Not authorized to issue credentials");
        _;
    }
    
    modifier validCredential(uint256 _credentialId) {
        require(_credentialId > 0 && _credentialId <= _credentialIds.current(), "Invalid credential ID");
        require(credentials[_credentialId].isActive, "Credential is not active");
        _;
    }
    
    /**
     * @dev Register a new educational institution
     */
    function registerInstitution(
        string memory _name,
        string memory _accreditation,
        address _admin,
        GovernanceFramework[] memory _frameworks
    ) external onlyOwner {
        require(bytes(_name).length > 0, "Institution name cannot be empty");
        require(_admin != address(0), "Invalid admin address");
        
        institutions[_name] = Institution({
            name: _name,
            accreditation: _accreditation,
            admin: _admin,
            supportedFrameworks: _frameworks,
            isActive: true
        });
        
        authorizedIssuers[_admin] = true;
        
        emit InstitutionRegistered(_name, _admin, _frameworks);
    }
    
    /**
     * @dev Issue a new academic credential
     */
    function issueCredential(
        address _student,
        string memory _studentId,
        CredentialType _credentialType,
        string memory _title,
        string memory _institution,
        string memory _program,
        string memory _grade,
        uint256 _credits,
        uint256 _completionDate,
        string memory _ipfsHash,
        GovernanceFramework[] memory _applicableFrameworks
    ) external onlyAuthorizedIssuer nonReentrant returns (uint256) {
        require(_student != address(0), "Invalid student address");
        require(bytes(_studentId).length > 0, "Student ID cannot be empty");
        require(bytes(_title).length > 0, "Credential title cannot be empty");
        require(bytes(_institution).length > 0, "Institution cannot be empty");
        require(institutions[_institution].isActive, "Institution not registered");
        
        _credentialIds.increment();
        uint256 newCredentialId = _credentialIds.current();
        
        Credential storage newCredential = credentials[newCredentialId];
        newCredential.id = newCredentialId;
        newCredential.student = _student;
        newCredential.studentId = _studentId;
        newCredential.credentialType = _credentialType;
        newCredential.title = _title;
        newCredential.institution = _institution;
        newCredential.program = _program;
        newCredential.grade = _grade;
        newCredential.credits = _credits;
        newCredential.issueDate = block.timestamp;
        newCredential.completionDate = _completionDate;
        newCredential.isActive = true;
        newCredential.ipfsHash = _ipfsHash;
        newCredential.applicableFrameworks = _applicableFrameworks;
        
        // Initialize compliance status for all applicable frameworks
        for (uint i = 0; i < _applicableFrameworks.length; i++) {
            newCredential.frameworkCompliance[_applicableFrameworks[i]] = true;
        }
        
        studentCredentials[_student].push(newCredentialId);
        
        emit CredentialIssued(
            newCredentialId,
            _student,
            _studentId,
            _credentialType,
            _title,
            _institution
        );
        
        return newCredentialId;
    }
    
    /**
     * @dev Verify a credential's authenticity
     */
    function verifyCredential(uint256 _credentialId) 
        external 
        view 
        validCredential(_credentialId) 
        returns (
            bool isValid,
            address student,
            string memory title,
            string memory institution,
            uint256 issueDate,
            bool isActive
        ) 
    {
        Credential storage cred = credentials[_credentialId];
        
        return (
            cred.isActive && institutions[cred.institution].isActive,
            cred.student,
            cred.title,
            cred.institution,
            cred.issueDate,
            cred.isActive
        );
    }
    
    /**
     * @dev Get detailed credential information
     */
    function getCredentialDetails(uint256 _credentialId)
        external
        view
        validCredential(_credentialId)
        returns (
            uint256 id,
            address student,
            string memory studentId,
            CredentialType credentialType,
            string memory title,
            string memory institution,
            string memory program,
            string memory grade,
            uint256 credits,
            uint256 issueDate,
            uint256 completionDate,
            string memory ipfsHash
        )
    {
        Credential storage cred = credentials[_credentialId];
        
        return (
            cred.id,
            cred.student,
            cred.studentId,
            cred.credentialType,
            cred.title,
            cred.institution,
            cred.program,
            cred.grade,
            cred.credits,
            cred.issueDate,
            cred.completionDate,
            cred.ipfsHash
        );
    }
    
    /**
     * @dev Check governance framework compliance for a credential
     */
    function checkFrameworkCompliance(
        uint256 _credentialId,
        GovernanceFramework _framework
    ) external view validCredential(_credentialId) returns (bool) {
        return credentials[_credentialId].frameworkCompliance[_framework];
    }
    
    /**
     * @dev Update governance framework compliance status
     */
    function updateFrameworkCompliance(
        uint256 _credentialId,
        GovernanceFramework _framework,
        bool _compliant
    ) external onlyAuthorizedIssuer validCredential(_credentialId) {
        credentials[_credentialId].frameworkCompliance[_framework] = _compliant;
        
        emit ComplianceUpdated(_credentialId, _framework, _compliant);
    }
    
    /**
     * @dev Get all credentials for a student
     */
    function getStudentCredentials(address _student) 
        external 
        view 
        returns (uint256[] memory) 
    {
        return studentCredentials[_student];
    }
    
    /**
     * @dev Revoke a credential (in case of fraud or error)
     */
    function revokeCredential(uint256 _credentialId) 
        external 
        onlyAuthorizedIssuer 
        validCredential(_credentialId) 
    {
        credentials[_credentialId].isActive = false;
    }
    
    /**
     * @dev Add authorized issuer
     */
    function addAuthorizedIssuer(address _issuer) external onlyOwner {
        authorizedIssuers[_issuer] = true;
    }
    
    /**
     * @dev Remove authorized issuer
     */
    function removeAuthorizedIssuer(address _issuer) external onlyOwner {
        authorizedIssuers[_issuer] = false;
    }
    
    /**
     * @dev Get total number of credentials issued
     */
    function getTotalCredentials() external view returns (uint256) {
        return _credentialIds.current();
    }
    
    /**
     * @dev Check if an address is an authorized issuer
     */
    function isAuthorizedIssuer(address _issuer) external view returns (bool) {
        return authorizedIssuers[_issuer] || _issuer == owner();
    }
    
    /**
     * @dev Get institution details
     */
    function getInstitutionDetails(string memory _institutionName)
        external
        view
        returns (
            string memory name,
            string memory accreditation,
            address admin,
            bool isActive
        )
    {
        Institution storage inst = institutions[_institutionName];
        return (
            inst.name,
            inst.accreditation,
            inst.admin,
            inst.isActive
        );
    }
    
    /**
     * @dev Emergency pause function
     */
    function pauseInstitution(string memory _institutionName) external onlyOwner {
        institutions[_institutionName].isActive = false;
    }
    
    /**
     * @dev Unpause institution
     */
    function unpauseInstitution(string memory _institutionName) external onlyOwner {
        institutions[_institutionName].isActive = true;
    }
    
    /**
     * @dev Set Bologna Process compliance data for a credential
     */
    function setBolognaCompliance(
        uint256 _credentialId,
        uint256 _ectsCredits,
        uint8 _eqfLevel,
        bool _diplomaSupplementIssued,
        string[] memory _learningOutcomes,
        string memory _qualityAssuranceAgency,
        bool _jointDegreeProgram,
        string[] memory _mobilityPartners
    ) external onlyAuthorizedIssuer {
        require(_credentialId > 0 && _credentialId <= credentialCounter, "Invalid credential ID");
        require(_eqfLevel >= 1 && _eqfLevel <= 8, "Invalid EQF level");
        require(_ectsCredits > 0, "ECTS credits must be positive");
        
        BolognaData storage bolognaData = credentialBolognaData[_credentialId];
        bolognaData.ectsCredits = _ectsCredits;
        bolognaData.eqfLevel = _eqfLevel;
        bolognaData.diplomaSupplementIssued = _diplomaSupplementIssued;
        bolognaData.learningOutcomes = _learningOutcomes;
        bolognaData.qualityAssuranceAgency = _qualityAssuranceAgency;
        bolognaData.jointDegreeProgram = _jointDegreeProgram;
        bolognaData.mobilityPartners = _mobilityPartners;
        bolognaData.automaticRecognition = true; // Bologna Process enables automatic recognition
        
        emit BolognaComplianceSet(_credentialId, _ectsCredits, _eqfLevel, true);
    }
    
    /**
     * @dev Get Bologna Process compliance data for a credential
     */
    function getBolognaCompliance(uint256 _credentialId)
        external
        view
        returns (
            uint256 ectsCredits,
            uint8 eqfLevel,
            bool diplomaSupplementIssued,
            string[] memory learningOutcomes,
            string memory qualityAssuranceAgency,
            bool jointDegreeProgram,
            string[] memory mobilityPartners,
            bool automaticRecognition
        )
    {
        require(_credentialId > 0 && _credentialId <= credentialCounter, "Invalid credential ID");
        
        BolognaData storage bolognaData = credentialBolognaData[_credentialId];
        return (
            bolognaData.ectsCredits,
            bolognaData.eqfLevel,
            bolognaData.diplomaSupplementIssued,
            bolognaData.learningOutcomes,
            bolognaData.qualityAssuranceAgency,
            bolognaData.jointDegreeProgram,
            bolognaData.mobilityPartners,
            bolognaData.automaticRecognition
        );
    }
    
    /**
     * @dev Update ECTS credits for a credential
     */
    function updateECTSCredits(uint256 _credentialId, uint256 _newEctsCredits) 
        external 
        onlyAuthorizedIssuer 
    {
        require(_credentialId > 0 && _credentialId <= credentialCounter, "Invalid credential ID");
        require(_newEctsCredits > 0, "ECTS credits must be positive");
        
        uint256 oldCredits = credentialBolognaData[_credentialId].ectsCredits;
        credentialBolognaData[_credentialId].ectsCredits = _newEctsCredits;
        
        emit ECTSCreditsUpdated(_credentialId, oldCredits, _newEctsCredits);
    }
    
    /**
     * @dev Check if credential qualifies for automatic recognition under Bologna Process
     */
    function isEligibleForAutomaticRecognition(uint256 _credentialId) 
        external 
        view 
        returns (bool) 
    {
        require(_credentialId > 0 && _credentialId <= credentialCounter, "Invalid credential ID");
        
        BolognaData storage bolognaData = credentialBolognaData[_credentialId];
        
        // Criteria for automatic recognition:
        // 1. Must have ECTS credits assigned
        // 2. Must have valid EQF level
        // 3. Must have quality assurance agency
        // 4. Institution must support Bologna Process framework
        
        return bolognaData.ectsCredits > 0 &&
               bolognaData.eqfLevel >= 1 && bolognaData.eqfLevel <= 8 &&
               bytes(bolognaData.qualityAssuranceAgency).length > 0 &&
               bolognaData.automaticRecognition;
    }
    
    /**
     * @dev Get total ECTS credits for a student
     */
    function getStudentTotalECTS(address _student) 
        external 
        view 
        returns (uint256 totalECTS) 
    {
        uint256[] memory studentCreds = studentCredentials[_student];
        
        for (uint256 i = 0; i < studentCreds.length; i++) {
            totalECTS += credentialBolognaData[studentCreds[i]].ectsCredits;
        }
        
        return totalECTS;
    }
    
    /**
     * @dev Check Bologna Process framework compliance for credential
     */
    function checkBolognaCompliance(uint256 _credentialId) 
        external 
        view 
        returns (bool compliant, string memory report) 
    {
        require(_credentialId > 0 && _credentialId <= credentialCounter, "Invalid credential ID");
        
        BolognaData storage bolognaData = credentialBolognaData[_credentialId];
        
        string memory issues = "";
        bool isCompliant = true;
        
        if (bolognaData.ectsCredits == 0) {
            issues = string(abi.encodePacked(issues, "Missing ECTS credits assignment; "));
            isCompliant = false;
        }
        
        if (bolognaData.eqfLevel < 1 || bolognaData.eqfLevel > 8) {
            issues = string(abi.encodePacked(issues, "Invalid EQF level; "));
            isCompliant = false;
        }
        
        if (bytes(bolognaData.qualityAssuranceAgency).length == 0) {
            issues = string(abi.encodePacked(issues, "Missing quality assurance agency; "));
            isCompliant = false;
        }
        
        if (bolognaData.learningOutcomes.length == 0) {
            issues = string(abi.encodePacked(issues, "Missing learning outcomes; "));
            isCompliant = false;
        }
        
        string memory finalReport = isCompliant ? 
            "Credential fully compliant with Bologna Process standards" : 
            string(abi.encodePacked("Compliance issues: ", issues));
            
        return (isCompliant, finalReport);
    }
}