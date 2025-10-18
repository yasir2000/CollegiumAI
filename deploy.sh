#!/bin/bash

# CollegiumAI Deployment Automation Script
# Version: 1.0.0 "Cognitive Genesis"
# Usage: ./deploy.sh [environment] [options]

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VERSION="1.0.0"
PROJECT_NAME="CollegiumAI"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Default values
ENVIRONMENT="development"
SKIP_TESTS=false
SKIP_BACKUP=false
FORCE_DEPLOY=false
DRY_RUN=false

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --skip-backup)
                SKIP_BACKUP=true
                shift
                ;;
            --force)
                FORCE_DEPLOY=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done
}

show_help() {
    cat << EOF
CollegiumAI Deployment Script v$VERSION

Usage: $0 [OPTIONS]

OPTIONS:
    -e, --environment    Target environment (development, staging, production)
    --skip-tests         Skip running tests before deployment
    --skip-backup        Skip creating backup before deployment
    --force              Force deployment even if tests fail
    --dry-run            Show what would be done without executing
    -h, --help           Show this help message

ENVIRONMENTS:
    development          Local development deployment
    staging              Staging environment deployment
    production           Production environment deployment
    docker               Docker containerized deployment
    institutional        University server deployment

EXAMPLES:
    $0 --environment development
    $0 --environment production --skip-tests
    $0 --environment docker --dry-run

EOF
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed"
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2)
    local python_major=$(echo $python_version | cut -d'.' -f1)
    local python_minor=$(echo $python_version | cut -d'.' -f2)
    
    if [[ $python_major -lt 3 ]] || [[ $python_minor -lt 8 ]]; then
        error "Python 3.8+ is required. Found: $python_version"
    fi
    
    info "Python version: $python_version ✓"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        error "pip3 is not installed"
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        error "git is not installed"
    fi
    
    # Environment-specific checks
    case $ENVIRONMENT in
        docker)
            if ! command -v docker &> /dev/null; then
                error "Docker is not installed"
            fi
            if ! command -v docker-compose &> /dev/null; then
                error "Docker Compose is not installed"
            fi
            ;;
        production|institutional)
            if ! command -v nginx &> /dev/null; then
                warn "Nginx is not installed - required for production"
            fi
            if ! command -v postgresql &> /dev/null; then
                warn "PostgreSQL is not installed - database required"
            fi
            ;;
    esac
    
    log "Prerequisites check completed ✓"
}

# Create virtual environment
setup_venv() {
    log "Setting up virtual environment..."
    
    local venv_path="$PROJECT_DIR/venv"
    
    if [[ ! -d "$venv_path" ]]; then
        if [[ $DRY_RUN == true ]]; then
            info "[DRY RUN] Would create virtual environment at $venv_path"
        else
            python3 -m venv "$venv_path"
        fi
    else
        info "Virtual environment already exists"
    fi
    
    if [[ $DRY_RUN == false ]]; then
        source "$venv_path/bin/activate"
        pip install --upgrade pip
        log "Virtual environment ready ✓"
    fi
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."
    
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would install dependencies from requirements.txt"
        return
    fi
    
    if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then
        pip install -r "$PROJECT_DIR/requirements.txt"
        log "Dependencies installed ✓"
    else
        error "requirements.txt not found"
    fi
}

# Run tests
run_tests() {
    if [[ $SKIP_TESTS == true ]]; then
        warn "Skipping tests as requested"
        return
    fi
    
    log "Running tests..."
    
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would run test suite"
        return
    fi
    
    local test_results=0
    
    # Quick test
    if [[ -f "$PROJECT_DIR/quick_test.py" ]]; then
        python "$PROJECT_DIR/quick_test.py" || test_results=$?
    fi
    
    # Comprehensive test suite
    if [[ -f "$PROJECT_DIR/comprehensive_test_suite.py" ]]; then
        python "$PROJECT_DIR/comprehensive_test_suite.py" || test_results=$?
    fi
    
    if [[ $test_results -ne 0 ]]; then
        if [[ $FORCE_DEPLOY == true ]]; then
            warn "Tests failed but continuing due to --force flag"
        else
            error "Tests failed. Use --force to deploy anyway or fix the issues."
        fi
    else
        log "Tests passed ✓"
    fi
}

# Create backup
create_backup() {
    if [[ $SKIP_BACKUP == true ]]; then
        warn "Skipping backup as requested"
        return
    fi
    
    log "Creating backup..."
    
    local backup_dir="$PROJECT_DIR/backups"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$backup_dir/backup_$timestamp.tar.gz"
    
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would create backup at $backup_file"
        return
    fi
    
    mkdir -p "$backup_dir"
    
    # Create application backup
    tar -czf "$backup_file" \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.git' \
        --exclude='backups' \
        "$PROJECT_DIR"
    
    log "Backup created: $backup_file ✓"
}

# Environment-specific configuration
configure_environment() {
    log "Configuring for $ENVIRONMENT environment..."
    
    local env_file="$PROJECT_DIR/.env"
    local env_template="$PROJECT_DIR/.env.example"
    
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would configure environment: $ENVIRONMENT"
        return
    fi
    
    # Copy template if .env doesn't exist
    if [[ ! -f "$env_file" ]] && [[ -f "$env_template" ]]; then
        cp "$env_template" "$env_file"
        warn "Created .env from template - please review and update configuration"
    fi
    
    # Environment-specific configurations
    case $ENVIRONMENT in
        development)
            sed -i 's/DEBUG=false/DEBUG=true/' "$env_file" 2>/dev/null || true
            sed -i 's/LOG_LEVEL=INFO/LOG_LEVEL=DEBUG/' "$env_file" 2>/dev/null || true
            ;;
        staging)
            sed -i 's/DEBUG=true/DEBUG=false/' "$env_file" 2>/dev/null || true
            sed -i 's/LOG_LEVEL=DEBUG/LOG_LEVEL=INFO/' "$env_file" 2>/dev/null || true
            ;;
        production)
            sed -i 's/DEBUG=true/DEBUG=false/' "$env_file" 2>/dev/null || true
            sed -i 's/LOG_LEVEL=DEBUG/LOG_LEVEL=WARNING/' "$env_file" 2>/dev/null || true
            ;;
    esac
    
    log "Environment configuration completed ✓"
}

# Deploy based on environment
deploy_application() {
    log "Deploying to $ENVIRONMENT environment..."
    
    case $ENVIRONMENT in
        development)
            deploy_development
            ;;
        staging)
            deploy_staging
            ;;
        production)
            deploy_production
            ;;
        docker)
            deploy_docker
            ;;
        institutional)
            deploy_institutional
            ;;
        *)
            error "Unknown environment: $ENVIRONMENT"
            ;;
    esac
}

# Development deployment
deploy_development() {
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would start development server"
        return
    fi
    
    log "Starting development server..."
    python "$PROJECT_DIR/main.py" --mode=interactive &
    local server_pid=$!
    
    sleep 5
    
    # Verify deployment
    if kill -0 $server_pid 2>/dev/null; then
        log "Development server started successfully (PID: $server_pid) ✓"
        info "Access the application at: http://localhost:8000"
    else
        error "Failed to start development server"
    fi
}

# Docker deployment
deploy_docker() {
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would build and start Docker containers"
        return
    fi
    
    log "Building Docker containers..."
    docker-compose build
    
    log "Starting Docker services..."
    docker-compose up -d
    
    # Wait for services to be ready
    sleep 10
    
    # Verify deployment
    if docker-compose ps | grep -q "Up"; then
        log "Docker deployment successful ✓"
        info "Access the application at: http://localhost:8000"
    else
        error "Docker deployment failed"
    fi
}

# Production deployment
deploy_production() {
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would deploy to production with systemd service"
        return
    fi
    
    log "Deploying to production..."
    
    # Create systemd service if it doesn't exist
    local service_file="/etc/systemd/system/collegiumai.service"
    if [[ ! -f "$service_file" ]]; then
        create_systemd_service
    fi
    
    # Reload systemd and restart service
    sudo systemctl daemon-reload
    sudo systemctl enable collegiumai
    sudo systemctl restart collegiumai
    
    # Wait for service to start
    sleep 10
    
    # Verify deployment
    if systemctl is-active --quiet collegiumai; then
        log "Production deployment successful ✓"
        info "Service status: $(systemctl is-active collegiumai)"
    else
        error "Production deployment failed - check logs with: journalctl -u collegiumai"
    fi
}

# Institutional deployment
deploy_institutional() {
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would deploy to institutional environment"
        return
    fi
    
    log "Deploying to institutional environment..."
    
    # Similar to production but with additional security measures
    deploy_production
    
    # Configure nginx if needed
    configure_nginx
    
    log "Institutional deployment completed ✓"
}

# Staging deployment
deploy_staging() {
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would deploy to staging environment"
        return
    fi
    
    log "Deploying to staging environment..."
    
    # Similar to production but with staging configuration
    deploy_production
    
    log "Staging deployment completed ✓"
}

# Create systemd service
create_systemd_service() {
    log "Creating systemd service..."
    
    local service_content="[Unit]
Description=CollegiumAI University Assistant
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python main.py --mode=server --host=127.0.0.1 --port=8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target"
    
    echo "$service_content" | sudo tee /etc/systemd/system/collegiumai.service > /dev/null
    log "Systemd service created ✓"
}

# Configure nginx
configure_nginx() {
    log "Configuring nginx..."
    
    local nginx_config="/etc/nginx/sites-available/collegiumai"
    
    if [[ ! -f "$nginx_config" ]]; then
        warn "Nginx configuration not found - creating basic configuration"
        
        local config_content="server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}"
        
        echo "$config_content" | sudo tee "$nginx_config" > /dev/null
        sudo ln -sf "$nginx_config" /etc/nginx/sites-enabled/
        sudo nginx -t && sudo systemctl reload nginx
        
        log "Basic nginx configuration created ✓"
    fi
}

# Post-deployment verification
verify_deployment() {
    log "Verifying deployment..."
    
    if [[ $DRY_RUN == true ]]; then
        info "[DRY RUN] Would verify deployment"
        return
    fi
    
    local max_attempts=30
    local attempt=1
    local success=false
    
    while [[ $attempt -le $max_attempts ]]; do
        info "Verification attempt $attempt/$max_attempts..."
        
        case $ENVIRONMENT in
            development|docker)
                if curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
                    success=true
                    break
                fi
                ;;
            production|staging|institutional)
                if systemctl is-active --quiet collegiumai; then
                    success=true
                    break
                fi
                ;;
        esac
        
        sleep 2
        ((attempt++))
    done
    
    if [[ $success == true ]]; then
        log "Deployment verification successful ✓"
    else
        error "Deployment verification failed"
    fi
}

# Cleanup function
cleanup() {
    log "Performing cleanup..."
    
    # Clean up temporary files
    find "$PROJECT_DIR" -name "*.pyc" -delete 2>/dev/null || true
    find "$PROJECT_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Clean old backups (keep last 5)
    if [[ -d "$PROJECT_DIR/backups" ]]; then
        cd "$PROJECT_DIR/backups"
        ls -t backup_*.tar.gz | tail -n +6 | xargs rm -f 2>/dev/null || true
    fi
    
    log "Cleanup completed ✓"
}

# Print deployment summary
print_summary() {
    echo
    echo "=============================================="
    echo "     CollegiumAI Deployment Summary"
    echo "=============================================="
    echo "Environment: $ENVIRONMENT"
    echo "Version: $VERSION"
    echo "Timestamp: $(date)"
    echo "=============================================="
    
    case $ENVIRONMENT in
        development)
            echo "Access URL: http://localhost:8000"
            echo "Logs: Check terminal output"
            ;;
        docker)
            echo "Access URL: http://localhost:8000"
            echo "Logs: docker-compose logs -f collegiumai"
            ;;
        production|staging|institutional)
            echo "Service: systemctl status collegiumai"
            echo "Logs: journalctl -u collegiumai -f"
            echo "Nginx: systemctl status nginx"
            ;;
    esac
    
    echo "=============================================="
    echo
}

# Main deployment function
main() {
    echo "🎓 CollegiumAI Deployment Script v$VERSION"
    echo "=========================================="
    
    parse_args "$@"
    
    if [[ $DRY_RUN == true ]]; then
        warn "DRY RUN MODE - No changes will be made"
    fi
    
    # Deployment steps
    check_prerequisites
    setup_venv
    install_dependencies
    run_tests
    create_backup
    configure_environment
    deploy_application
    verify_deployment
    cleanup
    print_summary
    
    log "🎉 Deployment completed successfully!"
}

# Error handling
trap 'error "Deployment failed at line $LINENO"' ERR

# Run main function
main "$@"