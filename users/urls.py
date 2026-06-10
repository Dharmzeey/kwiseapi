"""Kwise World — auth URL patterns."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView, AdminCustomerListView, AdminCustomerDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("admin/customers/", AdminCustomerListView.as_view(), name="admin-customer-list"),
    path("admin/customers/<int:pk>/", AdminCustomerDetailView.as_view(), name="admin-customer-detail"),
]
