# Stock Market Analytics ETL Workflow

## Description
A Data Pipeline for Automating the ETL workflow of the stock market data and then building a BI product on top of this data, whether it's a dashboard or a forecast predictive model.

**Data Stack**:
<img src="https://seeklogo.com/images/D/dbt-logo-500AB0BAA7-seeklogo.com.png" alt="drawing" width="50"/>
<img src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" alt="drawing" width="50"/>
<img src="https://greatexpectations.io/static/protag-f9bde762a58323b62e2c19c514c74ba8.png" alt="drawing" width="50"/>
<img src="https://cdn.icon-icons.com/icons2/2699/PNG/512/google_bigquery_logo_icon_168150.png" alt="drawing" width="50"/>


## General Pipeline Structure
- The pipeline consists of four layers data should go through:
    - Extraction and Load
    - Validation and quality gates
    - Transformation
    - BI

## TO-DO
- Save stocks tickers data from Yahoo Finance to Google BigQuery
- Create a Great Expectation Suite and Checkpoints using the Great Expectation package to validate and test the loaded data (Validation)
- Automate styling and formatting by adding the following tasks (quality gates):
    - a task for formatting python code using black lib
    - a task to check the linting using pylint, yamllint, sqlfluff
    - a task to run unit tests using pytest, pytest-cov
- Setup A dbt-core project as a transformation layer above the source data
- Build the stocks transformations with dbt (Transformation)
- Add dbt tests (+freshness to the source) to all transformations
- Add python unit testing to test core python scripts functionality
- Create a dashboard to share those transformations (BI)
