# Generated by Django 5.0.3 on 2024-04-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='76f71f34', editable=False, max_length=8),
        ),
    ]
