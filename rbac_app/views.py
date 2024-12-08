from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Role, Permission, AuditLog
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, AuditLogSerializer


class UserManagementView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({'success': True, "message": "Users retrieved successfully", 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, "message": "Failed to retrieve users", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
            roles = Role.objects.filter(id__in=data.get('role_ids', []))
            user.roles.set(roles)
            user.save()
            return Response({'success': True, 'message': 'User created successfully.', "data": {"username": user.username}})
        except Exception as e:
            return Response({'success': False, "message": "Failed to create user", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleManagementView(APIView):
    def get(self, request):
        try:
            roles = Role.objects.all()
            serializer = RoleSerializer(roles, many=True)
            return Response({'success': True, "message": "Roles retrieved successfully", 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, "message": "Failed to retrieve roles", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if not request.user.is_staff:  # Restrict role management to admins only
                return Response({"success": False, "message": "Only admins can assign permissions"},
                                status=status.HTTP_403_FORBIDDEN)

            data = request.data
            role = Role.objects.create(name=data['name'])
            permissions = Permission.objects.filter(id__in=data['permission_ids'])
            role.permissions.set(permissions)
            return Response({'success': True, 'message': 'Role created and permissions assigned', "data": {"role": role.name}})
        except Exception as e:
            return Response({'success': False, "message": "Failed to create role", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionManagementView(APIView):
    def post(self, request):
        try:
            serializer = PermissionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "message": "Permission created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"success": False, "message": "Failed to create permission", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, "message": "Failed to process permission creation", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            permissions = Permission.objects.all()
            serializer = PermissionSerializer(permissions, many=True)
            return Response({'success': True, "message": "Permissions retrieved successfully", 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, "message": "Failed to retrieve permissions", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccessValidationView(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data['username']
            action = data['action']
            resource = data['resource']

            user = User.objects.get(username=username)
            has_access = user.roles.filter(permissions__name=action, permissions__resource=resource).exists()
            AuditLog.objects.create(
                user=user,
                action=action,
                resource=resource,
                outcome='granted' if has_access else 'denied'
            )
            return Response({"success": has_access, "message": "Access granted" if has_access else "Access denied"})
        except User.DoesNotExist:
            return Response({"success": False, "message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, "message": "Failed to validate access", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuditLogView(APIView):
    def get(self, request):
        try:
            logs = AuditLog.objects.all()
            serializer = AuditLogSerializer(logs, many=True)
            return Response({'success': True, "message": "Audit logs retrieved successfully", 'data': serializer.data})
        except Exception as e:
            return Response({'success': False, "message": "Failed to retrieve audit logs", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RolePermissionsView(APIView):
    def get(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            permissions = role.permissions.all()
            serializer = PermissionSerializer(permissions, many=True)
            return Response({"success": True, "message": "Permissions retrieved successfully", "data": serializer.data})
        except Role.DoesNotExist:
            return Response({"success": False, "message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, "message": "Failed to retrieve role permissions", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
