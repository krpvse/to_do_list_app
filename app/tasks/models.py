from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=42, verbose_name='Заголовок')
    task_type = models.CharField(max_length=10, verbose_name='Тип задачи')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнена')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'Задача: {self.title} | Тип задачи: {self.task_type} | Пользователь: {self.user}'
