from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Create a Google Social Application for development (fixes DoesNotExist error)'

    def handle(self, *args, **options):
        """
        Create a Google SocialApp with placeholder credentials for development.
        This fixes the DoesNotExist error when accessing /accounts/login/
        """
        
        # Check if Google SocialApp already exists
        if SocialApp.objects.filter(provider='google').exists():
            self.stdout.write(
                self.style.WARNING('Google SocialApp already exists. Skipping creation.')
            )
            return

        # Create Google SocialApp with placeholder credentials
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth (Development)',
            client_id='placeholder-client-id',
            secret='placeholder-client-secret'
        )

        # Associate with the default site
        site = Site.objects.get(id=1)
        google_app.sites.add(site)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created Google SocialApp: {google_app.name}\n'
                f'Associated with site: {site}\n'
                f'Note: Replace placeholder credentials with real Google OAuth credentials '
                f'in production.'
            )
        )