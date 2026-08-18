"""
Apple device catalog — accurate manufacturer specifications.

PRICING: every `price_band_ngn` is intentionally empty. Fill from your own
inventory before publishing. `conditions_available` and `is_in_stock` are
likewise left for you — nothing here should claim availability you don't have,
because these fields feed Product JSON-LD.

Specs are from Apple's published technical specifications. Do not edit spec
values without a source.
"""

APPLE_DEVICES = [
    # ─── iPhone 11 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 11",
        "slug": "apple-iphone-11",
        "form_factor": "phone",
        "release_year": 2019,
        "chipset": "Apple A13 Bionic",
        "ram_options": ["4GB"],
        "storage_options": ["64GB", "128GB", "256GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Liquid Retina HD LCD",
            "resolution": "1792 × 828",
            "refresh_rate": "60Hz",
            "brightness": "625 nits (typical)",
        },
        "camera_specs": {
            "main": "12MP f/1.8 wide, OIS",
            "ultra_wide": "12MP f/2.4",
            "front": "12MP TrueDepth",
            "video": "4K up to 60fps",
        },
        "battery_capacity_mah": 3110,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Still receives iOS updates six years after launch — rare longevity at this price",
            "A13 Bionic handles WhatsApp, banking apps and social media without lag",
            "Very large parts and screen-repair market in Nigeria, so servicing is cheap",
            "LCD panel does not burn in, unlike OLED phones of the same age",
        ],
        "cons": [
            "No 5G — irrelevant today in Nigeria, but limits resale value later",
            "LCD looks washed out next to any OLED phone",
            "Battery health on used units is often below 85%, so budget for a replacement",
            "Slow 20W charging and no charger in most used boxes",
        ],
        "verdict_summary": (
            "The iPhone 11 is the cheapest way into a genuinely usable iPhone in Nigeria. "
            "Buy it if you want iMessage, FaceTime and iOS updates on the smallest budget — "
            "but check the battery health figure before you pay, because most units at this "
            "age need a new battery."
        ),
        "meta_description": (
            "iPhone 11 in Nigeria: specs, battery health warning, and whether it is still "
            "worth buying used. Honest verdict from Kwise World."
        ),
        "tag_slugs": ["budget-pick", "student", "first-iphone"],
    },
    # ─── iPhone 12 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 12",
        "slug": "apple-iphone-12",
        "form_factor": "phone",
        "release_year": 2020,
        "chipset": "Apple A14 Bionic",
        "ram_options": ["4GB"],
        "storage_options": ["64GB", "128GB", "256GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2532 × 1170",
            "refresh_rate": "60Hz",
            "brightness": "625 nits typical, 1200 nits peak HDR",
        },
        "camera_specs": {
            "main": "12MP f/1.6 wide, OIS",
            "ultra_wide": "12MP f/2.4",
            "front": "12MP TrueDepth",
            "video": "4K up to 60fps, Dolby Vision HDR",
        },
        "battery_capacity_mah": 2815,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "First iPhone with an OLED screen at the standard tier — big jump over iPhone 11",
            "Ceramic Shield front glass survives drops better than iPhone 11",
            "MagSafe accessories work, and they are widely available in Lagos and Ibadan",
            "Flat-edge design that still looks current five years on",
        ],
        "cons": [
            "2,815 mAh is the smallest battery of any modern iPhone — heavy users will charge twice daily",
            "60Hz display feels slow next to any 120Hz Android at the same price",
            "No charger in the box, even on new units",
            "OLED burn-in is a real risk on heavily used examples — check for it",
        ],
        "verdict_summary": (
            "The iPhone 12 is worth it over the iPhone 11 only for the OLED screen and 5G. "
            "If your day involves heavy WhatsApp, maps and streaming, the small battery will "
            "frustrate you — step up to the iPhone 13 instead."
        ),
        "meta_description": (
            "iPhone 12 in Nigeria: full specs, the battery problem nobody mentions, and "
            "whether to spend a little more on the iPhone 13."
        ),
        "tag_slugs": ["budget-pick", "student", "first-iphone"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 12 Pro Max",
        "slug": "apple-iphone-12-pro-max",
        "form_factor": "phone",
        "release_year": 2020,
        "chipset": "Apple A14 Bionic",
        "ram_options": ["6GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.7 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2778 × 1284",
            "refresh_rate": "60Hz",
            "brightness": "800 nits typical, 1200 nits peak HDR",
        },
        "camera_specs": {
            "main": "12MP f/1.6 wide, sensor-shift OIS",
            "ultra_wide": "12MP f/2.4",
            "telephoto": "12MP f/2.2, 2.5× optical",
            "front": "12MP TrueDepth",
            "video": "4K up to 60fps, Dolby Vision HDR",
        },
        "battery_capacity_mah": 3687,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Sensor-shift stabilisation — still one of the steadiest handheld video iPhones",
            "Stainless steel frame and largest battery in the iPhone 12 family",
            "LiDAR scanner improves low-light autofocus and portrait edge detection",
            "Big-screen Pro experience at a fraction of a current Pro Max price",
        ],
        "cons": [
            "Heavy at 228g and physically large — not a one-hand phone",
            "60Hz display on a device this expensive originally",
            "Stainless steel frame scratches and scuffs visibly on used units",
            "Battery health is the deciding factor at this age — verify before buying",
        ],
        "verdict_summary": (
            "The iPhone 12 Pro Max is the value pick if you want a big-screen iPhone with "
            "proper stabilised video and don't need the newest chip. Buy it for video, "
            "screen size and price — skip it if you want something pocketable."
        ),
        "meta_description": (
            "iPhone 12 Pro Max in Nigeria: specs, video quality, and who should still buy "
            "one used in 2026."
        ),
        "tag_slugs": ["content-creator", "photography", "big-screen"],
    },
    # ─── iPhone 13 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 13",
        "slug": "apple-iphone-13",
        "form_factor": "phone",
        "release_year": 2021,
        "chipset": "Apple A15 Bionic",
        "ram_options": ["4GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2532 × 1170",
            "refresh_rate": "60Hz",
            "brightness": "800 nits typical, 1200 nits peak HDR",
        },
        "camera_specs": {
            "main": "12MP f/1.6 wide, sensor-shift OIS",
            "ultra_wide": "12MP f/2.4",
            "front": "12MP TrueDepth",
            "video": "4K up to 60fps, Cinematic mode 1080p30",
        },
        "battery_capacity_mah": 3240,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Battery life jumped substantially over the iPhone 12 — this is the real upgrade",
            "Sensor-shift stabilisation inherited from the 12 Pro Max",
            "128GB base storage instead of 64GB",
            "A15 Bionic is still fast enough for everything in 2026",
        ],
        "cons": [
            "Still 60Hz",
            "Only 4GB RAM, so heavy multitaskers will see apps reload in the background",
            "No telephoto lens — zoomed shots are digital crops",
        ],
        "verdict_summary": (
            "The iPhone 13 is the best-value used iPhone in Nigeria right now. It fixed the "
            "iPhone 12's battery problem, keeps the same design, and still gets full iOS "
            "updates — if you want one iPhone recommendation on a mid budget, this is it."
        ),
        "meta_description": (
            "iPhone 13 in Nigeria: why it is the best-value used iPhone to buy, full specs, "
            "and how it compares to the iPhone 14."
        ),
        "tag_slugs": ["best-value", "student", "first-iphone", "battery-life"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 13 Pro Max",
        "slug": "apple-iphone-13-pro-max",
        "form_factor": "phone",
        "release_year": 2021,
        "chipset": "Apple A15 Bionic (5-core GPU)",
        "ram_options": ["6GB"],
        "storage_options": ["128GB", "256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.7 inches",
            "type": "Super Retina XDR OLED, ProMotion LTPO",
            "resolution": "2778 × 1284",
            "refresh_rate": "120Hz adaptive (10–120Hz)",
            "brightness": "1000 nits typical, 1200 nits peak HDR",
        },
        "camera_specs": {
            "main": "12MP f/1.5 wide, sensor-shift OIS",
            "ultra_wide": "12MP f/1.8 with macro",
            "telephoto": "12MP f/2.8, 3× optical",
            "front": "12MP TrueDepth",
            "video": "4K up to 60fps, ProRes, Cinematic mode",
        },
        "battery_capacity_mah": 4352,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Longest-lasting iPhone battery of its generation — genuinely a full day of heavy use",
            "First iPhone with 120Hz ProMotion, and it still feels smooth today",
            "Full triple-camera system with 3× optical zoom and macro",
            "ProRes video recording for serious content work",
        ],
        "cons": [
            "240g — one of the heaviest iPhones ever made",
            "Notch is large compared to the Dynamic Island on newer models",
            "Stainless steel frame shows wear on used units",
        ],
        "verdict_summary": (
            "The iPhone 13 Pro Max is the smartest big-battery buy for anyone who films on "
            "an iPhone but won't pay current Pro Max money. You get 120Hz, 3× zoom, ProRes "
            "and the best battery Apple has shipped — at a used price."
        ),
        "meta_description": (
            "iPhone 13 Pro Max in Nigeria: battery life, ProRes video, 120Hz display and "
            "whether it still beats newer models on value."
        ),
        "tag_slugs": ["content-creator", "photography", "battery-life", "big-screen"],
    },
    # ─── iPhone 14 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 14",
        "slug": "apple-iphone-14",
        "form_factor": "phone",
        "release_year": 2022,
        "chipset": "Apple A15 Bionic (5-core GPU)",
        "ram_options": ["6GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2532 × 1170",
            "refresh_rate": "60Hz",
            "brightness": "800 nits typical, 1200 nits peak HDR",
        },
        "camera_specs": {
            "main": "12MP f/1.5 wide, sensor-shift OIS",
            "ultra_wide": "12MP f/2.4",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K up to 60fps, Action mode, Cinematic 4K30",
        },
        "battery_capacity_mah": 3279,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "6GB RAM and the faster 5-core GPU A15 — smoother than the iPhone 13 under load",
            "Front camera finally has autofocus, which matters for selfie video",
            "Action mode gives gimbal-like stabilisation for walking shots",
            "Crash Detection and satellite Emergency SOS",
        ],
        "cons": [
            "Almost identical to the iPhone 13 in daily use — not worth a big price gap",
            "Still 60Hz and still no telephoto lens",
            "Satellite SOS is not available in Nigeria",
        ],
        "verdict_summary": (
            "The iPhone 14 only makes sense if the price gap over the iPhone 13 is small. "
            "The extra RAM and Action mode are real, but a buyer choosing on value should "
            "take the 13 and spend the difference on storage or a battery replacement."
        ),
        "meta_description": (
            "iPhone 14 in Nigeria: full specs and an honest answer on whether it is worth "
            "more than an iPhone 13."
        ),
        "tag_slugs": ["best-value", "student", "first-iphone"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 14 Pro Max",
        "slug": "apple-iphone-14-pro-max",
        "form_factor": "phone",
        "release_year": 2022,
        "chipset": "Apple A16 Bionic",
        "ram_options": ["6GB"],
        "storage_options": ["128GB", "256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.7 inches",
            "type": "Super Retina XDR OLED, ProMotion LTPO, always-on",
            "resolution": "2796 × 1290",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 2000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.78 quad-pixel, sensor-shift OIS",
            "ultra_wide": "12MP f/2.2 with macro",
            "telephoto": "12MP f/2.8, 3× optical",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K up to 60fps, ProRes, Cinematic 4K30, Action mode",
        },
        "battery_capacity_mah": 4323,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "2,000-nit outdoor brightness — the first iPhone genuinely readable in Nigerian midday sun",
            "48MP main sensor, a real jump in detail over every 12MP iPhone before it",
            "Dynamic Island replaces the notch",
            "Excellent battery life, close to the 13 Pro Max",
        ],
        "cons": [
            "240g and physically large",
            "Lightning port, not USB-C — a real annoyance if everything else you own is USB-C",
            "48MP shots eat storage fast in ProRAW",
        ],
        "verdict_summary": (
            "The iPhone 14 Pro Max is the value sweet spot in used Pro Max models. You get "
            "the 48MP sensor, the always-on 2,000-nit screen and Dynamic Island — everything "
            "the 15 Pro Max has except USB-C and 5× zoom."
        ),
        "meta_description": (
            "iPhone 14 Pro Max in Nigeria: 48MP camera, 2000-nit display, battery life and "
            "how it compares to the 15 Pro Max on value."
        ),
        "tag_slugs": ["photography", "content-creator", "battery-life", "big-screen", "best-value"],
    },
    # ─── iPhone 15 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 15",
        "slug": "apple-iphone-15",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Apple A16 Bionic",
        "ram_options": ["6GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2556 × 1179",
            "refresh_rate": "60Hz",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 2000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.6 quad-pixel, sensor-shift OIS (2× optical-quality crop)",
            "ultra_wide": "12MP f/2.4",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K up to 60fps, Cinematic 4K30, Action mode",
        },
        "battery_capacity_mah": 3349,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "USB-C at last — one cable for phone, laptop and power bank",
            "48MP main sensor trickled down from the Pro, plus a usable 2× zoom crop",
            "2,000-nit outdoor brightness on a non-Pro iPhone",
            "Dynamic Island instead of the notch",
        ],
        "cons": [
            "USB-C port runs at USB 2.0 speed — file transfers are slow despite the connector",
            "Still 60Hz in 2023, which was hard to defend even then",
            "No telephoto lens",
        ],
        "verdict_summary": (
            "The iPhone 15 is the first standard iPhone worth paying up for in years, mostly "
            "because of USB-C and the 48MP sensor. If you charge a laptop and a phone from "
            "the same brick, that alone justifies choosing it over the iPhone 14."
        ),
        "meta_description": (
            "iPhone 15 in Nigeria: USB-C, 48MP camera, full specs, and whether it beats the "
            "iPhone 14 on value."
        ),
        "tag_slugs": ["best-value", "first-iphone", "photography"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 15 Pro Max",
        "slug": "apple-iphone-15-pro-max",
        "form_factor": "phone",
        "release_year": 2023,
        "chipset": "Apple A17 Pro",
        "ram_options": ["8GB"],
        "storage_options": ["256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.7 inches",
            "type": "Super Retina XDR OLED, ProMotion LTPO, always-on",
            "resolution": "2796 × 1290",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 2000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.78 quad-pixel, sensor-shift OIS",
            "ultra_wide": "12MP f/2.2 with macro",
            "telephoto_5x": "12MP f/2.8 tetraprism, 5× optical",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K up to 60fps, ProRes to external drive, Log, Action mode",
        },
        "battery_capacity_mah": 4441,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "5× tetraprism zoom, exclusive to the Pro Max that year",
            "Titanium frame drops weight to 221g from the 14 Pro Max's 240g",
            "USB-C at USB 3 speed (10Gbps) — genuinely fast transfers, unlike the standard 15",
            "Customisable Action button replaces the mute switch",
            "ProRes recording direct to an external SSD removes the storage problem",
        ],
        "cons": [
            "A17 Pro ran hot at launch; fixed in software but heavy gaming still warms it",
            "5× zoom means you lose the 3× focal length many people used more often",
            "Expensive even used",
        ],
        "verdict_summary": (
            "The iPhone 15 Pro Max is the one to buy if you shoot video professionally and "
            "want zoom reach. The 5× lens and USB 3 transfer speeds are the two things that "
            "actually separate it from a 14 Pro Max — if you don't need either, save money."
        ),
        "meta_description": (
            "iPhone 15 Pro Max in Nigeria: 5x zoom, titanium build, ProRes video and an "
            "honest comparison against the 14 Pro Max."
        ),
        "tag_slugs": ["photography", "content-creator", "big-screen", "flagship"],
    },
    # ─── iPhone 16 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 16",
        "slug": "apple-iphone-16",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Apple A18",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2556 × 1179",
            "refresh_rate": "60Hz",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 2000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.6 Fusion, sensor-shift OIS (2× optical-quality crop)",
            "ultra_wide": "12MP f/2.2 with autofocus and macro",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K up to 60fps Dolby Vision, Cinematic, Action mode, spatial video",
        },
        "battery_capacity_mah": 3561,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "8GB RAM — the first standard iPhone specced for Apple Intelligence",
            "Ultra-wide gains autofocus, so macro photography works on a non-Pro iPhone",
            "Camera Control button gives a physical shutter and quick camera launch",
            "Meaningfully bigger battery than the iPhone 15",
        ],
        "cons": [
            "Still 60Hz — Apple held 120Hz back for the Pro line one more year",
            "Apple Intelligence features are region-limited and English-first",
            "No telephoto lens",
        ],
        "verdict_summary": (
            "The iPhone 16 is the standard iPhone to buy if you want the longest software "
            "runway — 8GB RAM means it will keep receiving AI features that the iPhone 15 "
            "and older will not. For everything else, an iPhone 15 does the same job cheaper."
        ),
        "meta_description": (
            "iPhone 16 in Nigeria: A18 chip, Camera Control, 8GB RAM for Apple Intelligence, "
            "and whether to buy it over the iPhone 15."
        ),
        "tag_slugs": ["flagship", "first-iphone", "photography"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 16 Pro Max",
        "slug": "apple-iphone-16-pro-max",
        "form_factor": "phone",
        "release_year": 2024,
        "chipset": "Apple A18 Pro",
        "ram_options": ["8GB"],
        "storage_options": ["256GB", "512GB", "1TB"],
        "display_specs": {
            "size": "6.9 inches",
            "type": "Super Retina XDR OLED, ProMotion LTPO, always-on",
            "resolution": "2868 × 1320",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 2000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.78 Fusion, second-gen sensor-shift OIS",
            "ultra_wide": "48MP f/2.2 with autofocus and macro",
            "telephoto_5x": "12MP f/2.8 tetraprism, 5× optical",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K120 Dolby Vision, ProRes, Log, four studio mics",
        },
        "battery_capacity_mah": 4685,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "4K at 120fps — slow motion at full resolution, which no other phone offered at launch",
            "Largest iPhone battery ever at the time, and it shows in real use",
            "48MP ultra-wide finally matches the main sensor's detail",
            "Four studio-quality mics make it usable for interviews without external audio",
        ],
        "cons": [
            "6.9 inches is genuinely unwieldy for smaller hands",
            "227g",
            "Very expensive, and the 15 Pro Max covers most of the same ground",
        ],
        "verdict_summary": (
            "The iPhone 16 Pro Max is the best iPhone for video work available used in "
            "Nigeria. 4K120 recording and the four-mic array are the reasons to buy it — "
            "if you only take photos, a 15 Pro Max saves you a lot for very little loss."
        ),
        "meta_description": (
            "iPhone 16 Pro Max in Nigeria: 4K120 video, 48MP ultra-wide, biggest iPhone "
            "battery, and how it compares to the 15 Pro Max."
        ),
        "tag_slugs": ["photography", "content-creator", "big-screen", "flagship", "battery-life"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 16e",
        "slug": "apple-iphone-16e",
        "form_factor": "phone",
        "release_year": 2025,
        "chipset": "Apple A18",
        "ram_options": ["8GB"],
        "storage_options": ["128GB", "256GB", "512GB"],
        "display_specs": {
            "size": "6.1 inches",
            "type": "Super Retina XDR OLED",
            "resolution": "2532 × 1170",
            "refresh_rate": "60Hz",
            "brightness": "800 nits typical, 1200 nits peak HDR",
        },
        "camera_specs": {
            "main": "48MP f/1.6 Fusion, sensor-shift OIS (2× optical-quality crop)",
            "front": "12MP TrueDepth with autofocus",
            "video": "4K up to 60fps Dolby Vision, Action mode",
        },
        "battery_capacity_mah": 4005,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "Best battery life of any 6.1-inch iPhone, thanks to Apple's own C1 modem",
            "A18 chip and 8GB RAM — same core performance as the iPhone 16",
            "Cheapest route to Apple Intelligence and a long update runway",
        ],
        "cons": [
            "Single rear camera — no ultra-wide at all",
            "No MagSafe magnets, only standard Qi wireless charging",
            "Dimmer 800-nit screen and still a notch rather than Dynamic Island",
        ],
        "verdict_summary": (
            "The iPhone 16e is the pick if battery life and long software support matter more "
            "to you than cameras. You lose the ultra-wide lens and MagSafe — if you shoot "
            "wide group shots or use magnetic accessories, buy an iPhone 15 instead."
        ),
        "meta_description": (
            "iPhone 16e in Nigeria: best iPhone battery life at its size, but no ultra-wide "
            "camera and no MagSafe. Full specs and verdict."
        ),
        "tag_slugs": ["battery-life", "budget-pick", "first-iphone", "student"],
    },
    # ─── iPhone 17 series ────────────────────────────────────────────────────
    {
        "brand": "Apple",
        "model_name": "iPhone 17",
        "slug": "apple-iphone-17",
        "form_factor": "phone",
        "release_year": 2025,
        "chipset": "Apple A19",
        "ram_options": ["8GB"],
        "storage_options": ["256GB", "512GB"],
        "display_specs": {
            "size": "6.3 inches",
            "type": "Super Retina XDR OLED, ProMotion LTPO",
            "resolution": "2622 × 1206",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 3000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.6 Fusion, sensor-shift OIS (2× optical-quality crop)",
            "ultra_wide": "48MP f/2.2 with autofocus and macro",
            "front": "18MP Center Stage square sensor",
            "video": "4K up to 60fps Dolby Vision, Action mode, dual capture",
        },
        "battery_capacity_mah": 3692,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "120Hz ProMotion finally arrives on the standard iPhone — the single biggest change",
            "256GB base storage, double the previous entry point",
            "3,000-nit outdoor brightness, the brightest iPhone screen yet",
            "18MP Center Stage front camera reframes group selfies automatically",
            "Ceramic Shield 2 on the front, more scratch resistant than before",
        ],
        "cons": [
            "Still no telephoto lens",
            "Battery is only slightly larger than the iPhone 16's",
            "Premium pricing on a very recent model — used supply is thin and expensive",
        ],
        "verdict_summary": (
            "The iPhone 17 is the first standard iPhone that doesn't compromise on the screen. "
            "If 120Hz smoothness is what has kept you on Android, this is the iPhone that "
            "closes that gap — but wait for used prices to settle before buying."
        ),
        "meta_description": (
            "iPhone 17 in Nigeria: 120Hz ProMotion on the standard model at last, 256GB base "
            "storage, full specs and verdict."
        ),
        "tag_slugs": ["flagship", "photography", "first-iphone"],
    },
    {
        "brand": "Apple",
        "model_name": "iPhone 17 Pro Max",
        "slug": "apple-iphone-17-pro-max",
        "form_factor": "phone",
        "release_year": 2025,
        "chipset": "Apple A19 Pro",
        "ram_options": ["12GB"],
        "storage_options": ["256GB", "512GB", "1TB", "2TB"],
        "display_specs": {
            "size": "6.9 inches",
            "type": "Super Retina XDR OLED, ProMotion LTPO, always-on",
            "resolution": "2868 × 1320",
            "refresh_rate": "120Hz adaptive (1–120Hz)",
            "brightness": "1000 nits typical, 1600 nits peak HDR, 3000 nits outdoor",
        },
        "camera_specs": {
            "main": "48MP f/1.78 Fusion, second-gen sensor, sensor-shift OIS",
            "ultra_wide": "48MP f/2.2 with autofocus and macro",
            "telephoto_5x": "48MP telephoto, 8× optical-quality zoom (200mm equivalent)",
            "front": "18MP Center Stage square sensor",
            "video": "4K120 Dolby Vision, ProRes RAW, Apple Log 2, open gate recording",
        },
        # 4,832 mAh is the physical-SIM variant, which is what Canadian units are
        # (model A3522). eSIM-only regions such as the US ship a 5,088 mAh cell.
        "battery_capacity_mah": 4832,
        "battery_wh": None,
        "price_band_ngn": "",
        "conditions_available": [],
        "is_in_stock": False,
        "pros": [
            "8× optical-quality zoom, the longest reach Apple has ever shipped",
            "All three rear cameras are 48MP for the first time",
            "Vapor chamber cooling and aluminium unibody — sustained performance is much better",
            "Ceramic Shield 2 adds an anti-reflective coating, so daylight legibility improves",
            "12GB RAM, the most in any iPhone",
            "Apple Log 2 and open gate recording put it into professional video workflows",
        ],
        "cons": [
            "Very expensive, and used supply in Nigeria is limited and premium-priced",
            "Aluminium replaces titanium — a downgrade in perceived material quality for some",
            "Largest and heaviest iPhone to carry daily",
        ],
        "verdict_summary": (
            "The iPhone 17 Pro Max is the most capable video camera Apple has put in a phone, "
            "and the 8× zoom finally beats Samsung's reach. Buy it only if you shoot "
            "professionally — for everyone else the price gap over a 16 Pro Max is not "
            "justified by daily use."
        ),
        "meta_description": (
            "iPhone 17 Pro Max in Nigeria: 8x optical zoom, triple 48MP cameras, Apple Log 2 "
            "and vapor chamber cooling. Full specs and honest verdict."
        ),
        "tag_slugs": ["photography", "content-creator", "flagship", "big-screen", "gaming"],
    },
]
