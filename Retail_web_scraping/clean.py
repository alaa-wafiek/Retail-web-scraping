import pandas as pd

INPUT_FILE = "Retail_web_scraping\\seoudi_scraped_data.csv"
OUTPUT_FILE = "Retail_web_scraping\\seoudi_scraped_data_clean.csv"

df = pd.read_csv(INPUT_FILE)
df["scrape_id"] = range(1, len(df) + 1)
df["scraped_at"] = pd.to_datetime(df["scraped_at"], format="mixed").dt.strftime("%Y-%m-%d %H:%M:%S")
text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].str.strip()

df["product_type"] = df["product_type"].str.title()   # 'cheese' -> 'Cheese'
df["weight_unit"] = df["weight_unit"].str.lower()      # 'Kg'/'Pieces' -> 'kg'/'pieces'

if "pack_count" in df.columns:
    mask = df["pack_count"].notna() & df["weight_value"].isna()
    df.loc[mask, "weight_value"] = pd.to_numeric(df.loc[mask, "pack_count"], errors="coerce")
    df.loc[mask, "weight_unit"] = "pieces"
    df = df.drop(columns=["pack_count"])

def strip_decimal_for_pieces(df):
    if "weight_value" not in df.columns or "weight_unit" not in df.columns:
        return df

    mask = (df["weight_unit"].fillna("").str.lower() == "pieces") & df["weight_value"].notna()
    df = df.copy()

    def normalize_piece_value(value):
        if pd.isna(value):
            return value
        number = pd.to_numeric(value, errors="coerce")
        if pd.isna(number):
            return value
        if float(number).is_integer():
            return int(number)
        return float(number)

    df.loc[mask, "weight_value"] = df.loc[mask, "weight_value"].map(normalize_piece_value)
    return df


df = strip_decimal_for_pieces(df)

df.to_csv(OUTPUT_FILE, index=False)
print(f"Done. Cleaned {len(df)} rows -> {OUTPUT_FILE}")