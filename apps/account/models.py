from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
  
  
        
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)
    is_seller = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    email_otp = models.CharField(blank=True, max_length=4, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
    
 
class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    @property
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=2)
 
 
             
PUNJAB_CITIES = (
    ("Lahore", "Lahore"),
    ("Faisalabad", "Faisalabad"),
    ("Rawalpindi", "Rawalpindi"),
    ("Multan", "Multan"),
    ("Gujranwala", "Gujranwala"),
    ("Sialkot", "Sialkot"),
    ("Bahawalpur", "Bahawalpur"),
    ("Sargodha", "Sargodha"),
    ("Sheikhupura", "Sheikhupura"),
    ("Rahim Yar Khan", "Rahim Yar Khan"),
    ("Jhang", "Jhang"),
    ("Gujrat", "Gujrat"),
    ("Kasur", "Kasur"),
    ("Okara", "Okara"),
    ("Wah Cantt", "Wah Cantt"),
    ("Dera Ghazi Khan", "Dera Ghazi Khan"),
    ("Chiniot", "Chiniot"),
    ("Pakpattan", "Pakpattan"),
    ("Mianwali", "Mianwali"),
)


class Address(TimeStampedModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )

    label = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    line = models.CharField(max_length=255)
    line2 = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        choices=PUNJAB_CITIES
    )
    postal_code = models.CharField(max_length=20)
    region = models.CharField(
    max_length=100,
    blank=True,
    null=True
    ) 
    country = models.CharField(
        max_length=100,
        default="Pakistan"
    )

    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_default", "-created_at"]

    def save(self, *args, **kwargs):

        if self.is_default:

            Address.objects.filter(
                user=self.user
            ).update(is_default=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.city}"
     

class Wallet(TimeStampedModel):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    account_number = models.CharField(
        max_length=12,
        unique=True
    )

    # cached balance
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=3,
        default="USD"
    )

    def refresh_balance(self):

        credits = self.transactions.filter(
            direction="credit"
        ).aggregate(
            total=models.Sum("amount")
        )["total"] or 0

        debits = self.transactions.filter(
            direction="debit"
        ).aggregate(
            total=models.Sum("amount")
        )["total"] or 0

        self.balance = credits - debits
        self.save(update_fields=["balance"])

    def __str__(self):
        return f"{self.user.email}"
       
    
class WalletTransaction(TimeStampedModel):

    TYPE_CHOICES = (
        ("topup_simulated", "Topup Simulated"),
        ("order_payment", "Order Payment"),
        ("sale_proceeds", "Sale Proceeds"),
        ("refund_in", "Refund In"),
        ("refund_out", "Refund Out"),
        ("withdrawal_hold", "Withdrawal Hold"),
        ("withdrawal_release", "Withdrawal Release"),
        ("withdrawal_settled", "Withdrawal Settled"),
        ("platform_fee", "Platform Fee"),
    )

    DIRECTION_CHOICES = (
        ("credit", "Credit"),
        ("debit", "Debit"),
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    direction = models.CharField(
        max_length=20,
        choices=DIRECTION_CHOICES
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    related_object_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    related_object_id = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type}"
    
       
class BankAccount(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_accounts")
    holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    country = models.CharField(
    max_length=100,
    default="Pakistan"
    )
    account_number_encrypted = models.TextField()
    last4 = models.CharField(max_length=4)
    routing_code = models.CharField(max_length=50, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bank_name} ****{self.last4}"
    

class Withdrawal(TimeStampedModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("settled", "Settled"),
        ("rejected", "Rejected")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    decided_at = models.DateTimeField(null=True, blank=True)
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="processed_withdrawals")


    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.status})"
    
    
# User = identity
# Wallet = money container
# Transaction = history of money movement
# BankAccount = external cash-out method
# Withdrawal = request to move money outside system