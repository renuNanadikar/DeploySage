from app.services.risk_scoring_service import calculate_risk_score


def test_no_signals_is_low_risk():
    result = calculate_risk_score(changed_files=["src/utils/format.py"], ci_status="unknown")

    assert result.score == 0
    assert result.risk_level == "LOW"
    assert result.signals == []


def test_ci_failed_alone_is_low_risk_boundary():
    result = calculate_risk_score(changed_files=["src/utils/format.py"], ci_status="failed")

    assert result.score == 30
    assert result.risk_level == "LOW"
    assert "CI failed" in result.signals


def test_auth_change_with_ci_failure_is_medium_risk():
    result = calculate_risk_score(changed_files=["src/auth/middleware.py"], ci_status="failed")

    assert result.score == 50
    assert result.risk_level == "MEDIUM"
    assert "CI failed" in result.signals
    assert "Authentication-related code changed" in result.signals


def test_multiple_high_weight_signals_reach_high_risk():
    result = calculate_risk_score(
        changed_files=["src/auth/login.py", "db/migration_0001.sql", "package-lock.json"],
        ci_status="failed",
    )

    assert result.score == 80
    assert result.risk_level == "HIGH"


def test_score_clamps_at_100():
    changed_files = [
        "src/auth/login.py",
        "src/billing/charge.py",
        "db/migration_0001.sql",
        "package-lock.json",
        "Dockerfile",
        ".github/workflows/ci.yml",
        "config/.env",
    ] + [f"src/file_{i}.py" for i in range(25)]

    result = calculate_risk_score(changed_files=changed_files, ci_status="failed")

    assert result.score == 100
    assert result.risk_level == "HIGH"


def test_ci_passed_and_tests_added_clamp_at_zero():
    result = calculate_risk_score(
        changed_files=["tests/test_login.py"],
        ci_status="passed",
    )

    assert result.score == 0
    assert result.risk_level == "LOW"
    assert "CI passed" in result.signals
    assert "Tests were added or updated" in result.signals
