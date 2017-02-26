from rest_framework import serializers
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to represent User model
    """
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'password')
        write_only_fields = ('password', )

    def create(self, validated_data):
        """
        Creating of User instance
        :param validated_data: values of fields
        :return: User instance
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        Updating of User instance
        :param validated_data: values of fields
        :return: User instance
        """
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to represent Employee model
    """
    class Meta:
        model = Employee
        fields = ('id', 'user', 'role', )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to represent Project model
    """
    def validate_managers(self, value):
        """
        Validation of field 'managers'
        :param value: field 'managers'
        :return: valid value or raise ValidationError
        """
        managers = value
        for manager in managers:
            if manager.role != Employee.MANAGER:
                raise serializers.ValidationError('Assigned manager is developer')

        return value

    def validate_developers(self, value):
        """
        Validation of field 'developers'
        :param value: field 'developers'
        :return: valid value or raise ValidationError
        """
        developers = value
        for developer in developers:
            if developer.role != Employee.DEVELOPER:
                raise serializers.ValidationError('Assigned developer is manager')

        return value

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'managers', 'developers')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to represent Task model
    """
    due_date = serializers.DateTimeField(
        format='%d-%m-%Y %H:%M:%S'
    )

    class Meta:
        model = Task
        fields = ('id', 'project', 'assigned_employee', 'title', 'description', 'due_date', 'type', 'status', )