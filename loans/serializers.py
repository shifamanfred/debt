from rest_framework import serializers
from .models import LoanProduct, LoanApplication, Loan, Repayment, RepaymentSchedule


class LoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = ['id', 'name', 'description', 'min_amount', 'max_amount', 
                 'interest_rate', 'min_term_months', 'max_term_months', 
                 'processing_fee_percentage', 'late_payment_fee', 
                 'min_credit_score', 'requires_collateral', 'requires_guarantor', 
                 'is_active']
        read_only_fields = ['id']


class LoanApplicationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    loan_product_name = serializers.CharField(source='loan_product.name', read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = ['id', 'application_number', 'client', 'client_name', 
                 'loan_product', 'loan_product_name', 'requested_amount', 
                 'requested_term_months', 'purpose', 'status', 'reviewed_by', 
                 'review_notes', 'reviewed_at', 'created_at']
        read_only_fields = ['id', 'application_number', 'reviewed_at', 'created_at']


class LoanSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    loan_product_name = serializers.CharField(source='loan_product.name', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'loan_number', 'application', 'client', 'client_name',
                 'loan_product', 'loan_product_name', 'principal_amount', 
                 'interest_rate', 'term_months', 'monthly_payment', 'total_interest',
                 'total_amount', 'outstanding_balance', 'status', 'disbursed_amount',
                 'disbursement_date', 'approval_date', 'first_payment_date', 
                 'maturity_date']
        read_only_fields = ['id', 'loan_number', 'approval_date']


class RepaymentSerializer(serializers.ModelSerializer):
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)
    
    class Meta:
        model = Repayment
        fields = ['id', 'receipt_number', 'loan', 'loan_number', 'amount', 
                 'payment_date', 'payment_method', 'principal_paid', 'interest_paid',
                 'late_fee_paid', 'status', 'transaction_reference', 'notes', 
                 'recorded_by']
        read_only_fields = ['id', 'receipt_number']


class RepaymentScheduleSerializer(serializers.ModelSerializer):
    loan_number = serializers.CharField(source='loan.loan_number', read_only=True)
    
    class Meta:
        model = RepaymentSchedule
        fields = ['id', 'loan', 'loan_number', 'installment_number', 'due_date',
                 'principal_due', 'interest_due', 'total_due', 'principal_paid',
                 'interest_paid', 'total_paid', 'outstanding_balance', 'status']
        read_only_fields = ['id']
