<h1 align="center"> Продуктовый помощник <a href="http://food-gramm.sytes.net/" target="_blank">Foodgram</a>
<img src="https://github.com/goforbg/telegram-emoji-gifs/blob/master/wine-glasses.gif" height="30"/></h1>

<a href="http://food-gramm.sytes.net/" target="_blank">Foodgram</a>, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

<h2>Мы используем:</h2>

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](http://food-gramm.sytes.net/api/docs/)   <img src="https://free-images.com/or/a309/arrow_outline_red_left_1.jpg" height="15"/>   здесь "живёт" документация к API проекта

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone https://github.com/NIK-TIGER-BILL/foodgram-project-react
```
## Для работы с удаленным сервером💻 (на ubuntu):
* Выполните вход на свой удаленный сервер

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Локально отредактируйте файл infra/nginx.conf, вписав в строку server_name свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

* Cоздайте .env файл и впишите <img src="https://github.com/goforbg/telegram-emoji-gifs/blob/master/pencil-writing.gif" height="20"/>:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
    ```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    SECRET_KEY=<секретный ключ проекта django>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    ```
    Workflow состоит из трёх шагов:
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.
  
* На сервере соберите docker-compose:
```
sudo docker-compose up -d --build
```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
    - Примените миграции:
    ```
    sudo docker-compose exec backend python manage.py makemigrations
    sudo docker-compose exec backend python manage.py migrate
    ```
    - Загрузите ингридиенты  в базу данных (необязательно):  
    *По умолчанию выбирается файл ingredients.json*
    ```
    sudo docker-compose exec backend python manage.py load_ingredients <Название файла из директории data>
    ```
    - Создайте суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
<h3 align="center"> 👨🏼‍💻Проект подготовил <a href="https://github.com/Kerones/" target="_blank">Василий Гантимуров</a> совместно с <a href="https://github.com/yandex-praktikum/"target="_blank">Yandex Practicum</a> <img src="https://yt3.googleusercontent.com/-pnsqu0xQYwxMhUVq-HZJHf691DEhTlEl1fZvjUtUwJIKMyTqXDBVvK7d2dSjFUTYdHFpTYvAo8=s900-c-k-c0x00ffffff-no-rj" height="18"/ </h3>
