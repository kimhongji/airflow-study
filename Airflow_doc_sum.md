# airflow doc. 을 보면서 정리한 세부사항 및 알아두면 좋을 것들
link: https://airflow.apache.org/docs/

1. [UI/Screenshots](#ui/screenshots)
2.

-------------------------

## UI/Screenshots (https://airflow.apache.org/docs/apache-airflow/stable/ui.html)

1. web으로 들어가서 보면 현재 실행되고 있는 DAG 들 확인이 가능하고, 현재 succeeded, failed, running 인지 알 수 있음.
만약에 다 완료된 task 감추고 싶으면 cnf 파일에서 아래처럼 수정
```
show_recent_stats_for_completed_runs = False
```

2. Tree view는 pipeline 속에서 task들을 확인하고 오류가 난 부분이 없는지 visual 적으로 확인 가능
tree에 검은 테두리가 있는건: scheduled run 이고 / 검은 테두리가 없는건 임시적으로 triggered 된거임

3. Graph view는 


