# Generated by Django 5.0.3 on 2024-04-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0052_alter_cartbankmodel_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartbankmodel',
            name='uuid',
            field=models.CharField(default='cabf9a51-2', editable=False, max_length=10),
        ),
    ]
