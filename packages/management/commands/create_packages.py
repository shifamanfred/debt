from django.core.management.base import BaseCommand
from packages.models import Package


class Command(BaseCommand):
    help = 'Create default subscription packages'

    def handle(self, *args, **options):
        packages_data = [
            {
                'name': 'Starter',
                'package_type': 'STARTER',
                'description': 'Perfect for small microlending businesses just getting started',
                'monthly_price': 49.99,
                'annual_price': 499.99,
                'max_clients': 100,
                'max_loans': 50,
                'max_employees': 3,
                'credit_bureau_access': False,
                'sms_notifications': False,
                'email_notifications': True,
                'advanced_reporting': False,
                'api_access': False,
                'custom_branding': False,
            },
            {
                'name': 'Professional',
                'package_type': 'PROFESSIONAL',
                'description': 'Full-featured package for growing microlending businesses',
                'monthly_price': 149.99,
                'annual_price': 1499.99,
                'max_clients': 500,
                'max_loans': 250,
                'max_employees': 10,
                'credit_bureau_access': True,
                'sms_notifications': True,
                'email_notifications': True,
                'advanced_reporting': True,
                'api_access': True,
                'custom_branding': False,
            },
            {
                'name': 'Enterprise',
                'package_type': 'ENTERPRISE',
                'description': 'Unlimited features for large microlending organizations',
                'monthly_price': 499.99,
                'annual_price': 4999.99,
                'max_clients': 10000,
                'max_loans': 5000,
                'max_employees': 50,
                'credit_bureau_access': True,
                'sms_notifications': True,
                'email_notifications': True,
                'advanced_reporting': True,
                'api_access': True,
                'custom_branding': True,
            },
        ]

        for package_data in packages_data:
            package, created = Package.objects.get_or_create(
                name=package_data['name'],
                defaults=package_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created package: {package.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Package already exists: {package.name}')
                )

        self.stdout.write(self.style.SUCCESS('Package setup complete!'))
