from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/ricepasta-pulses/rice"
CATEGORY = "Rice"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-rice.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
