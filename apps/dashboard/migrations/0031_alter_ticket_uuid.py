# Generated by Django 5.0.3 on 2024-04-06 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='348c3a73', editable=False, max_length=8),
        ),
    ]
