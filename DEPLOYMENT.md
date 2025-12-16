# Deployment Guide

This guide covers deploying the Microlenders Management System to production.

## Pre-Deployment Checklist

- [ ] PostgreSQL database configured and secured
- [ ] Environment variables configured
- [ ] Secret key changed from default
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Static files configured
- [ ] Media files storage configured
- [ ] SSL certificate obtained
- [ ] Backup strategy in place
- [ ] Monitoring configured

## Production Settings

### Environment Variables

Create a `.env` file with production values:

```env
SECRET_KEY=your-production-secret-key-very-long-and-random
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=microlenders_production
DB_USER=microlenders_prod_user
DB_PASSWORD=strong-production-password
DB_HOST=your-db-host
DB_PORT=5432

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# For production file storage (optional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### Update Settings for Production

Edit `microlenders_system/settings.py`:

```python
# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## Deployment Options

### Option 1: Traditional Server (Ubuntu)

#### 1. Server Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install Python and dependencies
sudo apt-get install python3-pip python3-venv python3-dev
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install nginx
sudo apt-get install supervisor
```

#### 2. Application Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash microlenders
sudo su - microlenders

# Clone repository
git clone <repository-url> /home/microlenders/app
cd /home/microlenders/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Database Setup

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE microlenders_production;
CREATE USER microlenders_prod WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE microlenders_production TO microlenders_prod;
ALTER USER microlenders_prod CREATEDB;
\q
```

#### 4. Run Migrations

```bash
cd /home/microlenders/app
source venv/bin/activate
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
python manage.py create_packages
python manage.py collectstatic --noinput
```

#### 5. Configure Gunicorn

Create `/home/microlenders/app/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

errorlog = "/home/microlenders/logs/gunicorn-error.log"
accesslog = "/home/microlenders/logs/gunicorn-access.log"
loglevel = "info"
```

#### 6. Configure Supervisor

Create `/etc/supervisor/conf.d/microlenders.conf`:

```ini
[program:microlenders]
command=/home/microlenders/app/venv/bin/gunicorn microlenders_system.wsgi:application -c /home/microlenders/app/gunicorn_config.py
directory=/home/microlenders/app
user=microlenders
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/microlenders/logs/supervisor.log
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start microlenders
```

#### 7. Configure Nginx

Create `/etc/nginx/sites-available/microlenders`:

```nginx
upstream microlenders_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 100M;

    location /static/ {
        alias /home/microlenders/app/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /home/microlenders/app/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://microlenders_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/microlenders /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "microlenders_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=microlenders_db
      - POSTGRES_USER=microlenders_user
      - POSTGRES_PASSWORD=your_password
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn microlenders_system.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DB_NAME=microlenders_db
      - DB_USER=microlenders_user
      - DB_PASSWORD=your_password
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### 3. Deploy with Docker

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate_schemas --shared
docker-compose exec web python manage.py migrate_schemas
docker-compose exec web python manage.py create_packages
docker-compose exec web python manage.py createsuperuser
```

### Option 3: Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate_schemas --shared
heroku run python manage.py migrate_schemas
heroku run python manage.py create_packages
```

#### AWS Elastic Beanstalk

1. Install EB CLI
2. Create `.ebextensions/django.config`
3. Deploy: `eb init` and `eb create`

#### Google Cloud Platform

1. Use Cloud SQL for PostgreSQL
2. Deploy on App Engine or Cloud Run
3. Configure Cloud Storage for media files

## Post-Deployment

### 1. Create Superuser

```bash
python manage.py createsuperuser
```

### 2. Set up Monitoring

- Configure application monitoring (e.g., Sentry)
- Set up database monitoring
- Configure server monitoring
- Set up log aggregation

### 3. Configure Backups

```bash
# Database backup script
#!/bin/bash
BACKUP_DIR=/home/microlenders/backups
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U microlenders_prod microlenders_production > $BACKUP_DIR/db_$DATE.sql
find $BACKUP_DIR -type f -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /home/microlenders/scripts/backup.sh
```

### 4. Performance Optimization

- Enable database connection pooling
- Configure caching (Redis/Memcached)
- Optimize database queries
- Use CDN for static files
- Enable gzip compression

### 5. Security Hardening

- Configure firewall (ufw/iptables)
- Disable root SSH login
- Use SSH keys instead of passwords
- Regular security updates
- Configure fail2ban
- Regular security audits

## Maintenance

### Update Application

```bash
cd /home/microlenders/app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate_schemas
python manage.py collectstatic --noinput
sudo supervisorctl restart microlenders
```

### Database Maintenance

```bash
# Vacuum database
python manage.py dbshell
VACUUM ANALYZE;

# Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Monitor Logs

```bash
# Application logs
tail -f /home/microlenders/logs/gunicorn-error.log

# Nginx logs
tail -f /var/log/nginx/error.log

# PostgreSQL logs
tail -f /var/log/postgresql/postgresql-14-main.log
```

## Scaling

### Horizontal Scaling

- Use load balancer (Nginx/HAProxy)
- Deploy multiple application servers
- Use shared database
- Use centralized file storage (S3)
- Use centralized cache (Redis)

### Database Scaling

- Read replicas for read-heavy workloads
- Connection pooling (PgBouncer)
- Database sharding (for extreme scale)
- Regular query optimization

## Troubleshooting

### Application won't start
- Check logs: `sudo supervisorctl tail -f microlenders`
- Verify database connection
- Check environment variables

### Static files not loading
- Run: `python manage.py collectstatic`
- Check Nginx configuration
- Verify file permissions

### Database connection issues
- Check PostgreSQL is running
- Verify credentials
- Check firewall rules
- Test connection: `psql -h host -U user -d database`

### Performance issues
- Check database slow query log
- Monitor server resources
- Review application logs
- Check for N+1 queries

## Support and Monitoring

### Set up Alerts

- Database down
- Application errors
- High CPU/Memory usage
- Disk space low
- SSL certificate expiration

### Regular Tasks

- [ ] Weekly: Review error logs
- [ ] Weekly: Check backup integrity
- [ ] Monthly: Security updates
- [ ] Monthly: Database optimization
- [ ] Quarterly: Security audit
- [ ] Yearly: SSL certificate renewal (if not auto-renewed)

## Disaster Recovery

1. **Have a backup strategy**
2. **Test restore procedures regularly**
3. **Document recovery steps**
4. **Keep off-site backups**
5. **Have a communication plan**

For questions or issues, contact the development team.
