python 3.9.2 사용 

### 실행방법
가상환경 생성
* python3 -m venv venv 

* source venv/bin/activate

로컬 설치
* pip install -r requirements.txt

로컬 DB 생성
* python manage.py makemigrations
* python manage.py migrate
* python manage.py migrate --run-syncdb

로컬 실행
* python manage.py runserver

swaager 확인
* http://127.0.0.1:8000/swagger/

테스트 코드 실행
* pytest 

테스트 코드 커버리지 확인
* pytest --cov-report term --cov

