# DeploySage API

Python FastAPI service for DeploySage.

## Setup

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload --port 3000
```

## Health Check

```text
GET http://localhost:3000/health
```
