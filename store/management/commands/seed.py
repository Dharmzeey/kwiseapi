"""
python manage.py seed

Populates the database with the initial Kwise World catalog.
Safe to run multiple times — uses update_or_create.

iPhone variants are generated automatically from iphone_catalog_2.csv.
Samsung variants are generated automatically from samsung_catalog.csv.
Laptops, accessories, and one-time offers are defined inline.
"""
import csv
import os

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Category, Brand, Product, ProductSpec


# ── iPhone model specs lookup ─────────────────────────────────────────────────

IPHONE_SPECS = {
    "iPhone 6":          {"series": "iPhone 6",  "chip": "A8",          "display": '4.7" Retina IPS LCD',                        "camera": "8MP",                              "battery": "1810mAh", "featured": False, "badge": ""},
    "iPhone 6 Plus":     {"series": "iPhone 6",  "chip": "A8",          "display": '5.5" Retina IPS LCD',                        "camera": "8MP OIS",                          "battery": "2915mAh", "featured": False, "badge": ""},
    "iPhone 6s":         {"series": "iPhone 6s", "chip": "A9",          "display": '4.7" Retina IPS LCD',                        "camera": "12MP",                             "battery": "1715mAh", "featured": False, "badge": ""},
    "iPhone 6s Plus":    {"series": "iPhone 6s", "chip": "A9",          "display": '5.5" Retina IPS LCD',                        "camera": "12MP OIS",                         "battery": "2750mAh", "featured": False, "badge": ""},
    "iPhone 7":          {"series": "iPhone 7",  "chip": "A10 Fusion",  "display": '4.7" Retina IPS LCD',                        "camera": "12MP",                             "battery": "1960mAh", "featured": False, "badge": ""},
    "iPhone 7 Plus":     {"series": "iPhone 7",  "chip": "A10 Fusion",  "display": '5.5" Retina IPS LCD',                        "camera": "12MP Dual OIS",                    "battery": "2900mAh", "featured": False, "badge": ""},
    "iPhone 8":          {"series": "iPhone 8",  "chip": "A11 Bionic",  "display": '4.7" Retina IPS LCD',                        "camera": "12MP",                             "battery": "1821mAh", "featured": False, "badge": ""},
    "iPhone 8 Plus":     {"series": "iPhone 8",  "chip": "A11 Bionic",  "display": '5.5" Retina IPS LCD',                        "camera": "12MP Dual OIS",                    "battery": "2691mAh", "featured": False, "badge": ""},
    "iPhone X":          {"series": "iPhone X",  "chip": "A11 Bionic",  "display": '5.8" Super Retina OLED',                     "camera": "12MP Dual OIS",                    "battery": "2716mAh", "featured": False, "badge": ""},
    "iPhone XS":         {"series": "iPhone XS", "chip": "A12 Bionic",  "display": '5.8" Super Retina XDR OLED',                 "camera": "12MP Dual OIS",                    "battery": "2658mAh", "featured": False, "badge": ""},
    "iPhone XS Max":     {"series": "iPhone XS", "chip": "A12 Bionic",  "display": '6.5" Super Retina XDR OLED',                 "camera": "12MP Dual OIS",                    "battery": "3174mAh", "featured": False, "badge": ""},
    "iPhone XR":         {"series": "iPhone XR", "chip": "A12 Bionic",  "display": '6.1" Liquid Retina LCD',                     "camera": "12MP",                             "battery": "2942mAh", "featured": False, "badge": ""},
    "iPhone 11":         {"series": "iPhone 11", "chip": "A13 Bionic",  "display": '6.1" Liquid Retina LCD',                     "camera": "12MP Dual",                        "battery": "3110mAh", "featured": False, "badge": ""},
    "iPhone 11 Pro":     {"series": "iPhone 11", "chip": "A13 Bionic",  "display": '5.8" Super Retina XDR OLED',                 "camera": "12MP Triple",                      "battery": "3046mAh", "featured": False, "badge": ""},
    "iPhone 11 Pro Max": {"series": "iPhone 11", "chip": "A13 Bionic",  "display": '6.5" Super Retina XDR OLED',                 "camera": "12MP Triple",                      "battery": "3969mAh", "featured": False, "badge": ""},
    "iPhone 12 mini":    {"series": "iPhone 12", "chip": "A14 Bionic",  "display": '5.4" Super Retina XDR OLED',                 "camera": "12MP Dual",                        "battery": "2227mAh", "featured": False, "badge": ""},
    "iPhone 12":         {"series": "iPhone 12", "chip": "A14 Bionic",  "display": '6.1" Super Retina XDR OLED',                 "camera": "12MP Dual",                        "battery": "2815mAh", "featured": False, "badge": ""},
    "iPhone 12 Pro":     {"series": "iPhone 12", "chip": "A14 Bionic",  "display": '6.1" Super Retina XDR OLED',                 "camera": "12MP Triple + LiDAR",              "battery": "2815mAh", "featured": False, "badge": ""},
    "iPhone 12 Pro Max": {"series": "iPhone 12", "chip": "A14 Bionic",  "display": '6.7" Super Retina XDR OLED',                 "camera": "12MP Triple + Sensor-shift OIS",   "battery": "3687mAh", "featured": False, "badge": ""},
    "iPhone 13 mini":    {"series": "iPhone 13", "chip": "A15 Bionic",  "display": '5.4" Super Retina XDR OLED',                 "camera": "12MP Dual",                        "battery": "2438mAh", "featured": False, "badge": ""},
    "iPhone 13":         {"series": "iPhone 13", "chip": "A15 Bionic",  "display": '6.1" Super Retina XDR OLED',                 "camera": "12MP Dual + Sensor-shift OIS",     "battery": "3227mAh", "featured": True,  "badge": "Best Seller"},
    "iPhone 13 Pro":     {"series": "iPhone 13", "chip": "A15 Bionic",  "display": '6.1" ProMotion Super Retina XDR OLED',       "camera": "12MP Triple + LiDAR",              "battery": "3095mAh", "featured": False, "badge": ""},
    "iPhone 13 Pro Max": {"series": "iPhone 13", "chip": "A15 Bionic",  "display": '6.7" ProMotion Super Retina XDR OLED',       "camera": "12MP Triple + LiDAR",              "battery": "4352mAh", "featured": True,  "badge": "Top Rated"},
    "iPhone 14":         {"series": "iPhone 14", "chip": "A15 Bionic",  "display": '6.1" Super Retina XDR OLED',                 "camera": "12MP Dual + Photonic Engine",      "battery": "3279mAh", "featured": False, "badge": ""},
    "iPhone 14 Plus":    {"series": "iPhone 14", "chip": "A15 Bionic",  "display": '6.7" Super Retina XDR OLED',                 "camera": "12MP Dual + Photonic Engine",      "battery": "4323mAh", "featured": False, "badge": ""},
    "iPhone 14 Pro":     {"series": "iPhone 14", "chip": "A16 Bionic",  "display": '6.1" ProMotion Always-On Super Retina XDR',  "camera": "48MP Triple + LiDAR",              "battery": "3200mAh", "featured": True,  "badge": "Best Seller"},
    "iPhone 14 Pro Max": {"series": "iPhone 14", "chip": "A16 Bionic",  "display": '6.7" ProMotion Always-On Super Retina XDR',  "camera": "48MP Triple + LiDAR",              "battery": "4323mAh", "featured": True,  "badge": "Top Rated"},
    "iPhone 15":         {"series": "iPhone 15", "chip": "A16 Bionic",  "display": '6.1" Super Retina XDR Dynamic Island OLED',  "camera": "48MP Dual + Photonic Engine",      "battery": "3349mAh", "featured": False, "badge": ""},
    "iPhone 15 Plus":    {"series": "iPhone 15", "chip": "A16 Bionic",  "display": '6.7" Super Retina XDR Dynamic Island OLED',  "camera": "48MP Dual + Photonic Engine",      "battery": "4383mAh", "featured": False, "badge": ""},
    "iPhone 15 Pro":     {"series": "iPhone 15", "chip": "A17 Pro",     "display": '6.1" ProMotion Super Retina XDR OLED',       "camera": "48MP Triple + 3x Tele",            "battery": "3274mAh", "featured": True,  "badge": ""},
    "iPhone 15 Pro Max": {"series": "iPhone 15", "chip": "A17 Pro",     "display": '6.7" ProMotion Super Retina XDR OLED',       "camera": "48MP Triple + 5x Tele",            "battery": "4422mAh", "featured": True,  "badge": "Best Seller"},
    "iPhone 16":         {"series": "iPhone 16", "chip": "A18",         "display": '6.1" Super Retina XDR Dynamic Island OLED',  "camera": "48MP Dual + Camera Control",       "battery": "3561mAh", "featured": True,  "badge": ""},
    "iPhone 16 Plus":    {"series": "iPhone 16", "chip": "A18",         "display": '6.7" Super Retina XDR Dynamic Island OLED',  "camera": "48MP Dual + Camera Control",       "battery": "4674mAh", "featured": False, "badge": ""},
    "iPhone 16 Pro":     {"series": "iPhone 16", "chip": "A18 Pro",     "display": '6.3" ProMotion Always-On Super Retina XDR',  "camera": "48MP Triple + 5x Tele + Camera Control", "battery": "3582mAh", "featured": True,  "badge": "Best Seller"},
    "iPhone 16 Pro Max": {"series": "iPhone 16", "chip": "A18 Pro",     "display": '6.9" ProMotion Always-On Super Retina XDR',  "camera": "48MP Triple + 5x Tele + Camera Control", "battery": "4685mAh", "featured": True,  "badge": "Top Rated"},
    "iPhone 17":         {"series": "iPhone 17", "chip": "A19",         "display": '6.1" ProMotion Super Retina XDR OLED',       "camera": "48MP Dual + Camera Control",       "battery": "3600mAh", "featured": True,  "badge": "New"},
    "iPhone 17 Air":     {"series": "iPhone 17", "chip": "A19",         "display": '6.6" ProMotion Super Retina XDR OLED',       "camera": "48MP + Camera Control",            "battery": "2800mAh", "featured": True,  "badge": "New"},
    "iPhone 17 Pro":     {"series": "iPhone 17", "chip": "A19 Pro",     "display": '6.3" ProMotion Always-On Super Retina XDR',  "camera": "48MP Triple + Periscope Tele + Camera Control", "battery": "3700mAh", "featured": True,  "badge": "New"},
    "iPhone 17 Pro Max": {"series": "iPhone 17", "chip": "A19 Pro",     "display": '6.9" ProMotion Always-On Super Retina XDR',  "camera": "48MP Triple + Periscope Tele + Camera Control", "battery": "4800mAh", "featured": True,  "badge": "New"},
    "iPhone SE (1st gen)": {"series": "iPhone SE", "chip": "A9",        "display": '4.0" Retina IPS LCD',                        "camera": "12MP",                             "battery": "1624mAh", "featured": False, "badge": ""},
    "iPhone SE (2nd gen)": {"series": "iPhone SE", "chip": "A13 Bionic","display": '4.7" Retina IPS LCD',                        "camera": "12MP",                             "battery": "1821mAh", "featured": False, "badge": ""},
    "iPhone SE (3rd gen)": {"series": "iPhone SE", "chip": "A15 Bionic","display": '4.7" Retina IPS LCD',                        "camera": "12MP",                             "battery": "2018mAh", "featured": False, "badge": ""},
}


# ── Samsung model specs lookup ────────────────────────────────────────────────

SAMSUNG_SPECS = {
    "Galaxy S9+":      {"series": "Galaxy S9",  "chip": "Exynos 9810",        "display": '6.2" Quad HD+ Super AMOLED',    "camera": "12MP Dual OIS",       "battery": "3500mAh", "featured": False, "badge": ""},
    "Galaxy S10+":     {"series": "Galaxy S10", "chip": "Exynos 9820",        "display": '6.4" Quad HD+ Dynamic AMOLED', "camera": "12MP Triple",         "battery": "4100mAh", "featured": False, "badge": ""},
    "Galaxy S22":      {"series": "Galaxy S22", "chip": "Snapdragon 8 Gen 1", "display": '6.1" FHD+ Dynamic AMOLED 2X',  "camera": "50MP Triple",         "battery": "3700mAh", "featured": False, "badge": ""},
    "Galaxy S22 Ultra":{"series": "Galaxy S22", "chip": "Snapdragon 8 Gen 1", "display": '6.8" QHD+ Dynamic AMOLED 2X',  "camera": "108MP Quad + S Pen",  "battery": "5000mAh", "featured": True,  "badge": "Best Seller"},
    "Galaxy S23 Ultra":{"series": "Galaxy S23", "chip": "Snapdragon 8 Gen 2", "display": '6.8" QHD+ Dynamic AMOLED 2X',  "camera": "200MP Quad + S Pen",  "battery": "5000mAh", "featured": True,  "badge": "Top Rated"},
    "Galaxy A35":      {"series": "Galaxy A",   "chip": "Exynos 1380",        "display": '6.6" FHD+ Super AMOLED',       "camera": "50MP Triple",         "battery": "5000mAh", "featured": False, "badge": ""},
    "Galaxy A55":      {"series": "Galaxy A",   "chip": "Exynos 1480",        "display": '6.6" FHD+ Super AMOLED',       "camera": "50MP Triple",         "battery": "5000mAh", "featured": False, "badge": ""},
    "Galaxy S24":      {"series": "Galaxy S24", "chip": "Snapdragon 8 Gen 3", "display": '6.2" FHD+ Dynamic AMOLED 2X',  "camera": "50MP Triple",         "battery": "4000mAh", "featured": True,  "badge": ""},
    "Galaxy S24+":     {"series": "Galaxy S24", "chip": "Snapdragon 8 Gen 3", "display": '6.7" QHD+ Dynamic AMOLED 2X',  "camera": "50MP Triple",         "battery": "4900mAh", "featured": False, "badge": ""},
    "Galaxy S24 Ultra":{"series": "Galaxy S24", "chip": "Snapdragon 8 Gen 3", "display": '6.8" QHD+ Dynamic AMOLED 2X',  "camera": "200MP Quad + S Pen",  "battery": "5000mAh", "featured": True,  "badge": "Best Seller"},
    "Galaxy S25":      {"series": "Galaxy S25", "chip": "Snapdragon 8 Elite", "display": '6.2" FHD+ Dynamic AMOLED 2X',  "camera": "50MP Triple",         "battery": "4000mAh", "featured": True,  "badge": "New"},
    "Galaxy S25+":     {"series": "Galaxy S25", "chip": "Snapdragon 8 Elite", "display": '6.7" QHD+ Dynamic AMOLED 2X',  "camera": "50MP Triple",         "battery": "4900mAh", "featured": False, "badge": "New"},
    "Galaxy S25 Ultra":{"series": "Galaxy S25", "chip": "Snapdragon 8 Elite", "display": '6.9" QHD+ Dynamic AMOLED 2X',  "camera": "200MP Quad + S Pen",  "battery": "5000mAh", "featured": True,  "badge": "New"},
    "Galaxy Z Flip7":  {"series": "Galaxy Z Flip", "chip": "Snapdragon 8 Elite", "display": '6.7" FHD+ Foldable AMOLED', "camera": "50MP Dual",           "battery": "4000mAh", "featured": True,  "badge": "New"},
    "Galaxy Z Fold7":  {"series": "Galaxy Z Fold", "chip": "Snapdragon 8 Elite", "display": '7.9" QHD+ Foldable AMOLED', "camera": "200MP Triple",        "battery": "4400mAh", "featured": True,  "badge": "New"},
}


# ── Description helpers ───────────────────────────────────────────────────────

def _iphone_description(model_name: str, capacity: str, colors: list, specs: dict, status: str) -> str:
    condition = "Brand new, sealed." if status == "Brand New" else "Clean Foreign Used — fully tested."
    color_str = " · ".join(colors[:4]) + (" + more" if len(colors) > 4 else "")
    return (
        f"{model_name} {capacity}. {specs['chip']} chip, {specs['display']} display, "
        f"{specs['camera']} camera. {condition} Colors: {color_str}."
    )


def _samsung_description(model_name: str, capacity: str, colors: list, specs: dict, status: str) -> str:
    condition = "Brand new, sealed." if status == "Brand New" else "Clean Foreign Used — fully tested."
    color_str = " · ".join(colors[:4]) + (" + more" if len(colors) > 4 else "")
    return (
        f"{model_name} {capacity}. {specs['chip']} processor, {specs['display']} display, "
        f"{specs['camera']} camera. {condition} Colors: {color_str}."
    )


# ── Catalog data ──────────────────────────────────────────────────────────────

CATEGORIES = [
    {
        "slug": "phones", "name": "Phones", "icon": "phone", "order": 1,
        "blurb": "iPhone & Samsung — brand new and clean Foreign Used.",
        "brands": [
            {"slug": "iphone",  "name": "iPhone"},
            {"slug": "samsung", "name": "Samsung"},
        ],
    },
    {
        "slug": "laptops", "name": "Laptops", "icon": "laptop", "order": 2,
        "blurb": "HP, Lenovo, Apple & Dell — top models for work, study and play.",
        "brands": [
            {"slug": "hp",     "name": "HP"},
            {"slug": "lenovo", "name": "Lenovo"},
            {"slug": "apple",  "name": "Apple"},
            {"slug": "dell",   "name": "Dell"},
        ],
    },
    {
        "slug": "accessories", "name": "Accessories", "icon": "charger", "order": 3,
        "blurb": "Chargers, power banks, cables, pouches, screen guards, laptop accessories, audio & gadgets.",
        "brands": [
            {"slug": "chargers",        "name": "Chargers"},
            {"slug": "power-banks",     "name": "Power Banks"},
            {"slug": "cables",          "name": "Cables"},
            {"slug": "pouches",         "name": "Pouches & Cases"},
            {"slug": "screen-guards",   "name": "Screen Guards"},
            {"slug": "laptop-batteries","name": "Laptop Batteries"},
            {"slug": "laptop-chargers", "name": "Laptop Adapters"},
            {"slug": "laptop-other",    "name": "Cooling & Sleeves"},
            {"slug": "audio",           "name": "Audio"},
            {"slug": "gadgets",         "name": "Gadgets"},
        ],
    },
]

PRODUCTS = [
    # ── HP Laptops ────────────────────────────────────────────────────────────
    {
        "name": 'HP EliteBook 840 G1', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 180000, "old_price": 200000,
        "status": "Foreign Used",
        "description": "Compact 14-inch business ultrabook. Solid build, fast SSD, ex-UK corporate.",
        "specs": {"CPU": "Intel Core i5 (4th Gen)", "RAM": "8GB", "Storage": "256GB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 820 G3', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 220000,
        "status": "Foreign Used",
        "description": "12-inch ultrabook with i7, ideal for travel and light work. Ex-UK, clean.",
        "specs": {"CPU": "Intel Core i7 (6th Gen)", "RAM": "8GB", "Storage": "256GB SSD", "Display": '12.5" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 820 G4', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 240000, "old_price": 270000,
        "status": "Foreign Used",
        "description": "Slim business ultrabook — i5, 256GB SSD, snappy performance.",
        "specs": {"CPU": "Intel Core i5 (7th Gen)", "RAM": "8GB", "Storage": "256GB SSD", "Display": '12.5" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 840 G3', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 250000, "old_price": 270000,
        "status": "Foreign Used",
        "description": "The reliable 840 G3 — dual-band WiFi, fast SSD, ex-UK corporate.",
        "specs": {"CPU": "Intel Core i5 (6th Gen)", "RAM": "8GB", "Storage": "256GB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 840 G4', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 300000,
        "status": "Foreign Used",
        "description": "Upgraded 840 with 7th gen i5 and 256GB SSD. Business-grade reliability.",
        "specs": {"CPU": "Intel Core i5 (7th Gen)", "RAM": "8GB", "Storage": "256GB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 840 G6', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 400000,
        "status": "Foreign Used", "is_featured": True,
        "description": "Modern thin-frame 840 with 8th-gen i5, 16GB RAM and fast SSD. Ex-UK, excellent condition.",
        "specs": {"CPU": "Intel Core i5 (8th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 830 G7', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 430000,
        "status": "Foreign Used",
        "description": "13-inch premium ultrabook with 16GB RAM and SSD. Lightweight, professional.",
        "specs": {"CPU": "Intel Core i5 (10th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '13.3" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 1040 G6', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 500000,
        "status": "Foreign Used", "is_featured": True,
        "description": "HP's top-tier ultrabook — feather-light carbon chassis, premium display.",
        "specs": {"CPU": "Intel Core i7 (8th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP EliteBook 1040 G8', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 800000,
        "status": "Foreign Used", "is_featured": True,
        "description": "Flagship 1040 G8 — i7 11th gen, 32GB RAM, 1TB SSD. Near-new condition.",
        "specs": {"CPU": "Intel Core i7 (11th Gen)", "RAM": "32GB", "Storage": "1TB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'HP ProBook 450 G5', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 150000,
        "status": "Foreign Used",
        "description": "Affordable 15-inch workhorse with i5 and large storage. Great value.",
        "specs": {"CPU": "Intel Core i5 (8th Gen)", "RAM": "8GB", "Storage": "500GB HDD", "Display": '15.6" FHD'},
        "series": "ProBook",
    },
    {
        "name": 'HP ProBook 11 G4', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 200000,
        "status": "Foreign Used",
        "description": "Compact rugged 11-inch ProBook. Ideal for students and light work.",
        "specs": {"CPU": "Intel Celeron", "RAM": "8GB", "Storage": "128GB SSD", "Display": '11.6" HD'},
        "series": "ProBook",
    },
    {
        "name": 'HP ProBook 11 G5', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 190000,
        "status": "Foreign Used",
        "description": "Updated G5 edition of the rugged compact ProBook 11.",
        "specs": {"CPU": "Intel Celeron", "RAM": "8GB", "Storage": "128GB SSD", "Display": '11.6" HD'},
        "series": "ProBook",
    },

    # ── Dell Laptops ──────────────────────────────────────────────────────────
    {
        "name": 'Dell Vostro 15', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 150000,
        "status": "Foreign Used",
        "description": "Entry-level 15-inch Dell. Solid daily driver for light tasks.",
        "specs": {"CPU": "Intel Core i3", "RAM": "4GB", "Storage": "128GB SSD", "Display": '15.6" HD'},
        "series": "Vostro",
    },
    {
        "name": 'Dell Latitude 3190', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 170000,
        "status": "Foreign Used",
        "description": "Compact 11-inch education-grade Latitude. Rugged, reliable, ex-UK.",
        "specs": {"CPU": "Intel Celeron N", "RAM": "8GB", "Storage": "128GB SSD", "Display": '11.6" HD'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 5300', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 370000, "old_price": 400000,
        "status": "Foreign Used",
        "description": "13-inch business Latitude with i7, 16GB RAM. Thin, light, professional.",
        "specs": {"CPU": "Intel Core i7 (8th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '13.3" FHD'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 5410', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 280000, "old_price": 310000,
        "status": "Foreign Used", "is_featured": True,
        "description": "14-inch corporate Latitude — i5 10th gen, backlit keyboard, fingerprint reader.",
        "specs": {"CPU": "Intel Core i5 (10th Gen)", "RAM": "8GB", "Storage": "256GB SSD", "Display": '14" FHD'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 5510', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 350000,
        "status": "Foreign Used",
        "description": "15-inch touchscreen Latitude with i5, 16GB RAM and backlit keyboard.",
        "specs": {"CPU": "Intel Core i5 (10th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '15.6" FHD Touch'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 5520', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 380000,
        "status": "Foreign Used",
        "description": "15-inch 11th-gen i5 with touchscreen, fingerprint and facial recognition.",
        "specs": {"CPU": "Intel Core i5 (11th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '15.6" FHD Touch'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 5530', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 450000,
        "status": "Foreign Used", "is_featured": True,
        "description": "15-inch modern Latitude with 512GB SSD and backlit keyboard. Nearly new.",
        "specs": {"CPU": "Intel Core i5 (12th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '15.6" FHD'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 5540', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 480000,
        "status": "Foreign Used",
        "description": "13th-gen 15-inch Latitude — backlit keyboard, fingerprint, facial recognition.",
        "specs": {"CPU": "Intel Core i5 (13th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '15.6" FHD'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Latitude 7390', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 430000,
        "status": "Foreign Used",
        "description": "Premium 13-inch ultrabook from Dell's top Latitude line. Ultra-thin, business-grade.",
        "specs": {"CPU": "Intel Core i7 (8th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '13.3" FHD'},
        "series": "Latitude",
    },
    {
        "name": 'Dell Precision 3561', "cat": "laptops", "brand": "dell",
        "thumb": "laptop", "tint": "indigo", "price": 380000,
        "status": "Foreign Used",
        "description": "Entry workstation with i7 11th gen and dedicated graphics. For creators and engineers.",
        "specs": {"CPU": "Intel Core i7 (11th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '15.6" FHD'},
        "series": "Precision",
    },

    # ── Lenovo Laptops ────────────────────────────────────────────────────────
    {
        "name": 'Lenovo Yoga x13', "cat": "laptops", "brand": "lenovo",
        "thumb": "laptop", "tint": "indigo", "price": 470000, "old_price": 500000,
        "status": "Foreign Used",
        "description": "2-in-1 convertible with 10th-gen i7, 16GB RAM and 512GB SSD. Touchscreen, stylus-ready.",
        "specs": {"CPU": "Intel Core i7 (10th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '13.3" FHD Touch'},
        "series": "Yoga",
    },
    {
        "name": 'Lenovo ThinkPad Yoga x390', "cat": "laptops", "brand": "lenovo",
        "thumb": "laptop", "tint": "indigo", "price": 370000,
        "status": "Foreign Used",
        "description": "ThinkPad-grade build in a touchscreen convertible. 8th-gen i5, 16GB RAM.",
        "specs": {"CPU": "Intel Core i5 (8th Gen)", "RAM": "16GB", "Storage": "256GB SSD", "Display": '13.3" FHD Touch'},
        "series": "ThinkPad",
    },
    {
        "name": 'Lenovo ThinkPad Yoga x1', "cat": "laptops", "brand": "lenovo",
        "thumb": "laptop", "tint": "indigo", "price": 350000,
        "status": "Foreign Used",
        "description": "Premium ThinkPad convertible with OLED touch display option and solid i5 performance.",
        "specs": {"CPU": "Intel Core i5 (8th Gen)", "RAM": "8GB", "Storage": "512GB SSD", "Display": '13.3" FHD Touch'},
        "series": "ThinkPad",
    },

    # ── Apple Laptops ─────────────────────────────────────────────────────────
    {
        "name": 'Apple MacBook Pro 2020', "cat": "laptops", "brand": "apple",
        "thumb": "laptop", "tint": "indigo", "price": 670000,
        "status": "Foreign Used", "is_featured": True,
        "description": "Intel MacBook Pro 2020 — 16GB RAM, 512GB SSD. Silent Magic Keyboard, Touch Bar.",
        "specs": {"CPU": "Intel Core i5 (10th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '13.3" Retina'},
        "series": "MacBook Pro",
    },
    {
        "name": 'Apple MacBook Pro 2018', "cat": "laptops", "brand": "apple",
        "thumb": "laptop", "tint": "indigo", "price": 500000,
        "status": "Foreign Used",
        "description": "15-inch MacBook Pro 2018 — i7, 16GB RAM, 512GB SSD. Great for creative work.",
        "specs": {"CPU": "Intel Core i7 (8th Gen)", "RAM": "16GB", "Storage": "512GB SSD", "Display": '15.6" Retina'},
        "series": "MacBook Pro",
    },

    # ── Phone Chargers ────────────────────────────────────────────────────────
    {
        "name": 'Apple 20W USB-C Charger (2-Pin)', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 15000,
        "description": "Compact Apple-grade 20W USB-C adapter. Fast-charges iPhone 8 and above. 2-pin plug.",
        "specs": {"Output": "20W PD", "Port": "USB-C", "Plug": "2-Pin"},
    },
    {
        "name": 'Apple 20W Charger + Lightning Cable', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 22000,
        "description": "Complete fast-charge set — 20W adapter and USB-C to Lightning cable in the box.",
        "specs": {"Output": "20W PD", "Includes": "Adapter + Cable", "Cable": "USB-C to Lightning"},
    },
    {
        "name": 'Apple 20W USB-C Charger (3-Pin)', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 17000,
        "description": "Same 20W fast-charge power but with a 3-pin UK-style plug.",
        "specs": {"Output": "20W PD", "Port": "USB-C", "Plug": "3-Pin"},
    },
    {
        "name": 'Apple 40W Dual USB-C Charger', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 28000, "is_featured": True,
        "description": "Charge two Apple devices simultaneously. 40W total, two USB-C ports.",
        "specs": {"Output": "40W Total", "Ports": "2x USB-C", "Compat": "iPhone / iPad / Mac"},
    },
    {
        "name": 'Samsung 45W Super Fast Charger', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 19000,
        "description": "Official Samsung Super Fast Charging 2.0. Designed for S22 Ultra, S23 Ultra, S24 series.",
        "specs": {"Output": "45W", "Port": "USB-C", "Tech": "Super Fast Charging 2.0"},
    },
    {
        "name": 'Samsung 65W Travel Adapter', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 26000, "is_featured": True,
        "description": "High-power Samsung adapter for phones and tablets. Compact travel design.",
        "specs": {"Output": "65W", "Port": "USB-C", "Tech": "Super Fast Charging"},
    },
    {
        "name": 'Oraimo iPhone Fast Charger', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 9500,
        "description": "Reliable Oraimo 20W charger for iPhones. MFi-grade performance at a smart price.",
        "specs": {"Output": "20W PD", "Port": "USB-C", "Brand": "Oraimo"},
    },
    {
        "name": 'Oraimo Android Fast Charger', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 8500,
        "description": "Quick Charge compatible Oraimo adapter for Samsung and Android phones.",
        "specs": {"Output": "18W QC", "Port": "USB-A", "Brand": "Oraimo"},
    },
    {
        "name": 'Dual USB Car Charger', "cat": "accessories", "brand": "chargers",
        "thumb": "charger", "tint": "orange", "price": 7000,
        "description": "Charge two phones at once from your car's 12V socket. Compact, heat-resistant.",
        "specs": {"Output": "24W Total", "Ports": "USB-A + USB-C", "Mount": "12V Socket"},
    },

    # ── Laptop Chargers ───────────────────────────────────────────────────────
    {
        "name": 'HP 65W USB-C Adapter (Corner)', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "blue", "price": 18000,
        "description": "Replacement adapter for HP EliteBook 830/840/1040 G-series with USB-C corner connector.",
        "specs": {"Output": "20V / 3.25A — 65W", "Connector": "USB-C Corner", "Fit": "HP EliteBook G6/G7"},
    },
    {
        "name": 'HP 65W USB-C Adapter (Straight)', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "blue", "price": 18500,
        "description": "Straight USB-C variant for HP EliteBook models that take a direct plug.",
        "specs": {"Output": "20V / 3.25A — 65W", "Connector": "USB-C Straight", "Fit": "HP EliteBook G6/G7"},
    },
    {
        "name": 'HP 65W USB-C Adapter (Oval)', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "blue", "price": 24000,
        "description": "Oval USB-C connector variant — fits specific HP EliteBook models.",
        "specs": {"Output": "20V / 3.25A — 65W", "Connector": "USB-C Oval", "Fit": "HP EliteBook"},
    },
    {
        "name": 'HP 65W Small Pin Adapter', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "blue", "price": 18000,
        "description": "Barrel-pin charger for older HP ProBook, EliteBook and Pavilion models.",
        "specs": {"Output": "19.5V / 4.62A — 65W", "Connector": "Small Barrel Pin", "Fit": "HP ProBook / Pavilion"},
    },
    {
        "name": 'Dell 65W USB-C Adapter', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "indigo", "price": 19000,
        "description": "USB-C power delivery adapter for modern Dell Latitude and XPS models.",
        "specs": {"Output": "20V / 3.25A — 65W", "Connector": "USB-C", "Fit": "Dell Latitude 5x / XPS"},
    },
    {
        "name": 'Dell 65W Small Pin Adapter', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "indigo", "price": 20000,
        "description": "Slim barrel-pin charger for Dell Inspiron and older Latitude models.",
        "specs": {"Output": "19.5V / 3.34A — 65W", "Connector": "Small Barrel Pin", "Fit": "Dell Inspiron / Latitude"},
    },
    {
        "name": 'Dell 90W Big Pin Adapter', "cat": "accessories", "brand": "laptop-chargers",
        "thumb": "charger", "tint": "indigo", "price": 23000,
        "description": "Higher-wattage oval-tip charger for Dell Vostro and larger Latitude models.",
        "specs": {"Output": "19.5V / 4.62A — 90W", "Connector": "Big Barrel Oval", "Fit": "Dell Vostro / Latitude"},
    },

    # ── Laptop Batteries ──────────────────────────────────────────────────────
    {
        "name": 'HP Battery CM03XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 28500, "is_featured": True,
        "description": "Replacement battery for HP EliteBook 840 G1 and G2. Restore all-day battery life.",
        "specs": {"Part": "CM03XL", "Fit": "HP EliteBook 840 G1 / G2", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery SB03XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 30000,
        "description": "Battery for HP EliteBook 820 G1 and G2. Brings your old 820 back to life.",
        "specs": {"Part": "SB03XL", "Fit": "HP EliteBook 820 G1 / G2", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery SN03XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 30000,
        "description": "Battery for HP EliteBook 820 G3 and G4. Fresh cells, long run time.",
        "specs": {"Part": "SN03XL", "Fit": "HP EliteBook 820 G3 / G4", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery CS03XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 30000,
        "description": "Drop-in replacement for HP EliteBook 840 G3 and G4.",
        "specs": {"Part": "CS03XL", "Fit": "HP EliteBook 840 G3 / G4", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery BG06XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 38000,
        "description": "Large-capacity battery for HP EliteBook 1040 G3. Premium long-life cells.",
        "specs": {"Part": "BG06XL", "Fit": "HP EliteBook 1040 G3", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery BM04XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 35000,
        "description": "Replacement battery for HP EliteBook 1030 G3.",
        "specs": {"Part": "BM04XL", "Fit": "HP EliteBook 1030 G3", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery OM03XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 36000,
        "description": "Battery for HP EliteBook 1030 G2. Slim form factor, high energy density.",
        "specs": {"Part": "OM03XL", "Fit": "HP EliteBook 1030 G2", "Type": "Li-ion"},
    },
    {
        "name": 'HP Battery BT04XL', "cat": "accessories", "brand": "laptop-batteries",
        "thumb": "battery", "tint": "blue", "price": 33000,
        "description": "Battery for HP EliteBook Folio 9470m. Easy swap, direct fit.",
        "specs": {"Part": "BT04XL", "Fit": "HP EliteBook Folio 9470m", "Type": "Li-ion"},
    },

    # ── Cables ────────────────────────────────────────────────────────────────
    {
        "name": 'Oraimo USB-A to Lightning Cable', "cat": "accessories", "brand": "cables",
        "thumb": "cable", "tint": "orange", "price": 7500,
        "description": "Reliable Oraimo charging cable for iPhone and AirPods. Nylon-braided, tangle-free.",
        "specs": {"Length": "1m", "Connector": "USB-A to Lightning", "Jacket": "Nylon Braided"},
    },
    {
        "name": 'USB-C to Lightning Cable', "cat": "accessories", "brand": "cables",
        "thumb": "cable", "tint": "orange", "price": 9500,
        "description": "Fast-charge cable for iPhone 8 and above. Pairs with 20W USB-C adapter.",
        "specs": {"Length": "1m", "Connector": "USB-C to Lightning", "Speed": "Fast Charge"},
    },
    {
        "name": 'Oraimo USB-C to USB-C Cable', "cat": "accessories", "brand": "cables",
        "thumb": "cable", "tint": "orange", "price": 7000,
        "description": "60W USB-C cable for Samsung, laptops and modern Androids. Braided for durability.",
        "specs": {"Length": "1m", "Connector": "USB-C to USB-C", "Speed": "60W PD"},
    },
    {
        "name": 'USB-A to Micro USB Cable', "cat": "accessories", "brand": "cables",
        "thumb": "cable", "tint": "orange", "price": 4500,
        "description": "Standard Micro USB cable for older Android phones and accessories.",
        "specs": {"Length": "1m", "Connector": "USB-A to Micro USB", "Speed": "Standard Charge"},
    },

    # ── Power Banks ───────────────────────────────────────────────────────────
    {
        "name": '20,000mAh Power Bank', "cat": "accessories", "brand": "power-banks",
        "thumb": "powerbank", "tint": "orange", "price": 22000, "is_featured": True,
        "description": "Multi-day power for trips and long days. Fast-charge in and out via USB-C.",
        "specs": {"Capacity": "20,000mAh", "Output": "22.5W", "Ports": "USB-C + 2x USB-A"},
    },
    {
        "name": '27,000mAh Power Bank', "cat": "accessories", "brand": "power-banks",
        "thumb": "powerbank", "tint": "orange", "price": 23000, "is_featured": True,
        "description": "High-capacity travel companion — charges your phone 6+ times. USB-C PD 65W output.",
        "specs": {"Capacity": "27,000mAh", "Output": "65W PD", "Ports": "USB-C + 2x USB-A"},
    },

    # ── Pouches & Cases ───────────────────────────────────────────────────────
    {
        "name": 'Phone Pouch — iPhone 6 / 8 / SE', "cat": "accessories", "brand": "pouches",
        "thumb": "case", "tint": "orange", "price": 3000,
        "description": "Slim PU leather sleeve for iPhone 6, 7, 8 and SE (2nd/3rd gen). Drop-safe, scratch-free.",
        "specs": {"Fit": "iPhone 6 · 7 · 8 · SE (2nd/3rd gen)", "Material": "PU Leather", "Closure": "Magnetic flap"},
    },
    {
        "name": 'Phone Pouch — iPhone X / 11', "cat": "accessories", "brand": "pouches",
        "thumb": "case", "tint": "orange", "price": 3500,
        "description": "Tailored sleeve for iPhone X, XS, XR, 11, 11 Pro and 11 Pro Max models.",
        "specs": {"Fit": "iPhone X · XS · XR · 11 series", "Material": "PU Leather", "Closure": "Magnetic flap"},
    },
    {
        "name": 'Phone Pouch — iPhone 12 / 13 / 14', "cat": "accessories", "brand": "pouches",
        "thumb": "case", "tint": "orange", "price": 4000,
        "description": "Protective sleeve that fits all 12, 13 and 14 series iPhones (standard + Plus/Max).",
        "specs": {"Fit": "iPhone 12 · 13 · 14 (all variants)", "Material": "PU Leather", "Closure": "Magnetic flap"},
    },
    {
        "name": 'Phone Pouch — iPhone 15 / 16 / 17', "cat": "accessories", "brand": "pouches",
        "thumb": "case", "tint": "orange", "price": 4500,
        "description": "Modern-cut sleeve for the latest iPhone generations. Titanium-edge safe.",
        "specs": {"Fit": "iPhone 15 · 16 · 17 (all variants)", "Material": "PU Leather", "Closure": "Magnetic flap"},
    },
    {
        "name": 'Phone Pouch — Samsung S9 / S10', "cat": "accessories", "brand": "pouches",
        "thumb": "case", "tint": "orange", "price": 4000,
        "description": "Slim protective sleeve for Galaxy S9+ and S10+ models.",
        "specs": {"Fit": "Galaxy S9+ · S10+", "Material": "PU Leather", "Closure": "Magnetic flap"},
    },
    {
        "name": 'Phone Pouch — Samsung S20–S25', "cat": "accessories", "brand": "pouches",
        "thumb": "case", "tint": "orange", "price": 4500,
        "description": "Well-fitted sleeve for Galaxy S20 through S25 series (standard, + and Ultra).",
        "specs": {"Fit": "Galaxy S20 · S21 · S22 · S23 · S24 · S25 series", "Material": "PU Leather", "Closure": "Magnetic flap"},
    },

    # ── Screen Guards ─────────────────────────────────────────────────────────
    {
        "name": 'Screen Guard — iPhone X / 11', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 1500,
        "description": "9H tempered glass for iPhone X, XS, XR, 11, 11 Pro and 11 Pro Max.",
        "specs": {"Hardness": "9H", "Fit": "iPhone X · XS · XR · 11 series", "Pack": "2-pack + alignment kit"},
    },
    {
        "name": 'Screen Guard — iPhone 12 / 13', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 1700,
        "description": "Precision-cut 9H glass for iPhone 12 and 13 series (mini, standard, Pro, Max).",
        "specs": {"Hardness": "9H", "Fit": "iPhone 12 · 13 (all variants)", "Pack": "2-pack + alignment kit"},
    },
    {
        "name": 'Screen Guard — iPhone 14', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 2000,
        "description": "9H tempered glass precisely cut for iPhone 14 and 14 Plus.",
        "specs": {"Hardness": "9H", "Fit": "iPhone 14 · 14 Plus", "Pack": "2-pack + alignment kit"},
    },
    {
        "name": 'Screen Guard — iPhone 15', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 2000,
        "description": "9H glass for iPhone 15 and 15 Plus. Curved-edge safe cutouts.",
        "specs": {"Hardness": "9H", "Fit": "iPhone 15 · 15 Plus", "Pack": "2-pack + alignment kit"},
    },
    {
        "name": 'Screen Guard — iPhone 16 / 17', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 2500,
        "description": "Latest-gen 9H glass for iPhone 16, 17 and their Plus/Pro/Max variants.",
        "specs": {"Hardness": "9H", "Fit": "iPhone 16 · 17 (all variants)", "Pack": "2-pack + alignment kit"},
    },
    {
        "name": 'Privacy Screen Guard — Samsung Ultra', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 4500,
        "description": "Anti-spy 9H glass for Galaxy S22 Ultra, S23 Ultra, S24 Ultra and S25 Ultra.",
        "specs": {"Hardness": "9H", "Feature": "28° Privacy Filter", "Fit": "Galaxy Ultra series"},
    },
    {
        "name": 'Screen Guard — Samsung S20–S25', "cat": "accessories", "brand": "screen-guards",
        "thumb": "shield", "tint": "orange", "price": 4000,
        "description": "Crystal-clear 9H tempered glass for Galaxy S20 through S25 (standard/+).",
        "specs": {"Hardness": "9H", "Fit": "Galaxy S20 · S21 · S22 · S23 · S24 · S25", "Pack": "2-pack"},
    },

    # ── Laptop Other ──────────────────────────────────────────────────────────
    {
        "name": 'Adjustable Laptop Stand', "cat": "accessories", "brand": "laptop-other",
        "thumb": "laptop", "tint": "blue", "price": 10000,
        "description": "Ergonomic aluminium stand — 6 height settings, keeps your laptop cool.",
        "specs": {"Material": "Aluminium", "Fit": "10–17 inch", "Levels": "6 adjustable heights"},
    },
    {
        "name": 'Laptop Handbag 14"', "cat": "accessories", "brand": "laptop-other",
        "thumb": "case", "tint": "blue", "price": 13000,
        "description": "Stylish tote with padded compartment for 14-inch laptops. Multiple pockets.",
        "specs": {"Fit": '14"', "Material": "Canvas + PU trim", "Pockets": "3 exterior"},
    },
    {
        "name": 'Laptop Backpack 15.6"', "cat": "accessories", "brand": "laptop-other",
        "thumb": "case", "tint": "blue", "price": 15000, "is_featured": True,
        "description": "Padded, water-resistant backpack with USB charging port and 15.6-inch laptop sleeve.",
        "specs": {"Fit": '15.6"', "Material": "Water-resistant nylon", "Extra": "USB charging port"},
    },
    {
        "name": 'Wireless Mouse', "cat": "accessories", "brand": "laptop-other",
        "thumb": "laptop", "tint": "blue", "price": 3500,
        "description": "Silent 2.4GHz wireless mouse. DPI adjustable, ergonomic grip, nano USB receiver.",
        "specs": {"Connection": "2.4GHz Wireless", "DPI": "800 / 1200 / 1600", "Battery": "AA (included)"},
    },

    # ── Audio ─────────────────────────────────────────────────────────────────
    {
        "name": 'Apple AirPods (3rd Gen)', "cat": "accessories", "brand": "audio",
        "thumb": "cable", "tint": "blue", "price": 145000, "is_featured": True,
        "description": "Spatial audio, Adaptive EQ and 30h total battery with the case. Brand new, sealed.",
        "specs": {"Audio": "Spatial Audio + Adaptive EQ", "Battery": "6h + 24h case", "Resistance": "IPX4"},
    },
    {
        "name": 'Apple AirPods Pro (2nd Gen)', "cat": "accessories", "brand": "audio",
        "thumb": "cable", "tint": "blue", "price": 250000, "is_featured": True, "badge": "Best Seller",
        "description": "Active Noise Cancellation, Transparency mode and H2 chip. Brand new, sealed.",
        "specs": {"Audio": "ANC + Transparency + Spatial Audio", "Battery": "6h + 24h case", "Resistance": "IP54"},
    },
    {
        "name": 'Apple AirPods Max', "cat": "accessories", "brand": "audio",
        "thumb": "cable", "tint": "blue", "price": 480000,
        "description": "Premium over-ear headphones with Active Noise Cancellation and Spatial Audio.",
        "specs": {"Audio": "ANC + Spatial Audio", "Battery": "20h ANC on", "Driver": "40mm custom"},
    },

    # ── Gadgets ───────────────────────────────────────────────────────────────
    {
        "name": 'Airtel Universal Pocket WiFi', "cat": "accessories", "brand": "gadgets",
        "thumb": "powerbank", "tint": "orange", "price": 25000,
        "description": "Multi SIM support. Create a personal 4G hotspot anywhere. Supports up to 10 devices simultaneously.",
        "specs": {"Network": "4G LTE", "Devices": "Up to 10", "Battery": "1500mAh"},
    },
    {
        "name": 'Starlink Gen 3 Kit', "cat": "accessories", "brand": "gadgets",
        "thumb": "powerbank", "tint": "indigo", "price": 600000, "is_featured": True, "badge": "New",
        "description": "Super fast satellite internet. Blazing speeds anywhere in Nigeria — dish, router and cables included.",
        "specs": {"Speed": "100–200 Mbps", "Latency": "20–40ms", "Includes": "Dish + Router + Cables"},
    },
    {
        "name": 'Sony PS5 Slim', "cat": "accessories", "brand": "gadgets",
        "thumb": "powerbank", "tint": "indigo", "price": 850000, "is_featured": True, "badge": "Best Seller",
        "description": "The compact PS5 Slim disc edition. Brand new, sealed. Nigeria warranty.",
        "specs": {"Storage": "1TB SSD", "Resolution": "4K 120fps", "Form": "Slim disc edition"},
    },

    # ── One-time offers ───────────────────────────────────────────────────────
    {
        "name": 'iPhone 14 Pro Max 128GB', "cat": "phones", "brand": "iphone",
        "thumb": "phone", "tint": "blue", "price": 780000, "old_price": 980000,
        "status": "Nigeria-Used", "is_one_time": True, "stock": 1,
        "one_time_note": "Tiny hairline scratch on back glass. Screen flawless. Battery 86%.",
        "description": "One unit only. A clean Nigeria-used Pro Max at a price that won't repeat.",
        "specs": {"Storage": "256GB", "Display": '6.7" ProMotion', "Chip": "A16 Bionic", "Camera": "48MP Triple"},
        "series": "iPhone 14",
    },
    {
        "name": 'iPhone 13 Pro Max 128GB', "cat": "phones", "brand": "iphone",
        "thumb": "phone", "tint": "blue", "price": 430000, "old_price": 620000,
        "status": "Nigeria-Used", "is_one_time": True, "stock": 1,
        "one_time_note": "Aftermarket screen (excellent quality). Body clean. Battery 88%.",
        "description": "One unit only. Big-battery Pro Max with a quality replacement screen.",
        "specs": {"Storage": "128GB", "Display": '6.7" ProMotion', "Chip": "A15 Bionic", "Camera": "12MP Triple"},
        "series": "iPhone 13",
    },
    {
        "name": 'Galaxy S23 Ultra', "cat": "phones", "brand": "samsung",
        "thumb": "phone", "tint": "indigo", "price": 820000, "old_price": 1000000,
        "status": "Foreign Used", "is_one_time": True, "stock": 1,
        "one_time_note": "Faint single pixel dot, invisible in normal use. S Pen included.",
        "description": "One unit only. Foreign Used Ultra with a barely-there blemish and a big discount.",
        "specs": {"Storage": "256GB", "Display": '6.8" QHD+ AMOLED', "Chip": "Snapdragon 8 Gen 2", "Camera": "200MP Quad"},
        "series": "Galaxy S23",
    },
    {
        "name": 'MacBook Air 2020', "cat": "laptops", "brand": "apple",
        "thumb": "laptop", "tint": "indigo", "price": 430000,
        "status": "Nigeria-Used", "is_one_time": True, "stock": 1,
        "one_time_note": "Neatly used with a low cycle count. Runs perfectly.",
        "description": "One unit only. A silent, fast M1 Air with a cosmetic dent — pure value.",
        "specs": {"CPU": "core i5", "RAM": "8GB", "Storage": "256GB SSD", "Display": '13.3" Retina'},
        "series": "MacBook Air",
    },
    {
        "name": 'HP EliteBook 840 (ex-UK)', "cat": "laptops", "brand": "hp",
        "thumb": "laptop", "tint": "blue", "price": 360000, "old_price": 520000,
        "status": "Foreign Used", "is_one_time": True, "stock": 1,
        "one_time_note": "Visible dent on palm rest. Fully functional, keyboard perfect.",
        "description": "One unit only. Workhorse EliteBook with a battle scar and a steep markdown.",
        "specs": {"CPU": "Intel Core i7-10610U", "RAM": "16GB", "Storage": "512GB SSD", "Display": '14" FHD'},
        "series": "EliteBook",
    },
    {
        "name": 'Galaxy Z Fold4', "cat": "phones", "brand": "samsung",
        "thumb": "phone", "tint": "indigo", "price": 720000, "old_price": 950000,
        "status": "Foreign Used", "is_one_time": True, "stock": 1,
        "one_time_note": "Light crease wear (normal for folds). Hinge tight, no dead pixels.",
        "description": "One unit only. A foldable tablet-phone at an unrepeatable price.",
        "specs": {"Storage": "256GB", "Display": '7.6" Foldable AMOLED', "Chip": "Snapdragon 8+ Gen 1", "Cover": '6.2" AMOLED'},
        "series": "Galaxy Z Fold",
    },
]


# ── CSV loaders ───────────────────────────────────────────────────────────────

KWISEAPI_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def load_iphone_products() -> list[dict]:
    products = []
    csv_path = os.path.join(KWISEAPI_DIR, "data", "iphone_catalog_2.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            model    = row["model_name"]
            capacity = row["capacity"]
            price    = int(row["price"])
            status   = row["status"]
            colors   = [c.strip() for c in row["colors"].split("|")]
            sp       = IPHONE_SPECS.get(model, {})
            full_name = f"{model} {capacity}"
            slug      = slugify(full_name)
            products.append({
                "name":         full_name,
                "series":       sp.get("series", model),
                "cat":          "phones",
                "brand":        "iphone",
                "thumb":        "phone",
                "tint":         "blue",
                "status":       status,
                "price":        price,
                "colors":       colors,
                "description":  _iphone_description(model, capacity, colors, sp, status),
                "is_featured":  sp.get("featured", False),
                "badge":        sp.get("badge", ""),
                "specs": {
                    "Storage": capacity,
                    "Chip":    sp.get("chip", ""),
                    "Display": sp.get("display", ""),
                    "Camera":  sp.get("camera", ""),
                    "Battery": sp.get("battery", ""),
                },
            })
    return products


def load_samsung_products() -> list[dict]:
    products = []
    csv_path = os.path.join(KWISEAPI_DIR, "data", "samsung_catalog.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            model    = row["model_name"]
            capacity = row["capacity"]
            price    = int(row["price"])
            status   = row["status"]
            colors   = [c.strip() for c in row["colors"].split("|")]
            sp       = SAMSUNG_SPECS.get(model, {})
            full_name = f"{model} {capacity}"
            slug      = slugify(full_name)
            products.append({
                "name":         full_name,
                "series":       sp.get("series", model),
                "cat":          "phones",
                "brand":        "samsung",
                "thumb":        "phone",
                "tint":         "indigo",
                "status":       status,
                "price":        price,
                "colors":       colors,
                "description":  _samsung_description(model, capacity, colors, sp, status),
                "is_featured":  sp.get("featured", False),
                "badge":        sp.get("badge", ""),
                "specs": {
                    "Storage": capacity,
                    "Chip":    sp.get("chip", ""),
                    "Display": sp.get("display", ""),
                    "Camera":  sp.get("camera", ""),
                    "Battery": sp.get("battery", ""),
                },
            })
    return products


# ── Management command ────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Seed the database with the initial Kwise World catalog."

    def handle(self, *args, **options):
        cat_map   = {}
        brand_map = {}

        for c_data in CATEGORIES:
            brands_data = c_data.pop("brands")
            cat, _ = Category.objects.update_or_create(
                slug=c_data["slug"],
                defaults={k: v for k, v in c_data.items() if k != "slug"},
            )
            cat_map[cat.slug] = cat
            c_data["brands"] = brands_data  # restore for idempotency

            for b_data in brands_data:
                brand, _ = Brand.objects.update_or_create(
                    category=cat, slug=b_data["slug"],
                    defaults={"name": b_data["name"]},
                )
                brand_map[(cat.slug, brand.slug)] = brand

        self.stdout.write(f"  {Category.objects.count()} categories, {Brand.objects.count()} brands")

        iphone_products  = load_iphone_products()
        samsung_products = load_samsung_products()
        all_products     = iphone_products + samsung_products + PRODUCTS

        for p_data in all_products:
            specs      = p_data.pop("specs", {})
            cat_slug   = p_data.pop("cat")
            brand_slug = p_data.pop("brand")
            cat        = cat_map[cat_slug]
            brand      = brand_map[(cat_slug, brand_slug)]

            product, _ = Product.objects.update_or_create(
                slug=slugify(p_data["name"]),
                defaults={
                    "name":          p_data["name"],
                    "category":      cat,
                    "brand":         brand,
                    "thumb":         p_data.get("thumb", "phone"),
                    "tint":          p_data.get("tint", "blue"),
                    "price":         p_data["price"],
                    "old_price":     p_data.get("old_price"),
                    "status":        p_data.get("status", "Brand New"),
                    "is_featured":   p_data.get("is_featured", False),
                    "badge":         p_data.get("badge", ""),
                    "is_one_time":   p_data.get("is_one_time", False),
                    "stock":         p_data.get("stock", 25),
                    "description":   p_data.get("description", ""),
                    "one_time_note": p_data.get("one_time_note", ""),
                    "colors":        p_data.get("colors", []),
                    "series":        p_data.get("series", ""),
                },
            )

            ProductSpec.objects.filter(product=product).delete()
            for order, (key, value) in enumerate(specs.items()):
                ProductSpec.objects.create(product=product, key=key, value=value, order=order)

        self.stdout.write(
            f"  {Product.objects.count()} products "
            f"({len(iphone_products)} iPhone + {len(samsung_products)} Samsung from CSV, "
            f"{len(PRODUCTS)} inline)"
        )
        self.stdout.write(self.style.SUCCESS("Seed complete."))
