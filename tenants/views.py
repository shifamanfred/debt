from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer, BusinessRegistrationSerializer
from packages.models import Package
from users.models import User


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register_business(self, request):
        """
        Business registration endpoint.
        Allows businesses to register by choosing a package.
        """
        serializer = BusinessRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    data = serializer.validated_data
                    
                    # Get the package
                    package = Package.objects.get(id=data['package_id'])
                    
                    # Create schema name from business name
                    schema_name = data['business_name'].lower().replace(' ', '_')[:63]
                    
                    # Create tenant
                    tenant = Tenant.objects.create(
                        schema_name=schema_name,
                        name=data['business_name'],
                        business_name=data['business_name'],
                        business_email=data['business_email'],
                        business_phone=data['business_phone'],
                        address=data['address'],
                        package=package
                    )
                    
                    # Create domain
                    Domain.objects.create(
                        domain=data['domain'],
                        tenant=tenant,
                        is_primary=True
                    )
                    
                    # Create admin user in tenant's schema
                    # Note: In production, this would switch to the tenant schema
                    admin_user = User.objects.create(
                        username=data['admin_username'],
                        email=data['admin_email'],
                        role='TENANT_ADMIN',
                        is_staff=True
                    )
                    admin_user.set_password(data['admin_password'])
                    admin_user.save()
                    
                    return Response({
                        'message': 'Business registered successfully',
                        'tenant_id': tenant.id,
                        'schema_name': tenant.schema_name,
                        'domain': data['domain']
                    }, status=status.HTTP_201_CREATED)
                    
            except Package.DoesNotExist:
                return Response(
                    {'error': 'Package not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]

