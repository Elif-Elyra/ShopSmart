from django.contrib import admin
from .models import Order, SubOrder, Review

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "total", "status", "created_at")
    list_filter = ("status",)
    

@admin.register(SubOrder)
class SubOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "seller", "status", "subtotal")
    list_filter = ("status",)
    
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "created_at")
