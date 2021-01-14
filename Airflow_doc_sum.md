# airflow doc. 을 보면서 정리한 세부사항 및 알아두면 좋을 것들

-------------------------

## UI / Screenshots
1. web으로 들어가서 보면 현재 실행되고 있는 DAG 들 확인이 가능하고, 현재 succeeded, failed, running 인지 알 수 있음.
만약에 다 완료된 task 감추고 싶으면 cnf 파일에서 아래처럼 수정
```
show_recent_stats_for_completed_runs = False
```
2. Tree view는 


