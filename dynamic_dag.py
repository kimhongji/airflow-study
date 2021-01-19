# Dynamically Generating DAGs in Airflow

from datetime import datetime
from airflow import DAG

from airflow.operators.python_operator import PythonOperator

def create_dag(dag_id, schedule, dag_number, default_args):
	def hello_world_py(*args):
		print("hello world")
		print("this is DAG: {}".format(str(dag_number)))


	dag = DAG(dag_id, schedule_interval = schedule, default_args = default_args)


	with dag:
		t1 = PythonOperator(
			task_id = "hello!",
			python_callable=hello_world_py,
			dag_number=dag_number
			)


	return dag

for n in range(1, 10):
	dag_id = 'hello_world_{}'.format(str(n))

	default_args = {
		'owner' :'hayz',
		'start_date' : datetime(2020,1,20)
	}

	schedule = '@daily'

	dag_number = n

	globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args) 