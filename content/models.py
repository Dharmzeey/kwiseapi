"""
Kwise World — content models.

Supports three page types built on top of a shared Device catalog:
  - Device profile  (/phones/<slug>)
  - Comparison      (/compare/<slug>)
  - BuyingGuide     (/guides/<slug>)
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .constants import (
    CAMERA_SPEC_KEYS,
    CONDITION_LABELS,
    DISPLAY_SPEC_KEYS,
    FORM_FACTOR_CHOICES,
    FORM_FACTOR_PHONE,
    MAX_EXTRA_WINNER_CATEGORIES,
    WINNER_CATEGORIES,
    WINNER_VALUES,
)


class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    bio = models.TextField()
    credentials = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to="authors/", blank=True)

    def __str__(self):
        return self.name


class UseCaseTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    brand = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    form_factor = models.CharField(
        max_length=20,
        choices=FORM_FACTOR_CHOICES,
        default=FORM_FACTOR_PHONE,
        help_text="Physical device category. Not a use-case — drives filtering, not persona guides.",
    )
    release_year = models.PositiveIntegerField()

    chipset = models.CharField(max_length=100)
    ram_options = models.JSONField(default=list)
    storage_options = models.JSONField(default=list)
    display_specs = models.JSONField(default=dict)
    camera_specs = models.JSONField(default=dict)
    battery_capacity_mah = models.PositiveIntegerField(
        null=True, blank=True, help_text="Phone battery in mAh. Leave blank for laptops (use battery_wh)."
    )
    battery_wh = models.PositiveIntegerField(
        null=True, blank=True, help_text="Laptop battery in watt-hours. Leave blank for phones (use mAh)."
    )

    price_band_ngn = models.CharField(max_length=50, blank=True)
    price_band_cad = models.CharField(max_length=50, blank=True)
    conditions_available = models.JSONField(default=list)

    use_case_tags = models.ManyToManyField(UseCaseTag, blank=True)

    pros = models.JSONField(default=list)
    cons = models.JSONField(default=list)
    verdict_summary = models.TextField(
        blank=True,
        help_text="1–2 sentence direct verdict. Lead with the answer — AI engines lift this near-verbatim.",
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Controls the /phones/<slug> meta description. Falls back to verdict_summary if blank.",
    )

    hero_image = models.ImageField(upload_to="devices/", blank=True)
    is_in_stock = models.BooleanField(
        default=True,
        help_text=(
            "Human-facing stock hint only. NOT wired to the live catalog yet, so it is "
            "deliberately excluded from Product structured data until it is."
        ),
    )

    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["brand", "model_name"]

    def __str__(self):
        return f"{self.brand} {self.model_name}"

    def clean(self):
        errors = {}
        bad_display = [k for k in self.display_specs if k not in DISPLAY_SPEC_KEYS]
        if bad_display:
            errors["display_specs"] = (
                f"Unknown display spec key(s): {', '.join(bad_display)}. "
                f"Allowed: {', '.join(DISPLAY_SPEC_KEYS)}."
            )
        bad_camera = [k for k in self.camera_specs if k not in CAMERA_SPEC_KEYS]
        if bad_camera:
            errors["camera_specs"] = (
                f"Unknown camera spec key(s): {', '.join(bad_camera)}. "
                f"Allowed: {', '.join(CAMERA_SPEC_KEYS)}."
            )
        bad_conditions = [c for c in self.conditions_available if c not in CONDITION_LABELS]
        if bad_conditions:
            errors["conditions_available"] = (
                f"Unknown condition label(s): {', '.join(bad_conditions)}. "
                f"Allowed: {', '.join(CONDITION_LABELS)}."
            )
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model_name}")
        # For content models the slug IS the search-matching URL, so a silent
        # collision (samsung-galaxy-s24-1) is worse than a hard error.
        if Device.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError(
                {"slug": f"A device with slug '{self.slug}' already exists. Choose a distinct slug."}
            )
        super().save(*args, **kwargs)


class Comparison(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True,
        help_text="Must match natural search phrasing, e.g. 'galaxy-s24-vs-s24-ultra'.",
    )
    device_a = models.ForeignKey(Device, related_name="comparisons_as_a", on_delete=models.PROTECT)
    device_b = models.ForeignKey(Device, related_name="comparisons_as_b", on_delete=models.PROTECT)

    intro = models.TextField(
        help_text="Open with a direct 1–2 sentence verdict, not scene-setting.",
    )
    winner_by_category = models.JSONField(
        default=dict,
        help_text='{"camera": "a", "battery": "b", "display": "a", "value": "b", "performance": "a"}. Values: a / b / tie.',
    )
    overall_recommendation = models.TextField(
        help_text='Use if/then phrasing: "If you shoot video → A. If you want better value → B."',
    )

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["-published_at", "-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["device_a", "device_b"], name="unique_comparison_pair"
            ),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.device_a_id and self.device_b_id and self.device_a_id == self.device_b_id:
            raise ValidationError("A comparison must be between two different devices.")

        errors = {}
        bad_values = {
            k: v for k, v in self.winner_by_category.items() if v not in WINNER_VALUES
        }
        if bad_values:
            errors["winner_by_category"] = (
                f"Invalid winner value(s) {bad_values}. Allowed: {', '.join(WINNER_VALUES)}."
            )
        extra = [k for k in self.winner_by_category if k not in WINNER_CATEGORIES]
        if len(extra) > MAX_EXTRA_WINNER_CATEGORIES:
            errors.setdefault("winner_by_category", "")
            errors["winner_by_category"] += (
                f" Too many non-canonical categories ({', '.join(extra)}); "
                f"at most {MAX_EXTRA_WINNER_CATEGORIES} beyond {WINNER_CATEGORIES} allowed."
            )
        if errors:
            raise ValidationError(errors)

        # Reject the reversed pair existing as a separate row.
        if self.device_a_id and self.device_b_id:
            reversed_qs = Comparison.objects.filter(
                device_a_id=self.device_b_id, device_b_id=self.device_a_id
            ).exclude(pk=self.pk)
            if reversed_qs.exists():
                raise ValidationError(
                    "A comparison for the reversed device pair already exists. "
                    "Edit that one instead of creating a duplicate."
                )

    def _normalise_pair(self):
        """Store the pair in a deterministic (alphabetical by slug) order.

        When we swap the devices we must also swap every a/b winner value so the
        semantics stay correct. 'tie' is unaffected by the swap.
        """
        if not (self.device_a_id and self.device_b_id):
            return
        if self.device_a.slug > self.device_b.slug:
            self.device_a, self.device_b = self.device_b, self.device_a
            swap = {"a": "b", "b": "a"}
            self.winner_by_category = {
                k: swap.get(v, v) for k, v in self.winner_by_category.items()
            }

    def save(self, *args, **kwargs):
        self._normalise_pair()
        if self.published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class BuyingGuide(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    use_case_tag = models.ForeignKey(UseCaseTag, on_delete=models.PROTECT)

    intro = models.TextField(
        help_text="Open with a direct verdict/summary of who this guide is for.",
    )
    body = models.TextField(blank=True, help_text="Optional supplementary prose.")

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["-published_at", "-updated_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class BuyingGuideEntry(models.Model):
    guide = models.ForeignKey(BuyingGuide, related_name="entries", on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    rank = models.PositiveIntegerField()
    blurb = models.TextField(
        help_text='Why THIS device for THIS persona. Use if/then: "If you need the best camera → this one."',
    )

    class Meta:
        ordering = ["rank"]
        constraints = [
            models.UniqueConstraint(fields=["guide", "rank"], name="unique_guide_rank"),
            models.UniqueConstraint(fields=["guide", "device"], name="unique_guide_device"),
        ]

    def __str__(self):
        return f"#{self.rank} — {self.device}"


class FAQBlock(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "question"],
                name="unique_faq_per_object",
            ),
        ]

    def __str__(self):
        return self.question
