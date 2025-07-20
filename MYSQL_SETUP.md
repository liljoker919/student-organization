# MySQL Database Configuration

This document describes the MySQL database configuration for production deployment.

## Environment Configuration

The application automatically switches between SQLite (development) and MySQL (production) based on the `DEBUG` environment variable.

### Development (DEBUG=True)
- Uses SQLite database (`db.sqlite3`)
- No additional configuration required

### Production (DEBUG=False)
- Uses MySQL database
- Requires the following environment variables:

```bash
# Required
MYSQL_DATABASE_PASSWORD=your_password_here

# Optional (with defaults shown)
MYSQL_DATABASE_NAME=routine101_db
MYSQL_DATABASE_USER=dbmasteruser
MYSQL_DATABASE_HOST=ls-dea471356e9733d36d898ad29f683b7852ae0f02.c3aomgso0h3s.us-east-2.rds.amazonaws.com
MYSQL_DATABASE_PORT=3306
```

## MySQL Client Installation

For production environments, install the MySQL client:

```bash
pip install mysqlclient==2.2.4
```

Or on Ubuntu/Debian systems:
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install mysqlclient==2.2.4
```

## Database Migration

After setting up the MySQL database and configuring environment variables:

```bash
# Set production environment
export DEBUG=False
export MYSQL_DATABASE_PASSWORD=your_actual_password

# Run migrations
python manage.py migrate
```

## Testing Configuration

To verify the database configuration is working:

```bash
# Test development configuration
DEBUG=True python -c "from student_organization.settings import DATABASES; print(DATABASES['default']['ENGINE'])"

# Test production configuration  
DEBUG=False MYSQL_DATABASE_PASSWORD=test python -c "from student_organization.settings import DATABASES; print(DATABASES['default']['ENGINE'])"
```

## Security Notes

- Never commit database passwords to version control
- Use environment variables or secure secret management for credentials
- Ensure the MySQL instance is properly secured and accessible only from authorized sources