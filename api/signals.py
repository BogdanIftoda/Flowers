from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from rest_framework_simplejwt.tokens import Token

@receiver(post_save, sender=User)
def notify_task_save(sender, instance, **kwargs):
    Token.objects.create(user=instance)