@echo off
REM SnapChef Startup Script for Windows
echo 🍳 Starting SnapChef - Real-time Recipe Search System
echo ==================================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit .env file and add your Hugging Face API key
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist data mkdir data
if not exist logs mkdir logs

REM Build and start Docker containers
echo 🐳 Building and starting Docker containers...
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service health...

REM Check Redis
docker-compose exec -T redis redis-cli ping | findstr "PONG" >nul
if %errorlevel% equ 0 (
    echo ✅ Redis is running
) else (
    echo ❌ Redis is not responding
)

REM Check Elasticsearch
curl -s http://localhost:9200/_cluster/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Elasticsearch is running
) else (
    echo ❌ Elasticsearch is not responding
)

REM Check Backend API
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend API is running
) else (
    echo ❌ Backend API is not responding
)

REM Check Frontend
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend is running
) else (
    echo ❌ Frontend is not responding
)

echo.
echo 🎉 SnapChef is starting up!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📊 API Docs: http://localhost:8000/docs
echo.
echo Press any key to view logs or Ctrl+C to stop all services
pause >nul

REM Show logs
docker-compose logs -f
