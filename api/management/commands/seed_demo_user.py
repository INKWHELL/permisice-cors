from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creates the demo account (joe / testpass123) used in the 5.3 evidence."

    def handle(self, *args, **options):
        if not User.objects.filter(username="joe").exists():
            User.objects.create_user(
                username="joe", email="joe@example.com", password="testpass123"
            )
            self.stdout.write(self.style.SUCCESS("Created demo user: joe / testpass123"))
        else:
            self.stdout.write("Demo user 'joe' already exists.")
