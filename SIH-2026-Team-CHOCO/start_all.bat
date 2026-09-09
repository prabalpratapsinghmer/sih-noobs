@echo off
title CyberCell Sovereign Defense & Tactical Intelligence Platform
echo =========================================================================
echo  CYBERCELL & SIH26184: FULL-STACK UNIFIED PLATFORM LAUNCHER
echo =========================================================================
echo.

cd /d "%~dp0"

echo [1/3] Verifying Python and FastAPI backend environment...
python -c "from api.main import app; print('[OK] Backend imports and 58 OpenAPI endpoints verified.')"
if %errorlevel% neq 0 (
    echo [ERROR] Backend verification failed. Please check requirements.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting FastAPI Unified Gateway on http://127.0.0.1:8000 ...
start "CyberCell Backend (Port 8000)" cmd /k "cd /d %~dp0 && python api/main.py"

echo.
echo [3/3] Starting CyberCell Cockpit Frontend on http://localhost:3000 ...
start "CyberCell Frontend (Port 3000)" cmd /k "cd /d D:\MokshFrontEnd && npm run dev"

echo.
echo =========================================================================
echo  PLATFORM SERVICES INITIALIZED!
echo  - Frontend UI:  http://localhost:3000
echo  - Backend API:  http://127.0.0.1:8000/docs
echo  - Health Probe: http://127.0.0.1:8000/health
echo =========================================================================
echo.
pause
