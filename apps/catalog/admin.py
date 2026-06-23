from django.contrib import admin
from .models import Category, Product, ProductImage, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("id","name","slug","parent")
    prepopulated_fields = {"slug":("name",)}
    ordering =("id",)
    



class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1



# In core/admin.py
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "seller",
        "title",
        "price",
        "thumbnail",
        "stock",
        "status",
        "category",
        "created_at"
    ]

    list_filter = ("status", "condition", "category")
    search_fields = ("title", "sku")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]
    list_editable = ("price", "stock", "status")
    ordering = ("-created_at",)
    
   
@admin.register(CartItem) 
class CartItemAdmin(admin.ModelAdmin):
    list_display =["cart", "product", "quantity", "unit_price_snapshot"]
