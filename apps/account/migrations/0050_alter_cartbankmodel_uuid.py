# Generated by Django 5.0.3 on 2024-04-06 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0049_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='baf76ec0-d', editable=False, max_length=10),
        ),
    ]
