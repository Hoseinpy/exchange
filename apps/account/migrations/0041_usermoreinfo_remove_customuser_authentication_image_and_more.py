# Generated by Django 5.0.3 on 2024-04-06 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0040_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMoreInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('father_name', models.CharField(max_length=30, null=True)),
                ('national_code', models.CharField(max_length=10, null=True)),
                ('phone_number', models.CharField(max_length=14, null=True)),
                ('authentication_image', models.ImageField(null=True, upload_to='user_info/')),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='authentication_image',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='father_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='national_code',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='2bd625b8-2', editable=False, max_length=10),
        ),
        migrations.AddField(
            model_name='customuser',
            name='more_info',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.usermoreinfo'),
        ),
    ]
