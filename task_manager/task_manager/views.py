from rest_framework import viewsets
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project, Task
from task_manager.task_manager.serializers import UserSerializer, EmployeeSerializer, ProjectSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()\
        .filter(managers__role=Employee.MANAGER)\
        .filter(developers__role=Employee.DEVELOPER)
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
