# Generated by Django 5.0.3 on 2024-04-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_remove_currency_price_remove_currency_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencywallet',
            name='code',
            field=models.CharField(max_length=16, null=True),
        ),
    ]