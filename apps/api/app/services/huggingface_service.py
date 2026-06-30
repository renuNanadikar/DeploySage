def generate_pr_documentation(pr_title: str, diff: str) -> dict:
    return {
        "generated_title": "DeploySage PR Summary",
        "generated_description": "This PR introduces the first DeploySage PR analysis flow.",
        "provider": "hardcoded",
    }