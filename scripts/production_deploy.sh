#!/bin/bash

# CollegiumAI Production Deployment Script
# Version: 1.0.0 "Cognitive Genesis"
# For Ubuntu/Debian-based systems

set -euo pipefail

# Configuration
PROJECT_NAME="CollegiumAI"
PROJECT_DIR="/opt/collegiumai"
SERVICE_USER="collegiumai"
DOMAIN_NAME="${DOMAIN_NAME:-localhost}"
SSL_EMAIL="${SSL_EMAIL:-admin@localhost}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() { echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"; }
warn() { echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"; }
error() { echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"; exit 1; }
info() { echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"; }

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root (use sudo)"
    fi
}

# Update system packages
update_system() {
    log "Updating system packages..."
    apt update && apt upgrade -y
    apt install -y curl wget git software-properties-common apt-transport-https ca-certificates gnupg lsb-release
}

# Install Python 3.11
install_python() {
    log "Installing Python 3.11..."
    
    if ! command -v python3.11 &> /dev/null; then
        add-apt-repository ppa:deadsnakes/ppa -y
        apt update
        apt install -y python3.11 python3.11-venv python3.11-pip python3.11-dev
    fi
    
    # Set Python 3.11 as default python3
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    
    python3 --version
    log "Python 3.11 installed ✓"
}

# Install PostgreSQL
install_postgresql() {
    log "Installing PostgreSQL..."
    
    if ! command -v psql &> /dev/null; then
        apt install -y postgresql postgresql-contrib
        systemctl enable postgresql
        systemctl start postgresql
    fi
    
    # Create database and user
    sudo -u postgres psql << EOF
CREATE USER IF NOT EXISTS $SERVICE_USER WITH PASSWORD '$SERVICE_USER\_pass';
CREATE DATABASE IF NOT EXISTS $SERVICE_USER OWNER $SERVICE_USER;
GRANT ALL PRIVILEGES ON DATABASE $SERVICE_USER TO $SERVICE_USER;
ALTER USER $SERVICE_USER CREATEDB;
\q
EOF
    
    log "PostgreSQL installed and configured ✓"
}

# Install Redis
install_redis() {
    log "Installing Redis..."
    
    if ! command -v redis-server &> /dev/null; then
        apt install -y redis-server
        systemctl enable redis-server
        systemctl start redis-server
    fi
    
    # Configure Redis
    sed -i 's/^# requirepass.*/requirepass redis_pass/' /etc/redis/redis.conf
    systemctl restart redis-server
    
    log "Redis installed and configured ✓"
}

# Install Nginx
install_nginx() {
    log "Installing Nginx..."
    
    if ! command -v nginx &> /dev/null; then
        apt install -y nginx
        systemctl enable nginx
        systemctl start nginx
    fi
    
    # Remove default site
    rm -f /etc/nginx/sites-enabled/default
    
    log "Nginx installed ✓"
}

# Install Docker (optional)
install_docker() {
    log "Installing Docker..."
    
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
        apt update
        apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        systemctl enable docker
        systemctl start docker
        
        # Add service user to docker group
        usermod -aG docker $SERVICE_USER
    fi
    
    log "Docker installed ✓"
}

# Create service user
create_service_user() {
    log "Creating service user..."
    
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd -r -m -s /bin/bash $SERVICE_USER
        usermod -aG sudo $SERVICE_USER
    fi
    
    log "Service user '$SERVICE_USER' created ✓"
}

# Setup application directory
setup_application() {
    log "Setting up application..."
    
    # Create project directory
    mkdir -p $PROJECT_DIR
    chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR
    
    # Clone repository as service user
    sudo -u $SERVICE_USER bash << EOF
cd $PROJECT_DIR
if [ ! -d ".git" ]; then
    git clone https://github.com/yasir2000/CollegiumAI.git .
else
    git pull origin main
fi

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs data backups config
EOF
    
    log "Application setup completed ✓"
}

# Configure environment
configure_environment() {
    log "Configuring environment..."
    
    # Create .env file
    sudo -u $SERVICE_USER bash << EOF
cd $PROJECT_DIR
if [ ! -f ".env" ]; then
    cp .env.example .env
    
    # Update configuration for production
    sed -i 's/DEBUG=true/DEBUG=false/' .env
    sed -i 's/LOG_LEVEL=DEBUG/LOG_LEVEL=INFO/' .env
    sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$SERVICE_USER:${SERVICE_USER}_pass@localhost:5432/$SERVICE_USER|" .env
    sed -i 's|REDIS_URL=.*|REDIS_URL=redis://:redis_pass@localhost:6379/0|' .env
    
    # Generate secret keys
    SECRET_KEY=\$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    JWT_SECRET=\$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=\$SECRET_KEY/" .env
    sed -i "s/JWT_SECRET=.*/JWT_SECRET=\$JWT_SECRET/" .env
fi
EOF
    
    log "Environment configured ✓"
}

# Create systemd service
create_systemd_service() {
    log "Creating systemd service..."
    
    cat > /etc/systemd/system/collegiumai.service << EOF
[Unit]
Description=CollegiumAI University Assistant v1.0.0
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python main.py --mode=server --host=127.0.0.1 --port=8000
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=collegiumai

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$PROJECT_DIR

# Resource limits
LimitNOFILE=65536
LimitNPROC=32768

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable collegiumai
    
    log "Systemd service created ✓"
}

# Configure Nginx
configure_nginx() {
    log "Configuring Nginx..."
    
    # Create Nginx configuration
    cat > /etc/nginx/sites-available/collegiumai << EOF
# HTTP redirect to HTTPS
server {
    listen 80;
    server_name $DOMAIN_NAME;
    return 301 https://\$server_name\$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name $DOMAIN_NAME;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";

    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;

    location / {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }

    # Logging
    access_log /var/log/nginx/collegiumai_access.log;
    error_log /var/log/nginx/collegiumai_error.log;
}
EOF
    
    # Enable site
    ln -sf /etc/nginx/sites-available/collegiumai /etc/nginx/sites-enabled/
    
    # Test configuration
    nginx -t
    
    log "Nginx configured ✓"
}

# Setup SSL with Let's Encrypt
setup_ssl() {
    log "Setting up SSL certificate..."
    
    if [[ "$DOMAIN_NAME" != "localhost" ]]; then
        # Install certbot
        if ! command -v certbot &> /dev/null; then
            apt install -y certbot python3-certbot-nginx
        fi
        
        # Get certificate
        certbot --nginx -d $DOMAIN_NAME --email $SSL_EMAIL --agree-tos --non-interactive
        
        # Setup auto-renewal
        systemctl enable certbot.timer
        systemctl start certbot.timer
        
        log "SSL certificate installed ✓"
    else
        warn "Skipping SSL setup for localhost"
        
        # Create self-signed certificate for testing
        mkdir -p /etc/ssl/private /etc/ssl/certs
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout /etc/ssl/private/collegiumai.key \
            -out /etc/ssl/certs/collegiumai.crt \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        
        # Update Nginx config for self-signed certificate
        sed -i 's|/etc/letsencrypt/live/.*/fullchain.pem|/etc/ssl/certs/collegiumai.crt|' /etc/nginx/sites-available/collegiumai
        sed -i 's|/etc/letsencrypt/live/.*/privkey.pem|/etc/ssl/private/collegiumai.key|' /etc/nginx/sites-available/collegiumai
    fi
}

# Configure firewall
configure_firewall() {
    log "Configuring firewall..."
    
    if command -v ufw &> /dev/null; then
        ufw --force enable
        ufw default deny incoming
        ufw default allow outgoing
        ufw allow ssh
        ufw allow 'Nginx Full'
        ufw deny 8000  # Block direct access to application
        ufw deny 5432  # Block direct database access
        ufw deny 6379  # Block direct Redis access
        
        ufw --force reload
        log "Firewall configured ✓"
    else
        warn "UFW not available, skipping firewall configuration"
    fi
}

# Setup monitoring and logging
setup_monitoring() {
    log "Setting up monitoring and logging..."
    
    # Setup log rotation
    cat > /etc/logrotate.d/collegiumai << EOF
$PROJECT_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload collegiumai
    endscript
}
EOF
    
    # Setup system monitoring script
    cat > /usr/local/bin/collegiumai-monitor << 'EOF'
#!/bin/bash
# CollegiumAI Health Monitor

SERVICE_NAME="collegiumai"
LOG_FILE="/var/log/collegiumai-monitor.log"

check_service() {
    if ! systemctl is-active --quiet $SERVICE_NAME; then
        echo "$(date): $SERVICE_NAME is not running, attempting restart" >> $LOG_FILE
        systemctl restart $SERVICE_NAME
        sleep 10
        
        if systemctl is-active --quiet $SERVICE_NAME; then
            echo "$(date): $SERVICE_NAME restarted successfully" >> $LOG_FILE
        else
            echo "$(date): Failed to restart $SERVICE_NAME" >> $LOG_FILE
        fi
    fi
}

check_health() {
    if ! curl -f -s http://localhost:8000/health > /dev/null; then
        echo "$(date): Health check failed" >> $LOG_FILE
        systemctl restart $SERVICE_NAME
    fi
}

check_service
check_health
EOF
    
    chmod +x /usr/local/bin/collegiumai-monitor
    
    # Setup cron job for monitoring
    (crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/collegiumai-monitor") | crontab -
    
    log "Monitoring setup completed ✓"
}

# Initialize database
initialize_database() {
    log "Initializing database..."
    
    sudo -u $SERVICE_USER bash << EOF
cd $PROJECT_DIR
source venv/bin/activate

# Run database initialization if it exists
if [ -f "scripts/init_db.sql" ]; then
    PGPASSWORD="${SERVICE_USER}_pass" psql -h localhost -U $SERVICE_USER -d $SERVICE_USER -f scripts/init_db.sql
fi

# Run any Python database setup
if [ -f "scripts/setup_db.py" ]; then
    python scripts/setup_db.py
fi
EOF
    
    log "Database initialized ✓"
}

# Start services
start_services() {
    log "Starting services..."
    
    # Start PostgreSQL and Redis
    systemctl restart postgresql
    systemctl restart redis-server
    
    # Start CollegiumAI
    systemctl restart collegiumai
    
    # Start Nginx
    systemctl restart nginx
    
    # Wait for services to start
    sleep 10
    
    log "Services started ✓"
}

# Verify deployment
verify_deployment() {
    log "Verifying deployment..."
    
    local checks_passed=0
    local total_checks=5
    
    # Check systemd service
    if systemctl is-active --quiet collegiumai; then
        info "✓ CollegiumAI service is running"
        ((checks_passed++))
    else
        warn "✗ CollegiumAI service is not running"
    fi
    
    # Check database connection
    if sudo -u $SERVICE_USER PGPASSWORD="${SERVICE_USER}_pass" psql -h localhost -U $SERVICE_USER -d $SERVICE_USER -c "SELECT 1;" > /dev/null 2>&1; then
        info "✓ Database connection successful"
        ((checks_passed++))
    else
        warn "✗ Database connection failed"
    fi
    
    # Check Redis connection
    if redis-cli -a redis_pass ping > /dev/null 2>&1; then
        info "✓ Redis connection successful"
        ((checks_passed++))
    else
        warn "✗ Redis connection failed"
    fi
    
    # Check HTTP health endpoint
    if curl -f -s http://localhost(8000/health > /dev/null; then
        info "✓ Health endpoint responding"
        ((checks_passed++))
    else
        warn "✗ Health endpoint not responding"
    fi
    
    # Check Nginx
    if systemctl is-active --quiet nginx; then
        info "✓ Nginx is running"
        ((checks_passed++))
    else
        warn "✗ Nginx is not running"
    fi
    
    if [[ $checks_passed -eq $total_checks ]]; then
        log "All deployment checks passed! ($checks_passed/$total_checks) ✓"
        return 0
    else
        warn "Some deployment checks failed ($checks_passed/$total_checks)"
        return 1
    fi
}

# Print deployment summary
print_summary() {
    echo
    echo "=============================================="
    echo "   CollegiumAI Production Deployment Summary"
    echo "=============================================="
    echo "Domain: $DOMAIN_NAME"
    echo "Application Directory: $PROJECT_DIR"
    echo "Service User: $SERVICE_USER"
    echo "Database: PostgreSQL (localhost:5432)"
    echo "Cache: Redis (localhost:6379)"
    echo "Web Server: Nginx"
    echo "SSL: $([ "$DOMAIN_NAME" != "localhost" ] && echo "Let's Encrypt" || echo "Self-signed")"
    echo "=============================================="
    echo
    echo "Service Management:"
    echo "  Start:   sudo systemctl start collegiumai"
    echo "  Stop:    sudo systemctl stop collegiumai"
    echo "  Restart: sudo systemctl restart collegiumai"
    echo "  Status:  sudo systemctl status collegiumai"
    echo "  Logs:    sudo journalctl -u collegiumai -f"
    echo
    echo "Application URLs:"
    echo "  HTTPS: https://$DOMAIN_NAME"
    echo "  HTTP:  http://$DOMAIN_NAME (redirects to HTTPS)"
    echo "  Health: https://$DOMAIN_NAME/health"
    echo
    echo "Configuration Files:"
    echo "  App Config: $PROJECT_DIR/.env"
    echo "  Nginx Config: /etc/nginx/sites-available/collegiumai"
    echo "  Service Config: /etc/systemd/system/collegiumai.service"
    echo "=============================================="
}

# Main deployment function
main() {
    echo "🎓 CollegiumAI Production Deployment v1.0.0"
    echo "============================================="
    
    log "Starting production deployment..."
    
    check_root
    update_system
    install_python
    install_postgresql
    install_redis
    install_nginx
    create_service_user
    setup_application
    configure_environment
    initialize_database
    create_systemd_service
    configure_nginx
    setup_ssl
    configure_firewall
    setup_monitoring
    start_services
    
    if verify_deployment; then
        print_summary
        log "🎉 Production deployment completed successfully!"
        info "Your CollegiumAI instance is now running at: https://$DOMAIN_NAME"
    else
        error "Deployment verification failed. Please check the logs and fix any issues."
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN_NAME="$2"
            shift 2
            ;;
        --email)
            SSL_EMAIL="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --domain DOMAIN    Domain name for SSL certificate"
            echo "  --email EMAIL      Email for Let's Encrypt"
            echo "  --help            Show this help"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

# Run main function
main "$@"