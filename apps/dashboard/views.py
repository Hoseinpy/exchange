import uuid
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
from rest_framework.pagination import PageNumberPagination


User = get_user_model()


class IrWalletView(APIView):
    """ user see his ir wallet """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = User.objects.filter(email=request.user.email).first()
        serializer = IrWalletSerializer(wallets)
        return Response(serializer.data, status.HTTP_200_OK)


class CurrencyWalletView(APIView):
    """ user see his currency wallet """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = CurrencyWallet.objects.filter(user=request.user)
        serializer = CurrencyWalletSerializer(wallets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketListForAdminApiView(generics.ListAPIView):
    """ admin see all tickets """
    class PagenationSetting(PageNumberPagination):
        page_size = 10

    permission_classes = [IsAdminUser]
    serializer_class = TicketListSerializer
    queryset = Ticket.objects.all().order_by('-created_at')
    pagination_class = PagenationSetting
    

class TicketDetailForAdminAPIView(APIView):
    
    """ admin see more info from ticket and reply message or can change ticket status"""
    
    permission_classes = [IsAdminUser]

    def current_ticket(self, uuid):
        ticket = Ticket.objects.filter(uuid__iexact=uuid).first()
        if ticket:
            return ticket
        else:
            raise Http404()

    def get(self, request, uuid):
        serializer = TicketDetailSerializer(self.current_ticket(uuid))
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, uuid): # add answer
        serializer = TicketAnswerSerializer(data=request.data)
        if serializer.is_valid():
            admin_answer = serializer.data.get('answer')
            answer = TicketAnswer.objects.create(ticket=self.current_ticket(uuid), answer=admin_answer, user=request.user)
            answer.save()
            return Response({'status': 'success'}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid): # change ticket status
        ticket = self.current_ticket(uuid)
        serializer = AdminChangeTicketStatusSerializer(ticket, data=request.data)
        if serializer.is_valid():
            change_status = serializer.validated_data.get('status')
            ticket.status = change_status
            serializer.save()
            return Response({'status': 'success'}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TicketListForOwnerApiView(APIView):
    """ The owner sees all his tickets """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TicketDetailForUserApiView(APIView):
    """ owner see more info from ticket and reply message"""
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
            user_answer = serializer.data.get('answer')
            answer = TicketAnswer.objects.create(ticket=self.current_ticket(uuid), answer=user_answer, user=request.user)
            answer.save()
            return Response({'status': 'success'}, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TicketAddApiView(APIView):
    """ user can add ticket """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketDetailSerializer(data=request.data)
        if serializer.is_valid():
            Ticket.objects.create(user=request.user, title=serializer.validated_data['title'],
                                   description=serializer.validated_data['description'], status='Pending', uuid=str(uuid.uuid4())[:14])
            
            return Response({'statsu': 'success'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)