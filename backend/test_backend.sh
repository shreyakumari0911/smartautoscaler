#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🧪 Testing Smart Cloud Autoscaler Backend"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed${NC}"
    exit 1
fi

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
pip install pytest pytest-cov

# Run tests
echo "🚀 Running tests..."
pytest tests/ -v --cov=app

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi

# Start the server in the background
echo "🚀 Starting server..."
uvicorn app.main:app --reload --port 8000 &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Test endpoints
echo "🔍 Testing endpoints..."

# Test root endpoint
curl -s http://localhost:8000/ | grep -q "healthy"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Root endpoint OK${NC}"
else
    echo -e "${RED}❌ Root endpoint failed${NC}"
fi

# Test health endpoint
curl -s http://localhost:8000/health | grep -q "healthy"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Health endpoint OK${NC}"
else
    echo -e "${RED}❌ Health endpoint failed${NC}"
fi

# Test metrics endpoint
curl -s http://localhost:8000/metrics | grep -q "cpu_usage_percent"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Metrics endpoint OK${NC}"
else
    echo -e "${RED}❌ Metrics endpoint failed${NC}"
fi

# Test system metrics endpoint
curl -s http://localhost:8000/system/current | grep -q "cpu_usage"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ System metrics endpoint OK${NC}"
else
    echo -e "${RED}❌ System metrics endpoint failed${NC}"
fi

# Stop the server
echo "🛑 Stopping server..."
kill $SERVER_PID

echo "✨ Testing complete!" 