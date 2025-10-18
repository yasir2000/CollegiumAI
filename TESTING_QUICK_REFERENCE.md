# CollegiumAI Testing Quick Reference Guide

## 🚀 How to Test All Features and Components

### 📋 Prerequisites

Before running tests, install dependencies:
```bash
pip install -r requirements.txt
pip install pytest anthropic ollama openai tiktoken
```

## 🎯 Testing by Category

### 1. **LLM Framework Testing** 🧠

#### Individual Provider Tests:
```bash
# Test OpenAI integration
python -m cli.commands.llm test openai "Explain machine learning"

# Test Anthropic integration  
python -m cli.commands.llm test anthropic "Write a haiku about education"

# Test Ollama local models
python -m cli.commands.llm test ollama "Help me plan my studies"

# Check provider status
python -m cli.commands.llm status
python -m cli.commands.llm list-models
```

#### Comprehensive LLM Tests:
```bash
# Run full LLM test suite
python tests/test_llm_framework.py

# Run quick validation
python tests/test_llm_framework.py --quick

# Run comprehensive tests
python tests/test_llm_framework.py --comprehensive
```

### 2. **Agent Framework Testing** 🤖

#### Individual Agent Tests:
```bash
# Test Academic Advisor
python -m cli.commands.agent test academic_advisor "Help me choose courses for my major"

# Test Student Services
python -m cli.commands.agent test student_services "I need tutoring help"

# Test Bologna Process Agent
python -m cli.commands.agent test bologna_process "Convert my US credits to ECTS"

# Interactive testing
python -m cli.commands.agent test academic_advisor --interactive
```

#### Performance Testing:
```bash
# Benchmark individual agents
python -m cli.commands.agent benchmark academic_advisor
python -m cli.commands.agent benchmark student_services

# Test all agents
python -m cli.commands.agent benchmark --all-agents

# Inspect agent capabilities
python -m cli.commands.agent inspect academic_advisor
```

### 3. **Blockchain Integration Testing** 🔗

#### Blockchain Tests:
```bash
# Run all blockchain demos
python examples/python/blockchain-credentials.py --demo all

# Test specific functions
python examples/python/blockchain-credentials.py --demo create
python examples/python/blockchain-credentials.py --demo verify
python examples/python/blockchain-credentials.py --demo compliance

# Performance testing
python examples/python/blockchain-credentials.py --demo performance --transactions 100
```

#### Blockchain CLI Tests:
```bash
# Create academic record
python -m cli.commands.blockchain create-record --student-id S001 --course-id CS101

# Verify credential
python -m cli.commands.blockchain verify --credential-id <credential_id>

# Check compliance
python -m cli.commands.blockchain check-compliance --framework AACSB
```

### 4. **Bologna Process Testing** 🎓

#### Bologna Process Tests:
```bash
# Run all Bologna Process demos
python examples/python/bologna-process-integration.py --demo all

# Test ECTS conversion
python examples/python/bologna-process-integration.py --demo ects

# Test qualification mapping
python examples/python/bologna-process-integration.py --demo qualification

# Test mobility support
python examples/python/bologna-process-integration.py --demo mobility
```

### 5. **Governance & Compliance Testing** 📋

#### Governance Tests:
```bash
# Check AACSB compliance
python -m cli.commands.governance check-compliance --framework AACSB

# Check WASC compliance
python -m cli.commands.governance check-compliance --framework WASC

# Check multiple frameworks
python -m cli.commands.governance check-compliance --framework HEFCE
python -m cli.commands.governance check-compliance --framework QAA

# Generate compliance report
python -m cli.commands.governance generate-report --output compliance_report.pdf
```

### 6. **API Gateway Testing** 🌐

#### API Server Tests:
```bash
# Start API server
python api/server.py

# Test health endpoint
curl -X GET http://localhost:8000/health

# Test agent communication
curl -X POST http://localhost:8000/agents/query \
  -H "Content-Type: application/json" \
  -d '{"agent_type":"academic_advisor","query":"Help me plan my courses"}'

# Test authentication
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

### 7. **End-to-End Integration Testing** 🔄

#### Integration Scenarios:
```bash
# Run basic integration demo
python examples/integration/run_integration_demo.py basic

# Run enhanced integration demo
python examples/integration/run_integration_demo.py enhanced

# Run comprehensive demo
python examples/integration/run_integration_demo.py enhanced comprehensive

# Run specific scenario
python examples/integration/complete_integration_demo.py STUDENT_ENROLLMENT
python examples/integration/complete_integration_demo.py RESEARCH_COLLABORATION
python examples/integration/complete_integration_demo.py CONTENT_GOVERNANCE
python examples/integration/complete_integration_demo.py UNIVERSITY_PARTNERSHIPS
```

#### Integration Test Suite:
```bash
# Run full integration test suite
python tests/integration_test_runner.py

# Run specific test categories
python tests/integration_test_runner.py --category component
python tests/integration_test_runner.py --category integration
python tests/integration_test_runner.py --category scenario
python tests/integration_test_runner.py --category performance
```

### 8. **Performance Testing** ⚡

#### Performance Benchmarks:
```bash
# LLM provider performance
python -m cli.commands.llm benchmark --provider openai --requests 50
python -m cli.commands.llm benchmark --provider anthropic --requests 50
python -m cli.commands.llm benchmark --all-providers

# Agent performance
python -m cli.commands.agent benchmark academic_advisor --queries 100
python -m cli.commands.agent benchmark --all-agents

# System performance
python tests/performance_tests.py --full-load
python tests/performance_tests.py --stress-test
```

### 9. **Security Testing** 🛡️

#### Security & Privacy Tests:
```bash
# Test FERPA compliance
python -m cli.commands.security test-ferpa-compliance

# Test data encryption
python -m cli.commands.security test-encryption

# Test access control
python -m cli.commands.security test-rbac

# Test audit logging
python -m cli.commands.security test-audit-logs

# Run security audit
python -m cli.commands.security audit --comprehensive
```

## 🧪 Comprehensive Test Suites

### Quick Test Run (5-10 minutes):
```bash
# Essential functionality
python test_demonstration.py
python tests/test_llm_framework.py --quick
python -m cli.commands.agent test academic_advisor "test query"
```

### Standard Test Run (30-60 minutes):
```bash
# Comprehensive testing
python tests/integration_test_runner.py --full
python tests/test_llm_framework.py --comprehensive
python examples/integration/complete_integration_demo.py --all-scenarios
```

### Full Test Suite (1-2 hours):
```bash
# Complete validation
python tests/integration_test_runner.py --full
python -m cli.commands.agent benchmark --all-agents
python -m cli.commands.llm benchmark --all-providers
python examples/integration/performance_tests.py --full-load
```

## 📊 Test Monitoring & Results

### Test Results Dashboard:
```bash
# Generate test report
python tests/generate_test_report.py

# Monitor test results
python tests/test_monitor.py --watch

# Export test metrics
python tests/export_metrics.py --format json --output test_results.json
```

### Continuous Testing:
```bash
# Watch mode for development
python tests/watch_tests.py

# Pre-commit testing
python tests/precommit_tests.py

# Automated regression testing
python tests/regression_tests.py --baseline
```

## 🎯 Testing Best Practices

### 1. **Test Isolation**
```bash
# Clean test environment
python tests/cleanup_test_env.py

# Reset test data
python tests/reset_test_data.py
```

### 2. **Mock External Dependencies**
```bash
# Run tests with mocks
python tests/test_with_mocks.py

# Test offline mode
python tests/test_offline.py
```

### 3. **Environment Testing**
```bash
# Test in development environment
ENVIRONMENT=dev python tests/test_llm_framework.py

# Test in staging environment
ENVIRONMENT=staging python tests/integration_test_runner.py

# Test in production-like environment
ENVIRONMENT=prod python tests/production_tests.py
```

## 🚀 Test Automation

### GitHub Actions Pipeline:
```yaml
# .github/workflows/test.yml
name: CollegiumAI Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          python tests/test_llm_framework.py
          python tests/integration_test_runner.py
          python -m cli.commands.agent benchmark --all-agents
```

### Local Automation:
```bash
# Set up automated testing
python tests/setup_automation.py

# Run nightly tests
python tests/nightly_tests.py

# Generate weekly reports
python tests/weekly_report.py
```

## 📈 Success Metrics

### Target Metrics:
- **Success Rate**: >95% for critical paths
- **Performance**: <2s response time for standard queries
- **Coverage**: >90% code coverage
- **Availability**: >99.9% uptime for core services
- **Security**: Zero critical vulnerabilities

### Monitoring:
```bash
# Check current metrics
python tests/check_metrics.py

# Generate metrics dashboard
python tests/metrics_dashboard.py

# Alert on metric thresholds
python tests/metric_alerts.py
```

## 🎉 Testing Confidence

With this comprehensive testing approach, CollegiumAI ensures:

✅ **All components work correctly** across different scenarios
✅ **Performance meets requirements** under various load conditions
✅ **Security standards are maintained** with regular audits
✅ **Compliance frameworks are satisfied** with automated checking
✅ **Integration workflows function seamlessly** end-to-end
✅ **Quality standards are met** for educational outcomes

**Ready to test every feature and component of CollegiumAI!** 🚀🧪✨