import subprocess
import os

# Start backend
subprocess.Popen(["powershell", "-Command", "uvicorn app.main:app --reload"])

# Start frontend
subprocess.Popen(["powershell", "-Command", "cd web; python -m http.server 5500"])

print("Backend running at: http://localhost:8000")
print("Frontend running at: http://localhost:5500")
