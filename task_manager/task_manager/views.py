from rest_framework import viewsets
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee
from task_manager.task_manager.serializers import UserSerializer, EmployeeSerializer, ManagerSerializer, DeveloperSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
