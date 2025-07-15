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
4. Run the server: `python manage.py runserver`

## Email Configuration (Development)

This project uses MailHog for email testing during development. MailHog captures emails sent by the application and provides a web interface to view them.

### MailHog Setup

1. Download MailHog from [releases page](https://github.com/mailhog/MailHog/releases)
2. Extract the executable to your project directory or a location in your PATH
3. Run the executable:
   - **Windows**: `./MailHog.exe`
   - **macOS/Linux**: `./MailHog`

MailHog will start and listen on:
- **SMTP Server**: localhost:1025 (for sending emails)
- **Web Interface**: localhost:8025 (for viewing emails)

### Testing Email Configuration

1. Start MailHog by running the executable (`./MailHog.exe` on Windows or `./MailHog` on macOS/Linux)
2. Send a test email using the management command:
   ```bash
   python manage.py send_test_email
   ```
3. View the email in MailHog's web interface: http://localhost:8025

### Email Configuration Details

- **Development**: Emails are sent to MailHog (localhost:1025)
- **Production**: Configure using environment variables:
  - `EMAIL_HOST` - SMTP server hostname
  - `EMAIL_PORT` - SMTP server port (default: 587)
  - `EMAIL_USE_TLS` - Enable TLS (default: True)
  - `EMAIL_USE_SSL` - Enable SSL (default: False)
  - `EMAIL_HOST_USER` - SMTP username
  - `EMAIL_HOST_PASSWORD` - SMTP password
  - `DEFAULT_FROM_EMAIL` - Default sender email address