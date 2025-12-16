from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from .models import Client
from .serializers import ClientSerializer, ClientEnrollmentSerializer
from users.models import User


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter clients based on user role."""
        user = self.request.user
        if user.is_client:
            # Clients can only see their own profile
            return Client.objects.filter(user=user)
        else:
            # Admins and employees can see all clients
            return Client.objects.all()
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def enroll(self, request):
        """
        Client self-enrollment endpoint (free of charge).
        Allows clients to create their account and profile.
        """
        serializer = ClientEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    data = serializer.validated_data
                    
                    # Create user account
                    user = User.objects.create(
                        username=data['username'],
                        email=data['email'],
                        role='CLIENT',
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        phone=data['phone']
                    )
                    user.set_password(data['password'])
                    user.save()
                    
                    # Create client profile
                    client = Client.objects.create(
                        user=user,
                        first_name=data['first_name'],
                        middle_name=data.get('middle_name', ''),
                        last_name=data['last_name'],
                        date_of_birth=data['date_of_birth'],
                        gender=data['gender'],
                        national_id=data['national_id'],
                        email=data['email'],
                        phone=data['phone'],
                        alternative_phone=data.get('alternative_phone', ''),
                        address=data['address'],
                        city=data['city'],
                        postal_code=data.get('postal_code', ''),
                        employment_status=data['employment_status'],
                        employer_name=data.get('employer_name', ''),
                        employer_phone=data.get('employer_phone', ''),
                        employer_address=data.get('employer_address', ''),
                        monthly_income=data.get('monthly_income'),
                        marital_status=data['marital_status'],
                        number_of_dependents=data.get('number_of_dependents', 0),
                        emergency_contact_name=data.get('emergency_contact_name', ''),
                        emergency_contact_phone=data.get('emergency_contact_phone', ''),
                        emergency_contact_relationship=data.get('emergency_contact_relationship', '')
                    )
                    
                    return Response({
                        'message': 'Client enrolled successfully',
                        'client_id': client.id,
                        'username': user.username
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        View client profile (free of charge).
        Clients can view their own profile.
        """
        client = self.get_object()
        
        # Check permission
        if request.user.is_client and client.user != request.user:
            return Response(
                {'error': 'You can only view your own profile'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(client)
        return Response(serializer.data)

