from scraper_engine import run_category

BASE_URL = "https://seoudisupermarket.com/en/ricepasta-pulses/pasta"
CATEGORY = "Pasta"
SUBCATEGORY = "N/A"
OUTPUT_FILE = "seoudi-pasta.csv"

run_category(BASE_URL, CATEGORY, SUBCATEGORY, OUTPUT_FILE)
