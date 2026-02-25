-- Table: Activity

-- +--------------+---------+
-- | Column Name  | Type    |
-- +--------------+---------+
-- | player_id    | int     |
-- | device_id    | int     |
-- | event_date   | date    |
-- | games_played | int     |
-- +--------------+---------+
-- (player_id, event_date) is the primary key (combination of columns with unique values) of this table.
-- This table shows the activity of players of some games.
-- Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.

-- Write a solution to report the fraction of players that logged in again on the day after the day they first logged in, rounded to 2 decimal places. In other words, you need to determine the number of players who logged in on the day immediately following their initial login, and divide it by the number of total players.

with base as (
    select
    player_id,
    event_date,
    row_number() over (
        partition by player_id order by event_date
    ) as rn,
    lag(event_date) over (
        partition by player_id order by event_date
    ) as prev_date
    from Activity
),
player_cnt as (
    select 
        count(distinct player_id) as cnt
    from Activity
)
select
    coalesce(
        round(
            sum(case when (event_date - prev_date) = 1 then 1 else 0 end)::numeric
            / nullif((select cnt from player_cnt)::numeric, 0),
            2
        ),
        0
    ) as fraction
from base
where rn = 2
