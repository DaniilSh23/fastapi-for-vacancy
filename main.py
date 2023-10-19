"""
Основной файл для запуска веб-приложения

$ uvicorn main:APP --reload
"""
from typing import Any

import uvicorn
from fastapi import FastAPI, Response
from tortoise.contrib.fastapi import register_tortoise

from database.models import QuestionsPydantic
from services.question_services import QuestionService
from settings import MY_LOGGER, DB_CONFIG

APP = FastAPI()


""" ДЕЙСТВИЯ ПО СТАРТУ И СТОПУ ВЕБ_ПРИЛОЖЕНИЯ """


@APP.on_event("startup")
async def startup():
    """
    Функция, которая будет выполняться при старте веб-приложухи
    """
    MY_LOGGER.debug(f'Выполнение действий при старте приложения')
    pass


@APP.on_event("shutdown")
async def shutdown():
    """
    Функция, которая будет выполняться при остановке приложухи
    """
    MY_LOGGER.debug('Выполнение действий при завершении работы приложения')
    pass

""" ЭНДПОИНТЫ """


@APP.get(path='/get_questions/', status_code=200, response_model=list[QuestionsPydantic])
async def get_questions(questions_numb: int = 1) -> Any:
    """
    Эндпоинт для получения вопросов
    """
    status, content = await QuestionService.get_questions(question_numb=questions_numb)
    if status != 200:
        return Response(status_code=status, content=content)
    # "Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины.
    # В случае его отсутствия - пустой объект." - задача не понятна.
    # Неоднозначно написано, что должно вернуть мое веб-приложение в ответ на запрос,
    # поэтому я буду возвращать вновь созданные вопросы
    return content


register_tortoise(
    app=APP,
    config=DB_CONFIG,
    # generate_schemas=True,
)


if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=8000)
