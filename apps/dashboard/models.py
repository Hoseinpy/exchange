from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


STATUS_CHOICES = {
    'new': 'New',
    'closed': 'Closed'
}


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, null=True)

    def __str__(self):
        return self.title


class TicketAnswer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket