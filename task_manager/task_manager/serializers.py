from rest_framework import serializers
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups', 'password')
        write_only_fields = ('password', )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'user', 'role', )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    def validate_managers(self, value):
        managers = value
        for manager in managers:
            if manager.role != Employee.MANAGER:
                raise serializers.ValidationError('Assigned manager is developer')

        return value

    def validate_developers(self, value):
        developers = value
        for developer in developers:
            if developer.role != Employee.DEVELOPER:
                raise serializers.ValidationError('Assigned developer is manager')

        return value

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'managers', 'developers')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    due_date = serializers.DateTimeField(
        format='%D-%M-%Y %H:%M:%S'
    )

    class Meta:
        model = Task
        fields = ('id', 'project', 'assigned_employee', 'title', 'description', 'due_date', 'type', 'status', )