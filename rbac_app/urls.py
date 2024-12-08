from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserManagementView, RoleManagementView, PermissionManagementView, AccessValidationView, AuditLogView, RolePermissionsView

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('users/', UserManagementView.as_view(), name='user_management'),
    path('roles/', RoleManagementView.as_view(), name='role_management'),
    path('permissions/', PermissionManagementView.as_view(), name='permission_management'),
    path('validate-access/', AccessValidationView.as_view(), name='access_validation'),
    path('audit-logs/', AuditLogView.as_view(), name='audit_logs'),
    path('role-permissions/<int:role_id>/', RolePermissionsView.as_view(), name='role_permissions'),
]
