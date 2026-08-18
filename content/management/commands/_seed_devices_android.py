"""
Samsung and Google device catalog — accurate manufacturer specifications.

PRICING: `price_band_ngn`, `conditions_available` and `is_in_stock` are left
empty on purpose. Fill from your own inventory before publishing.

Chipset note: Samsung ships different silicon by region. Canadian retail units
of the S24 and S25 families carry Snapdragon; European and most African retail
units carry Exynos. This is a real differentiator for a Canada-sourced seller
and it is stated per-device below — verify against the model number on each
unit before repeating the claim in a listing.
"""

SAMSUNG_DEVICES = [
    # ─── Galaxy S flagship line ──────────────────────────────────────────────
    {
        "brand": "Samsung",
        "model_name": "Galaxy S21",
        "slug": "samsung-galaxy-s21",
        "form_factor": "phone",
        "release_year": 2021,
        "chipset": "Snapdragon 888 (North America) / Exynos 2100 (global)",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.2 inches",
            "type": "Dynamic AMOLED 2X",
            "resolution": "2400 × 1080",
            "refresh_rate": "120Hz adaptive",
            "brightness": "1300 nits peak",
        },
        "camera_specs": {
            "main": "12MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "telephoto": "64MP f/2.0, 3× hybrid zoom",
            "front": "10MP f/2.2",
            "video": "8K30, 4K60",
        },
        "battery_capacity_mah": 4000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "120Hz flagship experience at what is now an entry-level price",
            "Compact 6.2-inch body that is easy to hold and pocket",
            "Snapdragon 888 on North American units is still capable in 2026",
            "IP68 rated",
        ],
        "cons": [
            "Plastic back panel, unlike the S21+ and S21 Ultra",
            "Software support has now ended — no more Android version upgrades",
            "1080p cap on the display, no QHD option",
            "Snapdragon 888 runs hot under sustained gaming",
        ],
        "verdict_summary": (
            "The Galaxy S21 is a cheap way into a 120Hz compact flagship, but its update "
            "window has closed. Buy it only if price is the deciding factor and you accept "
            "that security patches have stopped."
        ),
        "meta_description": (
            "Samsung Galaxy S21 in Nigeria: specs, the end of software support, and whether "
            "it is still worth buying used."
        ),
        "tag_slugs": ["budget-pick", "compact"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy S22 Ultra",
        "slug": "samsung-galaxy-s22-ultra",
        "form_factor": "phone",
        "release_year": 2022,
        "chipset": "Snapdragon 8 Gen 1 (North America) / Exynos 2200 (global)",
        "ram_options": ["8GB", "12GB"],
        "storage_options": ["128GB", "256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.8 inches",
            "type": "Dynamic AMOLED 2X, LTPO",
            "resolution": "3088 × 1440",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1750 nits peak",
        },
        "camera_specs": {
            "main": "108MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "telephoto": "10MP f/2.4, 3× optical",
            "telephoto_5x": "10MP f/4.9, 10× optical periscope",
            "front": "40MP f/2.2",
            "video": "8K24, 4K60",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "10× true optical periscope zoom — longer reach than any S24 or S25 Ultra",
            "Built-in S Pen with the lowest latency Samsung had shipped at the time",
            "First Ultra to adopt the Note design language",
            "45W charging",
        ],
        "cons": [
            "Snapdragon 8 Gen 1 is the least efficient flagship chip of its generation — it runs hot",
            "Battery drains faster than the S23 Ultra despite the same 5,000 mAh capacity",
            "Curved display edges cause accidental touches and cost more to replace",
        ],
        "verdict_summary": (
            "The Galaxy S22 Ultra is the cheapest way to get a true 10× optical periscope, "
            "which Samsung dropped after this generation. Buy it for zoom reach and the S Pen "
            "— avoid it if heat and battery drain would annoy you, because the 8 Gen 1 is the "
            "weak point."
        ),
        "meta_description": (
            "Samsung Galaxy S22 Ultra in Nigeria: 10x optical zoom, S Pen, and the "
            "Snapdragon 8 Gen 1 heat problem explained."
        ),
        "tag_slugs": ["photography", "big-screen", "s-pen", "budget-pick"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy S23",
        "slug": "samsung-galaxy-s23",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Snapdragon 8 Gen 2 for Galaxy",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Dynamic AMOLED 2X",
            "resolution": "2340 × 1080",
            "refresh_rate": "120Hz adaptive (48–120Hz)",
            "brightness": "1750 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "telephoto": "10MP f/2.4, 3× optical",
            "front": "12MP f/2.2",
            "video": "8K30, 4K60",
        },
        "battery_capacity_mah": 3900,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Snapdragon 8 Gen 2 for Galaxy on every unit worldwide — no Exynos lottery",
            "Far more efficient than the S22, so real battery life improved despite similar capacity",
            "Genuine 3× optical telephoto on a compact phone, which few rivals offer",
            "Four Android version upgrades from launch",
        ],
        "cons": [
            "3,900 mAh is small for heavy use",
            "25W charging is slow",
            "1080p display resolution",
        ],
        "verdict_summary": (
            "The Galaxy S23 is the compact Android to buy used if you want a real telephoto "
            "lens and guaranteed Snapdragon silicon. It is the most efficient small flagship "
            "Samsung has made — but if you stream or navigate all day, get a phone with a "
            "5,000 mAh battery instead."
        ),
        "meta_description": (
            "Samsung Galaxy S23 in Nigeria: Snapdragon 8 Gen 2, 3x optical zoom, compact "
            "size. Full specs and buying verdict."
        ),
        "tag_slugs": ["compact", "photography", "best-value"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy S23 Ultra",
        "slug": "samsung-galaxy-s23-ultra",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Snapdragon 8 Gen 2 for Galaxy",
        "ram_options": ["8GB", "12GB"],
        "storage_options": ["256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.8 inches",
            "type": "Dynamic AMOLED 2X, LTPO",
            "resolution": "3088 × 1440",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1750 nits peak",
        },
        "camera_specs": {
            "main": "200MP f/1.7, OIS",
            "ultra_wide": "12MP f/2.2",
            "telephoto": "10MP f/2.4, 3× optical",
            "telephoto_5x": "10MP f/4.9, 10× optical periscope",
            "front": "12MP f/2.2",
            "video": "8K30, 4K60",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "200MP main sensor plus a genuine 10× optical periscope — the most versatile zoom kit Samsung ever shipped",
            "Snapdragon 8 Gen 2 for Galaxy fixed the S22 Ultra's heat and battery problems",
            "Built-in S Pen",
            "Excellent night photography, a clear step up from the S22 Ultra",
        ],
        "cons": [
            "234g and physically large",
            "Curved edges are more fragile and costlier to repair than the flat S24 Ultra",
            "45W charging is slower than Chinese rivals at the same price",
        ],
        "verdict_summary": (
            "The Galaxy S23 Ultra is the best-value Ultra you can buy used in Nigeria. It has "
            "the 200MP sensor and the 10× periscope Samsung later removed, and none of the "
            "S22 Ultra's overheating — if zoom matters to you, this is the smart buy."
        ),
        "meta_description": (
            "Samsung Galaxy S23 Ultra in Nigeria: 200MP camera, 10x optical zoom, S Pen. "
            "Why it may be better value than the S24 Ultra."
        ),
        "tag_slugs": ["photography", "content-creator", "big-screen", "s-pen", "best-value"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy S24",
        "slug": "samsung-galaxy-s24",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Snapdragon 8 Gen 3 for Galaxy (Canada/US) / Exynos 2400 (Europe, Africa retail)",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.2 inches",
            "type": "Dynamic AMOLED 2X",
            "resolution": "2340 × 1080",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "2600 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "telephoto": "10MP f/2.4, 3× optical",
            "front": "12MP f/2.2",
            "video": "8K30, 4K60",
        },
        "battery_capacity_mah": 4000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Seven years of OS and security updates — the longest support of any Android at launch",
            "2,600-nit peak brightness makes it readable in direct sun",
            "Canada-sourced units carry Snapdragon 8 Gen 3, faster than the Exynos units sold in African retail",
            "Compact and genuinely one-hand usable",
        ],
        "cons": [
            "4,000 mAh battery is the weak point — heavy users will need a top-up by evening",
            "25W charging remains slow",
            "Galaxy AI features need an internet connection for most of the useful ones",
        ],
        "verdict_summary": (
            "The Galaxy S24 is the best compact Android to buy in Nigeria, and Canada-sourced "
            "units get the faster Snapdragon chip that African retail units do not. Buy it if "
            "you want flagship speed in a small body and a seven-year update runway."
        ),
        "meta_description": (
            "Samsung Galaxy S24 in Nigeria: Snapdragon vs Exynos explained, 7 years of "
            "updates, full specs and buying verdict."
        ),
        "tag_slugs": ["compact", "flagship", "best-value", "photography"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy S24 Ultra",
        "slug": "samsung-galaxy-s24-ultra",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Snapdragon 8 Gen 3 for Galaxy",
        "ram_options": ["12GB"],
        "storage_options": ["256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.8 inches",
            "type": "Dynamic AMOLED 2X, LTPO, flat with Gorilla Armor",
            "resolution": "3120 × 1440",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "2600 nits peak",
        },
        "camera_specs": {
            "main": "200MP f/1.7, OIS",
            "ultra_wide": "12MP f/2.2",
            "telephoto": "10MP f/2.4, 3× optical",
            "telephoto_5x": "50MP f/3.4, 5× optical periscope",
            "front": "12MP f/2.2",
            "video": "8K30, 4K120",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Gorilla Armor glass cuts reflections dramatically — the most usable screen outdoors of any phone",
            "Flat display instead of curved, so screen protectors fit properly and repairs cost less",
            "Titanium frame",
            "50MP 5× periscope crops to a very usable 10×, better detail than the S23 Ultra's 10× at most distances",
            "Seven years of updates",
        ],
        "cons": [
            "232g, heavy in the hand and in a pocket",
            "Dropped the true 10× optical lens the S22 and S23 Ultra had",
            "45W charging",
        ],
        "verdict_summary": (
            "The Galaxy S24 Ultra is the best all-round Android flagship for Nigerian "
            "conditions, mainly because the anti-reflective Gorilla Armor screen stays "
            "readable in harsh sunlight. Buy it for the camera system and the flat screen; "
            "skip it if you specifically want 10× optical, which the S23 Ultra still has."
        ),
        "meta_description": (
            "Samsung Galaxy S24 Ultra in Nigeria: 200MP camera, anti-glare Gorilla Armor "
            "screen, titanium build. Full specs and verdict."
        ),
        "tag_slugs": ["photography", "content-creator", "big-screen", "s-pen", "flagship", "gaming"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy S25 Ultra",
        "slug": "samsung-galaxy-s25-ultra",
        "form_factor": "phone",
        "release_year": 2025,
        "chipset": "Snapdragon 8 Elite for Galaxy",
        "ram_options": ["12GB", "16GB"],
        "storage_options": ["256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.9 inches",
            "type": "Dynamic AMOLED 2X, LTPO, flat with Gorilla Armor 2",
            "resolution": "3120 × 1440",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "2600 nits peak",
        },
        "camera_specs": {
            "main": "200MP f/1.7, OIS",
            "ultra_wide": "50MP f/1.9",
            "telephoto": "10MP f/2.4, 3× optical",
            "telephoto_5x": "50MP f/3.4, 5× optical periscope",
            "front": "12MP f/2.2",
            "video": "8K30, 4K120, Log recording",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "50MP ultra-wide replaces the old 12MP sensor — the biggest real camera upgrade over the S24 Ultra",
            "Snapdragon 8 Elite is substantially faster and cooler under sustained load",
            "218g, noticeably lighter than the S24 Ultra despite a larger screen",
            "Log video recording for colour grading in post",
        ],
        "cons": [
            "S Pen lost Bluetooth remote functions — no more air gestures or camera shutter",
            "Charging speed unchanged at 45W",
            "Very close to the S24 Ultra in daily use for a large price gap",
        ],
        "verdict_summary": (
            "The Galaxy S25 Ultra is the better phone, but the S24 Ultra is the better buy "
            "unless the upgraded 50MP ultra-wide and the lighter body matter to you. If you "
            "shoot a lot of wide shots or hold your phone for hours, the upgrade is real."
        ),
        "meta_description": (
            "Samsung Galaxy S25 Ultra in Nigeria: 50MP ultra-wide, Snapdragon 8 Elite, "
            "lighter body. Whether to buy it over the S24 Ultra."
        ),
        "tag_slugs": ["photography", "content-creator", "big-screen", "s-pen", "flagship", "gaming"],
    },
    # ─── Galaxy A mid-range line ─────────────────────────────────────────────
    {
        "brand": "Samsung",
        "model_name": "Galaxy A54 5G",
        "slug": "samsung-galaxy-a54-5g",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Exynos 1380",
        "ram_options": ["6GB", "8GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.4 inches",
            "type": "Super AMOLED",
            "resolution": "2340 × 1080",
            "refresh_rate": "120Hz",
            "brightness": "1000 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "macro": "5MP f/2.4",
            "front": "32MP f/2.2",
            "video": "4K30",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "5,000 mAh battery comfortably lasts a full day of heavy Nigerian use",
            "IP67 water and dust resistance, rare at this tier",
            "120Hz Super AMOLED with OIS on the main camera",
            "Four Android upgrades and five years of security patches",
            "microSD card slot",
        ],
        "cons": [
            "Exynos 1380 throttles noticeably in long gaming sessions",
            "25W charging with no charger in the box",
            "No headphone jack",
        ],
        "verdict_summary": (
            "The Galaxy A54 is the safest mid-range Android buy in Nigeria. Battery, screen, "
            "water resistance and update support are all better than anything else at its "
            "level — the only compromise is gaming performance."
        ),
        "meta_description": (
            "Samsung Galaxy A54 5G in Nigeria: 5000mAh battery, IP67, 120Hz AMOLED. Full "
            "specs and why it is the safest mid-range pick."
        ),
        "tag_slugs": ["best-value", "student", "battery-life", "budget-pick"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy A55 5G",
        "slug": "samsung-galaxy-a55-5g",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Exynos 1480",
        "ram_options": ["8GB", "12GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.6 inches",
            "type": "Super AMOLED, Gorilla Glass Victus+",
            "resolution": "2340 × 1080",
            "refresh_rate": "120Hz",
            "brightness": "1000 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "macro": "5MP f/2.4",
            "front": "32MP f/2.2",
            "video": "4K30",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Metal frame instead of plastic — feels a class above the A54",
            "Exynos 1480 with AMD RDNA graphics, a real gaming improvement over the A54",
            "Gorilla Glass Victus+ front, unusually tough for a mid-ranger",
            "Larger 6.6-inch screen",
        ],
        "cons": [
            "Heavier at 213g",
            "Still 25W charging",
            "Camera hardware is essentially unchanged from the A54",
        ],
        "verdict_summary": (
            "The Galaxy A55 is the A54 with a better frame and better graphics. If you game, "
            "the Exynos 1480 upgrade is worth paying for; if you don't, the A54 gives you the "
            "same cameras and battery for less."
        ),
        "meta_description": (
            "Samsung Galaxy A55 5G in Nigeria: metal frame, better gaming performance, and "
            "how it compares to the A54."
        ),
        "tag_slugs": ["best-value", "student", "battery-life", "gaming"],
    },
    {
        "brand": "Samsung",
        "model_name": "Galaxy A56 5G",
        "slug": "samsung-galaxy-a56-5g",
        "form_factor": "phone",
        "release_year": 2025,
        "chipset": "Exynos 1580",
        "ram_options": ["8GB", "12GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.7 inches",
            "type": "Super AMOLED, Gorilla Glass Victus+",
            "resolution": "2340 × 1080",
            "refresh_rate": "120Hz",
            "brightness": "1200 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.8, OIS",
            "ultra_wide": "12MP f/2.2",
            "macro": "5MP f/2.4",
            "front": "12MP f/2.2",
            "video": "4K30",
        },
        "battery_capacity_mah": 5000,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "45W charging at last — the A-series' longest-standing complaint finally addressed",
            "Six years of OS and security updates, matching some flagships",
            "Brighter 1,200-nit display",
            "Exynos 1580 is the fastest chip yet in this line",
        ],
        "cons": [
            "Front camera dropped from 32MP to 12MP",
            "Still no telephoto lens",
            "Recent enough that used stock is limited and priced close to new",
        ],
        "verdict_summary": (
            "The Galaxy A56 is the mid-range Android to buy if you want the longest support "
            "window and fast charging. Six years of updates at this price is the headline — "
            "but if charging speed doesn't bother you, the A54 is far better value."
        ),
        "meta_description": (
            "Samsung Galaxy A56 5G in Nigeria: 45W charging, six years of updates, 1200-nit "
            "screen. Full specs and verdict."
        ),
        "tag_slugs": ["best-value", "student", "battery-life"],
    },
]

GOOGLE_DEVICES = [
    {
        "brand": "Google",
        "model_name": "Pixel 7a",
        "slug": "google-pixel-7a",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Google Tensor G2",
        "ram_options": ["8GB"],
        "storage_options": ["128GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "OLED",
            "resolution": "2400 × 1080",
            "refresh_rate": "90Hz",
            "brightness": "1000 nits peak",
        },
        "camera_specs": {
            "main": "64MP f/1.89, OIS",
            "ultra_wide": "13MP f/2.2",
            "front": "13MP f/2.2",
            "video": "4K60",
        },
        "battery_capacity_mah": 4385,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Takes better photos than phones costing far more, thanks to Google's processing",
            "Clean Android with no duplicate apps or preinstalled bloat",
            "Magic Eraser and Photo Unblur make ordinary shots look edited",
            "Compact and light",
        ],
        "cons": [
            "Tensor G2 runs warm and is slower than Snapdragon rivals in raw performance",
            "Only 128GB and no microSD slot",
            "Update window is shorter than the Pixel 8 generation's seven years",
            "Google does not sell officially in Nigeria, so warranty is seller-provided only",
        ],
        "verdict_summary": (
            "The Pixel 7a is the cheapest way to get genuinely flagship-level photos. Buy it "
            "if photography is your priority and you accept average raw performance — this is "
            "a camera-first phone, not an all-rounder."
        ),
        "meta_description": (
            "Google Pixel 7a in Nigeria: flagship camera quality on a mid-range budget. Full "
            "specs, weaknesses, and who should buy it."
        ),
        "tag_slugs": ["photography", "budget-pick", "compact", "student"],
    },
    {
        "brand": "Google",
        "model_name": "Pixel 8",
        "slug": "google-pixel-8",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Google Tensor G3",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.2 inches",
            "type": "Actua OLED",
            "resolution": "2400 × 1080",
            "refresh_rate": "120Hz",
            "brightness": "2000 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.68, OIS",
            "ultra_wide": "12MP f/2.2 with autofocus and macro",
            "front": "10.5MP f/2.2",
            "video": "4K60, Audio Magic Eraser",
        },
        "battery_capacity_mah": 4575,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Seven years of OS and security updates from launch — through to 2030",
            "2,000-nit display, bright enough for direct sunlight",
            "Best-in-class computational photography and video processing",
            "Compact 6.2-inch body with a 120Hz screen",
        ],
        "cons": [
            "Tensor G3 lags Snapdragon 8 Gen 3 in games and sustained workloads",
            "No telephoto lens — that is reserved for the Pro",
            "27W charging",
        ],
        "verdict_summary": (
            "The Pixel 8 is the best compact camera phone with a long update runway. Buy it "
            "if you want great photos and seven years of software without paying flagship "
            "money — buy a Galaxy S24 instead if you game heavily."
        ),
        "meta_description": (
            "Google Pixel 8 in Nigeria: seven years of updates, 2000-nit screen, best-in-class "
            "camera processing. Specs and verdict."
        ),
        "tag_slugs": ["photography", "compact", "best-value"],
    },
    {
        "brand": "Google",
        "model_name": "Pixel 8a",
        "slug": "google-pixel-8a",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Google Tensor G3",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Actua OLED",
            "resolution": "2400 × 1080",
            "refresh_rate": "120Hz",
            "brightness": "2000 nits peak",
        },
        "camera_specs": {
            "main": "64MP f/1.89, OIS",
            "ultra_wide": "13MP f/2.2",
            "front": "13MP f/2.2",
            "video": "4K60",
        },
        "battery_capacity_mah": 4492,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Seven years of updates on a mid-range phone — nothing else at this price matches it",
            "Same Tensor G3 as the flagship Pixel 8, so AI photo features are identical",
            "120Hz 2,000-nit screen, a big jump over the Pixel 7a",
            "Best photo quality available at its price in Nigeria",
        ],
        "cons": [
            "Tensor G3 gets warm and throttles under load",
            "Plastic back",
            "18W charging is slow",
        ],
        "verdict_summary": (
            "The Pixel 8a takes the best photos of any mid-range phone sold in Nigeria and "
            "comes with a seven-year update promise. Buy it if the camera is your deciding "
            "factor — the Galaxy A54 wins on battery and gaming instead."
        ),
        "meta_description": (
            "Google Pixel 8a in Nigeria: best mid-range camera, seven years of updates, 120Hz "
            "screen. Full specs and honest verdict."
        ),
        "tag_slugs": ["photography", "budget-pick", "compact", "student", "best-value"],
    },
    {
        "brand": "Google",
        "model_name": "Pixel 9 Pro",
        "slug": "google-pixel-9-pro",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Google Tensor G4",
        "ram_options": ["16GB"],
        "storage_options": ["128GB", "256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.3 inches",
            "type": "Super Actua OLED, LTPO",
            "resolution": "2856 × 1280",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "3000 nits peak",
        },
        "camera_specs": {
            "main": "50MP f/1.68, OIS",
            "ultra_wide": "48MP f/1.7 with autofocus and macro",
            "telephoto_5x": "48MP f/2.8, 5× optical",
            "front": "42MP f/2.2 with autofocus",
            "video": "8K30 via Video Boost, 4K60",
        },
        "battery_capacity_mah": 4700,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "3,000-nit display, among the brightest phone screens available",
            "Full triple-camera system in a compact 6.3-inch body — rare combination",
            "16GB RAM enables on-device AI features other phones run in the cloud",
            "42MP front camera with autofocus is the best selfie camera on any phone",
            "Seven years of updates",
        ],
        "cons": [
            "Tensor G4 still trails Snapdragon on gaming and sustained performance",
            "Expensive, and Nigerian used supply is thin",
            "No official Google warranty or service presence in Nigeria",
        ],
        "verdict_summary": (
            "The Pixel 9 Pro is the best small flagship camera phone you can buy. If you want "
            "5× zoom, a triple camera and a bright screen without carrying a 6.9-inch slab, "
            "nothing else comes close — accept that gaming performance is not its strength."
        ),
        "meta_description": (
            "Google Pixel 9 Pro in Nigeria: 5x zoom in a compact body, 3000-nit screen, 42MP "
            "selfie camera. Full specs and verdict."
        ),
        "tag_slugs": ["photography", "content-creator", "compact", "flagship"],
    },
    {
        "brand": "Google",
        "model_name": "Pixel 9a",
        "slug": "google-pixel-9a",
        "form_factor": "phone",
        "release_year": 2025,
        "chipset": "Google Tensor G4",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB"],
        "display_specs": {
            "size": "6.3 inches",
            "type": "Actua OLED",
            "resolution": "2424 × 1080",
            "refresh_rate": "120Hz",
            "brightness": "2700 nits peak",
        },
        "camera_specs": {
            "main": "48MP f/1.7, OIS",
            "ultra_wide": "13MP f/2.2 with macro",
            "front": "13MP f/2.2",
            "video": "4K60",
        },
        "battery_capacity_mah": 5100,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "5,100 mAh — the largest battery Google has ever put in a Pixel",
            "Tensor G4 and seven years of updates at mid-range pricing",
            "Macro focus added to the ultra-wide lens",
            "IP68 rating, up from IP67 on the 8a",
        ],
        "cons": [
            "Main sensor is physically smaller than the Pixel 8a's, so low-light shots lost a little ground",
            "Flat, plainer design without the Pixel camera bar",
            "23W charging",
        ],
        "verdict_summary": (
            "The Pixel 9a is the Pixel to buy if battery life has been the thing stopping you. "
            "It trades a little low-light camera quality for a much bigger battery — a good "
            "swap for most people, but Pixel 8a still wins on pure photo quality."
        ),
        "meta_description": (
            "Google Pixel 9a in Nigeria: biggest ever Pixel battery, seven years of updates, "
            "and the camera trade-off versus the Pixel 8a."
        ),
        "tag_slugs": ["photography", "battery-life", "budget-pick", "student", "best-value"],
    },
]
