{{ config(
    materialized='view'
    )
}}

with prices as (
    select
        Date,
        Adj_Close as current_price,
        lag(Adj_Close, 1) over ( order by Date) as previous_price
    from
        {{ source('stocks_storage', 'stocks_data') }}
)
,daily_returns as (
    select
        Date,
        (current_price  / cast(previous_price as float)) - 1 as daily_return
    from
        prices
)
select
    date(Date) as date,
    avg(daily_return) as total_return_over_time
from
    daily_returns
where
    date(Date) <= start_date
    and date(Date) >= current_date()
