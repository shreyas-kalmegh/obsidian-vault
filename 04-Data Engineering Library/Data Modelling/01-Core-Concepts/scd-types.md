# SCD Types (Dimensions)

## Overview
Slowly Changing Dimensions (SCD) define how attribute changes are stored over time.
Choose type per attribute, not blindly per table.

## Type 1: Overwrite
- No history kept
- Best for corrections or non-analytical attributes

Example:
- Fixing typo in `customer_name`

## Type 2: New Row per Change
- Full history with validity range
- Typical columns: `effective_from`, `effective_to`, `is_current`

Example:
- `customer_tier` changes from `Silver` to `Gold`

## Type 3: Previous Value Column
- Limited history (current + prior)
- Simpler than Type 2, but not full timeline

Example:
- `previous_plan`, `current_plan`

## Type 4: Current + History Table
- Current attributes in main dimension
- Historical changes in separate history table

## Type 6: Hybrid (1+2+3)
- Supports full history plus convenient current/prior reporting
- Powerful but can increase model complexity

## Example Type 2 Pattern
```sql
-- Simplified Type 2 update idea
-- 1) expire current row
-- 2) insert new current row
```

## Late-Arriving Changes
For Type 2, late updates can require:
- Back-dating `effective_from`
- Recomputing affected validity windows
- Rebuilding impacted facts if PIT logic is used

## Common Mistakes
- Using Type 2 for every changing attribute
- Allowing multiple `is_current = true` rows per natural key
- Using load timestamp as business effective timestamp

## Practical Checklist
1. Define which attributes are Type 1 vs Type 2.
2. Enforce one current row per business key.
3. Test non-overlapping validity intervals.
4. Define late-arrival correction workflow.

## Related Notes
- [[surrogate-vs-natural-keys]]
- [[late-arriving-data]]
