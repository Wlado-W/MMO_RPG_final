from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class BaseModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        abstract = True

class Post(BaseModel):
    CAT = (('tanks', 'Танки'),
           ('healers', 'Хилы'),
           ('damage_dealers', 'ДД'),
           ('dealers', 'Торговцы'),
           ('gildmasters', 'Гилдмастеры'),
           ('quest_givers', 'Квестгиверы'),
           ('blacksmiths', 'Кузнецы'),
           ('tanners', 'Кожевники'),
           ('potion_makers', 'Зельевары'),
           ('spell_masters', 'Мастера заклинаний'))
    category = models.CharField(max_length=15, choices=CAT, verbose_name='Категория')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = RichTextField(verbose_name='Текст объявления')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Response(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    text = models.TextField(verbose_name='Текст')
    status = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
