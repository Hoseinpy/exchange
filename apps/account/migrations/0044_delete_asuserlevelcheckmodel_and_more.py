# Generated by Django 5.0.3 on 2024-04-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0043_asuserlevelcheckmodel_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AsUserLevelCheckModel',
        ),
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='21e43715-0', editable=False, max_length=10),
        ),
    ]