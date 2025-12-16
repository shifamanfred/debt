from rest_framework import serializers
from .models import Package


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'package_type', 'description', 'monthly_price', 
                 'annual_price', 'max_clients', 'max_loans', 'max_employees',
                 'credit_bureau_access', 'sms_notifications', 'email_notifications',
                 'advanced_reporting', 'api_access', 'custom_branding', 'is_active']
        read_only_fields = ['id']
