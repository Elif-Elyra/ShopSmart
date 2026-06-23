from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import ( IsAuthenticated, AllowAny )
from rest_framework.exceptions import PermissionDenied
from .models import Product, Category, ProductImage, Cart, CartItem
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    CartItemSerializer,
    CartSerializer   
)
from rest_framework import status
from rest_framework.response import  Response
from .services import add_to_cart
from .permissions import ( IsSeller, IsOwnerOrReadOnly )
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# =========================================================
# Categories
# =========================================================

class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


def get_category_tree_ids(category): # it is is used to separate the nested ids or catagories
    ids = []
    queue = [category]
    while queue:
        current = queue.pop(0) # remove 0 ind, insert in current 
        ids.append(current.id)
        children = list(current.children.all()) #query which is used to check child of current variable
        queue.extend(children) # add in queue
    return ids


class CategoryProductsView(APIView): # product by the category
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category_ids = get_category_tree_ids(category)
            products = Product.objects.filter(category_id__in=category_ids)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)


class CategoryClickAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        category_id = request.data.get("category_id")

        return Response({
            "message": "Category click tracked",
            "category_id": category_id
        })

# =========================================================
# Public Products API
# =========================================================

class PublicProductView(ModelViewSet):
    """
    Public products API.
    Only active products are visible.
    Read only access.
    """

    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    
    filterset_fields = ["category"]
    # SEARCH FILTER
    search_fields = [
        "title",
        "description",
        "category__name",
    ]
    # SORTING
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Product.objects.filter(status="active").select_related("category", "seller").prefetch_related("images", "reviews", "reviews__user")
    
    
    


# =========================================================
# Seller Dashboard Products API
# =========================================================

class SellerProductView(ModelViewSet):
    """
    Seller dashboard API.
    Seller can manage only their own products.
    """

    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
        IsSeller,
        IsOwnerOrReadOnly,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user
        )
        
    def perform_create(self, serializer):
        product = serializer.save(
           seller=self.request.user,
           status="active",
           condition ="new"
        )

        images = self.request.FILES.getlist("images")
        print("IMAGES:", images)

        for index, image in enumerate(images):
            print("saving image:", image)

            ProductImage.objects.create(
              product=product,
              image=image,
              position=index
            )
            
            
            
    def perform_update(self, serializer):
        
        product = self.get_object()

        if product.seller != self.request.user:
            raise PermissionDenied(
                "You cannot edit this product."
            )

        serializer.save()
        images = self.request.FILES.getlist("images") #  Get all uploaded files from request under key "images" and return them as a list.
        current_count = product.images.count()

        for index, image in enumerate(images, start=current_count):
            ProductImage.objects.create(
            product=product,
            image=image,
            position=index
        )

    def perform_destroy(self, instance):

        if instance.seller != self.request.user:
            raise PermissionDenied(
                "You cannot delete this product."
            )

        instance.delete()
        
        
# =========================================================
# Cart Product 
# =========================================================
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): # for get request 
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(
            cart,
            context={"request": request} #it's used to pass that info which is not available in model
        )
        
        return Response(serializer.data)
    
    
    
    

class CartItemViewSet(ModelViewSet):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        )


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Item removed"
        })
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]

        # prevent own product purchase
        if product.seller == request.user:
            raise ValidationError(
                {"detail": "You cannot cart or buy your own product"}
            )

        item = add_to_cart(
             user=request.user,
             product_id=product.id,
             quantity=serializer.validated_data["quantity"],
             )
    
        output = CartItemSerializer(
            
            item,
            context=self.get_serializer_context(),)
        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
            )       

    def perform_update(self, serializer):

        item = serializer.instance
        quantity = serializer.validated_data["quantity"]
        if quantity > item.product.stock:
            raise ValidationError(
                {"detail": "Not enough stock"}
            )
        serializer.save()