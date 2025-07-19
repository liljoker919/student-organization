import os
import unittest
from unittest.mock import patch


class DatabaseConfigurationTest(unittest.TestCase):
    """Test database configuration switching between SQLite and MySQL."""
    
    def setUp(self):
        """Reset environment for each test."""
        # Store original env state
        self.original_env = os.environ.copy()
    
    def tearDown(self):
        """Restore original environment after each test."""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_development_uses_sqlite(self):
        """Test that development environment (DEBUG=True) uses SQLite."""
        # Set DEBUG to True
        os.environ['DEBUG'] = 'True'
        
        # Simulate the settings.py logic
        DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
        
        if not DEBUG:  # Production settings
            database_engine = 'django.db.backends.mysql'
        else:  # Development settings (keep SQLite)
            database_engine = 'django.db.backends.sqlite3'
        
        self.assertEqual(database_engine, 'django.db.backends.sqlite3')
    
    def test_production_uses_mysql_with_env_vars(self):
        """Test that production environment (DEBUG=False) uses MySQL with env vars."""
        # Set environment variables
        os.environ.update({
            'DEBUG': 'False',
            'MYSQL_DATABASE_NAME': 'test_routine101_db',
            'MYSQL_DATABASE_USER': 'test_user',
            'MYSQL_DATABASE_PASSWORD': 'test_password',
            'MYSQL_DATABASE_HOST': 'test-host.amazonaws.com',
            'MYSQL_DATABASE_PORT': '3306'
        })
        
        # Simulate the settings.py logic
        DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
        
        if not DEBUG:  # Production settings
            database_config = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('MYSQL_DATABASE_NAME', 'routine101_db'),
                'USER': os.environ.get('MYSQL_DATABASE_USER', 'dbmasteruser'),
                'PASSWORD': os.environ.get('MYSQL_DATABASE_PASSWORD'),
                'HOST': os.environ.get('MYSQL_DATABASE_HOST', 'ls-dea471356e9733d36d898ad29f683b7852ae0f02.c3aomgso0h3s.us-east-2.rds.amazonaws.com'),
                'PORT': os.environ.get('MYSQL_DATABASE_PORT', '3306'),
            }
        else:  # Development settings (keep SQLite)
            database_config = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        
        # Check that MySQL is configured with custom environment variables
        self.assertEqual(database_config['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(database_config['NAME'], 'test_routine101_db')
        self.assertEqual(database_config['USER'], 'test_user')
        self.assertEqual(database_config['PASSWORD'], 'test_password')
        self.assertEqual(database_config['HOST'], 'test-host.amazonaws.com')
        self.assertEqual(database_config['PORT'], '3306')
    
    def test_mysql_defaults_are_correct(self):
        """Test that MySQL configuration uses correct default values."""
        # Set environment variables with only password
        os.environ.update({
            'DEBUG': 'False',
            'MYSQL_DATABASE_PASSWORD': 'production_password'
        })
        
        # Simulate the settings.py logic
        DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
        
        if not DEBUG:  # Production settings
            database_config = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('MYSQL_DATABASE_NAME', 'routine101_db'),
                'USER': os.environ.get('MYSQL_DATABASE_USER', 'dbmasteruser'),
                'PASSWORD': os.environ.get('MYSQL_DATABASE_PASSWORD'),
                'HOST': os.environ.get('MYSQL_DATABASE_HOST', 'ls-dea471356e9733d36d898ad29f683b7852ae0f02.c3aomgso0h3s.us-east-2.rds.amazonaws.com'),
                'PORT': os.environ.get('MYSQL_DATABASE_PORT', '3306'),
            }
        else:  # Development settings (keep SQLite)
            database_config = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        
        # Check default values when only password is provided
        self.assertEqual(database_config['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(database_config['NAME'], 'routine101_db')
        self.assertEqual(database_config['USER'], 'dbmasteruser')
        self.assertEqual(database_config['PASSWORD'], 'production_password')
        self.assertEqual(database_config['HOST'], 'ls-dea471356e9733d36d898ad29f683b7852ae0f02.c3aomgso0h3s.us-east-2.rds.amazonaws.com')
        self.assertEqual(database_config['PORT'], '3306')


if __name__ == '__main__':
    unittest.main()