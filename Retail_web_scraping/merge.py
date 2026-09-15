import csv
import os

input_folder = r"C:\Users\ACER\Desktop\AI\scraping\Retail_web_scraping\processed"
output_folder = r"C:\Users\ACER\Desktop\AI\scraping\Retail_web_scraping"
output_file = os.path.join(output_folder, "seoudi_scraped_data.csv")

csv_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".csv")]

fieldnames = []
for filename in csv_files:
    filepath = os.path.join(input_folder, filename)
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        for col in header:
            if col not in fieldnames:
                fieldnames.append(col)

total_rows = 0
with open(output_file, "w", newline="", encoding="utf-8-sig") as out_f:
    writer = csv.DictWriter(out_f, fieldnames=fieldnames)
    writer.writeheader()

    for filename in csv_files:
        filepath = os.path.join(input_folder, filename)
        with open(filepath, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                writer.writerow(row)
                total_rows += 1

print(f"Combined {len(csv_files)} files into {output_file}")
print(f"Total rows written: {total_rows}")
print(f"Columns ({len(fieldnames)}): {fieldnames}")