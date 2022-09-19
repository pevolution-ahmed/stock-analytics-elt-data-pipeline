{{ config(
    materialized='view'
    )
}}

select
    Adj_Close,
    round(avg(High - Low),2) as avg_volatility,
    dense_rank() over(order by avg(High - Low) asc) as ranking
    date(Date) as date
from
    {{ source('stocks_storage', 'stocks_data')}}
group by
    1