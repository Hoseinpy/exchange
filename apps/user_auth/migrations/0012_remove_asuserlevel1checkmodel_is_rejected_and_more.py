# Generated by Django 5.0.3 on 2024-04-10 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0011_asuserlevel1checkmodel_is_rejected_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asuserlevel1checkmodel',
            name='is_rejected',
        ),
        migrations.AlterField(
            model_name='asuserlevel1checkmodel',
            name='uuid',
            field=models.CharField(default='bc65b93a-3', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='asuserlevel2checkmodel',
            name='uuid',
            field=models.CharField(default='74d512b8-6', editable=False, max_length=10),
        ),
    ]