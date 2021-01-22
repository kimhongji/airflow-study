# Airflow 관련 FAQ

Airflow 관련하여 자주하는 질문, 헷갈리는 것들

----------------

Q. 생성한 테스크가 스케쥴링 되지 않아요!
A. 다양한 이유들이 있음. 
  1. airflow 엔진에 본인의 DAG 가 컴파일 되어 있지 않을 수 있으니 아래 커맨드를 통해 확인해 보고, 두번째 커맨드를 통해 DAG의 tree를 확인 해 볼수 있음.
  안나온다면.. airflow dags 에 업로드가 안된거임 $AIRFLOW_HOME/dags 폴더 안에 정의한 dag python 파일이 있나 확인해 보삼.
  
    ```
    $ airflow dags list
    $ airflow tasks list (task_id) --tree
    ```
  
  2. airflow 가 기본적으로 DAG 에 "airflow" 나 "DAG" 가 언급이 되어 있지 않은거를 무시할 수 있음! 
  3. *start_date* 가 적절하게 설정이 되었나? airflow scheduler는 *start_date* + *schedule_interval* 되면 작업을 시작함.
  3. *schedule_interval* 이 적절하게 설정이 되었나? default는 하루(datetime.timedelta(1))이고, 변경하려면 DAG 오브젝트에서 설정해야함!
  4. *start_date*를 현재 시점 보다 뒤로 하진 않았는가? 
  5. 혹시 이전의 task의 의존성이 존해하지는 않은가? 이전 task가 성공해야 다음 task가 실행되는 *depends_on_past*가 true로 되어있지는 않은지 확인해보삼
  6. *concurrency*파라미터와 *max_active_runs* 에 대해서 알아보고 확인해보기
  
  
Q. *start_date*는 어떻게 다루는건가여?  
A. now() 등과 같은 동적인 기간은 혼란스러울 수 있으므로 권유하지 않음. 그리고 *schedule_interval*을 설정할 때는 cron 형식을 취하는 것이 반복적인 스케쥴 관리에 좋음.

Q. catchup 파라미터는 뭔가요?  
A. catchup이 true 가 된다면, start_date와 현재 trigger된 시점에 따라 기존 돌아가지 못했던 DAG를 순차적으로 실행할 수 있게 하함. 

Q. DAG를 통적으로 생성할 수 있을 까?  
A. airflow는 /dags 폴더를 확인하며 탐색을 함. dag_id 이름을 동적으로 생성해 가는데 기본적인 *globals()* 함수를 이용한 것이고, python에서 dictionary역할을 함
 
```python
def create_dag(dag_id):
    """
    A function returning a DAG object.
    """

    return DAG(dag_id)


for i in range(10):
    dag_id = f'foo_{i}'
    globals()[dag_id] = DAG(dag_id)

    # or better, call a function that returns a DAG object!
    other_dag_id = f'bar_{i}'
    globals()[other_dag_id] = create_dag(other_dag_id)
```

Q. dag 연산을 더 빠르게 할 순 없는지?
A. 다양한 방법들이 있음. 보통 airflow.cfg 의 파라미터를 튜닝 하는 방식임
 - *parallelism* : airflow의 전체 클러스터에서 task 인스턴스가 동시에 돌아가는 갯수를 관리함
 - *concurrency* : 스케쥴러가 돌아가는 dag에서 최대..? dag에서 설정하지 않으면 cfg의 *dag_concurrency* 값을 이용함
 - *task_concurrency*
 - *max_active_runs*
 - *pool*
 
 
