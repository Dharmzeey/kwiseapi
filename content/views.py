from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BuyingGuide, Comparison, Device
from .serializers import (
    BuyingGuideListSerializer,
    BuyingGuideSerializer,
    ComparisonListSerializer,
    ComparisonSerializer,
    DeviceListSerializer,
    DeviceSerializer,
    SitemapEntrySerializer,
)


class DeviceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        qs = Device.objects.filter(published=True).prefetch_related("use_case_tags")
        use_case = self.request.query_params.get("use_case")
        brand = self.request.query_params.get("brand")
        if use_case:
            qs = qs.filter(use_case_tags__slug=use_case)
        if brand:
            qs = qs.filter(brand__iexact=brand)
        return qs.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DeviceSerializer
        return DeviceListSerializer


class ComparisonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Comparison.objects.filter(published=True).select_related("device_a", "device_b", "author")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ComparisonSerializer
        return ComparisonListSerializer


class BuyingGuideViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        qs = BuyingGuide.objects.filter(published=True).select_related("use_case_tag", "author")
        use_case = self.request.query_params.get("use_case")
        if use_case:
            qs = qs.filter(use_case_tag__slug=use_case)
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BuyingGuideSerializer
        return BuyingGuideListSerializer


class DynamicCompareView(APIView):
    """
    GET /api/content/compare/?a=<slug>&b=<slug>
    Returns a structured spec diff for any two published devices.
    Works even when no editorial Comparison object exists for this pair.
    """
    permission_classes = [AllowAny]

    SPEC_CATEGORIES = [
        ("Chipset",       lambda d: d.chipset),
        ("RAM",           lambda d: ", ".join(d.ram_options) if d.ram_options else "—"),
        ("Storage",       lambda d: ", ".join(d.storage_options) if d.storage_options else "—"),
        ("Display size",  lambda d: d.display_specs.get("size", "—")),
        ("Display type",  lambda d: d.display_specs.get("type", "—")),
        ("Refresh rate",  lambda d: d.display_specs.get("refresh_rate", "—")),
        ("Battery",       lambda d: (
            f"{d.battery_capacity_mah} mAh" if d.battery_capacity_mah
            else f"{d.battery_wh} Wh" if d.battery_wh
            else "—"
        )),
        ("Price (NGN)",   lambda d: d.price_band_ngn or "—"),
        ("Price (CAD)",   lambda d: d.price_band_cad or "—"),
    ]

    def get(self, request):
        a_slug = request.query_params.get("a")
        b_slug = request.query_params.get("b")
        if not a_slug or not b_slug:
            return Response({"error": "Both ?a= and ?b= slugs are required."}, status=400)

        try:
            device_a = Device.objects.prefetch_related("use_case_tags").get(slug=a_slug, published=True)
            device_b = Device.objects.prefetch_related("use_case_tags").get(slug=b_slug, published=True)
        except Device.DoesNotExist:
            return Response({"error": "One or both devices not found."}, status=404)

        diff = []
        for label, getter in self.SPEC_CATEGORIES:
            a_val = getter(device_a)
            b_val = getter(device_b)
            diff.append({"label": label, "a_value": a_val, "b_value": b_val})

        return Response({
            "device_a": DeviceSerializer(device_a).data,
            "device_b": DeviceSerializer(device_b).data,
            "diff": diff,
        })


class SitemapDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        entries = []
        for d in Device.objects.filter(published=True).values("slug", "updated_at"):
            entries.append({"type": "device", "slug": d["slug"], "updated_at": d["updated_at"]})
        for c in Comparison.objects.filter(published=True).values("slug", "updated_at"):
            entries.append({"type": "comparison", "slug": c["slug"], "updated_at": c["updated_at"]})
        for g in BuyingGuide.objects.filter(published=True).values("slug", "updated_at"):
            entries.append({"type": "guide", "slug": g["slug"], "updated_at": g["updated_at"]})
        return Response(SitemapEntrySerializer(entries, many=True).data)
