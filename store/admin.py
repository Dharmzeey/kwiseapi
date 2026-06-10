from django.contrib import admin
from .models import Category, Brand, Product, ProductSpec, Review, Order, OrderItem, PendingTransaction


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
    list_display = ["name", "slug", "category", "brand", "price", "storage_variant", "status", "is_featured", "is_one_time", "stock"]
    list_filter = ["category", "brand", "status", "is_featured", "is_one_time"]
    search_fields = ["name", "slug"]
    inlines = [ProductSpecInline]
    readonly_fields = ["slug", "created_at", "updated_at"]
    fieldsets = [
        ("Identity", {"fields": ["name", "slug", "category", "brand"]}),
        ("Image", {"fields": ["image", "thumb", "tint"]}),
        ("Pricing", {"fields": ["storage_variant", "price", "old_price"]}),
        ("Details", {"fields": ["status", "badge", "is_featured", "is_one_time", "stock", "colors"]}),
        ("Content", {"fields": ["description", "one_time_note"]}),
        ("Meta", {"fields": ["rating", "review_count", "created_at", "updated_at"]}),
    ]


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
    list_display = ["reference", "status", "payment_status", "total", "confirmed_at", "dispatched_at", "delivered_at", "created_at"]
    list_filter = ["status", "payment_status"]
    search_fields = ["reference", "guest_email"]
    readonly_fields = ["reference", "payment_status", "subtotal", "delivery_fee", "total",
                       "confirmed_at", "dispatched_at", "delivered_at", "created_at"]
    inlines = [OrderItemInline]


@admin.register(PendingTransaction)
class PendingTransactionAdmin(admin.ModelAdmin):
    list_display = ["reference", "guest_email", "total", "created_at"]
    search_fields = ["reference", "guest_email"]
    readonly_fields = ["reference", "user", "guest_name", "guest_email", "guest_phone",
                       "delivery_address", "cart_data", "subtotal", "delivery_fee", "total", "created_at"]

