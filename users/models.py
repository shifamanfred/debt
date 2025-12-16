from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model for the system.
    Supports different user roles: superadmin, tenant_admin, employee, client
    """
    USER_ROLES = [
        ('SUPERADMIN', 'Super Admin'),
        ('TENANT_ADMIN', 'Tenant Admin'),
        ('EMPLOYEE', 'Employee'),
        ('CLIENT', 'Client'),
    ]
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='CLIENT')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    # Profile
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    national_id = models.CharField(max_length=50, blank=True)
    
    # Employee-specific fields
    employee_number = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_superadmin(self):
        return self.role == 'SUPERADMIN'
    
    @property
    def is_tenant_admin(self):
        return self.role == 'TENANT_ADMIN'
    
    @property
    def is_employee(self):
        return self.role == 'EMPLOYEE'
    
    @property
    def is_client(self):
        return self.role == 'CLIENT'

