import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.analysis_run import AnalysisRun
from app.models.deployment_gate_decision import DeploymentGateDecision
from app.models.pr_summary_version import PRSummaryVersion
from app.models.pull_request import PullRequest
from app.models.repository import Repository
from app.models.risk_score_version import RiskScoreVersion
from app.schemas.pr import PRAnalyzeRequest
from app.services.llm_service import generate_pr_summary
from app.services.risk_scoring_service import calculate_risk_score
from app.services.versioning_service import get_next_analysis_version

GATE_DECISIONS = {
    "LOW": ("PASS", "Low risk, safe to proceed."),
    "MEDIUM": ("WARN", "Medium risk, review recommended before merging."),
    "HIGH": ("BLOCK", "High risk, manual review required before deployment."),
}


@dataclass
class PRAnalysisResult:
    analysis_run_id: uuid.UUID
    summary: str
    risk_score: int
    risk_level: str
    gate_decision: str


def _get_or_create_repository(db: Session, payload: PRAnalyzeRequest) -> Repository:
    repository = (
        db.query(Repository)
        .filter(
            Repository.github_owner == payload.repository.owner,
            Repository.github_repo == payload.repository.name,
        )
        .first()
    )
    if repository is None:
        repository = Repository(
            github_owner=payload.repository.owner,
            github_repo=payload.repository.name,
        )
        db.add(repository)
        db.flush()
    return repository


def _get_or_create_pull_request(db: Session, repository: Repository, payload: PRAnalyzeRequest) -> PullRequest:
    pull_request = (
        db.query(PullRequest)
        .filter(
            PullRequest.repository_id == repository.id,
            PullRequest.pr_number == payload.pull_request.number,
        )
        .first()
    )
    if pull_request is None:
        pull_request = PullRequest(repository_id=repository.id, pr_number=payload.pull_request.number)
        db.add(pull_request)

    pull_request.title = payload.pull_request.title
    pull_request.author = payload.pull_request.author
    pull_request.base_branch = payload.pull_request.base_branch
    pull_request.head_branch = payload.pull_request.head_branch
    pull_request.latest_commit_sha = payload.pull_request.commit_sha
    pull_request.state = "open"
    db.flush()
    return pull_request


def analyze_pr(db: Session, payload: PRAnalyzeRequest) -> PRAnalysisResult:
    repository = _get_or_create_repository(db, payload)
    pull_request = _get_or_create_pull_request(db, repository, payload)

    analysis_version = get_next_analysis_version(db, pull_request.id)
    analysis_run = AnalysisRun(
        pull_request_id=pull_request.id,
        commit_sha=payload.pull_request.commit_sha,
        analysis_version=analysis_version,
        status="completed",
        model_name="mock-llm",
        prompt_version="v1",
    )
    db.add(analysis_run)
    db.flush()

    risk_result = calculate_risk_score(payload.changed_files, payload.test_status)
    summary_result = generate_pr_summary(payload.diff, payload.changed_files)
    gate_decision, gate_reason = GATE_DECISIONS[risk_result.risk_level]

    db.add(
        PRSummaryVersion(
            analysis_run_id=analysis_run.id,
            summary_markdown=summary_result["summary"],
            key_changes=summary_result["key_changes"],
            testing_notes=summary_result["testing_notes"],
            deployment_notes=summary_result["deployment_notes"],
        )
    )
    db.add(
        RiskScoreVersion(
            analysis_run_id=analysis_run.id,
            risk_score=risk_result.score,
            risk_level=risk_result.risk_level,
            signals=risk_result.signals,
            explanation=(
                f"Risk score {risk_result.score} based on: "
                f"{', '.join(risk_result.signals) or 'no notable signals'}."
            ),
            recommendation=gate_reason,
        )
    )
    db.add(
        DeploymentGateDecision(
            analysis_run_id=analysis_run.id,
            decision=gate_decision,
            reason=gate_reason,
        )
    )

    db.commit()

    return PRAnalysisResult(
        analysis_run_id=analysis_run.id,
        summary=summary_result["summary"],
        risk_score=risk_result.score,
        risk_level=risk_result.risk_level,
        gate_decision=gate_decision,
    )
