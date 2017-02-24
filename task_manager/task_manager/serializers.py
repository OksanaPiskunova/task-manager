from rest_framework import serializers
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', 'role')


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', )


class DeveloperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', )
