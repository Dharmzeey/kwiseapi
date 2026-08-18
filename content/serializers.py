from rest_framework import serializers

from .models import Author, BuyingGuide, BuyingGuideEntry, Comparison, Device, FAQBlock, UseCaseTag


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "slug", "bio", "credentials", "avatar"]


class UseCaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseCaseTag
        fields = ["id", "name", "slug", "description"]


class FAQBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQBlock
        fields = ["id", "question", "answer", "order"]


class DeviceListSerializer(serializers.ModelSerializer):
    use_case_tags = UseCaseTagSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = [
            "id", "brand", "model_name", "slug", "form_factor", "release_year",
            "price_band_ngn", "price_band_cad", "is_in_stock",
            "hero_image", "verdict_summary", "use_case_tags",
            "created_at", "updated_at",
        ]


class DeviceSerializer(serializers.ModelSerializer):
    use_case_tags = UseCaseTagSerializer(many=True, read_only=True)
    faqs = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = [
            "id", "brand", "model_name", "slug", "form_factor", "release_year",
            "chipset", "ram_options", "storage_options",
            "display_specs", "camera_specs", "battery_capacity_mah", "battery_wh",
            "price_band_ngn", "price_band_cad", "conditions_available",
            "use_case_tags", "pros", "cons", "verdict_summary", "meta_description",
            "hero_image", "is_in_stock", "faqs", "created_at", "updated_at",
        ]

    def get_faqs(self, obj):
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(obj)
        faqs = FAQBlock.objects.filter(content_type=ct, object_id=obj.pk)
        return FAQBlockSerializer(faqs, many=True).data


class ComparisonListSerializer(serializers.ModelSerializer):
    device_a = DeviceListSerializer(read_only=True)
    device_b = DeviceListSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comparison
        fields = ["id", "title", "slug", "device_a", "device_b", "author", "published_at", "created_at", "updated_at", "meta_description"]


class ComparisonSerializer(serializers.ModelSerializer):
    device_a = DeviceSerializer(read_only=True)
    device_b = DeviceSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    faqs = serializers.SerializerMethodField()

    class Meta:
        model = Comparison
        fields = [
            "id", "title", "slug", "device_a", "device_b",
            "intro", "winner_by_category", "overall_recommendation",
            "author", "published_at", "created_at", "updated_at", "meta_description", "faqs",
        ]

    def get_faqs(self, obj):
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(obj)
        faqs = FAQBlock.objects.filter(content_type=ct, object_id=obj.pk)
        return FAQBlockSerializer(faqs, many=True).data


class BuyingGuideEntrySerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:
        model = BuyingGuideEntry
        fields = ["id", "rank", "device", "blurb"]


class BuyingGuideListSerializer(serializers.ModelSerializer):
    use_case_tag = UseCaseTagSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BuyingGuide
        fields = ["id", "title", "slug", "use_case_tag", "intro", "author", "published_at", "created_at", "updated_at", "meta_description"]


class BuyingGuideSerializer(serializers.ModelSerializer):
    use_case_tag = UseCaseTagSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    entries = BuyingGuideEntrySerializer(many=True, read_only=True)
    faqs = serializers.SerializerMethodField()

    class Meta:
        model = BuyingGuide
        fields = [
            "id", "title", "slug", "use_case_tag",
            "intro", "body", "entries",
            "author", "published_at", "created_at", "updated_at", "meta_description", "faqs",
        ]

    def get_faqs(self, obj):
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(obj)
        faqs = FAQBlock.objects.filter(content_type=ct, object_id=obj.pk)
        return FAQBlockSerializer(faqs, many=True).data


class SitemapEntrySerializer(serializers.Serializer):
    type = serializers.CharField()
    slug = serializers.CharField()
    updated_at = serializers.DateTimeField()
