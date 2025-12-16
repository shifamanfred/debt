# Quick Start Guide

This guide will help you get the microlenders management system up and running quickly.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd debt

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Access PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE microlenders_db;
CREATE USER microlenders_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE microlenders_db TO microlenders_user;
ALTER USER microlenders_user CREATEDB;
\q
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=microlenders_db
DB_USER=microlenders_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run Migrations

```bash
# Migrate shared schemas (tenants, packages, domains)
python manage.py migrate_schemas --shared

# Migrate tenant schemas
python manage.py migrate_schemas
```

### 5. Create Public Tenant (Required for django-tenants)

```bash
python manage.py shell
```

```python
from tenants.models import Tenant, Domain

# Create public tenant
tenant = Tenant(
    schema_name='public',
    name='Public',
    business_name='Public Schemas',
    business_email='admin@localhost',
    business_phone='0000000000',
)
tenant.save()

# Create domain
domain = Domain()
domain.domain = 'localhost'
domain.tenant = tenant
domain.is_primary = True
domain.save()

exit()
```

### 6. Create Default Packages

```bash
python manage.py create_packages
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000/admin/

## Testing the System

### 1. View Available Packages

```bash
curl http://localhost:8000/api/packages/
```

### 2. Register a Business

```bash
curl -X POST http://localhost:8000/api/tenants/register_business/ \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Demo Microfinance",
    "business_email": "demo@micro.com",
    "business_phone": "+1234567890",
    "address": "123 Main St",
    "package_id": 1,
    "admin_username": "demoadmin",
    "admin_email": "admin@micro.com",
    "admin_password": "SecurePass123!",
    "domain": "demo.localhost"
  }'
```

### 3. Enroll a Client

```bash
curl -X POST http://localhost:8000/api/clients/enroll/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "gender": "M",
    "national_id": "ID123456789",
    "phone": "+1234567890",
    "address": "456 Oak St",
    "city": "Springfield",
    "employment_status": "EMPLOYED",
    "employer_name": "ABC Company",
    "monthly_income": "5000.00",
    "marital_status": "SINGLE"
  }'
```

## Common Tasks

### Create a Loan Product

1. Login to admin panel: http://localhost:8000/admin/
2. Go to Loan Products
3. Click "Add Loan Product"
4. Fill in the details and save

### Process a Loan Application

1. Client submits application via API
2. Admin reviews in admin panel or via API
3. Approve/Reject the application
4. If approved, create loan record
5. Disburse the loan
6. Set up repayment schedule

## Troubleshooting

### Issue: Cannot connect to database
**Solution**: Ensure PostgreSQL is running and credentials are correct

```bash
# Check PostgreSQL status
sudo systemctl status postgresql
```

### Issue: Migration errors
**Solution**: Drop and recreate database (development only!)

```bash
sudo -u postgres psql
DROP DATABASE microlenders_db;
CREATE DATABASE microlenders_db;
GRANT ALL PRIVILEGES ON DATABASE microlenders_db TO microlenders_user;
\q
```

Then run migrations again.

### Issue: Import errors
**Solution**: Ensure all dependencies are installed

```bash
pip install -r requirements.txt
```

### Issue: Static files not loading
**Solution**: Collect static files

```bash
python manage.py collectstatic
```

## Next Steps

1. **Explore the Admin Panel**: http://localhost:8000/admin/
2. **Read API Documentation**: See `API_DOCUMENTATION.md`
3. **Configure Production Settings**: See `DEPLOYMENT.md`
4. **Set up SSL/HTTPS** for production
5. **Configure email settings** for notifications
6. **Set up backup procedures** for database

## Getting Help

- Check the main README.md for detailed information
- Review API_DOCUMENTATION.md for API usage
- See DATABASE_SETUP.md for database configuration
- Review DEPLOYMENT.md for production deployment

## Security Notes

⚠️ **Important**: 
- Change the SECRET_KEY in production
- Use strong passwords
- Enable HTTPS in production
- Restrict DEBUG=False in production
- Set proper ALLOWED_HOSTS
- Keep dependencies updated
- Regular database backups

Enjoy using the Microlenders Management System!
