"""
Kwise World — store views.

Uses DRF generic class-based views.  No ViewSets, no Routers.
"""
import hashlib
import hmac
import json
import urllib.request
from django.conf import settings as django_settings
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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
from django.db.models import Q, Sum, F

from .models import Category, Brand, Product, ProductSpec, Order, OrderItem, PendingTransaction, Review
from .serializers import (
    CategorySerializer,
    CategoryWriteSerializer,
    BrandSerializer,
    BrandWriteSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWriteSerializer,
    AdminProductSerializer,
    AdminOrderSerializer,
    AdminPendingTransactionSerializer,
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
        if sort == "rating":
            return qs.order_by(F("rating").desc(nulls_last=True))
        order_map = {
            "low": ["price"],
            "high": ["-price"],
        }
        return qs.order_by(*order_map.get(sort, ["-is_featured", "name"]))


class CategorySeriesView(APIView):
    """GET /api/categories/<slug>/series/  — distinct non-empty series for a category."""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        qs = Product.objects.filter(category__slug=slug).exclude(series="")
        if brand := request.query_params.get("brand"):
            qs = qs.filter(brand__slug=brand)
        series = qs.values_list("series", flat=True).distinct().order_by("series")
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

class ReviewListView(ListAPIView):
    """GET /api/reviews/?limit=6  — verified reviews for the homepage."""
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        limit = int(self.request.query_params.get("limit", 6))
        return (
            Review.objects
            .filter(is_verified=True)
            .select_related("product")
            .order_by("-created_at")[:limit]
        )


class AdminReviewListView(ListAPIView):
    """GET /api/admin/reviews/?verified=0|1"""
    serializer_class = ReviewSerializer
    permission_classes = [IsSuperUser]
    pagination_class = None

    def get_queryset(self):
        qs = Review.objects.select_related("product").order_by("-created_at")
        v = self.request.query_params.get("verified")
        if v == "0":
            qs = qs.filter(is_verified=False)
        elif v == "1":
            qs = qs.filter(is_verified=True)
        return qs


class AdminReviewVerifyView(APIView):
    """PATCH /api/admin/reviews/<pk>/verify/"""
    permission_classes = [IsSuperUser]

    def patch(self, request, pk):
        try:
            review = Review.objects.select_related("product").get(pk=pk)
        except Review.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        review.is_verified = not review.is_verified
        review.save(update_fields=["is_verified"])
        review.product.refresh_rating()
        return Response(ReviewSerializer(review).data)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        product = review.product
        review.delete()
        product.refresh_rating()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        product.refresh_rating()

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
        pending = serializer.save()
        print(pending)
        return Response(
            {
                "reference": pending.reference,
                "total": pending.total,
                "authorization_url": getattr(pending, "authorization_url", None),
            },
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


# ── Paystack webhook ──────────────────────────────────────────────────────────

@method_decorator(csrf_exempt, name="dispatch")
class PaystackWebhookView(APIView):
    """
    POST /api/payments/webhook/
    Paystack calls this after every payment event.
    Only on charge.success do we:
      1. Verify HMAC signature.
      2. Confirm the transaction server-to-server with Paystack.
      3. Look up the PendingTransaction by reference.
      4. Create the real Order + OrderItems from the snapshot.
      5. Delete the PendingTransaction.
    Orders are therefore only ever created after successful payment.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Verify Paystack HMAC signature
        sig = request.headers.get("x-paystack-signature", "")
        secret = django_settings.PAYSTACK_SECRET_KEY.encode()
        digest = hmac.new(secret, msg=request.body, digestmod=hashlib.sha512).hexdigest()
        if not hmac.compare_digest(digest, sig):
            return Response({"detail": "Invalid signature."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Parse event — only care about charge.success
        try:
            event = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"detail": "Bad JSON."}, status=status.HTTP_400_BAD_REQUEST)

        if event.get("event") != "charge.success":
            return Response({"detail": "Ignored."}, status=status.HTTP_200_OK)

        reference = event.get("data", {}).get("reference", "")
        if not reference:
            return Response({"detail": "No reference."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Verify server-to-server with Paystack (never trust webhook payload alone)
        try:
            verify_req = urllib.request.Request(
                f"{django_settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}",
                headers={
                    "Authorization": f"Bearer {django_settings.PAYSTACK_SECRET_KEY}",
                    "User-Agent": "KwiseWorld/1.0",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(verify_req, timeout=10) as resp:
                verify_data = json.loads(resp.read())
        except Exception:
            return Response({"detail": "Paystack verify failed."}, status=status.HTTP_502_BAD_GATEWAY)

        if verify_data.get("data", {}).get("status") != "success":
            return Response({"detail": "Payment not successful."}, status=status.HTTP_200_OK)

        # 4. Idempotency — if order already exists (webhook fired twice), return OK
        if Order.objects.filter(reference=reference).exists():
            return Response({"detail": "Already processed."}, status=status.HTTP_200_OK)

        # 5. Look up the pending transaction
        try:
            pending = PendingTransaction.objects.get(reference=reference)
        except PendingTransaction.DoesNotExist:
            return Response({"detail": "Pending transaction not found."}, status=status.HTTP_404_NOT_FOUND)

        # 6. Create the real Order from the snapshot
        order = Order.objects.create(
            reference=pending.reference,
            user=pending.user,
            guest_name=pending.guest_name,
            guest_email=pending.guest_email,
            guest_phone=pending.guest_phone,
            delivery_address=pending.delivery_address,
            subtotal=pending.subtotal,
            delivery_fee=pending.delivery_fee,
            total=pending.total,
            status="confirmed",
            payment_status="paid",
            confirmed_at=timezone.now(),
        )

        for item in pending.cart_data:
            try:
                product = Product.objects.get(slug=item["product_slug"])
            except Product.DoesNotExist:
                continue
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item["product_name"],
                unit_price=item["unit_price"],
                quantity=item["quantity"],
            )
            if item.get("is_one_time"):
                product.stock = max(0, product.stock - item["quantity"])
                product.save(update_fields=["stock"])

        # 7. Clean up the pending record
        pending.delete()

        return Response({"detail": "OK."}, status=status.HTTP_200_OK)


# ── Admin views (superuser only) ──────────────────────────────────────────────

class AdminStatsView(APIView):
    """GET /api/admin/stats/ — dashboard numbers + recent orders + low stock."""
    permission_classes = [IsSuperUser]

    def get(self, request):
        total_revenue = Order.objects.filter(
            status__in=["confirmed", "dispatched", "delivered"]
        ).aggregate(total=Sum("total"))["total"] or 0

        recent_orders = Order.objects.prefetch_related("items").order_by("-created_at")[:8]
        low_stock = (
            Product.objects
            .filter(stock__lte=3, is_one_time=False)
            .select_related("category", "brand")
            .order_by("stock")[:10]
        )

        return Response({
            "products": Product.objects.count(),
            "orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status="pending").count(),
            "total_revenue": total_revenue,
            "recent_orders": AdminOrderSerializer(recent_orders, many=True).data,
            "low_stock": AdminProductSerializer(low_stock, many=True).data,
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
    """GET /api/admin/orders/?q=&status="""
    permission_classes = [IsSuperUser]
    serializer_class = AdminOrderSerializer

    def get_queryset(self):
        qs = Order.objects.prefetch_related("items__product").order_by("-created_at")
        p = self.request.query_params
        if q := p.get("q", "").strip():
            qs = qs.filter(
                Q(reference__icontains=q) |
                Q(guest_name__icontains=q) |
                Q(guest_email__icontains=q) |
                Q(guest_phone__icontains=q)
            )
        if status_filter := p.get("status", "").strip():
            qs = qs.filter(status=status_filter)
        return qs


class AdminOrderUpdateView(APIView):
    """PATCH /api/admin/orders/<reference>/status/ — update order status.

    'confirmed' is set exclusively by the Paystack webhook; it cannot be
    set here.  Only dispatched / delivered / cancelled are admin-settable.
    """
    permission_classes = [IsSuperUser]

    ADMIN_STATUSES = {"dispatched", "delivered", "cancelled"}

    def patch(self, request, reference):
        try:
            order = Order.objects.get(reference=reference)
        except Order.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in self.ADMIN_STATUSES:
            return Response(
                {"detail": f"Choose from: {', '.join(sorted(self.ADMIN_STATUSES))}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        update_fields = ["status", "updated_at"]
        order.status = new_status

        now = timezone.now()
        if new_status == "dispatched" and not order.dispatched_at:
            order.dispatched_at = now
            update_fields.append("dispatched_at")
        elif new_status == "delivered" and not order.delivered_at:
            order.delivered_at = now
            update_fields.append("delivered_at")
            if not order.dispatched_at:
                order.dispatched_at = now
                update_fields.append("dispatched_at")

        order.save(update_fields=update_fields)
        return Response(AdminOrderSerializer(order).data)


# ── Admin: Pending Transactions ───────────────────────────────────────────────

class AdminPendingTransactionListView(ListAPIView):
    """GET /api/admin/pending-transactions/"""
    permission_classes = [IsSuperUser]
    serializer_class = AdminPendingTransactionSerializer
    pagination_class = None

    def get_queryset(self):
        return PendingTransaction.objects.order_by("-created_at")


# ── Admin: Category CRUD ──────────────────────────────────────────────────────

class AdminCategoryListView(APIView):
    """GET /api/admin/categories/   POST /api/admin/categories/"""
    permission_classes = [IsSuperUser]

    def get(self, request):
        cats = Category.objects.prefetch_related("brands").order_by("order", "name")
        return Response(CategorySerializer(cats, many=True).data)

    def post(self, request):
        serializer = CategoryWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cat = serializer.save()
        return Response(CategorySerializer(cat).data, status=status.HTTP_201_CREATED)


class AdminCategoryDetailView(APIView):
    """PATCH / DELETE /api/admin/categories/<slug>/"""
    permission_classes = [IsSuperUser]

    def _get(self, slug):
        try:
            return Category.objects.prefetch_related("brands").get(slug=slug)
        except Category.DoesNotExist:
            return None

    def patch(self, request, slug):
        cat = self._get(slug)
        if not cat:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryWriteSerializer(cat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        cat = serializer.save()
        return Response(CategorySerializer(cat).data)

    def delete(self, request, slug):
        cat = self._get(slug)
        if not cat:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin: Brand CRUD ─────────────────────────────────────────────────────────

class AdminBrandListView(APIView):
    """GET /api/admin/brands/   POST /api/admin/brands/"""
    permission_classes = [IsSuperUser]

    def get(self, request):
        qs = Brand.objects.select_related("category").order_by("category__name", "name")
        return Response(BrandSerializer(qs, many=True).data)

    def post(self, request):
        serializer = BrandWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand = serializer.save()
        return Response(BrandSerializer(brand).data, status=status.HTTP_201_CREATED)


class AdminBrandDetailView(APIView):
    """PATCH / DELETE /api/admin/brands/<pk>/"""
    permission_classes = [IsSuperUser]

    def _get(self, pk):
        try:
            return Brand.objects.select_related("category").get(pk=pk)
        except Brand.DoesNotExist:
            return None

    def patch(self, request, pk):
        brand = self._get(pk)
        if not brand:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BrandWriteSerializer(brand, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        brand = serializer.save()
        return Response(BrandSerializer(brand).data)

    def delete(self, request, pk):
        brand = self._get(pk)
        if not brand:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
