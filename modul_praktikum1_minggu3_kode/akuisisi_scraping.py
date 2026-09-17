"""
Praktikum 1 - Minggu 3 - Bagian B
Akuisisi Data via Web Scraping/Crawling (books.toscrape.com)

Mata Kuliah: Data Analitik
Sub-CPMK-03: akuisisi, pembersihan, dan transformasi data dari berbagai sumber

Catatan etika: books.toscrape.com adalah situs sandbox resmi yang memang
dibuat untuk latihan scraping. Untuk situs lain, SELALU periksa robots.txt
dan Terms of Service sebelum melakukan scraping/crawling.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

os.makedirs("data_raw", exist_ok=True)

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "MahasiswaDataAnalitik-ITDel/1.0 (tugas praktikum)"}


def ambil_satu_halaman(nomor_halaman):
    url = BASE_URL.format(nomor_halaman)
    response = requests.get(url, headers=HEADERS, timeout=15)
    if response.status_code != 200:
        return None
    return response.text


def ekstrak_buku(html):
    soup = BeautifulSoup(html, "lxml")
    hasil = []
    for produk in soup.select("article.product_pod"):
        judul_tag = produk.select_one("h3 a")
        judul = judul_tag["title"] if judul_tag else None

        harga_tag = produk.select_one("p.price_color")
        harga_mentah = harga_tag.get_text(strip=True) if harga_tag else None

        rating_tag = produk.select_one("p.star-rating")
        kelas_rating = rating_tag["class"] if rating_tag else []
        rating_mentah = next((k for k in kelas_rating if k != "star-rating"), None)

        ketersediaan_tag = produk.select_one("p.instock.availability")
        ketersediaan_mentah = ketersediaan_tag.get_text(strip=True) if ketersediaan_tag else None

        hasil.append({
            "judul": judul,
            "harga_mentah": harga_mentah,               # masih string, contoh "£51.77"
            "rating_mentah": rating_mentah,              # masih teks: "One".."Five"
            "ketersediaan_mentah": ketersediaan_mentah   # masih kalimat, contoh "In stock"
        })
    return hasil


def crawl_beberapa_halaman(jumlah_halaman=5, jeda_detik=1):
    """Crawling sopan: batasi jumlah halaman dan beri jeda antar-request."""
    semua_buku = []
    for halaman in range(1, jumlah_halaman + 1):
        print(f"Mengambil halaman {halaman} ...")
        html = ambil_satu_halaman(halaman)
        if html is None:
            print(f"  Halaman {halaman} tidak tersedia, berhenti crawling.")
            break
        semua_buku.extend(ekstrak_buku(html))
        time.sleep(jeda_detik)   # jeda sopan agar tidak membebani server
    return semua_buku


def main():
    data_buku = crawl_beberapa_halaman(jumlah_halaman=5, jeda_detik=1)
    df_buku = pd.DataFrame(data_buku)
    print(df_buku.head())
    print("Jumlah baris:", len(df_buku))

    df_buku.to_csv("data_raw/buku_scraping_mentah.csv", index=False)
    print("CSV mentah tersimpan: data_raw/buku_scraping_mentah.csv")


if __name__ == "__main__":
    main()
