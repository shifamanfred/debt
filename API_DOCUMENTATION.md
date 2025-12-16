# API Documentation

## Authentication

Most API endpoints require authentication. Use Django's session authentication or token-based authentication.

### Login
```bash
POST /api/auth/login/
{
    "username": "your_username",
    "password": "your_password"
}
```

## Example API Requests

### 1. Business Registration

```bash
curl -X POST http://localhost:8000/api/tenants/register_business/ \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "ABC Microfinance",
    "business_email": "info@abcmicro.com",
    "business_phone": "+1234567890",
    "address": "123 Main St, City",
    "package_id": 1,
    "admin_username": "admin",
    "admin_email": "admin@abcmicro.com",
    "admin_password": "securepassword",
    "domain": "abc.microlenders.com"
  }'
```

### 2. View Available Packages

```bash
curl http://localhost:8000/api/packages/
```

### 3. Client Self-Enrollment

```bash
curl -X POST http://localhost:8000/api/clients/enroll/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "gender": "M",
    "national_id": "ID123456",
    "phone": "+1234567890",
    "address": "456 Oak St",
    "city": "Springfield",
    "employment_status": "EMPLOYED",
    "employer_name": "ABC Company",
    "monthly_income": "5000.00",
    "marital_status": "SINGLE",
    "number_of_dependents": 0
  }'
```

### 4. Submit Loan Application

```bash
curl -X POST http://localhost:8000/api/loan-applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "client": 1,
    "loan_product": 1,
    "requested_amount": "10000.00",
    "requested_term_months": 12,
    "purpose": "Business expansion"
  }'
```

### 5. Approve Loan Application

```bash
curl -X POST http://localhost:8000/api/loan-applications/1/approve/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "review_notes": "Approved based on good credit history"
  }'
```

### 6. Disburse Loan

```bash
curl -X POST http://localhost:8000/api/loans/1/disburse/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "disbursed_amount": "10000.00"
  }'
```

### 7. Record Repayment

```bash
curl -X POST http://localhost:8000/api/repayments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "loan": 1,
    "amount": "1000.00",
    "payment_date": "2024-01-15",
    "payment_method": "BANK_TRANSFER",
    "principal_paid": "800.00",
    "interest_paid": "200.00",
    "transaction_reference": "TXN123456"
  }'
```

### 8. View Credit Score

```bash
curl http://localhost:8000/api/credit-scores/1/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### 9. View Client Profile

```bash
curl http://localhost:8000/api/clients/1/profile/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### 10. List Loan Products

```bash
curl http://localhost:8000/api/loan-products/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

## Response Formats

### Success Response
```json
{
  "message": "Operation successful",
  "data": { }
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": { }
}
```

## Status Codes

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Pagination

List endpoints support pagination:
```
GET /api/clients/?page=2&page_size=20
```

## Filtering

Some endpoints support filtering:
```
GET /api/loans/?status=ACTIVE
GET /api/loan-applications/?status=PENDING
GET /api/clients/?employment_status=EMPLOYED
```

## Ordering

Use the `ordering` parameter:
```
GET /api/loans/?ordering=-created_at
GET /api/clients/?ordering=last_name
```
