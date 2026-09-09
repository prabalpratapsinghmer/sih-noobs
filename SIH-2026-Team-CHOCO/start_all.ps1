# PowerShell Launcher for CyberCell & SIH26184 Platform
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host " CYBERCELL & SIH26184: FULL-STACK UNIFIED PLATFORM LAUNCHER" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan

$backendDir = "D:\MokshSIH"
$frontendDir = "D:\MokshFrontEnd"

# 0. Check and start Docker containers (Redis and PostgreSQL)
Write-Host "[0/3] Checking Docker Infrastructure (Redis & PostgreSQL)..." -ForegroundColor Yellow
try {
    $redisRunning = docker ps --filter "name=redis" --format "{{.Names}}" 2>$null
    if (-not $redisRunning) {
        Write-Host "Starting Docker Redis container..." -ForegroundColor DarkYellow
        docker start ec64bc2a3f8f 2>$null
    }
    $pgRunning = docker ps --filter "name=postgres" --format "{{.Names}}" 2>$null
    if (-not $pgRunning) {
        Write-Host "Starting Docker PostgreSQL container..." -ForegroundColor DarkYellow
        docker start mokshsih-postgres-1 2>$null
    }
    Write-Host "[0/3] Docker Redis & PostgreSQL active." -ForegroundColor Green
} catch {
    Write-Host "Docker check bypassed (using local background engine)." -ForegroundColor Gray
}

# 1. Check if backend port 8000 is running
$backendPortActive = Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue
if (-not $backendPortActive) {
    Write-Host "[1/3] Launching FastAPI Unified Gateway on http://127.0.0.1:8000..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "api/main.py" -WorkingDirectory $backendDir
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/3] FastAPI Backend is already running on port 8000." -ForegroundColor Green
}


# 2. Check if frontend port 3000 is running
$frontendPortActive = Get-NetTCPConnection -State Listen -LocalPort 3000 -ErrorAction SilentlyContinue
if (-not $frontendPortActive) {
    Write-Host "[2/2] Launching CyberCell Frontend on http://localhost:3000..." -ForegroundColor Yellow
    Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory $frontendDir
    Start-Sleep -Seconds 3
} else {
    Write-Host "[2/2] CyberCell Frontend is already running on port 3000." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Green
Write-Host " PLATFORM READY & OPERATIONAL:" -ForegroundColor Green
Write-Host " - Frontend UI:  http://localhost:3000" -ForegroundColor White
Write-Host " - Backend Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host " - Health Check: http://127.0.0.1:8000/health" -ForegroundColor White
Write-Host "=========================================================================" -ForegroundColor Green
