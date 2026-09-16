from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/hot-drinks/tea"
CATEGORY = "Tea"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-tea.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
