def generate_pr_documentation(pr_title: str, diff: str) -> dict:
    """Return temporary PR documentation until LLM generation is enabled."""

    # The Hugging Face implementation will replace this dummy response later,
    # without requiring API or GitHub Actions changes.
    _ = (pr_title, diff)

    return {
        "generated_title": "DeploySage PR Summary",
        "generated_description": "This PR introduces the first DeploySage PR analysis flow.",
        "provider": "hardcoded",
    }
