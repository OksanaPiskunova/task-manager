from rest_framework import serializers
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', )


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', 'role', )


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', )


class DeveloperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description', 'managers', 'developers')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('project', 'assigned_employee', 'title', 'description', 'due_date', 'type', 'status', )
