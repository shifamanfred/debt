# Microlenders Management System

A comprehensive multi-tenant SaaS platform for microlending businesses. This system provides complete loan management capabilities including client enrollment, loan applications, approvals, disbursements, repayments, and credit bureau functionality.

## Features

### Multi-Tenancy
- **Business Registration**: Businesses can register by selecting a subscription package
- **Isolated Data**: Each tenant has its own database schema for data isolation
- **Custom Domains**: Support for custom domain mapping per tenant
- **Package-based Subscriptions**: Different tiers with varying features and limits

### User Management
- **Role-Based Access Control (RBAC)**:
  - Super Admin: System-wide management
  - Tenant Admin: Business owner/manager
  - Employee: Staff members with operational access
  - Client: Loan applicants and borrowers

### Client Portal (Free Access)
- **Self-Enrollment**: Clients can register for free
- **Profile Management**: View and update personal information
- **Loan Application**: Apply for loans online
- **Loan Tracking**: View loan status and repayment schedules
- **Credit Score**: View personal credit score

### Loan Management
- **Loan Products**: Define different loan types with custom terms
- **Application Workflow**:
  - Client submits application
  - Review and approval process
  - Automated loan creation on approval
- **Disbursement Tracking**: Record and track loan disbursements
- **Repayment Management**: 
  - Scheduled repayments
  - Payment recording
  - Multiple payment methods
- **Collections**: Track overdue payments and collections

### Credit Bureau System
- **Credit Scoring**: Automated credit score calculation
- **Risk Assessment**: Categorize clients by risk level
- **Loan History**: Complete historical records
- **Blacklist Management**: Track defaulters and high-risk clients
- **Credit Reporting**: Similar to credit bureau functionality

### System Administration
- **Superadmin Dashboard**: System-wide oversight
- **Tenant Management**: Monitor and manage all businesses
- **Package Management**: Create and modify subscription plans
- **Employee Management**: Tenant-level staff management
- **Reporting**: Comprehensive analytics and reports

## Technology Stack

- **Backend**: Django 4.2+
- **API**: Django REST Framework
- **Multi-tenancy**: django-tenants
- **Database**: PostgreSQL (required for multi-tenancy)
- **Authentication**: Django Authentication + Token-based auth

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd debt
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
Create a PostgreSQL database and update settings:
```bash
# Set environment variables or update microlenders_system/settings.py
export DB_NAME=microlenders_db
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

5. **Run migrations**
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Create default packages**
```bash
python manage.py shell
```
```python
from packages.models import Package

Package.objects.create(
    name="Starter",
    package_type="STARTER",
    description="Basic package for small businesses",
    monthly_price=49.99,
    max_clients=100,
    max_loans=50,
    max_employees=3,
    email_notifications=True
)

Package.objects.create(
    name="Professional",
    package_type="PROFESSIONAL",
    description="Full-featured package for growing businesses",
    monthly_price=149.99,
    max_clients=500,
    max_loans=250,
    max_employees=10,
    credit_bureau_access=True,
    sms_notifications=True,
    email_notifications=True,
    advanced_reporting=True
)
```

8. **Run the development server**
```bash
python manage.py runserver
```

## API Endpoints

### Public Endpoints (No Authentication Required)

#### Business Registration
```
POST /api/tenants/register_business/
```
Register a new business/tenant with package selection.

#### Package Listing
```
GET /api/packages/
```
View available subscription packages.

#### Client Enrollment
```
POST /api/clients/enroll/
```
Free client self-enrollment.

#### User Registration
```
POST /api/users/register/
```
General user registration.

### Protected Endpoints (Authentication Required)

#### Clients
- `GET /api/clients/` - List all clients (filtered by role)
- `GET /api/clients/{id}/` - Get client details
- `GET /api/clients/{id}/profile/` - View client profile
- `PUT /api/clients/{id}/` - Update client
- `DELETE /api/clients/{id}/` - Delete client

#### Loan Products
- `GET /api/loan-products/` - List loan products
- `POST /api/loan-products/` - Create loan product (admin only)
- `GET /api/loan-products/{id}/` - Get product details
- `PUT /api/loan-products/{id}/` - Update product
- `DELETE /api/loan-products/{id}/` - Delete product

#### Loan Applications
- `GET /api/loan-applications/` - List applications (filtered by role)
- `POST /api/loan-applications/` - Submit application
- `GET /api/loan-applications/{id}/` - Get application details
- `POST /api/loan-applications/{id}/approve/` - Approve application
- `POST /api/loan-applications/{id}/reject/` - Reject application

#### Loans
- `GET /api/loans/` - List loans (filtered by role)
- `POST /api/loans/` - Create loan
- `GET /api/loans/{id}/` - Get loan details
- `POST /api/loans/{id}/disburse/` - Disburse loan
- `PUT /api/loans/{id}/` - Update loan

#### Repayments
- `GET /api/repayments/` - List repayments
- `POST /api/repayments/` - Record repayment
- `GET /api/repayments/{id}/` - Get repayment details

#### Repayment Schedules
- `GET /api/repayment-schedules/` - List schedules
- `GET /api/repayment-schedules/{id}/` - Get schedule details

#### Credit Bureau
- `GET /api/credit-scores/` - List credit scores
- `GET /api/credit-scores/{id}/` - Get credit score
- `POST /api/credit-scores/{id}/recalculate/` - Recalculate score
- `GET /api/blacklist/` - List blacklisted clients (admin only)
- `POST /api/blacklist/` - Add to blacklist
- `POST /api/blacklist/{id}/clear/` - Clear blacklist record
- `GET /api/loan-history/` - View loan history

## User Roles and Permissions

### Super Admin
- Full system access
- Manage all tenants
- Create and modify packages
- System-wide monitoring

### Tenant Admin
- Manage their business
- Add/remove employees
- Approve/reject loans
- View all clients and loans
- Access reporting

### Employee
- Process loan applications
- Record repayments
- Manage client data
- View assigned loans

### Client
- View own profile (free)
- Apply for loans
- View loan status
- View repayment schedule
- View credit score

## Business Workflows

### 1. Business Registration Flow
1. Business selects a package
2. Fills registration form
3. System creates:
   - Tenant schema
   - Domain mapping
   - Admin user account
4. Business can start operations

### 2. Client Enrollment Flow (Free)
1. Client fills self-enrollment form
2. System creates:
   - User account
   - Client profile
   - Initial credit score
3. Client can immediately:
   - View profile
   - Apply for loans

### 3. Loan Application Flow
1. Client submits application
2. System validates:
   - Client eligibility
   - Loan product requirements
   - Credit score threshold
3. Application enters review queue
4. Admin/Employee reviews
5. Approval/Rejection decision
6. If approved, loan is created

### 4. Loan Disbursement Flow
1. Approved loan awaits disbursement
2. Admin/Employee processes disbursement
3. System records:
   - Disbursement amount
   - Disbursement date
   - Payment method
4. Repayment schedule generated
5. Loan becomes active

### 5. Repayment Flow
1. Client makes payment
2. Employee records repayment
3. System updates:
   - Loan outstanding balance
   - Repayment schedule
   - Client credit score
4. Generate receipt

### 6. Credit Scoring Flow
- Automatic calculation based on:
  - Loan history
  - Payment behavior
  - Defaults
  - Late payments
- Scores range: 0-1000
- Risk levels: Low, Medium, High, Very High

### 7. Blacklist Management
- Triggered by:
  - Loan defaults
  - Multiple late payments
  - Fraudulent activity
- Affects future loan eligibility
- Can be cleared by admin

## SaaS Features

### Package Tiers
1. **Starter** ($49.99/month)
   - Up to 100 clients
   - Up to 50 active loans
   - 3 employees
   - Email notifications

2. **Professional** ($149.99/month)
   - Up to 500 clients
   - Up to 250 active loans
   - 10 employees
   - Credit bureau access
   - SMS notifications
   - Advanced reporting
   - API access

3. **Enterprise** (Custom pricing)
   - Unlimited clients
   - Unlimited loans
   - Unlimited employees
   - All features
   - Custom branding
   - Dedicated support

### Billing Features
- Monthly/Annual billing options
- Automatic subscription management
- Usage tracking
- Upgrade/Downgrade options

## Security Features

- **Data Isolation**: Schema-based multi-tenancy
- **Authentication**: Django authentication system
- **Authorization**: Role-based access control
- **Password Security**: Hashed passwords
- **HTTPS**: SSL/TLS support (configure in production)
- **Input Validation**: Comprehensive validation
- **SQL Injection Protection**: ORM-based queries

## Deployment

### Production Considerations

1. **Database**: Use PostgreSQL with proper backups
2. **Static Files**: Use WhiteNoise or CDN
3. **Media Files**: Use cloud storage (S3, etc.)
4. **Environment Variables**: Secure configuration
5. **HTTPS**: Enable SSL certificates
6. **Monitoring**: Set up logging and monitoring
7. **Backups**: Regular database backups
8. **Scaling**: Consider load balancing

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=microlenders_db
DB_USER=postgres
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432
```

## Contributing

This is a private project. For contributions, please contact the project maintainers.

## Support

For support and inquiries, please contact the system administrator.

## License

Proprietary - All rights reserved.

