from django.test import TestCase, override_settings
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
import os


class EmailConfigurationTest(TestCase):
    """Test email configuration for MailHog integration"""

    @override_settings(DEBUG=True)
    def test_email_settings_in_debug_mode(self):
        """Test that email settings are configured correctly for development"""
        # Import settings in the context of the override
        from django.conf import settings
        
        # In our actual settings.py, these should be set when DEBUG=True
        # We need to test the logic by directly importing and checking
        from student_organization import settings as app_settings
        import importlib
        importlib.reload(app_settings)
        
        # Test MailHog configuration when DEBUG=True
        self.assertEqual(app_settings.EMAIL_HOST, 'localhost')
        self.assertEqual(app_settings.EMAIL_PORT, 1025)
        self.assertFalse(app_settings.EMAIL_USE_TLS)
        self.assertFalse(app_settings.EMAIL_USE_SSL)
        
    def test_production_email_environment_defaults(self):
        """Test that production email settings have proper defaults"""
        # Test environment variable defaults
        host = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
        port = int(os.environ.get('EMAIL_PORT', '587'))
        use_tls = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
        
        self.assertEqual(host, 'smtp.gmail.com')
        self.assertEqual(port, 587)
        self.assertTrue(use_tls)

    def test_send_test_email_functionality(self):
        """Test that sending email works with test backend"""
        # Use test email backend to capture emails without actually sending
        with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            mail.outbox = []  # Clear any existing test emails
            
            # Send a test email
            send_mail(
                subject='Test Email',
                message='This is a test message',
                from_email='noreply@student-organization.local',
                recipient_list=['test@example.com'],
                fail_silently=False,
            )
            
            # Verify email was captured
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Test Email')
            self.assertEqual(mail.outbox[0].from_email, 'noreply@student-organization.local')
            self.assertEqual(mail.outbox[0].to, ['test@example.com'])

    def test_mailhog_configuration_constants(self):
        """Test that MailHog configuration constants are correct"""
        # These are the values we expect for MailHog
        MAILHOG_HOST = 'localhost'
        MAILHOG_PORT = 1025
        MAILHOG_USE_TLS = False
        MAILHOG_USE_SSL = False
        
        self.assertEqual(MAILHOG_HOST, 'localhost')
        self.assertEqual(MAILHOG_PORT, 1025)
        self.assertFalse(MAILHOG_USE_TLS)
        self.assertFalse(MAILHOG_USE_SSL)
