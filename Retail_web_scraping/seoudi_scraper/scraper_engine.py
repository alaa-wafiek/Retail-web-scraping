import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_DOMAIN = "https://seoudisupermarket.com"
STORE = "Seoudi Supermarket"

def build_driver(headless=False):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless=new")
    return webdriver.Chrome(options=chrome_options)

def ensure_store_selected(driver):
    driver.get(f"{BASE_DOMAIN}/en/")
    time.sleep(3)
    if "select-store" in driver.current_url:
        print("Please select your store/location in the browser")
        input("\nAfter selecting the store and reaching the Seoudi homepage, press ENTER here")

def get_product_cards(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup.select("article.ProductCard")

def extract_products(driver, category, subcategory):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = soup.select("article.ProductCard")
    products = []
    for card in cards:
        name_tag = card.select_one("a.ProductCard__Name")
        if not name_tag:
            continue
        product_name = name_tag.get_text(" ", strip=True)
        href = name_tag.get("href")
        if href:
            product_url = urljoin(BASE_DOMAIN, href)
        else:
            product_url = ""

        current_price = ""
        price_tag = card.select_one("span.font-bold")
        if price_tag:
            current_price = price_tag.get_text(" ", strip=True)

        original_price = ""
        original_tag = card.select_one("span.line-through")
        if original_tag:
            original_price = original_tag.get_text(" ", strip=True)

        discount = ""
        discount_tag = card.select_one("span.ProductCard__BadgeLabel--discount")
        if discount_tag:
            discount = discount_tag.get_text(" ", strip=True)

        availability = "In Stock"
        out_of_stock = card.select_one("div.OutOfStock")
        if out_of_stock:
            availability = "Out of Stock"

        brand = ""
        brand_tag = card.select_one("[class*='Brand']")
        if brand_tag:
            brand = brand_tag.get_text(" ", strip=True)

        weight_value = ""
        weight_unit = ""
        text = card.get_text(" ", strip=True)
        weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(kg|g|ml|l|liter|litre)", text, re.IGNORECASE)
        if weight_match:
            weight_value = weight_match.group(1)
            weight_unit = weight_match.group(2)

        product_type = "N/A"
        products.append({
            "scrape_id": "",
            "store": STORE,
            "product_name": product_name,
            "current_price": current_price,
            "brand": brand,
            "product_type": product_type,
            "category": category,
            "subcategory": subcategory,
            "weight_value": weight_value,
            "weight_unit": weight_unit,
            "original_price": original_price,
            "currency": "EGP",
            "product_url": product_url,
            "availability": availability,
            "scraped_at": pd.Timestamp.now(),
            "discount": discount})
    return products

def scrape_category_page(driver, wait, url, category, subcategory):
    print(f"\nOpening {category} / {subcategory}")
    driver.get(url)
    time.sleep(4)
    try:
        wait.until(lambda d: len(get_product_cards(d)) > 0)
    except:
        print("\nNo products detected immediately.")
        time.sleep(5)

    all_products = []
    seen_urls = set()
    initial_products = extract_products(driver, category, subcategory)
    print(f"\nInitial products found: {len(initial_products)}")
    for product in initial_products:
        url = product["product_url"]
        if url and url not in seen_urls:
            seen_urls.add(url)
            all_products.append(product)

    print(f"Unique products collected: {len(all_products)}")
    page_number = 1
    while True:
        try:
            load_more = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[.//span[contains(normalize-space(), 'Load More')]]")))
        except:
            print("\nNo Load More button found, Finished pagination")
            break
        old_count = len(get_product_cards(driver))
        driver.execute_script("""arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});""", load_more)
        time.sleep(1)
        print("Clicking Load More")
        driver.execute_script("arguments[0].click();", load_more)
        try:
            WebDriverWait(driver, 15).until(lambda d: len(get_product_cards(d)) > old_count)
        except:
            print("Pagination finished.")
            break
        time.sleep(2)
        current_products = extract_products(driver, category, subcategory)
        new_products = 0
        for product in current_products:
            url = product["product_url"]
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_products.append(product)
                new_products += 1

        page_number += 1
        print(f"Load More #{page_number - 1}: {new_products} new products")
        print(f"Total unique products: {len(all_products)}")
        if new_products == 0:
            print("\nNo new unique products found, Stopping pagination.")
            break
    return all_products

def save_csv(products, filename):
    df = pd.DataFrame(products)
    df["scrape_id"] = range(1, len(df) + 1)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print("SCRAPING FINISHED")
    print(f"Total unique products: {len(df)}")
    print(f"CSV saved to: {filename}")
    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")
    return df

def run_category(url, category, subcategory, output_file):
    driver = build_driver()
    wait = WebDriverWait(driver, 20)
    try:
        print("\nOpening Seoudi website")
        ensure_store_selected(driver)
        products = scrape_category_page(driver, wait, url, category, subcategory)
        save_csv(products, output_file)
    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        input("\nPress ENTER to close the browser")
        driver.quit()

def run_multi_category(pages, output_file):
    driver = build_driver()
    wait = WebDriverWait(driver, 20)
    all_products = []
    try:
        print("\nOpening Seoudi website")
        ensure_store_selected(driver)
        for page in pages:
            products = scrape_category_page(driver, wait, page["url"], page["category"], page["subcategory"])
            all_products.extend(products)
        save_csv(all_products, output_file)
    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        input("\nPress ENTER to close the browser")
        driver.quit()
