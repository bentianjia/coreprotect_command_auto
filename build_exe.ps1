$ErrorActionPreference = "Stop"

try {
    Write-Host "Setting up Electron mirror..."
    $env:ELECTRON_MIRROR = "https://npmmirror.com/mirrors/electron/"
    $env:ELECTRON_BUILDER_BINARIES_MIRROR = "https://npmmirror.com/mirrors/electron-builder-binaries/"
    $env:npm_config_registry = "https://registry.npmmirror.com"
    $env:NODE_TLS_REJECT_UNAUTHORIZED = "0"

    Write-Host "Installing dependencies..."
    npm install
    if ($LASTEXITCODE -ne 0) { throw "npm install failed with exit code $LASTEXITCODE" }

    Write-Host "Building executable..."
    npm run build
    if ($LASTEXITCODE -ne 0) { throw "npm run build failed with exit code $LASTEXITCODE" }

    Write-Host "Build complete! Check the 'dist' folder." -ForegroundColor Green
} catch {
    Write-Host "An error occurred: $_" -ForegroundColor Red
} finally {
    Write-Host "Press Enter to exit..."
    Read-Host
}
