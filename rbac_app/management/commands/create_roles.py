from django.core.management.base import BaseCommand
from rbac_app.models import Role, Permission


class Command(BaseCommand):
    help = 'Populate the Roles and Permissions tables with initial data'

    def handle(self, *args, **kwargs):
        # Create permissions
        permissions_data = [
            {'name': 'read', 'resource': 'API_ONE'},
            {'name': 'write', 'resource': 'API_TWO'},
            {'name': 'delete', 'resource': 'API_THREE'},
        ]

        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                name=perm_data['name'],
                resource=perm_data['resource']
            )
            if created:
                self.stdout.write(f"Permission '{permission}' created.")
            else:
                self.stdout.write(f"Permission '{permission}' already exists.")

        # Create roles and assign permissions
        roles_data = {
            'Staff': ['read', 'write'],  # API_ONE, API_TWO
            'Supervisor': ['read', 'write', 'delete'],  # API_ONE, API_TWO, API_THREE
            'Admin': ['read', 'write', 'delete']  # All APIs
        }

        for role_name, perms in roles_data.items():
            role, created = Role.objects.get_or_create(name=role_name)
            for perm_name in perms:
                permission = Permission.objects.get(name=perm_name)
                role.permissions.add(permission)
            if created:
                self.stdout.write(f"Role '{role_name}' created and permissions assigned.")
            else:
                self.stdout.write(f"Role '{role_name}' already exists.")
