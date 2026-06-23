# ==============================
# BLOCK 1
# IMPORTS + HELPERS + VALIDATION
# ==============================

from decimal import Decimal
from django.utils import timezone
import hashlib
import json
import random
from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.exceptions import ValidationError

from apps.catalog.models import Cart
from apps.account.models import (
    Address,
    Wallet,
    WalletTransaction
)

from .models import (
    Order,
    SubOrder,
    OrderItem,
    IdempotencyKey
)
from apps.orders.models import Notification

class CheckoutService:
    # -----------------------------
    # GENERATE UNIQUE ACCOUNT NUMBER
    # -----------------------------
    
    @staticmethod #Python decorator
    def generate_account_number():

        while True:
            account_number = "".join(random.choices("0123456789",k=12))
            exists = (Wallet.objects.filter(account_number = account_number).exists())
            if not exists:
                return account_number

    # -----------------------------
    # indentify REQUEST HASH
    # -----------------------------

    @staticmethod #decorator wrapp the function 
    def generate_request_hash(data):
        #payload = request data, json.dumps = dic to json str,str to byte, 256#
        payload = json.dumps( data, sort_keys=True )
        return hashlib.sha256( payload.encode()).hexdigest()

    # -----------------------------
    # LUHN CHECK
    # -----------------------------

    @staticmethod
    def luhn_check(card_number):
             
        digits = [ int(d) for d in card_number ] # str in int list
        checksum = 0
        reverse_digits = ( digits[::-1] ) #reverse
        
        for index, digit in enumerate( reverse_digits ): # built-in function which is used to find ind, digit
            if index % 2 == 1: #odd number
                digit *= 2 # square
                if digit > 9:
                    digit -= 9 # minus 9
            checksum += digit 
        return ( checksum % 10 == 0 )

    # -----------------------------
    # CARD BRAND
    # -----------------------------

    @staticmethod
    def get_card_brand(card_number):
        if card_number.startswith("4"):
            return "Visa"
        if card_number.startswith( ("51", "52","53","54","55") ):
            return "Mastercard"
        
        return "Unknown"

    # -----------------------------
    # VALIDATE CARD
    # -----------------------------

    @staticmethod
    def validate_card(payment):
        card_number = (payment.get("card_number","" ).replace(" ", "").strip() )
        holder_name = ( payment.get( "holder_name", "" ).strip())
        expiry_month = (payment.get("expiry_month" ) )
        expiry_year = ( payment.get("expiry_year" ))
        cvv = ( payment.get( "cvv", "" ).strip() )

        # is Number || len 13 || 19 digits
        if ( not card_number.isdigit() or len(card_number) < 13  or len(card_number) > 19 ):
            raise ValidationError({"detail": "invalid_card_number"})
        
        # Luhn check
        if not ( CheckoutService.luhn_check(card_number)):
            raise ValidationError({ "detail":"invalid_card_number" })
        
        # Cardholder validation
        if ( len(holder_name) < 2 or len(holder_name) > 60 ):
            raise ValidationError({ "detail": "invalid_cardholder_name" })

        # CVV validation is number, length 3,4
        if ( not cvv.isdigit() or len(cvv) not in [3, 4] ):
            raise ValidationError({ "detail": "invalid_cvv" })

        try:
            expiry_month = int(expiry_month) # may be it's str so it convert str to numbers
            expiry_year = int(expiry_year)
        except ( TypeError, ValueError ):
            raise ValidationError({ "detail": "invalid_expiry" })

        # Month validation
        if ( expiry_month < 1 or expiry_month > 12 ): #month should in 1 to 12
            raise ValidationError({ "detail": "invalid_expiry_month" })

        current_year = timezone.now().year
        current_month = timezone.now().month

        if ( expiry_year < current_year ):
            raise ValidationError({"detail": "expired_card" })

        if ( expiry_year == current_year and expiry_month < current_month ):
            raise ValidationError({ "detail": "expired_card" })

        return True

    # -----------------------------
    # SIMULATED PAYMENT
    # -----------------------------

    @staticmethod
    def simulate_payment(payment, cart_total):
        CheckoutService.validate_card(payment)
        card_number = (payment ["card_number"] )

        # deterministic decline
        if card_number.endswith( "0000"):
            raise ValidationError({"detail": "do_not_honor"})

        if card_number.endswith("0001"):
            raise ValidationError({"detail":"insufficient_funds"})
           # "attribute get karo
        limit = Decimal(str(getattr(settings,"SIMULATED_CARD_LIMIT",5000)))

        if cart_total > limit:
            raise ValidationError({"detail":"limit_exceeded"})

        return True
      
    # ==============================
    # BLOCK 2 => WALLET HELPERS + CHECKOUT
    # ==============================

    @staticmethod
    def get_wallet_balance( wallet ):

        credits = (
            WalletTransaction.objects.filter(
                wallet=wallet,
                direction="credit"
            ).aggregate(total=Coalesce(
                    Sum("amount"),
                    Decimal("0")
                )
            )["total"] )

        debits = (WalletTransaction.objects.filter(
                wallet=wallet,
                direction="debit"
            ).aggregate( #db-level calculations, sum of all the val 
                total=Coalesce( # if 1st val none then take it 2nd decimal("0")
                    Sum("amount"), # sum() col val
                    Decimal("0")
                )
            )["total"] ) #after aggregate the value in return in dic so it store in total key 

        return ( credits - debits )

    @staticmethod
    def get_or_create_wallet( user_id ):

        wallet, _ = (
            Wallet.objects.get_or_create(
                user_id=user_id,
                defaults={
                    "account_number": CheckoutService.generate_account_number(),
                    "currency":getattr( settings,"DEFAULT_CURRENCY","USD")
                }
            )
        )
        return wallet



    @staticmethod
    def create_wallet_transaction(wallet, transaction_type, direction, amount, reference, related_object_type,    related_object_id ):

            transaction = (
                WalletTransaction.objects.create(
                    wallet=wallet,
                    transaction_type=transaction_type,
                    direction=direction,
                    amount=amount,
                    reference=reference,
                    related_object_type=related_object_type,
                    related_object_id=related_object_id
                )
            )
            wallet.refresh_balance()
            return transaction

    @staticmethod
    @transaction.atomic
    def create_order( user, data, idempotency_key ):

        request_hash = (CheckoutService.generate_request_hash( data ))
        existing_key = ( IdempotencyKey.objects.filter(user=user, key=idempotency_key) .first())

        if existing_key:
            if ( existing_key.request_hash != request_hash ):

                raise ValidationError({
                    "detail":(
                        "Request payload "
                        "changed for same "
                        "idempotency key"
                    )
                })

            return ( existing_key.response )

        cart = (Cart.objects.select_for_update().get(user=user))

        cart_items = list( cart.items.select_related("product"))

        if not cart_items:
            raise ValidationError({
                "detail": "Cart is empty"
            })

        cart_total = Decimal("0")

        for item in cart_items:

            cart_total += (item.quantity * item.unit_price_snapshot)

        payment = ( data["payment"] )

        CheckoutService.simulate_payment(
            payment=payment,
            cart_total=cart_total
        )

        try:
           address = Address.objects.get(id=data["address_id"], user=user)
        except Address.DoesNotExist:
           raise ValidationError({"detail": "Invalid or missing address."})

        buyer_wallet = (
            CheckoutService.get_or_create_wallet( user.id)
        )

        # simulated card topup

        CheckoutService.create_wallet_transaction(
            wallet= buyer_wallet,
            transaction_type="topup_simulated",
            direction="credit",
            amount=cart_total,
            reference=f"TOPUP_{user.id}",
            related_object_type="order",
            related_object_id=0
        )

        card_number = (
            payment["card_number" ] )

        order = (
            Order.objects.create(
                buyer=user,
                total=cart_total,
                status= "paid",
                shipping_address={
                    "line": address.line,
                    "line2":address.line2,
                    "city":address.city,
                    "region":address.region,
                    "postal_code": ( address.postal_code),
                    "country": address.country,
                },

                card_brand=(
                    CheckoutService.get_card_brand(card_number)
                ),

                card_last4=(card_number[-4:]),

                idempotency_key = idempotency_key
            )
        )
        
        Notification.objects.create(
            user=user,
            type_noti="order_placed",
            payload={ 
                     "message":(f"Order #{order.id} "f"placed successfully"),       
                     "order_id":order.id,
                     "status":order.status,
                     "total":str(order.total)
            }
        )

        # buyer debit

        CheckoutService.create_wallet_transaction(
            wallet = buyer_wallet,
            transaction_type="order_payment",
            direction="debit",
            amount= cart_total,
            reference = f"ORDER_{order.id}",
            related_object_type= "order",
            related_object_id = order.id
        )

        seller_map = {}
        for item in cart_items:
            seller_id = (item.product.seller_id)
            seller_map.setdefault(seller_id,[]).append(item)

        for (seller_id, seller_items) in (seller_map.items()):
            subtotal = ( Decimal("0"))

            suborder = (
                SubOrder.objects.create(
                    order=order,
                    seller_id=seller_id,
                    subtotal=0,
                    status="paid",
                    shipping="standard"
                )
            )

            for item in seller_items:
                line_total = (item.quantity * item.unit_price_snapshot)
                OrderItem.objects.create(
                    suborder=suborder,
                    product=item.product,
                    product_title=item.product.title,
                    product_sku=item.product.sku,
                    product_price=item.unit_price_snapshot,
                    quantity=item.quantity,
                    line_total=line_total
                )

                subtotal += (line_total)

            suborder.subtotal = ( subtotal)

            suborder.save()
            
            Notification.objects.create(
                user_id=seller_id,
                type_noti="new_order",
                payload={
                    "message":( f"You received a new "  f"order #{suborder.id}"),
                    "suborder_id":suborder.id,
                    "subtotal":str(subtotal),
                    "buyer":user.username
                    }
                )

            seller_wallet = (
                CheckoutService.get_or_create_wallet( seller_id )
            )

            CheckoutService.create_wallet_transaction(
                wallet=seller_wallet,
                transaction_type="sale_proceeds",
                direction="credit",
                amount=subtotal,
                reference=(f"SALE_" f"{suborder.id}"),
                related_object_type="suborder",
                related_object_id=suborder.id
            )

        cart.items.all().delete()

        response_data = {
            "message":"Checkout successful",
            "order_id": order.id,
            "status":order.status,
            "total":str(order.total)
        }

        IdempotencyKey.objects.create(
            user=user,
            key=idempotency_key,
            request_hash=request_hash,
            response= response_data
        )
        return response_data
    


# SUCCESS PAYLOAD

{
    "address_id": 1,
    "payment": {
        "card_number":
        "4242424242424242",

        "holder_name":
        "Ahsan Iqbal",

        "expiry_month":
        12,

        "expiry_year":
        2030,

        "cvv":
        "123"
    }
}
# SUCCESS RESPONSE
{
    "message":
    "Checkout successful",

    "order_id":
    12,

    "status":
    "paid",

    "total":
    "450.00"
}
# FAIL CARD
"4242424242420000"

{
    "code":"do_not_honor"
}
# FAIL FUNDS

"4242424242420001"
{
    "code":"insufficient_funds"
}