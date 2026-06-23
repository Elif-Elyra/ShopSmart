from django.test import TestCase

# Create your tests here.
# ============================================================
# apps/catalog/tests.py
# Catalog app ki saari APIs ka test file.
# Categories, Products (public + seller), Cart, CartItem — sab cover hai.
# Run karo: python manage.py test apps.catalog.tests
# ============================================================

from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.account.models import User
from apps.catalog.models import Category, Product, ProductImage, Cart, CartItem


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


def make_category(name="Electronics", parent=None):
    return Category.objects.create(
        name=name,
        slug=name.lower().replace(" ", "-"),
        parent=parent,
    )


def make_product(seller, category=None, title="Test Product", price="500.00",
                  stock=10, status="active", sku=None):
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
        status=status,
    )


# ============================================================
# CATEGORY TESTS
# ============================================================

class CategoryListTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_anyone_can_list_categories(self):
        make_category("Electronics")
        make_category("Books")
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_category_includes_nested_children(self):
        parent = make_category("Electronics")
        make_category("Phones", parent=parent)
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parent_data = next(c for c in response.data if c["id"] == parent.id)
        self.assertEqual(len(parent_data["children"]), 1)
        self.assertEqual(parent_data["children"][0]["name"], "Phones")


class CategoryProductsViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.seller = make_seller()
        self.parent = make_category("Electronics")
        self.child = make_category("Phones", parent=self.parent)

    def test_products_under_parent_category_include_child_products(self):
        # Parent category ke andar child category ka product bhi aana chahiye
        make_product(self.seller, category=self.child, title="iPhone")
        response = self.client.get(f"/api/categories/{self.parent.id}/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "iPhone")

    def test_invalid_category_returns_404(self):
        response = self.client.get("/api/categories/9999/products/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryClickTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_category_click_tracked(self):
        category = make_category()
        response = self.client.post(
            "/api/analytics/category-click/",
            {"category_id": category.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category_id"], str(category.id))


# ============================================================
# PUBLIC PRODUCT TESTS
# ============================================================

class PublicProductViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.seller = make_seller()
        self.category = make_category()

    def test_only_active_products_are_listed(self):
        make_product(self.seller, category=self.category, title="Active Item",
                      sku="SKU-A", status="active")
        make_product(self.seller, category=self.category, title="Draft Item",
                      sku="SKU-D", status="draft")
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Active Item")

    def test_product_detail_by_slug(self):
        product = make_product(self.seller, category=self.category, title="Cool Gadget")
        response = self.client.get(f"/api/products/{product.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Cool Gadget")
        self.assertIn("average_rating", response.data)
        self.assertIn("review_count", response.data)

    def test_inactive_product_detail_not_found(self):
        product = make_product(self.seller, category=self.category, title="Hidden",
                                status="inactive")
        response = self.client.get(f"/api/products/{product.slug}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_by_title(self):
        make_product(self.seller, category=self.category, title="Red Shoes", sku="SKU-RS")
        make_product(self.seller, category=self.category, title="Blue Hat", sku="SKU-BH")
        response = self.client.get("/api/products/?search=Shoes")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Red Shoes")

    def test_filter_by_category(self):
        other_category = make_category("Books")
        make_product(self.seller, category=self.category, title="Phone", sku="SKU-P")
        make_product(self.seller, category=other_category, title="Novel", sku="SKU-N")
        response = self.client.get(f"/api/products/?category={self.category.id}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Phone")

    def test_ordering_by_price(self):
        make_product(self.seller, category=self.category, title="Cheap", price="10.00", sku="SKU-C")
        make_product(self.seller, category=self.category, title="Expensive", price="999.00", sku="SKU-E")
        response = self.client.get("/api/products/?ordering=price")
        prices = [item["price"] for item in response.data]
        self.assertEqual(prices, sorted(prices))

    def test_cannot_create_via_public_endpoint(self):
        # http_method_names = ["get"] hai, post allowed nahi
        self.client.force_authenticate(user=self.seller)
        response = self.client.post("/api/products/", {"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ============================================================
# SELLER PRODUCT TESTS
# ============================================================

class SellerProductViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.seller = make_seller()
        self.other_seller = make_seller(email="other_seller@mail.com")
        self.buyer = make_user()
        self.category = make_category()

    def test_unauthenticated_cannot_access(self):
        response = self.client.get("/api/seller/products/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_seller_cannot_access(self):
        self.client.force_authenticate(user=self.buyer)
        response = self.client.get("/api/seller/products/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_sees_only_own_products(self):
        make_product(self.seller, category=self.category, title="Mine", sku="SKU-MINE")
        make_product(self.other_seller, category=self.category, title="Not Mine", sku="SKU-NOTMINE")
        self.client.force_authenticate(user=self.seller)
        response = self.client.get("/api/seller/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Mine")

    def test_seller_can_create_product(self):
        self.client.force_authenticate(user=self.seller)
        payload = {
            "title": "New Product",
            "slug": "new-product",
            "sku": "SKU-NEW",
            "category": self.category.id,
            "price": "150.00",
            "stock": 5,
            "description": "Brand new",
        }
        response = self.client.post("/api/seller/products/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(sku="SKU-NEW")
        self.assertEqual(product.seller, self.seller)
        self.assertEqual(product.status, "active")
        self.assertEqual(product.condition, "new")

    def test_seller_cannot_edit_other_sellers_product(self):
        product = make_product(self.other_seller, category=self.category,
                                title="Their Product", sku="SKU-THEIRS")
        self.client.force_authenticate(user=self.seller)
        response = self.client.patch(
            f"/api/seller/products/{product.slug}/",
            {"title": "Hacked"},
        )
        # get_queryset is scoped to request.user, so it's invisible -> 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_seller_can_update_own_product(self):
        product = make_product(self.seller, category=self.category,
                                title="Old Title", sku="SKU-OLD")
        self.client.force_authenticate(user=self.seller)
        response = self.client.patch(
            f"/api/seller/products/{product.slug}/",
            {"title": "Updated Title"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.title, "Updated Title")

    def test_seller_can_delete_own_product(self):
        product = make_product(self.seller, category=self.category,
                                title="To Delete", sku="SKU-DEL")
        self.client.force_authenticate(user=self.seller)
        response = self.client.delete(f"/api/seller/products/{product.slug}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(sku="SKU-DEL").exists())

    def test_seller_cannot_delete_other_sellers_product(self):
        product = make_product(self.other_seller, category=self.category,
                                title="Their Product", sku="SKU-THEIRS2")
        self.client.force_authenticate(user=self.seller)
        response = self.client.delete(f"/api/seller/products/{product.slug}/")
        # not visible in get_queryset -> 404 before perform_destroy runs
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Product.objects.filter(sku="SKU-THEIRS2").exists())


# ============================================================
# CART TESTS
# ============================================================

class CartViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.category = make_category()
        self.client.force_authenticate(user=self.buyer)

    def test_unauthenticated_cannot_view_cart(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cart_creates_cart_if_missing(self):
        self.assertFalse(Cart.objects.filter(user=self.buyer).exists())
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Cart.objects.filter(user=self.buyer).exists())

    def test_cart_totals_reflect_items(self):
        product = make_product(self.seller, category=self.category,
                                title="Mug", price="20.00", sku="SKU-MUG")
        cart = Cart.objects.create(user=self.buyer)
        CartItem.objects.create(cart=cart, product=product, quantity=3)
        response = self.client.get("/api/cart/")
        self.assertEqual(response.data["total_items"], 3)
        self.assertEqual(Decimal(response.data["subtotal"]), Decimal("60.00"))


class CartItemViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.buyer = make_user()
        self.seller = make_seller()
        self.category = make_category()
        self.product = make_product(self.seller, category=self.category,
                                     title="Keyboard", price="50.00", stock=10,
                                     sku="SKU-KB")
        self.client.force_authenticate(user=self.buyer)

    def test_add_item_to_cart(self):
        response = self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 2,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get(cart__user=self.buyer, product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.unit_price_snapshot, Decimal("50.00"))

    def test_cannot_add_own_product_to_cart(self):
        own_product = make_product(self.buyer, category=self.category,
                                    title="Own Item", sku="SKU-OWN")
        # buyer behaves as seller here for this product
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post("/api/cart/items/", {
            "product": own_product.id,
            "quantity": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_add_more_than_stock(self):
        response = self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 999,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_adding_existing_item_increments_quantity(self):
        self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 2,
        })
        response = self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 3,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get(cart__user=self.buyer, product=self.product)
        self.assertEqual(cart_item.quantity, 5)

    def test_adding_existing_item_beyond_stock_fails(self):
        self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 8,
        })
        response = self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 5,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        cart_item = CartItem.objects.get(cart__user=self.buyer, product=self.product)
        self.assertEqual(cart_item.quantity, 8)  # unchanged

    def test_update_quantity_within_stock(self):
        cart = Cart.objects.create(user=self.buyer)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.patch(f"/api/cart/items/{item.id}/", {"quantity": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_update_quantity_beyond_stock_fails(self):
        cart = Cart.objects.create(user=self.buyer)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.patch(f"/api/cart/items/{item.id}/", {"quantity": 50})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_cart_item(self):
        cart = Cart.objects.create(user=self.buyer)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.delete(f"/api/cart/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Item removed")
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_user_only_sees_own_cart_items(self):
        other_buyer = make_user(email="other_buyer@mail.com")
        other_cart = Cart.objects.create(user=other_buyer)
        CartItem.objects.create(cart=other_cart, product=self.product, quantity=1)
        response = self.client.get("/api/cart/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_cannot_modify_others_cart_item(self):
        other_buyer = make_user(email="other_buyer2@mail.com")
        other_cart = Cart.objects.create(user=other_buyer)
        item = CartItem.objects.create(cart=other_cart, product=self.product, quantity=1)
        response = self.client.patch(f"/api/cart/items/{item.id}/", {"quantity": 2})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_zero_quantity_rejected_by_serializer_validation(self):
        response = self.client.post("/api/cart/items/", {
            "product": self.product.id,
            "quantity": 0,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ============================================================
# MODEL-LEVEL TESTS
# ============================================================

class ProductImageModelTests(TestCase):

    def setUp(self):
        self.seller = make_seller()
        self.category = make_category()
        self.product = make_product(self.seller, category=self.category,
                                     title="Thumbnail Test", sku="SKU-THUMB")

    def test_first_image_sets_product_thumbnail(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.assertFalse(self.product.thumbnail)
        image_file = SimpleUploadedFile(
            "test.jpg", b"fake-image-bytes", content_type="image/jpeg"
        )
        ProductImage.objects.create(
            product=self.product,
            image=image_file,
            position=0,
        )
        self.product.refresh_from_db()
        self.assertTrue(self.product.thumbnail)