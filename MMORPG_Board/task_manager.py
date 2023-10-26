from datetime import datetime
from celery import shared_task
from django.contrib.auth.models import User
from .models import Post, Response
from django.core.mail import send_mail
from django.utils import timezone

def get_greeting():
    current_time = datetime.now().time()
    if current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 17:
        return "Добрый день"
    else:
        return "Добрый вечер"

@shared_task
def send_response_email(respond_id):
    greeting = get_greeting()
    respond = Response.objects.get(id=respond_id)
    subject = 'MMORPG Fans: новый отклик на объявление!'
    message = f'{greeting}, {respond.post.author}! На ваше объявление есть новый отклик!\n' \
              f'Прочитать отклик: http://127.0.0.1:8000/responses/{respond.post.id}'
    send_mail(subject, message, 'zimina.nina202020@yandex.ru', [respond.post.author.email])

@shared_task
def send_acceptance_email(response_id):
    greeting = get_greeting()
    respond = Response.objects.get(id=response_id)
    subject = 'MMORPG Fans: Ваш отклик принят!'
    message = f'{greeting}, {respond.author}, Автор объявления "{respond.post.title}" принял Ваш отклик!\n' \
              f'Посмотреть принятые отклики: http://127.0.0.1:8000/responses'
    send_mail(subject, message, 'zimina.nina202020@yandex.ru', [respond.post.author.email])

@shared_task
def send_weekly_posts_email():
    greeting = get_greeting()
    now = timezone.now()
    last_week_posts = Post.objects.filter(dateCreation__gte=now - timedelta(days=7))

    if last_week_posts:
        for user in User.objects.all():
            post_list = '\n'.join([f'{post.title}\nhttp://127.0.0.1:8000/post/{post.id}' for post in last_week_posts])
            subject = 'MMORPG Fans: посты за прошедшую неделю.'
            message = f'{greeting}, {user.username}!\nПредлагаем Вам ознакомиться с новыми объявлениями, ' \
                      f'появившимися за последние 7 дней:\n{post_list}'
            send_mail(subject, message, 'zimina.nina202020@yandex.ru', [user.email])
