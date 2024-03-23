# Generated by Django 5.0.3 on 2024-03-23 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_customuser_user_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='ir_wallet',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_level',
            field=models.CharField(choices=[('0', 'level0'), ('1', 'level1'), ('2', 'level2'), ('3', 'level3')], default=0, max_length=4, null=True),
        ),
        migrations.CreateModel(
            name='IrWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=0, max_digits=30)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
