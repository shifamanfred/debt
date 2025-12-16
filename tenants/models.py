from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """
    Tenant model representing a business/organization in the multi-tenant system.
    Each tenant has its own schema in the database.
    """
    name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    business_email = models.EmailField(unique=True)
    business_phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    # Package/Subscription
    package = models.ForeignKey('packages.Package', on_delete=models.SET_NULL, null=True, blank=True)
    subscription_start_date = models.DateTimeField(auto_now_add=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Business details
    registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Auto-generated fields from TenantMixin
    # schema_name (required, unique)
    
    class Meta:
        db_table = 'tenants'
        
    def __str__(self):
        return self.business_name


class Domain(DomainMixin):
    """
    Domain model for tenant domains.
    Each tenant can have multiple domains.
    """
    pass

