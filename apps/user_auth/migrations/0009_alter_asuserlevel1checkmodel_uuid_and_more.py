# Generated by Django 5.0.3 on 2024-04-07 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0008_alter_asuserlevel1checkmodel_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asuserlevel1checkmodel',
            name='uuid',
            field=models.CharField(default='b9f7ac37-c', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='asuserlevel2checkmodel',
            name='uuid',
            field=models.CharField(default='06ec405f-e', editable=False, max_length=10),
        ),
    ]
