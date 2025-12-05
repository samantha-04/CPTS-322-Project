# Demo script to show update workflow for the assignment
# Usage: run in PowerShell from the repo root

Write-Host "Current frontend VERSION:"
Get-Content .\code\frontend\VERSION

Write-Host "\nNow updating VERSION to v2.0 for demo..."
Set-Content -Path .\code\frontend\VERSION -Value "v2.0"

Write-Host "Updated VERSION content:"
Get-Content .\code\frontend\VERSION

Write-Host "\nBuild and run steps (manual) -- run these after confirming the change:\n"
Write-Host "# Build both images"
Write-Host "docker-compose build"
Write-Host "\n# Or build just the frontend image"
Write-Host "docker-compose build frontend"
Write-Host "\n# Start services"
Write-Host "docker-compose up -d"
Write-Host "\n# Check frontend API for version"
Write-Host "Invoke-RestMethod -Uri 'http://localhost:8000/api/hello' -Method Get | ConvertTo-Json -Depth 5"

Write-Host "\n(If you prefer to run containers without docker-compose, build and run the frontend Dockerfile directly.)"
