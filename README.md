### Что это за проект?:smiley_cat:
Всё просто: Api_YaMDb - это бэкенд для сбора отзывов и оценок о произведениях (книги, фильмы, музыка) + API реализованный на Django Rest Framework.
Он предоставляет интерфейс для удобного взаимодействия с бизнес-логикой сервиса в формате JSON.

### Начало взаимодействия с API :old_key:
После запуска проекта, в версии V1 доступны для GET-запросов все [эндпоинты](http://127.0.0.1:8000/api/v1/) кроме списка пользователей http://127.0.0.1:8000/api/v1/users/. (Доступен только администратору)
Для получения полного доступа к интерфейсу необходимо: 

1. Зарегистровать нового пользователя, отправив POST запрос 
с именем пользователя и почтой в формате:

```
{
"email": "user@example.com",
"username": "string"
}
```
на адрес http://127.0.0.1:8000/api/v1/auth/signup/. В ответ на указанную почту придёт письмо с кодом активации.

2. Получить JWT-токен, отправив POST запрос в формате: 
```
{
"username": "string",
"confirmation_code": "string"
}
```
на эндпоинт http://127.0.0.1:8000/api/v1/auth/token/. В ответ придёт токен в формате JSON.
Токен из строки "token" необходимо отправлять в headers запроса с ключом Authorization. Значение ключа в виде Bearer "ваш токен без ковычек".
Срок действия токена - 24 часа. Необходимо обновление по истечении срока.

### Документация проекта: :blue_book:
После запуска проекта (python3 manage.py runserver) документация со списком эндпоинтов доступна по ссылке:
http://127.0.0.1:8000/redoc


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Artem4es/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
py -m venv venv
```

```
source venv/Scripts/activate (venv/bin/activate для МасOS, Linux)
```

```
python -m pip install --upgrade pip (python3 далее везде для MacOS, Linux)
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
### This project was created and maintained by [Oleg Chebotarev](https://github.com/oleg4bat), [Dmitry Gerasimov](https://github.com/Dmitry-Ge) and [Artem Ezhov](https://github.com/Artem4es)
All rights reserved😆