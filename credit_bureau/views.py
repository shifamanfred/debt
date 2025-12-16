from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import CreditScore, Blacklist, LoanHistory
from .serializers import CreditScoreSerializer, BlacklistSerializer, LoanHistorySerializer
from clients.models import Client


class CreditScoreViewSet(viewsets.ModelViewSet):
    queryset = CreditScore.objects.all()
    serializer_class = CreditScoreSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter credit scores based on user role."""
        user = self.request.user
        if user.is_client:
            # Clients can only see their own credit score
            try:
                client = Client.objects.get(user=user)
                return CreditScore.objects.filter(client=client)
            except Client.DoesNotExist:
                return CreditScore.objects.none()
        else:
            # Admins and employees can see all credit scores
            return CreditScore.objects.all()
    
    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        """Recalculate credit score."""
        credit_score = self.get_object()
        credit_score.calculate_score()
        serializer = self.get_serializer(credit_score)
        return Response(serializer.data)


class BlacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only admins and employees can view blacklist."""
        user = self.request.user
        if user.is_client:
            return Blacklist.objects.none()
        else:
            return Blacklist.objects.all()
    
    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """Clear a blacklist record."""
        blacklist = self.get_object()
        blacklist.status = 'CLEARED'
        blacklist.cleared_by = request.user
        blacklist.cleared_date = timezone.now().date()
        blacklist.notes = request.data.get('notes', '')
        blacklist.save()
        
        return Response({'message': 'Blacklist record cleared'})


class LoanHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoanHistory.objects.all()
    serializer_class = LoanHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter loan history based on user role."""
        user = self.request.user
        if user.is_client:
            # Clients can only see their own history
            try:
                client = Client.objects.get(user=user)
                return LoanHistory.objects.filter(client=client)
            except Client.DoesNotExist:
                return LoanHistory.objects.none()
        else:
            # Admins and employees can see all history
            return LoanHistory.objects.all()

