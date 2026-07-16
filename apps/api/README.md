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

## GitHub Actions configuration

The PR-analysis workflow calls this service and then updates the pull request
with the returned `generated_title` and `generated_description`. Set the
repository variable `DEPLOYSAGE_API_URL` to the public base URL of this API
(for example, `https://deploysage.example.com`). The workflow already declares
the required `pull-requests: write` permission.
