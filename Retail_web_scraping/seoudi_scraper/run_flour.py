from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/sugar-home-baking/flour"
CATEGORY = "Flour"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-flour.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
