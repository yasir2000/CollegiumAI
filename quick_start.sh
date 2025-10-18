#!/bin/bash

# Quick CollegiumAI Deployment - Fast Setup
# Version: 1.0.0

set -e

echo "🚀 CollegiumAI Quick Deploy - 30 seconds to running!"
echo "================================================="

# Check if Python is available
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install minimal dependencies for demo
echo "📥 Installing core dependencies..."
pip install --quiet --upgrade pip
pip install --quiet numpy pandas asyncio aiohttp

# Create minimal config
if [ ! -f ".env" ]; then
    echo "⚙️ Creating configuration..."
    cat > .env << EOF
DEBUG=true
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=5
SESSION_TIMEOUT=3600
EOF
fi

# Quick test
echo "🧪 Running quick validation..."
$PYTHON_CMD quick_test.py || echo "⚠️ Some tests failed, but continuing..."

# Start the system
echo "🎉 Starting CollegiumAI..."
echo "📍 Access at: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop"
echo "================================================="

$PYTHON_CMD main.py --mode=demo