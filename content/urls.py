from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuyingGuideViewSet, ComparisonViewSet, DeviceViewSet, DynamicCompareView, SitemapDataView

router = DefaultRouter()
router.register("devices", DeviceViewSet, basename="device")
router.register("comparisons", ComparisonViewSet, basename="comparison")
router.register("guides", BuyingGuideViewSet, basename="guide")

urlpatterns = [
    path("", include(router.urls)),
    path("compare/", DynamicCompareView.as_view(), name="dynamic-compare"),
    path("sitemap-data/", SitemapDataView.as_view(), name="sitemap-data"),
]
