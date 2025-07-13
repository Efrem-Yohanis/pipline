from django.db import models
from datetime import timedelta, date

class MembershipPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    duration_days = models.PositiveIntegerField(default=30)  # Duration in days
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.duration_days} days)"

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # New field
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # New: active/inactive
    is_vip = models.BooleanField(default=False)    # New: VIP status
    membership_expiry = models.DateField(null=True, blank=True)  # New: expiry date
    last_visit = models.DateField(null=True, blank=True)  # New field
    check_in_count = models.IntegerField(default=0)  # New field
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True)  # Updated field
    address = models.CharField(max_length=255, blank=True, null=True)  # New
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)  # New
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)  # New
    medical_history = models.TextField(blank=True, null=True)  # New
    allergies = models.TextField(blank=True, null=True)  # New

    def save(self, *args, **kwargs):
        # Set expiry based on plan if not set
        if self.membership_plan and (not self.membership_expiry or self.join_date == date.today()):
            self.membership_expiry = self.join_date + timedelta(days=self.membership_plan.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)  # Comma-separated
    schedule = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def get_specialization_list(self):
        return self.specialization.split(',') if self.specialization else []

    def __str__(self):
        return self.name

class GymClass(models.Model):
    title = models.CharField(max_length=100)
    schedule = models.DateTimeField()
    trainer = models.ForeignKey(Staff, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=20)  # New: class capacity

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    # Optionally add payment type, status, etc.

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

class CheckIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    # Optionally add location, type, etc.