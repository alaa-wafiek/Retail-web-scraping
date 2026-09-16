from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/cheese-labneh"
CATEGORY = "Cheese & Labneh"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-cheese-labneh.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
