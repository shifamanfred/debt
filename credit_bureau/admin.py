from django.contrib import admin
from .models import CreditScore, Blacklist, LoanHistory


@admin.register(CreditScore)
class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ['client', 'score', 'risk_level', 'total_loans', 'active_loans', 
                   'defaulted_loans', 'last_calculated']
    list_filter = ['risk_level']
    search_fields = ['client__first_name', 'client__last_name', 'client__national_id']
    readonly_fields = ['last_calculated', 'created_at', 'updated_at']


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ['client', 'reason', 'status', 'amount_owed', 'blacklisted_date', 
                   'expiry_date']
    list_filter = ['reason', 'status', 'blacklisted_date']
    search_fields = ['client__first_name', 'client__last_name', 'client__national_id']
    readonly_fields = ['blacklisted_date', 'created_at', 'updated_at']


@admin.register(LoanHistory)
class LoanHistoryAdmin(admin.ModelAdmin):
    list_display = ['client', 'loan', 'loan_amount', 'completion_status', 'days_overdue', 
                   'final_payment_date']
    list_filter = ['completion_status']
    search_fields = ['client__first_name', 'client__last_name', 'loan__loan_number']
    readonly_fields = ['created_at', 'updated_at']

