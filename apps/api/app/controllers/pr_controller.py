from app.schemas.pr_analysis import PRAnalyzeRequest, PRAnalyzeResponse
from app.services.github_service import is_github_payload_ready
from app.services.huggingface_service import generate_pr_documentation


def analyze_pr(payload: PRAnalyzeRequest) -> PRAnalyzeResponse:
    documentation = generate_pr_documentation(
        pr_title=payload.pr_title,
        diff=payload.diff,
    )

    github_ready = is_github_payload_ready(
        repository_owner=payload.repository_owner,
        repository_name=payload.repository_name,
        pr_number=payload.pr_number,
    )

    return PRAnalyzeResponse(
        generated_title=documentation["generated_title"],
        generated_description=documentation["generated_description"],
        provider=documentation["provider"],
        github_ready=github_ready,
    )