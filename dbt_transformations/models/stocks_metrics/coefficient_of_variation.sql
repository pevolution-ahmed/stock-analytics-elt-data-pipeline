{{ config(
    materialized='view'
    )
}}

with avg_std_of_stocks as (
    select
        avg(Adj_Close) as mean,
        STDDEV(Adj_Close) over() as std ,
        date(Date) as date
    from
        {{ source('stocks_storage', 'stocks_data')}}
    group by
        date(Date)
)

select
    mean / std as cov,
    date
from
    avg_std_of_stocks
