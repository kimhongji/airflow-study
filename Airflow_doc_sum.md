# airflow doc. 을 보면서 정리한 세부사항 및 알아두면 좋을 것들
### link: https://airflow.apache.org/docs/

### 1. [UI/Screenshots](#ui/screenshots)
### 2. [Concepts](#concepts)
### 3. [Additional Functionality](#additional-functionality)

-----------------------------

## UI/Screenshots (https://airflow.apache.org/docs/apache-airflow/stable/ui.html)

1. web으로 들어가서 보면 현재 실행되고 있는 DAG 들 확인이 가능하고, 현재 succeeded, failed, running 인지 알 수 있음.
만약에 다 완료된 task 감추고 싶으면 cnf 파일에서 아래처럼 수정
```
show_recent_stats_for_completed_runs = False
```

2. Tree view는 pipeline 속에서 task들을 확인하고 오류가 난 부분이 없는지 visual 적으로 확인 가능
tree에 검은 테두리가 있는건: scheduled run 이고 / 검은 테두리가 없는건 임시적으로 triggered 된거임

3. Graph view는 DAG 그래프를 상태에 따라 표현해준다.

4. Variable View는 job을 진행하면서 사용되는 key-value 변수들을 관리함. key 값의 이름이 password, secret, api_key 등과 같은 단어가 있으면 자동적으로 감춰짐.
표시해도 괜찮으면 *hide_sensitive_variable_fields* 변수를 설정하면 됨.

5. Gantt Chart는 task 기간이나 중복되는건 없는지 등을 확인 할 수 있게 함. 그리고 bottleneck도 확인 할 수 있음(어디서 시간을 많이 잡는 지 등으로)

6. Task Duration은 과거의 n 번의 실행을 통해서 어떤 DAG 가 상대적으로 비용이 많이 소모가 되는지 등을 확인 할 수 있음

-------------------------
## Concepts

1. DAGs: 전체적으로 자신의 task들을 모아놓은 그래프라고 말할 수 있음.
airflow는 기본적으로 "airflow" 혹은 "DAG" 가 포함된 파이썬 파일을 기본적으로 찾고 이를 바꾸고 싶으면 *DAG_DISCOVERY_SAFE_MODE*를 False로 수정하면 됨.

2. Scope: DAG를 함수 내부의 local 로 선언할 수가 있는데, 내부의 *subDagOperator*를 이용하는 경우 용이함

3. Default Arguments: task내의 공통의 인자들을 관리하기에 용이함. 변경하고 싶다면 override 하면 됨

4. Context Manager: 새로운 operator를 자동으로 할당해주는 건데 아래 처럼 쓰인다.
```python
with DAG('my_dag', start_date=datetime(2016, 1, 1)) as dag:
    op = DummyOperator('op')

op.dag is dag # True

```

5. DAG Runs: DAG의 물리적인 인스턴스. 보통 schedular에 의해 생성되고 때론 trigger에 의해 생성됨.

6. execution_date: 실제로 DAG가 실행되는 시간

7. Task Instances: execution_date안에서 실행되고 있는 task를 말함

8. Task Lifecyle: No status -> scheduled -> queued -> running -> (success, failed) -> 필요시 retry

9. Operators: 각 operator는 하나의 task를 나타냄. 만약에 두 operator 가 데이터를 공유하고 싶다면, 하나의 operator로 결합할 수 있다. 
아니면 XCom이라는 operator간 통신할 수 있는 기능을 활용하면 된다. 
```
  (1) BashOperator: bash command 실행  
  (2) PythonOpeator: python 함수 실행  
  (3) EmailOperator: email 보내기  
  (4) simpleHttpOperator: Http request 보내기  
  (5) mysqloperator, sqliteoperator, jdbcoperator etc...(about SQL)  
```

----------------------------

## Additional Functionality

1. Hooks: 외부의 데이터베이스에 접근하기 위한 인터페이스.  

2. Pools: task의 병렬 실행에 제한을 둬서 병목현상을 방지함. (UI에서 menu -> admin -> pools 에서 확인 가능) 우선순위 변수(*priority_weight*) 설정을 통해 우선순위를 설정할 수 있음.

3. Connections: 외부 시스템과 정보를 교환 하고 싶을때 사용하며 *conn_id* 를 이용함. 

4. Queues: 기본 queue 설정은 airflow.cfg의 celery -> default_queue에 있음. 

5. XComs: task간의 메시지를 교류할 수 있게 해주는 "cross-communication"의 약어임. 원칙적으로 key-value 형태로 정의되며, pushed 와 pulled 를 사용하여 주고 받음.  
``` 
 주의) max size는 48KB 정도로 대용량 파일 전송의 용도로는 적합하지 않음!
```

*provide_context* 설정을 꼭 *true* 해야 함

```python
 # inside a PythonOperator called 'pushing_task'
def push_function():
    return value

# inside another PythonOperator where provide_context=True
def pull_function(**context):
    value = context['task_instance'].xcom_pull(task_ids='pushing_task')
 ```
