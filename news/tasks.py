from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from datetime import date, timedelta 
from news.models import Category, Post,User

@shared_task
def send_mail(user_pk,post_pk):
    user = User.objects.get(pk=user_pk)
    post = Post.objects.get(pk=post_pk)
    site = Site.objects.get_current()
    print(f'Отправка письма {user.email}')
    msg = EmailMultiAlternatives(subject=post.title,to=[user.email])
    html_content = render_to_string('post.html',{'post':post,'user':user,'site':site})
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_mail_category(today,category_pk):
    category = Category.objects.get(pk=category_pk)
    list_email = category.subscribers.exclude(email='').values_list('email',flat=True)
    if list_email :
        site = Site.objects.get_current()
        last_week = today - timedelta(days=7)
        news=Post.objects.filter(date__range=[last_week,today],category=category).order_by('date')
        print(f'Отправка письма {list_email}')
        msg = EmailMultiAlternatives(
            subject=f'{category.name}. Новости за неделю.',
            to=list_email, 
        )
        html_content = render_to_string('news_week.html',{'news_list':news,'site':site})
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# Рассылка еженедельных новостей 
@shared_task
def week_news():
    print('Новости за неделю')
    today = date.today()
    categories = Category.objects.exclude(subscribers=None)
    # Отправляем новости по каждой категории всем её подписчикам
    for category in categories:
        send_mail_category(today,category.pk)
