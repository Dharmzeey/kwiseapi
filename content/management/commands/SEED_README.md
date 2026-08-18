# Kwise World production seed — what you need to do before running it

**38 devices · 16 comparisons · 12 buying guides · 57 ranked guide entries · 63 FAQs**

All specifications are from manufacturer documentation. All prices are blank on purpose.

---

## 1. Required model changes first

The seed uses three fields that don't exist yet. Add them, migrate, then seed:

```python
# Device
form_factor = models.CharField(max_length=10, choices=[("phone","Phone"),("laptop","Laptop")])
battery_wh  = models.PositiveIntegerField(null=True, blank=True)  # laptops publish Wh, not mAh
meta_description = models.CharField(max_length=160, blank=True)
```

Also apply the constraints from the earlier fix list — in particular the `(device_a, device_b)`
uniqueness on `Comparison` and `(guide, device)` on `BuyingGuideEntry`. The seed's validator
already enforces both, so a migration adding them will apply cleanly against seeded data.

Drop `price_band_cad` if you're Nigeria-only. Nothing in this seed writes to it.

---

## 2. What you must fill in

Three fields are deliberately empty on **every** device, because getting them wrong is worse
than leaving them blank — they feed `Product` structured data, and wrong prices or false
availability in schema is actively harmful:

| Field | What to put |
|---|---|
| `price_band_ngn` | Your real band, e.g. `"₦480,000 – ₦550,000"` |
| `conditions_available` | Subset of `["Grade A+", "Grade A", "Grade B", "Grade C"]` |
| `is_in_stock` | `True` only when actually stocked |

Also: **both author records are `TODO` placeholders.** Author bios are E-E-A-T signals — put
real names, real years in business, real testing process. Understate rather than overstate.

The command warns about all of these on every run and refuses to publish quietly.

---

## 3. Run order

```bash
python manage.py seed_content --dry-run    # validates, writes nothing
python manage.py seed_content              # writes everything UNPUBLISHED
# ... fill prices, conditions, stock, author bios in Django admin ...
python manage.py seed_content --publish    # re-run to publish
```

`--flush` wipes all content rows first, for clean dev resets. The command is fully idempotent
and wrapped in a single transaction — a failure writes nothing.

---

## 4. Verify before publishing

These are accurate as written but worth a second check, because they're the kind of thing that
changes or that I'd want you to confirm against a unit in hand:

- **Snapdragon vs Exynos on Canadian S24/S25 units.** Stated repeatedly across the seed as a
  selling point. Confirm against the model number on your actual stock — it's a strong
  differentiator, so it's worth being certain.
- **eSIM support by Nigerian network.** The seed deliberately says support "varies and has been
  expanding" rather than naming operators, because this changes. Check current status per network.
- **Nigerian LTE bands.** Seed cites band 3 (1800MHz) and band 7 (2600MHz) as carrying most 4G
  traffic. Confirm against current operator deployments.
- **iOS/Android version support windows.** Written as "check the current list" rather than naming
  versions, so they won't go stale — but verify before writing anything more specific.
- **iPhone 17 / 17 Pro Max.** Released after my reliable knowledge cutoff; specs here are from
  Apple and GSMArena, including the 4,832 mAh figure that applies to the physical-SIM (Canadian)
  variant specifically. Double-check if you list one.
- **Galaxy S26 family is deliberately excluded.** Sources conflicted on charging speed and the
  ultra-wide sensor. Add it once you have a unit and can verify.

---

## 5. Design decisions worth knowing

**No naira figures in any guide title or slug.** Price-anchored titles ("under ₦300,000") go stale
the moment the rate moves and force you to re-edit every guide — and they create the contradiction
your old seed had, where an out-of-budget phone was ranked inside a budget guide. Prices live on
device pages only.

**No years in slugs.** `best-camera-phone-in-nigeria`, not `-2024`. Undated slugs age without
redirect churn; the visible `updated_at` badge carries freshness.

**`laptop` is no longer a use-case tag.** It's `form_factor` on Device. That's why the student
laptop guide now correctly files under `student` and will surface in that persona.

**Comparison slugs match search phrasing exactly** — `galaxy-s24-vs-s24-ultra`, not a formal
product name. Don't "tidy" these; matching how people type is most of the value.

**Every `intro` and `overall_recommendation` leads with the verdict** and uses if/then phrasing.
That's the format AI answer engines lift most cleanly.

**The Nigeria-specific FAQs are the highest-value content here.** Carrier lock checks, battery
health thresholds, iCloud Activation Lock, off-lease laptop provenance, Canadian SIM tray
differences — this is knowledge that isn't published anywhere else in this form, and it's what
will get you cited rather than a spec rewrite of GSMArena.

---

## 6. Files

```
content/constants.py                                  spec key + category vocabularies
content/management/commands/
    seed_content.py                                   the command (validation, flags, idempotency)
    _seed_devices_apple.py                            14 Apple devices
    _seed_devices_android.py                          10 Samsung, 5 Google
    _seed_devices_laptops.py                          9 laptops
    _seed_comparisons.py                              authors, 16 tags, 16 comparisons
    _seed_guides.py                                   12 guides + Nigeria-specific device FAQs
```

Data is split from logic so you can edit prices and copy without touching the command.
