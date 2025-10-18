# CollegiumAI SDK Examples

This directory contains comprehensive examples demonstrating how to use the CollegiumAI SDK for various university scenarios.

## Available Examples

### 1. Academic Advising (`academic-advising.py`)
- Course selection assistance
- Degree planning and progression tracking
- Academic policy compliance checking
- GPA impact analysis

### 2. Student Services (`student-services.py`)
- Tutoring service coordination
- Mental health support routing
- Career counseling assistance
- Accessibility accommodation management

### 3. Blockchain Credentials (`blockchain-credentials.py`)
- Academic credential issuance
- Credential verification
- Student transcript management
- Multi-framework compliance verification

### 4. Governance Compliance (`governance-compliance.py`)
- Compliance audit creation
- Framework-specific assessments
- Institutional compliance reporting
- Automated compliance monitoring

### 5. Multi-Agent Collaboration (`multi-agent-collaboration.py`)
- Agent orchestration examples
- Collaborative problem-solving
- Cross-agent knowledge sharing
- Complex scenario handling

## Quick Start

### Python Examples

```bash
# Install the SDK
pip install collegiumai-sdk

# Run basic example
python examples/academic-advising.py

# Run with custom configuration
python examples/student-services.py --api-key your-key --debug
```

### JavaScript/TypeScript Examples

```bash
# Install the SDK
npm install @collegiumai/sdk

# Run basic example
node examples/academic-advising.js

# Run TypeScript example
npx ts-node examples/blockchain-credentials.ts
```

## Configuration

All examples support configuration through:

### Environment Variables
```bash
export COLLEGIUMAI_API_KEY="your-api-key"
export COLLEGIUMAI_BASE_URL="https://api.collegiumai.com/v1"
export COLLEGIUMAI_DEBUG="true"
```

### Configuration Files
Create a `.env` file in the examples directory:
```
COLLEGIUMAI_API_KEY=your-api-key
COLLEGIUMAI_BASE_URL=https://api.collegiumai.com/v1
COLLEGIUMAI_DEBUG=true
```

## Example Data

The `data/` directory contains sample data for all examples:
- Student profiles for different personas
- Course catalogs and academic programs
- Sample governance audit data
- Blockchain test credentials

## Integration Patterns

### 1. Simple Query Pattern
```python
from collegiumai import CollegiumAIClient, PersonaType

async def simple_example():
    client = CollegiumAIClient({'api_key': 'your-key'})
    
    advisor = client.agent('academic_advisor')
    response = await advisor.query(
        message="Help me choose courses for Computer Science major",
        user_type=PersonaType.TRADITIONAL_STUDENT
    )
    
    print(response.final_response)
```

### 2. Multi-Agent Collaboration
```python
async def collaboration_example():
    async with CollegiumAIClient(config) as client:
        # Get multiple agents
        advisor = client.agent('academic_advisor')
        services = client.agent('student_services')
        
        # Coordinate between agents
        academic_plan = await advisor.query("Plan my degree path")
        support_plan = await services.query(
            "What support services do I need?",
            context=academic_plan.context
        )
```

### 3. Blockchain Integration
```python
async def blockchain_example():
    async with CollegiumAIClient(config) as client:
        # Issue credential
        result = await client.blockchain.issue_credential(
            student_data={
                'student_id': 'STU123456',
                'blockchain_address': '0x742d35Cc6631C0532925a3b8D526Ed2CF1Ba7A',
                'name': 'John Doe',
                'email': 'john.doe@university.edu'
            },
            credential_data={
                'title': 'Bachelor of Science in Computer Science',
                'program': 'Computer Science',
                'degree': 'Bachelor',
                'grade': 'A',
                'graduation_date': datetime(2024, 5, 15)
            },
            governance_frameworks=['aacsb', 'wasc']
        )
        
        # Verify credential
        verification = await client.blockchain.verify_credential(
            result['credential_id']
        )
```

## Testing Examples

Each example includes test cases that can be run independently:

```bash
# Run all tests
pytest examples/tests/

# Run specific example tests
pytest examples/tests/test_academic_advising.py

# Run with coverage
pytest examples/tests/ --cov=examples
```

## Deployment Examples

### Docker Deployment
```bash
cd examples/deployment/docker
docker-compose up -d
```

### Kubernetes Deployment
```bash
cd examples/deployment/kubernetes
kubectl apply -f collegiumai-sdk-deployment.yaml
```

### AWS Lambda Example
```bash
cd examples/deployment/lambda
serverless deploy
```

## Performance Examples

The `performance/` directory contains examples for:
- Load testing with multiple concurrent agents
- Benchmarking different query patterns
- Optimizing API usage and caching
- Monitoring and logging best practices

## Troubleshooting

Common issues and solutions:

### Authentication Errors
```python
# Check API key configuration
client = CollegiumAIClient({'api_key': 'your-key', 'debug': True})
health = await client.health_check()
print(health)
```

### Timeout Issues
```python
# Increase timeout for complex queries
config = SDKConfig(timeout=60, max_retries=5)
client = CollegiumAIClient(config)
```

### Blockchain Connection Issues
```python
# Check blockchain status
status = await client.blockchain.get_network_status()
if not status['connected']:
    print("Blockchain not available")
```

## Contributing

To add new examples:

1. Create a new example file in the appropriate language directory
2. Add comprehensive documentation and comments
3. Include test cases in the `tests/` directory
4. Update this README with the new example
5. Add sample data if needed

## Support

For questions about these examples:
- Documentation: https://docs.collegiumai.com
- GitHub Issues: https://github.com/collegiumai/framework/issues
- Community Forum: https://community.collegiumai.com
- Email: sdk-support@collegiumai.com