# Deployment Guide

This guide provides detailed instructions for deploying the Family Tree application to various platforms.

## Prerequisites

Before deploying, ensure you have:
- A GitHub account and git installed
- Python 3.9 or higher
- A database service (PostgreSQL recommended)
- A hosting platform account (Railway, Heroku, or PythonAnywhere)

## 1. Railway Deployment (Recommended)

Railway is the easiest and most cost-effective option for deploying Flask applications.

### Step 1: Prepare Your Code
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Select your repository

### Step 3: Configure Environment
In your Railway dashboard:
1. Go to the Variables tab
2. Add the following environment variables:
```
FLASK_ENV=production
SECRET_KEY=<generate-a-strong-secret-key>
```

### Step 4: Add PostgreSQL Database
1. Click "New" → "Database"
2. Select "PostgreSQL"
3. Railway will automatically set `DATABASE_URL`

### Step 5: Deploy
1. Push changes to GitHub
2. Railway automatically deploys on push
3. Check deployment status in Railway dashboard

### Troubleshooting Railway

**Issue**: Database connection error
- Check DATABASE_URL environment variable
- Verify database is running

**Issue**: Import errors
- Ensure all packages in requirements.txt are installed
- Check Python version compatibility

## 2. Heroku Deployment

### Step 1: Prepare Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Install Heroku CLI
```bash
npm install -g heroku
heroku login
```

### Step 3: Create Heroku App
```bash
heroku create your-app-name
```

### Step 4: Set Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set DATABASE_URL=<postgres-url>
```

### Step 5: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### Step 6: Deploy
```bash
git push heroku main
```

### View Logs
```bash
heroku logs --tail
```

### Troubleshooting Heroku

**Scale your app**:
```bash
heroku ps:scale web=1
```

**Run migrations**:
```bash
heroku run flask db upgrade
```

**Check config**:
```bash
heroku config
```

## 3. PythonAnywhere Deployment

### Step 1: Create Account
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Go to Web section

### Step 2: Add Web App
1. Click "Add a new web app"
2. Choose Python 3.9+
3. Choose Flask framework

### Step 3: Upload Code
Using Git:
```bash
ssh pythonanywherenote@your-domain.pythonanywhere.com
git clone <your-repo-url>
```

Or upload files directly via web interface

### Step 4: Configure Virtual Environment
```bash
cd ~
python3.9 -m venv myenv
source myenv/bin/activate
pip install -r mysite/requirements.txt
```

### Step 5: Update WSGI File
Edit the WSGI configuration file:
```python
import sys
path = '/home/pythonanywherenote/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

### Step 6: Configure Database
Set PostgreSQL connection in environment variables via web interface

### Step 7: Reload
Click "Reload" in Web section

## 4. AWS Elastic Beanstalk Deployment

### Step 1: Install EB CLI
```bash
pip install awseb
eb init
```

### Step 2: Create Environment
```bash
eb create family-tree-env
```

### Step 3: Set Environment Variables
```bash
eb setenv FLASK_ENV=production SECRET_KEY=<your-secret-key>
```

### Step 4: Deploy
```bash
eb deploy
```

### Step 5: Add RDS Database
1. Go to RDS console
2. Create PostgreSQL database
3. Add connection string to environment variables

## 5. DigitalOcean App Platform

### Step 1: Connect GitHub
1. Go to DigitalOcean App Platform
2. Click "Create App"
3. Connect your GitHub account

### Step 2: Configure
1. Select your repository
2. Set environment variables:
   - FLASK_ENV=production
   - SECRET_KEY=<your-secret-key>

### Step 3: Add Database
1. Click "Create Database"
2. Choose PostgreSQL
3. Add to app spec

### Step 4: Deploy
Click "Deploy App"

## Environment Variables Required

All production deployments require these environment variables:

```
# Flask Configuration
FLASK_ENV=production
FLASK_APP=app.py

# Security
SECRET_KEY=<very-long-random-string>

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Optional
DEBUG=False
WORKERS=4
```

### Generate Secure Secret Key

```python
import secrets
print(secrets.token_urlsafe(32))
```

Or in Python:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Database Migration

### Create Database Tables
```bash
# Development
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

### Verify Tables
```bash
# PostgreSQL
psql <database-url>
\dt  # list tables
```

## SSL/HTTPS Setup

### For Heroku
HTTPS is automatically provided

### For Railway
HTTPS is automatically provided

### For Custom Domain
1. Use CloudFlare for free SSL
2. Or Let's Encrypt with certbot

## Performance Optimization

### 1. Database Indexing
Add indexes to frequently queried columns:
```python
# In models/user.py
username = db.Column(db.String(80), unique=True, nullable=False, index=True)
```

### 2. Caching
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### 3. Database Connection Pooling
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

## Monitoring and Logging

### Sentry Integration
```python
import sentry_sdk
sentry_sdk.init("<your-sentry-dsn>")
```

### Application Logs
Monitor logs in your deployment platform's dashboard:
- Railway: View in dashboard
- Heroku: `heroku logs --tail`
- PythonAnywhere: View in console

## Backup and Recovery

### Database Backup

**PostgreSQL**:
```bash
pg_dump <database-url> > backup.sql
```

**Restore**:
```bash
psql <database-url> < backup.sql
```

### File Backup
Keep backups of:
- `requirements.txt`
- `.env` (securely)
- User uploaded photos (if not using cloud storage)

## Custom Domain Setup

### 1. Buy Domain
From: GoDaddy, Namecheap, Google Domains, etc.

### 2. Update DNS Records
Point to your hosting provider:
```
CNAME: www -> <app>.herokuapp.com  # For Heroku
A Record: <IP>                      # For VPS
```

### 3. Configure in App
Update Flask config if needed

## Security Checklist

- [ ] SECRET_KEY is strong and unique
- [ ] FLASK_ENV is set to 'production'
- [ ] Database password is strong
- [ ] HTTPS/SSL is enabled
- [ ] Database backups are automated
- [ ] Logs are monitored
- [ ] User data is encrypted
- [ ] Regular security updates
- [ ] Rate limiting is enabled
- [ ] CORS is properly configured

## Troubleshooting Common Issues

### 502 Bad Gateway
- Check app logs
- Verify database connection
- Check memory/CPU limits

### Database Connection Timeout
- Verify DATABASE_URL
- Check network security groups
- Increase connection pool size

### Static Files Not Loading
- Run `flask collect-static` if applicable
- Check static files path configuration
- Verify CloudFront/CDN setup

### High Memory Usage
- Reduce worker count
- Optimize database queries
- Add caching layer

## Scaling Your Application

### Horizontal Scaling
- Add more dynos (Heroku)
- Add more replicas (Railway)
- Load balancer configuration

### Vertical Scaling
- Increase memory allocation
- Upgrade database tier
- Use faster processors

## Maintenance

### Regular Tasks
- Monitor performance
- Review logs
- Update dependencies monthly
- Backup database regularly
- Test disaster recovery

### Dependency Updates
```bash
pip list --outdated
pip install --upgrade package-name
```

## Support

For deployment-specific issues:
- Railway Support: https://railway.app/support
- Heroku Support: https://www.heroku.com/support
- PythonAnywhere Support: https://help.pythonanywhere.com
