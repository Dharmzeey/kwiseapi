"""
Auto-link store.Product records to swap.StorageVariant records.

Product names follow the pattern  "{IphoneModel.name} {capacity}"
e.g. "iPhone 15 Pro Max 256GB"  →  model.name="iPhone 15 Pro Max", capacity="256GB"

Usage:
    python manage.py link_storage_variants           # dry-run (shows what would change)
    python manage.py link_storage_variants --apply   # actually saves the links
    python manage.py link_storage_variants --unlink  # removes all existing links (--apply required)
"""

from django.core.management.base import BaseCommand

from store.models import Product
from swap.models import StorageVariant


class Command(BaseCommand):
    help = "Auto-link store Products to swap StorageVariants by matching name + capacity."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Save changes to the database. Without this flag the command only reports.",
        )
        parser.add_argument(
            "--unlink",
            action="store_true",
            help="Remove all existing storage_variant links (requires --apply).",
        )

    def handle(self, *args, **options):
        apply  = options["apply"]
        unlink = options["unlink"]

        if unlink:
            qs = Product.objects.filter(storage_variant__isnull=False)
            self.stdout.write(f"Would unlink {qs.count()} product(s).")
            if apply:
                qs.update(storage_variant=None)
                self.stdout.write(self.style.WARNING("All links removed."))
            return

        # Build a lookup:  "{model.name} {capacity}" → StorageVariant
        variant_map = {
            f"{sv.model.name} {sv.capacity}": sv
            for sv in StorageVariant.objects.select_related("model").filter(is_active=True)
        }

        linked = skipped = already = unmatched = 0
        claimed = set()  # variant PKs assigned this run — prevents OneToOne conflicts

        # "Brand New" / "Foreign Used" sort before "Nigeria-Used" — they win the slot
        for product in Product.objects.select_related("storage_variant").order_by("status"):
            name = product.name.strip()

            # Skip non-iPhone products that obviously won't match
            if not name.startswith("iPhone"):
                skipped += 1
                continue

            variant = variant_map.get(name)

            if variant is None:
                self.stdout.write(self.style.WARNING(f"  no match : {name!r}"))
                unmatched += 1
                continue

            if product.storage_variant_id == variant.pk:
                claimed.add(variant.pk)
                already += 1
                continue

            if variant.pk in claimed:
                self.stdout.write(self.style.WARNING(f"  conflict : {name!r} (variant already claimed)"))
                skipped += 1
                continue

            claimed.add(variant.pk)
            self.stdout.write(f"  link     : {name!r}  ->  {variant}")
            linked += 1

            if apply:
                product.storage_variant = variant
                product.save(update_fields=["storage_variant"])

        mode = "Linked" if apply else "Would link"
        self.stdout.write(self.style.SUCCESS(
            f"\n{mode} {linked} | already linked {already} | "
            f"no match {unmatched} | skipped (non-iPhone) {skipped}"
        ))
        if not apply:
            self.stdout.write("  re-run with --apply to save.")
