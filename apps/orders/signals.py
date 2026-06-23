# ============================================================
# signals.py
# Yeh file Django Signals handle karti hai.
# Signal matlab — jab koi event ho (jaise order ship ho),
# toh automatically kuch action trigger ho jaye.
# Hume manually har jagah code likhne ki zaroorat nahi.
# ============================================================

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SubOrder, Notification, Order




@receiver(post_save, sender=SubOrder)
def suborder_status_notification(sender, instance, **kwargs):

    # Jab seller ne order ship kiya
    if instance.status == "shipped":
        Notification.objects.create(
            user=instance.order.buyer,        # Buyer ko notify karo
            type_noti="order_shipped",
            payload={
                "message": f"Your order #{instance.id} has been shipped",
                "tracking_code": instance.tracking_code,
                "suborder_id": instance.id
            }
        )

    # Jab buyer ne delivery confirm ki
    elif instance.status == "delivered":
        Notification.objects.create(
            user=instance.seller,             # Seller ko notify karo
            type_noti="delivery_confirmed",
            payload={
                "message": f"Buyer confirmed delivery for order #{instance.id}",
                "suborder_id": instance.id
            }
        )


