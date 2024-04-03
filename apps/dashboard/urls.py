from django.urls import path
from .views import (IrWalletView, TicketListForAdminApiView,
                    TicketListForOwnerApiView, TicketAddApiView, TicketDetailApiView,
                    TicketAnswerAPIView, CurrencyWalletView)


urlpatterns = [
    path('real-wallet/', IrWalletView.as_view(), name='real-wallet-api'),
    path('currency-wallet/',CurrencyWalletView.as_view(), name='currency-wallet-api'),
    path('tickets/', TicketListForAdminApiView.as_view(), name='Ticket-list-for-admin-api'),
    path('user-ticket/', TicketListForOwnerApiView.as_view(), name='Ticket-list-for-owner-api'),
    path('user-ticket/add', TicketAddApiView.as_view(), name='Ticket-add-api'),
    path('user-ticket/<str:uuid>', TicketDetailApiView.as_view(), name='Ticket-detail-for-user-api'),
    path('tickets/<str:uuid>', TicketAnswerAPIView.as_view(), name='Ticket-detail-for-admin-api'),
]
