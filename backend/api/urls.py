from rest_framework import routers
from .views import (
    MemberViewSet, StaffViewSet, GymClassViewSet,
    PaymentViewSet, InventoryItemViewSet, CheckInViewSet,
    RecentActivityView, MemberDetailView, MembershipPlanViewSet
)
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'classes', GymClassViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'inventory', InventoryItemViewSet)
router.register(r'checkins', CheckInViewSet)
router.register(r'plans', MembershipPlanViewSet)

urlpatterns = [
    path('members/<int:pk>/', MemberDetailView.as_view()),
    path('activity/', RecentActivityView.as_view()),
    path('', include(router.urls)),
]