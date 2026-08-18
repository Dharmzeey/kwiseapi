"""
Laptop catalog — Canadian corporate off-lease models, the actual supply channel.

Battery is recorded in `battery_wh` (watt-hours), not mAh. Laptop manufacturers
publish Wh; converting to mAh is meaningless without the cell voltage, so the
Device model needs a separate `battery_wh` field (see the fix list).

`camera_specs` carries only a `webcam` key for laptops. The comparison table
should skip empty rows rather than render blanks.

PRICING: left empty deliberately. Configurations vary enormously in off-lease
stock, so price bands should be set per SKU from your own inventory.
"""

LAPTOP_DEVICES = [
    # ─── Lenovo ThinkPad ─────────────────────────────────────────────────────
    {
        "brand": "Lenovo",
        "model_name": "ThinkPad X13 Gen 3",
        "slug": "lenovo-thinkpad-x13-gen-3",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Intel Core i5-1235U / i7-1265U (12th gen)",
        "ram_options": ["16GB", "32GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "13.3 inches",
            "type": "IPS anti-glare, 16:10",
            "resolution": "1920 × 1200",
            "refresh_rate": "60Hz",
            "brightness": "300–400 nits depending on panel",
        },
        "camera_specs": {
            "webcam": "1080p with optional IR for Windows Hello, ThinkShutter privacy cover",
        },
        "battery_capacity_mah": None,
        "battery_wh": 54,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Best keyboard on any laptop in this price range — the reason ThinkPads keep their reputation",
            "16:10 display shows more of a document or code file than a 16:9 panel",
            "Passes MIL-STD-810H durability testing",
            "Around 1.2–1.3kg, easy to carry all day",
            "Physical webcam shutter, which matters if you take client calls",
        ],
        "cons": [
            "Integrated Iris Xe graphics only — not for video editing or 3D work",
            "Soldered RAM on most configurations, so check the spec before buying, you cannot upgrade later",
            "12th gen U-series chips throttle under long sustained loads",
            "13.3 inches is tight if you work in wide spreadsheets",
        ],
        "verdict_summary": (
            "The ThinkPad X13 Gen 3 is the best laptop to buy if you type all day and move "
            "around. Keyboard, build quality and weight are all class-leading — just confirm "
            "the RAM configuration before you pay, because it usually cannot be upgraded."
        ),
        "meta_description": (
            "Lenovo ThinkPad X13 Gen 3 in Nigeria: best-in-class keyboard, 16:10 screen, "
            "MIL-STD build. Specs, weaknesses and buying verdict."
        ),
        "tag_slugs": ["laptop-portable", "student", "business", "developer"],
    },
    {
        "brand": "Lenovo",
        "model_name": "ThinkPad T14 Gen 3",
        "slug": "lenovo-thinkpad-t14-gen-3",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Intel Core i5-1240P / i7-1260P (12th gen)",
        "ram_options": ["16GB", "32GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "14 inches",
            "type": "IPS anti-glare, 16:10",
            "resolution": "1920 × 1200",
            "refresh_rate": "60Hz",
            "brightness": "300–400 nits depending on panel",
        },
        "camera_specs": {
            "webcam": "1080p with optional IR, ThinkShutter privacy cover",
        },
        "battery_capacity_mah": None,
        "battery_wh": 52,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "P-series chips give substantially more sustained performance than U-series X13 units",
            "One SO-DIMM slot on many configurations, so RAM can often be upgraded",
            "14-inch 16:10 screen is the best size-to-portability balance for most work",
            "Same excellent ThinkPad keyboard",
        ],
        "cons": [
            "P-series runs hot and the fan is audible under load",
            "Battery life is shorter than the X13 because of the faster chip",
            "Around 1.4kg, heavier than the X13",
        ],
        "verdict_summary": (
            "The ThinkPad T14 Gen 3 is the pick over the X13 if you compile code, run virtual "
            "machines or keep dozens of tabs open. You trade battery life and a little weight "
            "for real sustained performance — and often the ability to add RAM later."
        ),
        "meta_description": (
            "Lenovo ThinkPad T14 Gen 3 in Nigeria: P-series performance, upgradeable RAM, "
            "14-inch 16:10 screen. Specs and verdict."
        ),
        "tag_slugs": ["laptop-portable", "developer", "business", "student"],
    },
    {
        "brand": "Lenovo",
        "model_name": "ThinkPad X1 Carbon Gen 10",
        "slug": "lenovo-thinkpad-x1-carbon-gen-10",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Intel Core i5-1240P / i7-1260P (12th gen)",
        "ram_options": ["16GB", "32GB"],
        "storage_options": ["512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "14 inches",
            "type": "IPS or OLED, 16:10",
            "resolution": "1920 × 1200 up to 2880 × 1800",
            "refresh_rate": "60Hz",
            "brightness": "400 nits on the brighter IPS panels",
        },
        "camera_specs": {
            "webcam": "1080p with IR, computer vision presence detection, ThinkShutter",
        },
        "battery_capacity_mah": None,
        "battery_wh": 57,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Around 1.12kg — the lightest serious business laptop in this channel",
            "Carbon fibre and magnesium chassis, both light and rigid",
            "Higher-resolution panel options including OLED",
            "Four-speaker Dolby Atmos audio, unusually good for a business machine",
        ],
        "cons": [
            "Soldered RAM on every configuration — buy the capacity you need up front",
            "Commands a price premium over the T14 for similar performance",
            "Thin chassis limits sustained performance under long loads",
        ],
        "verdict_summary": (
            "The X1 Carbon Gen 10 is the one to buy if weight is your top priority and budget "
            "allows. It is the lightest way to carry a full 14-inch business laptop — but you "
            "pay a premium over a T14 that performs the same or better."
        ),
        "meta_description": (
            "ThinkPad X1 Carbon Gen 10 in Nigeria: 1.12kg carbon fibre build, OLED option, "
            "premium business laptop. Specs and verdict."
        ),
        "tag_slugs": ["laptop-portable", "business", "developer"],
    },
    # ─── Dell Latitude ───────────────────────────────────────────────────────
    {
        "brand": "Dell",
        "model_name": "Latitude 5530",
        "slug": "dell-latitude-5530",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Intel Core i5-1245U / i7-1265U (12th gen)",
        "ram_options": ["8GB", "16GB", "32GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "15.6 inches",
            "type": "IPS anti-glare, 16:9",
            "resolution": "1920 × 1080",
            "refresh_rate": "60Hz",
            "brightness": "250 nits on standard panels",
        },
        "camera_specs": {
            "webcam": "1080p, IR option for Windows Hello",
        },
        "battery_capacity_mah": None,
        "battery_wh": 54,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "15.6-inch screen with a numeric keypad — much better for spreadsheet and accounting work",
            "Two SO-DIMM slots, so RAM is genuinely upgradeable and cheap to expand",
            "DDR5 memory support",
            "Very common in Canadian corporate fleets, so parts and replacements are easy to source",
        ],
        "cons": [
            "250-nit panel is dim and hard to read near a window or outdoors",
            "16:9 aspect ratio shows less vertical content than 16:10 rivals",
            "Around 1.7kg — noticeably heavier to carry daily",
        ],
        "verdict_summary": (
            "The Dell Latitude 5530 is the desk laptop. Buy it if you work seated with "
            "spreadsheets and want a big screen and cheap RAM upgrades — the dim display and "
            "weight make it a poor choice if you move around."
        ),
        "meta_description": (
            "Dell Latitude 5530 in Nigeria: 15.6-inch screen, upgradeable DDR5 RAM, numeric "
            "keypad. Specs, the dim-screen warning, and verdict."
        ),
        "tag_slugs": ["laptop-desk", "business", "student"],
    },
    {
        "brand": "Dell",
        "model_name": "Latitude 7430",
        "slug": "dell-latitude-7430",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Intel Core i5-1245U / i7-1265U (12th gen)",
        "ram_options": ["16GB", "32GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "14 inches",
            "type": "IPS anti-glare",
            "resolution": "1920 × 1080 or 1920 × 1200",
            "refresh_rate": "60Hz",
            "brightness": "up to 400 nits on brighter panels",
        },
        "camera_specs": {
            "webcam": "1080p with IR and SafeShutter automatic privacy cover",
        },
        "battery_capacity_mah": None,
        "battery_wh": 58,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Around 1.28kg, genuinely portable for a 14-inch business machine",
            "58Wh battery is one of the largest in this class — long runtime",
            "SafeShutter closes the webcam automatically when not in use",
            "Brighter panel options than the Latitude 5530",
        ],
        "cons": [
            "Soldered RAM — no upgrades after purchase",
            "Keyboard is good but not at ThinkPad level",
            "Panel brightness varies a lot between configurations, so check the actual unit",
        ],
        "verdict_summary": (
            "The Latitude 7430 is Dell's answer to the ThinkPad X13 and it is a fair fight — "
            "bigger battery, brighter screen options, slightly worse keyboard. Buy it if "
            "battery life is what you optimise for."
        ),
        "meta_description": (
            "Dell Latitude 7430 in Nigeria: 1.28kg, 58Wh battery, bright 14-inch panel. Specs "
            "and how it compares to the ThinkPad X13."
        ),
        "tag_slugs": ["laptop-portable", "business", "developer", "student"],
    },
    # ─── HP EliteBook ────────────────────────────────────────────────────────
    {
        "brand": "HP",
        "model_name": "EliteBook 840 G9",
        "slug": "hp-elitebook-840-g9",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Intel Core i5-1245U / i7-1265U (12th gen)",
        "ram_options": ["16GB", "32GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "14 inches",
            "type": "IPS anti-glare, 16:10",
            "resolution": "1920 × 1200",
            "refresh_rate": "60Hz",
            "brightness": "250–400 nits depending on panel",
        },
        "camera_specs": {
            "webcam": "5MP with auto framing and lighting correction",
        },
        "battery_capacity_mah": None,
        "battery_wh": 51,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "5MP webcam with auto framing — clearly the best laptop webcam in this channel",
            "16:10 display and a solid aluminium chassis",
            "Excellent speakers for video calls",
            "Around 1.36kg",
        ],
        "cons": [
            "Soldered RAM",
            "Base 250-nit panels are dim; the 400-nit option is worth seeking out",
            "Keyboard is comfortable but has shallower travel than a ThinkPad",
        ],
        "verdict_summary": (
            "The EliteBook 840 G9 is the pick if you live on video calls. The 5MP auto-framing "
            "webcam and speakers are a genuine step above every ThinkPad and Latitude here — "
            "check which display panel a unit has before buying."
        ),
        "meta_description": (
            "HP EliteBook 840 G9 in Nigeria: 5MP auto-framing webcam, 16:10 screen, aluminium "
            "build. Specs and buying verdict."
        ),
        "tag_slugs": ["laptop-portable", "business", "student"],
    },
    # ─── Apple Mac ───────────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "MacBook Air M1",
        "slug": "apple-macbook-air-m1",
        "form_factor": "laptop",
        "release_year": 2020,
        "chipset": "Apple M1 (8-core CPU, 7 or 8-core GPU)",
        "ram_options": ["8GB", "16GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD"],
        "display_specs": {
            "size": "13.3 inches",
            "type": "Retina IPS, 16:10",
            "resolution": "2560 × 1600",
            "refresh_rate": "60Hz",
            "brightness": "400 nits",
        },
        "camera_specs": {
            "webcam": "720p FaceTime HD",
        },
        "battery_capacity_mah": None,
        "battery_wh": 49,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Completely fanless and silent — nothing to clog with dust, which matters in Nigerian conditions",
            "15 or more hours of real battery life, still class-leading years later",
            "Sharp 2560 × 1600 Retina display far above any Windows laptop at this price",
            "Very strong resale value",
        ],
        "cons": [
            "8GB base RAM is soldered and cannot be upgraded — insist on 16GB if you multitask",
            "720p webcam is poor",
            "Only two Thunderbolt ports, so you will need a hub",
            "Some Windows-only business and accounting software will not run",
        ],
        "verdict_summary": (
            "The MacBook Air M1 is still the best battery life and build quality you can buy "
            "at its price. Buy the 16GB version if you can find one — the 8GB model becomes "
            "limiting quickly and there is no way to upgrade it later."
        ),
        "meta_description": (
            "MacBook Air M1 in Nigeria: fanless design, 15+ hour battery, Retina display. Why "
            "the RAM configuration matters more than anything else."
        ),
        "tag_slugs": ["laptop-portable", "student", "developer", "best-value"],
    },
    {
        "brand": "Apple",
        "model_name": "MacBook Air M2",
        "slug": "apple-macbook-air-m2",
        "form_factor": "laptop",
        "release_year": 2022,
        "chipset": "Apple M2 (8-core CPU, 8 or 10-core GPU)",
        "ram_options": ["8GB", "16GB", "24GB"],
        "storage_options": ["256GB SSD", "512GB SSD", "1TB SSD", "2TB SSD"],
        "display_specs": {
            "size": "13.6 inches",
            "type": "Liquid Retina IPS, 16:10",
            "resolution": "2560 × 1664",
            "refresh_rate": "60Hz",
            "brightness": "500 nits",
        },
        "camera_specs": {
            "webcam": "1080p FaceTime HD",
        },
        "battery_capacity_mah": None,
        "battery_wh": 52,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "500-nit display, noticeably brighter than the M1 and usable near windows",
            "1080p webcam replaces the M1's poor 720p camera",
            "MagSafe charging frees up both USB-C ports",
            "Still fanless and silent",
            "Thinner and lighter than the M1 despite a larger screen",
        ],
        "cons": [
            "256GB base models use a single NAND chip, making SSD read speeds slower than the M1's",
            "8GB base RAM again, and still soldered",
            "Notch in the display",
        ],
        "verdict_summary": (
            "The MacBook Air M2 is worth the step up from the M1 mainly for the brighter "
            "screen and the 1080p webcam. If you take video calls or work near daylight, pay "
            "the difference — and avoid the 256GB model, which has slower storage."
        ),
        "meta_description": (
            "MacBook Air M2 in Nigeria: 500-nit screen, 1080p webcam, MagSafe. The 256GB SSD "
            "issue explained, plus full specs."
        ),
        "tag_slugs": ["laptop-portable", "student", "developer", "business"],
    },
    {
        "brand": "Apple",
        "model_name": "MacBook Pro 14 (M1 Pro)",
        "slug": "apple-macbook-pro-14-m1-pro",
        "form_factor": "laptop",
        "release_year": 2021,
        "chipset": "Apple M1 Pro (8 or 10-core CPU, 14 or 16-core GPU)",
        "ram_options": ["16GB", "32GB"],
        "storage_options": ["512GB SSD", "1TB SSD", "2TB SSD"],
        "display_specs": {
            "size": "14.2 inches",
            "type": "Liquid Retina XDR mini-LED, 16:10",
            "resolution": "3024 × 1964",
            "refresh_rate": "120Hz ProMotion adaptive",
            "brightness": "1000 nits sustained full-screen, 1600 nits peak HDR",
        },
        "camera_specs": {
            "webcam": "1080p FaceTime HD",
        },
        "battery_capacity_mah": None,
        "battery_wh": 70,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Mini-LED XDR display at 120Hz — the best screen on any laptop in this channel by a wide margin",
            "Hardware video encoders make 4K editing dramatically faster than any Intel laptop here",
            "Full port selection: HDMI, SD card reader, MagSafe, three Thunderbolt",
            "Excellent speakers and a 1080p webcam",
        ],
        "cons": [
            "Heavy for its size at around 1.6kg",
            "Expensive even used",
            "Fans do spin up under sustained export loads, unlike the Air",
            "Overkill if you only browse and write documents",
        ],
        "verdict_summary": (
            "The MacBook Pro 14 with M1 Pro is the machine to buy if you edit video or "
            "photos seriously. Nothing else in the Canadian off-lease channel comes close on "
            "screen quality or export speed — but it is wasted money for ordinary office work."
        ),
        "meta_description": (
            "MacBook Pro 14 M1 Pro in Nigeria: mini-LED 120Hz XDR display, fast 4K video "
            "editing, full port selection. Specs and verdict."
        ),
        "tag_slugs": ["laptop-portable", "content-creator", "developer", "business"],
    },
]
