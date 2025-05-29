# Function to check if a command exists
function Test-CommandExists {
    param (
        [string]$command
    )
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try { 
        if (Get-Command $command) { 
            return $true 
        }
    }
    catch { 
        return $false 
    }
    finally { 
        $ErrorActionPreference = $oldPreference 
    }
}

Write-Host "🚀 Starting Smart Cloud Autoscaler..." -ForegroundColor Green

# Check prerequisites
Write-Host "🔍 Checking prerequisites..."

# Check Python
if (-not (Test-CommandExists python)) {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    exit 1
}

# Check Node.js
if (-not (Test-CommandExists node)) {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    exit 1
}

# Check Docker
if (-not (Test-CommandExists docker)) {
    Write-Host "❌ Docker is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ All prerequisites met" -ForegroundColor Green

# Start backend
Write-Host "🚀 Starting backend..."
Set-Location backend

# Create and activate virtual environment if it doesn't exist
if (-not (Test-Path venv)) {
    Write-Host "📦 Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📥 Installing backend dependencies..."
pip install -r requirements.txt

# Create models directory if it doesn't exist
if (-not (Test-Path "app\models")) {
    New-Item -ItemType Directory -Force -Path app\models
}

# Start backend in background
Write-Host "🚀 Starting FastAPI server..."
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "app.main:app --reload --port 8000"

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..."
Start-Sleep -Seconds 5

# Start frontend
Write-Host "🚀 Starting frontend..."
Set-Location ..\frontend

# Install dependencies
Write-Host "📥 Installing frontend dependencies..."
npm install

# Start frontend in background
Write-Host "🚀 Starting React development server..."
Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "start"

# Start monitoring stack
Write-Host "🚀 Starting monitoring stack..."
Set-Location ..
docker-compose up -d prometheus grafana

Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000"
Write-Host "🔧 Backend API: http://localhost:8000"
Write-Host "📊 Prometheus: http://localhost:9090"
Write-Host "📈 Grafana: http://localhost:3000 (admin/admin)"

# Keep PowerShell window open
Write-Host "`nPress Ctrl+C to stop all services..."
try {
    while ($true) { Start-Sleep -Seconds 1 }
}
catch {
    # Empty catch block to satisfy PowerShell syntax
}
finally {
    Write-Host "`n🛑 Stopping services..."
    Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process
    docker-compose down
} 