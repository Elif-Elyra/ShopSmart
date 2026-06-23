from django.contrib import admin
from .models import User, Address, Wallet, WalletTransaction, BankAccount, Withdrawal

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "fullname", "is_seller", "created_at")
    search_fields = ("email", "fullname")




@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'city', 'country', 'is_default')
    list_filter = ('city', 'country', 'is_default')
    search_fields = ('user__email', 'city', 'postal_code') # Changed username to email to match your User model



@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "account_number", "balance", "currency")
    readonly_fields = ("balance",) # Good practice to keep balance read-only in admin



@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin): # Corrected inheritance
    list_display = ('wallet', 'transaction_type', 'direction', 'amount', 'created_at')
    list_filter = ('transaction_type', 'direction')



@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin): # Corrected inheritance
    list_display = ('user', 'bank_name', 'holder_name', 'last4', 'is_primary')



@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("user", "bank_account", "amount", "status", "created_at")
    list_filter = ("status",)