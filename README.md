# fastapi-for-vacancy
### Тестовое задание для вакансии

## Для запуска:
1. Создать файл ```.env``` и заполнить его переменными, указанными в примере (файл ```env```)
    - DATABASE_NAME=название БД
    - DATABASE_USER=пользователь БД
    - DATABASE_PASSWORD=пароль БД
    - DATABASE_HOST=my_db
    - DATABASE_PORT=5432
    - POSTGRES_VOLUME_PATH=путь к папке на диске, где будет хранится том для контейнера postgres 
    - FASTAPI_APP_PATH=путь к папке с проектом
2. Выполняем команду ```docker compose up -d```
3. Убеждаемся, что все окей работает, путем чтения логов ```docker compose logs -f```

