"""
Authors, use-case taxonomy, and head-to-head comparisons.

AUTHOR BIOS are placeholders marked TODO. E-E-A-T signals must be accurate —
overstating experience is worse than understating it. Replace with real names,
real years, real credentials before publishing.

Comparison slugs deliberately mirror how people type these queries. Do not
"improve" them into formal product names — "s24-vs-s24-ultra" is what gets
searched, and matching that phrasing is most of the value.
"""

AUTHORS = [
    {
        "name": "TODO — replace with real name",
        "slug": "kwise-editorial",
        "bio": (
            "TODO: replace with a real bio. State how long Kwise World has been trading, "
            "roughly how many devices have passed through the business, and that every "
            "device listed is tested before sale. Keep it factual — do not inflate numbers."
        ),
        "credentials": "TODO — e.g. 'Founder, Kwise World · N years in device sourcing and resale'",
    },
    {
        "name": "TODO — replace with real name",
        "slug": "kwise-technical",
        "bio": (
            "TODO: replace with the bio of whoever does device testing and grading. "
            "Mention the testing process (battery health check, IMEI verification, "
            "carrier-lock check, screen and port inspection) — the process is the credential."
        ),
        "credentials": "TODO — e.g. 'Device testing and grading lead, Kwise World'",
    },
]

USE_CASE_TAGS = [
    {"name": "Best Value", "slug": "best-value",
     "description": "Devices that give the most performance and longevity for the money."},
    {"name": "Photography", "slug": "photography",
     "description": "Phones chosen primarily for still photo quality and zoom range."},
    {"name": "Content Creator", "slug": "content-creator",
     "description": "Devices for shooting, editing and publishing video and social content."},
    {"name": "Battery Life", "slug": "battery-life",
     "description": "Devices that survive a full day of heavy use without a power bank."},
    {"name": "Student", "slug": "student",
     "description": "Affordable, durable devices for coursework, research and note-taking."},
    {"name": "Business", "slug": "business",
     "description": "Productivity-focused devices for professional and office work."},
    {"name": "Developer", "slug": "developer",
     "description": "Machines with the RAM, sustained performance and screen space for writing code."},
    {"name": "Gaming", "slug": "gaming",
     "description": "Devices with the sustained performance and thermals for heavy games."},
    {"name": "Budget Pick", "slug": "budget-pick",
     "description": "The most capable devices at the lowest entry prices."},
    {"name": "Compact", "slug": "compact",
     "description": "Phones under 6.4 inches that stay comfortable in one hand."},
    {"name": "Big Screen", "slug": "big-screen",
     "description": "Phones 6.7 inches and above for media, reading and multitasking."},
    {"name": "Flagship", "slug": "flagship",
     "description": "Current-generation top-tier devices with no meaningful compromises."},
    {"name": "First iPhone", "slug": "first-iphone",
     "description": "Good entry points for someone moving to iOS for the first time."},
    {"name": "S Pen", "slug": "s-pen",
     "description": "Samsung devices with a built-in stylus for notes and drawing."},
    {"name": "Portable Laptop", "slug": "laptop-portable",
     "description": "Laptops light enough to carry every day."},
    {"name": "Desk Laptop", "slug": "laptop-desk",
     "description": "Larger laptops intended to stay on a desk, with more screen space."},
]

COMPARISONS = [
    # ─── iPhone vs iPhone ────────────────────────────────────────────────────
    {
        "title": "iPhone 13 vs iPhone 14 — Which Should You Buy in Nigeria?",
        "slug": "iphone-13-vs-iphone-14",
        "device_a_slug": "apple-iphone-13",
        "device_b_slug": "apple-iphone-14",
        "author_slug": "kwise-editorial",
        "intro": (
            "Buy the iPhone 13 unless the price gap is small. The iPhone 14 adds 6GB of RAM, "
            "Action mode video stabilisation and a front camera that can focus — real "
            "improvements, but not ones most people notice daily. Everything else, including "
            "the screen, the main camera and the chip, is effectively the same."
        ),
        "winner_by_category": {
            "camera": "b", "display": "tie", "battery": "tie",
            "performance": "b", "value": "a", "portability": "tie",
        },
        "overall_recommendation": (
            "If the price difference is small → iPhone 14, for the extra RAM and Action mode. "
            "If you are choosing on value → iPhone 13, and put the savings toward more storage. "
            "If you shoot a lot of selfie video → iPhone 14, because its front camera autofocuses."
        ),
        "meta_description": (
            "iPhone 13 vs iPhone 14 in Nigeria: what actually changed, what did not, and "
            "which one is the better buy used."
        ),
        "faqs": [
            {"question": "Is the iPhone 14 much better than the iPhone 13?",
             "answer": (
                 "No. They share the same screen, the same main camera hardware and nearly the "
                 "same chip. The iPhone 14 adds 6GB of RAM instead of 4GB, Action mode for "
                 "stabilised video, and autofocus on the front camera. In everyday use most "
                 "people cannot tell them apart."
             ), "order": 1},
            {"question": "Does the iPhone 13 still get iOS updates?",
             "answer": (
                 "Yes. The iPhone 13 launched in 2021 and Apple typically supports iPhones with "
                 "major iOS releases for five to seven years, so it has a substantial runway "
                 "left. Check Apple's current compatibility list for the newest iOS version "
                 "before buying."
             ), "order": 2},
            {"question": "Which has better battery life, iPhone 13 or iPhone 14?",
             "answer": (
                 "They are almost identical — 3,240 mAh versus 3,279 mAh. On used units the "
                 "deciding factor is battery health percentage, not the model. A well-kept "
                 "iPhone 13 at 92% health will outlast an iPhone 14 at 80%."
             ), "order": 3},
        ],
    },
    {
        "title": "iPhone 14 vs iPhone 15 — Is USB-C Worth the Upgrade?",
        "slug": "iphone-14-vs-iphone-15",
        "device_a_slug": "apple-iphone-14",
        "device_b_slug": "apple-iphone-15",
        "author_slug": "kwise-editorial",
        "intro": (
            "The iPhone 15 is the better phone and the upgrade is real this time. It swaps the "
            "12MP main camera for a 48MP sensor with a usable 2× zoom crop, doubles outdoor "
            "screen brightness to 2,000 nits, replaces the notch with the Dynamic Island, and "
            "moves to USB-C. If your budget stretches, take the 15."
        ),
        "winner_by_category": {
            "camera": "b", "display": "b", "battery": "b",
            "performance": "b", "value": "a", "portability": "tie",
        },
        "overall_recommendation": (
            "If you already own USB-C chargers and cables → iPhone 15, one cable for everything. "
            "If you want the sharpest photos on a standard iPhone → iPhone 15, for the 48MP sensor. "
            "If you are on a strict budget → iPhone 14 still does everything well."
        ),
        "meta_description": (
            "iPhone 14 vs iPhone 15 in Nigeria: 48MP camera, USB-C, brighter screen. Which is "
            "the better buy and why."
        ),
        "faqs": [
            {"question": "Is the iPhone 15 USB-C fast for transferring files?",
             "answer": (
                 "No. The standard iPhone 15 has a USB-C connector but it runs at USB 2.0 speed, "
                 "the same as the old Lightning port. Only the iPhone 15 Pro and Pro Max "
                 "transfer at USB 3 speeds. The benefit on the standard model is cable "
                 "convenience, not speed."
             ), "order": 1},
            {"question": "Does the iPhone 15 have a telephoto camera?",
             "answer": (
                 "No dedicated telephoto lens. It uses a crop from the 48MP main sensor to give "
                 "a 2× zoom that Apple calls optical quality. It looks good in daylight but "
                 "loses detail in low light, unlike a true telephoto lens."
             ), "order": 2},
        ],
    },
    {
        "title": "iPhone 15 vs iPhone 16 — Which Is Worth Buying?",
        "slug": "iphone-15-vs-iphone-16",
        "device_a_slug": "apple-iphone-15",
        "device_b_slug": "apple-iphone-16",
        "author_slug": "kwise-editorial",
        "intro": (
            "Buy the iPhone 16 if you want the longest software runway. Its 8GB of RAM is the "
            "requirement for Apple Intelligence features, which the iPhone 15 cannot run at "
            "all. Beyond that the differences are modest: a slightly bigger battery, an "
            "autofocusing ultra-wide that enables macro shots, and the new Camera Control button."
        ),
        "winner_by_category": {
            "camera": "b", "display": "tie", "battery": "b",
            "performance": "b", "value": "a", "portability": "tie",
        },
        "overall_recommendation": (
            "If you want AI features and the longest support window → iPhone 16. "
            "If you want the same daily experience for less → iPhone 15. "
            "If you shoot close-up product or food photos → iPhone 16, because its ultra-wide focuses."
        ),
        "meta_description": (
            "iPhone 15 vs iPhone 16 in Nigeria: Apple Intelligence, Camera Control, macro "
            "photography. Honest comparison and buying advice."
        ),
        "faqs": [
            {"question": "Can the iPhone 15 run Apple Intelligence?",
             "answer": (
                 "No. Apple Intelligence requires 8GB of RAM, and the standard iPhone 15 has "
                 "6GB. Only the iPhone 15 Pro and Pro Max from that generation support it. "
                 "Every iPhone 16 model does."
             ), "order": 1},
            {"question": "Is Apple Intelligence available in Nigeria?",
             "answer": (
                 "Feature availability and supported languages vary by region and change with "
                 "each iOS release. Check Apple's current feature availability page for Nigeria "
                 "before buying a phone specifically for these features."
             ), "order": 2},
        ],
    },
    {
        "title": "iPhone 14 Pro Max vs iPhone 15 Pro Max — Which Pro Max to Buy",
        "slug": "iphone-14-pro-max-vs-iphone-15-pro-max",
        "device_a_slug": "apple-iphone-14-pro-max",
        "device_b_slug": "apple-iphone-15-pro-max",
        "author_slug": "kwise-technical",
        "intro": (
            "The 15 Pro Max wins on three things that matter: 5× optical zoom instead of 3×, "
            "USB-C at real USB 3 speeds, and 221g instead of 240g thanks to titanium. If none "
            "of those three matter to you, the 14 Pro Max is the far better value — the screen "
            "and main camera are essentially identical."
        ),
        "winner_by_category": {
            "camera": "b", "display": "tie", "battery": "b",
            "performance": "b", "value": "a", "portability": "b",
        },
        "overall_recommendation": (
            "If you shoot distant subjects — events, wildlife, stage — → iPhone 15 Pro Max for the 5× lens. "
            "If you record ProRes video and need fast offloading → iPhone 15 Pro Max, USB 3 transfer. "
            "If you mostly shoot people and everyday scenes → iPhone 14 Pro Max, and save the difference."
        ),
        "meta_description": (
            "iPhone 14 Pro Max vs 15 Pro Max in Nigeria: 5x zoom, titanium weight, USB-C "
            "speeds. Which Pro Max is the smarter used buy."
        ),
        "faqs": [
            {"question": "Is 5x zoom better than 3x zoom on iPhone?",
             "answer": (
                 "For distant subjects, yes — the 15 Pro Max reaches much further optically. "
                 "But 3× is the more useful everyday focal length for portraits and general "
                 "shooting, and the 15 Pro Max has to crop digitally to reach 3×. Which is "
                 "better depends entirely on what you photograph."
             ), "order": 1},
            {"question": "Does the iPhone 14 Pro Max have USB-C?",
             "answer": (
                 "No, it uses Lightning. USB-C arrived with the iPhone 15 generation. If every "
                 "other device you own charges over USB-C, that inconvenience is worth factoring "
                 "into the decision."
             ), "order": 2},
        ],
    },
    {
        "title": "iPhone 15 Pro Max vs iPhone 16 Pro Max — Full Comparison",
        "slug": "iphone-15-pro-max-vs-iphone-16-pro-max",
        "device_a_slug": "apple-iphone-15-pro-max",
        "device_b_slug": "apple-iphone-16-pro-max",
        "author_slug": "kwise-technical",
        "intro": (
            "The 16 Pro Max is the better phone for video. It records 4K at 120fps, upgrades "
            "the ultra-wide from 12MP to 48MP, adds four studio microphones and carries the "
            "biggest battery Apple had shipped. For photography alone the gap is small — the "
            "main sensor and the 5× lens are largely unchanged."
        ),
        "winner_by_category": {
            "camera": "b", "display": "b", "battery": "b",
            "performance": "b", "value": "a", "portability": "a",
        },
        "overall_recommendation": (
            "If you shoot video for a living → iPhone 16 Pro Max, for 4K120 and the mic array. "
            "If you mainly take photos → iPhone 15 Pro Max, near-identical results for much less. "
            "If a 6.9-inch phone is too big for you → iPhone 15 Pro Max at 6.7 inches."
        ),
        "meta_description": (
            "iPhone 15 Pro Max vs 16 Pro Max in Nigeria: 4K120 video, 48MP ultra-wide, battery "
            "life compared. Which is worth the money."
        ),
        "faqs": [
            {"question": "What is the difference between iPhone 15 Pro Max and 16 Pro Max cameras?",
             "answer": (
                 "The main 48MP sensor and 5× telephoto are broadly similar. The 16 Pro Max "
                 "upgrades the ultra-wide from 12MP to 48MP with autofocus, adds 4K recording "
                 "at 120fps, and includes four studio-quality microphones. The gains are mostly "
                 "on the video side."
             ), "order": 1},
        ],
    },
    {
        "title": "iPhone 16e vs iPhone 15 — Battery or Cameras?",
        "slug": "iphone-16e-vs-iphone-15",
        "device_a_slug": "apple-iphone-16e",
        "device_b_slug": "apple-iphone-15",
        "author_slug": "kwise-editorial",
        "intro": (
            "This one comes down to a single trade. The iPhone 16e has a much bigger battery "
            "and a newer chip with a longer support runway. The iPhone 15 has an ultra-wide "
            "camera, MagSafe magnets and a brighter screen. Pick the one whose weakness you "
            "can live with."
        ),
        "winner_by_category": {
            "camera": "b", "display": "b", "battery": "a",
            "performance": "a", "value": "tie", "portability": "tie",
        },
        "overall_recommendation": (
            "If your phone dies before evening → iPhone 16e, it has the best battery at this size. "
            "If you shoot group photos or landscapes → iPhone 15, because the 16e has no ultra-wide lens. "
            "If you use magnetic car mounts or wallets → iPhone 15, the 16e has no MagSafe magnets."
        ),
        "meta_description": (
            "iPhone 16e vs iPhone 15 in Nigeria: better battery versus better cameras. Which "
            "trade-off suits you."
        ),
        "faqs": [
            {"question": "Does the iPhone 16e have MagSafe?",
             "answer": (
                 "No. It supports standard Qi wireless charging but has no MagSafe magnets, so "
                 "magnetic chargers, car mounts and wallets will not attach without a magnetic "
                 "case."
             ), "order": 1},
            {"question": "Why does the iPhone 16e have better battery life?",
             "answer": (
                 "Two reasons: a larger 4,005 mAh cell, and Apple's own C1 modem, which is more "
                 "power efficient than the Qualcomm modems in other iPhones."
             ), "order": 2},
        ],
    },
    # ─── Samsung vs Samsung ──────────────────────────────────────────────────
    {
        "title": "Galaxy S24 vs S24 Ultra — Which Samsung Should You Buy?",
        "slug": "galaxy-s24-vs-s24-ultra",
        "device_a_slug": "samsung-galaxy-s24",
        "device_b_slug": "samsung-galaxy-s24-ultra",
        "author_slug": "kwise-editorial",
        "intro": (
            "The S24 Ultra is better, but not for everyone. It wins clearly on camera range, "
            "battery and screen, and it adds the S Pen. The standard S24 runs the same "
            "Snapdragon chip on Canada-sourced units, weighs 65g less, and costs substantially "
            "less. Size and camera reach are the real decision, not speed."
        ),
        "winner_by_category": {
            "camera": "b", "display": "b", "battery": "b",
            "performance": "tie", "value": "a", "portability": "a",
        },
        "overall_recommendation": (
            "If you zoom often or shoot events → S24 Ultra, for the 5× periscope. "
            "If you want a phone you can use one-handed → Galaxy S24. "
            "If you take handwritten notes or annotate documents → S24 Ultra, for the S Pen. "
            "If battery life is the priority → S24 Ultra, 5,000 mAh against 4,000 mAh."
        ),
        "meta_description": (
            "Galaxy S24 vs S24 Ultra in Nigeria: camera, battery, size and price compared. "
            "Which Samsung flagship is the right buy."
        ),
        "faqs": [
            {"question": "Is the Galaxy S24 Ultra worth the extra money over the S24?",
             "answer": (
                 "It is if you use the zoom, the S Pen, or need all-day battery. The S24 Ultra "
                 "has a 5× optical periscope and a 5,000 mAh battery against the S24's 4,000 mAh. "
                 "If you do none of those things, the S24 delivers the same speed in a smaller, "
                 "cheaper body."
             ), "order": 1},
            {"question": "Does the Galaxy S24 have the Snapdragon or Exynos chip in Nigeria?",
             "answer": (
                 "It depends where the unit was sold originally. Canadian and US retail units "
                 "carry the Snapdragon 8 Gen 3 for Galaxy; European and most African retail "
                 "units carry the Exynos 2400. Check the model number on the specific device — "
                 "the two perform differently under sustained load."
             ), "order": 2},
            {"question": "Do both the S24 and S24 Ultra get seven years of updates?",
             "answer": (
                 "Yes. Samsung committed to seven years of OS and security updates for the "
                 "entire S24 family from launch, which is the longest Android support "
                 "commitment of that generation."
             ), "order": 3},
        ],
    },
    {
        "title": "Galaxy S23 Ultra vs S24 Ultra — Is the Upgrade Worth It?",
        "slug": "galaxy-s23-ultra-vs-s24-ultra",
        "device_a_slug": "samsung-galaxy-s23-ultra",
        "device_b_slug": "samsung-galaxy-s24-ultra",
        "author_slug": "kwise-technical",
        "intro": (
            "The S24 Ultra has the better screen and the better everyday zoom; the S23 Ultra "
            "has the longer optical reach. Samsung replaced the S23 Ultra's true 10× periscope "
            "with a 50MP 5× lens that crops to 10× — sharper at moderate distances, weaker at "
            "extreme ones. The flat, anti-reflective screen on the S24 Ultra is the bigger "
            "practical upgrade."
        ),
        "winner_by_category": {
            "camera": "tie", "display": "b", "battery": "tie",
            "performance": "b", "value": "a", "portability": "tie",
        },
        "overall_recommendation": (
            "If you shoot at extreme distances → S23 Ultra, it still has true 10× optical. "
            "If you use your phone outdoors in bright sun → S24 Ultra, the anti-glare screen is transformative. "
            "If you break screens or hate curved edges → S24 Ultra, the flat panel is cheaper to protect and repair. "
            "If value is the deciding factor → S23 Ultra gives you 90% of the phone."
        ),
        "meta_description": (
            "Galaxy S23 Ultra vs S24 Ultra in Nigeria: 10x versus 5x zoom, anti-glare screen, "
            "flat versus curved. Which Ultra to buy."
        ),
        "faqs": [
            {"question": "Why did Samsung remove the 10x zoom from the S24 Ultra?",
             "answer": (
                 "Samsung replaced the 10MP 10× periscope with a 50MP 5× lens. Because the new "
                 "sensor has far more resolution, cropping it to 10× produces more detail than "
                 "the old lens did at most realistic distances. At genuinely extreme range the "
                 "S23 Ultra's true optical 10× still wins."
             ), "order": 1},
            {"question": "What is Gorilla Armor on the S24 Ultra?",
             "answer": (
                 "It is a glass formulation with a strong anti-reflective coating. It cuts "
                 "screen reflections dramatically, which makes the phone far more readable in "
                 "direct sunlight — a genuine advantage in Nigerian daytime conditions."
             ), "order": 2},
        ],
    },
    {
        "title": "Galaxy S24 Ultra vs S25 Ultra — Should You Upgrade?",
        "slug": "galaxy-s24-ultra-vs-s25-ultra",
        "device_a_slug": "samsung-galaxy-s24-ultra",
        "device_b_slug": "samsung-galaxy-s25-ultra",
        "author_slug": "kwise-technical",
        "intro": (
            "The S25 Ultra's real upgrades are a 50MP ultra-wide replacing a 12MP one, a faster "
            "and cooler Snapdragon 8 Elite, and a body that is 14g lighter with a larger screen. "
            "Everything else — main camera, zoom lenses, battery, charging — carries over. For "
            "most buyers the S24 Ultra remains the better value."
        ),
        "winner_by_category": {
            "camera": "b", "display": "b", "battery": "tie",
            "performance": "b", "value": "a", "portability": "b",
        },
        "overall_recommendation": (
            "If you shoot wide landscapes or group photos → S25 Ultra, the 50MP ultra-wide is a real jump. "
            "If you game heavily → S25 Ultra, the Snapdragon 8 Elite runs cooler under sustained load. "
            "If you use the S Pen for remote camera control → S24 Ultra, the S25 Ultra dropped Bluetooth from the pen. "
            "If value decides it → S24 Ultra, comfortably."
        ),
        "meta_description": (
            "Galaxy S24 Ultra vs S25 Ultra in Nigeria: 50MP ultra-wide, Snapdragon 8 Elite, "
            "and the S Pen feature Samsung removed."
        ),
        "faqs": [
            {"question": "What did Samsung remove from the S Pen on the S25 Ultra?",
             "answer": (
                 "Bluetooth. The S25 Ultra's S Pen still writes and draws normally, but it can "
                 "no longer be used as a remote camera shutter or for air gestures. If you used "
                 "the pen to trigger the shutter from a distance, the S24 Ultra keeps that."
             ), "order": 1},
        ],
    },
    {
        "title": "Galaxy A54 vs A55 — Which Mid-Range Samsung to Buy",
        "slug": "galaxy-a54-vs-a55",
        "device_a_slug": "samsung-galaxy-a54-5g",
        "device_b_slug": "samsung-galaxy-a55-5g",
        "author_slug": "kwise-editorial",
        "intro": (
            "The cameras are the same, the battery is the same, and the charging speed is the "
            "same. What the A55 adds is a metal frame, tougher Gorilla Glass Victus+, a larger "
            "screen and a meaningfully better GPU. If you game, that GPU is the whole argument. "
            "If you don't, the A54 is the smarter spend."
        ),
        "winner_by_category": {
            "camera": "tie", "display": "b", "battery": "tie",
            "performance": "b", "value": "a", "portability": "a",
        },
        "overall_recommendation": (
            "If you play graphically heavy games → Galaxy A55, the Exynos 1480 GPU is a real upgrade. "
            "If you want the best price for the same cameras and battery → Galaxy A54. "
            "If you are hard on your phone → Galaxy A55, metal frame and Victus+ glass."
        ),
        "meta_description": (
            "Galaxy A54 vs A55 in Nigeria: same cameras, better gaming and build on the A55. "
            "Which mid-range Samsung is the better buy."
        ),
        "faqs": [
            {"question": "Is the Galaxy A55 camera better than the A54?",
             "answer": (
                 "No. Both use a 50MP main sensor with OIS, a 12MP ultra-wide, a 5MP macro and "
                 "a 32MP front camera. Photo output is very close. The A55's advantages are "
                 "build quality, screen size and graphics performance."
             ), "order": 1},
        ],
    },
    # ─── Google vs Google ────────────────────────────────────────────────────
    {
        "title": "Pixel 8a vs Pixel 9a — Camera or Battery?",
        "slug": "pixel-8a-vs-pixel-9a",
        "device_a_slug": "google-pixel-8a",
        "device_b_slug": "google-pixel-9a",
        "author_slug": "kwise-technical",
        "intro": (
            "The Pixel 9a has a much bigger battery, a bigger screen and a newer chip. The "
            "Pixel 8a has the physically larger main camera sensor, which still gives it an "
            "edge in low light. Both promise seven years of updates, so this is a battery "
            "versus low-light photography decision."
        ),
        "winner_by_category": {
            "camera": "a", "display": "b", "battery": "b",
            "performance": "b", "value": "a", "portability": "a",
        },
        "overall_recommendation": (
            "If you shoot indoors and at night → Pixel 8a, its larger sensor gathers more light. "
            "If you need your phone to last a full heavy day → Pixel 9a, 5,100 mAh against 4,492 mAh. "
            "If you want the newest hardware and IP68 → Pixel 9a."
        ),
        "meta_description": (
            "Pixel 8a vs Pixel 9a in Nigeria: bigger battery versus better low-light camera. "
            "Which Pixel A-series to buy."
        ),
        "faqs": [
            {"question": "Does the Pixel 9a take better photos than the Pixel 8a?",
             "answer": (
                 "In good light they are very close. In low light the Pixel 8a often has the "
                 "edge, because its main sensor is physically larger despite the lower "
                 "megapixel count. Sensor size matters more than megapixels for low-light "
                 "photography."
             ), "order": 1},
        ],
    },
    # ─── Cross-brand ─────────────────────────────────────────────────────────
    {
        "title": "iPhone 15 Pro Max vs Galaxy S24 Ultra — iOS or Android?",
        "slug": "iphone-15-pro-max-vs-galaxy-s24-ultra",
        "device_a_slug": "apple-iphone-15-pro-max",
        "device_b_slug": "samsung-galaxy-s24-ultra",
        "author_slug": "kwise-editorial",
        "intro": (
            "The S24 Ultra wins on screen, zoom versatility and the S Pen. The iPhone 15 Pro "
            "Max wins on video quality, app ecosystem consistency and long-term resale value "
            "in Nigeria. Neither is objectively better — the platform you already have "
            "accessories and contacts on usually decides it."
        ),
        "winner_by_category": {
            "camera": "b", "display": "b", "battery": "b",
            "performance": "tie", "value": "b", "portability": "a",
        },
        "overall_recommendation": (
            "If you shoot and edit video → iPhone 15 Pro Max, still the strongest video pipeline. "
            "If you want the most versatile camera kit and a stylus → Galaxy S24 Ultra. "
            "If you resell your phone every year or two → iPhone, it holds value better in Nigeria. "
            "If you work outdoors in bright sun → Galaxy S24 Ultra, for the anti-glare screen."
        ),
        "meta_description": (
            "iPhone 15 Pro Max vs Galaxy S24 Ultra in Nigeria: video, zoom, screen and resale "
            "value compared. Which flagship suits you."
        ),
        "faqs": [
            {"question": "Which holds resale value better in Nigeria, iPhone or Samsung?",
             "answer": (
                 "iPhones generally depreciate more slowly in the Nigerian used market than "
                 "equivalent Android flagships. If you upgrade frequently, that difference "
                 "narrows the real cost gap between the two."
             ), "order": 1},
            {"question": "Is the Galaxy S24 Ultra camera better than the iPhone 15 Pro Max?",
             "answer": (
                 "For stills and zoom range, the S24 Ultra is more versatile — 200MP main "
                 "sensor, 3× and 5× lenses. For video, the iPhone remains stronger on colour "
                 "consistency, stabilisation and editing workflow. It depends on which you "
                 "shoot more."
             ), "order": 2},
        ],
    },
    {
        "title": "Galaxy S24 vs Pixel 8 — Best Compact Android in Nigeria",
        "slug": "galaxy-s24-vs-pixel-8",
        "device_a_slug": "samsung-galaxy-s24",
        "device_b_slug": "google-pixel-8",
        "author_slug": "kwise-technical",
        "intro": (
            "Both are small Android phones with seven-year update promises and excellent "
            "screens. The Galaxy S24 is faster, has a real 3× telephoto lens and comes with "
            "local service support. The Pixel 8 processes photos better and runs clean Android "
            "with no duplicate apps. Speed versus photo processing is the choice."
        ),
        "winner_by_category": {
            "camera": "tie", "display": "a", "battery": "b",
            "performance": "a", "value": "b", "portability": "tie",
        },
        "overall_recommendation": (
            "If you game or want the fastest phone → Galaxy S24, Snapdragon beats Tensor clearly. "
            "If you want the best point-and-shoot photos with no effort → Pixel 8. "
            "If you need zoom → Galaxy S24, the Pixel 8 has no telephoto lens at all. "
            "If local warranty and service matter → Galaxy S24, Samsung has a service presence in Nigeria and Google does not."
        ),
        "meta_description": (
            "Galaxy S24 vs Pixel 8 in Nigeria: performance, camera processing, zoom and local "
            "support compared. Best compact Android pick."
        ),
        "faqs": [
            {"question": "Can I service a Google Pixel in Nigeria?",
             "answer": (
                 "Google has no official retail or service presence in Nigeria, so Pixel repairs "
                 "depend on independent technicians and imported parts. Samsung and Apple both "
                 "have far wider local service networks. Factor that into the decision if you "
                 "keep phones for years."
             ), "order": 1},
        ],
    },
    # ─── Laptops ─────────────────────────────────────────────────────────────
    {
        "title": "ThinkPad X13 vs Dell Latitude 5530 — Which Refurbished Laptop?",
        "slug": "thinkpad-x13-vs-latitude-5530",
        "device_a_slug": "lenovo-thinkpad-x13-gen-3",
        "device_b_slug": "dell-latitude-5530",
        "author_slug": "kwise-technical",
        "intro": (
            "These solve different problems. The ThinkPad X13 is a 1.2kg 13.3-inch machine "
            "with the best keyboard in its class and a taller 16:10 screen. The Latitude 5530 "
            "is a 1.7kg 15.6-inch desk machine with a numeric keypad and, crucially, "
            "upgradeable RAM. Portability versus screen size and expandability."
        ),
        "winner_by_category": {
            "display": "a", "battery": "a", "performance": "tie",
            "value": "b", "portability": "a", "keyboard": "a", "upgradeability": "b",
        },
        "overall_recommendation": (
            "If you carry your laptop daily → ThinkPad X13, half a kilo lighter is a real difference. "
            "If you work in spreadsheets or accounting → Latitude 5530, for the bigger screen and numeric keypad. "
            "If you want to add RAM later → Latitude 5530, it has two accessible SO-DIMM slots. "
            "If you type all day → ThinkPad X13, the keyboard is genuinely better."
        ),
        "meta_description": (
            "ThinkPad X13 vs Dell Latitude 5530 in Nigeria: weight, screen, keyboard and RAM "
            "upgradeability compared for refurbished buyers."
        ),
        "faqs": [
            {"question": "Can I upgrade the RAM on a ThinkPad X13 Gen 3?",
             "answer": (
                 "Usually not. Most X13 Gen 3 configurations use soldered LPDDR5 memory, so the "
                 "RAM you buy is the RAM you keep. Confirm the specific configuration before "
                 "purchase and buy 16GB or more if you multitask heavily."
             ), "order": 1},
            {"question": "Is a 250-nit laptop screen bright enough?",
             "answer": (
                 "It is fine in an office or at night, but it becomes hard to read near a "
                 "window or in a bright room. If you often work in daylight, look for a 400-nit "
                 "panel configuration instead."
             ), "order": 2},
            {"question": "Why are Canadian off-lease laptops good value?",
             "answer": (
                 "Corporate fleets replace machines on fixed three-year cycles regardless of "
                 "condition, so units come off lease still working well and having been "
                 "maintained under warranty. They were also specified for business durability "
                 "rather than consumer price points."
             ), "order": 3},
        ],
    },
    {
        "title": "MacBook Air M1 vs M2 — Which Is the Better Buy?",
        "slug": "macbook-air-m1-vs-m2",
        "device_a_slug": "apple-macbook-air-m1",
        "device_b_slug": "apple-macbook-air-m2",
        "author_slug": "kwise-technical",
        "intro": (
            "The M2 Air is the better machine for anyone who takes video calls or works near "
            "daylight — a 500-nit screen against 400, and a 1080p webcam against 720p. The M1 "
            "is the better value and, on 256GB models, actually has faster storage. Both are "
            "fanless and both last all day."
        ),
        "winner_by_category": {
            "display": "b", "battery": "tie", "performance": "b",
            "value": "a", "portability": "b", "webcam": "b",
        },
        "overall_recommendation": (
            "If you are on video calls regularly → MacBook Air M2, the 1080p webcam is a clear upgrade. "
            "If you work near windows or outdoors → MacBook Air M2, 500 nits versus 400. "
            "If budget is the priority → MacBook Air M1, still excellent and cheaper. "
            "Whichever you choose, buy 16GB RAM if you can — it cannot be upgraded afterwards."
        ),
        "meta_description": (
            "MacBook Air M1 vs M2 in Nigeria: screen brightness, webcam, SSD speed and value "
            "compared. Which to buy used."
        ),
        "faqs": [
            {"question": "Is 8GB RAM enough on a MacBook Air?",
             "answer": (
                 "For browsing, documents and light work, yes. For heavy multitasking, large "
                 "spreadsheets, development work or photo editing, 8GB becomes limiting and the "
                 "machine starts writing to the SSD to compensate. RAM is soldered on both "
                 "models, so buy 16GB if your work is demanding."
             ), "order": 1},
            {"question": "Why is the 256GB MacBook Air M2 SSD slower?",
             "answer": (
                 "Apple used a single larger NAND chip in the 256GB M2 configuration instead of "
                 "two smaller ones. Two chips can be read in parallel; one cannot. In practice "
                 "the difference shows up in large file transfers, not in everyday use."
             ), "order": 2},
        ],
    },
    {
        "title": "ThinkPad T14 vs HP EliteBook 840 G9 — Business Laptop Comparison",
        "slug": "thinkpad-t14-vs-elitebook-840-g9",
        "device_a_slug": "lenovo-thinkpad-t14-gen-3",
        "device_b_slug": "hp-elitebook-840-g9",
        "author_slug": "kwise-technical",
        "intro": (
            "The ThinkPad T14 has the better keyboard and more sustained performance from its "
            "P-series chip. The EliteBook 840 G9 has a far better webcam — 5MP with auto "
            "framing against 1080p — and better speakers. If your day is meetings, take the "
            "HP. If your day is typing and processing, take the Lenovo."
        ),
        "winner_by_category": {
            "display": "tie", "battery": "tie", "performance": "a",
            "value": "tie", "portability": "b", "keyboard": "a", "webcam": "b",
        },
        "overall_recommendation": (
            "If you live on video calls → EliteBook 840 G9, the 5MP auto-framing webcam is in another class. "
            "If you write, code or compile → ThinkPad T14, better keyboard and stronger sustained performance. "
            "If you want the option to add RAM later → ThinkPad T14, many configurations have a SO-DIMM slot."
        ),
        "meta_description": (
            "ThinkPad T14 Gen 3 vs HP EliteBook 840 G9 in Nigeria: keyboard, webcam, "
            "performance and upgradeability compared."
        ),
        "faqs": [
            {"question": "Which business laptop has the best webcam?",
             "answer": (
                 "The HP EliteBook 840 G9, by a clear margin. Its 5MP camera with automatic "
                 "framing and lighting correction is noticeably better than the 1080p cameras "
                 "in comparable ThinkPad and Latitude models."
             ), "order": 1},
        ],
    },
]
