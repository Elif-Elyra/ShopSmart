from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Cart, CartItem, Product



def add_to_cart(user, product_id, quantity):
    
    with transaction.atomic(): 
        #get the product id and also lock that row for another users
        product = Product.objects.select_for_update().get(id = product_id)
        
        if quantity > product.stock:
            raise ValidationError( { "detail":"not enough stock" })
        
        # checks that user have a cart or not if not then create
        cart, _ = Cart.objects.get_or_create(user=user)  
        item, created = CartItem.objects.get_or_create(
            cart = cart,
            product = product,
            defaults ={
                "quantity": quantity,
                "unit_price_snapshot": product.price
            })
        
        if not created:
            new_qty = item.quantity + quantity
            if new_qty > product.stock:
                raise ValidationError({ "detail": "Not enough stock"})

            item.quantity = new_qty
            item.save()

        return item
        
        
       