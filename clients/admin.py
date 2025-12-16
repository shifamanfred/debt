from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'national_id', 'email', 'phone', 'employment_status', 'is_active', 'enrollment_date']
    list_filter = ['employment_status', 'marital_status', 'is_active', 'is_verified']
    search_fields = ['first_name', 'last_name', 'national_id', 'email', 'phone']
    readonly_fields = ['enrollment_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 
                      'gender', 'national_id')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'alternative_phone', 'address', 'city', 'postal_code')
        }),
        ('Employment Information', {
            'fields': ('employment_status', 'employer_name', 'employer_phone', 'employer_address', 
                      'monthly_income')
        }),
        ('Personal Details', {
            'fields': ('marital_status', 'number_of_dependents')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 
                      'emergency_contact_relationship')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified', 'enrollment_date')
        }),
    )

