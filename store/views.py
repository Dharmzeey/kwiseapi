"""
Kwise World — store views.

Uses DRF generic class-based views.  No ViewSets, no Routers.
"""
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Category, Product, Order
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)


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
      status    – condition      e.g. ?status=UK-Used
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

class OrderCreateView(GenericAPIView):
    """POST /api/orders/"""
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]

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
