# Deployment Guide

## For GitHub/Production Deployment

### Security Checklist
- [x] Moved SECRET_KEY to environment variables (.env)
- [x] Created .gitignore to exclude sensitive files
- [x] Created .env.example template
- [x] Configured ALLOWED_HOSTS from environment
- [x] Set DEBUG to False by default
- [x] Email configuration moved to environment variables

### Before Deploying to Production

1. **Generate a new SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Add this to your `.env` file

2. **Set environment variables on deployment platform:**
   - `SECRET_KEY`: Your generated secret key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: Your domain name
   - `EMAIL_HOST_USER`: Your email
   - `EMAIL_HOST_PASSWORD`: Your email app password

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate --noinput
   ```

### ML Model Files
The following files are required but not tracked in Git (due to .gitignore):
- `inte_des/interior_model.pkl`
- `inte_des/room_encoder.pkl`
- `inte_des/material_encoder.pkl`
- `inte_des/light_encoder.pkl`

To generate these files locally:
```bash
python train_model.py
```

Then upload them to your production server or include them in your deployment.

### Deployment Platforms
- **Heroku**: Set config vars for all `.env` variables
- **Railway/Render**: Add environment variables in settings
- **AWS/DigitalOcean**: Create `.env` file or use Docker

### Quick Start for Development
```bash
# Copy example env file
cp .env.example .env

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```
