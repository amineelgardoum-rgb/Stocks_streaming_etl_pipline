{{ config(materialized='table') }}

WITH raw_stock_data AS (
    SELECT 
        id,
        data
    FROM {{ source('raw', 'raw_data') }}
    WHERE data IS NOT NULL
)

SELECT 
    id AS raw_id,
    (data->>'c')::float AS current_price,
    (data->>'d')::float AS change_amount,
    (data->>'dp')::float AS change_percent,
    (data->>'h')::float AS day_high,
    (data->>'l')::float AS day_low,
    (data->>'o')::float AS day_open,
    (data->>'pc')::float AS prev_close,
    data->>'symbol' AS symbol,
    CASE 
        WHEN data->>'fetched_time' IS NOT NULL 
        THEN TO_TIMESTAMP((data->>'fetched_time')::bigint / 1000.0)
        ELSE NULL
    END AS fetched_at
FROM raw_stock_data
WHERE (data->>'c') IS NOT NULL
