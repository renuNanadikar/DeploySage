from dataclasses import dataclass, field

LOCK_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Pipfile.lock"}


@dataclass
class RiskResult:
    score: int
    risk_level: str
    signals: list[str] = field(default_factory=list)


def calculate_risk_score(changed_files: list[str], ci_status: str) -> RiskResult:
    score = 0
    signals: list[str] = []

    if ci_status == "failed":
        score += 30
        signals.append("CI failed")

    if any("auth" in f.lower() for f in changed_files):
        score += 20
        signals.append("Authentication-related code changed")

    if any("payment" in f.lower() or "billing" in f.lower() for f in changed_files):
        score += 20
        signals.append("Payment/billing-related code changed")

    if any("migration" in f.lower() for f in changed_files):
        score += 18
        signals.append("Database migration changed")

    if any(f.rsplit("/", 1)[-1] in LOCK_FILES for f in changed_files):
        score += 12
        signals.append("Dependency lock file changed")

    if any(f.rsplit("/", 1)[-1] == "Dockerfile" for f in changed_files):
        score += 12
        signals.append("Dockerfile changed")

    if any(".github/workflows" in f for f in changed_files):
        score += 12
        signals.append("CI/CD workflow changed")

    if any(f.endswith(".env") or "/config/" in f for f in changed_files):
        score += 10
        signals.append("Environment/config file changed")

    if len(changed_files) > 20:
        score += 10
        signals.append("Large PR with more than 20 files changed")

    if any(".test." in f or ".spec." in f or f.startswith("tests/") or "test_" in f for f in changed_files):
        score -= 8
        signals.append("Tests were added or updated")

    if ci_status == "passed":
        score -= 20
        signals.append("CI passed")

    score = max(0, min(100, score))
    risk_level = "HIGH" if score >= 66 else "MEDIUM" if score >= 31 else "LOW"

    return RiskResult(score=score, risk_level=risk_level, signals=signals)
