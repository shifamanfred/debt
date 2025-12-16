from django.contrib import admin
from .models import LoanProduct, LoanApplication, Loan, Repayment, RepaymentSchedule


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'interest_rate', 'min_amount', 'max_amount', 'min_term_months', 
                   'max_term_months', 'is_active']
    list_filter = ['is_active', 'requires_collateral', 'requires_guarantor']
    search_fields = ['name', 'description']


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'client', 'loan_product', 'requested_amount', 
                   'status', 'created_at']
    list_filter = ['status', 'loan_product', 'created_at']
    search_fields = ['application_number', 'client__first_name', 'client__last_name', 
                    'client__national_id']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_number', 'client', 'principal_amount', 'interest_rate', 'status', 
                   'disbursement_date']
    list_filter = ['status', 'loan_product', 'disbursement_date']
    search_fields = ['loan_number', 'client__first_name', 'client__last_name', 
                    'client__national_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'loan', 'amount', 'payment_date', 'payment_method', 'status']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['receipt_number', 'loan__loan_number', 'transaction_reference']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RepaymentSchedule)
class RepaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ['loan', 'installment_number', 'due_date', 'total_due', 'total_paid', 'status']
    list_filter = ['status', 'due_date']
    search_fields = ['loan__loan_number']
    readonly_fields = ['created_at', 'updated_at']

