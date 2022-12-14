
install:
	pip install --upgrade pip &&\
		pip install -r requirement.txt

start:
	airflow webserver & airflow scheduler

run_dbt:
	cd ./dbt_transformations && dbt run

format:
	black *.y

lint:
	pylint --disable=R,C ./dags/*.py

# test:
# 	python -m pyrest -vv --cov=
