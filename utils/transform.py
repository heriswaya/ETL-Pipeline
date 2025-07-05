# utils/transform.py

import pandas as pd

def transform_data(data):
    try:
        # Ubah ke DataFrame
        df = pd.DataFrame(data)

        # Hapus baris dengan nilai null
        df = df.dropna()

        # Hapus duplikat
        df = df.drop_duplicates()

        # Hapus baris dengan title = "Unknown Product"
        df = df[df['Title'].str.lower() != "unknown product"]

        # Konversi kolom Price ke Rupiah
        # Pastikan price bertipe float terlebih dahulu
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')  # Jika gagal konversi, jadi NaN
        df = df.dropna(subset=['Price'])  # Drop jika price tak bisa dikonversi
        df['Price'] = df['Price'] * 16000

        # Final check untuk null dan duplikat
        df = df.dropna()
        df = df.drop_duplicates()

        return df

    except Exception as e:
        print(f"❌ Error during transformation: {e}")
        return pd.DataFrame()  # return DataFrame kosong jika gagal
