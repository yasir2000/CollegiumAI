# CollegiumAI Deployment Guide

Version: 1.0.0 "Cognitive Genesis"  
Last Updated: October 19, 2025

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Local Development Deployment](#local-development-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Institutional Deployment](#institutional-deployment)
- [Production Deployment](#production-deployment)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides comprehensive instructions for deploying CollegiumAI v1.0.0 "Cognitive Genesis" across different environments, from local development to enterprise-scale production deployments.

### Deployment Options

1. **Local Development**: Single-machine development and testing
2. **Docker Containerized**: Portable, scalable container deployment
3. **Cloud Deployment**: AWS, Azure, GCP cloud platforms
4. **Institutional**: University server infrastructure
5. **Production Scale**: Enterprise-grade multi-node deployment

---

## Prerequisites

### System Requirements

#### Minimum Requirements
- **OS**: Ubuntu 20.04+, Windows 10+, macOS 11+
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB available space
- **CPU**: 4 cores minimum, 8 cores recommended

#### Recommended Requirements
- **OS**: Ubuntu 22.04 LTS or Windows 11
- **Python**: 3.11 (optimal performance)
- **RAM**: 32GB for full cognitive processing
- **Storage**: 50GB SSD for optimal performance
- **CPU**: 16 cores for multi-agent processing
- **GPU**: NVIDIA RTX 3080+ for enhanced AI processing (optional)

### Software Dependencies

```bash
# Python 3.8+ with pip
python --version  # Should be 3.8+
pip --version

# Git for source control
git --version

# Optional: Docker for containerized deployment
docker --version
docker-compose --version
```

### Network Requirements

- **Outbound HTTPS**: Access to AI model APIs (OpenAI, Anthropic, etc.)
- **Inbound HTTP/HTTPS**: For web interface (ports 8000, 8080, 443)
- **Database Access**: PostgreSQL, MongoDB if using external databases
- **Redis**: For caching and session management

---

## Local Development Deployment

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yasir2000/CollegiumAI.git
cd CollegiumAI

# Create virtual environment
python -m venv collegiumai_env

# Activate virtual environment
# On Windows:
collegiumai_env\Scripts\activate
# On macOS/Linux:
source collegiumai_env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas, numpy, sklearn, tensorflow, torch; print('Dependencies installed successfully')"
```

### Step 3: Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
```

Example `.env` configuration:
```bash
# AI Model Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OLLAMA_HOST=http://localhost:11434

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/collegiumai
REDIS_URL=redis://localhost:6379/0

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=15
SESSION_TIMEOUT=7200

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
```

### Step 4: Initialize System

```bash
# Run quick validation
python quick_test.py

# Run comprehensive tests
python comprehensive_test_suite.py

# Initialize system
python main.py --mode=interactive
```

### Step 5: Verification

```bash
# Test cognitive processing
python -c "
import asyncio
from framework.cognitive import CognitivePersonaFactory, PersonaType

async def test():
    factory = CognitivePersonaFactory()
    student = factory.create_agent(PersonaType.TRADITIONAL_STUDENT)
    result = await student.process_intelligent_request({
        'text': 'Hello, I need help with my studies',
        'context': {'domain': 'academic'}
    })
    print(f'System working! Confidence: {result.get(\"confidence\", 0):.2f}')

asyncio.run(test())
"
```

---

## Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 collegiumai && \
    chown -R collegiumai:collegiumai /app
USER collegiumai

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Start command
CMD ["python", "main.py", "--mode=server", "--host=0.0.0.0", "--port=8000"]
```

### Step 2: Create Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  collegiumai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/collegiumai
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: collegiumai
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - collegiumai
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Step 3: Build and Deploy

```bash
# Build the image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f collegiumai

# Scale the application
docker-compose up -d --scale collegiumai=3

# Stop services
docker-compose down
```

### Step 4: Docker Validation

```bash
# Check container health
docker-compose ps

# Test the application
curl http://localhost:8000/health

# Run tests in container
docker-compose exec collegiumai python quick_test.py
```

---

## Cloud Deployment

### AWS Deployment

#### Using AWS ECS (Elastic Container Service)

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Create ECS cluster
aws ecs create-cluster --cluster-name collegiumai-cluster

# Build and push to ECR
aws ecr create-repository --repository-name collegiumai
docker build -t collegiumai .
docker tag collegiumai:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/collegiumai:latest
aws ecr get-login-password | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/collegiumai:latest
```

#### ECS Task Definition (ecs-task-definition.json)

```json
{
  "family": "collegiumai",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "collegiumai",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/collegiumai:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:pass@rds-endpoint:5432/collegiumai"
        },
        {
          "name": "REDIS_URL", 
          "value": "redis://redis-endpoint:6379/0"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/collegiumai",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Install Azure CLI
pip install azure-cli

# Login to Azure
az login

# Create resource group
az group create --name collegiumai-rg --location eastus

# Create container registry
az acr create --resource-group collegiumai-rg --name collegiumairegistry --sku Basic

# Build and push image
az acr build --registry collegiumairegistry --image collegiumai:v1.0.0 .

# Deploy container instance
az container create \
  --resource-group collegiumai-rg \
  --name collegiumai-instance \
  --image collegiumairegistry.azurecr.io/collegiumai:v1.0.0 \
  --cpu 2 \
  --memory 4 \
  --port 8000 \
  --environment-variables \
    DATABASE_URL="postgresql://user:pass@db-server:5432/collegiumai" \
    REDIS_URL="redis://redis-server:6379/0"
```

### Google Cloud Platform (GCP)

#### Using Google Cloud Run

```bash
# Install Google Cloud SDK
# Follow: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project your-project-id

# Build and deploy
gcloud builds submit --tag gcr.io/your-project-id/collegiumai
gcloud run deploy collegiumai \
  --image gcr.io/your-project-id/collegiumai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --set-env-vars DATABASE_URL="postgresql://user:pass@db:5432/collegiumai"
```

---

## Institutional Deployment

### University Server Setup

#### Prerequisites
- Ubuntu 22.04 LTS server
- Root or sudo access
- Static IP address
- SSL certificate for HTTPS

#### Step 1: Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-pip python3.11-venv git nginx postgresql redis-server

# Create application user
sudo useradd -m -s /bin/bash collegiumai
sudo usermod -aG sudo collegiumai

# Switch to application user
sudo su - collegiumai
```

#### Step 2: Application Setup

```bash
# Clone repository
git clone https://github.com/yasir2000/CollegiumAI.git
cd CollegiumAI

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create configuration
cp .env.example .env
nano .env  # Configure for production
```

#### Step 3: Database Setup

```bash
# Configure PostgreSQL
sudo -u postgres createuser collegiumai
sudo -u postgres createdb collegiumai -O collegiumai
sudo -u postgres psql -c "ALTER USER collegiumai PASSWORD 'secure_password';"

# Configure Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

#### Step 4: Systemd Service

Create `/etc/systemd/system/collegiumai.service`:

```ini
[Unit]
Description=CollegiumAI University Assistant
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=collegiumai
WorkingDirectory=/home/collegiumai/CollegiumAI
Environment=PATH=/home/collegiumai/CollegiumAI/venv/bin
ExecStart=/home/collegiumai/CollegiumAI/venv/bin/python main.py --mode=server --host=127.0.0.1 --port=8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable collegiumai
sudo systemctl start collegiumai
sudo systemctl status collegiumai
```

#### Step 5: Nginx Configuration

Create `/etc/nginx/sites-available/collegiumai`:

```nginx
server {
    listen 80;
    server_name collegiumai.university.edu;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name collegiumai.university.edu;

    ssl_certificate /path/to/ssl/certificate.crt;
    ssl_certificate_key /path/to/ssl/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Logging
    access_log /var/log/nginx/collegiumai_access.log;
    error_log /var/log/nginx/collegiumai_error.log;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/collegiumai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Production Deployment

### High Availability Setup

#### Load Balancer Configuration

```nginx
# /etc/nginx/nginx.conf
upstream collegiumai_backend {
    least_conn;
    server 10.0.1.10:8000 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:8000 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name collegiumai.university.edu;

    location / {
        proxy_pass http://collegiumai_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health check
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
    }
}
```

#### Database Clustering

```bash
# PostgreSQL Master-Slave Setup
# Master configuration in postgresql.conf
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3

# Create replication user
CREATE USER replica_user REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD 'secure_password';
```

### Monitoring and Logging

#### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'collegiumai'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

#### Grafana Dashboard

Key metrics to monitor:
- Response time and throughput
- Cognitive processing success rate
- Memory usage and CPU utilization
- Database connection pool status
- Cache hit rates
- Error rates and types

### Backup Strategy

```bash
#!/bin/bash
# backup_collegiumai.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/collegiumai"

# Database backup
pg_dump -h localhost -U collegiumai collegiumai > "$BACKUP_DIR/db_backup_$DATE.sql"

# Application files backup
tar -czf "$BACKUP_DIR/app_backup_$DATE.tar.gz" /home/collegiumai/CollegiumAI

# Configuration backup
cp /home/collegiumai/CollegiumAI/.env "$BACKUP_DIR/config_backup_$DATE.env"

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.sql" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.env" -mtime +30 -delete

echo "Backup completed: $DATE"
```

---

## Monitoring and Maintenance

### Health Checks

```python
# health_check.py
import asyncio
import requests
import sys
from datetime import datetime

async def health_check():
    """Comprehensive health check for CollegiumAI"""
    
    checks = {
        'web_server': False,
        'database': False,
        'redis': False,
        'cognitive_engine': False,
        'multi_agent': False
    }
    
    try:
        # Web server check
        response = requests.get('http://localhost:8000/health', timeout=10)
        checks['web_server'] = response.status_code == 200
        
        # Database check
        # Implementation depends on your database setup
        
        # Redis check
        # Implementation depends on your Redis setup
        
        # Cognitive engine check
        from framework.cognitive import CognitivePersonaFactory, PersonaType
        factory = CognitivePersonaFactory()
        agent = factory.create_agent(PersonaType.TRADITIONAL_STUDENT)
        result = await agent.process_intelligent_request({
            'text': 'Health check test',
            'context': {'test': True}
        })
        checks['cognitive_engine'] = result.get('confidence', 0) > 0
        
        # Multi-agent check
        from multi_agent_system import MultiAgentOrchestrator
        # Mock check for multi-agent system
        checks['multi_agent'] = True
        
    except Exception as e:
        print(f"Health check error: {e}")
    
    # Report results
    all_healthy = all(checks.values())
    status = "HEALTHY" if all_healthy else "UNHEALTHY"
    
    print(f"{datetime.now()}: System Status: {status}")
    for component, healthy in checks.items():
        status_icon = "✅" if healthy else "❌"
        print(f"  {status_icon} {component}")
    
    return all_healthy

if __name__ == "__main__":
    healthy = asyncio.run(health_check())
    sys.exit(0 if healthy else 1)
```

### Performance Monitoring

```python
# performance_monitor.py
import asyncio
import time
import psutil
import logging
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.response_times = []
        
    async def monitor_system(self):
        """Monitor system performance metrics"""
        
        while True:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network stats
            network = psutil.net_io_counters()
            
            # Log metrics
            logging.info(f"Performance Metrics - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
            
            # Alert if thresholds exceeded
            if cpu_percent > 80:
                logging.warning(f"High CPU usage: {cpu_percent}%")
            if memory_percent > 85:
                logging.warning(f"High memory usage: {memory_percent}%")
            if disk_percent > 90:
                logging.error(f"Low disk space: {disk_percent}% used")
            
            await asyncio.sleep(60)  # Monitor every minute

# Usage
monitor = PerformanceMonitor()
asyncio.run(monitor.monitor_system())
```

### Automated Maintenance

```bash
#!/bin/bash
# maintenance.sh - Daily maintenance tasks

LOG_FILE="/var/log/collegiumai/maintenance.log"
echo "$(date): Starting maintenance tasks" >> $LOG_FILE

# Rotate logs
find /var/log/collegiumai -name "*.log" -size +100M -exec gzip {} \;
find /var/log/collegiumai -name "*.gz" -mtime +30 -delete

# Clean temporary files
find /tmp -name "collegiumai_*" -mtime +1 -delete

# Update system packages (if needed)
apt list --upgradable | grep -i security && apt update && apt upgrade -y

# Restart services if needed
if systemctl is-failed --quiet collegiumai; then
    systemctl restart collegiumai
    echo "$(date): Restarted CollegiumAI service" >> $LOG_FILE
fi

# Database maintenance
sudo -u postgres vacuumdb --all --analyze --verbose

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "$(date): WARNING - Disk usage at ${DISK_USAGE}%" >> $LOG_FILE
    # Send alert email
    echo "Disk usage critical on CollegiumAI server: ${DISK_USAGE}%" | mail -s "CollegiumAI Disk Alert" admin@university.edu
fi

echo "$(date): Maintenance tasks completed" >> $LOG_FILE
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Error: ModuleNotFoundError
# Solution: Check virtual environment and dependencies
source venv/bin/activate
pip install -r requirements.txt
python -c "import sys; print(sys.path)"
```

#### 2. Memory Issues

```bash
# Error: Out of memory
# Solution: Increase system memory or optimize configuration
# Reduce MAX_CONCURRENT_REQUESTS in .env
# Monitor with: htop or top
```

#### 3. Database Connection Issues

```bash
# Error: Database connection failed
# Solution: Check database status and credentials
sudo systemctl status postgresql
psql -h localhost -U collegiumai -d collegiumai -c "SELECT 1;"
```

#### 4. Port Already in Use

```bash
# Error: Port 8000 already in use
# Solution: Find and kill process or use different port
sudo lsof -i :8000
sudo kill -9 PID
# Or change port in configuration
```

### Diagnostic Commands

```bash
# System status
systemctl status collegiumai
journalctl -u collegiumai -f

# Performance check
python health_check.py

# Network connectivity
curl -v http://localhost:8000/health
netstat -tlnp | grep 8000

# Database connectivity
psql -h localhost -U collegiumai -c "SELECT version();"

# Log analysis
tail -f /var/log/collegiumai/app.log
grep -i error /var/log/collegiumai/app.log
```

### Recovery Procedures

#### Service Recovery

```bash
# If service crashes
sudo systemctl stop collegiumai
sudo systemctl start collegiumai
sudo systemctl status collegiumai

# If database issues
sudo systemctl restart postgresql
sudo systemctl restart redis-server
```

#### Data Recovery

```bash
# Restore from backup
sudo systemctl stop collegiumai
psql -h localhost -U collegiumai -d collegiumai < /backups/collegiumai/db_backup_latest.sql
sudo systemctl start collegiumai
```

---

## Security Considerations

### SSL/TLS Configuration

```bash
# Generate SSL certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d collegiumai.university.edu
```

### Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw deny 8000  # Block direct access to application port
```

### Security Hardening

```bash
# Disable unused services
sudo systemctl disable apache2
sudo systemctl disable sendmail

# Update system regularly
sudo apt update && sudo apt upgrade -y

# Monitor failed login attempts
sudo fail2ban-client status
```

---

**Your CollegiumAI v1.0.0 "Cognitive Genesis" is now ready for production deployment! Choose the deployment method that best fits your requirements and follow the appropriate section above.**

For additional support, see [CONTRIBUTING.md](CONTRIBUTING.md) or [SECURITY.md](SECURITY.md).