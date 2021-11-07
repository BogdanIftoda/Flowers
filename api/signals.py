from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from rest_framework_simplejwt.models import TokenUser

@receiver(post_save, sender=User)
def notify_task_save(sender, instance, **kwargs):
    TokenUser.objects.create(user=instance)