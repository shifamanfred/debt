from django.db import models


class Package(models.Model):
    """
    Package/Subscription plans for businesses to choose from.
    """
    PACKAGE_TYPES = [
        ('STARTER', 'Starter'),
        ('PROFESSIONAL', 'Professional'),
        ('ENTERPRISE', 'Enterprise'),
        ('CUSTOM', 'Custom'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES, default='STARTER')
    description = models.TextField()
    
    # Pricing
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    annual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Limits and features
    max_clients = models.IntegerField(help_text="Maximum number of clients allowed")
    max_loans = models.IntegerField(help_text="Maximum number of active loans")
    max_employees = models.IntegerField(help_text="Maximum number of employees")
    
    # Features
    credit_bureau_access = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    advanced_reporting = models.BooleanField(default=False)
    api_access = models.BooleanField(default=False)
    custom_branding = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'packages'
        ordering = ['monthly_price']
        
    def __str__(self):
        return f"{self.name} - ${self.monthly_price}/month"

