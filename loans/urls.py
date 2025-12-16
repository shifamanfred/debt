from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoanProductViewSet, LoanApplicationViewSet, LoanViewSet,
    RepaymentViewSet, RepaymentScheduleViewSet
)

router = DefaultRouter()
router.register(r'loan-products', LoanProductViewSet)
router.register(r'loan-applications', LoanApplicationViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'repayments', RepaymentViewSet)
router.register(r'repayment-schedules', RepaymentScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
