from django.db import models
from django.conf import settings
from apps.account.models import TimeStampedModel

# [fiels.name for field in Product._meta.fields] => list comprehension

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    on_delete=models.PROTECT,
    related_name="children"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self): # current object instance
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    
class Product(TimeStampedModel):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    CONDITION = (
        ("new", "new"),
        ("used", "used"),
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    condition = models.CharField(max_length=10, choices=CONDITION, default="new")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    thumbnail = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["status"]),
        ]
        constraints = [ # rule applied on database field to control what data is allowed
             models.CheckConstraint(
                  condition=models.Q(price__gte=0),
                  name="price_non_negative"
           
       
             ),
             models.CheckConstraint(
                 condition=models.Q(stock__gte=0),
                 name="stock_non_negative"
             ),
        
    
        ]
        
    def __str__(self):
        return f"{self.title} ({self.sku})"
    
    
    
class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["position"]
        indexes = [
            models.Index(fields=["product", "position"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields = ["product", "position"],
                name="unique_product_image_position"
            )
        ]
    
    def save(self, *args, **kwargs): #current object instance,  Extra unnamed arguments, Extra named arguments.
          is_new = self.pk is None
          super().save(*args, **kwargs)
          if is_new and not self.product.thumbnail:
              self.product.thumbnail = self.image
              self.product.save()
        

    def __str__(self):
        return f"{self.product.title} image #{self.position}"
    
    

class Cart(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-updated_at"]
        

    def __str__(self):
        return f"Cart ({self.user.fullname} with this {self.user.email})" 
    
       

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    unit_price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        constraints = [

            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart"
            ),

            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="quantity_min_1"
            )
        ]

    def save(self, *args, **kwargs):

        if self.unit_price_snapshot is None:
            self.unit_price_snapshot = self.product.price

        super().save(*args, **kwargs)   
    
    