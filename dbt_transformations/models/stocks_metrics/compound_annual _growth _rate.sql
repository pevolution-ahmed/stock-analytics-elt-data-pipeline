{{ config(
    materialized='view'
    )
}}

with stock_constraints as (
    select
        first_value(date(Date)) over(partition by Stock order by Date) as start_date,
        first_value(date(Date)) over(partition by Stock order by Date desc) as end_date,
        first_value(Adj_Close) over(partition by Stock order by Date) as begin_price,
        first_value(Adj_Close) over(partition by Stock order by Date desc) as end_price,
    from
        {{ source('stocks_storage', 'stocks_data')}}
    limit 1
)

select
    round((pow((end_price / begin_price), 1 / {{ datediff('start_date', 'end_date', 'year') }} )-1)*100,4) as CAGR
from 
    stock_constraints

