# Generated by Django 5.0.3 on 2024-03-29 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='55253f40', editable=False, max_length=8),
        ),
    ]
