import json

from app.prompts import PR_DOCUMENTATION_PROMPT
from app.services.huggingface_service import generate_text


def generate_pr_documentation(pr_title: str, diff: str) -> dict:
    """Generate PR documentation from the title and code diff using Hugging Face."""

    prompt = PR_DOCUMENTATION_PROMPT.format(
        pr_title=pr_title,
        diff=diff,
    )
    generated_text = generate_text(prompt=prompt)
    documentation = _parse_documentation(generated_text)

    return {
        "generated_title": documentation["title"],
        "generated_description": documentation["description"],
        "provider": "huggingface",
    }


def _parse_documentation(generated_text: str) -> dict[str, str]:
    """Validate the JSON contract returned by the LLM before updating a PR."""

    cleaned_text = generated_text.strip()
    if cleaned_text.startswith("```") and cleaned_text.endswith("```"):
        cleaned_text = cleaned_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()

    try:
        documentation = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Hugging Face returned invalid PR documentation JSON.") from exc

    title = documentation.get("title") if isinstance(documentation, dict) else None
    description = documentation.get("description") if isinstance(documentation, dict) else None
    if not isinstance(title, str) or not title.strip():
        raise RuntimeError("Hugging Face response is missing a PR title.")
    if not isinstance(description, str) or not description.strip():
        raise RuntimeError("Hugging Face response is missing a PR description.")

    return {
        "title": title.strip(),
        "description": description.strip(),
    }
