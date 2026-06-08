from django.conf import settings
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

CATALOG_TTL = 60 * 60 * 2  # 2 hours

from .models import DefectPricing, DefectType, IphoneModel, IphoneSeries, StorageVariant, SwapEstimate
from .serializers import (
    DefectTypeSerializer,
    EstimateRequestSerializer,
    IphoneModelSerializer,
    IphoneSeriesSerializer,
    StorageVariantSerializer,
)


class SeriesListView(generics.ListAPIView):
    serializer_class = IphoneSeriesSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return IphoneSeries.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        key = "swap:catalog:series"
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, CATALOG_TTL)
        return response


class ModelListView(generics.ListAPIView):
    serializer_class = IphoneModelSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return IphoneModel.objects.filter(
            series_id=self.kwargs["series_id"],
            series__is_active=True,
            is_active=True,
        ).select_related("series")

    def list(self, request, *args, **kwargs):
        key = f"swap:catalog:models:{self.kwargs['series_id']}"
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, CATALOG_TTL)
        return response


class StorageListView(generics.ListAPIView):
    serializer_class = StorageVariantSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return StorageVariant.objects.filter(
            model_id=self.kwargs["model_id"],
            model__is_active=True,
            is_active=True,
        ).select_related("model")

    def list(self, request, *args, **kwargs):
        key = f"swap:catalog:storage:{self.kwargs['model_id']}"
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, CATALOG_TTL)
        return response


class DefectListView(generics.ListAPIView):
    serializer_class = DefectTypeSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return DefectType.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        key = "swap:catalog:defects"
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, CATALOG_TTL)
        return response


class EstimateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        req = EstimateRequestSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)

        data = req.validated_data

        from_storage = (
            StorageVariant.objects
            .select_related("model__series")
            .get(pk=data["from_storage_id"])
        )
        to_storage = (
            StorageVariant.objects
            .select_related("model__series")
            .get(pk=data["to_storage_id"])
        )
        defects = list(
            DefectType.objects.filter(pk__in=data["defect_ids"], is_active=True)
        ) if data["defect_ids"] else []

        from_value = from_storage.swap_in_value_ngn
        total_repair_cost = 0
        repair_breakdown = []

        for defect in defects:
            try:
                pricing = DefectPricing.objects.get(
                    defect=defect,
                    iphone_model=from_storage.model,
                    is_active=True,
                )
                deduction_pct = pricing.deduction_pct
                repair_cost = pricing.repair_cost_ngn
            except DefectPricing.DoesNotExist:
                deduction_pct = defect.default_deduction_pct
                repair_cost = 0

            from_value = round(from_value * (100 - deduction_pct) / 100)
            total_repair_cost += repair_cost
            repair_breakdown.append({
                "defect": defect.name,
                "deduction_pct": deduction_pct,
                "repair_cost_ngn": repair_cost,
            })

        from_value_int = from_value
        to_value = to_storage.uk_end_user_price_ngn
        service_fee = int(getattr(settings, "SWAP_SERVICE_FEE_NGN", 10_000))
        net = (to_value - from_value_int) + total_repair_cost + service_fee

        direction = "upgrade" if net > 0 else "downgrade" if net < 0 else "even"

        session_key = request.session.session_key or ""
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        estimate = SwapEstimate.objects.create(
            session_key=session_key,
            from_storage=from_storage,
            to_storage=to_storage,
            from_base_value_ngn=from_storage.swap_in_value_ngn,
            from_value_ngn=from_value_int,
            total_repair_cost_ngn=total_repair_cost,
            to_value_ngn=to_value,
            service_fee_ngn=service_fee,
            net_amount_ngn=net,
        )
        estimate.defects.set(defects)

        return Response({
            "from_device": str(from_storage),
            "from_base_value_ngn": from_storage.swap_in_value_ngn,
            "from_value_ngn": from_value_int,
            "to_device": str(to_storage),
            "to_value_ngn": to_value,
            "repair_breakdown": repair_breakdown,
            "total_repair_cost_ngn": total_repair_cost,
            "service_fee_ngn": service_fee,
            "net_ngn": net,
            "direction": direction,
            "defects_applied": [d.name for d in defects],
        })
