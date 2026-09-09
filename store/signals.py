import json
import logging
import threading
import urllib.parse
import urllib.request

from django.conf import settings
from django.db.models.signals import post_save, post_delete
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


def _revalidate_paths(paths):
    """POST to the Next.js on-demand ISR webhook so admin edits show up immediately
    instead of waiting out the 5-minute page cache."""
    secret = getattr(settings, "REVALIDATION_SECRET", "")
    url = getattr(settings, "REVALIDATION_URL", "")
    if not secret or not url:
        return

    def _ping():
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps({"secret": secret, "paths": paths}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as exc:
            logger.warning("Revalidation ping failed for %s: %s", paths, exc)

    threading.Thread(target=_ping, daemon=True).start()


@receiver(post_save, sender="store.Product")
def revalidate_on_product_save(sender, instance, **kwargs):
    """Any admin edit (visibility, price, stock, ...) should reflect on the
    storefront right away rather than waiting on ISR to expire."""
    paths = ["/", f"/category/{instance.category.slug}", f"/product/{instance.slug}"]
    if instance.is_one_time:
        paths.append("/offers")
    _revalidate_paths(paths)


@receiver(post_delete, sender="store.Product")
def revalidate_on_product_delete(sender, instance, **kwargs):
    paths = ["/", f"/category/{instance.category.slug}", "/offers"]
    _revalidate_paths(paths)
