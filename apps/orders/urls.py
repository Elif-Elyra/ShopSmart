from django.urls import path, include
from .views  import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    r"reviews",
    ReviewViewSet,
    basename="reviews"
)

urlpatterns = [
    path("", include(router.urls)),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("orders/", OrderListView.as_view() ),
    path( "orders/<int:id>/", OrderDetailView.as_view() ),
    path("orders/<int:id>/cancel/", CancelOrderView.as_view() ),
    path("seller/orders/", SellerOrderListView.as_view() ),
    path("seller/orders/<int:id>/ship/", ShipOrderView.as_view()),
    path("seller/orders/<int:id>/deliver/",ConfirmDeliveryView.as_view(), name="confirm-delivery"),
    path("notifications/", NotificationListView.as_view() ),

]
