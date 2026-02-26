# Hooks, Connections, and Provider Patterns

## Overview
Hooks are provider-specific clients used by operators/sensors to communicate with external systems. Connections store credentials and endpoint metadata used by hooks.

## Mental Model
- Operator/sensor defines orchestration logic.
- Hook handles integration details (auth, client creation, API calls).
- Connection supplies runtime credentials/config.

This separation keeps DAG code cleaner and easier to rotate secrets.

## Example: Using a Hook in Custom Task Code

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

def run_quality_check():
    hook = PostgresHook(postgres_conn_id="analytics_postgres")
    result = hook.get_first("SELECT count(*) FROM analytics.orders WHERE ds = CURRENT_DATE")
    if result[0] == 0:
        raise ValueError("No rows loaded for today")
```

## Connection Best Practices
- Use `conn_id` references, not hardcoded secrets.
- Store secrets in a backend (Vault/Secrets Manager) where possible.
- Standardize connection naming (`team_system_env` style).
- Keep least-privilege credentials for each DAG domain.

## Provider Pattern Guidance
1. Prefer provider operators/hooks before custom integration code.
2. Wrap repeated integration logic in shared utility modules/plugins.
3. Keep custom hooks thin and testable.
4. Add timeouts/retry handling for external calls.

## Common Pitfalls
- Placing credentials directly in DAG code.
- Re-implementing provider logic already available in hooks/operators.
- Running large data extraction through hooks into XCom payloads.
- Ignoring API throttling limits; no backoff strategy.

## Practical Rule
Use hooks for control-plane integration operations and metadata checks. For large data movement, orchestrate external jobs and pass object references, not payloads.
