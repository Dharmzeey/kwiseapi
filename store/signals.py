from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender="swap.StorageVariant")
def sync_product_price(sender, instance, **kwargs):
    """When a StorageVariant's price changes, update any linked store Product."""
    try:
        product = instance.store_product
    except Exception:
        return
    if product and product.price != instance.uk_end_user_price_ngn:
        product.price = instance.uk_end_user_price_ngn
        product.save(update_fields=["price", "updated_at"])
