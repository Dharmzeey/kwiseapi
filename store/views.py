"""
Kwise World — store views.

Uses DRF generic class-based views.  No ViewSets, no Routers.
"""
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Sum

from .models import Category, Brand, Product, ProductSpec, Order
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWriteSerializer,
    AdminProductSerializer,
    AdminOrderSerializer,
    ReviewSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)


class IsSuperUser(BasePermission):
    """Allow access only to superusers."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


# ── Categories ────────────────────────────────────────────────────────────────

class CategoryListView(ListAPIView):
    """GET /api/categories/"""
    queryset = Category.objects.prefetch_related("brands").all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


# ── Products ──────────────────────────────────────────────────────────────────

class ProductListView(ListAPIView):
    """
    GET /api/products/

    Query params:
      category  – slug           e.g. ?category=phones
      brand     – slug           e.g. ?brand=iphone
      status    – condition      e.g. ?status=Foreign Used
      q         – search text    e.g. ?q=iphone+15
      one_time  – 1 / 0
      sort      – featured | low | high | rating
      max_price – upper bound in Naira
    """
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Product.objects.select_related("category", "brand")
        p = self.request.query_params

        if category := p.get("category"):
            qs = qs.filter(category__slug=category)
        if brand := p.get("brand"):
            qs = qs.filter(brand__slug=brand)
        if series := p.get("series"):
            qs = qs.filter(series=series)
        if condition := p.get("status"):
            qs = qs.filter(status=condition)
        if q := p.get("q", "").strip():
            qs = qs.filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(brand__name__icontains=q)
            )
        if (one_time := p.get("one_time")) is not None:
            qs = qs.filter(is_one_time=(one_time == "1"))
        if max_price := p.get("max_price"):
            try:
                qs = qs.filter(price__lte=int(max_price))
            except ValueError:
                pass

        sort = p.get("sort", "featured")
        order_map = {
            "low": ["price"],
            "high": ["-price"],
            "rating": ["-rating"],
        }
        return qs.order_by(*order_map.get(sort, ["-is_featured", "name"]))


class CategorySeriesView(APIView):
    """GET /api/categories/<slug>/series/  — distinct non-empty series for a category."""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        series = (
            Product.objects
            .filter(category__slug=slug)
            .exclude(series="")
            .values_list("series", flat=True)
            .distinct()
            .order_by("series")
        )
        return Response(list(series))


class ProductDetailView(RetrieveAPIView):
    """GET /api/products/<id>/"""
    queryset = Product.objects.select_related("category", "brand").prefetch_related("specs", "reviews")
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    lookup_url_kwarg = "id"  # URL still uses <id>, maps to slug field


class ProductRelatedView(ListAPIView):
    """GET /api/products/<id>/related/"""
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        slug = self.kwargs["id"]
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Product.objects.none()
        return (
            Product.objects
            .filter(category=product.category, is_one_time=False)
            .exclude(slug=slug)
            .order_by("-is_featured", "name")[:4]
        )


# ── Reviews ───────────────────────────────────────────────────────────────────

class ReviewCreateView(GenericAPIView):
    """POST /api/products/<id>/reviews/"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            product = Product.objects.get(slug=id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)

        reviews = product.reviews.all()
        product.rating = round(sum(r.rating for r in reviews) / reviews.count(), 1)
        product.review_count = reviews.count()
        product.save(update_fields=["rating", "review_count"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ── Orders ────────────────────────────────────────────────────────────────────

class CartVerifyView(APIView):
    """POST /api/cart/verify/ — return current DB prices for cart items."""
    permission_classes = [AllowAny]

    def post(self, request):
        items = request.data if isinstance(request.data, list) else request.data.get("items", [])
        result = []
        for item in items:
            try:
                product = Product.objects.get(slug=item["product_id"])
                result.append({
                    "product_id": item["product_id"],
                    "name": product.name,
                    "quantity": int(item.get("quantity", 1)),
                    "unit_price": product.price,
                    "available": not product.sold_out,
                })
            except (Product.DoesNotExist, KeyError):
                result.append({"product_id": item.get("product_id", ""), "available": False})
        return Response(result)


class OrderCreateView(GenericAPIView):
    """POST /api/orders/"""
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {"reference": order.reference, "total": order.total, "status": order.status},
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(RetrieveAPIView):
    """GET /api/orders/<reference>/"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    lookup_field = "reference"
    queryset = Order.objects.prefetch_related("items__product")


class MyOrderListView(ListAPIView):
    """GET /api/orders/mine/"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")


# ── Admin views (superuser only) ──────────────────────────────────────────────

class AdminStatsView(APIView):
    """GET /api/admin/stats/ — dashboard numbers."""
    permission_classes = [IsSuperUser]

    def get(self, request):
        total_revenue = Order.objects.filter(
            status__in=["confirmed", "dispatched", "delivered"]
        ).aggregate(total=Sum("total"))["total"] or 0

        return Response({
            "products": Product.objects.count(),
            "orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status="pending").count(),
            "total_revenue": total_revenue,
        })


class AdminProductListView(ListCreateAPIView):
    """GET /api/admin/products/   POST /api/admin/products/"""
    permission_classes = [IsSuperUser]
    pagination_class = None

    def get_queryset(self):
        return Product.objects.select_related("category", "brand").prefetch_related("specs").order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer
        return AdminProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(AdminProductSerializer(product).data, status=status.HTTP_201_CREATED)


class AdminProductDetailView(RetrieveUpdateDestroyAPIView):
    """GET / PATCH / DELETE /api/admin/products/<slug>/"""
    permission_classes = [IsSuperUser]
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.select_related("category", "brand").prefetch_related("specs")

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductWriteSerializer
        return AdminProductSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = ProductWriteSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(AdminProductSerializer(product).data)


class AdminProductImageView(APIView):
    """POST /api/admin/products/<slug>/image/ — upload product image."""
    permission_classes = [IsSuperUser]

    def post(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if "image" not in request.FILES:
            return Response({"detail": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete old image file if present
        if product.image:
            product.image.delete(save=False)

        product.image = request.FILES["image"]
        product.save(update_fields=["image"])
        return Response({"image": request.build_absolute_uri(product.image.url)})

    def delete(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if product.image:
            product.image.delete(save=False)
            product.image = None
            product.save(update_fields=["image"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminProductSpecView(APIView):
    """PUT /api/admin/products/<slug>/specs/ — replace all specs for a product."""
    permission_classes = [IsSuperUser]

    def put(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        specs = request.data  # expects [{"key": ..., "value": ...}, ...]
        if not isinstance(specs, list):
            return Response({"detail": "Expected a list of {key, value} objects."}, status=status.HTTP_400_BAD_REQUEST)

        ProductSpec.objects.filter(product=product).delete()
        for i, spec in enumerate(specs):
            if spec.get("key") and spec.get("value"):
                ProductSpec.objects.create(product=product, key=spec["key"], value=spec["value"], order=i)

        return Response({"detail": "Specs updated.", "count": len(specs)})


class AdminOrderListView(ListAPIView):
    """GET /api/admin/orders/"""
    permission_classes = [IsSuperUser]
    serializer_class = AdminOrderSerializer

    def get_queryset(self):
        return Order.objects.prefetch_related("items__product").order_by("-created_at")


class AdminOrderUpdateView(APIView):
    """PATCH /api/admin/orders/<reference>/status/ — update order status."""
    permission_classes = [IsSuperUser]

    VALID_STATUSES = {"pending", "confirmed", "dispatched", "delivered", "cancelled"}

    def patch(self, request, reference):
        try:
            order = Order.objects.get(reference=reference)
        except Order.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in self.VALID_STATUSES:
            return Response({"detail": f"Invalid status. Choose from: {', '.join(self.VALID_STATUSES)}"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save(update_fields=["status"])
        return Response(AdminOrderSerializer(order).data)
