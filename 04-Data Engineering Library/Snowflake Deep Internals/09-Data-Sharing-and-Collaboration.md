# Data Sharing and Collaboration

## Snowflake data sharing model
Snowflake enables secure sharing without copying data in many scenarios.

Benefits:
- Faster collaboration across teams and organizations.
- Reduced data duplication and movement complexity.

## Shares, listings, and collaboration patterns
Common options:
- Direct account-to-account shares
- Marketplace/private listings (depending on use case)
- Internal sharing across business units

## Producer responsibilities
If you publish shared datasets:
- Stabilize schema contracts.
- Document refresh cadence and SLA.
- Communicate breaking changes with lead time.

## Consumer responsibilities
If you consume shared datasets:
- Create abstraction views rather than binding dashboards directly to shared raw tables.
- Monitor for schema drift and data freshness.
- Define ownership for incident response.

## Governance in shared data
- Apply masking and row access policies before publishing.
- Tag sensitive columns and restrict grants via consumer roles.
- Track usage/audit access for contractual or compliance needs.

## Practical collaboration playbook
1. Define data contract (fields, types, freshness).
2. Publish a versioned shared schema.
3. Expose changelog and deprecation policy.
4. Validate consumer adoption before major changes.
