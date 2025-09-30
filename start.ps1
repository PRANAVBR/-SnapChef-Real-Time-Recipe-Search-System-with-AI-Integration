# SnapChef PowerShell Startup Script
Write-Host "🍳 Starting SnapChef - Real-time Recipe Search System" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "⚠️  Please edit .env file and add your Hugging Face API key" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Blue
if (-not (Test-Path "data")) { New-Item -ItemType Directory -Name "data" }
if (-not (Test-Path "logs")) { New-Item -ItemType Directory -Name "logs" }

# Build and start Docker containers
Write-Host "🐳 Building and starting Docker containers..." -ForegroundColor Blue
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check if services are running
Write-Host "🔍 Checking service health..." -ForegroundColor Blue

# Check Redis
try {
    $redisCheck = docker-compose exec -T redis redis-cli ping 2>$null
    if ($redisCheck -match "PONG") {
        Write-Host "✅ Redis is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Redis is not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Redis is not responding" -ForegroundColor Red
}

# Check Elasticsearch
try {
    $esResponse = Invoke-WebRequest -Uri "http://localhost:9200/_cluster/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($esResponse.StatusCode -eq 200) {
        Write-Host "✅ Elasticsearch is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Elasticsearch is not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Elasticsearch is not responding" -ForegroundColor Red
}

# Check Backend API
try {
    $apiResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($apiResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend API is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend API is not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Backend API is not responding" -ForegroundColor Red
}

# Check Frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Frontend is not responding" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Frontend is not responding" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 SnapChef is starting up!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow

# Show logs
docker-compose logs -f
