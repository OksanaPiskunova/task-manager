from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project, Task
from task_manager.task_manager.serializers import UserSerializer, EmployeeSerializer, ProjectSerializer, TaskSerializer
from task_manager.task_manager.permissions import IsManagerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing User objects
    """
    permission_classes = (permissions.IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Employee objects
    """
    permission_classes = (IsManagerOrReadOnly, )
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Project objects
    """
    permission_classes = (IsManagerOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Task objects
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
