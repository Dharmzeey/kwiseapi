"""
Management command: python manage.py seed_content

Populates the content app with the real device catalog, comparisons and buying
guides. Idempotent — safe to re-run. Every write is inside a single transaction,
so a failure leaves the database untouched rather than half-seeded.

Usage:
    python manage.py seed_content --dry-run     validate everything, write nothing
    python manage.py seed_content               create or update all content
    python manage.py seed_content --flush       delete all seeded content first
    python manage.py seed_content --publish     also mark everything published

By default nothing is published. Devices ship with empty price bands and
is_in_stock=False, so publishing before you fill those in would put empty
prices and false availability into Product JSON-LD. Fill prices, then run with
--publish or flip the flags in Django admin.
"""
import sys

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from content.constants import (
    ALLOWED_EXTRA_WINNER_CATEGORIES,
    CAMERA_SPEC_KEYS,
    CONDITION_LABELS,
    DISPLAY_SPEC_KEYS,
    FORM_FACTORS,
    LAPTOP_WINNER_CATEGORIES,
    WINNER_CATEGORIES,
    WINNER_VALUES,
)
from content.models import (
    Author,
    BuyingGuide,
    BuyingGuideEntry,
    Comparison,
    Device,
    FAQBlock,
    UseCaseTag,
)

from ._seed_comparisons import AUTHORS, COMPARISONS, USE_CASE_TAGS
from ._seed_devices_android import GOOGLE_DEVICES, SAMSUNG_DEVICES
from ._seed_devices_apple import APPLE_DEVICES
from ._seed_devices_laptops import LAPTOP_DEVICES
from ._seed_guides import BUYING_GUIDES, DEVICE_FAQS

ALL_DEVICES = APPLE_DEVICES + SAMSUNG_DEVICES + GOOGLE_DEVICES + LAPTOP_DEVICES


class Command(BaseCommand):
    help = "Seed the content app with the device catalog, comparisons and buying guides."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Validate all seed data and report problems without writing anything.",
        )
        parser.add_argument(
            "--flush", action="store_true",
            help="Delete all existing content records before seeding.",
        )
        parser.add_argument(
            "--publish", action="store_true",
            help="Mark seeded content as published. Only use once prices are filled in.",
        )

    # ── validation ──────────────────────────────────────────────────────────
    def validate(self):
        errors = []
        device_slugs = set()
        tag_slugs = {t["slug"] for t in USE_CASE_TAGS}
        author_slugs = {a["slug"] for a in AUTHORS}

        for d in ALL_DEVICES:
            slug = d.get("slug", "<missing slug>")

            if slug in device_slugs:
                errors.append(f"device '{slug}': duplicate slug")
            device_slugs.add(slug)

            if d.get("form_factor") not in FORM_FACTORS:
                errors.append(f"device '{slug}': form_factor must be one of {FORM_FACTORS}")

            for key in d.get("display_specs", {}):
                if key not in DISPLAY_SPEC_KEYS:
                    errors.append(f"device '{slug}': unknown display_specs key '{key}'")

            for key in d.get("camera_specs", {}):
                if key not in CAMERA_SPEC_KEYS:
                    errors.append(f"device '{slug}': unknown camera_specs key '{key}'")

            for label in d.get("conditions_available", []):
                if label not in CONDITION_LABELS:
                    errors.append(f"device '{slug}': unknown condition label '{label}'")

            for ts in d.get("tag_slugs", []):
                if ts not in tag_slugs:
                    errors.append(f"device '{slug}': references unknown tag '{ts}'")

            meta = d.get("meta_description", "")
            if len(meta) > 160:
                errors.append(f"device '{slug}': meta_description is {len(meta)} chars (max 160)")

        comparison_slugs = set()
        for c in COMPARISONS:
            slug = c.get("slug", "<missing slug>")

            if slug in comparison_slugs:
                errors.append(f"comparison '{slug}': duplicate slug")
            comparison_slugs.add(slug)

            for key in ("device_a_slug", "device_b_slug"):
                if c[key] not in device_slugs:
                    errors.append(f"comparison '{slug}': references unknown device '{c[key]}'")

            if c["device_a_slug"] == c["device_b_slug"]:
                errors.append(f"comparison '{slug}': device_a and device_b are the same")

            # reversed-pair duplicate check
            reverse = (c["device_b_slug"], c["device_a_slug"])
            if reverse in {(x["device_a_slug"], x["device_b_slug"]) for x in COMPARISONS}:
                errors.append(
                    f"comparison '{slug}': a reversed duplicate of this device pair also exists"
                )

            if c["author_slug"] not in author_slugs:
                errors.append(f"comparison '{slug}': unknown author '{c['author_slug']}'")

            device_map = {d["slug"]: d for d in ALL_DEVICES}
            form_a = device_map.get(c["device_a_slug"], {}).get("form_factor")
            canonical = (
                LAPTOP_WINNER_CATEGORIES if form_a == "laptop" else WINNER_CATEGORIES
            )
            extras = [k for k in c["winner_by_category"] if k not in canonical]
            unknown_extras = [k for k in extras if k not in ALLOWED_EXTRA_WINNER_CATEGORIES]
            if unknown_extras:
                errors.append(
                    f"comparison '{slug}': unknown winner categories {unknown_extras}"
                )
            if len(extras) > 2:
                errors.append(
                    f"comparison '{slug}': {len(extras)} extra winner categories (max 2)"
                )
            for cat, val in c["winner_by_category"].items():
                if val not in WINNER_VALUES:
                    errors.append(
                        f"comparison '{slug}': category '{cat}' has value '{val}', "
                        f"expected one of {WINNER_VALUES}"
                    )

            if len(c.get("meta_description", "")) > 160:
                errors.append(f"comparison '{slug}': meta_description exceeds 160 chars")

        guide_slugs = set()
        for g in BUYING_GUIDES:
            slug = g.get("slug", "<missing slug>")

            if slug in guide_slugs:
                errors.append(f"guide '{slug}': duplicate slug")
            guide_slugs.add(slug)

            if g["use_case_slug"] not in tag_slugs:
                errors.append(f"guide '{slug}': unknown use_case tag '{g['use_case_slug']}'")

            if g["author_slug"] not in author_slugs:
                errors.append(f"guide '{slug}': unknown author '{g['author_slug']}'")

            ranks, devices_seen = set(), set()
            for e in g["entries"]:
                if e["device_slug"] not in device_slugs:
                    errors.append(f"guide '{slug}': references unknown device '{e['device_slug']}'")
                if e["rank"] in ranks:
                    errors.append(f"guide '{slug}': duplicate rank {e['rank']}")
                ranks.add(e["rank"])
                if e["device_slug"] in devices_seen:
                    errors.append(f"guide '{slug}': device '{e['device_slug']}' listed twice")
                devices_seen.add(e["device_slug"])

            if len(g.get("meta_description", "")) > 160:
                errors.append(f"guide '{slug}': meta_description exceeds 160 chars")

        for slug in DEVICE_FAQS:
            if slug not in device_slugs:
                errors.append(f"DEVICE_FAQS: references unknown device '{slug}'")

        return errors

    # ── warnings (non-fatal) ────────────────────────────────────────────────
    def warnings(self):
        warns = []
        for d in ALL_DEVICES:
            if not d.get("price_band_ngn"):
                warns.append(f"device '{d['slug']}': price_band_ngn is empty")
            if not d.get("conditions_available"):
                warns.append(f"device '{d['slug']}': conditions_available is empty")
        for a in AUTHORS:
            if "TODO" in a["name"] or "TODO" in a["bio"]:
                warns.append(f"author '{a['slug']}': still contains TODO placeholder text")
        return warns

    # ── helpers ─────────────────────────────────────────────────────────────
    def sync_faqs(self, obj, faqs):
        """Create or update FAQ blocks for any object, keyed on question text."""
        ct = ContentType.objects.get_for_model(obj.__class__)
        for faq in faqs:
            FAQBlock.objects.update_or_create(
                content_type=ct,
                object_id=obj.pk,
                question=faq["question"],
                defaults={"answer": faq["answer"], "order": faq["order"]},
            )

    def flush(self):
        for model in (BuyingGuideEntry, BuyingGuide, Comparison, FAQBlock, Device,
                      UseCaseTag, Author):
            count = model.objects.all().delete()[0]
            self.stdout.write(f"  Deleted {count} {model.__name__} rows")

    # ── main ────────────────────────────────────────────────────────────────
    def handle(self, *args, **options):
        # This output uses ✓ ✗ … ! ₦ etc. Windows consoles default to cp1252 and
        # would crash on those characters mid-run. Force UTF-8 so the progress log
        # never aborts a seed.
        for stream in (sys.stdout, sys.stderr):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass

        dry_run = options["dry_run"]
        publish = options["publish"]

        self.stdout.write("Validating seed data…")
        errors = self.validate()
        if errors:
            for e in errors:
                self.stdout.write(self.style.ERROR(f"  ✗ {e}"))
            raise CommandError(f"{len(errors)} validation error(s). Nothing was written.")
        self.stdout.write(self.style.SUCCESS("  ✓ validation passed"))

        for w in self.warnings():
            self.stdout.write(self.style.WARNING(f"  ! {w}"))

        if dry_run:
            self.stdout.write(self.style.SUCCESS("\nDry run complete. No changes written."))
            return

        if publish:
            self.stdout.write(self.style.WARNING(
                "\n--publish is set. Confirm prices and stock flags are correct — these feed "
                "Product structured data."
            ))

        now = timezone.now()

        with transaction.atomic():
            if options["flush"]:
                self.stdout.write("\nFlushing existing content…")
                self.flush()

            # 1. Authors
            self.stdout.write("\nAuthors…")
            authors = {}
            for a in AUTHORS:
                obj, created = Author.objects.update_or_create(
                    slug=a["slug"],
                    defaults={k: v for k, v in a.items() if k != "slug"},
                )
                authors[a["slug"]] = obj
                self.stdout.write(f"  {'+' if created else '~'} {obj.name}")

            # 2. Use-case tags
            self.stdout.write("\nUse-case tags…")
            tags = {}
            for t in USE_CASE_TAGS:
                obj, created = UseCaseTag.objects.update_or_create(
                    slug=t["slug"],
                    defaults={k: v for k, v in t.items() if k != "slug"},
                )
                tags[t["slug"]] = obj
                self.stdout.write(f"  {'+' if created else '~'} {obj.name}")

            # 3. Devices
            self.stdout.write("\nDevices…")
            devices = {}
            for raw in ALL_DEVICES:
                d = dict(raw)                     # never mutate the source data
                tag_slugs = d.pop("tag_slugs", [])
                slug = d.pop("slug")
                d["published"] = publish
                obj, created = Device.objects.update_or_create(slug=slug, defaults=d)
                obj.use_case_tags.set([tags[ts] for ts in tag_slugs])
                devices[slug] = obj
                self.stdout.write(f"  {'+' if created else '~'} {obj}")

            # 4. Comparisons
            self.stdout.write("\nComparisons…")
            for raw in COMPARISONS:
                c = dict(raw)
                faqs = c.pop("faqs", [])
                slug = c.pop("slug")
                c["device_a"] = devices[c.pop("device_a_slug")]
                c["device_b"] = devices[c.pop("device_b_slug")]
                c["author"] = authors[c.pop("author_slug")]
                c["published"] = publish
                if publish:
                    c["published_at"] = now
                obj, created = Comparison.objects.update_or_create(slug=slug, defaults=c)
                self.sync_faqs(obj, faqs)
                self.stdout.write(f"  {'+' if created else '~'} {obj.title}")

            # 5. Buying guides
            self.stdout.write("\nBuying guides…")
            for raw in BUYING_GUIDES:
                g = dict(raw)
                faqs = g.pop("faqs", [])
                entries = g.pop("entries", [])
                slug = g.pop("slug")
                g["use_case_tag"] = tags[g.pop("use_case_slug")]
                g["author"] = authors[g.pop("author_slug")]
                g["published"] = publish
                if publish:
                    g["published_at"] = now
                obj, created = BuyingGuide.objects.update_or_create(slug=slug, defaults=g)

                # Entries are replaced wholesale so ranks can be reordered safely
                # without tripping the (guide, rank) uniqueness constraint.
                obj.entries.all().delete()
                for e in entries:
                    BuyingGuideEntry.objects.create(
                        guide=obj,
                        device=devices[e["device_slug"]],
                        rank=e["rank"],
                        blurb=e["blurb"],
                    )
                self.sync_faqs(obj, faqs)
                self.stdout.write(f"  {'+' if created else '~'} {obj.title} ({len(entries)} entries)")

            # 6. Device-level FAQs
            self.stdout.write("\nDevice FAQs…")
            for slug, faqs in DEVICE_FAQS.items():
                self.sync_faqs(devices[slug], faqs)
                self.stdout.write(f"  ~ {devices[slug]} ({len(faqs)} FAQs)")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {len(ALL_DEVICES)} devices, {len(COMPARISONS)} comparisons, "
            f"{len(BUYING_GUIDES)} guides."
        ))
        if not publish:
            self.stdout.write(
                "Everything is unpublished. Fill in price_band_ngn, conditions_available "
                "and is_in_stock, then re-run with --publish."
            )
