def is_github_payload_ready(repository_owner: str, repository_name: str, pr_number: int) -> bool:
    return bool(repository_owner and repository_name and pr_number)