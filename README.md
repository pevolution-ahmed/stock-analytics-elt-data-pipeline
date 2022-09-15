# Stock Market Analytic DataOps Workflow

## Description:
DataOps Pipeline for Automating the ETL process of the stock market data and then build a BI product on top of these data whether it's a dashboard or a forecast predictive model.

## TO-DO:
- Save stocks ticker data from yahoo finance to Google BigQuery
- Create a Great Expectation Suite and Checkpoints using the Great Expectation package to validate and test the loaded data (Test suite)
- Add the following tasks:
    - a task for formatting the code using black lib
    - a task to check the linting using pylint
    - a task to run unit tests using pytest, pytest-cov
- Setup A dbt-core project as a transformation layer above the source data
