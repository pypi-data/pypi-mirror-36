JENNIFER5 Python
===================

JENNIFER 5, JenniferSoft APM Python agent

제니퍼란?
제니퍼는 Python 환경에서 운영 중인 시스템을 실시간 모니터링(Monitoring) 할 수 있는 APM 프로그램입니다. 
Python 환경에서의 모든 트랜잭션과 인프라 전반에서 대한 정확하고 심층적인 상세 정보를 통해 운영 중인 시스템을 최소한의 부하로 모니터링 해 보세요.

제니퍼 Python agent 설치방법
----------------------------

제니퍼 에이전트를 일반적으로 설치하는 방법을 설명한다. PyPI(pip)를 통해서
설치한다.

1. 지원 범위

   1. OS: Linux 배포판과 macOS를 지원한다
   2. Python: CPython의 2.x버전은 2.7 이상, 3.x 버전은 3.3 이상을
      지원한다.
   3. Web framework 지원 범위

      1. `Flask >= v0.11`_
      2. `django >= v1.5`_

   4. DB driver

      1. MySQL or MariaDB

         1. `mysqlclient`_
         2. `pymysql`_

      2. sqlite3

         1. `sqlite3`_

2. 설치 방법

   1. pip를 통해서 jennifer를 설치한다.

      .. code:: sh

         $ pip install jennifer

   2. 설정 방법

      설치하고 나면 ``jennifer-admin``\ 이라는 커멘드가 설치된다.
      제니퍼 에이전트를 시작하기에 앞서서 JENNIFER의 data server와 연결시에
      필요한 설정들을 마쳐야 한다. 설정 템플릿은 명령어를 통해서 가능하다.

      .. code:: sh

         $ jennifer-admin generate-config

      해당 명령어를 실행하면 ``jennifer.ini``\ 파일이 생성된다. 생성된
      파일의 각 필드에 대해서 설명하면

      +-----------------------------------+-----------------------------------+
      | 필드                              | 설명                              |
      +===================================+===================================+
      | server_address                    | data server의 IP                  |
      +-----------------------------------+-----------------------------------+
      | server_port                       | data server의 port                |
      +-----------------------------------+-----------------------------------+
      | domain_id                         | 도메인 ID, 테스트를 신청하면      |
      |                                   | 제니퍼에서 제공한다.              |
      +-----------------------------------+-----------------------------------+
      | inst_id                           | 인스턴스의 아이디                 |
      +-----------------------------------+-----------------------------------+
      | log_path                          | log 파일의 경로                   |
      +-----------------------------------+-----------------------------------+

   3. ``inst_id``\ 의 설정방법 인스턴스의 ID는 Data server가 agent를
      식별하기 위한 값이다. Data server가 유니크하게 할당할 수 있기 때문에
      -1로 적어두면 Data server가 할당한 값을 사용할 수 있다. 수동으로
      설정도 가능하지만, 권장하지 않는다.

   4. 실행 위 과정에서 생성한 설정파일을 가지고 이제 JENNIFER를 실행할 수
      있다.

      .. code:: sh

         $ JENNIFER_CONFIG_FILE=<설정파일 경로> jennifer-admin run <python 실행 코드>

      ``<설정파일 경로>``\ 는 위에서 생성한 설정파일의 경로를 의미한다.
      ``<python 실행  코드>``\ 는 기존에 파이썬 웹 애플리케이션 서버를
      실행하던 커맨드(예: python manage.py runserver, uwsgi -i uwsgi.ini,
      …)를 의미한다.

      예를들어,
      ``sh  $ JENNIFER_CONFIG_FILE=jennifer.ini jennifer-admin run uwsgi -i uwsgi.ini``
      위와 같이 실행할 수 있다.

License
--------

© Copyright 2018 JenniferSoft, All right reserved.


.. _Flask >= v0.11: http://flask.pocoo.org/
.. _django >= v1.5: https://www.djangoproject.com/
.. _mysqlclient: https://github.com/PyMySQL/mysqlclient-python
.. _pymysql: https://github.com/PyMySQL/PyMySQL
.. _sqlite3: https://docs.python.org/2/library/sqlite3.html
