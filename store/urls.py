"""Kwise World — store URL patterns (no Routers)."""
from django.urls import path
from .views import (
    CategoryListView,
    CategorySeriesView,
    ProductListView,
    ProductDetailView,
    ProductRelatedView,
    ReviewListView,
    ReviewCreateView,
    CartVerifyView,
    OrderCreateView,
    OrderDetailView,
    MyOrderListView,
    PaystackWebhookView,
    # Admin
    AdminStatsView,
    AdminProductListView,
    AdminProductDetailView,
    AdminProductImageView,
    AdminProductSpecView,
    AdminOrderListView,
    AdminOrderUpdateView,
    AdminReviewListView,
    AdminReviewVerifyView,
)

urlpatterns = [
    # Categories
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<slug:slug>/series/", CategorySeriesView.as_view(), name="category-series"),

    # Products
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<str:id>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<str:id>/related/", ProductRelatedView.as_view(), name="product-related"),
    path("products/<str:id>/reviews/", ReviewCreateView.as_view(), name="product-review-create"),

    # Reviews
    path("reviews/", ReviewListView.as_view(), name="review-list"),

    # Cart
    path("cart/verify/", CartVerifyView.as_view(), name="cart-verify"),

    # Orders
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/mine/", MyOrderListView.as_view(), name="order-mine"),
    path("orders/<str:reference>/", OrderDetailView.as_view(), name="order-detail"),

    # Payments
    path("payments/webhook/", PaystackWebhookView.as_view(), name="paystack-webhook"),

    # Admin API
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),
    path("admin/products/", AdminProductListView.as_view(), name="admin-product-list"),
    path("admin/products/<slug:slug>/", AdminProductDetailView.as_view(), name="admin-product-detail"),
    path("admin/products/<slug:slug>/image/", AdminProductImageView.as_view(), name="admin-product-image"),
    path("admin/products/<slug:slug>/specs/", AdminProductSpecView.as_view(), name="admin-product-specs"),
    path("admin/orders/", AdminOrderListView.as_view(), name="admin-order-list"),
    path("admin/orders/<str:reference>/status/", AdminOrderUpdateView.as_view(), name="admin-order-status"),
    path("admin/reviews/", AdminReviewListView.as_view(), name="admin-review-list"),
    path("admin/reviews/<int:pk>/verify/", AdminReviewVerifyView.as_view(), name="admin-review-verify"),
]
