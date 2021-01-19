from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.utils.dates import round_time
from airflow.utils import timezone


default_args = {
	'owner': 'hayz',
	'depends_on_past': False,  #default status: False
	'start_date': round_time(timezone.utcnow(), timedelta(minutes=10)),
	'email': ['hayz.de@kakaoenterprise.com'],
	'email_on_failure': True,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

dag = DAG(
	'straw_delivery',
	default_args=default_args,
	description='A simple tutorial DAG',
	schedule_interval=timedelta(minutes=5),
)

t1 = BashOperator(
	task_id='straw-cli',
	bash_command='/Users/kakao_ent/git_straw/straw-cli-1.0.0-rc16/bin/straw-cli count  --strawUrl=(straw_url) --executorMemory 2G > $AIRFLOW_HOME/log',
	dag=dag,
)

t2 = BashOperator(
	task_id='print_result',
	depends_on_past=True,  #override argument
	bash_command='cat $AIRFLOW_HOME/log | grep RESULT > $AIRFLOW_HOME/result.log',
	retries=3,
	dag=dag,
)

t1 >> t2
