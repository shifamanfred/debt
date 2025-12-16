# Database Setup Guide

## PostgreSQL Installation

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### macOS
```bash
brew install postgresql
brew services start postgresql
```

### Windows
Download and install from: https://www.postgresql.org/download/windows/

## Database Configuration

1. **Access PostgreSQL**
```bash
sudo -u postgres psql
```

2. **Create Database**
```sql
CREATE DATABASE microlenders_db;
```

3. **Create User**
```sql
CREATE USER microlenders_user WITH PASSWORD 'your_secure_password';
```

4. **Grant Privileges**
```sql
GRANT ALL PRIVILEGES ON DATABASE microlenders_db TO microlenders_user;
ALTER USER microlenders_user CREATEDB;
```

5. **Exit PostgreSQL**
```sql
\q
```

## Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=microlenders_db
DB_USER=microlenders_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

## Running Migrations

### For multi-tenancy setup:

1. **Migrate shared apps** (run first)
```bash
python manage.py migrate_schemas --shared
```

2. **Migrate tenant apps** (run after shared)
```bash
python manage.py migrate_schemas
```

### Creating a Public Tenant

The public tenant is required for django-tenants:

```python
python manage.py shell
```

```python
from tenants.models import Tenant, Domain

# Create public tenant
tenant = Tenant(
    schema_name='public',
    name='Public',
    business_name='Public Schemas',
    business_email='admin@example.com',
    business_phone='0000000000',
)
tenant.save()

# Create domain for public tenant
domain = Domain()
domain.domain = 'localhost'  # Use your domain here
domain.tenant = tenant
domain.is_primary = True
domain.save()
```

## Database Backup

### Backup
```bash
pg_dump -U microlenders_user microlenders_db > backup.sql
```

### Restore
```bash
psql -U microlenders_user microlenders_db < backup.sql
```

## Common Issues

### Issue: psycopg2 installation fails
**Solution**: Install PostgreSQL development files
```bash
# Ubuntu/Debian
sudo apt-get install libpq-dev python3-dev

# macOS
brew install postgresql
```

### Issue: Permission denied for database
**Solution**: Grant proper permissions
```sql
GRANT ALL PRIVILEGES ON DATABASE microlenders_db TO microlenders_user;
ALTER USER microlenders_user CREATEDB;
```

### Issue: Migration conflicts
**Solution**: Reset migrations (development only!)
```bash
python manage.py migrate --fake-initial
```

## Production Database Considerations

1. **Use connection pooling** (e.g., pgBouncer)
2. **Enable SSL connections**
3. **Set up regular backups**
4. **Configure proper indexes**
5. **Monitor query performance**
6. **Use read replicas for scaling**
7. **Enable query logging for debugging**
8. **Set appropriate `max_connections`**

## Database Schema

The multi-tenant architecture uses PostgreSQL schemas:
- `public` schema: Shared data (tenants, packages, domains)
- `tenant_xxx` schemas: Tenant-specific data (users, clients, loans)

Each tenant has isolated data in their own schema, ensuring data privacy and security.
