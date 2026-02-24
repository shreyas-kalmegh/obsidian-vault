# Python Production Readiness: Practical Notes

## Quick Reference Table

| Area | Goal | Recommended Default | Common Failure |
|---|---|---|---|
| Python runtime | Reproducible execution | Pin Python version (`3.11.x` etc.) | Works locally, breaks in CI/prod |
| Environments | Isolate dependencies | `venv` per project | Global package conflicts |
| Dependency mgmt | Deterministic installs | `pyproject.toml` + lock file | Unpinned transitive upgrades |
| Packaging | Clean import/install model | `src/` layout + wheel build | Import from cwd hides packaging bugs |
| Testing | Regression safety | `pytest` + CI | Untested edge cases |
| Shipping | Reliable deploy artifact | Wheel/container | Snowflake runtime environments |
| Observability | Operability | Structured logs + health checks | Silent failures, slow incident response |

---

## 1) `sys.path` and Imports (Why Code Works in IDE but Fails in Prod)

`sys.path` is where Python looks for modules.

```python
import sys
print(sys.path)
```

Import order typically includes:
- Script directory / current working directory
- Standard library
- Site-packages from active environment

Production caveats:
- Running from different working directory changes import behavior.
- Relying on ad-hoc `PYTHONPATH` leads to environment-specific bugs.
- Prefer installable packages over path hacks.

Good practice:
- Use package imports (`from myapp.service import run`) not relative filesystem assumptions.
- Use `python -m myapp.cli` for entrypoint execution.

---

## 2) Virtual Environments (`venv`)

Create and activate:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate       # Windows PowerShell/CMD
```

Why:
- Isolates dependencies per project.
- Prevents global/site-package contamination.

Caveats:
- Never commit `.venv` to git.
- Ensure IDE/interpreter points to project venv.
- Recreate venv on Python minor-version mismatch.

---

## 3) Dependency Management

Use `pyproject.toml` as source of truth.

Example (minimal):

```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "requests>=2.32,<3",
  "pydantic>=2.7,<3"
]
```

Locking strategy:
- App/service: use lock file for fully reproducible deploys.
- Library: keep ranges in `pyproject.toml`, test across supported versions.

Caveats:
- Pinning only top-level deps is not enough for apps.
- Unbounded deps (`>=`) can break unexpectedly.
- Separate runtime vs dev deps (`pytest`, `ruff`, etc.).

---

## 4) Modules, Packages, and `src/` Layout

Recommended structure:

```text
repo/
  pyproject.toml
  src/
    myapp/
      __init__.py
      cli.py
      service.py
  tests/
    test_service.py
```

Why `src/` layout:
- Prevents accidental imports from repository root.
- Forces tests to import installed package behavior.

Caveats:
- Missing `__init__.py` can change import semantics.
- Name collisions with stdlib (`email.py`, `json.py`) cause import shadowing.

---

## 5) CLI Entrypoints

Expose command via console script:

```toml
[project.scripts]
myapp = "myapp.cli:main"
```

```python
# src/myapp/cli.py

def main():
    print("hello")
```

Benefits:
- Stable command name after install.
- No need for brittle relative paths.

---

## 6) Shipping Libraries vs Shipping Applications

Library shipping (for reuse):
- Publish wheel/sdist.
- Keep API stable and versioned.
- Broader dependency compatibility ranges.

Application shipping (for deployment):
- Ship locked dependencies.
- Prefer container image or wheel + locked environment.
- Include config, health checks, and startup contracts.

Caveat:
- Library-style loose deps are risky for services; service deploys need determinism.

---

## 7) Build and Distribute Packages

Build artifacts:

```bash
python -m pip install --upgrade build
python -m build
```

Outputs:
- `dist/*.whl` (wheel)
- `dist/*.tar.gz` (sdist)

Install locally for verification:

```bash
python -m pip install dist/<your-wheel>.whl
```

Caveats:
- Test installation in a fresh venv.
- Validate metadata (`requires-python`, dependencies, entrypoints).

---

## 8) Configuration and Secrets

Pattern:
- Defaults in code
- Environment-specific overrides via env vars
- Secrets from secret manager (not repo)

```python
import os

DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
DB_URL = os.environ["DB_URL"]  # required
```

Caveats:
- Never commit secrets.
- Fail fast for missing required env vars.
- Keep config schema explicit and validated.

---

## 9) Logging and Observability

Prefer structured logging with context fields.

```python
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("myapp")
log.info("job_started", extra={"job_id": "123"})
```

Production baseline:
- Request/job IDs
- Error logs with stack trace
- Health/readiness endpoints for services

Caveats:
- Avoid logging secrets/PII.
- Avoid overly chatty DEBUG in production.

---

## 10) Testing with `pytest`

Basic test:

```python
# tests/test_math_utils.py

def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
```

Run:

```bash
pytest -q
```

Parametrized tests:

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_cases(a, b, expected):
    assert a + b == expected
```

Useful patterns:
- Fixtures for setup/teardown
- `monkeypatch` for env vars/time/network stubs
- Marker split: unit vs integration

Caveats:
- Flaky tests often come from time/network/shared state.
- Keep tests deterministic and isolated.

---

## 11) CI Quality Gates (Minimum)

Recommended pipeline:
1. Install with lock file
2. Lint/format check
3. Type check (optional but high value)
4. `pytest`
5. Build artifact

Caveats:
- CI environment should match runtime (OS/Python version) as closely as possible.
- Failing to run tests against built artifact misses packaging defects.

---

## 12) Database and I/O Safety

Patterns:
- Retry transient errors with backoff.
- Use idempotent operations where possible.
- Set explicit client timeouts.

Caveats:
- No timeout means potentially hung workers.
- Unbounded retries can amplify outages.

---

## 13) Concurrency in Production Services

- I/O-bound APIs: threads/async
- CPU-heavy workloads: process pool / separate worker service
- Always define queue limits and timeout budgets

Caveats:
- Backpressure is mandatory under burst traffic.
- Avoid blocking calls inside async handlers.

---

## 14) Release and Versioning Basics

Use semantic versioning guidance:
- MAJOR: breaking changes
- MINOR: backward-compatible features
- PATCH: fixes

Release checklist:
- Changelog entry
- Version bump
- Green CI
- Tagged release

---

## 15) High-Value Gotchas

- Importing from cwd masks missing package installation.
- Running tests without active venv gives false confidence.
- Missing lock file causes non-reproducible deploys.
- "Works on my machine" due to hidden local env vars.
- Global mutable state in services causes cross-request leaks.
- No timeout/retry policy leads to cascading failures.
- Shipping source only without verifying wheel install.

---

## 16) Production Readiness Checklist

- Python version pinned and documented.
- Project uses isolated venv.
- Dependencies declared and locked.
- Package structure installable (`src/` + entrypoint).
- Tests pass in CI on clean environment.
- Artifact build and install verified.
- Config and secrets externalized.
- Logging, health checks, and alerts in place.
- Timeouts/retries/backpressure defined.

---

## 17) Recommended Tooling Stack (Minimal, High ROI)

Baseline stack:
- `ruff` for lint + format (fast, replaces multiple tools)
- `mypy` for static typing on critical paths
- `pytest` for tests
- `pytest-cov` for coverage gates
- `pre-commit` for local quality checks before push

Install (dev):

```bash
python -m pip install ruff mypy pytest pytest-cov pre-commit
```

Minimal `pyproject.toml` tool config:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.mypy]
python_version = "3.11"
warn_unused_configs = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
no_implicit_optional = true

[tool.pytest.ini_options]
addopts = "-q --maxfail=1 --cov=src --cov-report=term-missing"
testpaths = ["tests"]
```

Minimal `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.0
    hooks:
      - id: ruff-check
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.18.2
    hooks:
      - id: mypy
```

Enable hooks:

```bash
pre-commit install
pre-commit run --all-files
```

Caveats:
- Start strict typing on changed/new modules first if legacy code is large.
- Coverage % alone is not quality; prioritize meaningful assertions and edge cases.
- Keep tool versions pinned in CI for consistent behavior.
