# Generated by Django 5.0.3 on 2024-04-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0039_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='c4f8d9b8', editable=False, max_length=8),
        ),
    ]