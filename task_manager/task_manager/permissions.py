from rest_framework import permissions
from task_manager.task_manager.models import Employee


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Permission class.
    If employee is manager -> True
    Else -> False
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.id is None:
            return False

        user_id = request.user.id
        employee = Employee.objects.get(user=user_id)

        return employee.role == Employee.MANAGER
