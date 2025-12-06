Write-Host "Starting Backend..."
Start-Process powershell -ArgumentList "uvicorn app.main:app --reload"

Write-Host "Starting Frontend..."
Start-Process powershell -ArgumentList "cd web; python -m http.server 5500"
