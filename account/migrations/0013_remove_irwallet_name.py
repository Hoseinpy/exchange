# Generated by Django 5.0.3 on 2024-03-23 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_customuser_ir_wallet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irwallet',
            name='name',
        ),
    ]
