# Generated by Django 5.0.3 on 2024-03-25 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
