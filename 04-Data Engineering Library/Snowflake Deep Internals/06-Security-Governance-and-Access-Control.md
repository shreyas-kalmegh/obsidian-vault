# Security, Governance, and Access Control

## Role-based access control (RBAC)
Snowflake uses roles as the primary permission model.

Practical pattern:
- Create functional roles (`ROLE_ETL`, `ROLE_BI_ANALYST`).
- Map users or service principals to those roles.
- Grant least privilege required.

## Separation of duties
Common split:
- Security/admin roles manage grants and policies.
- Engineering roles manage pipelines.
- Analyst roles consume curated marts.

This reduces accidental privilege escalation.

## Object ownership and grant strategy
- Ownership controls object management rights.
- Future grants simplify schema onboarding.

Guideline:
- Avoid ad hoc direct grants to individual users.
- Standardize grants at schema/database level via roles.

## Data protection features
- Dynamic data masking
- Row access policies
- Tagging and classification for governance

Use case:
- Expose shared marts while masking PII columns for non-privileged roles.

## Network and auth controls
- SSO federation and MFA
- Network policies for allowed IP ranges
- Key-pair auth for service accounts where appropriate

## Governance operating model
- Keep grant logic in version-controlled SQL.
- Run periodic access reviews.
- Audit high-risk object access and policy bypass events.
