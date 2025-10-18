SELECT 
    v:c::float  AS current_price,
    v:d::float  AS change_amount,
    v:dp::float AS change_percent,
    v:h::float  AS day_high,
    v:l::float  AS day_low,
    v:o::float  AS day_open,
    v:pc::float AS prev_close,
    v:t::timestamp AS market_timestamp,
    v:symbol::string AS symbol,
    v:fetched_time::timestamp AS fetched_at  -- fixed here
FROM {{ source('raw','bronze_stocks_quotes_raw') }}
WHERE v:c IS NOT NULL
