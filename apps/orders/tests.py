# ============================================================
# apps/orders/tests.py
# Orders app ki saari APIs ka test file.
# Order list/detail, cancel, ship, deliver, checkout,
# notifications, reviews — sab cover hai.
# Run karo: python manage.py test apps.orders.tests
# ============================================================

from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from apps.account.models import User, Address, Wallet
from apps.catalog.models import Category, Product, Cart, CartItem
from apps.orders.models import Order, SubOrder, OrderItem, Notification, Review, IdempotencyKey
from apps.orders.services import CheckoutService


# ============================================================
# HELPER FUNCTIONS — baar baar same data banana avoid karo
# ============================================================

def make_user(email="buyer@mail.com", password="Test@1234", is_seller=False):
    return User.objects.create_user(
        email=email,
        password=password,
        username=email.split("@")[0],
        fullname="Test User",
        is_seller=is_seller,
    )


def make_seller(email="seller@mail.com"):
    return make_user(email=email, is_seller=True)


def make_category(name="Electronics"):
    category, _ = Category.objects.get_or_create(
        slug=name.lower().replace(" ", "-"),
        defaults={
            "name": name,
        },
    )
    return category


def make_product(seller, category=None, title="Test Product", price="500.00",
                  stock=10, sku=None):
    if category is None:
        category = make_category()
    if sku is None:
        sku = f"SKU-{title.lower().replace(' ', '-')}"
    return Product.objects.create(
        seller=seller,
        category=category,
        title=title,
        slug=title.lower().replace(" ", "-"),
        description="A nice product",
        price=Decimal(price),
        stock=stock,
        sku=sku,
        condition="new",
        status="active",
    )


def make_address(user):
    return Address.objects.create(
        user=user,
        line="123 Main St",
        city="Lahore",
        postal_code="54000",
        country="Pakistan",
    )


def make_order_with_suborder(buyer, seller, product, quantity=1,
                              order_status="paid", suborder_status="paid"):
    """
    Ek complete Order + SubOrder + OrderItem banao test ke liye,
    bina CheckoutService chalaye (fast + isolated).
    """
    order = Order.objects.create(
        buyer=buyer,
        total=product.price * quantity,
        status=order_status,
        shipping_address={"line": "123 Main St", "city": "Lahore"},
        idempotency_key=f"test-key-{Order.objects.count()}",
    )
    suborder = SubOrder.objects.create(
        order=order,
        seller=seller,
        subtotal=product.price * quantity,
        status=suborder_status,
    )
    OrderItem.objects.create(
        suborder=suborder,
        product=product,
        product_title=product.title,
        product_sku=product.sku,
        product_price=product.price,
        quantity=quantity,
        line_total=product.price * quantity,
    )
    return order, suborder


VALID_PAYMENT = {
    "card_number": "4242424242424242",
    "holder_name": "Ahsan Iqbal",
    "expiry_month": 12,
    "expiry_year": 2030,
    "cvv": "123",
}


# ============================================================
# ORDER LIST & DETAIL TESTS
# ============================================================

class OrderListDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller)
        self.order, self.suborder = make_order_with_suborder(self.buyer, self.seller, self.product)
        self.client.force_authenticate(user=self.buyer)

    def test_buyer_can_list_own_orders(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_buyer_cannot_see_other_buyers_orders(self):
        other_buyer = make_user(email="other@mail.com")
        make_order_with_suborder(other_buyer, self.seller, self.product)
        response = self.client.get("/api/orders/")
        self.assertEqual(len(response.data), 1)

    def test_order_detail_returns_correct_order(self):
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)

    def test_order_detail_wrong_id_returns_404(self):
        response = self.client.get("/api/orders/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_of_other_buyer_returns_404(self):
        other_buyer = make_user(email="intruder@mail.com")
        self.client.force_authenticate(user=other_buyer)
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# CANCEL ORDER TESTS
# ============================================================

class CancelOrderTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller)

    def test_pending_payment_order_can_be_cancelled(self):
        order, _ = make_order_with_suborder(
            self.buyer, self.seller, self.product,
            order_status="pending_payment", suborder_status="pending_payment",
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(f"/api/orders/{order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "cancelled")

    def test_paid_order_can_be_cancelled(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product,
            order_status="paid", suborder_status="paid",
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(f"/api/orders/{order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        suborder.refresh_from_db()
        self.assertEqual(suborder.status, "cancelled")

    def test_shipped_order_cannot_be_cancelled(self):
        order, _ = make_order_with_suborder(
            self.buyer, self.seller, self.product,
            order_status="shipped", suborder_status="shipped",
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(f"/api/orders/{order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.status, "shipped")

    def test_other_buyer_cannot_cancel_order(self):
        order, _ = make_order_with_suborder(self.buyer, self.seller, self.product)
        other = make_user(email="intruder@mail.com")
        self.client.force_authenticate(user=other)
        response = self.client.post(f"/api/orders/{order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_order_returns_404(self):
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post("/api/orders/9999/cancel/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_cannot_cancel(self):
        order, _ = make_order_with_suborder(self.buyer, self.seller, self.product)
        response = self.client.post(f"/api/orders/{order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# SELLER ORDER LIST TESTS
# ============================================================

class SellerOrderListTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller)

    def test_seller_sees_own_suborders(self):
        make_order_with_suborder(self.buyer, self.seller, self.product)
        self.client.force_authenticate(user=self.seller)
        response = self.client.get("/api/seller/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_seller_does_not_see_other_sellers_suborders(self):
        other_seller = make_seller(email="other_seller@mail.com")
        other_product = make_product(other_seller, title="Other Product", sku="SKU-OTHER")
        make_order_with_suborder(self.buyer, other_seller, other_product)
        self.client.force_authenticate(user=self.seller)
        response = self.client.get("/api/seller/orders/")
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated_cannot_list(self):
        response = self.client.get("/api/seller/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# SHIP ORDER TESTS
# ============================================================

class ShipOrderTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller)

    def test_seller_can_ship_paid_order(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="paid"
        )
        self.client.force_authenticate(user=self.seller)
        response = self.client.post(
            f"/api/seller/orders/{suborder.id}/ship/",
            {"tracking_code": "TRK123456"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        suborder.refresh_from_db()
        self.assertEqual(suborder.status, "shipped")
        self.assertEqual(suborder.tracking_code, "TRK123456")
        self.assertIsNotNone(suborder.shipped_at)

    def test_cannot_ship_non_paid_order(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="pending_payment"
        )
        self.client.force_authenticate(user=self.seller)
        response = self.client.post(
            f"/api/seller/orders/{suborder.id}/ship/",
            {"tracking_code": "TRK000"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_other_seller_cannot_ship(self):
        order, suborder = make_order_with_suborder(self.buyer, self.seller, self.product)
        other_seller = make_seller(email="faker@mail.com")
        self.client.force_authenticate(user=other_seller)
        response = self.client.post(
            f"/api/seller/orders/{suborder.id}/ship/",
            {"tracking_code": "TRK999"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_shipping_notifies_buyer_via_signal(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="paid"
        )
        self.client.force_authenticate(user=self.seller)
        self.client.post(
            f"/api/seller/orders/{suborder.id}/ship/",
            {"tracking_code": "TRK777"},
        )
        notification = Notification.objects.filter(
            user=self.buyer, type_noti="order_shipped"
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.payload["suborder_id"], suborder.id)
        self.assertEqual(notification.payload["tracking_code"], "TRK777")


# ============================================================
# CONFIRM DELIVERY TESTS
# ============================================================

class ConfirmDeliveryTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller)

    def test_buyer_can_confirm_shipped_order(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="shipped"
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(f"/api/seller/orders/{suborder.id}/deliver/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        suborder.refresh_from_db()
        self.assertEqual(suborder.status, "delivered")
        self.assertIsNotNone(suborder.delivered_at)

    def test_cannot_confirm_non_shipped_order(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="paid"
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(f"/api/seller/orders/{suborder.id}/deliver/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_confirm_returns_400(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="shipped"
        )
        suborder.delivered_at = timezone.now()
        suborder.save()
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post(f"/api/seller/orders/{suborder.id}/deliver/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_other_buyer_cannot_confirm(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="shipped"
        )
        other = make_user(email="intruder2@mail.com")
        self.client.force_authenticate(user=other)
        response = self.client.post(f"/api/seller/orders/{suborder.id}/deliver/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_confirm_delivery_notifies_seller_via_signal(self):
        order, suborder = make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="shipped"
        )
        self.client.force_authenticate(user=self.buyer)
        self.client.post(f"/api/seller/orders/{suborder.id}/deliver/")
        notification = Notification.objects.filter(
            user=self.seller, type_noti="delivery_confirmed"
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.payload["suborder_id"], suborder.id)


# ============================================================
# NOTIFICATION LIST TESTS
# ============================================================

class NotificationListTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.client.force_authenticate(user=self.user)

    def test_notification_list_returns_correct_counts(self):
        Notification.objects.create(
            user=self.user, type_noti="order_shipped", payload={"message": "shipped"}
        )
        Notification.objects.create(
            user=self.user, type_noti="delivery_confirmed",
            payload={"message": "delivered"}, is_read=True,
        )
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["unread"], 1)
        self.assertEqual(len(response.data["results"]), 2)

    def test_other_users_notifications_not_visible(self):
        other = make_user(email="nosy@mail.com")
        Notification.objects.create(user=other, type_noti="order_shipped", payload={})
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.data["count"], 0)

    def test_unauthenticated_cannot_list_notifications(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# CHECKOUT VIEW TESTS (service mocked — view-level behavior only)
# ============================================================

class CheckoutViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.client.force_authenticate(user=self.buyer)

    def test_checkout_requires_idempotency_key_header(self):
        response = self.client.post("/api/checkout/", {
            "address_id": 1,
            "payment": VALID_PAYMENT,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Idempotency-Key", response.data["detail"])

    @patch("apps.orders.views.CheckoutService.create_order")
    def test_checkout_with_key_calls_service(self, mock_create):
        mock_create.return_value = {
            "message": "Checkout successful", "order_id": 1,
            "status": "paid", "total": "500.00",
        }
        response = self.client.post(
            "/api/checkout/",
            {"address_id": 1, "payment": VALID_PAYMENT},
            format="json",
            HTTP_IDEMPOTENCY_KEY="unique-key-123",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_create.assert_called_once()
        self.assertEqual(response.data["order_id"], 1)

    def test_checkout_invalid_payload_returns_400(self):
        response = self.client.post(
            "/api/checkout/",
            {"address_id": "not-an-int"},
            format="json",
            HTTP_IDEMPOTENCY_KEY="key-1",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_cannot_checkout(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            "/api/checkout/",
            {"address_id": 1, "payment": VALID_PAYMENT},
            format="json",
            HTTP_IDEMPOTENCY_KEY="key-2",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# CHECKOUT SERVICE TESTS (full integration, real DB flow)
# ============================================================

class CheckoutServiceTests(TestCase):

    def setUp(self):
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller, price="500.00", stock=5)
        self.address = make_address(self.buyer)
        cart = Cart.objects.create(user=self.buyer)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.cart = cart

    def test_successful_checkout_creates_order_and_suborder(self):
        result = CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-success-1",
        )
        self.assertEqual(result["status"], "paid")
        order = Order.objects.get(id=result["order_id"])
        self.assertEqual(order.total, Decimal("1000.00"))
        self.assertEqual(order.buyer, self.buyer)
        suborder = order.suborders.first()
        self.assertEqual(suborder.seller, self.seller)
        self.assertEqual(suborder.subtotal, Decimal("1000.00"))

    def test_checkout_empties_cart(self):
        CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-success-2",
        )
        self.assertEqual(self.cart.items.count(), 0)

    def test_checkout_creates_notifications_for_buyer_and_seller(self):
        CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-success-3",
        )
        self.assertTrue(
            Notification.objects.filter(user=self.buyer, type_noti="order_placed").exists()
        )
        self.assertTrue(
            Notification.objects.filter(user=self.seller, type_noti="new_order").exists()
        )

    def test_checkout_credits_seller_wallet(self):
        CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-success-4",
        )
        seller_wallet = Wallet.objects.get(user=self.seller)
        self.assertEqual(seller_wallet.balance, Decimal("1000.00"))

    def test_checkout_empty_cart_raises_error(self):
        self.cart.items.all().delete()
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": self.address.id, "payment": VALID_PAYMENT},
                idempotency_key="key-empty",
            )

    def test_checkout_invalid_address_raises_error(self):
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": 9999, "payment": VALID_PAYMENT},
                idempotency_key="key-bad-address",
            )

    def test_checkout_declined_card_raises_error(self):
        declined_payment = dict(VALID_PAYMENT, card_number="4242424242420000")
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": self.address.id, "payment": declined_payment},
                idempotency_key="key-declined",
            )

    def test_checkout_insufficient_funds_card_raises_error(self):
        declined_payment = dict(VALID_PAYMENT, card_number="4242424242420001")
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": self.address.id, "payment": declined_payment},
                idempotency_key="key-insufficient",
            )

    def test_repeated_idempotency_key_returns_same_response(self):
        first = CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-repeat",
        )
        second = CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-repeat",
        )
        self.assertEqual(first, second)
        self.assertEqual(Order.objects.count(), 1)

    def test_same_key_different_payload_raises_error(self):
        CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-conflict",
        )
        # Hash mismatch is detected before the (now-empty) cart is touched
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": 9999, "payment": VALID_PAYMENT},
                idempotency_key="key-conflict",
            )

    def test_items_from_multiple_sellers_create_multiple_suborders(self):
        seller2 = make_seller(email="seller2@mail.com")
        product2 = make_product(seller2, title="Other Item", price="100.00",
                                 stock=5, sku="SKU-OTHER-ITEM")
        CartItem.objects.create(cart=self.cart, product=product2, quantity=1)

        result = CheckoutService.create_order(
            user=self.buyer,
            data={"address_id": self.address.id, "payment": VALID_PAYMENT},
            idempotency_key="key-multi-seller",
        )
        order = Order.objects.get(id=result["order_id"])
        self.assertEqual(order.suborders.count(), 2)
        self.assertEqual(order.total, Decimal("1100.00"))

    def test_luhn_invalid_card_raises_error(self):
        bad_card_payment = dict(VALID_PAYMENT, card_number="1234567890123456")
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": self.address.id, "payment": bad_card_payment},
                idempotency_key="key-luhn",
            )

    def test_expired_card_raises_error(self):
        expired_payment = dict(VALID_PAYMENT, expiry_year=2020)
        with self.assertRaises(Exception):
            CheckoutService.create_order(
                user=self.buyer,
                data={"address_id": self.address.id, "payment": expired_payment},
                idempotency_key="key-expired",
            )


class CheckoutServiceHelperTests(TestCase):
    """Unit tests for CheckoutService static helper methods."""

    def test_luhn_check_valid_number(self):
        self.assertTrue(CheckoutService.luhn_check("4242424242424242"))

    def test_luhn_check_invalid_number(self):
        self.assertFalse(CheckoutService.luhn_check("1234567890123456"))

    def test_get_card_brand_visa(self):
        self.assertEqual(CheckoutService.get_card_brand("4242424242424242"), "Visa")

    def test_get_card_brand_mastercard(self):
        self.assertEqual(CheckoutService.get_card_brand("5242424242424242"), "Mastercard")

    def test_get_card_brand_unknown(self):
        self.assertEqual(CheckoutService.get_card_brand("9999999999999999"), "Unknown")

    def test_generate_account_number_is_unique_and_numeric(self):
        acc_number = CheckoutService.generate_account_number()
        self.assertEqual(len(acc_number), 12)
        self.assertTrue(acc_number.isdigit())

    def test_generate_request_hash_is_deterministic(self):
        data1 = {"a": 1, "b": 2}
        data2 = {"b": 2, "a": 1}
        self.assertEqual(
            CheckoutService.generate_request_hash(data1),
            CheckoutService.generate_request_hash(data2),
        )


# ============================================================
# REVIEW TESTS
# ============================================================

class ReviewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.product = make_product(self.seller)

    def test_delivered_buyer_can_leave_review(self):
        make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="delivered"
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post("/api/reviews/", {
            "product": self.product.id,
            "rating": 5,
            "comment": "Great product!",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Review.objects.filter(user=self.buyer, product=self.product).exists()
        )

    def test_non_delivered_buyer_cannot_review(self):
        make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="paid"
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post("/api/reviews/", {
            "product": self.product.id,
            "rating": 4,
            "comment": "Trying to review early",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buyer_without_order_cannot_review(self):
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post("/api/reviews/", {
            "product": self.product.id,
            "rating": 3,
            "comment": "Never bought this",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_review_for_same_product_rejected(self):
        make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="delivered"
        )
        Review.objects.create(
            user=self.buyer, product=self.product, rating=5, comment="First review"
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post("/api/reviews/", {
            "product": self.product.id,
            "rating": 2,
            "comment": "Second review attempt",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_reviews_by_product(self):
        other_product = make_product(self.seller, title="Other", sku="SKU-OTHER-REVIEW")
        Review.objects.create(
            user=self.buyer, product=self.product, rating=5, comment="Nice"
        )
        Review.objects.create(
            user=self.buyer, product=other_product, rating=3, comment="Meh"
        )
        self.client.force_authenticate(user=self.buyer)
        response = self.client.get(f"/api/reviews/?product={self.product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_cannot_create_review(self):
        response = self.client.post("/api/reviews/", {
            "product": self.product.id,
            "rating": 5,
            "comment": "Anonymous review",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_rating_out_of_range_raises_db_error(self):
        # NOTE: 'rating' has no serializer-level validator, only a DB
        # CheckConstraint (1-5). An out-of-range value passes serializer
        # validation and fails at the database layer with IntegrityError,
        # not a clean 400 response. This test documents that current
        # behavior; consider adding a validate_rating() to the serializer.
        from django.db import IntegrityError

        make_order_with_suborder(
            self.buyer, self.seller, self.product, suborder_status="delivered"
        )
        self.client.force_authenticate(user=self.buyer)
        with self.assertRaises(IntegrityError):
            self.client.post("/api/reviews/", {
                "product": self.product.id,
                "rating": 10,
                "comment": "Too high a rating",
            })