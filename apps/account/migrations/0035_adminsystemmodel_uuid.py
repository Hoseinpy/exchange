# Generated by Django 5.0.3 on 2024-04-06 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_alter_adminsystemmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminsystemmodel',
            name='uuid',
            field=models.CharField(default='82ec318d-c', editable=False, max_length=10),
        ),
    ]