from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta, date
import random

from users.models import CustomUser
from classes.models import StudentClass
from tasks.models import Task, Notification


class Command(BaseCommand):
    help = 'Generate comprehensive test data for all models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=8,
            help='Number of users to create (default: 8)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Notification.objects.all().delete()
            Task.objects.all().delete()
            StudentClass.objects.all().delete()
            CustomUser.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        num_users = options['users']
        
        self.stdout.write(self.style.SUCCESS(f'Generating test data for {num_users} users...'))
        
        # Generate users
        users = self.create_users(num_users)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
        
        # Generate classes for each user
        all_classes = []
        for user in users:
            classes = self.create_classes_for_user(user)
            all_classes.extend(classes)
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_classes)} classes'))
        
        # Generate tasks for each user and their classes
        all_tasks = []
        for user in users:
            user_classes = StudentClass.objects.filter(user=user)
            tasks = self.create_tasks_for_user(user, user_classes)
            all_tasks.extend(tasks)
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_tasks)} tasks'))
        
        # Generate notifications for tasks
        all_notifications = []
        for task in all_tasks:
            notifications = self.create_notifications_for_task(task)
            all_notifications.extend(notifications)
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_notifications)} notifications'))
        
        # Print summary
        self.print_summary(users)

    def create_users(self, num_users):
        """Create test users with predictable credentials"""
        users = []
        roles = ['student', 'parent']
        
        # Create a mix of students and parents
        for i in range(1, num_users + 1):
            role = roles[i % 2]  # Alternate between student and parent
            username = f'testuser{i}'
            email = f'testuser{i}@example.com'
            password = 'testpass123'  # Common password for all test users
            
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name=f'Test{i}',
                last_name='User',
                role=role,
                is_active=True
            )
            users.append(user)
            
        return users

    def create_classes_for_user(self, user):
        """Create 3-5 classes for each user"""
        classes = []
        num_classes = random.randint(3, 5)
        
        # Sample class data
        class_names = [
            'Mathematics', 'English Literature', 'Physics', 'Chemistry', 'Biology',
            'History', 'Geography', 'Computer Science', 'Art', 'Music',
            'Physical Education', 'Spanish', 'French', 'Psychology', 'Economics'
        ]
        
        teachers = [
            'Dr. Smith', 'Prof. Johnson', 'Ms. Williams', 'Mr. Brown', 'Dr. Davis',
            'Prof. Miller', 'Ms. Wilson', 'Mr. Moore', 'Dr. Taylor', 'Prof. Anderson'
        ]
        
        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
        ]
        
        icons = [
            'https://cdn-icons-png.flaticon.com/512/3002/3002543.png',  # Math
            'https://cdn-icons-png.flaticon.com/512/2940/2940685.png',  # Book
            'https://cdn-icons-png.flaticon.com/512/3003/3003984.png',  # Science
            'https://cdn-icons-png.flaticon.com/512/2942/2942813.png',  # Chemistry
            'https://cdn-icons-png.flaticon.com/512/3003/3003467.png',  # Biology
        ]
        
        selected_classes = random.sample(class_names, num_classes)
        
        for i, class_name in enumerate(selected_classes):
            # Generate class times (random hour between 8 AM and 4 PM)
            start_hour = random.randint(8, 15)
            start_time = timezone.now().replace(
                hour=start_hour, 
                minute=random.choice([0, 30]), 
                second=0, 
                microsecond=0
            )
            end_time = start_time + timedelta(hours=1, minutes=30)
            
            student_class = StudentClass.objects.create(
                user=user,
                name=class_name,
                color=random.choice(colors),
                icon=random.choice(icons),
                teacher=random.choice(teachers),
                start_time=start_time,
                end_time=end_time
            )
            classes.append(student_class)
            
        return classes

    def create_tasks_for_user(self, user, user_classes):
        """Create 10-20 tasks for each user across their classes"""
        tasks = []
        num_tasks = random.randint(10, 20)
        
        task_types = ['assignment', 'test']
        priorities = ['high', 'medium', 'low']
        statuses = ['todo', 'in_progress', 'complete']
        
        # Sample task names
        assignment_names = [
            'Chapter 1 Review', 'Essay Assignment', 'Problem Set 3', 'Lab Report',
            'Research Paper', 'Group Project', 'Book Report', 'Case Study Analysis',
            'Presentation Prep', 'Homework Assignment', 'Practice Problems',
            'Creative Writing', 'Data Analysis', 'Literature Review'
        ]
        
        test_names = [
            'Midterm Exam', 'Quiz 1', 'Final Exam', 'Pop Quiz', 'Unit Test',
            'Chapter Test', 'Vocabulary Quiz', 'Math Test', 'Science Quiz',
            'History Exam', 'Language Test', 'Comprehension Test'
        ]
        
        for i in range(num_tasks):
            task_type = random.choice(task_types)
            
            if task_type == 'assignment':
                task_name = random.choice(assignment_names)
                description = f"Complete the {task_name.lower()} as outlined in the course syllabus. Submit before the due date."
            else:
                task_name = random.choice(test_names)
                description = f"Prepare for the {task_name.lower()}. Review all covered materials and practice problems."
            
            # Generate due dates (some past, some future)
            days_offset = random.randint(-30, 60)  # 30 days ago to 60 days in future
            due_date = date.today() + timedelta(days=days_offset)
            
            # Status logic: completed tasks are usually past due, incomplete are usually future
            if days_offset < -7:  # Past due by more than a week
                status = random.choices(statuses, weights=[0.1, 0.2, 0.7])[0]  # Mostly complete
            elif days_offset < 0:  # Past due but recent
                status = random.choices(statuses, weights=[0.3, 0.4, 0.3])[0]  # Mixed
            else:  # Future due dates
                status = random.choices(statuses, weights=[0.6, 0.3, 0.1])[0]  # Mostly todo/in_progress
            
            task = Task.objects.create(
                user=user,
                task_type=task_type,
                name=f"{task_name} - {random.choice(list(user_classes)).name}",
                student_class=random.choice(list(user_classes)),
                description=description,
                due_date=due_date,
                priority=random.choice(priorities),
                status=status
            )
            tasks.append(task)
            
        return tasks

    def create_notifications_for_task(self, task):
        """Create 0-3 notifications for each task"""
        notifications = []
        num_notifications = random.randint(0, 3)
        
        notification_messages = [
            f"Reminder: {task.name} is due soon!",
            f"Don't forget about {task.name}",
            f"Task {task.name} has been updated",
            f"Your {task.name} is overdue",
            f"Great job completing {task.name}!",
            f"New comment on {task.name}",
            f"Assignment {task.name} requires your attention"
        ]
        
        for i in range(num_notifications):
            # Generate notification times (recent past)
            days_ago = random.randint(0, 14)
            hours_ago = random.randint(0, 23)
            created_at = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
            
            notification = Notification.objects.create(
                user=task.user,
                task=task,
                message=random.choice(notification_messages),
                is_read=random.choice([True, False]),
                created_at=created_at
            )
            notifications.append(notification)
            
        return notifications

    def print_summary(self, users):
        """Print a summary of created data and user credentials"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('TEST DATA GENERATION COMPLETE'))
        self.stdout.write(self.style.SUCCESS('='*50))
        
        self.stdout.write(f'\nTotal Users: {len(users)}')
        self.stdout.write(f'Total Classes: {StudentClass.objects.count()}')
        self.stdout.write(f'Total Tasks: {Task.objects.count()}')
        self.stdout.write(f'Total Notifications: {Notification.objects.count()}')
        
        self.stdout.write(self.style.SUCCESS('\n' + '-'*50))
        self.stdout.write(self.style.SUCCESS('TEST USER CREDENTIALS'))
        self.stdout.write(self.style.SUCCESS('-'*50))
        self.stdout.write('Common password for all users: testpass123')
        self.stdout.write('\nUsernames and details:')
        
        for user in users:
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'    Email: {user.email}')
            self.stdout.write(f'    Name: {user.first_name} {user.last_name}')
            self.stdout.write(f'    Role: {user.role}')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('Use these credentials to log into the application for testing.'))
        self.stdout.write(self.style.SUCCESS('\nCommand completed successfully!'))