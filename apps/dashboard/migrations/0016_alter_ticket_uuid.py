# Generated by Django 5.0.3 on 2024-03-29 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='613475cb', editable=False, max_length=8),
        ),
    ]
