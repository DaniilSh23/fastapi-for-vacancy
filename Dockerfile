FROM python:3.11-slim

RUN mkdir "fastapi_app"

COPY requirements.txt /fastapi_app/

RUN apt update

RUN apt install python3-dev libpq-dev postgresql-contrib curl -y

RUN apt-get install build-essential -y

RUN pip install psycopg2-binary

RUN python -m pip install --no-cache-dir -r /fastapi_app/requirements.txt

COPY . /fastapi_app/

WORKDIR /fastapi_app

# Открываем 8000 порт
EXPOSE 8000

# Запуск
ENTRYPOINT ["/fastapi_app/entrypoint.sh"]