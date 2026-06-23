from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "username", "password", "fullname"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username") or validated_data["email"].split("@")[0],
            password=validated_data["password"],
            fullname=validated_data["fullname"],
            is_active=False
        )
        return user



class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_seller"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'fullname',
            'phone',
            'is_seller',
            'is_email_verified',
            'email_otp',
            'otp_created_at',
            'created_at',
        ]
        read_only_fields = ['id', 'is_email_verified', 'otp_created_at', 'created_at']
        

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

        fields = [
            "id",
            "label",
            "line",
            "line2",
            "city",
            "postal_code",
            "country",
            "is_default",
        ]

        read_only_fields = [
            "country"
        ]
                               
        
class WalletTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletTransaction

        fields = [
            "id",
            "transaction_type",
            "direction",
            "amount",
            "reference",
            "related_object_type",
            "related_object_id",
            "created_at"
        ] 
        
          
        
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "wallet",
            "transaction_type",
            "direction",
            "amount",
            "reference",
            "created_at",
            "updated_at"
        ]
        
        
class BankAccountSerializer(serializers.ModelSerializer):

    account_number = serializers.CharField(write_only=True, required=True)
    user = serializers.CharField( source="User.fullname", read_only=True )

    class Meta:
        model = BankAccount
        fields = [
            "id",
            "user",
            "holder_name",
            "bank_name",
            "country",
            "account_number",
            "last4",
            "routing_code",
            "is_primary",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "user",
            "last4",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        account_number = validated_data.pop("account_number")
        validated_data["last4"] = account_number[-4:]
        # Encrypt here
        validated_data["account_number_encrypted"] = account_number

        return BankAccount.objects.create(**validated_data)
        

class WithdrawalSerializer(serializers.ModelSerializer):
    user = serializers.CharField( source="User.fullname", read_only=True )
    
    class Meta:
        model = Withdrawal
        fields = [
            "id",
            "user",
            "bank_account",
            "amount",
            "status",
            "created_at",
            "updated_at"
        ]
        
        
class WalletSerializer(serializers.ModelSerializer):

    available_balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = [
            "account_number",
            "balance",
            "available_balance",
            "currency",
            "created_at"
        ]

    def get_available_balance(
        self,
        obj
    ):

        withdrawal_hold = (
            obj.transactions.filter( transaction_type= "withdrawal_hold" ).aggregate(total=models.Sum("amount") )["total"]
            or 0
        )

        return ( obj.balance - withdrawal_hold )