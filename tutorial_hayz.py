from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': days_ago(2),
	'email': ['hayz.de@kakaoenterprise.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

dag = DAG(
	'tutorial_hayz',
	default_args=default_args,
	description='A simple tutorial DAG',
	schedule_interval=timedelta(days=1),
)

t1 = BashOperator(
	task_id='print_date',
	bash_command='date',
	dag=dag,
)

t2 = BashOperator(
	task_id='print_wd',
	depends_on_past=False,
	bash_command='pwd',
	retries=3,
	dag=dag,
)

t1 >> t2
