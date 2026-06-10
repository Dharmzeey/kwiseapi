"""Kwise World — user views (register, login, profile)."""
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count, Sum

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


def _token_pair(user):
    """Return access + refresh token dict for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class RegisterView(GenericAPIView):
    """POST /api/auth/register/"""
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, "tokens": _token_pair(user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    """POST /api/auth/login/"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {"user": UserSerializer(user).data, "tokens": _token_pair(user)},
        )


class ProfileView(RetrieveUpdateAPIView):
    """GET / PATCH /api/auth/profile/"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ── Admin customer views ──────────────────────────────────────────────────────

class AdminCustomerListView(APIView):
    """GET /api/auth/admin/customers/"""
    permission_classes = [IsSuperUser]

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        qs = User.objects.annotate(
            order_count=Count("orders"),
            total_spent=Sum("orders__total"),
        ).order_by("-date_joined")

        if q:
            qs = qs.filter(
                email__icontains=q
            ) | User.objects.annotate(
                order_count=Count("orders"),
                total_spent=Sum("orders__total"),
            ).filter(first_name__icontains=q) | User.objects.annotate(
                order_count=Count("orders"),
                total_spent=Sum("orders__total"),
            ).filter(last_name__icontains=q)
            qs = qs.distinct()

        data = [
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "phone": u.phone,
                "date_joined": u.date_joined,
                "order_count": u.order_count,
                "total_spent": u.total_spent or 0,
            }
            for u in qs
        ]
        return Response(data)


class AdminCustomerDetailView(APIView):
    """GET /api/auth/admin/customers/<pk>/"""
    permission_classes = [IsSuperUser]

    def get(self, request, pk):
        try:
            user = User.objects.annotate(
                order_count=Count("orders"),
                total_spent=Sum("orders__total"),
            ).get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        from store.serializers import OrderSerializer
        orders = user.orders.prefetch_related("items").order_by("-created_at")

        return Response({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "date_joined": user.date_joined,
            "is_active": user.is_active,
            "order_count": user.order_count,
            "total_spent": user.total_spent or 0,
            "orders": OrderSerializer(orders, many=True).data,
        })
