from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/cans-packets/canned-fish"
CATEGORY = "Canned Food"
SUBCATEGORY = "Canned Fish"
OUTPUT_FILE = "seoudi-canned-fish.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
