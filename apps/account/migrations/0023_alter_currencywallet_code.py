# Generated by Django 5.0.3 on 2024-04-03 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_currencywallet_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencywallet',
            name='code',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
