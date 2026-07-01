import uuid

from pydantic import BaseModel


class RepositoryInput(BaseModel):
    owner: str
    name: str


class PullRequestInput(BaseModel):
    number: int
    title: str
    author: str
    base_branch: str
    head_branch: str
    commit_sha: str


class PRAnalyzeRequest(BaseModel):
    repository: RepositoryInput
    pull_request: PullRequestInput
    diff: str
    changed_files: list[str]
    test_status: str


class PRAnalyzeResponse(BaseModel):
    analysis_run_id: uuid.UUID
    summary: str
    risk_score: int
    risk_level: str
    gate_decision: str
