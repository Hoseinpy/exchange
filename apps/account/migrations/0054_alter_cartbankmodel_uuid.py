# Generated by Django 5.0.3 on 2024-04-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0053_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='5bc75e91-f', editable=False, max_length=10),
        ),
    ]