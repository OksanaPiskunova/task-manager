# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_auto_20170224_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('type', models.CharField(choices=[('Bug', 'Bug'), ('Improvement', 'Improvement'), ('Feature', 'Feature')], default='Feature', max_length=15)),
                ('status', models.CharField(choices=[('To do', 'To do'), ('In progress', 'In progress'), ('Waiting for info', 'Waiting for info'), ('Testing', 'Testing'), ('Done', 'Done')], default='To do', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Developer', 'Developer')], default='Developer', max_length=10),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_manager.Employee'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_manager.Project'),
        ),
        migrations.AddField(
            model_name='project',
            name='developers',
            field=models.ManyToManyField(related_name='developers_projects', to='task_manager.Employee'),
        ),
        migrations.AddField(
            model_name='project',
            name='managers',
            field=models.ManyToManyField(related_name='managers_projects', to='task_manager.Employee'),
        ),
    ]