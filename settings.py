"""
Различные настройки для работы веб-приложения.
"""
import os
import sys
from pathlib import Path

import loguru
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = os.environ.get('DATABASE_PORT')

BASE_DIR = Path(__file__).resolve().parent

GET_QUESTIONS_URL = 'https://jservice.io/api/random'

# Настройки логгера
MY_LOGGER = loguru.logger
MY_LOGGER.remove()  # Удаляем все предыдущие обработчики логов
MY_LOGGER.add(  # Все логи от DEBUG и выше в stdout
    sink=sys.stdout,
    level='DEBUG',
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
MY_LOGGER.add(  # системные логи в файл
    sink=f'{BASE_DIR}/logs/sys_log.log',
    level='DEBUG',
    rotation='2 MB',
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

# Конфигурация БД
DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DATABASE_HOST,
                "port": DATABASE_PORT,
                "user": DATABASE_USER,
                "password": DATABASE_PASSWORD,
                "database": DATABASE_NAME,
            }
        },
    },
    "apps": {
        "models": {
            "models": ["database.models"],
            "default_connection": "default"
        }
    }
}
