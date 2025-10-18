/**
 * CollegiumAI SDK - TypeScript/JavaScript Client Library
 * Comprehensive SDK for integrating with the CollegiumAI Framework
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Core types and interfaces
export interface SDKConfig {
  apiBaseUrl?: string;
  apiKey?: string;
  timeout?: number;
  maxRetries?: number;
  blockchainEnabled?: boolean;
  debug?: boolean;
}

export interface UniversityContext {
  institutionName: string;
  establishmentDate: Date;
  location: {
    city: string;
    state: string;
    country: string;
  };
  accreditations: string[];
  totalStudents: number;
  totalFaculty: number;
  totalStaff: number;
  departments: string[];
  academicPrograms: string[];
  governanceFrameworks: GovernanceFramework[];
}

export interface AgentResponse {
  success: boolean;
  thoughts: Array<{
    observation: string;
    reasoning: string;
    actionPlan: string;
    timestamp: string;
  }>;
  actions: Array<{
    action: string;
    input: any;
    output: any;
    timestamp: string;
  }>;
  finalResponse: string;
  confidence: number;
  collaboratingAgents?: string[];
  recommendations?: string[];
}

// Enums
export enum PersonaType {
  // Student Personas
  TRADITIONAL_STUDENT = 'traditional_student',
  NON_TRADITIONAL_STUDENT = 'non_traditional_student',
  INTERNATIONAL_STUDENT = 'international_student',
  TRANSFER_STUDENT = 'transfer_student',
  FIRST_GENERATION_STUDENT = 'first_generation_student',
  GRADUATE_STUDENT = 'graduate_student',
  STUDENT_ATHLETE = 'student_athlete',
  ONLINE_STUDENT = 'online_student',
  PRE_PROFESSIONAL_STUDENT = 'pre_professional_student',
  RESEARCH_ORIENTED_STUDENT = 'research_oriented_student',
  SOCIAL_ACTIVIST = 'social_activist',
  ENTREPRENEURIAL_STUDENT = 'entrepreneurial_student',
  GLOBAL_CITIZEN = 'global_citizen',
  CAREER_CHANGER = 'career_changer',
  LATERAL_LEARNER = 'lateral_learner',
  CREATIVE_MIND = 'creative_mind',
  INNOVATOR = 'innovator',
  COMMUNITY_BUILDER = 'community_builder',
  CONTINUING_LEARNER = 'continuing_learner',
  COMMUNITY_SERVER = 'community_server',
  DIGITAL_NATIVE = 'digital_native',
  ADVOCATE_FOR_CHANGE = 'advocate_for_change',
  FAMILY_COMMITMENT = 'family_commitment',
  CREATIVE_PROBLEM_SOLVER = 'creative_problem_solver',
  COMMUTER_STUDENT = 'commuter_student',
  RETURNING_ADULT_STUDENT = 'returning_adult_student',
  STUDENT_WITH_DISABILITIES = 'student_with_disabilities',

  // Administrative Staff Personas
  ACADEMIC_ADVISOR = 'academic_advisor',
  REGISTRAR = 'registrar',
  FINANCIAL_AID_OFFICER = 'financial_aid_officer',
  ADMISSIONS_OFFICER = 'admissions_officer',
  HR_MANAGER = 'hr_manager',
  IT_SUPPORT_SPECIALIST = 'it_support_specialist',
  FACILITIES_MANAGER = 'facilities_manager',
  COMMUNICATIONS_SPECIALIST = 'communications_specialist',
  STUDENT_SERVICES_COORDINATOR = 'student_services_coordinator',
  GRANTS_ADMIN_OFFICER = 'grants_admin_officer',
  DIVERSITY_INCLUSION_COORDINATOR = 'diversity_inclusion_coordinator',
  LEGAL_AFFAIRS_OFFICER = 'legal_affairs_officer',

  // Academic Staff Personas
  PROFESSOR = 'professor',
  LECTURER = 'lecturer',
  RESEARCHER = 'researcher',
  DEPARTMENT_HEAD = 'department_head',
  ADJUNCT_FACULTY = 'adjunct_faculty',
  POSTDOCTORAL_FELLOW = 'postdoctoral_fellow',
  ACADEMIC_ADMINISTRATOR = 'academic_administrator',
  LIBRARIAN = 'librarian',
  TEACHING_ASSISTANT = 'teaching_assistant',
  ACADEMIC_TECHNOLOGY_SPECIALIST = 'academic_technology_specialist',
  ACADEMIC_COUNSELOR = 'academic_counselor'
}

export enum GovernanceFramework {
  AACSB = 'aacsb',
  HEFCE = 'hefce',
  MIDDLE_STATES = 'middle_states',
  WASC = 'wasc',
  AACSU = 'aacsu',
  SPHEIR = 'spheir',
  QAA = 'qaa'
}

export enum ProcessType {
  STUDENT_ENROLLMENT = 'student_enrollment',
  CURRICULUM_MANAGEMENT = 'curriculum_management',
  FACULTY_MANAGEMENT = 'faculty_management',
  RESEARCH_MANAGEMENT = 'research_management',
  GOVERNANCE_COMPLIANCE = 'governance_compliance',
  STUDENT_SERVICES = 'student_services',
  RESOURCE_MANAGEMENT = 'resource_management',
  QUALITY_ASSURANCE = 'quality_assurance'
}

// Main client class
export class CollegiumAIClient {
  private config: Required<SDKConfig>;
  private httpClient: AxiosInstance;
  private _blockchain?: BlockchainClient;
  private _governance?: GovernanceClient;
  private _agents: Map<string, AgentClient> = new Map();

  constructor(config: SDKConfig = {}) {
    this.config = {
      apiBaseUrl: config.apiBaseUrl || 'http://localhost:4000/api/v1',
      apiKey: config.apiKey || '',
      timeout: config.timeout || 30000,
      maxRetries: config.maxRetries || 3,
      blockchainEnabled: config.blockchainEnabled ?? true,
      debug: config.debug || false,
    };

    this.httpClient = axios.create({
      baseURL: this.config.apiBaseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.apiKey && { Authorization: `Bearer ${this.config.apiKey}` }),
      },
    });

    this.setupInterceptors();
    this.initializeSubClients();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.httpClient.interceptors.request.use(
      (config) => {
        if (this.config.debug) {
          console.log(`[CollegiumAI SDK] Request: ${config.method?.toUpperCase()} ${config.url}`);
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.httpClient.interceptors.response.use(
      (response) => {
        if (this.config.debug) {
          console.log(`[CollegiumAI SDK] Response: ${response.status} ${response.config.url}`);
        }
        return response;
      },
      (error) => {
        if (this.config.debug) {
          console.error(`[CollegiumAI SDK] Error: ${error.response?.status} ${error.config?.url}`, error.response?.data);
        }
        return Promise.reject(error);
      }
    );
  }

  private initializeSubClients(): void {
    this._blockchain = new BlockchainClient(this);
    this._governance = new GovernanceClient(this);
  }

  public get blockchain(): BlockchainClient {
    if (!this._blockchain) {
      throw new Error('Blockchain client not initialized');
    }
    return this._blockchain;
  }

  public get governance(): GovernanceClient {
    if (!this._governance) {
      throw new Error('Governance client not initialized');
    }
    return this._governance;
  }

  public agent(agentType: string): AgentClient {
    if (!this._agents.has(agentType)) {
      this._agents.set(agentType, new AgentClient(this, agentType));
    }
    return this._agents.get(agentType)!;
  }

  public async getUniversityContext(): Promise<UniversityContext> {
    const response = await this.httpClient.get<UniversityContext>('/university/context');
    return response.data;
  }

  public async healthCheck(): Promise<{ status: string; version: string; services: Record<string, string> }> {
    const response = await this.httpClient.get('/health');
    return response.data;
  }

  // Internal method for making HTTP requests (used by sub-clients)
  public async makeRequest<T = any>(method: 'GET' | 'POST' | 'PUT' | 'DELETE', url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.httpClient.request({
      method,
      url,
      data,
    });
    return response.data;
  }
}

// Agent client class
export class AgentClient {
  constructor(private client: CollegiumAIClient, private agentType: string) {}

  public async query(options: {
    message: string;
    context?: Record<string, any>;
    userId?: string;
    userType?: PersonaType;
    collaborative?: boolean;
  }): Promise<AgentResponse> {
    const payload = {
      message: options.message,
      context: options.context || {},
      user_id: options.userId,
      user_type: options.userType,
      collaborative: options.collaborative ?? true,
      agent_type: this.agentType,
    };

    return this.client.makeRequest<AgentResponse>('POST', `/agents/${this.agentType}/query`, payload);
  }

  public async getAgentInfo(): Promise<{
    name: string;
    description: string;
    capabilities: string[];
    supportedPersonas: PersonaType[];
  }> {
    return this.client.makeRequest('GET', `/agents/${this.agentType}/info`);
  }

  public async updateKnowledgeBase(knowledge: Record<string, any>): Promise<{ success: boolean }> {
    return this.client.makeRequest('POST', `/agents/${this.agentType}/knowledge`, knowledge);
  }
}

// Blockchain client class
export class BlockchainClient {
  constructor(private client: CollegiumAIClient) {}

  public async issueCredential(options: {
    studentData: {
      studentId: string;
      blockchainAddress: string;
      name: string;
      email: string;
    };
    credentialData: {
      title: string;
      program: string;
      degree: string;
      grade: string;
      graduationDate: Date;
      ipfsHash?: string;
    };
    governanceFrameworks: GovernanceFramework[];
  }): Promise<{
    success: boolean;
    credentialId: number;
    transactionHash: string;
    gasUsed: string;
  }> {
    return this.client.makeRequest('POST', '/blockchain/credentials/issue', {
      student_data: options.studentData,
      credential_data: options.credentialData,
      governance_frameworks: options.governanceFrameworks,
    });
  }

  public async verifyCredential(credentialId: number): Promise<{
    valid: boolean;
    credential: {
      id: number;
      studentAddress: string;
      title: string;
      program: string;
      issueDate: Date;
      governanceFrameworks: GovernanceFramework[];
    };
    verification: {
      blockchainVerified: boolean;
      governanceCompliant: boolean;
      ipfsAccessible: boolean;
    };
  }> {
    return this.client.makeRequest('GET', `/blockchain/credentials/${credentialId}/verify`);
  }

  public async getStudentCredentials(studentAddress: string): Promise<Array<{
    id: number;
    title: string;
    program: string;
    issueDate: Date;
    verified: boolean;
  }>> {
    return this.client.makeRequest('GET', `/blockchain/students/${studentAddress}/credentials`);
  }

  public async getNetworkStatus(): Promise<{
    connected: boolean;
    networkId: number;
    blockNumber: number;
    gasPrice: string;
    contractsDeployed: Record<string, string>;
  }> {
    return this.client.makeRequest('GET', '/blockchain/status');
  }

  // Bologna Process Functions

  public async setBolognaCompliance(options: {
    credentialId: number;
    ectsCredits: number;
    eqfLevel: number;
    diplomaSupplementIssued: boolean;
    learningOutcomes: string[];
    qualityAssuranceAgency: string;
    jointDegreeProgram?: boolean;
    mobilityPartners?: string[];
  }): Promise<{
    success: boolean;
    transactionHash: string;
    gasUsed: string;
  }> {
    return this.client.makeRequest('POST', '/blockchain/credentials/bologna/compliance', {
      credential_id: options.credentialId,
      ects_credits: options.ectsCredits,
      eqf_level: options.eqfLevel,
      diploma_supplement_issued: options.diplomaSupplementIssued,
      learning_outcomes: options.learningOutcomes,
      quality_assurance_agency: options.qualityAssuranceAgency,
      joint_degree_program: options.jointDegreeProgram || false,
      mobility_partners: options.mobilityPartners || [],
    });
  }

  public async getBolognaCompliance(credentialId: number): Promise<{
    ectsCredits: number;
    eqfLevel: number;
    diplomaSupplementIssued: boolean;
    learningOutcomes: string[];
    qualityAssuranceAgency: string;
    jointDegreeProgram: boolean;
    mobilityPartners: string[];
    automaticRecognition: boolean;
  }> {
    return this.client.makeRequest('GET', `/blockchain/credentials/${credentialId}/bologna`);
  }

  public async updateEctsCredits(options: {
    credentialId: number;
    newEctsCredits: number;
  }): Promise<{
    success: boolean;
    transactionHash: string;
    oldCredits: number;
    newCredits: number;
  }> {
    return this.client.makeRequest('PUT', '/blockchain/credentials/ects', {
      credential_id: options.credentialId,
      new_ects_credits: options.newEctsCredits,
    });
  }

  public async checkAutomaticRecognitionEligibility(credentialId: number): Promise<{
    eligible: boolean;
    criteria: {
      hasEctsCredits: boolean;
      validEqfLevel: boolean;
      hasQualityAssurance: boolean;
      automaticRecognitionEnabled: boolean;
    };
  }> {
    return this.client.makeRequest('GET', `/blockchain/credentials/${credentialId}/auto-recognition`);
  }

  public async getStudentTotalEcts(studentAddress: string): Promise<{
    totalEcts: number;
    credentials: Array<{
      credentialId: number;
      title: string;
      ectsCredits: number;
    }>;
  }> {
    return this.client.makeRequest('GET', `/blockchain/students/${studentAddress}/ects-total`);
  }

  public async checkBolognaComplianceStatus(credentialId: number): Promise<{
    compliant: boolean;
    report: string;
    issues: string[];
    recommendations: string[];
  }> {
    return this.client.makeRequest('GET', `/blockchain/credentials/${credentialId}/bologna/compliance-check`);
  }
}

// Governance client class
export class GovernanceClient {
  constructor(private client: CollegiumAIClient) {}

  public async createAudit(options: {
    institution: string;
    framework: GovernanceFramework;
    auditData: {
      auditArea: string;
      status: 'compliant' | 'non_compliant' | 'under_review';
      findings: string;
      recommendations: string;
      nextReviewDate: Date;
    };
  }): Promise<{
    success: boolean;
    auditId: number;
    transactionHash: string;
  }> {
    return this.client.makeRequest('POST', '/governance/audits', {
      institution: options.institution,
      framework: options.framework,
      audit_data: options.auditData,
    });
  }

  public async getComplianceStatus(institution: string, framework: GovernanceFramework): Promise<{
    institution: string;
    framework: GovernanceFramework;
    overallStatus: 'compliant' | 'non_compliant' | 'under_review';
    lastAuditDate: Date;
    nextAuditDate: Date;
    areas: Array<{
      area: string;
      status: string;
      lastReviewed: Date;
    }>;
  }> {
    return this.client.makeRequest('GET', `/governance/compliance/${institution}/${framework}`);
  }

  public async getUpcomingAudits(daysAhead: number = 30): Promise<Array<{
    id: number;
    institution: string;
    framework: GovernanceFramework;
    auditArea: string;
    scheduledDate: Date;
    status: string;
  }>> {
    return this.client.makeRequest('GET', `/governance/audits/upcoming?days=${daysAhead}`);
  }

  public async getComplianceSummary(institution: string): Promise<{
    institution: string;
    overallComplianceRate: number;
    frameworks: Record<GovernanceFramework, {
      status: string;
      complianceRate: number;
      lastAudit: Date;
      nextAudit: Date;
    }>;
    recentAudits: Array<{
      framework: GovernanceFramework;
      area: string;
      status: string;
      date: Date;
    }>;
  }> {
    return this.client.makeRequest('GET', `/governance/compliance/${institution}/summary`);
  }
}

// Utility classes and helper functions
export class PersonaHelper {
  public static getStudentPersonas(): PersonaType[] {
    return [
      PersonaType.TRADITIONAL_STUDENT,
      PersonaType.NON_TRADITIONAL_STUDENT,
      PersonaType.INTERNATIONAL_STUDENT,
      PersonaType.TRANSFER_STUDENT,
      PersonaType.FIRST_GENERATION_STUDENT,
      PersonaType.GRADUATE_STUDENT,
      PersonaType.STUDENT_ATHLETE,
      PersonaType.ONLINE_STUDENT,
      PersonaType.PRE_PROFESSIONAL_STUDENT,
      PersonaType.RESEARCH_ORIENTED_STUDENT,
      PersonaType.SOCIAL_ACTIVIST,
      PersonaType.ENTREPRENEURIAL_STUDENT,
      PersonaType.GLOBAL_CITIZEN,
      PersonaType.CAREER_CHANGER,
      PersonaType.LATERAL_LEARNER,
      PersonaType.CREATIVE_MIND,
      PersonaType.INNOVATOR,
      PersonaType.COMMUNITY_BUILDER,
      PersonaType.CONTINUING_LEARNER,
      PersonaType.COMMUNITY_SERVER,
      PersonaType.DIGITAL_NATIVE,
      PersonaType.ADVOCATE_FOR_CHANGE,
      PersonaType.FAMILY_COMMITMENT,
      PersonaType.CREATIVE_PROBLEM_SOLVER,
      PersonaType.COMMUTER_STUDENT,
      PersonaType.RETURNING_ADULT_STUDENT,
      PersonaType.STUDENT_WITH_DISABILITIES,
    ];
  }

  public static getStaffPersonas(): PersonaType[] {
    return [
      PersonaType.ACADEMIC_ADVISOR,
      PersonaType.REGISTRAR,
      PersonaType.FINANCIAL_AID_OFFICER,
      PersonaType.ADMISSIONS_OFFICER,
      PersonaType.HR_MANAGER,
      PersonaType.IT_SUPPORT_SPECIALIST,
      PersonaType.FACILITIES_MANAGER,
      PersonaType.COMMUNICATIONS_SPECIALIST,
      PersonaType.STUDENT_SERVICES_COORDINATOR,
      PersonaType.GRANTS_ADMIN_OFFICER,
      PersonaType.DIVERSITY_INCLUSION_COORDINATOR,
      PersonaType.LEGAL_AFFAIRS_OFFICER,
    ];
  }

  public static getFacultyPersonas(): PersonaType[] {
    return [
      PersonaType.PROFESSOR,
      PersonaType.LECTURER,
      PersonaType.RESEARCHER,
      PersonaType.DEPARTMENT_HEAD,
      PersonaType.ADJUNCT_FACULTY,
      PersonaType.POSTDOCTORAL_FELLOW,
      PersonaType.ACADEMIC_ADMINISTRATOR,
      PersonaType.LIBRARIAN,
      PersonaType.TEACHING_ASSISTANT,
      PersonaType.ACADEMIC_TECHNOLOGY_SPECIALIST,
      PersonaType.ACADEMIC_COUNSELOR,
    ];
  }
}

export class GovernanceHelper {
  public static getFrameworkInfo(framework: GovernanceFramework): {
    name: string;
    region: string;
    focus: string;
    standards: string[];
  } {
    const frameworkInfo = {
      [GovernanceFramework.AACSB]: {
        name: 'Association to Advance Collegiate Schools of Business',
        region: 'Global',
        focus: 'Business school accreditation',
        standards: ['Continuous improvement', 'Faculty qualifications', 'Curriculum relevance'],
      },
      [GovernanceFramework.HEFCE]: {
        name: 'Higher Education Funding Council for England',
        region: 'England',
        focus: 'Higher education governance and funding',
        standards: ['Quality assurance', 'Student experience', 'Research excellence'],
      },
      [GovernanceFramework.MIDDLE_STATES]: {
        name: 'Middle States Commission on Higher Education',
        region: 'Mid-Atlantic US',
        focus: 'Regional accreditation',
        standards: ['Mission and goals', 'Ethics and integrity', 'Design and delivery of education'],
      },
      [GovernanceFramework.WASC]: {
        name: 'Western Association of Schools and Colleges',
        region: 'Western US',
        focus: 'Institutional accreditation',
        standards: ['Institutional capacity', 'Educational effectiveness', 'Meaning and quality'],
      },
      [GovernanceFramework.AACSU]: {
        name: 'American Association of Colleges and Universities',
        region: 'United States',
        focus: 'Liberal education and assessment',
        standards: ['Educational effectiveness', 'Student learning outcomes', 'Faculty development'],
      },
      [GovernanceFramework.SPHEIR]: {
        name: 'Strategic Partnerships for Higher Education Innovation and Reform',
        region: 'Global',
        focus: 'Innovation and reform partnerships',
        standards: ['Innovation practices', 'Partnership development', 'Reform implementation'],
      },
      [GovernanceFramework.QAA]: {
        name: 'Quality Assurance Agency for Higher Education',
        region: 'United Kingdom',
        focus: 'Quality assurance in higher education',
        standards: ['Academic standards', 'Quality enhancement', 'Student protection'],
      },
    };

    return frameworkInfo[framework] || { name: 'Unknown Framework', region: '', focus: '', standards: [] };
  }
}

export class ResponseBuilder {
  public static successResponse<T>(data: T, message: string = 'Success'): {
    success: boolean;
    message: string;
    data: T;
    timestamp: string;
  } {
    return {
      success: true,
      message,
      data,
      timestamp: new Date().toISOString(),
    };
  }

  public static errorResponse(error: string, code: number = 400): {
    success: boolean;
    error: string;
    code: number;
    timestamp: string;
  } {
    return {
      success: false,
      error,
      code,
      timestamp: new Date().toISOString(),
    };
  }
}

// Utility functions
export async function quickQuery(options: {
  agentType: string;
  message: string;
  userType?: PersonaType;
  apiKey?: string;
  apiBaseUrl?: string;
}): Promise<AgentResponse> {
  const client = new CollegiumAIClient({
    apiKey: options.apiKey,
    apiBaseUrl: options.apiBaseUrl,
  });

  const agent = client.agent(options.agentType);
  return agent.query({
    message: options.message,
    userType: options.userType || PersonaType.TRADITIONAL_STUDENT,
  });
}

// Example usage patterns
export class Examples {
  public static async academicAdvisingExample(): Promise<AgentResponse> {
    const client = new CollegiumAIClient({
      apiKey: 'your-api-key',
    });

    const advisor = client.agent('academic_advisor');

    return advisor.query({
      message: 'I need help selecting courses for next semester',
      context: {
        major: 'Computer Science',
        year: 'sophomore',
        gpa: 3.2,
        completedCredits: 45,
      },
      userType: PersonaType.TRADITIONAL_STUDENT,
    });
  }

  public static async credentialVerificationExample(): Promise<any> {
    const client = new CollegiumAIClient({
      apiKey: 'your-api-key',
      blockchainEnabled: true,
    });

    return client.blockchain.verifyCredential(12345);
  }

  public static async complianceAuditExample(): Promise<any> {
    const client = new CollegiumAIClient({
      apiKey: 'your-api-key',
    });

    return client.governance.createAudit({
      institution: 'University of Example',
      framework: GovernanceFramework.AACSB,
      auditData: {
        auditArea: 'Faculty Qualifications',
        status: 'compliant',
        findings: 'All faculty meet minimum qualifications',
        recommendations: 'Continue current hiring practices',
        nextReviewDate: new Date('2024-12-31'),
      },
    });
  }
}

// Default export
export default CollegiumAIClient;