from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Author, BuyingGuide, BuyingGuideEntry, Comparison, Device, FAQBlock, UseCaseTag


class FAQInline(GenericTabularInline):
    model = FAQBlock
    extra = 1
    fields = ["order", "question", "answer"]


class BuyingGuideEntryInline(admin.TabularInline):
    model = BuyingGuideEntry
    extra = 1
    fields = ["rank", "device", "blurb"]
    autocomplete_fields = ["device"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "credentials"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(UseCaseTag)
class UseCaseTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["brand", "model_name", "form_factor", "release_year", "price_band_ngn", "is_in_stock", "published", "updated_at"]
    list_filter = ["form_factor", "brand", "published", "is_in_stock", "use_case_tags"]
    list_editable = ["is_in_stock", "published"]
    search_fields = ["brand", "model_name", "slug"]
    prepopulated_fields = {"slug": ("brand", "model_name")}
    filter_horizontal = ["use_case_tags"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [FAQInline]
    fieldsets = [
        ("Identity", {"fields": ["brand", "model_name", "slug", "form_factor", "release_year", "use_case_tags"]}),
        ("Specs", {"fields": ["chipset", "ram_options", "storage_options", "display_specs", "camera_specs", "battery_capacity_mah", "battery_wh"]}),
        ("Pricing & Availability", {"fields": ["price_band_ngn", "price_band_cad", "conditions_available", "is_in_stock"]}),
        ("Editorial", {"fields": ["pros", "cons", "verdict_summary", "meta_description", "hero_image"]}),
        ("Publishing", {"fields": ["published", "created_at", "updated_at"]}),
    ]


@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ["title", "device_a", "device_b", "author", "published", "updated_at"]
    list_filter = ["published", "author"]
    list_editable = ["published"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["device_a", "device_b"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [FAQInline]
    fieldsets = [
        ("Identity", {"fields": ["title", "slug", "device_a", "device_b"]}),
        ("Content", {"fields": ["intro", "winner_by_category", "overall_recommendation"]}),
        ("Publishing", {"fields": ["author", "published", "published_at", "meta_description", "created_at", "updated_at"]}),
    ]


@admin.register(BuyingGuide)
class BuyingGuideAdmin(admin.ModelAdmin):
    list_display = ["title", "use_case_tag", "author", "published", "updated_at"]
    list_filter = ["published", "use_case_tag", "author"]
    list_editable = ["published"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    inlines = [BuyingGuideEntryInline, FAQInline]
    fieldsets = [
        ("Identity", {"fields": ["title", "slug", "use_case_tag"]}),
        ("Content", {"fields": ["intro", "body"]}),
        ("Publishing", {"fields": ["author", "published", "published_at", "meta_description", "created_at", "updated_at"]}),
    ]
