-- Example table:
-- dim_user_tier(user_id, service_tier_id, eff_start_ts, eff_end_ts, is_current)

BEGIN;

WITH src AS (
  -- Incoming snapshot/change set
  -- Replace this with your real staging table
  SELECT user_id, service_tier_id, now()::timestamp AS effective_from
  FROM staging_user_tier
),
changed AS (
  -- Current rows that actually changed
  SELECT d.user_id, s.service_tier_id, s.effective_from
  FROM dim_user_tier d
  JOIN src s ON s.user_id = d.user_id
  WHERE d.is_current = true
    AND d.service_tier_id IS DISTINCT FROM s.service_tier_id
),
closed AS (
  -- Close old current rows
  UPDATE dim_user_tier d
  SET eff_end_ts = c.effective_from,
      is_current = false
  FROM changed c
  WHERE d.user_id = c.user_id
    AND d.is_current = true
  RETURNING d.user_id
)
-- Insert new rows for:
-- 1) changed users, 2) brand new users
INSERT INTO dim_user_tier (user_id, service_tier_id, eff_start_ts, eff_end_ts, is_current)
SELECT s.user_id,
       s.service_tier_id,
       s.effective_from,
       '9999-12-31'::timestamp,
       true
FROM src s
LEFT JOIN dim_user_tier cur
  ON cur.user_id = s.user_id
 AND cur.is_current = true
WHERE cur.user_id IS NULL
   OR cur.service_tier_id IS DISTINCT FROM s.service_tier_id;

COMMIT;
