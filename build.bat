@echo off
echo ====================================
echo   CoreProtect Generator Packager
echo ====================================

:: 设置国内淘宝镜像，无需 VPN 即可快速下载，避免 TLS 报错
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set ELECTRON_BUILDER_BINARIES_MIRROR=https://npmmirror.com/mirrors/electron-builder-binaries/
set npm_config_registry=https://registry.npmmirror.com

echo 1. Installing dependencies (npm install)...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] npm install failed.
    pause
    exit /b %errorlevel%
)

echo 2. Packaging application (npm run build)...
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Packaging failed.
    pause
    exit /b %errorlevel%
)

echo ====================================
echo Build Success! Please check the "dist" folder.
echo ====================================
pause
