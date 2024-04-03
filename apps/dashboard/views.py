from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from apps.account.models import CurrencyWallet
from .models import Ticket, TicketAnswer
from .permission import IsOwnerOrAdmin
from .serializers import CurrencyWalletSerializer, IrWalletSerializer, TicketListSerializer, TicketDetailSerializer, \
    TicketAnswerSerializer, AdminChangeTicketStatusSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model


User = get_user_model()


class IrWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = User.objects.filter(email=request.user.email).first()
        serializer = IrWalletSerializer(wallets)
        return Response(serializer.data, status.HTTP_200_OK)


class CurrencyWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = CurrencyWallet.objects.filter(user=request.user)
        serializer = CurrencyWalletSerializer(wallets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketListForAdminApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        tickets = Ticket.objects.all().order_by('-created_at')
        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def current_ticket(self, uuid):
        ticket = Ticket.objects.filter(uuid__iexact=uuid).first()
        if ticket:
            return ticket
        else:
            raise Http404()

    def get(self, request, uuid):
        serializer = TicketDetailSerializer(self.current_ticket(uuid))
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, uuid):
        serializer = TicketAnswerSerializer(data=request.data)
        if serializer.is_valid():
            admin_answer = serializer.data.get('answer')
            answer = TicketAnswer.objects.create(ticket=self.current_ticket(uuid), answer=admin_answer)
            answer.save()
            return Response({'status': 'success'}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid):
        ticket = self.current_ticket(uuid)
        serializer = AdminChangeTicketStatusSerializer(ticket, data=request.data)
        if serializer.is_valid():
            change_status = serializer.validated_data.get('status')
            ticket.status = change_status
            serializer.save()
            return Response({'status': 'success'}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TicketListForOwnerApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketDetailApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketDetailSerializer
    lookup_field = 'uuid'


class TicketAddApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketDetailSerializer(data=request.data)
        if serializer.is_valid():
            Ticket.objects.create(user=request.user, title=serializer.validated_data['title'], description=serializer.validated_data['description'], status='pending')
            return Response({'statsu': 'success'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)