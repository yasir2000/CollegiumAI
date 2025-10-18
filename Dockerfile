# Use Python 3.11 slim image
FROM python:3.11-slim

# Set metadata
LABEL name="CollegiumAI"
LABEL version="1.0.0"
LABEL description="Advanced University Intelligence Platform"
LABEL maintainer="yasir2000"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    wget \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 collegiumai && \
    chown -R collegiumai:collegiumai /app && \
    chmod +x /app/deploy.sh

# Switch to non-root user
USER collegiumai

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/backups

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=10)" || exit 1

# Default command
CMD ["python", "main.py", "--mode=server", "--host=0.0.0.0", "--port=8000"]