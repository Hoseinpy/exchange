# Generated by Django 5.0.3 on 2024-04-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0048_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='c6e9b0d6-4', editable=False, max_length=10),
        ),
    ]
