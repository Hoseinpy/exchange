# Generated by Django 5.0.3 on 2024-04-06 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_alter_asuserlevelcheckmodel_uuid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='asuserlevelcheckmodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='asuserlevelcheckmodel',
            name='uuid',
            field=models.CharField(default='b666c62f-4', editable=False, max_length=10),
        ),
    ]
