from django.contrib import admin
from .models import Category, Brand, Product, ProductSpec, Review, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "category"]
    list_filter = ["category"]


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "category", "brand", "price", "status", "is_featured", "is_one_time", "stock"]
    list_filter = ["category", "brand", "status", "is_featured", "is_one_time"]
    search_fields = ["name", "id"]
    inlines = [ProductSpecInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["reviewer_name", "product", "rating", "is_verified", "created_at"]
    list_filter = ["is_verified", "rating"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "unit_price", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["reference", "status", "total", "created_at"]
    list_filter = ["status"]
    search_fields = ["reference", "guest_email"]
    readonly_fields = ["reference", "subtotal", "delivery_fee", "total", "created_at"]
    inlines = [OrderItemInline]
