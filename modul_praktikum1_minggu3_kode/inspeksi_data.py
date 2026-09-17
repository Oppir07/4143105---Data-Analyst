"""
Praktikum 1 - Minggu 3 - Bagian C
Inspeksi Awal Kualitas Data + Data Preparation Log

Mata Kuliah: Data Analitik
Sub-CPMK-03: akuisisi, pembersihan, dan transformasi data dari berbagai sumber

Jalankan setelah akuisisi_api.py dan akuisisi_scraping.py berhasil dijalankan
(membutuhkan data_raw/cuaca_api_mentah.csv dan data_raw/buku_scraping_mentah.csv).
"""
import pandas as pd


def inspeksi(nama, df):
    print(f"\n=== {nama} ===")
    print("Ukuran:", df.shape)
    print(df.info())
    print("\nMissing value per kolom:")
    print(df.isnull().sum())
    print("\nJumlah baris duplikat:", df.duplicated().sum())


def main():
    df_cuaca = pd.read_csv("data_raw/cuaca_api_mentah.csv")
    df_buku = pd.read_csv("data_raw/buku_scraping_mentah.csv")

    inspeksi("Data Cuaca (API)", df_cuaca)
    inspeksi("Data Buku (Scraping)", df_buku)

    # Isu format spesifik yang perlu dicatat manual
    print("\nContoh isu format - harga (masih string bersimbol mata uang):")
    print(df_buku["harga_mentah"].head())

    print("\nContoh isu format - rating (masih teks, bukan angka):")
    print(df_buku["rating_mentah"].unique())

    # --- Susun Data Preparation Log ---
    log = pd.DataFrame([
        {
            "sumber": "Open-Meteo API",
            "format_asal": "JSON (bersarang per jam)",
            "jumlah_baris": len(df_cuaca),
            "jumlah_kolom": df_cuaca.shape[1],
            "missing_value_ditemukan": int(df_cuaca.isnull().sum().sum()),
            "duplikat_ditemukan": int(df_cuaca.duplicated().sum()),
            "isu_format_ditemukan": "nama kolom mencampur nilai & satuan (suhu_c, kelembapan_persen)",
            "rencana_penanganan": "pisahkan nilai dan satuan pada Praktikum 2"
        },
        {
            "sumber": "Books to Scrape (scraping)",
            "format_asal": "HTML",
            "jumlah_baris": len(df_buku),
            "jumlah_kolom": df_buku.shape[1],
            "missing_value_ditemukan": int(df_buku.isnull().sum().sum()),
            "duplikat_ditemukan": int(df_buku.duplicated().sum()),
            "isu_format_ditemukan": "harga bersimbol mata uang (string), rating berupa kata, ketersediaan berupa kalimat",
            "rencana_penanganan": "parsing harga ke angka, mapping rating ke angka, ketersediaan ke boolean pada Praktikum 2"
        }
    ])

    log.to_csv("data_preparation_log.csv", index=False)
    print("\nData Preparation Log tersimpan: data_preparation_log.csv")
    print(log)


if __name__ == "__main__":
    main()
