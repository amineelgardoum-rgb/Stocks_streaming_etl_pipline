{{ config(materialized='table') }}
SELECT symbol,current_price,
ROUND(day_high::numeric,2) AS day_high,
ROUND(day_low ::numeric,2) AS day_low,
ROUND(day_open ::numeric,2) AS day_open,
ROUND(prev_close ::numeric,2) AS prev_close,
change_amount,
ROUND(change_percent ::numeric,4) AS change_percent,
fetched_at
FROM {{ ref('bronze_stg_stock_quotes') }}

WHERE current_price IS NOT NULL