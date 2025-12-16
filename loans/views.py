from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import LoanProduct, LoanApplication, Loan, Repayment, RepaymentSchedule
from .serializers import (
    LoanProductSerializer, LoanApplicationSerializer, LoanSerializer,
    RepaymentSerializer, RepaymentScheduleSerializer
)
from clients.models import Client
import uuid


class LoanProductViewSet(viewsets.ModelViewSet):
    queryset = LoanProduct.objects.filter(is_active=True)
    serializer_class = LoanProductSerializer
    permission_classes = [IsAuthenticated]


class LoanApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter applications based on user role."""
        user = self.request.user
        if user.is_client:
            # Clients see only their applications
            try:
                client = Client.objects.get(user=user)
                return LoanApplication.objects.filter(client=client)
            except Client.DoesNotExist:
                return LoanApplication.objects.none()
        else:
            # Admins and employees see all applications
            return LoanApplication.objects.all()
    
    def perform_create(self, serializer):
        """Auto-generate application number."""
        application_number = f"APP-{uuid.uuid4().hex[:8].upper()}"
        serializer.save(application_number=application_number)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a loan application."""
        application = self.get_object()
        
        if application.status != 'PENDING':
            return Response(
                {'error': 'Only pending applications can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'APPROVED'
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.review_notes = request.data.get('review_notes', '')
        application.save()
        
        return Response({'message': 'Application approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a loan application."""
        application = self.get_object()
        
        if application.status != 'PENDING':
            return Response(
                {'error': 'Only pending applications can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'REJECTED'
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.review_notes = request.data.get('review_notes', '')
        application.save()
        
        return Response({'message': 'Application rejected'})


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter loans based on user role."""
        user = self.request.user
        if user.is_client:
            # Clients see only their loans
            try:
                client = Client.objects.get(user=user)
                return Loan.objects.filter(client=client)
            except Client.DoesNotExist:
                return Loan.objects.none()
        else:
            # Admins and employees see all loans
            return Loan.objects.all()
    
    def perform_create(self, serializer):
        """Auto-generate loan number."""
        loan_number = f"LOAN-{uuid.uuid4().hex[:8].upper()}"
        serializer.save(loan_number=loan_number)
    
    @action(detail=True, methods=['post'])
    def disburse(self, request, pk=None):
        """Disburse a loan."""
        loan = self.get_object()
        
        if loan.status != 'APPROVED':
            return Response(
                {'error': 'Only approved loans can be disbursed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        disbursed_amount = request.data.get('disbursed_amount')
        if not disbursed_amount:
            return Response(
                {'error': 'Disbursed amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        loan.status = 'DISBURSED'
        loan.disbursed_amount = disbursed_amount
        loan.disbursement_date = timezone.now().date()
        loan.disbursed_by = request.user
        loan.save()
        
        return Response({'message': 'Loan disbursed successfully'})


class RepaymentViewSet(viewsets.ModelViewSet):
    queryset = Repayment.objects.all()
    serializer_class = RepaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Auto-generate receipt number."""
        receipt_number = f"RCP-{uuid.uuid4().hex[:8].upper()}"
        serializer.save(
            receipt_number=receipt_number,
            recorded_by=self.request.user
        )


class RepaymentScheduleViewSet(viewsets.ModelViewSet):
    queryset = RepaymentSchedule.objects.all()
    serializer_class = RepaymentScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter schedules based on user role."""
        user = self.request.user
        if user.is_client:
            # Clients see only their loan schedules
            try:
                client = Client.objects.get(user=user)
                return RepaymentSchedule.objects.filter(loan__client=client)
            except Client.DoesNotExist:
                return RepaymentSchedule.objects.none()
        else:
            # Admins and employees see all schedules
            return RepaymentSchedule.objects.all()

