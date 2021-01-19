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
  3. *start_date* 가 적절하게 설정이 되었나?
