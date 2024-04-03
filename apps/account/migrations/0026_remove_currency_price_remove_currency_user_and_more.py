# Generated by Django 5.0.3 on 2024-04-03 13:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_remove_currencywallet_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='price',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='user',
        ),
        migrations.AddField(
            model_name='currencywallet',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='currencywallet',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
