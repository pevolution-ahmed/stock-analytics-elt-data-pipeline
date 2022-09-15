{{ config(
    materialized='view'
    )
}}

with avg_std_of_stocks as (
    select
        avg(Adj_Close) as mean,
        std(Adj_Close) as std ,
        date(Date) as date
    from
        {{ source('stocks_storage', 'stocks_data')}}
)

select
    mean / std as cov,
    date
from
    avg_std_of_stocks
