# Generated by Django 5.0.3 on 2024-04-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='8452e8b2', editable=False, max_length=8),
        ),
    ]