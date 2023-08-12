<h1 align="center"> ����������� �������� <a href="http://food-gramm.sytes.net/" target="_blank">Foodgram</a></h1>

<a href="http://food-gramm.sytes.net/" target="_blank">Foodgram</a>, "����������� ��������". �� ���� ������� ������������ ����� ����������� �������, ������������� �� ���������� ������ �������������, ��������� ������������� ������� � ������ "���������", � ����� ������� � ������� ������� ������� ������ ���������, ����������� ��� ������������� ������ ��� ���������� ��������� ����.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](http://food-gramm.sytes.net/api/docs/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## ���������� � ������ �������
### ������������ ����������� �� ������:
```
git clone https://github.com/Kerones/foodgram-project-react
```
## ��� ������ � ��������� �������� (�� ubuntu):
* ��������� ���� �� ��������� ������
* ���������� docker �� ������:
```
sudo apt install docker.io 
```
* ���������� docker-compose �� ������:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker compose
```
* �������� ��������������� ���� infra/nginx.conf, ������ � ������ server_name ���� IP
* ���������� ���� docker-compose.production.yml �� ���������� infra �� �����:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
```
* �������� .env ���� � ������� ���� ������: 
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<��� ���� ������ postgres>
    DB_USER=<������������ ��>
    DB_PASSWORD=<������>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<��������� ���� ������� django>
    ```
* ��� ������ � workflow �������� � GitHub secrets ���������� ���������:
    ```
    DOCKER_USERNAME="��� ������������ ��������"
    DOCKER_PASSWORD="������ �� ��������"
        
    SECRET_KEY="��������� ���� ������� Django"
    
    USER="username ��� ����������� � �������"
    HOST="IP ������ �������"
    PASSPHRASE="������ ��� �������, ���� ����� ����������"
    SSH_KEY="��� SSH ���� (����� �������� �������� cat ~/.ssh/id_rsa)"
    ```
* �� ������� �������� docker-compose:
  
```
sudo docker compose -f docker-compose.production.yml up -d --build
```
* ��������� ��������� ������� (������ ����� ������� ������):
    - ��������� ��������:
    ```
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    ```
    - ��������� �������������� ����������� � ���� ������:
    ```
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_models
    ```
    - �������� ����������������� Django:
    ```
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
    ```      
<h3 align="center"> ???????������ ���������� <a href="https://github.com/Kerones/" target="_blank">������� ����������</a> ��������� � <a href="https://github.com/yandex-praktikum/"target="_blank">Yandex Practicum</a> <img src="https://yt3.googleusercontent.com/-pnsqu0xQYwxMhUVq-HZJHf691DEhTlEl1fZvjUtUwJIKMyTqXDBVvK7d2dSjFUTYdHFpTYvAo8=s900-c-k-c0x00ffffff-no-rj" height="18"</h3>