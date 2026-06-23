from rest_framework import serializers
from .models import *
from datetime import date
import re

class OrderSerializer(serializers.ModelSerializer):
    
    buyer_name = serializers.CharField( source="buyer.fullname", read_only=True )

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "buyer_name",
            "total",
            "status",
            "shipping_address",
            "card_brand",
            "card_last4",
            "idempotency_key",
            "created_at",
            "updated_at"
        ]
                     
class SubOrderSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(
        source="seller.fullname",
        read_only=True
    )

    buyer_name = serializers.CharField(
        source="order.buyer.fullname",
        read_only=True
    )

    class Meta:
        
        model = SubOrder
        fields = [
            "id",
            "order",  
            "seller_name",
            "buyer_name",        
            "seller",
            "status",
            "subtotal",
            "tracking_code",
            "shipping",
        ]
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "suborder",
            "product_title",
            "product",
            "quantity",
            "line_total",
        ]    
       
        
class IdempotencyKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = IdempotencyKey
        fields = [
            "id",
            "user",
            "key",
            "request_hash",
            "response",
            "created_at",
            "updated_at"
        ]       

class PaymentSerializer(serializers.Serializer):

    card_number = serializers.CharField( min_length=13,max_length=19)
    holder_name = serializers.CharField( min_length=2,max_length=60 )
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    cvv = serializers.CharField( min_length=3, max_length=4 )

    def validate_card_number(self, value):
       sanitized = re.sub( r"\D", "", value)
       if not sanitized.isdigit():
           raise serializers.ValidationError( "Card number must contain digits only" )
       if len(sanitized) < 13 or len(sanitized) > 19:
           raise serializers.ValidationError( "Card number length invalid")      
       return sanitized

    def validate_holder_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Cardholder name required" )

        return value

    def validate_cvv(self, value):

        if not value.isdigit():
            raise serializers.ValidationError(
                "Invalid CVV"
            )
        return value

    def validate(self, attrs):

        month = attrs["expiry_month"]
        year = attrs["expiry_year"]

        if month < 1 or month > 12:
            raise serializers.ValidationError({ "expiry_month": "Invalid month" })
        today = date.today()
        
        if ( year < today.year or ( year == today.year and month < today.month )):
            raise serializers.ValidationError({ "expiry_year": "Card expired"})
        return attrs


class CheckoutSerializer(serializers.Serializer):

    address_id = serializers.IntegerField()
    payment = PaymentSerializer()
    

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification

        fields = [
            "id",
            "type_noti",
            "payload",
            "is_read",
            "created_at",
            "updated_at"
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]
        

class ReviewSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.fullname",
        read_only=True
    )

    class Meta:

        model = Review

        fields = [
            "id",
            "user",
            "user_name",
            "product",
            "rating",
            "comment",
            "created_at",
            "updated_at"
        ]

        read_only_fields = [
            "user"
        ]  
    
    