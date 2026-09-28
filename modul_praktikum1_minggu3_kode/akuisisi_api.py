"""
Praktikum 1 - Minggu 3 - Bagian A
Akuisisi Data dari API Publik (Open-Meteo)
Data cuaca kota-kota di sekitar Danau Toba

Mata Kuliah: Data Analitik
Sub-CPMK-03: akuisisi, pembersihan, dan transformasi data dari berbagai sumber
"""
import requests
import pandas as pd
import json
import os
from datetime import datetime

os.makedirs("data_raw", exist_ok=True)

# Titik koordinat kota-kota di sekitar Danau Toba
KOTA = {
    "Balige":          {"lat": 2.3333, "lon": 99.0667},
    "Pematangsiantar": {"lat": 2.9595, "lon": 99.0687},
    "Medan":           {"lat": 3.5952, "lon": 98.6722},
}

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def ambil_data_cuaca(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",     # otomatis memakai zona waktu lokasi
        "forecast_days": 3
    }
    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()   # hentikan proses jika status bukan 200
    return response.json()


def main():
    # --- A2: Request data untuk tiap kota ---
    semua_respon = {}
    for kota, koordinat in KOTA.items():
        print(f"Mengambil data cuaca: {kota} ...")
        try:
            semua_respon[kota] = ambil_data_cuaca(koordinat["lat"], koordinat["lon"])
        except requests.exceptions.RequestException as e:
            print(f"  Gagal mengambil data {kota}: {e}")

    # --- A3: Simpan JSON mentah apa adanya (arsip data mentah, sebelum diubah bentuk apa pun) ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    json_path = f"data_raw/cuaca_api_mentah_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(semua_respon, f, ensure_ascii=False, indent=2)
    print(f"JSON mentah tersimpan: {json_path}")

    # --- A4: Ratakan JSON bersarang (per kota -> per jam) menjadi tabel ---
    daftar_baris = []
    for kota, data in semua_respon.items():
        jam = data["hourly"]["time"]
        suhu = data["hourly"]["temperature_2m"]
        kelembapan = data["hourly"]["relative_humidity_2m"]
        hujan = data["hourly"]["precipitation"]
        for i in range(len(jam)):
            daftar_baris.append({
                "kota": kota,
                "waktu": jam[i],
                "suhu_c": suhu[i],
                "kelembapan_persen": kelembapan[i],
                "presipitasi_mm": hujan[i]
            })

    df_cuaca = pd.DataFrame(daftar_baris)
    print(df_cuaca.head())
    print("Jumlah baris:", len(df_cuaca))

    # --- A5: Simpan sebagai CSV mentah ---
    df_cuaca.to_csv("data_raw/cuaca_api_mentah.csv", index=False)
    print("CSV mentah tersimpan: data_raw/cuaca_api_mentah.csv")


if __name__ == "__main__":
    main()
