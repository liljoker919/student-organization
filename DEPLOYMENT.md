# AWS Lightsail Deployment Setup

This repository includes automated deployment to AWS Lightsail via GitHub Actions. When code is pushed to the `main` branch, it automatically deploys to your Lightsail instance.

## Required GitHub Secrets

To enable automatic deployment, you need to configure the following secrets in your GitHub repository settings:

### Navigation: Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `LIGHTSAIL_HOST` | Public IP address or domain of your Lightsail instance | `192.168.1.100` or `myapp.example.com` |
| `LIGHTSAIL_USERNAME` | SSH username for your Lightsail instance | `ubuntu` (for Ubuntu) or `ec2-user` (for Amazon Linux) |
| `LIGHTSAIL_SSH_KEY` | Private SSH key for connecting to Lightsail | Contents of your `.pem` or private key file |
| `LIGHTSAIL_PORT` | SSH port (optional, defaults to 22) | `22` |

## Lightsail Instance Prerequisites

Your AWS Lightsail instance should have the following setup before the first deployment:

### 1. Project Directory Structure
```bash
/home/[username]/student-organization/
```

### 2. Git Repository
```bash
cd /home/[username]/
git clone https://github.com/liljoker919/student-organization.git
cd student-organization
```

### 3. Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Environment Variables (Production)
Create a `.env` file or set environment variables:
```bash
export DEBUG=False
export SECRET_KEY="your-production-secret-key-here"
export ALLOWED_HOSTS="your-domain.com,your-ip-address"
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Gunicorn Systemd Service

Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=Gunicorn instance to serve student-organization
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=[your-username]
Group=www-data
WorkingDirectory=/home/[your-username]/student-organization
Environment="PATH=/home/[your-username]/student-organization/venv/bin"
ExecStart=/home/[your-username]/student-organization/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          student_organization.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 7. Web Server (Nginx - Optional)
If using Nginx as reverse proxy, configure it to serve static files and proxy to Gunicorn.

## Deployment Process

The GitHub Actions workflow performs these steps automatically:

1. **Code Update**: Pulls latest changes from `main` branch
2. **Environment**: Activates Python virtual environment  
3. **Dependencies**: Installs/updates Python packages
4. **Database**: Runs Django migrations
5. **Static Files**: Collects static assets
6. **Service Restart**: Restarts Gunicorn systemd service
7. **Health Check**: Verifies service is running

## Troubleshooting

### Deployment Fails
1. Check GitHub Actions logs for specific error messages
2. Verify all required secrets are correctly configured
3. Ensure Lightsail instance meets prerequisites
4. Test SSH connection manually: `ssh -i key.pem username@host`

### Service Issues
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# View logs
sudo journalctl -u gunicorn

# Restart manually
sudo systemctl restart gunicorn
```

### Permission Issues
Ensure the SSH user has appropriate permissions:
```bash
# For systemctl commands
sudo usermod -aG sudo username

# For project directory
chown -R username:username /home/username/student-organization
```

## Security Notes

- Use a strong, unique SECRET_KEY for production
- Keep DEBUG=False in production
- Restrict ALLOWED_HOSTS to your domain/IP
- Use environment variables for sensitive configuration
- Regularly rotate SSH keys
- Keep your Lightsail instance updated with security patches