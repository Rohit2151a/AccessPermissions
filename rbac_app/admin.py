from django.contrib import admin
from .models import User, Role, AuditLog, Permission

admin.site.register(User)
admin.site.register(Role)
admin.site.register(AuditLog)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource')
