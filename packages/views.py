from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Package
from .serializers import PackageSerializer


class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing available packages.
    Read-only as packages are managed by superadmin.
    """
    queryset = Package.objects.filter(is_active=True)
    serializer_class = PackageSerializer
    permission_classes = [AllowAny]  # Anyone can view packages

