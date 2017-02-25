from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

# Set default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
app = Celery('task_manager', broker=settings.BROKER_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Logger
logger = get_task_logger(__name__)

# Load all necessary modules and classes
import django
django.setup()

# Now can load models
from task_manager.task_manager.models import Task


# Register periodic tasks
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, day_of_week='mon-fri')
    )


# Task to mailing notifications for the assigneed to the employee tasks
@app.task
def test():
    tasks = Task.objects.select_related('assigned_employee__user')
    for task in tasks:
        employee = task.assigned_employee
        message = 'You have task {0} ({1}, {2}) at Task Manager. Due date: {3}'.format(
            task.title, task.type, task.status, task.due_date
        )
        send_mail('Task Manager', message, 'task.manager@task.com', [employee.user.email, ])

    logger.info('Printed value')
