<h1 align="center"> Продуктовый помощник <a href="http://food-gramm.sytes.net/" target="_blank">Foodgram</a></h1>

<a href="http://food-gramm.sytes.net/" target="_blank">Foodgram</a>, "Продуктовый помощник". На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понаврившиеся рецепты в список "Избранное", а перед походом в магазин скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](http://food-gramm.sytes.net/api/docs/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Подготовка и запуск проекта
### Склонировать репозиторий на машину:
```
git clone https://github.com/Kerones/foodgram-project-react
```
## Для работы с удаленным сервером (на ubuntu):
* Выполните вход на удаленный сервер
* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker compose
```
* Локально отредаиктируйте файл infra/nginx.conf, вписав в строку server_name свой IP
* Скопируйте файл docker-compose.production.yml из директории infra на север:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
```
* Создайте .env файл и впишите свои данные: 
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
    ```
* Для работы с workflow добавьте в GitHub secrets переменные окружения:
    ```
    DOCKER_USERNAME="имя пользователя докерхаб"
    DOCKER_PASSWORD="пароль от докерхаб"
        
    SECRET_KEY="секретный ключ проекта Django"
    
    USER="username для подключения к серверу"
    HOST="IP вашего сервера"
    PASSPHRASE="пароль для сервера, если такой установлен"
    SSH_KEY="ваш SSH ключ (можно получить командой cat ~/.ssh/id_rsa)"
    ```
* На сервере соберите docker-compose:
  
```
sudo docker compose -f docker-compose.production.yml up -d --build
```
* Выполните следующие команды (только после первого деплоя):
    - Примените миграции:
    ```
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    ```
    - Загрузите подготовленные ингридиенты в базу данных:
    ```
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_models
    ```
    - Создайте суперпользователя Django:
    ```
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
    ```      
<h3 align="center"> ???????Проект подготовил <a href="https://github.com/Kerones/" target="_blank">Василий Гантимуров</a> совместно с <a href="https://github.com/yandex-praktikum/"target="_blank">Yandex Practicum</a> <img src="https://yt3.googleusercontent.com/-pnsqu0xQYwxMhUVq-HZJHf691DEhTlEl1fZvjUtUwJIKMyTqXDBVvK7d2dSjFUTYdHFpTYvAo8=s900-c-k-c0x00ffffff-no-rj" height="18"</h3>