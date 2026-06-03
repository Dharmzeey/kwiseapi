"""
Kwise World — store models.

Hierarchy: Category → Brand → Product → ProductSpec / Review
Orders: Order → OrderItem
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """e.g. Phones, Laptops, Accessories"""
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="phone")  # matches Icon name in frontend
    blurb = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    """e.g. iPhone, Samsung, HP, Lenovo — scoped to a category"""
    category = models.ForeignKey(Category, related_name="brands", on_delete=models.CASCADE)
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = [("category", "slug")]
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class Product(models.Model):
    """A single product listing."""

    STATUS_CHOICES = [
        ("Brand New", "Brand New"),
        ("UK-Used", "UK-Used"),
        ("Nigeria-Used", "Nigeria-Used"),
    ]

    TINT_CHOICES = [
        ("blue", "Blue"),
        ("indigo", "Indigo"),
        ("orange", "Orange"),
    ]

    # Identity
    slug = models.SlugField(unique=True)     # e.g. "iphone-15-pro-max" — used as public ID
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.PROTECT)

    # Visual
    thumb = models.CharField(max_length=50, default="phone")  # icon name
    tint = models.CharField(max_length=20, choices=TINT_CHOICES, default="blue")

    # Pricing
    price = models.PositiveIntegerField()  # in Naira
    old_price = models.PositiveIntegerField(null=True, blank=True)

    # Condition
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="UK-Used")

    # Ratings (denormalised for query speed)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.6)
    review_count = models.PositiveIntegerField(default=0)

    # Flags
    is_featured = models.BooleanField(default=False)
    badge = models.CharField(max_length=50, blank=True)
    is_one_time = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=25)

    # Content
    description = models.TextField()
    one_time_note = models.TextField(blank=True)

    colors = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return self.name

    @property
    def sold_out(self):
        return self.is_one_time and self.stock <= 0

    @property
    def save_amount(self):
        if self.old_price:
            return self.old_price - self.price
        return None


class ProductSpec(models.Model):
    """Key-value specification row (e.g. Storage: 256GB)."""
    product = models.ForeignKey(Product, related_name="specs", on_delete=models.CASCADE)
    key = models.CharField(max_length=80)
    value = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        unique_together = [("product", "key")]

    def __str__(self):
        return f"{self.product_id}: {self.key} = {self.value}"


class Review(models.Model):
    """Customer review for a product."""
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reviews",
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer_name} → {self.product_id} ({self.rating}★)"


class Order(models.Model):
    """A customer order."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("dispatched", "Dispatched"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    reference = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    guest_name = models.CharField(max_length=150, blank=True)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    subtotal = models.PositiveIntegerField()
    delivery_fee = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    """A line item inside an Order."""
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)  # snapshot
    unit_price = models.PositiveIntegerField()         # snapshot
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.order.reference} — {self.product_name} x{self.quantity}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
