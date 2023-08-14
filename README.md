# Bakery

Сайт для доставки булочных изделий.

Ссылка на сайт: https://tework123.ru/

Ссылка на гитхаб: https://github.com/Tework123/Bakery/

## Стартовая страница сайта: 

![image](https://github.com/Tework123/Bakery/assets/115368408/b390d93f-fc53-40cf-a13e-99534999984c)


## Использованные технологии:

### Frontend(писал FalconBone):
- React

### Backend(писал Tework123):
- Flask Веб-фреймворк
- Flask restful Для удобного написания api
- Flask-login Создает сессии и куки
- Flask-SQLAlchemy Позволяет работать с базой данных через python классы и функции
- Flask-migrate Обеспечивает миграции базы данных
- Flask-Mail Отправляет сообщения на почту
- Pytest unit test


### Веб-приложение развернуто на VPS с помощью docker(из ветки main).

### Docker-conteiners:

- frontend(nginx+react-app)
- backend(flask(qunicorn))
- db(postgres)
- pgbackups
- certbot
- redis(cash)
- worker(celery)

## Функциональность сайта:

- авторизация пользователей по коду с почты или телефона
- панель админа для создания работников, просмотра статистики сайта
- панель работника пекарни для добавления контента, для просмотра заказов пользователей
- добавление позиций в корзину
- заказ и оплата позиций

Also:

- unit test api
- кеширование стартовой страницы
- проверка api с помощью postman
- сгенерированная документация api с postman


## Схема базы данных:

![image](https://github.com/Tework123/Bakery/assets/115368408/1b9c6443-78dc-4302-adc7-824a72329320)



## Документация api(postman):

https://documenter.getpostman.com/view/25883857/2s946k6B7S

## Макеты страниц:

ссылка на гугл диск с фоточками


## Установка:

Создаем новую папку, создаем виртуальное окружение, активируем его.

Подключаем git к папке:

    git init 
    git clone https://github.com/Tework123/Bakery.git

### Установка backend:

Заходим в папку с приложением flask:

    cd backend
    
Устанавливаем зависимости:

    pip install -r requirements.txt
    
Создаем два .env файла, один в папке с приложением flask, другой в папке с docker-compose.

Заполняем .env файл примерно так:

    SQLALCHEMY_DATABASE_URI_POSTGRES = 'postgresql://postgres:password@localhost:5432/name_db'
    SQLALCHEMY_DATABASE_URI_POSTGRES_prod = 'postgresql://postgres:password@db:5432/name_db'
    SQLALCHEMY_DATABASE_URI_POSTGRES_TEST = 'postgresql://postgres:password@localhost:5432/name_db_test'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_DB = 'name_db'
    
    SECRET_KEY = 'asldkk12kelakfjafkj23jijraijfi23jappweovm1'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'myemail@gmail.com'
    MAIL_PASSWORD = 'sadasdkmvxvvqlwl'
    ADMINS = 'myemail@gmail.com'
    ADMIN_LOGIN = 'admin@admin.com'
    ADMIN_PASSWORD = 'admin'
    REDIS_URL_LOCAL = 'redis://127.0.0.1:6379'
    REDIS_URL_server = 'redis://redis:6379'
    REDIS_PASSWORD = 'mzxcvm213zmvdsf@k3ll1'


Локально поднимаем postgres, redis.

### Установка frontend:

- some code



В папке с flask приложением запускаем локальный сервер:

    flask run
