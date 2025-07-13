from api.models import Member, Staff, GymClass, Payment, InventoryItem, CheckIn
from django.utils import timezone
from datetime import timedelta

# Create Members
m1 = Member.objects.create(
    name="John Doe",
    email="john@example.com",
    phone="(555) 123-4567",
    is_active=True,
    is_vip=True,
    membership_expiry=timezone.now().date() + timedelta(days=30),
    last_visit=timezone.now().date() - timedelta(days=1),
    check_in_count=45,
    membership_type="Premium"
)
m2 = Member.objects.create(
    name="Jane Smith",
    email="jane@example.com",
    phone="(555) 987-6543",
    is_active=True,
    is_vip=False,
    membership_expiry=timezone.now().date() + timedelta(days=5),
    last_visit=timezone.now().date() - timedelta(days=2),
    check_in_count=32,
    membership_type="Premium"
)
m3 = Member.objects.create(
    name="Inactive User",
    email="inactive@example.com",
    phone="(555) 000-0000",
    is_active=False,
    is_vip=False,
    membership_expiry=timezone.now().date() - timedelta(days=1),
    last_visit=timezone.now().date() - timedelta(days=10),
    check_in_count=0,
    membership_type="Basic"
)

# Create Staff
s1 = Staff.objects.create(name="Alice Trainer", role="Trainer")
s2 = Staff.objects.create(name="Bob Manager", role="Manager")

# Create Classes
c1 = GymClass.objects.create(title="Yoga", schedule=timezone.now(), trainer=s1, capacity=15)
c2 = GymClass.objects.create(title="HIIT", schedule=timezone.now(), trainer=s1, capacity=12)

# Create Payments
Payment.objects.create(member=m1, amount=50.00)
Payment.objects.create(member=m2, amount=75.00)
Payment.objects.create(member=m1, amount=100.00)

# Create Inventory Items
InventoryItem.objects.create(name="Protein Bar", quantity=100)
InventoryItem.objects.create(name="Water Bottle", quantity=200)

# Create CheckIns
CheckIn.objects.create(member=m1)
CheckIn.objects.create(member=m2)
CheckIn.objects.create(member=m1)

print("Sample data inserted!")