"""
Post-save/delete signals that fire the Next.js revalidation webhook
whenever published content changes.
"""
import logging

import requests
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import BuyingGuide, Comparison, Device

logger = logging.getLogger(__name__)


def _revalidate(paths: list[str]) -> None:
    secret = getattr(settings, "REVALIDATION_SECRET", "")
    url = getattr(settings, "REVALIDATION_URL", "")
    if not secret or not url:
        return
    try:
        requests.post(url, json={"secret": secret, "paths": paths}, timeout=5)
    except Exception as exc:
        logger.warning("Revalidation webhook failed: %s", exc)


@receiver([post_save, post_delete], sender=Device)
def on_device_change(sender, instance, **kwargs):
    if not instance.published:
        return
    _revalidate([f"/phones/{instance.slug}", "/phones"])


@receiver([post_save, post_delete], sender=Comparison)
def on_comparison_change(sender, instance, **kwargs):
    if not instance.published:
        return
    _revalidate([f"/compare/{instance.slug}", "/compare"])


@receiver([post_save, post_delete], sender=BuyingGuide)
def on_guide_change(sender, instance, **kwargs):
    if not instance.published:
        return
    _revalidate([f"/guides/{instance.slug}", "/guides"])
