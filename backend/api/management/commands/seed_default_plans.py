from django.core.management.base import BaseCommand
from api.models import MembershipPlan

class Command(BaseCommand):
    help = "Seed default membership plans (Basic, Premium, VIP) if missing."

    def handle(self, *args, **kwargs):
        plans = [
            {"name": "Basic", "duration_days": 30, "price": 39, "description": "Gym access, Basic equipment, Locker room"},
            {"name": "Premium", "duration_days": 90, "price": 69, "description": "All Basic features, Group classes, Personal trainer consultation, Nutrition guidance"},
            {"name": "VIP", "duration_days": 365, "price": 99, "description": "All Premium features, Unlimited personal training, Priority booking, Premium amenities"},
        ]
        for plan in plans:
            obj, created = MembershipPlan.objects.get_or_create(name=plan["name"], defaults=plan)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created plan: {obj.name}"))
            else:
                self.stdout.write(f"Plan already exists: {obj.name}")
        self.stdout.write(self.style.SUCCESS("Default plans seeding complete."))
