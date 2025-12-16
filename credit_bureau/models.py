from django.db import models
from django.conf import settings


class CreditScore(models.Model):
    """
    Credit scoring for clients based on their loan history and behavior.
    """
    RISK_LEVEL = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('VERY_HIGH', 'Very High Risk'),
    ]
    
    client = models.OneToOneField('clients.Client', on_delete=models.CASCADE, related_name='credit_score')
    
    # Credit score (0-1000)
    score = models.IntegerField(default=500)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL, default='MEDIUM')
    
    # Factors
    total_loans = models.IntegerField(default=0)
    active_loans = models.IntegerField(default=0)
    completed_loans = models.IntegerField(default=0)
    defaulted_loans = models.IntegerField(default=0)
    
    on_time_payments = models.IntegerField(default=0)
    late_payments = models.IntegerField(default=0)
    missed_payments = models.IntegerField(default=0)
    
    total_borrowed = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_repaid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_outstanding = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Last updated
    last_calculated = models.DateTimeField(auto_now=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'credit_scores'
        
    def __str__(self):
        return f"{self.client.full_name} - Score: {self.score} ({self.risk_level})"
    
    def calculate_score(self):
        """
        Calculate credit score based on various factors.
        This is a simplified scoring algorithm.
        """
        base_score = 500
        
        # Positive factors
        if self.completed_loans > 0:
            base_score += min(self.completed_loans * 20, 150)
        
        if self.on_time_payments > 0 and (self.on_time_payments + self.late_payments) > 0:
            on_time_rate = self.on_time_payments / (self.on_time_payments + self.late_payments)
            base_score += int(on_time_rate * 200)
        
        # Negative factors
        if self.defaulted_loans > 0:
            base_score -= self.defaulted_loans * 100
        
        if self.late_payments > 0:
            base_score -= min(self.late_payments * 10, 100)
        
        if self.missed_payments > 0:
            base_score -= min(self.missed_payments * 20, 150)
        
        # Keep score within bounds
        self.score = max(0, min(base_score, 1000))
        
        # Determine risk level
        if self.score >= 750:
            self.risk_level = 'LOW'
        elif self.score >= 550:
            self.risk_level = 'MEDIUM'
        elif self.score >= 350:
            self.risk_level = 'HIGH'
        else:
            self.risk_level = 'VERY_HIGH'
        
        self.save()


class Blacklist(models.Model):
    """
    Blacklisted clients who have defaulted on loans or violated terms.
    Similar to credit bureau reporting.
    """
    BLACKLIST_REASON = [
        ('DEFAULT', 'Loan Default'),
        ('FRAUD', 'Fraudulent Activity'),
        ('MULTIPLE_DEFAULTS', 'Multiple Defaults'),
        ('LEGAL_ACTION', 'Legal Action Required'),
        ('OTHER', 'Other'),
    ]
    
    BLACKLIST_STATUS = [
        ('ACTIVE', 'Active'),
        ('UNDER_REVIEW', 'Under Review'),
        ('CLEARED', 'Cleared'),
        ('EXPIRED', 'Expired'),
    ]
    
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='blacklist_records')
    
    reason = models.CharField(max_length=20, choices=BLACKLIST_REASON)
    description = models.TextField()
    
    # Related loan if applicable
    related_loan = models.ForeignKey('loans.Loan', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Amount owed
    amount_owed = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=BLACKLIST_STATUS, default='ACTIVE')
    
    # Dates
    blacklisted_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    cleared_date = models.DateField(null=True, blank=True)
    
    # Action taken by
    blacklisted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='blacklisted_clients')
    cleared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cleared_blacklists')
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'blacklist'
        ordering = ['-blacklisted_date']
        
    def __str__(self):
        return f"{self.client.full_name} - {self.get_reason_display()} ({self.status})"


class LoanHistory(models.Model):
    """
    Complete loan history for credit reporting purposes.
    """
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='loan_history')
    loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE)
    
    # Snapshot of loan details at time of recording
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_term = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Outcome
    completion_status = models.CharField(max_length=20)  # COMPLETED, DEFAULT, WRITTEN_OFF
    final_payment_date = models.DateField(null=True, blank=True)
    
    # Performance
    days_overdue = models.IntegerField(default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_history'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.client.full_name} - {self.loan.loan_number}"

