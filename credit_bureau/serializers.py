from rest_framework import serializers
from .models import CreditScore, Blacklist, LoanHistory


class CreditScoreSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    
    class Meta:
        model = CreditScore
        fields = ['id', 'client', 'client_name', 'score', 'risk_level', 
                 'total_loans', 'active_loans', 'completed_loans', 'defaulted_loans',
                 'on_time_payments', 'late_payments', 'missed_payments',
                 'total_borrowed', 'total_repaid', 'current_outstanding',
                 'last_calculated']
        read_only_fields = ['id', 'last_calculated']


class BlacklistSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    
    class Meta:
        model = Blacklist
        fields = ['id', 'client', 'client_name', 'reason', 'description', 
                 'related_loan', 'amount_owed', 'status', 'blacklisted_date',
                 'expiry_date', 'cleared_date', 'blacklisted_by', 'cleared_by', 
                 'notes']
        read_only_fields = ['id', 'blacklisted_date']


class LoanHistorySerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)
    
    class Meta:
        model = LoanHistory
        fields = ['id', 'client', 'client_name', 'loan', 'loan_number', 
                 'loan_amount', 'loan_term', 'interest_rate', 'completion_status',
                 'final_payment_date', 'days_overdue', 'total_paid', 'notes']
        read_only_fields = ['id']
