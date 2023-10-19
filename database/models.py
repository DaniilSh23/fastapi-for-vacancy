"""
Модели ORM
"""

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Questions(models.Model):
    question_id = fields.IntField()
    question = fields.CharField(max_length=255)
    answer = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_id} | {self.question} | {self.answer}"


QuestionsPydantic = pydantic_model_creator(Questions, name="Questions")