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

## Hugging Face configuration

Set `HF_TOKEN` in the environment that runs the API. For a local PowerShell
session, set it before starting Uvicorn:

```powershell
$env:HF_TOKEN = "your_hugging_face_access_token"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 3000
```

The workflow sends the PR title and diff to the API; the API sends that data to
the configured Hugging Face model and returns its generated title and description.
