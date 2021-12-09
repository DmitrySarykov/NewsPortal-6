from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import *
from .models import PostCategory, User
 
 
@receiver(m2m_changed, sender=PostCategory)
def send_post(sender, instance, action, **kwargs):
    if action=="post_add":
        categories = instance.category.all()
        users = User.objects.filter(category__in = categories).exclude(email='').distinct()
        
        for user in users:
            send_mail.delay(user_pk=user.pk,post_pk=instance.pk)
