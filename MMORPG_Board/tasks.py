from celery import shared_task
from django.contrib.auth.models import User
from .models import Post, Response
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_response_email(respond_id):
    respond = Response.objects.get(id=respond_id)
    subject = 'MMORPG Fans: новый отклик на объявление!'
    message = f'Доброго дня, {respond.post.author}! На ваше объявление есть новый отклик!\n' \
              f'Прочитать отклик: http://127.0.0.1:8000/responses/{respond.post.id}'
    send_mail(subject, message, 'zimina.nina202020@yandex.ru', [respond.post.author.email])

@shared_task
def send_acceptance_email(response_id):
    respond = Response.objects.get(id=response_id)
    subject = 'MMORPG Fans: Ваш отклик принят!'
    message = f'Доброго дня, {respond.author}, Автор объявления "{respond.post.title}" принял Ваш отклик!\n' \
              f'Посмотреть принятые отклики: http://127.0.0.1:8000/responses'
    send_mail(subject, message, 'zimina.nina202020@yandex.ru', [respond.post.author.email])

@shared_task
def send_weekly_posts_email():
    now = timezone.now()
    last_week_posts = Post.objects.filter(dateCreation__gte=now - timedelta(days=7))

    if last_week_posts:
        for user in User.objects.all():
            post_list = '\n'.join([f'{post.title}\nhttp://127.0.0.1:8000/post/{post.id}' for post in last_week_posts])
            subject = 'MMORPG Fans: посты за прошедшую неделю.'
            message = f'Доброго дня, {user.username}!\nПредлагаем Вам ознакомиться с новыми объявлениями, ' \
                      f'появившимися за последние 7 дней:\n{post_list}'
            send_mail(subject, message, 'zimina.nina202020@yandex.ru', [user.email])
