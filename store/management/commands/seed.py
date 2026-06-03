"""
python manage.py seed

Populates the database with the initial Kwise World catalog.
Safe to run multiple times — uses update_or_create.
"""
from django.core.management.base import BaseCommand
from store.models import Category, Brand, Product, ProductSpec


CATEGORIES = [
    {
        "slug": "phones", "name": "Phones", "icon": "phone", "order": 1,
        "blurb": "iPhone & Samsung — brand new and clean UK-used.",
        "brands": [
            {"slug": "iphone", "name": "iPhone"},
            {"slug": "samsung", "name": "Samsung"},
        ],
    },
    {
        "slug": "laptops", "name": "Laptops", "icon": "laptop", "order": 2,
        "blurb": "HP, Lenovo, Apple & Dell — top models for work, study and play.",
        "brands": [
            {"slug": "hp", "name": "HP"},
            {"slug": "lenovo", "name": "Lenovo"},
            {"slug": "apple", "name": "Apple"},
            {"slug": "dell", "name": "Dell"},
        ],
    },
    {
        "slug": "accessories", "name": "Accessories", "icon": "charger", "order": 3,
        "blurb": "Chargers, power banks, cables, pouches & screen guards.",
        "brands": [
            {"slug": "chargers", "name": "Chargers"},
            {"slug": "power-banks", "name": "Power Banks"},
            {"slug": "cables", "name": "Cables"},
            {"slug": "pouches", "name": "Pouches & Cases"},
            {"slug": "screen-guards", "name": "Screen Guards"},
        ],
    },
    {
        "slug": "laptop-accessories", "name": "Laptop Accessories", "icon": "battery", "order": 4,
        "blurb": "Batteries, adapters, cooling pads & sleeves.",
        "brands": [
            {"slug": "laptop-batteries", "name": "Batteries"},
            {"slug": "laptop-chargers", "name": "Adapters"},
            {"slug": "laptop-other", "name": "Cooling & Sleeves"},
        ],
    },
]

PRODUCTS = [
    {"id": "iphone-15-pro-max", "name": "iPhone 15 Pro Max", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 1850000, "status": "Brand New", "rating": 4.9, "review_count": 128, "badge": "Best Seller", "is_featured": True, "colors": ["Natural Titanium", "Blue Titanium", "Black Titanium"], "description": "The flagship. Titanium build, A17 Pro chip and a 5x telephoto camera. Sealed, with full warranty.", "specs": {"Storage": "256GB", "Display": "6.7\" Super Retina XDR", "Chip": "A17 Pro", "Camera": "48MP Triple", "Battery": "4441mAh"}},
    {"id": "iphone-15", "name": "iPhone 15", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 1350000, "status": "Brand New", "rating": 4.8, "review_count": 74, "is_featured": True, "colors": ["Black", "Blue", "Pink", "Green"], "description": "Dynamic Island, USB-C and a 48MP main camera in a lighter, friendlier package.", "specs": {"Storage": "128GB", "Display": "6.1\" Super Retina XDR", "Chip": "A16 Bionic", "Camera": "48MP Dual"}},
    {"id": "iphone-14-pro", "name": "iPhone 14 Pro", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 950000, "old_price": 1100000, "status": "UK-Used", "rating": 4.7, "review_count": 56, "description": "Clean UK-used Pro. Battery health 89%+, no scratches, fully tested.", "specs": {"Storage": "256GB", "Display": "6.1\" ProMotion", "Chip": "A16 Bionic", "Camera": "48MP Triple"}},
    {"id": "iphone-13", "name": "iPhone 13", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 620000, "status": "UK-Used", "rating": 4.6, "review_count": 91, "description": "The everyday favourite. Excellent UK-used condition, great battery.", "specs": {"Storage": "128GB", "Display": "6.1\" Super Retina XDR", "Chip": "A15 Bionic", "Camera": "12MP Dual"}},
    {"id": "iphone-12", "name": "iPhone 12", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 470000, "status": "UK-Used", "rating": 4.5, "review_count": 63, "description": "Still mighty. 5G, flat edges, OLED display. Tested and certified.", "specs": {"Storage": "128GB", "Display": "6.1\" Super Retina XDR", "Chip": "A14 Bionic", "Camera": "12MP Dual"}},
    {"id": "iphone-11", "name": "iPhone 11", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 330000, "status": "UK-Used", "rating": 4.4, "review_count": 110, "description": "The smart-budget pick. Reliable, clean UK-used units.", "specs": {"Storage": "64GB", "Display": "6.1\" Liquid Retina", "Chip": "A13 Bionic", "Camera": "12MP Dual"}},
    {"id": "galaxy-s24-ultra", "name": "Galaxy S24 Ultra", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 1550000, "status": "Brand New", "rating": 4.9, "review_count": 88, "badge": "Best Seller", "is_featured": True, "colors": ["Titanium Gray", "Titanium Black", "Titanium Violet"], "description": "Built-in S Pen, 200MP camera and Galaxy AI. The Android flagship to beat.", "specs": {"Storage": "256GB", "Display": "6.8\" QHD+ AMOLED", "Chip": "Snapdragon 8 Gen 3", "Camera": "200MP Quad", "SPen": "Built-in"}},
    {"id": "galaxy-s23", "name": "Galaxy S23", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 980000, "status": "Brand New", "rating": 4.7, "review_count": 42, "is_featured": True, "colors": ["Phantom Black", "Cream", "Green"], "description": "Compact flagship power with all-day battery and a brilliant display.", "specs": {"Storage": "256GB", "Display": "6.1\" FHD+ AMOLED", "Chip": "Snapdragon 8 Gen 2", "Camera": "50MP Triple"}},
    {"id": "galaxy-z-flip5", "name": "Galaxy Z Flip5", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 1150000, "status": "Brand New", "rating": 4.6, "review_count": 29, "colors": ["Mint", "Graphite", "Lavender"], "description": "Pocketable, foldable, fun. A flagship that folds to half the size.", "specs": {"Storage": "256GB", "Display": "6.7\" Foldable AMOLED", "Chip": "Snapdragon 8 Gen 2", "Cover": "3.4\" Flex Window"}},
    {"id": "galaxy-a55", "name": "Galaxy A55", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 520000, "status": "Brand New", "rating": 4.5, "review_count": 37, "description": "Premium mid-ranger: metal frame, big AMOLED, dependable battery.", "specs": {"Storage": "128GB", "Display": "6.6\" Super AMOLED", "Chip": "Exynos 1480", "Camera": "50MP Triple"}},
    {"id": "galaxy-s22", "name": "Galaxy S22", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 560000, "status": "UK-Used", "rating": 4.5, "review_count": 51, "description": "Clean UK-used flagship at a smart price. Fully tested.", "specs": {"Storage": "128GB", "Display": "6.1\" AMOLED", "Chip": "Snapdragon 8 Gen 1", "Camera": "50MP Triple"}},
    {"id": "galaxy-a34", "name": "Galaxy A34", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 310000, "status": "UK-Used", "rating": 4.3, "review_count": 44, "description": "Big screen, big battery, small price. Great UK-used value.", "specs": {"Storage": "128GB", "Display": "6.6\" Super AMOLED", "Chip": "Dimensity 1080", "Camera": "48MP Triple"}},
    {"id": "hp-spectre-x360", "name": "HP Spectre x360", "cat": "laptops", "brand": "hp", "thumb": "laptop", "tint": "blue", "price": 1650000, "status": "Brand New", "rating": 4.8, "review_count": 33, "badge": "Best Seller", "is_featured": True, "description": "Convertible premium ultrabook. OLED touch display, gem-cut design.", "specs": {"CPU": "Intel Core Ultra 7", "RAM": "16GB", "Storage": "1TB SSD", "Display": "13.5\" 3K2K OLED Touch"}},
    {"id": "hp-pavilion-15", "name": "HP Pavilion 15", "cat": "laptops", "brand": "hp", "thumb": "laptop", "tint": "blue", "price": 780000, "status": "Brand New", "rating": 4.5, "review_count": 28, "description": "The dependable all-rounder for work and study. Fast SSD, full-size keyboard.", "specs": {"CPU": "Intel Core i5-1335U", "RAM": "16GB", "Storage": "512GB SSD", "Display": "15.6\" FHD"}},
    {"id": "hp-elitebook-840", "name": "HP EliteBook 840 G7", "cat": "laptops", "brand": "hp", "thumb": "laptop", "tint": "blue", "price": 520000, "status": "UK-Used", "rating": 4.6, "review_count": 47, "description": "Business-grade build, ex-UK corporate. Tough, fast, professional.", "specs": {"CPU": "Intel Core i7-10610U", "RAM": "16GB", "Storage": "512GB SSD", "Display": "14\" FHD"}},
    {"id": "hp-probook-450", "name": "HP ProBook 450 G8", "cat": "laptops", "brand": "hp", "thumb": "laptop", "tint": "blue", "price": 410000, "status": "UK-Used", "rating": 4.4, "review_count": 31, "description": "Reliable workhorse for everyday productivity. Clean UK-used.", "specs": {"CPU": "Intel Core i5-1135G7", "RAM": "8GB", "Storage": "256GB SSD", "Display": "15.6\" FHD"}},
    {"id": "lenovo-thinkpad-x1", "name": "Lenovo ThinkPad X1 Carbon", "cat": "laptops", "brand": "lenovo", "thumb": "laptop", "tint": "indigo", "price": 1450000, "status": "Brand New", "rating": 4.8, "review_count": 39, "is_featured": True, "description": "The iconic business ultrabook — featherlight carbon-fibre, legendary keyboard.", "specs": {"CPU": "Intel Core i7-1355U", "RAM": "16GB", "Storage": "1TB SSD", "Display": "14\" 2.8K OLED"}},
    {"id": "lenovo-yoga-slim-7", "name": "Lenovo Yoga Slim 7", "cat": "laptops", "brand": "lenovo", "thumb": "laptop", "tint": "indigo", "price": 920000, "status": "Brand New", "rating": 4.6, "review_count": 22, "description": "Slim, stylish and quiet. A gorgeous OLED for creators on the move.", "specs": {"CPU": "AMD Ryzen 7 7840U", "RAM": "16GB", "Storage": "512GB SSD", "Display": "14\" 2.8K OLED"}},
    {"id": "lenovo-ideapad-3", "name": "Lenovo IdeaPad 3", "cat": "laptops", "brand": "lenovo", "thumb": "laptop", "tint": "indigo", "price": 450000, "status": "Brand New", "rating": 4.3, "review_count": 41, "description": "Affordable, dependable everyday laptop for school and home.", "specs": {"CPU": "AMD Ryzen 5 7520U", "RAM": "8GB", "Storage": "512GB SSD", "Display": "15.6\" FHD"}},
    {"id": "lenovo-thinkpad-t480", "name": "Lenovo ThinkPad T480", "cat": "laptops", "brand": "lenovo", "thumb": "laptop", "tint": "indigo", "price": 380000, "status": "UK-Used", "rating": 4.5, "review_count": 58, "description": "The bulletproof classic. Ex-UK, dual-battery, endlessly reliable.", "specs": {"CPU": "Intel Core i5-8350U", "RAM": "16GB", "Storage": "256GB SSD", "Display": "14\" FHD"}},
    {"id": "charger-20w", "name": "20W USB-C Fast Charger", "cat": "accessories", "brand": "chargers", "thumb": "charger", "tint": "orange", "price": 18000, "rating": 4.6, "review_count": 84, "description": "Fast, compact USB-C power adapter. Charges iPhone & Galaxy in a hurry.", "specs": {"Output": "20W PD", "Port": "USB-C", "Box": "Charger only"}},
    {"id": "charger-65w-gan", "name": "65W GaN Charger", "cat": "accessories", "brand": "chargers", "thumb": "charger", "tint": "orange", "price": 32000, "rating": 4.7, "review_count": 52, "is_featured": True, "description": "One small brick for phone, tablet and laptop. GaN-cool and travel-ready.", "specs": {"Output": "65W PD", "Ports": "2x USB-C + USB-A", "Tech": "GaN"}},
    {"id": "powerbank-20000", "name": "20,000mAh Power Bank", "cat": "accessories", "brand": "power-banks", "thumb": "powerbank", "tint": "orange", "price": 42000, "rating": 4.6, "review_count": 67, "is_featured": True, "description": "Multi-day power for trips and long days. Fast-charge in and out.", "specs": {"Capacity": "20,000mAh", "Output": "22.5W", "Ports": "USB-C + 2x USB-A"}},
    {"id": "powerbank-10000", "name": "10,000mAh Slim Power Bank", "cat": "accessories", "brand": "power-banks", "thumb": "powerbank", "tint": "orange", "price": 28000, "rating": 4.5, "review_count": 39, "description": "Pocket-slim top-up that disappears into a bag.", "specs": {"Capacity": "10,000mAh", "Output": "20W", "Ports": "USB-C + USB-A"}},
    {"id": "cable-usbc-lightning", "name": "USB-C to Lightning Cable", "cat": "accessories", "brand": "cables", "thumb": "cable", "tint": "orange", "price": 9500, "rating": 4.5, "review_count": 73, "description": "Certified fast-charge cable for iPhone. Built to last.", "specs": {"Length": "1m", "Rating": "MFi Certified", "Speed": "Fast Charge"}},
    {"id": "cable-usbc-braided", "name": "Braided USB-C Cable 2m", "cat": "accessories", "brand": "cables", "thumb": "cable", "tint": "orange", "price": 7000, "rating": 4.4, "review_count": 61, "description": "Long, tough, tangle-free. Reaches from the socket to the sofa.", "specs": {"Length": "2m", "Jacket": "Nylon Braided", "Speed": "60W"}},
    {"id": "pouch-leather", "name": "Leather Phone Pouch", "cat": "accessories", "brand": "pouches", "thumb": "case", "tint": "orange", "price": 12000, "rating": 4.6, "review_count": 28, "description": "Slim sleeve that keeps your phone scratch-free in style.", "specs": {"Material": "PU Leather", "Fit": "Universal 6.1–6.8\""}},
    {"id": "case-clear", "name": "Shockproof Clear Case", "cat": "accessories", "brand": "pouches", "thumb": "case", "tint": "orange", "price": 8500, "rating": 4.5, "review_count": 95, "description": "Crystal-clear protection that shows off your phone.", "specs": {"Material": "TPU + PC", "Drop": "2m tested"}},
    {"id": "screen-guard-tempered", "name": "Tempered Glass Screen Guard", "cat": "accessories", "brand": "screen-guards", "thumb": "shield", "tint": "orange", "price": 5000, "rating": 4.5, "review_count": 142, "description": "Crisp, crack-resistant 9H glass. Comes with an alignment kit.", "specs": {"Hardness": "9H", "Pack": "2-pack + kit"}},
    {"id": "screen-guard-privacy", "name": "Privacy Screen Guard", "cat": "accessories", "brand": "screen-guards", "thumb": "shield", "tint": "orange", "price": 7500, "rating": 4.4, "review_count": 38, "description": "Keep prying eyes out. Anti-spy 9H tempered glass.", "specs": {"Hardness": "9H", "Feature": "28° Privacy Filter"}},
    {"id": "hp-charger-65w", "name": "HP 65W Laptop Charger", "cat": "laptop-accessories", "brand": "laptop-chargers", "thumb": "charger", "tint": "blue", "price": 22000, "rating": 4.5, "review_count": 33, "description": "Genuine-grade replacement charger for HP laptops.", "specs": {"Output": "65W", "Tip": "Blue Pin / USB-C", "Fit": "HP Pavilion / EliteBook"}},
    {"id": "lenovo-adapter-65w", "name": "Lenovo 65W USB-C Adapter", "cat": "laptop-accessories", "brand": "laptop-chargers", "thumb": "charger", "tint": "indigo", "price": 24000, "rating": 4.6, "review_count": 27, "description": "Slim USB-C power adapter for modern Lenovo machines.", "specs": {"Output": "65W", "Port": "USB-C", "Fit": "ThinkPad / Yoga / IdeaPad"}},
    {"id": "thinkpad-battery", "name": "ThinkPad Replacement Battery", "cat": "laptop-accessories", "brand": "laptop-batteries", "thumb": "battery", "tint": "indigo", "price": 38000, "rating": 4.4, "review_count": 19, "is_featured": True, "description": "Bring an old ThinkPad back to all-day life.", "specs": {"Capacity": "57Wh", "Cells": "6-cell", "Fit": "ThinkPad T-series"}},
    {"id": "hp-pavilion-battery", "name": "HP Pavilion Battery", "cat": "laptop-accessories", "brand": "laptop-batteries", "thumb": "battery", "tint": "blue", "price": 35000, "rating": 4.3, "review_count": 21, "description": "Fresh battery for fading HP Pavilions. Easy swap.", "specs": {"Capacity": "41Wh", "Cells": "3-cell", "Fit": "HP Pavilion 15"}},
    {"id": "cooling-pad", "name": "Laptop Cooling Pad", "cat": "laptop-accessories", "brand": "laptop-other", "thumb": "laptop", "tint": "blue", "price": 19000, "rating": 4.5, "review_count": 44, "description": "Keep things cool on hot afternoons. Adjustable, quiet fans.", "specs": {"Fans": "5x Quiet", "Fit": "Up to 17\"", "Ports": "USB Pass-through"}},
    {"id": "laptop-sleeve", "name": "15.6\" Laptop Sleeve", "cat": "laptop-accessories", "brand": "laptop-other", "thumb": "case", "tint": "indigo", "price": 11000, "rating": 4.6, "review_count": 36, "description": "Padded, water-resistant protection with a handy front pocket.", "specs": {"Fit": "15.6\"", "Material": "Water-resistant", "Pocket": "Front zip"}},
    # One-time offers
    {"id": "ot-iphone-14-promax", "name": "iPhone 14 Pro Max", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 780000, "old_price": 980000, "status": "Nigeria-Used", "is_one_time": True, "stock": 1, "rating": 4.5, "review_count": 6, "one_time_note": "Tiny hairline scratch on back glass. Screen flawless. Battery 86%.", "description": "One unit only. A clean Nigeria-used Pro Max at a price that won't repeat.", "specs": {"Storage": "256GB", "Display": "6.7\" ProMotion", "Chip": "A16 Bionic", "Camera": "48MP Triple"}},
    {"id": "ot-galaxy-s23-ultra", "name": "Galaxy S23 Ultra", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 820000, "old_price": 1000000, "status": "UK-Used", "is_one_time": True, "stock": 1, "rating": 4.4, "review_count": 4, "one_time_note": "Faint single pixel dot, invisible in normal use. S Pen included.", "description": "One unit only. UK-used Ultra with a barely-there blemish and a big discount.", "specs": {"Storage": "256GB", "Display": "6.8\" QHD+ AMOLED", "Chip": "Snapdragon 8 Gen 2", "Camera": "200MP Quad"}},
    {"id": "ot-macbook-air-m1", "name": "MacBook Air M1", "cat": "laptops", "brand": "hp", "thumb": "laptop", "tint": "indigo", "price": 650000, "old_price": 820000, "status": "Nigeria-Used", "is_one_time": True, "stock": 1, "rating": 4.6, "review_count": 9, "one_time_note": "Small dent on lid corner. Battery cycle count 210. Runs perfectly.", "description": "One unit only. A silent, fast M1 Air with a cosmetic dent — pure value.", "specs": {"CPU": "Apple M1", "RAM": "8GB", "Storage": "256GB SSD", "Display": "13.3\" Retina"}},
    {"id": "ot-hp-elitebook-dent", "name": "HP EliteBook 840 (ex-UK)", "cat": "laptops", "brand": "hp", "thumb": "laptop", "tint": "blue", "price": 360000, "old_price": 520000, "status": "UK-Used", "is_one_time": True, "stock": 1, "rating": 4.2, "review_count": 3, "one_time_note": "Visible dent on palm rest. Fully functional, keyboard perfect.", "description": "One unit only. Workhorse EliteBook with a battle scar and a steep markdown.", "specs": {"CPU": "Intel Core i7-10610U", "RAM": "16GB", "Storage": "512GB SSD", "Display": "14\" FHD"}},
    {"id": "ot-galaxy-zfold4", "name": "Galaxy Z Fold4", "cat": "phones", "brand": "samsung", "thumb": "phone", "tint": "indigo", "price": 720000, "old_price": 950000, "status": "UK-Used", "is_one_time": True, "stock": 1, "rating": 4.3, "review_count": 5, "one_time_note": "Light crease wear (normal for folds). Hinge tight, no dead pixels.", "description": "One unit only. A foldable tablet-phone at an unrepeatable price.", "specs": {"Storage": "256GB", "Display": "7.6\" Foldable AMOLED", "Chip": "Snapdragon 8+ Gen 1", "Cover": "6.2\" AMOLED"}},
    {"id": "ot-iphone-13-promax", "name": "iPhone 13 Pro Max", "cat": "phones", "brand": "iphone", "thumb": "phone", "tint": "blue", "price": 560000, "old_price": 700000, "status": "Nigeria-Used", "is_one_time": True, "stock": 1, "rating": 4.5, "review_count": 7, "one_time_note": "Aftermarket screen (excellent quality). Body clean. Battery 88%.", "description": "One unit only. Big-battery Pro Max with a quality replacement screen.", "specs": {"Storage": "128GB", "Display": "6.7\" ProMotion", "Chip": "A15 Bionic", "Camera": "12MP Triple"}},
]


class Command(BaseCommand):
    help = "Seed the database with the initial Kwise World catalog."

    def handle(self, *args, **options):
        cat_map = {}
        brand_map = {}

        for c_data in CATEGORIES:
            brands_data = c_data.pop("brands")
            cat, _ = Category.objects.update_or_create(
                slug=c_data["slug"],
                defaults={k: v for k, v in c_data.items() if k != "slug"},
            )
            cat_map[cat.slug] = cat
            c_data["brands"] = brands_data  # restore

            for b_data in brands_data:
                brand, _ = Brand.objects.update_or_create(
                    category=cat, slug=b_data["slug"],
                    defaults={"name": b_data["name"]},
                )
                brand_map[(cat.slug, brand.slug)] = brand

        self.stdout.write(f"  {Category.objects.count()} categories, {Brand.objects.count()} brands")

        for p_data in PRODUCTS:
            specs = p_data.pop("specs", {})
            cat_slug = p_data.pop("cat")
            brand_slug = p_data.pop("brand")
            cat = cat_map[cat_slug]
            brand = brand_map[(cat_slug, brand_slug)]

            product, _ = Product.objects.update_or_create(
                id=p_data["id"],
                defaults={
                    "name": p_data["name"],
                    "category": cat,
                    "brand": brand,
                    "thumb": p_data.get("thumb", "phone"),
                    "tint": p_data.get("tint", "blue"),
                    "price": p_data["price"],
                    "old_price": p_data.get("old_price"),
                    "status": p_data.get("status", "Brand New"),
                    "rating": p_data.get("rating", 4.6),
                    "review_count": p_data.get("review_count", 0),
                    "is_featured": p_data.get("is_featured", False),
                    "badge": p_data.get("badge", ""),
                    "is_one_time": p_data.get("is_one_time", False),
                    "stock": p_data.get("stock", 25),
                    "description": p_data.get("description", ""),
                    "one_time_note": p_data.get("one_time_note", ""),
                    "colors": p_data.get("colors", []),
                },
            )

            ProductSpec.objects.filter(product=product).delete()
            for order, (key, value) in enumerate(specs.items()):
                ProductSpec.objects.create(product=product, key=key, value=value, order=order)

        self.stdout.write(f"  {Product.objects.count()} products")
        self.stdout.write(self.style.SUCCESS("Seed complete."))
