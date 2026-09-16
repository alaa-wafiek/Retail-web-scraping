from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/dairy-eggs-cheese/milk-cream"
CATEGORY = "Milk"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-milk.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
