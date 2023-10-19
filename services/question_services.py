"""
Модуль с сервисами для бизнес-логики вопросов викторины.
"""
from typing import Tuple

import aiohttp

from database.models import Questions
from settings import GET_QUESTIONS_URL, MY_LOGGER


class QuestionService:
    """
    Класс с сервисами, описывающие бизес-логику для работы с вопросами.
    """
    @staticmethod
    async def get_questions(question_numb: int) -> Tuple[int, str | list]:
        """
        Метод для получения заданного количества вопросов и обработки их
        """
        # Кидаем запрос для получения новых вопросов
        status, content = await QuestionService.req_for_get_questions(question_numb)
        if status != 200:
            return status, content

        # Обрабатываем новые вопросы
        new_questions = list()
        for i_question in content:    # Итерируемся по каждому вопросу из ответа
            MY_LOGGER.debug(f'Обрабатываем вопрос с ID == {i_question.get("id")}')
            while True:
                question_obj, created = await Questions.get_or_create(
                    question_id=i_question.get('id'),
                    defaults={
                        "question": i_question.get('question'),
                        "answer": i_question.get('answer'),
                    }
                )
                if created:     # Если вопрос был создан, то тормозим бесконечный цикл
                    MY_LOGGER.debug(f'Вопрос с ID == {i_question.get("id")} не найден в БД и будет создан')
                    break
                MY_LOGGER.warning(f'Вопрос с ID == {i_question.get("id")} найден в БД, запрашиваем другой вопрос!')

                # Запрашиваем ещё один вопрос
                status, content = await QuestionService.req_for_get_questions(question_numb=1)
                if status != 200:
                    return status, content
                i_question = content[0]
            new_questions.append(question_obj)
        return 200, new_questions

    @staticmethod
    async def req_for_get_questions(question_numb: int) -> Tuple[int, str | dict]:
        """
        Метод для выполнения GET запроса и получения JSON ответа с новыми вопросами
        """
        # Выполняем запрос для получения нужного числа вопросов
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{GET_QUESTIONS_URL}?count={question_numb}') as response:
                if response.status != 200:
                    msg = (f'Не удалось выполнить запрос для получения {question_numb!r} вопросов! | '
                           f'Ответ: {response.text}')
                    MY_LOGGER.warning(msg)
                    return 400, msg
                return 200, await response.json()