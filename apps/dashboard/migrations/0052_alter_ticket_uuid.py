# Generated by Django 5.0.3 on 2024-04-10 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0051_alter_ticket_uuid_alter_ticketanswer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(editable=False, max_length=14),
        ),
    ]