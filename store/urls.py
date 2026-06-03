"""Kwise World — store URL patterns (no Routers)."""
from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    ProductRelatedView,
    ReviewCreateView,
    OrderCreateView,
    OrderDetailView,
    MyOrderListView,
)

urlpatterns = [
    # Categories
    path("categories/", CategoryListView.as_view(), name="category-list"),

    # Products
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<str:id>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<str:id>/related/", ProductRelatedView.as_view(), name="product-related"),
    path("products/<str:id>/reviews/", ReviewCreateView.as_view(), name="product-review-create"),

    # Orders
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/mine/", MyOrderListView.as_view(), name="order-mine"),
    path("orders/<str:reference>/", OrderDetailView.as_view(), name="order-detail"),
]
