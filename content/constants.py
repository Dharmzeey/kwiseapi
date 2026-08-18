"""
Canonical vocabularies for the content app.

Single source of truth for the structured keys used across every Device,
Comparison, and BuyingGuide. Every Device spec dict, every Comparison winner
map, and every condition label validates against these — in the models
(`clean()`) and in the seed command. Keeping them fixed is what allows
SpecComparisonTable to render aligned rows across any device pair; ragged keys
are the single most common cause of a broken comparison table.
"""

# ── Form factors ────────────────────────────────────────────────────────────────
# `laptop` is a form factor, NOT a use-case tag.
FORM_FACTOR_PHONE = "phone"
FORM_FACTOR_LAPTOP = "laptop"
FORM_FACTOR_CHOICES = [
    (FORM_FACTOR_PHONE, "Phone"),
    (FORM_FACTOR_LAPTOP, "Laptop"),
]
FORM_FACTORS = [FORM_FACTOR_PHONE, FORM_FACTOR_LAPTOP]

# ── Device spec keys ────────────────────────────────────────────────────────────
# Order here is the render order in the comparison table.
DISPLAY_SPEC_KEYS = [
    "size",
    "type",
    "resolution",
    "refresh_rate",
    "brightness",
]

CAMERA_SPEC_KEYS = [
    "main",
    "ultra_wide",
    "telephoto",
    "telephoto_5x",
    "macro",
    "front",
    "video",
    "webcam",  # laptops only
]

# ── Winner categories ───────────────────────────────────────────────────────────
# Canonical winner categories for a phone comparison. A comparison may add at
# most two extra device-class-specific rows (e.g. "keyboard" for laptops).
WINNER_CATEGORIES = [
    "camera",
    "display",
    "battery",
    "performance",
    "value",
    "portability",
]

# Laptop comparisons swap "camera" for keyboard/webcam concerns.
LAPTOP_WINNER_CATEGORIES = [
    "display",
    "battery",
    "performance",
    "value",
    "portability",
]

# Extra rows a comparison may add beyond its canonical set.
ALLOWED_EXTRA_WINNER_CATEGORIES = [
    "keyboard",
    "webcam",
    "upgradeability",
    "video quality",
    "software support",
]

# How many bespoke winner categories a comparison may add beyond the canonical set.
MAX_EXTRA_WINNER_CATEGORIES = 2

# Allowed values for each winner_by_category entry.
WINNER_VALUES = ["a", "b", "tie"]

# ── Conditions ──────────────────────────────────────────────────────────────────
# Grading vocabulary. Definitions live on the /grading reference page —
# every device page should link to it.
CONDITION_LABELS = [
    "Grade A+",
    "Grade A",
    "Grade B",
    "Grade C",
]
