from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/cooking-ingredients/oil"
CATEGORY = "Oil"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-oil.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
