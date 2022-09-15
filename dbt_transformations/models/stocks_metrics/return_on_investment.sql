{{ config(
    materialized='view'
    )
}}

with start_and_last_stock_values as (
    select
        first_value(Adj_Close) over() as start_val,
        last_value(Adj_Close) over() as last_val,
        date(Date) as date
    from
        {{ source('stocks_storage', 'stocks_data')}}
)
select
    ((end_val - start_val) / start_val) as return_on_invesment,
    date
from
    start_and_last_stock_values