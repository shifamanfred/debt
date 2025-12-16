from django.db import models
from django.conf import settings


class Client(models.Model):
    """
    Client model for loan applicants.
    Clients can self-enroll and view their profiles free of charge.
    """
    EMPLOYMENT_STATUS = [
        ('EMPLOYED', 'Employed'),
        ('SELF_EMPLOYED', 'Self Employed'),
        ('UNEMPLOYED', 'Unemployed'),
        ('STUDENT', 'Student'),
        ('RETIRED', 'Retired'),
    ]
    
    MARITAL_STATUS = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    national_id = models.CharField(max_length=50, unique=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Employment Information
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS)
    employer_name = models.CharField(max_length=200, blank=True)
    employer_phone = models.CharField(max_length=20, blank=True)
    employer_address = models.TextField(blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Personal Information
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS)
    number_of_dependents = models.IntegerField(default=0)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clients'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

