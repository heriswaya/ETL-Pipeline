# utils/load.py

import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def save_to_csv(df, filepath='products.csv'):
    try:
        df.to_csv(filepath, index=False)
        print(f"✅ Data saved to {filepath}")
    except Exception as e:
        print(f"❌ Failed to save to CSV: {e}")

def save_to_postgres(df, db_url, table_name="products"):
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("✅ Data saved to PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to save to PostgreSQL: {e}")

def save_to_gsheet(df, spreadsheet_id, range_start='Sheet1!A1'):
    try:
        SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # Autentikasi
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )

        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Siapkan data frame untuk dimasukkan (termasuk header)
        values = [df.columns.tolist()] + df.values.tolist()

        # Kirim data
        body = {
            'values': values
        }

        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_start,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"✅ Data saved to Google Sheets. {result.get('updatedCells')} cells updated.")

    except Exception as e:
        print(f"❌ Failed to save to Google Sheets: {e}")