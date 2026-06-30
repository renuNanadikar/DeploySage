DeploySage Feature 1 Test Case

Feature:
AI-generated PR documentation

Endpoint:
POST /api/pr/analyze

Purpose:
This endpoint receives pull request metadata and returns a generated PR title and description.

Current Test Behavior:
For now, the title and description are hardcoded.

Later Behavior:
The API will call Hugging Face to generate the PR documentation from the PR diff.

Example Request:
{
  "repository_owner": "renuNanadikar",
  "repository_name": "DeploySage",
  "pr_number": 1,
  "pr_title": "Initial Python API migration",
  "diff": "Hardcoded test diff for now"
}

Expected Response:
{
  "generated_title": "DeploySage PR Summary",
  "generated_description": "This PR introduces the first DeploySage PR analysis flow.",
  "provider": "hardcoded",
  "github_ready": true
}