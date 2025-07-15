// filepath: README.md
# Student Organization (ADHD Schoolwork Tracker)

A Django web application to help students with ADHD keep track of assignments, tests, and classes.  
## Features
- User roles: Student, Parent
- Class, assignment, and test management
- Reminders and notifications

## Setup
1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. (Optional) Generate test data: `python manage.py populate_test_data`
5. Run the server: `python manage.py runserver`

## Development

### Test Data Generation

For development and testing purposes, you can generate comprehensive test data using the Django management command.

**Prerequisites:** Ensure database migrations have been applied first:
```bash
python manage.py migrate
```

Then generate test data:
```bash
python manage.py populate_test_data
```

**Options:**
- `--users N`: Number of users to create (default: 8)
- `--clear`: Clear existing data before generating new data

**Examples:**
```bash
# Generate default test data (8 users)
python manage.py populate_test_data

# Generate test data for 10 users
python manage.py populate_test_data --users 10

# Clear existing data and create fresh test data
python manage.py populate_test_data --clear --users 5
```

**Test User Credentials:**
All generated test users use the same password: `testpass123`

Users are created with the following pattern:
- Username: `testuser1`, `testuser2`, etc.
- Email: `testuser1@example.com`, `testuser2@example.com`, etc.
- Roles: Alternates between 'parent' and 'student'

**Generated Data:**
- **Users**: Configurable number with predictable credentials
- **Classes**: 3-5 classes per user with realistic names, teachers, and schedules
- **Tasks**: 10-20 tasks per user with various types (assignment/test), priorities, and statuses
- **Notifications**: 0-3 notifications per task with realistic messages

All data includes proper model relationships and timezone-aware dates.