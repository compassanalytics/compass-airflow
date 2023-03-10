#%%
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from src.google.updaters import google_jobs

#%%
default_args = {
    "owner": "compass_airflow",
    "depends_on_past": False,
}

with DAG(
    "google_jobs_flows",
    default_args=default_args,
    description="All flows migrating Google data to S3",
    schedule_interval="@daily", 
    start_date=days_ago(0),
    tags=["google", "jobs"]
) as dag:

    t_jobs = PythonOperator(
        task_id="jobs",
        python_callable=google_jobs
    )