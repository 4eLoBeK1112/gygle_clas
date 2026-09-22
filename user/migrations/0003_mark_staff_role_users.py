from django.conf import settings
from django.db import migrations


def mark_staff_role_users(apps, schema_editor):
    AuthUser = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Student = apps.get_model('user', 'Student')
    Teacher = apps.get_model('user', 'Teacher')
    Admin = apps.get_model('user', 'Admin')

    staff_user_ids = set(
        Teacher.objects.values_list('user_id', flat=True)
    ) | set(
        Admin.objects.values_list('user_id', flat=True)
    )
    AuthUser.objects.filter(id__in=staff_user_ids).update(is_staff=True)


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0002_connect_roles_to_auth_users'),
    ]

    operations = [
        migrations.RunPython(mark_staff_role_users, migrations.RunPython.noop),
    ]