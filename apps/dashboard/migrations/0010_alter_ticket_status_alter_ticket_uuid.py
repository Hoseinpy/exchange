# Generated by Django 5.0.3 on 2024-03-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_ticketanswer_user_alter_ticket_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('open', 'Open'), ('closed', 'Closed')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(default='44cf9182', editable=False, max_length=8),
        ),
    ]