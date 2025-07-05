# main.py

from utils.extract import extract_product_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_gsheet, save_to_postgres

# Konstanta
CSV_PATH = 'products.csv'
SPREADSHEET_ID = '1hi2f6Fbk1LxKgLM2qH2hQo_irFY_-xJc7_r_P5ulO9I'
POSTGRES_DB_URL = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashion_studio_product_db'

def main():
    # 1. Extract
    print("🔍 Menjalankan tahap extract...")
    raw_data = extract_product_data()

    # 2. Transform
    print("🔧 Menjalankan tahap transform...")
    clean_data = transform_data(raw_data)

    # 3. Load
    print("💾 Menyimpan ke CSV...")
    save_to_csv(clean_data, filepath=CSV_PATH)

    print("💾 Menyimpan ke Google Sheets...")
    save_to_gsheet(clean_data, spreadsheet_id=SPREADSHEET_ID)

    print("💾 Menyimpan ke PostgreSQL...")
    save_to_postgres(clean_data, db_url=POSTGRES_DB_URL)

    print("✅ ETL Pipeline selesai dijalankan.")

if __name__ == "__main__":
    main()
