# ============================================================
# users/views.py
# User authentication se related saari APIs yahan hain.
# OTP sending ab RegisterView mein nahi — signal handle karta hai.
# ============================================================

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.db import transaction
import requests
from django.db.models import Q
from .models import *
from .serializer import *
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from django.core.paginator import Paginator
from apps.orders.services import CheckoutService
import secrets
import string


# ============================================================
# OTP generate karo — 6 digit secure number
# secrets library use karte hain kyunki random() predictable hota hai
# ============================================================

def generate_otp():
    return ''.join(secrets.choice(string.digits) for _ in range(6))


# ============================================================
# SendGrid se OTP email bhejo
# Yeh function external API (SendGrid) se baat karta hai
# ============================================================

def send_otp_email(email, otp):
    url = "https://api.sendgrid.com/v3/mail/send"

    payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": "Your OTP Code"
        }],
        "from": {
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "content": [{
            "type": "text/html",
            "value": f"Your OTP is: {otp}"
        }]
    }

    headers = {
        "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return {"success": True, "status": response.status_code}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout"}


# ============================================================
# REGISTER
# User save hone ke baad signal automatically OTP bhejega.
# Yahan ab manually OTP create ya email send nahi karna.
# ============================================================

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        with transaction.atomic():
            user = serializer.save()
            user.is_active = False
            user.save()
            # ✅ OTP aur email — signal/signals.py handle karega

        return Response({"detail": "User created. OTP sent."}, status=201)


# ============================================================
# VERIFY OTP
# User ne jo OTP enter kiya hai woh check karo
# ============================================================

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        # OTP database mein dhundo
        obj = OTP.objects.filter(
            email=email,
            code=otp,
            is_used=False
        ).first()

        if not obj:
            return Response({"detail": "Invalid OTP"}, status=400)

        # OTP expired toh nahi?
        if obj.is_expired:
            return Response({"detail": "OTP expired"}, status=400)

        # User ko active karo
        user = User.objects.get(email=email)
        user.is_active = True
        user.is_email_verified = True
        user.save()

        # OTP use ho gaya — mark karo
        obj.is_used = True
        obj.save()

        return Response({"detail": "Email verified"})


# ============================================================
# RESEND OTP
# Purana OTP delete karo, naya bhejo
# ============================================================

class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"detail": "User not found"}, status=404)

        # Purane saare OTPs delete karo
        OTP.objects.filter(email=email).delete()

        # Naya OTP banao aur bhejo
        otp = generate_otp()
        OTP.objects.create(email=email, code=otp)
        send_otp_email(email, otp)

        return Response({"detail": "OTP resent"})


# ============================================================
# RESET PASSWORD
# OTP verify karke password change karo
# ============================================================

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        obj = OTP.objects.filter(
            email=email,
            code=otp,
            is_used=False
        ).first()

        if not obj:
            return Response({"detail": "Invalid OTP"}, status=400)

        # OTP expire check
        if obj.is_expired:
            obj.delete()
            return Response({"detail": "OTP expired"}, status=400)

        # Password hash karke save karo
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        obj.is_used = True
        obj.save()

        return Response({"detail": "Password reset successful"})


# ============================================================
# LOGIN
# Email ya username se login, JWT token return karo
# ============================================================

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"detail": "missing credentials"}, status=400)

        try:
            # Email ya username dono se login ho sake
            user = User.objects.get(
                Q(email=identifier) | Q(username=identifier)
            )
        except User.DoesNotExist:
            return Response({"detail": "invalid credentials"}, status=401)

        # Email verified nahi toh login band
        if not user.is_active:
            return Response({"detail": "email not verified"}, status=403)

        # Password galat hai
        if not user.check_password(password):
            return Response({"detail": "invalid credentials"}, status=401)

        # JWT tokens banao
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=200)


# ============================================================
# LOGOUT
# Refresh token ko blacklist karo — dobara use na ho sake
# ============================================================

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"detail": "refresh token required"}, status=400)

            # Token validate karo aur blacklist mein daal do
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "logout successful"}, status=200)

        except TokenError:
            return Response({"detail": "Invalid or expired token"}, status=400)
        except Exception:
            return Response({"detail": "Something went wrong"}, status=500)


# ============================================================
# PROFILE
# Logged in user ka profile return karo
# ============================================================

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ============================================================
# BECOME SELLER
# Normal user ko seller banana
# ============================================================

class BecomeSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Pehle se seller hai toh dobara mat banao
        if user.is_seller:
            return Response({"message": "Already seller"})

        user.is_seller = True
        user.save()

        return Response({"message": "Seller activated"})


# ============================================================
# ADDRESS VIEWSET
# User apne addresses manage kar sake
# ============================================================

class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Sirf logged in user ke addresses
        return Address.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        # Address save karte waqt user automatically attach ho
        serializer.save(user=self.request.user)


# ============================================================
# WALLET
# User ka wallet balance dekho
# ============================================================

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Wallet dhundo ya banao
        wallet = CheckoutService.get_or_create_wallet(request.user.id)

        # Latest balance sync karo
        wallet.refresh_balance()

        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# WALLET TRANSACTIONS
# Wallet ki transaction history — paginated
# ============================================================

class WalletTransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = CheckoutService.get_or_create_wallet(request.user.id)

        transactions = WalletTransaction.objects.filter(
            wallet=wallet
        ).order_by("-created_at")

        page_number = request.GET.get("page", 1)
        paginator = Paginator(transactions, 10)  # 10 per page
        page = paginator.get_page(page_number)

        serializer = WalletTransactionSerializer(page, many=True)

        return Response({
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "results": serializer.data
        }, status=status.HTTP_200_OK)


# ============================================================
# BANK ACCOUNT VIEWSET
# User ke bank accounts manage karo
# ============================================================

class BankAccountViewSet(ModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        is_primary = serializer.validated_data.get("is_primary", False)

        # Agar naya account primary hai toh purane sab se primary hata do
        if is_primary:
            BankAccount.objects.filter(
                user=self.request.user
            ).update(is_primary=False)

        serializer.save(user=self.request.user)


# ============================================================
# WITHDRAWAL VIEWSET
# Seller apna paisa withdraw kare
# ============================================================

class WithdrawalViewSet(ModelViewSet):
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(
            user=self.request.user
        ).select_related("bank_account").order_by("-created_at")

    def perform_create(self, serializer):
        wallet = CheckoutService.get_or_create_wallet(self.request.user.id)
        amount = serializer.validated_data["amount"]

        # Latest balance check karo
        wallet.refresh_balance()

        # Balance kam hai toh rok do
        if wallet.balance < amount:
            raise ValidationError({"detail": "Insufficient wallet balance"})

        withdrawal = serializer.save(user=self.request.user)

        # Withdrawal ka amount hold karo (debit)
        CheckoutService.create_wallet_transaction(
            wallet=wallet,
            transaction_type="withdrawal_hold",
            direction="debit",
            amount=amount,
            reference=f"WITHDRAWAL_{withdrawal.id}",
            related_object_type="withdrawal",
            related_object_id=withdrawal.id
        )