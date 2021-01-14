# airflow doc. 을 보면서 정리한 세부사항 및 알아두면 좋을 것들
### link: https://airflow.apache.org/docs/

### 1. [UI/Screenshots](#ui/screenshots)
### 2. [Concepts](#concepts)

=========================

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

