from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Client
        fields = ['id', 'user', 'first_name', 'middle_name', 'last_name', 'full_name',
                 'date_of_birth', 'gender', 'national_id', 'email', 'phone', 
                 'alternative_phone', 'address', 'city', 'postal_code',
                 'employment_status', 'employer_name', 'employer_phone', 
                 'employer_address', 'monthly_income', 'marital_status', 
                 'number_of_dependents', 'emergency_contact_name', 
                 'emergency_contact_phone', 'emergency_contact_relationship',
                 'is_active', 'is_verified', 'enrollment_date']
        read_only_fields = ['id', 'enrollment_date']


class ClientEnrollmentSerializer(serializers.Serializer):
    """Serializer for client self-enrollment."""
    # User account details
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    # Personal information
    first_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    national_id = serializers.CharField(max_length=50)
    
    # Contact information
    phone = serializers.CharField(max_length=20)
    alternative_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Employment information
    employment_status = serializers.ChoiceField(choices=Client.EMPLOYMENT_STATUS)
    employer_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    employer_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    employer_address = serializers.CharField(required=False, allow_blank=True)
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    
    # Personal details
    marital_status = serializers.ChoiceField(choices=Client.MARITAL_STATUS)
    number_of_dependents = serializers.IntegerField(default=0)
    
    # Emergency contact
    emergency_contact_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    emergency_contact_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    emergency_contact_relationship = serializers.CharField(max_length=50, required=False, allow_blank=True)
