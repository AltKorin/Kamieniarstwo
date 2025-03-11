from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Client, Employee

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            if not Employee.objects.filter(user=instance).exists():
                Employee.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, position='Stanowisko testowe')
        else:
            if not Client.objects.filter(user=instance).exists():
                Client.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)