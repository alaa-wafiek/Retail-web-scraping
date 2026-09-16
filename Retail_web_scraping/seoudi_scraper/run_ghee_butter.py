from scraper_engine import run_multi_category

CATEGORY = "Ghee & Butter"
OUTPUT_FILE = "seoudi-ghee-butter.csv"

PAGES = [
    {"url": "https://seoudisupermarket.com/en/butter-margarine/butter-ghee", "category": CATEGORY, "subcategory": "Ghee"},
    {"url": "https://seoudisupermarket.com/en/butter-margarine/vegetable-ghee", "category": CATEGORY, "subcategory": "Vegetable Ghee"},
    {"url": "https://seoudisupermarket.com/en/butter-margarine/yellow-butter", "category": CATEGORY, "subcategory": "Yellow Butter"}]

run_multi_category(PAGES, OUTPUT_FILE)
