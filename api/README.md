# CollegiumAI API Documentation

## Overview

The CollegiumAI API provides comprehensive access to the AI Multi-Agent Collaborative Framework for Digital Universities. It offers both REST and GraphQL interfaces for interacting with AI agents, managing blockchain credentials, tracking governance compliance, and administering university operations.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [REST API](#rest-api)
4. [GraphQL API](#graphql-api)
5. [Rate Limiting](#rate-limiting)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [SDK Integration](#sdk-integration)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ (for client-side development)
- PostgreSQL or MySQL database
- Redis server
- Ethereum node or test network access

### Installation

1. **Install API Server Dependencies**:
   ```bash
   cd api/
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the Server**:
   ```bash
   # Development mode
   python server.py --reload --log-level debug
   
   # Production mode
   gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn.conf.py server:app
   ```

4. **Access the API**:
   - REST API: http://localhost:4000/docs (Swagger UI)
   - GraphQL API: http://localhost:4000/graphql (GraphiQL interface)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid JWT token in the Authorization header.

### Login Endpoint

```http
POST /auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user_data": {
    "user_id": "user123",
    "user_type": "traditional_student",
    "institution": "demo_university",
    "permissions": ["agent_query"]
  }
}
```

### Using the Token

Include the token in the Authorization header for all protected requests:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### User Permissions

- `agent_query`: Query AI agents
- `credential_issue`: Issue blockchain credentials
- `governance_audit`: Create compliance audits
- `admin`: Administrative access to all features

## REST API

The REST API follows RESTful conventions and provides comprehensive endpoints for all framework features.

### Base URL

```
https://api.collegiumai.com/api/v1
```

### Core Endpoints

#### System Health

```http
GET /health
```

Returns system health status and service availability.

#### University Context

```http
GET /university/context
Authorization: Bearer <token>
```

Returns university information and configuration.

### Agent Endpoints

#### Query AI Agent

```http
POST /agents/{agent_type}/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "I need help selecting courses for next semester",
  "context": {
    "major": "Computer Science",
    "year": "sophomore",
    "gpa": 3.2
  },
  "user_type": "traditional_student",
  "collaborative": true
}
```

**Agent Types**:
- `academic_advisor`: Academic guidance and course planning
- `student_services`: Student support and campus resources

**Response**:
```json
{
  "success": true,
  "thoughts": [
    {
      "observation": "Student needs course selection help",
      "reasoning": "Based on major and GPA...",
      "action_plan": "Recommend balanced course load",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "actions": [
    {
      "action": "query_course_catalog",
      "input": {"major": "Computer Science"},
      "output": {"courses": [...]},
      "timestamp": "2024-01-15T10:30:01Z"
    }
  ],
  "final_response": "Based on your academic profile...",
  "confidence": 0.92,
  "collaborating_agents": ["student_services"],
  "recommendations": [
    "Consider CS301 for algorithmic thinking",
    "Balance with general education requirements"
  ],
  "timestamp": "2024-01-15T10:30:02Z"
}
```

#### Get Agent Information

```http
GET /agents/{agent_type}/info
Authorization: Bearer <token>
```

Returns agent capabilities, supported personas, and description.

### Blockchain Endpoints

#### Issue Academic Credential

```http
POST /blockchain/credentials/issue
Authorization: Bearer <token>
Content-Type: application/json

{
  "student_data": {
    "student_id": "STU123456",
    "blockchain_address": "0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A",
    "name": "John Doe",
    "email": "john.doe@university.edu"
  },
  "credential_data": {
    "title": "Bachelor of Science in Computer Science",
    "program": "Computer Science",
    "degree": "Bachelor",
    "grade": "A",
    "graduation_date": "2024-05-15",
    "honors": "Cum Laude"
  },
  "governance_frameworks": ["aacsb", "wasc"]
}
```

**Response**:
```json
{
  "success": true,
  "credential_id": 12345,
  "transaction_hash": "0xabc123...",
  "gas_used": "150000",
  "governance_compliance": ["aacsb", "wasc"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Verify Credential

```http
GET /blockchain/credentials/{credential_id}/verify
Authorization: Bearer <token>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "valid": true,
    "credential": {
      "id": 12345,
      "student_address": "0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A",
      "title": "Bachelor of Science in Computer Science",
      "program": "Computer Science",
      "issue_date": "2024-05-15T00:00:00Z",
      "governance_frameworks": ["aacsb", "wasc"]
    },
    "verification": {
      "blockchain_verified": true,
      "governance_compliant": true,
      "ipfs_accessible": true
    }
  }
}
```

#### Get Student Credentials

```http
GET /blockchain/students/{student_address}/credentials
Authorization: Bearer <token>
```

Returns all credentials associated with a student's blockchain address.

#### Blockchain Network Status

```http
GET /blockchain/status
Authorization: Bearer <token>
```

Returns blockchain network connectivity and smart contract status.

### Governance Endpoints

#### Create Compliance Audit

```http
POST /governance/audits
Authorization: Bearer <token>
Content-Type: application/json

{
  "institution": "University of Example",
  "framework": "aacsb",
  "audit_data": {
    "audit_area": "Faculty Qualifications",
    "status": "compliant",
    "findings": "All faculty meet minimum qualifications",
    "recommendations": "Continue current hiring practices",
    "next_review_date": "2024-12-31"
  }
}
```

#### Get Compliance Status

```http
GET /governance/compliance/{institution}/{framework}
Authorization: Bearer <token>
```

Returns current compliance status for institution and governance framework.

#### Get Upcoming Audits

```http
GET /governance/audits/upcoming?days=30
Authorization: Bearer <token>
```

Returns audits scheduled within the specified timeframe.

## GraphQL API

The GraphQL API provides a flexible, type-safe interface for querying and mutating university data.

### Endpoint

```
https://api.collegiumai.com/graphql
```

### Schema Overview

```graphql
type Query {
  health: SystemHealth!
  universityInfo: UniversityInfo!
  verifyCredential(credentialId: Int!): CredentialVerification!
  studentCredentials(studentAddress: String!): [CredentialInfo!]!
  complianceStatus(institution: String!, framework: GovernanceFrameworkEnum!): ComplianceStatus!
  blockchainStatus: BlockchainStatus!
}

type Mutation {
  queryAgent(agentType: String!, queryInput: AgentQueryInput!): AgentQueryResult!
  issueCredential(
    studentData: StudentDataInput!
    credentialData: CredentialDataInput!
    governanceFrameworks: [GovernanceFrameworkEnum!]!
  ): CredentialInfo!
  createComplianceAudit(auditInput: ComplianceAuditInput!): ComplianceStatus!
}

type Subscription {
  agentInteractionUpdates: AgentQueryResult!
  blockchainEvents: String!
}
```

### Example Queries

#### Query Agent

```graphql
mutation {
  queryAgent(
    agentType: "academic_advisor"
    queryInput: {
      message: "I need help selecting courses for next semester"
      context: "{\"major\": \"Computer Science\", \"year\": \"sophomore\"}"
      userType: TRADITIONAL_STUDENT
      collaborative: true
    }
  ) {
    success
    finalResponse
    confidence
    thoughts {
      observation
      reasoning
      actionPlan
      timestamp
    }
    recommendations
  }
}
```

#### Verify Credential

```graphql
query {
  verifyCredential(credentialId: 12345) {
    valid
    credential {
      id
      title
      program
      issueDate
      governanceFrameworks
    }
    blockchainVerified
    governanceCompliant
    securityScore
  }
}
```

#### Real-time Subscriptions

```graphql
subscription {
  agentInteractionUpdates {
    success
    finalResponse
    confidence
    timestamp
  }
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse and ensure fair usage:

- **Health endpoints**: 30 requests/minute
- **Agent queries**: 20 requests/minute
- **Credential operations**: 10 requests/minute
- **Authentication**: 5 requests/minute

Rate limits are applied per IP address and can be increased for authenticated enterprise users.

### Rate Limit Headers

```http
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 19
X-RateLimit-Reset: 1642694400
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error information:

### Error Response Format

```json
{
  "success": false,
  "error": "Detailed error message",
  "code": 400,
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req-123abc"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## Examples

### Complete Workflow Example

```python
import asyncio
import aiohttp

async def complete_workflow():
    base_url = "https://api.collegiumai.com/api/v1"
    
    # 1. Authentication
    async with aiohttp.ClientSession() as session:
        # Login
        login_data = {
            "username": "admin",
            "password": "admin_password"
        }
        
        async with session.post(f"{base_url}/auth/login", json=login_data) as resp:
            auth_response = await resp.json()
            token = auth_response["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Query Academic Advisor
        agent_query = {
            "message": "Help me plan my computer science curriculum",
            "context": {
                "major": "Computer Science",
                "year": "freshman",
                "interests": ["AI", "web development"]
            },
            "user_type": "traditional_student"
        }
        
        async with session.post(
            f"{base_url}/agents/academic_advisor/query",
            headers=headers,
            json=agent_query
        ) as resp:
            advisor_response = await resp.json()
            print("Advisor Response:", advisor_response["final_response"])
        
        # 3. Issue Credential (for graduation)
        credential_data = {
            "student_data": {
                "student_id": "STU123456",
                "blockchain_address": "0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A",
                "name": "John Doe",
                "email": "john.doe@university.edu"
            },
            "credential_data": {
                "title": "Bachelor of Science in Computer Science",
                "program": "Computer Science",
                "degree": "Bachelor",
                "grade": "A",
                "graduation_date": "2024-05-15"
            },
            "governance_frameworks": ["aacsb", "wasc"]
        }
        
        async with session.post(
            f"{base_url}/blockchain/credentials/issue",
            headers=headers,
            json=credential_data
        ) as resp:
            credential_response = await resp.json()
            credential_id = credential_response["credential_id"]
            print(f"Credential issued: ID {credential_id}")
        
        # 4. Verify Credential
        async with session.get(
            f"{base_url}/blockchain/credentials/{credential_id}/verify",
            headers=headers
        ) as resp:
            verification = await resp.json()
            print("Credential verified:", verification["data"]["valid"])

# Run the example
asyncio.run(complete_workflow())
```

### GraphQL Client Example

```python
import asyncio
import aiohttp

async def graphql_example():
    url = "https://api.collegiumai.com/graphql"
    headers = {
        "Authorization": "Bearer your-jwt-token",
        "Content-Type": "application/json"
    }
    
    # GraphQL query
    query = """
    mutation {
      queryAgent(
        agentType: "academic_advisor"
        queryInput: {
          message: "What courses should I take next semester?"
          userType: TRADITIONAL_STUDENT
        }
      ) {
        success
        finalResponse
        confidence
        recommendations
      }
    }
    """
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers=headers,
            json={"query": query}
        ) as resp:
            result = await resp.json()
            print(result["data"]["queryAgent"]["finalResponse"])

asyncio.run(graphql_example())
```

## SDK Integration

For easier integration, use the official CollegiumAI SDKs:

### Python SDK

```python
from collegiumai import CollegiumAIClient, SDKConfig, PersonaType

async def main():
    config = SDKConfig(
        api_base_url="https://api.collegiumai.com/api/v1",
        api_key="your-api-key"
    )
    
    async with CollegiumAIClient(config) as client:
        # Query agent
        advisor = client.agent("academic_advisor")
        response = await advisor.query(
            message="Help me choose courses",
            user_type=PersonaType.TRADITIONAL_STUDENT
        )
        
        # Issue credential
        result = await client.blockchain.issue_credential(
            student_data={...},
            credential_data={...},
            governance_frameworks=["aacsb"]
        )
```

### JavaScript/TypeScript SDK

```typescript
import { CollegiumAIClient, PersonaType } from '@collegiumai/sdk';

const client = new CollegiumAIClient({
  apiBaseUrl: 'https://api.collegiumai.com/api/v1',
  apiKey: 'your-api-key'
});

// Query agent
const advisor = client.agent('academic_advisor');
const response = await advisor.query({
  message: 'Help me choose courses',
  userType: PersonaType.TRADITIONAL_STUDENT
});

// Issue credential
const result = await client.blockchain.issueCredential({
  studentData: {...},
  credentialData: {...},
  governanceFrameworks: ['aacsb']
});
```

## Support and Resources

- **Documentation**: https://docs.collegiumai.com
- **API Reference**: https://api.collegiumai.com/docs 
- **GraphQL Playground**: https://api.collegiumai.com/graphql
- **GitHub Repository**: https://github.com/collegiumai/framework
- **Community Forum**: https://community.collegiumai.com
- **Support Email**: api-support@collegiumai.com

## Changelog

### Version 1.0.0 (Current)
- Initial release with full REST and GraphQL APIs
- AI agent interactions (Academic Advisor, Student Services)
- Blockchain credential management
- Governance compliance tracking
- JWT authentication and authorization
- Rate limiting and security features
- Comprehensive documentation and examples