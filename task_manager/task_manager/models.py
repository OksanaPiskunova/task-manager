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

    def __str__(self):
        return self.user.username + ' (' + self.role + ')'


class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    managers = models.ManyToManyField(Employee, related_name='managers_projects')
    developers = models.ManyToManyField(Employee, related_name='developers_projects')


class Task(models.Model):
    BUG = 'Bug'
    IMPROVEMENT = 'Improvement'
    FEATURE = 'Feature'
    TYPES = (
        (BUG, BUG),
        (IMPROVEMENT, IMPROVEMENT),
        (FEATURE, FEATURE),
    )

    TO_DO = 'To do'
    IN_PROGRESS = 'In progress'
    WAITING = 'Waiting for info'
    TESTING = 'Testing'
    DONE = 'Done'
    STATUSES = (
        (TO_DO, TO_DO),
        (IN_PROGRESS, IN_PROGRESS),
        (WAITING, WAITING),
        (TESTING, TESTING),
        (DONE, DONE),
    )

    project = models.ForeignKey(Project)
    assigned_employee = models.ForeignKey(Employee)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateTimeField()
    type = models.CharField(
        max_length=15,
        choices=TYPES,
        default=FEATURE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=TO_DO
    )


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_employee(sender, instance, **kwargs):
    instance.employee.save()
