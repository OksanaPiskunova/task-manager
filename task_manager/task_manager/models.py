from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Employee Model (manager or developer)
class Employee(models.Model):
    MANAGER = 'Manager'
    DEVELOPER = 'Developer'
    ROLES = (
        (MANAGER, MANAGER),
        (DEVELOPER, DEVELOPER),
    )

    user = models.OneToOneField(
        User,
        verbose_name='User'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=DEVELOPER,
        verbose_name='Role'
    )

    def __str__(self):
        return '{0} ({1})'.format(
            self.user.username, self.role
        )

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ('id', )


# Project Model
class Project(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name='Title'
    )
    description = models.TextField(
        verbose_name='Description'
    )
    managers = models.ManyToManyField(
        Employee,
        related_name='managers_projects',
        verbose_name='Managers'
    )
    developers = models.ManyToManyField(
        Employee,
        related_name='developers_projects',
        verbose_name='Developers'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('id', )


# Task model
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

    project = models.ForeignKey(
        Project,
        verbose_name='Project'
    )
    assigned_employee = models.ForeignKey(
        Employee,
        verbose_name='Assigned employee'
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Title'
    )
    description = models.TextField(
        verbose_name='Description'
    )
    due_date = models.DateTimeField(
        verbose_name='Due date'
    )
    type = models.CharField(
        max_length=15,
        choices=TYPES,
        default=FEATURE,
        verbose_name='Type'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=TO_DO,
        verbose_name='Status'
    )

    def __str__(self):
        return '{0} ({1}, {2})'.format(
            self.title, self.type, self.status
        )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('id', )


# Create Employee after creating User
@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


# Update Employee after updating User
@receiver(post_save, sender=User)
def save_employee(sender, instance, **kwargs):
    instance.employee.save()
