# airflow-study
airflow tutorial &amp; study

---------------------

## Airflow 란? https://airflow.apache.org/
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


----------------------

## Quick Start and Tutorial
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
code: tutorial_hayz.py
task1: print_date (bash: 'date')
task2: print_wd  (base: 'pwd')

![image](https://user-images.githubusercontent.com/36401495/104290430-ae243680-54fd-11eb-9c46-48e0a17674cc.png)


## 참고
 https://zzsza.github.io/data/2018/01/04/airflow-1/,
 
 https://zzsza.github.io/kyle-school/week6/#/, 
 
 https://airflow.apache.org/docs/apache-airflow/1.10.14/index.html
 
 카카오페이지 if kakao : https://mk.kakaocdn.net/dn/if-kakao/conf2019/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C_2019/T03-S04.pdf)
