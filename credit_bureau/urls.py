from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditScoreViewSet, BlacklistViewSet, LoanHistoryViewSet

router = DefaultRouter()
router.register(r'credit-scores', CreditScoreViewSet)
router.register(r'blacklist', BlacklistViewSet)
router.register(r'loan-history', LoanHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
