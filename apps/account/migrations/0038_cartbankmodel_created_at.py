# Generated by Django 5.0.3 on 2024-04-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0037_cartbankmodel_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartbankmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
