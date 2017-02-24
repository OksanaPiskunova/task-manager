from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Employee(models.Model):
    MANAGER = 'Manager'
    DEVELOPER = 'Developer'
    ROLES = (
        (MANAGER, MANAGER),
        (DEVELOPER, DEVELOPER),
    )

    user = models.OneToOneField(User)
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=DEVELOPER
    )


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_employee(sender, instance, **kwargs):
    instance.employee.save()
