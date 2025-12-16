# Usage Examples

This document provides practical examples of common workflows in the Microlenders Management System.

## Table of Contents

1. [Business Registration](#business-registration)
2. [Client Enrollment](#client-enrollment)
3. [Loan Application Process](#loan-application-process)
4. [Loan Approval and Disbursement](#loan-approval-and-disbursement)
5. [Recording Repayments](#recording-repayments)
6. [Credit Score Management](#credit-score-management)
7. [Blacklist Management](#blacklist-management)

## Business Registration

### Scenario: A new microlending business wants to register

```python
import requests

url = "http://localhost:8000/api/tenants/register_business/"
data = {
    "business_name": "ABC Microfinance Ltd",
    "business_email": "contact@abcmicro.com",
    "business_phone": "+254712345678",
    "address": "123 Business Park, Nairobi, Kenya",
    "package_id": 1,  # Starter package
    "admin_username": "abc_admin",
    "admin_email": "admin@abcmicro.com",
    "admin_password": "SecurePassword123!",
    "domain": "abc.microlenders.local"
}

response = requests.post(url, json=data)
print(response.json())
# Output: {
#     "message": "Business registered successfully",
#     "tenant_id": 1,
#     "schema_name": "abc_microfinance_ltd",
#     "domain": "abc.microlenders.local"
# }
```

## Client Enrollment

### Scenario: A potential borrower wants to enroll (free)

```python
import requests

url = "http://localhost:8000/api/clients/enroll/"
data = {
    "username": "mary_wanjiku",
    "email": "mary.wanjiku@email.com",
    "password": "SecurePass456!",
    "first_name": "Mary",
    "middle_name": "Njeri",
    "last_name": "Wanjiku",
    "date_of_birth": "1985-06-15",
    "gender": "F",
    "national_id": "12345678",
    "phone": "+254712345679",
    "alternative_phone": "+254723456789",
    "address": "456 Riverside, Apartment 12",
    "city": "Nairobi",
    "postal_code": "00100",
    "employment_status": "EMPLOYED",
    "employer_name": "XYZ Corporation",
    "employer_phone": "+254722334455",
    "employer_address": "789 Industrial Area",
    "monthly_income": "75000.00",
    "marital_status": "MARRIED",
    "number_of_dependents": 2,
    "emergency_contact_name": "John Wanjiku",
    "emergency_contact_phone": "+254733445566",
    "emergency_contact_relationship": "Spouse"
}

response = requests.post(url, json=data)
print(response.json())
# Output: {
#     "message": "Client enrolled successfully",
#     "client_id": 1,
#     "username": "mary_wanjiku"
# }
```

## Loan Application Process

### Scenario: Client applies for a loan

```python
import requests

# First, login to get authentication token
login_url = "http://localhost:8000/api/auth/login/"
login_data = {
    "username": "mary_wanjiku",
    "password": "SecurePass456!"
}
session = requests.Session()
session.post(login_url, json=login_data)

# Submit loan application
app_url = "http://localhost:8000/api/loan-applications/"
app_data = {
    "client": 1,
    "loan_product": 1,  # Personal loan product
    "requested_amount": "100000.00",
    "requested_term_months": 12,
    "purpose": "Small business expansion - purchase of inventory"
}

response = session.post(app_url, json=app_data)
print(response.json())
# Output: {
#     "id": 1,
#     "application_number": "APP-A1B2C3D4",
#     "client": 1,
#     "client_name": "Mary Njeri Wanjiku",
#     "loan_product": 1,
#     "requested_amount": "100000.00",
#     "requested_term_months": 12,
#     "purpose": "Small business expansion - purchase of inventory",
#     "status": "PENDING",
#     ...
# }
```

## Loan Approval and Disbursement

### Scenario: Loan officer reviews and approves application

```python
import requests

# Login as admin/employee
session = requests.Session()
login_data = {
    "username": "abc_admin",
    "password": "SecurePassword123!"
}
session.post("http://localhost:8000/api/auth/login/", json=login_data)

# Approve application
approve_url = "http://localhost:8000/api/loan-applications/1/approve/"
approve_data = {
    "review_notes": "Client has good credit history and stable income. Approved for requested amount."
}

response = session.post(approve_url, json=approve_data)
print(response.json())
# Output: {"message": "Application approved successfully"}

# Create loan record
loan_url = "http://localhost:8000/api/loans/"
loan_data = {
    "application": 1,
    "client": 1,
    "loan_product": 1,
    "principal_amount": "100000.00",
    "interest_rate": "15.00",
    "term_months": 12,
    "monthly_payment": "9025.00",
    "total_interest": "8300.00",
    "total_amount": "108300.00",
    "outstanding_balance": "108300.00"
}

loan_response = session.post(loan_url, json=loan_data)
print(loan_response.json())

# Disburse loan
loan_id = loan_response.json()['id']
disburse_url = f"http://localhost:8000/api/loans/{loan_id}/disburse/"
disburse_data = {
    "disbursed_amount": "100000.00"
}

disburse_response = session.post(disburse_url, json=disburse_data)
print(disburse_response.json())
# Output: {"message": "Loan disbursed successfully"}
```

## Recording Repayments

### Scenario: Client makes a payment

```python
import requests
from datetime import date

session = requests.Session()
# Login as employee
session.post("http://localhost:8000/api/auth/login/", json={
    "username": "loan_officer",
    "password": "password"
})

# Record repayment
repayment_url = "http://localhost:8000/api/repayments/"
repayment_data = {
    "loan": 1,
    "amount": "9025.00",
    "payment_date": date.today().isoformat(),
    "payment_method": "MOBILE_MONEY",
    "principal_paid": "7525.00",
    "interest_paid": "1500.00",
    "late_fee_paid": "0.00",
    "transaction_reference": "MPESA-XYZ123456789",
    "notes": "First installment - on time"
}

response = session.post(repayment_url, json=repayment_data)
print(response.json())
# Output: {
#     "id": 1,
#     "receipt_number": "RCP-E7F8G9H0",
#     "loan": 1,
#     "amount": "9025.00",
#     "payment_date": "2024-01-15",
#     "payment_method": "MOBILE_MONEY",
#     "status": "COMPLETED",
#     ...
# }
```

## Credit Score Management

### Scenario: View and recalculate client credit score

```python
import requests

session = requests.Session()
session.post("http://localhost:8000/api/auth/login/", json={
    "username": "abc_admin",
    "password": "SecurePassword123!"
})

# View credit score
score_url = "http://localhost:8000/api/credit-scores/1/"
response = session.get(score_url)
print(response.json())
# Output: {
#     "id": 1,
#     "client": 1,
#     "client_name": "Mary Njeri Wanjiku",
#     "score": 650,
#     "risk_level": "MEDIUM",
#     "total_loans": 3,
#     "active_loans": 1,
#     "completed_loans": 2,
#     "defaulted_loans": 0,
#     "on_time_payments": 24,
#     "late_payments": 2,
#     ...
# }

# Recalculate score after new payment
recalc_url = "http://localhost:8000/api/credit-scores/1/recalculate/"
response = session.post(recalc_url)
print(response.json())
```

## Blacklist Management

### Scenario: Add a client to blacklist for default

```python
import requests
from datetime import date, timedelta

session = requests.Session()
session.post("http://localhost:8000/api/auth/login/", json={
    "username": "abc_admin",
    "password": "SecurePassword123!"
})

# Add to blacklist
blacklist_url = "http://localhost:8000/api/blacklist/"
blacklist_data = {
    "client": 5,  # Client who defaulted
    "reason": "DEFAULT",
    "description": "Client defaulted on loan after 6 months of non-payment",
    "related_loan": 10,
    "amount_owed": "75000.00",
    "status": "ACTIVE",
    "expiry_date": (date.today() + timedelta(days=365*2)).isoformat(),  # 2 years
    "notes": "Multiple attempts to contact client failed. Legal action being considered."
}

response = session.post(blacklist_url, json=blacklist_data)
print(response.json())

# Later, clear the blacklist record
blacklist_id = response.json()['id']
clear_url = f"http://localhost:8000/api/blacklist/{blacklist_id}/clear/"
clear_data = {
    "notes": "Client settled full amount plus penalties. Cleared from blacklist."
}

clear_response = session.post(clear_url, json=clear_data)
print(clear_response.json())
# Output: {"message": "Blacklist record cleared"}
```

## Common Queries

### Get all pending loan applications

```python
response = session.get("http://localhost:8000/api/loan-applications/?status=PENDING")
applications = response.json()
```

### Get active loans for a client

```python
response = session.get("http://localhost:8000/api/loans/?client=1&status=ACTIVE")
loans = response.json()
```

### Get overdue repayments

```python
from datetime import date

response = session.get("http://localhost:8000/api/repayment-schedules/?status=OVERDUE")
overdue = response.json()
```

### View loan history for a client

```python
response = session.get("http://localhost:8000/api/loan-history/?client=1")
history = response.json()
```

## Using the Admin Panel

### Access Admin Panel
1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to different sections:
   - **Tenants**: Manage businesses
   - **Packages**: View/edit subscription plans
   - **Users**: Manage all users
   - **Clients**: View client profiles
   - **Loan Products**: Configure loan offerings
   - **Loan Applications**: Review applications
   - **Loans**: Monitor active loans
   - **Repayments**: Track payments
   - **Credit Scores**: View credit information
   - **Blacklist**: Manage blacklisted clients

## Reporting Examples

### Generate Monthly Report

```python
import requests
from datetime import date, timedelta

session = requests.Session()
session.post("http://localhost:8000/api/auth/login/", json={
    "username": "abc_admin",
    "password": "SecurePassword123!"
})

# Get data for current month
start_date = date.today().replace(day=1)
end_date = date.today()

# New applications this month
apps_response = session.get(
    f"http://localhost:8000/api/loan-applications/?created_at__gte={start_date}"
)

# Disbursements this month
loans_response = session.get(
    f"http://localhost:8000/api/loans/?disbursement_date__gte={start_date}"
)

# Repayments this month
payments_response = session.get(
    f"http://localhost:8000/api/repayments/?payment_date__gte={start_date}"
)

# New clients this month
clients_response = session.get(
    f"http://localhost:8000/api/clients/?enrollment_date__gte={start_date}"
)

# Generate report
report = {
    "period": f"{start_date} to {end_date}",
    "new_applications": len(apps_response.json()['results']),
    "disbursed_loans": len(loans_response.json()['results']),
    "total_disbursed": sum(float(l['disbursed_amount']) for l in loans_response.json()['results']),
    "repayments_received": len(payments_response.json()['results']),
    "total_collected": sum(float(p['amount']) for p in payments_response.json()['results']),
    "new_clients": len(clients_response.json()['results'])
}

print(report)
```

## Best Practices

1. **Always use HTTPS in production**
2. **Validate input data** before sending to API
3. **Handle errors gracefully**
4. **Store authentication tokens securely**
5. **Log all financial transactions**
6. **Implement rate limiting** for API calls
7. **Regular backups** of all data
8. **Monitor credit scores** regularly
9. **Review blacklist** periodically
10. **Keep audit trails** for all operations

## Error Handling

```python
import requests

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raises HTTPError for bad responses
    result = response.json()
    print("Success:", result)
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.text}")
except requests.exceptions.ConnectionError:
    print("Failed to connect to the server")
except requests.exceptions.Timeout:
    print("Request timed out")
except Exception as e:
    print(f"An error occurred: {e}")
```

For more examples and detailed API documentation, see `API_DOCUMENTATION.md`.
