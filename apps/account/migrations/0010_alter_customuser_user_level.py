# Generated by Django 5.0.3 on 2024-03-22 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_customuser_is_authentication_customuser_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_level',
            field=models.CharField(choices=[('1', 'level1'), ('2', 'level2'), ('3', 'level3')], default=0, max_length=3, null=True),
        ),
    ]
