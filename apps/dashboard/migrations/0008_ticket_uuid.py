# Generated by Django 5.0.3 on 2024-03-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_ticketanswer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='4d4a747b', editable=False, max_length=8),
        ),
    ]
