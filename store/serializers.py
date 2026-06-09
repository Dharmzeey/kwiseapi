"""Kwise World — store serializers."""
from rest_framework import serializers
from .models import Category, Brand, Product, ProductSpec, Review, Order, OrderItem


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "slug", "name"]


class CategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "slug", "name", "icon", "blurb", "brands"]


class ProductSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpec
        fields = ["key", "value"]


class ReviewSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "reviewer_name", "rating", "text", "is_verified", "created_at", "product_name"]
        read_only_fields = ["id", "reviewer_name", "is_verified", "created_at", "product_name"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
            user = request.user
            validated_data["reviewer_name"] = (
                f"{user.first_name} {user.last_name}".strip() or user.email
            )
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product grids/listings."""
    id = serializers.SlugField(source="slug", read_only=True)  # slug exposed as id to frontend
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    brand_slug = serializers.CharField(source="brand.slug", read_only=True)
    save_amount = serializers.ReadOnlyField()
    sold_out = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "series",
            "category_slug", "brand_slug",
            "image", "thumb", "tint",
            "price", "old_price", "save_amount",
            "status", "rating", "review_count",
            "is_featured", "badge",
            "is_one_time", "stock", "sold_out",
            "colors",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for the product detail page."""
    id = serializers.SlugField(source="slug", read_only=True)  # slug exposed as id to frontend
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    brand_slug = serializers.CharField(source="brand.slug", read_only=True)
    specs = ProductSpecSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    save_amount = serializers.ReadOnlyField()
    sold_out = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id", "name",
            "category_slug", "brand_slug",
            "image", "thumb", "tint",
            "price", "old_price", "save_amount",
            "status", "rating", "review_count",
            "is_featured", "badge",
            "is_one_time", "stock", "sold_out",
            "description", "one_time_note",
            "colors", "specs", "reviews",
            "created_at",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "unit_price", "quantity", "line_total"]
        read_only_fields = ["product_name", "unit_price", "line_total"]


class OrderCreateSerializer(serializers.Serializer):
    """
    Accepts the cart payload from the frontend.

    Payload shape:
    {
      "items": [{"product_id": "iphone-15", "quantity": 1}],
      "guest_name":  "Ada Okafor",  # optional if authenticated
      "guest_email": "ada@example.com",
      "guest_phone": "+234 800 000 0000",
      "delivery_address": "12 Computer Village, Ikeja Lagos"
    }
    """
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        min_length=1,
    )
    guest_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    guest_email = serializers.EmailField(required=False, allow_blank=True)
    guest_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    delivery_address = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        validated = []
        for item in items:
            try:
                product = Product.objects.get(slug=item["product_id"])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product '{item['product_id']}' not found.")
            qty = int(item.get("quantity", 1))
            if qty < 1:
                raise serializers.ValidationError("Quantity must be at least 1.")
            if product.is_one_time and qty > 1:
                raise serializers.ValidationError(
                    f"'{product.name}' is a one-time item; quantity must be 1."
                )
            if product.sold_out:
                raise serializers.ValidationError(f"'{product.name}' is sold out.")
            validated.append({"product": product, "quantity": qty})
        return validated

    def create(self, validated_data):
        import random
        import string

        request = self.context.get("request")
        items = validated_data["items"]

        subtotal = sum(i["product"].price * i["quantity"] for i in items)
        delivery_fee = 0 if subtotal >= 500_000 else 5_000
        total = subtotal + delivery_fee
        ref = "KW-" + "".join(random.choices(string.digits, k=6))

        user = request.user if request and request.user.is_authenticated else None
        # Use profile data when authenticated, fall back to guest fields
        guest_name = f"{user.first_name} {user.last_name}".strip() if user else validated_data.get("guest_name", "")
        guest_email = user.email if user else validated_data.get("guest_email", "")
        guest_phone = getattr(user, "phone", "") or validated_data.get("guest_phone", "")

        order = Order.objects.create(
            reference=ref,
            user=user,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            delivery_address=validated_data.get("delivery_address", ""),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
        )

        for item in items:
            product = item["product"]
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=item["quantity"],
            )
            if product.is_one_time:
                product.stock = max(0, product.stock - item["quantity"])
                product.save(update_fields=["stock"])

        return order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "reference", "status",
            "subtotal", "delivery_fee", "total",
            "guest_name", "guest_email", "delivery_address",
            "items", "created_at",
        ]


# ── Admin serializers ─────────────────────────────────────────────────────────

class ProductWriteSerializer(serializers.ModelSerializer):
    """Used by admin to create / update a product (no image — handled separately)."""

    class Meta:
        model = Product
        fields = [
            "name", "category", "brand",
            "thumb", "tint",
            "price", "old_price",
            "status", "is_featured", "badge",
            "is_one_time", "stock",
            "description", "one_time_note",
            "colors",
        ]


class AdminProductSerializer(serializers.ModelSerializer):
    """Read-only admin list/detail — includes all fields."""
    id = serializers.SlugField(source="slug", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    brand_slug = serializers.CharField(source="brand.slug", read_only=True)
    specs = ProductSpecSerializer(many=True, read_only=True)
    save_amount = serializers.ReadOnlyField()
    sold_out = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id", "slug", "name",
            "category", "category_slug", "brand", "brand_slug",
            "image", "thumb", "tint",
            "price", "old_price", "save_amount",
            "status", "rating", "review_count",
            "is_featured", "badge",
            "is_one_time", "stock", "sold_out",
            "description", "one_time_note",
            "colors", "specs",
            "created_at", "updated_at",
        ]


class AdminOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "reference", "status",
            "subtotal", "delivery_fee", "total",
            "guest_name", "guest_email", "guest_phone", "delivery_address",
            "items", "created_at",
        ]
