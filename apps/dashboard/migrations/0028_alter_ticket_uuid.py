# Generated by Django 5.0.3 on 2024-04-06 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='4f439e94', editable=False, max_length=8),
        ),
    ]
