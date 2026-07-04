from app.prompts import PR_DOCUMENTATION_PROMPT
from app.services.huggingface_service import generate_text


def generate_pr_documentation(pr_title: str, diff: str) -> dict:
    prompt = PR_DOCUMENTATION_PROMPT.format(
        pr_title=pr_title,
        diff=diff,
    )

    generated_text = generate_text(prompt=prompt)

    return {
        "generated_title": f"AI Summary: {pr_title}",
        "generated_description": generated_text,
        "provider": "huggingface",
    }