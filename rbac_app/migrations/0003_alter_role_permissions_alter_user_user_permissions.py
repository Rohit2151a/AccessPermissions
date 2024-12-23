# Generated by Django 4.2.17 on 2024-12-07 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac_app', '0002_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(related_name='roles', to='rbac_app.permission'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='rbac_app.permission'),
        ),
    ]
