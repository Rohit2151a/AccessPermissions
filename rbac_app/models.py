from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=100)  # Action (e.g., read, write)
    resource = models.CharField(max_length=100)  # Resource (e.g., API_ONE)

    def __str__(self):
        return f"{self.name} - {self.resource}"


# Custom User model
class User(AbstractUser):
    # To avoid conflicts, define explicit related names for groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )
    roles = models.ManyToManyField('Role', related_name='users')


# Role model
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.name


# Audit Log model
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    outcome = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)


