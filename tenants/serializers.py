from rest_framework import serializers
from .models import Tenant, Domain


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'schema_name', 'name', 'business_name', 'business_email', 
                 'business_phone', 'address', 'package', 'is_active', 'created_at']
        read_only_fields = ['id', 'schema_name', 'created_at']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'domain', 'tenant', 'is_primary']


class BusinessRegistrationSerializer(serializers.Serializer):
    """Serializer for business registration."""
    business_name = serializers.CharField(max_length=200)
    business_email = serializers.EmailField()
    business_phone = serializers.CharField(max_length=20)
    address = serializers.CharField()
    package_id = serializers.IntegerField()
    admin_username = serializers.CharField(max_length=150)
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)
    domain = serializers.CharField(max_length=100)
