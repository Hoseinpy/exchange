from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class Ticket(models.Model):
    class StatusChoice(models.TextChoices):
        pending = 'Pending'
        open = 'Open'
        closed = 'Closed'

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=StatusChoice.choices, null=True)
    uuid = models.CharField(max_length=8, default=str(uuid.uuid4())[:8], editable=False)

    def __str__(self):
        return f'{self.title} - {self.user}'


class TicketAnswer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket}'