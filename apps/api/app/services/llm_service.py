def generate_pr_summary(diff: str, changed_files: list[str]) -> dict:
    """Mock stand-in for the real LLM call (Phase 2). Deterministic, no external API."""
    file_list = ", ".join(changed_files) if changed_files else "no files"

    return {
        "summary": f"This PR changes {len(changed_files)} file(s): {file_list}.",
        "key_changes": [f"Modified {f}" for f in changed_files],
        "testing_notes": "No test result was provided at PR analysis time.",
        "deployment_notes": "Review changes before deploying.",
        "risk_factors": [],
    }
