from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/sugar-home-baking/sugar"
CATEGORY = "Sugar"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-sugar.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
