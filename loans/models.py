from django.db import models
from django.conf import settings
from decimal import Decimal


class LoanProduct(models.Model):
    """
    Different types of loan products offered by the microlender.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Loan terms
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in percentage")
    min_term_months = models.IntegerField(help_text="Minimum loan term in months")
    max_term_months = models.IntegerField(help_text="Maximum loan term in months")
    
    # Fees
    processing_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    late_payment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Requirements
    min_credit_score = models.IntegerField(default=0)
    requires_collateral = models.BooleanField(default=False)
    requires_guarantor = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_products'
        
    def __str__(self):
        return f"{self.name} ({self.interest_rate}% p.a.)"


class LoanApplication(models.Model):
    """
    Loan applications submitted by clients.
    """
    APPLICATION_STATUS = [
        ('PENDING', 'Pending Review'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]
    
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='loan_applications')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    
    # Application details
    application_number = models.CharField(max_length=50, unique=True)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    requested_term_months = models.IntegerField()
    purpose = models.TextField()
    
    # Status and workflow
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='PENDING')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_applications'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Application {self.application_number} - {self.client.full_name}"


class Loan(models.Model):
    """
    Active loans that have been approved and disbursed.
    """
    LOAN_STATUS = [
        ('APPROVED', 'Approved'),
        ('DISBURSED', 'Disbursed'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DEFAULT', 'Default'),
        ('WRITTEN_OFF', 'Written Off'),
    ]
    
    application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='loan')
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='loans')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    
    # Loan details
    loan_number = models.CharField(max_length=50, unique=True)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Calculated fields
    total_interest = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='APPROVED')
    
    # Disbursement
    disbursed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    disbursement_date = models.DateField(null=True, blank=True)
    disbursed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='disbursed_loans')
    
    # Dates
    approval_date = models.DateField(auto_now_add=True)
    first_payment_date = models.DateField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Loan {self.loan_number} - {self.client.full_name}"
    
    def calculate_monthly_payment(self):
        """Calculate monthly payment using loan amortization formula."""
        if self.term_months == 0:
            return Decimal('0')
        
        r = self.interest_rate / Decimal('100') / Decimal('12')  # Monthly interest rate
        n = self.term_months
        
        if r == 0:
            return self.principal_amount / Decimal(str(n))
        
        # Monthly payment formula: P * [r(1+r)^n] / [(1+r)^n - 1]
        payment = self.principal_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return round(payment, 2)


class Repayment(models.Model):
    """
    Loan repayments and collections.
    """
    PAYMENT_METHOD = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('CHEQUE', 'Cheque'),
        ('CARD', 'Card'),
    ]
    
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    
    # Payment details
    receipt_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    
    # Breakdown
    principal_paid = models.DecimalField(max_digits=12, decimal_places=2)
    interest_paid = models.DecimalField(max_digits=12, decimal_places=2)
    late_fee_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='COMPLETED')
    
    # Reference
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    # Recorded by
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recorded_repayments')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'repayments'
        ordering = ['-payment_date']
        
    def __str__(self):
        return f"Payment {self.receipt_number} - {self.amount}"


class RepaymentSchedule(models.Model):
    """
    Scheduled repayments for loans.
    """
    SCHEDULE_STATUS = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('OVERDUE', 'Overdue'),
        ('WRITTEN_OFF', 'Written Off'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayment_schedule')
    
    installment_number = models.IntegerField()
    due_date = models.DateField()
    
    # Amounts
    principal_due = models.DecimalField(max_digits=12, decimal_places=2)
    interest_due = models.DecimalField(max_digits=12, decimal_places=2)
    total_due = models.DecimalField(max_digits=12, decimal_places=2)
    
    principal_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=SCHEDULE_STATUS, default='PENDING')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'repayment_schedules'
        ordering = ['due_date']
        unique_together = ['loan', 'installment_number']
        
    def __str__(self):
        return f"Schedule {self.installment_number} for Loan {self.loan.loan_number}"

