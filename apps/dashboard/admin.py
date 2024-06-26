from django.contrib import admin
from .models import Ticket, TicketAnswer


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'description', 'status', 'uuid', 'created_at']



@admin.register(TicketAnswer)
class TicketAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ticket', 'answer', 'created_at']