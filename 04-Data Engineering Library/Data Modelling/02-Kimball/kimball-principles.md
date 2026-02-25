# Kimball Principles

## Overview
Kimball modeling is process-centric dimensional design for analytics.
It optimizes for clear business metrics, fast BI queries, and iterative delivery.

## Core Principles
1. Model around business processes
- Example processes: Orders, Returns, Payments, Shipments

2. Declare grain first
- Every fact must have an explicit row-level meaning

3. Build facts + conformed dimensions
- Facts hold measures
- Conformed dimensions provide reusable context across marts

4. Deliver incrementally
- Start with one high-value mart, then expand via conformed dimensions

## Practical Design Flow
1. Select business process and key KPIs.
2. Define fact grain and required measures.
3. Identify dimensions and SCD policies.
4. Create bus matrix to align cross-domain reuse.
5. Ship one mart, validate with business users, then expand.

## Example: Orders Domain
- Fact: `fct_order_line`
- Dimensions: `dim_customer`, `dim_product`, `dim_date`, `dim_channel`
- KPIs: revenue, units, AOV, return rate

## Why Kimball Still Works in Lakehouse
- Gold layer can still be dimensional
- Iceberg/Delta storage does not replace modeling fundamentals
- Semantic clarity remains the main defense against metric disputes

## Common Mistakes
- Modeling source schema directly into analytics layer
- Skipping bus matrix and creating siloed marts
- Ignoring dimension conformance until late stage

## Practical Checklist
1. Process scope and KPI dictionary defined.
2. Grain statement documented for each fact.
3. Dimension conformance reviewed across domains.
4. Data tests added for PK/FK and duplicate grain.

## Related Notes
- [[bus-matrix]]
- [[conformed-dimensions]]
- [[star-vs-snowflake]]
