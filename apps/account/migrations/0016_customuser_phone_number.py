# Generated by Django 5.0.3 on 2024-03-25 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_cartbankmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=13, null=True),
        ),
    ]
