# Generated by Django 5.0.3 on 2024-04-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0046_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='15ac3fb0-4', editable=False, max_length=10),
        ),
    ]
