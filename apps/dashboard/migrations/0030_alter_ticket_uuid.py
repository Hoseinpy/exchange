# Generated by Django 5.0.3 on 2024-04-06 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='c9e1946c', editable=False, max_length=8),
        ),
    ]
