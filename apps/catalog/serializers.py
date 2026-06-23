from rest_framework import serializers
from .models import Category, Product, ProductImage,  CartItem, Cart
from rest_framework.exceptions import ValidationError
from django.db.models import Avg
from apps.orders.models import Review
from apps.orders.serializers import ReviewSerializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "position"]



class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    # when you want to create value by using custom fields, read only

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "children"]

    def get_children(self, obj): # Methods always need self, one category
        children = obj.children.all()
        return CategorySerializer(children, many=True).data # serializer to JSON



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    seller_name = serializers.CharField(source="seller.fullname", read_only=True )
    seller_id = serializers.IntegerField(
        source="seller.id",
        read_only=True
    )

    class Meta:
        model = Product
        fields =  [
            "id",
            "title",
            "slug",
            "sku",
            "condition",
            "category",
            "price",
            "stock",
            "description",
            "thumbnail",
            "seller_name",
            "category_name",
            "seller_id",
            "images",
        ]
    
    
            



class CartItemSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    product_image = serializers.SerializerMethodField()

    unit_price_snapshot = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem

        fields = [
            "id",
            "product",
            "product_title",
            "product_price",
            "product_image",
            "quantity",
            "unit_price_snapshot",
        ]


    def get_product_image(self, obj):
        request = self.context.get("request")

        if obj.product.thumbnail and request:
            return request.build_absolute_uri(obj.product.thumbnail.url)

        if obj.product.thumbnail:
            return obj.product.thumbnail.url

        return None
    
    
    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                {
                    
                "Quantity must be greater than 0"
                }
            )

        return value
    
    
           
  

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_items", "created_at", "updated_at", "subtotal"]
        
        
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())


    
    def get_subtotal(self, obj):
        return sum(
            item.quantity * item.unit_price_snapshot
            for item in obj.items.all()
        )
        
        
   
class ProductDetailSerializer(ProductSerializer):

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()


    class Meta(ProductSerializer.Meta):

        fields = ProductSerializer.Meta.fields + [
            "average_rating",
            "review_count",
            "reviews",
        ]


    def get_average_rating(self, obj):

        avg = obj.reviews.aggregate(
            avg=Avg("rating")
        )["avg"]

        if avg:
            return round(avg, 1)

        return 0


    def get_review_count(self, obj):

        return obj.reviews.count()


    def get_reviews(self, obj):

        reviews = obj.reviews.select_related(
            "user"
        ).order_by("-created_at")

        return ReviewSerializer(
            reviews,
            many=True,
            context=self.context
        ).data
 
     