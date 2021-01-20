# airflow-study
airflow tutorial &amp; study

1. [Airflow 란?](#airflow-란?)  
2. [Quick Start](#quick-start)
3. [Tutorial](#tutorial)

---------------------

## Airflow 란? 
https://airflow.apache.org/
- workflow management tool 임
- 원칙: Dynamic(pipeline 생성에 있어서 동적으로 코드 관리), Extensible(각자의 operator, executor 를 확장 가능), Elagant(pipeline 이 간결하고 명시적), Scalable(modular 구조와 메시지 큐 이용으로 n 개의 워커 위에서 돌아갈 수 있고, 무한히 확장이 가능함)
- Airflow 는 strom, spark streaming 같은 데이터 스트리밍 솔루션이 아니기 때문에 각 task 는 데이터를 이동 시켜 주지 않는다. 
- 사용하는 이유
 : ETL 작업 등 여러 시퀀셜한 로직등이 필요로 하는 작업이 있을 때 이를 관리할 수 있는게 필요함. 보통 관리할게 적다면 cron 등과 같은 자동 실행 도구를 사용하겠지만 작업이 많아질 경우 관리가 어려워짐. 이런걸 worklow management 라고 하며 기존 hadoop oozie, luigi 같은 솔루션이 있었음
 : 여러 작업들의 연결성(의존성) 을 관리할 수 있어서, 이전 작업의 결과가 다음 작업에 영향을 미침
- 선행 작업이 실패하면 후속 작업은 멈추게 되고, 연관성 없는 task 는 병렬로 계속 실행
- python 기반으로 제작되어 있음,
- scheduling: 특정 간격으로 계속해서 실행함 (cron 과 비슷해 보이지만 보다 많은 기능을 제공.. 하겠지?)
- backfill: 과거의 작업을 실행
- DAG(Directed Acyclic Graph; 방향성을 가진 비순환 그래프)기반으로 작업이 이루어짐
- DAG 시각화를 통해 workflow 동작 과정을 관리할 수 있음
(주의: 시간 설정시 UTC 를 사용하기 때문에 한국 시간은 +9hour 를 고려해야 함)

- webserver와 scheduler 두개를 실행 시키고 시작

```
$ airflow webserver
$ airflow scheduler
```

- Webserver: 웹 UI를 표현, workflow 상태 표시 실행, 조작 등 관리
- Scheduler: 설정한 작업 기준이 충족되었는지 확인, 선행 작업 확인, OK 하면 현재 task 들이 worker에 의해 실행됨
- python으로 task1 정의할 때 bashOperator 로 shell 명령어 넣을 수 있음 , task1 >> task2 이런식으로 선행 관계를 명시 할 수 있음 (BashOperator: Bash Command 실행, PythonOperator: Python 함수 실행, BigQueryOperator: BigQuery -> Table 저장 그 외 다양한 Operator 존재)
- 의존 관계는 >> , << 로도 가능한데 full 로는 아래와 같이 표현 함
- 세번째 줄은 task1 후에 task2, task3 병렬 실행을 의미함

```
task1.set_downstream(task2)
task2.set_upstream(task1)
task1 >> [task2, task3]
```

- 자세한 예시는 튜토리얼(https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html) 참고
- schedule 은 crontab 표현을 사용함 
- Operator가 instance 가 되면 task 라 불림
- Pool: 동시성 제어를 위해 활용되며 web console 을 통해 관리 가능 하며 지정된 slot 만큼 동시에 실행(thread pool 느낌인가?)
- Priority Weight: task 단위로 지정하며 기본 값은 1, 숫자 값이 높을수록 우선순위 지정됨. 
- 위의 두 pool 과 priority 문제를 저절히 사용하여 부하를 조정하며 성능을 튜닝할 수 있음

## 다른 Workflow Management 와의 차이점은 뭐지?
1. oozie : airflow 에 비해 web gui 도 약하고 java나 xml 로 관리함, 파이프 라인 구축이 복잡함, 대체적으로 UI 와 task 의존성 관리 측면에서 airflow 가 우수하다는 의견이 많음, 그리고 표현이 간결한 게 airflow 장점으로 꼽힘


## DAG Runs
DAG가 인스턴스화 되어서 실행하는 상태(?)를 나타냄
DAG에는 *schedule_interval* 을 이용하여 스케쥴링을 하고 cron 표현을 이용하여 설정할 수가 있고, timedelta 로도 표현이 가능하고, 또 cron의 "presets"을 이용할수도 있음. 

cron 의 presets 이란?

```
None: 스케쥴링 하지 않고 트리거에 의해 동작
@once
@hourly : 0 * * * *
@daily: 0 0 * * * 
@weekly: 0 0 * * 0
@monthly: 0 0 1 * *
@quarterly: 0 0 1 */3 *
@yearly: 0 0 1 1 *
```

### Passing Parameters when triggering dags
CLI를 통해서 실행시키거나, REST API, UI를 통해서 트리거를 할 때 json blob을 통해서 job을 건낼 수 있다. 
근데 트리거를 이용하면!!! 스케쥴링에는 안맞을 수도 있음...

kwargs를 이용하면 python 함수를 통해 pythonOperator를 이용해야 함... => 그러면 이전 dag 설정 같은 부분은 불리할 수도 있음!

```python
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

dag = DAG("example_parametrized_dag", schedule_interval=None, start_date=days_ago(2))

#print_arguments 함수는 kwargs를 활용하는 예시를 위해 추가
def print_arguments(**kwargs):
    table_name = kwargs['dag_run'].conf.get('table')
    print(table_name)

parameterized_task = BashOperator(
    task_id='parameterized_task',
    bash_command="echo value: {{ dag_run.conf['conf1'] }}",
    dag=dag,
)

```
----------------------

## Quick Start
Link : https://airflow.apache.org/docs/apache-airflow/1.10.14/tutorial.html / https://airflow.apache.org/docs/apache-airflow/1.10.14/installation.html

Mac OS
```
$ sudo easy_install pip  // brew install python -> pip3 로 설치됨 (pip -V 로  20.2.4 확인)

$ sudo -H pip install apache-airflow // pip 버전이 20.3 이상이라면 --use-deprecated legacy-resolver 옵션 추가

//실제 command 는 아래 임 permission 문제 때문에 --user 옵션을 추가하고 실행함
$ sudo -H pip install --user apache-airflow==1.10.14 --use-deprecated legacy-resolver --constraint https://raw.githubusercontent.com/apache/airflow/constraints-1.10.14/constraints-2.7.txt

$ pip freeze | grep airflow
$ vi ~/.bash_profile //path 설정
$ airflow db init
$ airflow users create \
--username admin \
--firstname kim \
--lastname hongji \
--role Admin \
--email hayz.de@kakaoenterprise.com

$ airflow webserver --port 8080
$ airflow scheduler
```
![image](https://user-images.githubusercontent.com/36401495/104279878-5df1a800-54ee-11eb-8de3-986170102f4d.png)

## Tutorial

### 코드 설명
1. Default Arguments: dictionary 형식으로 표현된 DAG 생성자에 대한 기본 변수 설정 값
특정한 operator (ex, BaseOperator)에 대한 설정은 Document를 참고하면 됨

```python
default_args = {
    'owner': 'airflow',                                #owner of the task
    'depends_on_past': False,                          #이전 task의 성공 여부를 반영하여 실행할지
    'start_date': days_ago(2),                         
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
```

```
** 주의 **
execution_date: 실행 날짜가 아니라 실행을 시작하려한 시간이다.
항상 UTC 기준으로의 시간을 생각해라!
start_date: 첫 DAG 시작 시간으로, 정적인 값이다!
schedule_interval: cron or timedelta 값을 받음, 주기적인 실행에 필요
```

2. DAG 생성
DAG object 를 생성해야함. 가장 첫줄은 dag_id로 unique한 identifier임.
또한 schedule_interval을 설정해야 함.

```python
dag = DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)
```

3. Task 설정
첫줄은 마찬가지로 task_id 로 unique 함.
task에 대한 규칙 및 룰
 (1) argument 명시하여 보내라
 (2) dictionary(default_args)에 있는 arguments를 override하여 사용하며, operator의 특별 argument 를 조합하라
    (ex, bash_command, task_id etc)
 (3) task_id와 owner 는 무조건 명시
 
 ```python
 t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)
 ```

4. Templating with Jinja 
 - Jinja Templating 이란? (https://jinja.palletsprojects.com/en/2.11.x/)
   : 파이썬 위에서 디자인을 원활히 해주기 위한 templating 언어/ 웹으로 확인을 할 수 있도록?
 - Airflow 에서의 역할은 파라미터들을 전달해줌. params에 건내 받은 인자를 이용해 bash_command 에서 받은 인자를 이용 
   params는 dictionary 형태로 선언.
   
```python
templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)
```
   
5.DAG 와 tasks document
DAG나 각 싱글 task에 대해서 각각 문서를 추가할 수 있고, DAG는 md만 지원하고, 각 task는 string, md, json, yaml 모두 지원함

```python
dag.doc_md = __doc__

t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""
```

6. 의존성 설정
예로 t1, t2, t3의 task가 선언이 되어 있을 때
아래와 같이 선언이 가능하다. 기본적으로 set_downstream은 >> 와 같고, set_upstream은 << 와 같이 표현이 가능하다.

```python
t1.set_downstream(t2)
t2.set_upstream(t1)
t1 >> t2
t2 << t1
t1 >> t2 >> t3 #chaining
t1 >> [t2, t3] #parallel
```

7. test
아래를 실행했을 때 아무것도 일어나지 않는다면, 코드 문제 없이 잘 컴파일 된것임
```
$ python ~/airflow/dags/tutorial.py
$ airflow list_dags #print the list of active DAGs
```

8. Task간 데이터를 주고 받아야 하는 경우
xcom을 사용한다. (admin-xcom)
참고로 pythonOperator에서의 python_collable 함수에서는 return값이 자동으로 xcom에 push됨

```python
#저장하기 
task_instance = kwargs['task_instance']
task_instance.xcom_push(key='the key', value=my_str)

#불러오기
task_instance.xcom_pull(task_id='my_task', key='the key')
```
code: tutorial_hayz.py  
task1: print_date (bash: 'date')  
task2: print_wd  (base: 'pwd')  
![image](https://user-images.githubusercontent.com/36401495/104290430-ae243680-54fd-11eb-9c46-48e0a17674cc.png)


## 참고
 https://zzsza.github.io/data/2018/01/04/airflow-1/,
 
 https://zzsza.github.io/kyle-school/week6/#/, 
 
 https://airflow.apache.org/docs/apache-airflow/1.10.14/index.html
 
 카카오페이지 if kakao : https://mk.kakaocdn.net/dn/if-kakao/conf2019/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_2019/T03-S04.pdf)
