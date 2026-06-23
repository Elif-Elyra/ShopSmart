from django.urls import path, include
from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    CategoriesView,
    PublicProductView,
    SellerProductView,
    CartItemViewSet,
    CartView,
    CategoryProductsView,
    CategoryClickAPIView
)

router = DefaultRouter()

# =========================================================
# PUBLIC PRODUCTS
# =========================================================
router.register(
    r"products",
    PublicProductView,
    basename="public-products"
)

# =========================================================
# SELLER PRODUCTS
# =========================================================
router.register(
    r"seller/products",
    SellerProductView,
    basename="seller-products"
)

# =========================================================
# CART ITEMS
# =========================================================
router.register(
    r"cart/items",
    CartItemViewSet,
    basename="cart-items"
)

urlpatterns = [

    # Categories
    path(
        "categories/",
        CategoriesView.as_view(),
        name="categories"
    ),

    path(
        "categories/<int:pk>/products/",
        CategoryProductsView.as_view(),
        name="category-products"
    ),

    # Analytics
    path(
        "analytics/category-click/",
        CategoryClickAPIView.as_view(),
        name="category-click"
    ),

    # Cart
    path(
        "cart/",
        CartView.as_view(),
        name="cart"
    ),

    # Router APIs
    path(
        "",
        include(router.urls)
    ),
]