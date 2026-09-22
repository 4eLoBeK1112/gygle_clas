from django.conf import settings
from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import migrations, models


def connect_existing_users(apps, schema_editor):
    CustomUser = apps.get_model('user', 'User')
    AuthUser = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Student = apps.get_model('user', 'Student')
    Teacher = apps.get_model('user', 'Teacher')
    Admin = apps.get_model('user', 'Admin')

    user_map = {}
    for custom_user in CustomUser.objects.all():
        auth_user = AuthUser.objects.filter(username=custom_user.username).first()
        if auth_user is None:
            auth_user = AuthUser(
                username=custom_user.username,
                email=custom_user.email,
                first_name=custom_user.first_name,
                last_name=custom_user.last_name,
                is_active=custom_user.is_active,
                is_staff=custom_user.is_staff,
            )
            try:
                identify_hasher(custom_user.password)
                auth_user.password = custom_user.password
            except Exception:
                auth_user.password = make_password(custom_user.password)
            auth_user.save()
        user_map[custom_user.pk] = auth_user.pk

    for model in (Student, Teacher, Admin):
        for role in model.objects.all():
            role.user_id = user_map[role.user_id]
            role.save(update_fields=['user'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(connect_existing_users, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='admin',
            name='user',
            field=models.OneToOneField(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]