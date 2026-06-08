from django.db import models

from .pricing import compute_prices


class IphoneSeries(models.Model):
    name = models.CharField(max_length=20)  # e.g. "6", "7", "8", "X", "11" ... "17", "SE"
    order = models.PositiveIntegerField()   # 6=0, 7=1, 8=2, X=3, 11=4, 12=5, 13=6, 14=7, 15=8, 16=9, 17=10, SE=11
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "iPhone Series"
        ordering = ["order"]

    def __str__(self):
        return f"iPhone {self.name}"


class IphoneModel(models.Model):
    class VariantType(models.TextChoices):
        STANDARD = "standard", "Standard"
        S = "s", "S"
        S_PLUS = "s-plus", "S Plus"
        MINI = "mini", "Mini"
        PLUS = "plus", "Plus"
        PRO = "pro", "Pro"
        MAX = "max", "Max"
        AIR = "air", "Air"
        XR = "xr", "XR"

    series = models.ForeignKey(IphoneSeries, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=60)    # e.g. "iPhone 13 Pro Max"
    slug = models.SlugField(unique=True)       # e.g. "iphone-13-pro-max"
    variant_type = models.CharField(max_length=10, choices=VariantType.choices)
    order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["series__order", "order"]

    def __str__(self):
        return self.name


class StorageVariant(models.Model):
    class Capacity(models.TextChoices):
        GB_32 = "32GB", "32 GB"
        GB_64 = "64GB", "64 GB"
        GB_128 = "128GB", "128 GB"
        GB_256 = "256GB", "256 GB"
        GB_512 = "512GB", "512 GB"
        TB_1 = "1TB", "1 TB"
        TB_2 = "2TB", "2 TB"

    model = models.ForeignKey(IphoneModel, on_delete=models.CASCADE, related_name="storage_variants")
    capacity = models.CharField(max_length=10, choices=Capacity.choices)
    swap_in_value_ngn = models.PositiveIntegerField(
        help_text="What the shop pays when accepting this used phone (NGN). Update as market rates shift.",
    )
    uk_end_user_price_ngn = models.PositiveIntegerField(
        help_text="UK-condition end-user market price (NGN). Used as the swap-to price in estimates.",
    )
    uk_reseller_price_ngn = models.PositiveIntegerField(
        help_text="UK-condition reseller price (NGN).",
        null=True,
        blank=True,
    )
    ng_end_user_price_ngn = models.PositiveIntegerField(
        help_text="Nigerian-used end-user price after shop refurbishment (NGN).",
        null=True,
        blank=True,
    )
    ng_reseller_price_ngn = models.PositiveIntegerField(
        help_text="Nigerian-used reseller price (NGN).",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("model", "capacity")
        ordering = ["model__order", "capacity"]

    def __str__(self):
        return f"{self.model.name} · {self.capacity}"

    def save(self, *args, **kwargs):
        """Auto-recompute all derived price fields whenever uk_reseller_price_ngn is set."""
        if self.uk_reseller_price_ngn:
            p = compute_prices(self.model.slug, self.uk_reseller_price_ngn)
            self.uk_end_user_price_ngn = p["uk_end"]
            self.swap_in_value_ngn     = p["swap_in"]
            self.ng_reseller_price_ngn = p["ng_reseller"]
            self.ng_end_user_price_ngn = p["ng_end"]
            if "update_fields" in kwargs and kwargs["update_fields"] is not None:
                kwargs["update_fields"] = list(
                    set(kwargs["update_fields"]) | {
                        "uk_end_user_price_ngn",
                        "swap_in_value_ngn",
                        "ng_reseller_price_ngn",
                        "ng_end_user_price_ngn",
                    }
                )
        super().save(*args, **kwargs)


class DefectType(models.Model):
    class Category(models.TextChoices):
        DAMAGE = "damage", "Physical Damage"
        FUNCTIONAL = "functional", "Functional Issue"
        REPLACED_PART = "replaced_part", "Replaced Part"

    class AppliesTo(models.TextChoices):
        FRONT = "front", "Front"
        BACK = "back", "Back"
        BOTH = "both", "Both"

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    default_deduction_pct = models.PositiveIntegerField(
        help_text=(
            "Fallback % deducted from base_value_ngn when no per-model DefectPricing "
            "row exists. Multiplicative stacking: final = base × ∏(1 − pct/100)."
        ),
    )
    applies_to_view = models.CharField(
        max_length=5,
        choices=AppliesTo.choices,
        default=AppliesTo.BOTH,
        help_text="Controls which phone face shows the damage overlay in the UI.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} (default -{self.default_deduction_pct} %)"


class DefectPricing(models.Model):
    defect = models.ForeignKey(
        DefectType,
        on_delete=models.CASCADE,
        related_name="pricing",
    )
    iphone_model = models.ForeignKey(
        IphoneModel,
        on_delete=models.CASCADE,
        related_name="defect_pricing",
    )
    deduction_pct = models.PositiveIntegerField(
        help_text="% deducted from this model's base_value_ngn for this defect.",
    )
    repair_cost_ngn = models.PositiveIntegerField(
        help_text=(
            "Cost (NGN) to repair or replace this part on this model. "
            "Added on top of the swap difference — update whenever parts/labour prices change."
        ),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("defect", "iphone_model")
        ordering = ["iphone_model__series__order", "iphone_model__order", "defect__order"]
        verbose_name = "Defect Pricing"
        verbose_name_plural = "Defect Pricing"

    def __str__(self):
        return (
            f"{self.defect.name} on {self.iphone_model.name} — "
            f"-{self.deduction_pct}% / ₦{self.repair_cost_ngn:,} repair"
        )


class SwapEstimate(models.Model):
    """
    Logged estimate session — used for analytics and price tuning.
    """

    session_key = models.CharField(max_length=40, db_index=True)
    from_storage = models.ForeignKey(
        StorageVariant, on_delete=models.PROTECT, related_name="swap_from"
    )
    to_storage = models.ForeignKey(
        StorageVariant, on_delete=models.PROTECT, related_name="swap_to"
    )
    defects = models.ManyToManyField(DefectType, blank=True)

    from_base_value_ngn = models.PositiveIntegerField()
    from_value_ngn = models.PositiveIntegerField()
    total_repair_cost_ngn = models.PositiveIntegerField(default=0)
    to_value_ngn = models.PositiveIntegerField()
    service_fee_ngn = models.PositiveIntegerField()
    net_amount_ngn = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_storage} → {self.to_storage} ({self.created_at:%Y-%m-%d})"
