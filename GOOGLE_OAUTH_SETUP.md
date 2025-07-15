# Google OAuth Setup

This document explains how to configure Google social login for the Student Organization application.

## Development Setup (Quick Fix)

For development and testing purposes, a Google SocialApp with placeholder credentials has been automatically created. This allows the login page to render without errors.

To ensure the Google SocialApp is set up correctly, run:

```bash
python manage.py setup_google_oauth
```

This command:
- Creates a Google SocialApp with placeholder credentials if none exists
- Associates it with the default site
- Fixes the `DoesNotExist` error on `/accounts/login/`

## Production Setup

For production use, you need to:

1. **Create Google OAuth 2.0 credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create or select a project
   - Enable the Google+ API
   - Go to "Credentials" and create "OAuth 2.0 Client IDs"
   - Add your domain to "Authorized redirect URIs" (e.g., `https://yourdomain.com/accounts/google/login/callback/`)

2. **Update the SocialApp in Django Admin:**
   - Go to `/admin/socialaccount/socialapp/`
   - Edit the existing Google SocialApp
   - Replace `placeholder-client-id` with your real Client ID
   - Replace `placeholder-client-secret` with your real Client Secret
   - Save the changes

3. **Update ALLOWED_HOSTS and Site configuration:**
   - Add your production domain to `ALLOWED_HOSTS` in settings.py
   - Update the Site object in Django Admin to match your domain

## Troubleshooting

### DoesNotExist Error
If you encounter `allauth.socialaccount.models.SocialApp.DoesNotExist` error:
- Run `python manage.py setup_google_oauth`
- Verify a Site object exists with the correct `SITE_ID`

### Login Page Not Loading
- Check that `allauth.socialaccount.providers.google` is in `INSTALLED_APPS`
- Verify `{% load socialaccount %}` is in your login template
- Ensure the SocialApp is associated with the correct Site

### OAuth Flow Errors
- Verify your Google OAuth credentials are correct
- Check that redirect URIs match in Google Console and your application
- Ensure your domain is properly configured