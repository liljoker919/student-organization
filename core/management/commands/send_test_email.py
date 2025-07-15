from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Send a test email to verify MailHog integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default='test@example.com',
            help='Email address to send test email to (default: test@example.com)'
        )
        parser.add_argument(
            '--subject',
            type=str,
            default='Test Email from Student Organization App',
            help='Subject line for the test email'
        )

    def handle(self, *args, **options):
        to_email = options['to']
        subject = options['subject']
        
        message = f"""
This is a test email from the Student Organization Django application.

Email Configuration:
- Backend: {settings.EMAIL_BACKEND}
- Host: {settings.EMAIL_HOST}
- Port: {settings.EMAIL_PORT}
- Use TLS: {settings.EMAIL_USE_TLS}
- Use SSL: {settings.EMAIL_USE_SSL}
- From Email: {settings.DEFAULT_FROM_EMAIL}

If you're seeing this email in MailHog, the email configuration is working correctly!

Time sent: {self.get_current_time()}
        """.strip()

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully sent test email to {to_email}\n'
                    f'Subject: {subject}\n'
                    f'From: {settings.DEFAULT_FROM_EMAIL}\n'
                    f'Check MailHog at http://localhost:8025 to view the email.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Failed to send test email: {str(e)}\n'
                    f'Make sure MailHog is running on localhost:1025'
                )
            )

    def get_current_time(self):
        from django.utils import timezone
        return timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')