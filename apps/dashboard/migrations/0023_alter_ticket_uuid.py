# Generated by Django 5.0.3 on 2024-04-03 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='03c109b6', editable=False, max_length=8),
        ),
    ]
