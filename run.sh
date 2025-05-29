#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Starting Smart Cloud Autoscaler..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command_exists python; then
    echo -e "${RED}❌ Python is not installed${NC}"
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

# Check Docker
if ! command_exists docker; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

# Check Docker Compose
if ! command_exists docker-compose; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"

# Start backend
echo "🚀 Starting backend..."
cd backend

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "📥 Installing backend dependencies..."
pip install -r requirements.txt

# Create models directory if it doesn't exist
mkdir -p app/models

# Start backend in background
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend
echo "🚀 Starting frontend..."
cd ../frontend

# Install dependencies
echo "📥 Installing frontend dependencies..."
npm install

# Start frontend in background
echo "🚀 Starting React development server..."
npm start &
FRONTEND_PID=$!

# Start monitoring stack
echo "🚀 Starting monitoring stack..."
cd ..
docker-compose up -d prometheus grafana

# Function to handle cleanup
cleanup() {
    echo "🛑 Stopping services..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    docker-compose down
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}✅ All services started!${NC}"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Prometheus: http://localhost:9090"
echo "📈 Grafana: http://localhost:3000 (admin/admin)"

# Keep script running
wait 