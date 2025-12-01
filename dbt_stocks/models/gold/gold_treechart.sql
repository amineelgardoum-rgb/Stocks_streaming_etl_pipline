{{ config(materialized='table') }}

WITH source AS (
  SELECT
    symbol,
    current_price::double precision AS current_price_dbl,
    fetched_at
  FROM {{ ref('silver_clean_stock_quotes') }}
  WHERE current_price IS NOT NULL
),

latest_day AS (
  -- fetched_at is already a timestamp, so just cast to date
  SELECT MAX(fetched_at)::date AS max_day
  FROM source
),

latest_prices AS (
  SELECT
    s.symbol,
    AVG(s.current_price_dbl) AS avg_price
  FROM source s
  JOIN latest_day ld
    ON s.fetched_at::date = ld.max_day
  GROUP BY s.symbol
),

all_time_volatility AS (
  SELECT
    symbol,
    STDDEV_POP(current_price_dbl) AS volatility,             
    CASE
      WHEN AVG(current_price_dbl) = 0 THEN NULL
      ELSE STDDEV_POP(current_price_dbl) / NULLIF(AVG(current_price_dbl), 0)
    END AS relative_volatility
  FROM source
  GROUP BY symbol
)

SELECT
  lp.symbol,
  lp.avg_price,
  v.volatility,
  v.relative_volatility
FROM latest_prices lp
JOIN all_time_volatility v 
  ON lp.symbol = v.symbol
ORDER BY lp.symbol
