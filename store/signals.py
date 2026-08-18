import logging
import threading
import urllib.parse
import urllib.request

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


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


@receiver(post_save, sender="store.Product")
def ping_indexnow(sender, instance, **kwargs):
    """Notify Bing IndexNow whenever a visible product is saved."""
    key = getattr(settings, "INDEXNOW_KEY", "")
    if not key or not instance.is_visible:
        return

    product_url = f"https://kwiseworld.com/product/{instance.slug}"

    def _ping():
        endpoint = (
            "https://api.indexnow.org/indexnow"
            f"?url={urllib.parse.quote(product_url, safe='')}"
            f"&key={key}"
        )
        try:
            urllib.request.urlopen(endpoint, timeout=5)
        except Exception as exc:
            logger.warning("IndexNow ping failed for %s: %s", product_url, exc)

    threading.Thread(target=_ping, daemon=True).start()
