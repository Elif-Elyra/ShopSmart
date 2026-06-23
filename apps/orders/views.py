# ============================================================
# orders/views.py
# Yahan se sirf order ka logic hai.
# Notifications ab signal handle karta hai — yahan se hata di gayi hain.
# ============================================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import CheckoutService
from .serializers import *
from .models import Order, SubOrder, Notification
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError


# ============================================================
# Buyer ke saare orders list karo
# ============================================================

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(buyer=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# ============================================================
# Ek specific order ki detail
# ============================================================

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            order = Order.objects.get(id=id, buyer=request.user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ============================================================
# Order cancel karo
# Sirf "pending_payment" ya "paid" orders cancel ho sakti hain
# ============================================================

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            order = Order.objects.get(id=id, buyer=request.user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        allowed_statuses = ["pending_payment", "paid"]
        suborders = order.suborders.all()

        # Har suborder check karo — agar koi cancel nahi ho sakta toh rok do
        for suborder in suborders:
            if suborder.status not in allowed_statuses:
                return Response(
                    {"detail": "Order cannot be cancelled"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Sab cancel kar do
        suborders.update(status="cancelled")
        order.status = "cancelled"
        order.save()

        return Response({"message": "Order cancelled successfully"})


# ============================================================
# Seller ke saare suborders list karo
# ============================================================

class SellerOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        suborders = SubOrder.objects.filter(seller=request.user)
        serializer = SubOrderSerializer(suborders, many=True)
        return Response(serializer.data)


# ============================================================
# Seller order ship kare
# NOTE: Notification ab yahan nahi — signal automatically bhejega
# ============================================================

class ShipOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            suborder = SubOrder.objects.get(id=id, seller=request.user)
        except SubOrder.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Sirf "paid" order ship ho sakta hai
        if suborder.status != "paid":
            return Response(
                {"detail": "Only paid orders can be shipped"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tracking_code = request.data.get("tracking_code")

        # Status update karo — signal yeh dekh ke buyer ko notify karega
        suborder.status = "shipped"
        suborder.tracking_code = tracking_code
        suborder.shipped_at = timezone.now()
        suborder.save()

        # ✅ Notification hata di — ab signal/signals.py mein handle hoti hai

        return Response({"message": "Order shipped"})


# ============================================================
# Buyer delivery confirm kare
# NOTE: Notification ab yahan nahi — signal automatically bhejega
# ============================================================

class ConfirmDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            suborder = SubOrder.objects.get(id=id, order__buyer=request.user)
        except SubOrder.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Sirf shipped order confirm ho sakta hai
        if suborder.status != "shipped":
            return Response(
                {"detail": "Only shipped orders can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Agar pehle se deliver ho chuka hai toh rok do
        if suborder.delivered_at:
            return Response(
                {"detail": "Order already delivered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Status update karo — signal yeh dekh ke seller ko notify karega
        suborder.status = "delivered"
        suborder.delivered_at = timezone.now()
        suborder.save(update_fields=["status", "delivered_at"])

        # ✅ Notification hata di — ab signal/signals.py mein handle hoti hai

        return Response(
            {"message": "Delivery confirmed successfully"},
            status=status.HTTP_200_OK
        )


# ============================================================
# Checkout — order place karo
# ============================================================

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Idempotency key — duplicate order se bachao
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return Response(
                {"detail": "Idempotency-Key required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = CheckoutService.create_order(
            user=request.user,
            data=serializer.validated_data,
            idempotency_key=idempotency_key
        )

        return Response(result)


# ============================================================
# Notifications list — user ki saari notifications
# ============================================================

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = NotificationSerializer(notifications, many=True)

        unread_count = notifications.filter(is_read=False).count()

        return Response({
            "count": notifications.count(),
            "unread": unread_count,
            "results": serializer.data
        })


# ============================================================
# Reviews — sirf delivered products ka review de sakte ho
# ============================================================

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # select_related se extra DB queries avoid hoti hain
        queryset = Review.objects.select_related("user", "product")
        product_id = self.request.query_params.get("product")

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data["product"]

        # Check karo — kya buyer ne yeh product deliver karwaya hai?
        delivered = OrderItem.objects.filter(
            suborder__order__buyer=user,
            suborder__status="delivered",
            product=product
        ).exists()

        if not delivered:
            raise ValidationError(
                {"detail": "You can review only delivered products."}
            )

        # Ek user, ek product — sirf ek hi review
        already_reviewed = Review.objects.filter(
            user=user,
            product=product
        ).exists()

        if already_reviewed:
            raise ValidationError(
                {"detail": "You have already reviewed this product."}
            )

        serializer.save(user=user)