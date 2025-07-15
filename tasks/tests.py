from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import authenticate
from io import StringIO

from users.models import CustomUser
from classes.models import StudentClass
from tasks.models import Task, Notification


class PopulateTestDataCommandTest(TestCase):
    """Test the populate_test_data management command"""

    def test_populate_test_data_command(self):
        """Test that the command creates the expected data"""
        # Capture command output
        out = StringIO()
        
        # Run the command with a small number of users
        call_command('populate_test_data', '--users', '2', stdout=out)
        
        # Verify data was created
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertTrue(StudentClass.objects.count() >= 6)  # 3-5 classes per user
        self.assertTrue(Task.objects.count() >= 20)  # 10-20 tasks per user
        self.assertTrue(Notification.objects.count() >= 0)  # 0-3 notifications per task
        
        # Verify user credentials work
        user = CustomUser.objects.first()
        authenticated_user = authenticate(
            username=user.username, 
            password='testpass123'
        )
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, user)
        
        # Verify relationships
        user_classes = StudentClass.objects.filter(user=user)
        user_tasks = Task.objects.filter(user=user)
        
        # Each task should belong to one of the user's classes
        for task in user_tasks:
            self.assertEqual(task.user, user)
            self.assertIn(task.student_class, user_classes)
        
        # Check command output contains expected information
        output = out.getvalue()
        self.assertIn('TEST DATA GENERATION COMPLETE', output)
        self.assertIn('testpass123', output)
        self.assertIn('testuser1', output)

    def test_populate_test_data_clear_option(self):
        """Test that the --clear option removes existing data"""
        # Create initial data
        call_command('populate_test_data', '--users', '1')
        initial_user_count = CustomUser.objects.count()
        
        # Clear and create new data
        call_command('populate_test_data', '--clear', '--users', '1')
        
        # Should still have 1 user (the new one)
        self.assertEqual(CustomUser.objects.count(), 1)
        
        # Verify we can still authenticate
        user = CustomUser.objects.first()
        authenticated_user = authenticate(
            username=user.username,
            password='testpass123'
        )
        self.assertIsNotNone(authenticated_user)
