import os
import django
from django.test import TestCase, override_settings
from django.conf import settings


class AllowedHostsConfigurationTest(TestCase):
    """Test ALLOWED_HOSTS configuration behavior"""
    
    def test_allowed_hosts_default_includes_routine101_and_ip(self):
        """Test that default ALLOWED_HOSTS includes 'routine101' and '18.188.144.39'"""
        # This test verifies the fallback behavior when no ALLOWED_HOSTS env var is set
        with self.settings():
            # Temporarily remove ALLOWED_HOSTS env var if it exists
            original_value = os.environ.get('ALLOWED_HOSTS')
            if 'ALLOWED_HOSTS' in os.environ:
                del os.environ['ALLOWED_HOSTS']
            
            try:
                # Re-import settings to get the updated configuration
                from importlib import reload
                from django.conf import settings as django_settings
                from student_organization import settings as app_settings
                reload(app_settings)
                
                # Check that the fallback hosts are present
                expected_hosts = ['routine101', '18.188.144.39', '3.149.217.170']
                actual_hosts = app_settings.ALLOWED_HOSTS
                
                self.assertEqual(actual_hosts, expected_hosts, 
                    f"Expected ALLOWED_HOSTS to be {expected_hosts}, but got {actual_hosts}")
                
            finally:
                # Restore original environment variable if it existed
                if original_value is not None:
                    os.environ['ALLOWED_HOSTS'] = original_value
    
    def test_allowed_hosts_environment_override(self):
        """Test that ALLOWED_HOSTS environment variable overrides default values"""
        test_hosts = "example.com,127.0.0.1,localhost"
        
        with self.settings():
            # Set the environment variable
            os.environ['ALLOWED_HOSTS'] = test_hosts
            
            try:
                # Re-import settings to get the updated configuration
                from importlib import reload
                from student_organization import settings as app_settings
                reload(app_settings)
                
                expected_hosts = test_hosts.split(',')
                actual_hosts = app_settings.ALLOWED_HOSTS
                
                self.assertEqual(actual_hosts, expected_hosts,
                    f"Expected ALLOWED_HOSTS to be {expected_hosts}, but got {actual_hosts}")
                
            finally:
                # Clean up
                if 'ALLOWED_HOSTS' in os.environ:
                    del os.environ['ALLOWED_HOSTS']
    
    def test_allowed_hosts_empty_environment_variable(self):
        """Test behavior when ALLOWED_HOSTS environment variable is empty"""
        with self.settings():
            # Set empty environment variable
            os.environ['ALLOWED_HOSTS'] = ''
            
            try:
                # Re-import settings to get the updated configuration
                from importlib import reload
                from student_organization import settings as app_settings
                reload(app_settings)
                
                # With empty env var, should fall back to default hosts
                expected_hosts = ['routine101', '18.188.144.39', '3.149.217.170']
                actual_hosts = app_settings.ALLOWED_HOSTS
                
                self.assertEqual(actual_hosts, expected_hosts,
                    f"Expected ALLOWED_HOSTS to be {expected_hosts}, but got {actual_hosts}")
                
            finally:
                # Clean up
                if 'ALLOWED_HOSTS' in os.environ:
                    del os.environ['ALLOWED_HOSTS']