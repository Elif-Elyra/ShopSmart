from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

router = DefaultRouter()

# ----------------------------
# ROUTERS
# ----------------------------

router.register(
    r"auth/addresses",
    AddressViewSet,
    basename="addresses"
)

router.register(
    r"bank-accounts",
    BankAccountViewSet,
    basename="bank-accounts"
)

router.register(
    r"withdrawals",
    WithdrawalViewSet,
    basename="withdrawals"
)

urlpatterns = [

    # ----------------------------
    # AUTH
    # ----------------------------

    path(
        "auth/register/",
        RegisterView.as_view()
    ),

    path(
        "auth/login/",
        LoginView.as_view()
    ),

    path(
        "auth/logout/",
        LogoutView.as_view()
    ),

    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view()
    ),

    # ----------------------------
    # OTP SYSTEM
    # ----------------------------

    path(
        "auth/verify-otp/",
        VerifyOTPView.as_view()
    ),

    path(
        "auth/resend-otp/",
        ResendOTPView.as_view()
    ),

    path(
        "auth/reset-password/",
        ResetPasswordView.as_view()
    ),

    # ----------------------------
    # USER
    # ----------------------------

    path(
        "auth/profile/",
        ProfileView.as_view()
    ),

    path(
        "auth/become-seller/",
        BecomeSellerView.as_view()
    ),

    # ----------------------------
    # WALLET
    # ----------------------------

    path(
        "wallet/",
        WalletView.as_view()
    ),

    path(
        "wallet/transactions/",
        WalletTransactionListView.as_view()
    ),

    # ----------------------------
    # ROUTER URLS
    # ----------------------------

    path(
        "",
        include(router.urls)
    ),
]