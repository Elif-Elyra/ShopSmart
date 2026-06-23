from django.db import models
from apps.catalog.models import Product
from apps.account.models import TimeStampedModel
from django.conf import settings
from django.core.validators import MaxLengthValidator

# Create your models here.


class Order(TimeStampedModel):

    STATUS_CHOICES = (
        ("pending_payment", "Pending Payment"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending_payment"
    )

    shipping_address = models.JSONField()

    # payment snapshot
    card_brand = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    card_last4 = models.CharField(
        max_length=4,
        blank=True,
        null=True
    )

    card_expiry_month = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    card_expiry_year = models.CharField(
        max_length=4,
        blank=True,
        null=True
    )

    idempotency_key = models.CharField(
        max_length=255,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["buyer"]),
            models.Index(fields=["status"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=0),
                name="order_total_non_negative"
            )
        ]

    def __str__(self):
        return f"Order #{self.id}"  


class SubOrder(TimeStampedModel):

    STATUS_CHOICES = (
        ("pending_payment", "Pending Payment"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="suborders"
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sales"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending_payment"
    )

    shipping = models.CharField(
        max_length=50,
        default="standard"
    )

    tracking_code = models.CharField(
        max_length=50,
        blank=True
    )

    shipped_at = models.DateTimeField(
        null=True,
        blank=True
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["id"]
 
    
    
class OrderItem(models.Model):
    suborder = models.ForeignKey(SubOrder,on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_title = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField( max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["suborder", "product"],
                name="unique_product_per_suborder"
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="orderitem_quantity_min_1"
            ),
            models.CheckConstraint(
                condition=models.Q(line_total__gte=0),
                name="line_total_non_negative"
            )
        ]

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"



class Review(TimeStampedModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField(
    validators=[MaxLengthValidator(500)]
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="one_review_per_user_product"
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="rating_between_1_5"
            )
        ]

    def __str__(self):
        return f"{self.user.email} → {self.product.title}"
    
    
    
class Notification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    type_noti = models.CharField(max_length=100)
    payload = models.JSONField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification ({self.user.email})"  
       
    
class IdempotencyKey(TimeStampedModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="idempotency_keys"
    )

    key = models.CharField(max_length=255)

    request_hash = models.CharField(
        max_length=255
    )

    response = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "key"],
                name="unique_idempotency_per_user"
            )
        ]
        
           