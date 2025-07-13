from django.shortcuts import render
from rest_framework import viewsets
from .models import Member, Staff, GymClass, Payment, InventoryItem, CheckIn, MembershipPlan
from .serializers import (
    MemberSerializer, StaffSerializer, GymClassSerializer,
    PaymentSerializer, InventoryItemSerializer, CheckInSerializer, MembershipPlanSerializer
)
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework import generics

# Create your views here.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all()
    serializer_class = GymClassSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(schedule__date=date)
        return queryset

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year and month:
            queryset = queryset.filter(date__year=year, date__month=month)
        return queryset

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(check_in_time__date=date)
        return queryset

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer

class RecentActivityView(APIView):
    def get(self, request):
        # Get last 10 check-ins, new members, payments, and classes
        checkins = CheckIn.objects.order_by('-check_in_time')[:3]
        new_members = Member.objects.order_by('-join_date')[:3]
        payments = Payment.objects.order_by('-date')[:2]
        classes = GymClass.objects.order_by('-schedule')[:2]
        activity = []
        for c in checkins:
            activity.append({
                'type': 'check-in',
                'member': c.member.name,
                'time': c.check_in_time.strftime('%Y-%m-%d %H:%M')
            })
        for m in new_members:
            activity.append({
                'type': 'new-member',
                'member': m.name,
                'time': m.join_date.strftime('%Y-%m-%d')
            })
        for p in payments:
            activity.append({
                'type': 'payment',
                'member': p.member.name,
                'time': p.date.strftime('%Y-%m-%d')
            })
        for gc in classes:
            activity.append({
                'type': 'class-booking',
                'member': gc.trainer.name,
                'time': gc.schedule.strftime('%Y-%m-%d %H:%M')
            })
        # Sort by time descending
        activity.sort(key=lambda x: x['time'], reverse=True)
        return Response(activity[:10])

class MemberDetailView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer