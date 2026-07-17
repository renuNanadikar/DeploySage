from app.schemas.pr_analysis import PRAnalyzeRequest, PRAnalyzeResponse
from app.services.github_service import is_github_payload_ready
from app.services.pr_service import generate_pr_documentation


def analyze_pr(payload: PRAnalyzeRequest) -> PRAnalyzeResponse:
    documentation = generate_pr_documentation(
        pr_title=payload.pr_title,
        diff=payload.diff,
    )
#This asks Hugging Face service to generate text.#

    github_ready = is_github_payload_ready(
        repository_owner=payload.repository_owner,
        repository_name=payload.repository_name,
        pr_number=payload.pr_number,
    )
#This checks whether we have enough GitHub data.#

    return PRAnalyzeResponse(
        generated_title=documentation["generated_title"],
        generated_description=documentation["generated_description"],
        provider=documentation["provider"],
        github_ready=github_ready,
    )
#The controller coordinates business flow. It does not directly call external APIs itself; it delegates to services.#