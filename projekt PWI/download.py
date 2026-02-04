import requests
from bs4 import BeautifulSoup
from pathlib import Path
import zipfile
import re
import pandas as pd

BASE_URL = "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/"
YEARS = list(range(2001, 2024))

ZIP_DIR = Path("imgw_zips")
CSV_DIR = Path("imgw_csv")

ZIP_DIR.mkdir(exist_ok=True)
CSV_DIR.mkdir(exist_ok=True)

for year in YEARS:
    url = f"{BASE_URL}{year}/"
    resp = requests.get(url)
    if resp.status_code != 200:
        continue
    
    soup = BeautifulSoup(resp.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".zip"):
            zip_path = ZIP_DIR / f"{year}_{href}"
            if not zip_path.exists():
                r = requests.get(url + href)
                zip_path.write_bytes(r.content)

CSV_RE = re.compile(r"k_d_\d{2}_\d{4}\.csv$")

for zip_path in ZIP_DIR.glob("*.zip"):

    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if CSV_RE.match(Path(name).name):
                z.extract(name, CSV_DIR)
            else:
                pass

OUT_FILE = "imgw_2001_2023.csv"

columns_to_keep = [
    "Kod_stacji", "Nazwa_stacji", "Rok", "Miesiac", "Dzien",
    "TMAX", "TMIN", "STD"
]

column_names = [
    "Kod_stacji", "Nazwa_stacji", "Rok", "Miesiac", "Dzien",
    "TMAX", "Status_TMAX", "TMIN", "Status_TMIN", "STD", "Status_STD",
    "TMNG", "Status_TMNG", "SMDB", "Status_SMDB", "Rodzaj_opadu",
    "PKSN", "Status_PKSN"
]

dfs = []
for csv_file in sorted(CSV_DIR.glob("k_d_*.csv")):
    
    df = pd.read_csv(
        csv_file,
        encoding="cp1250",
        sep=None,
        engine='python',
        quotechar='"'
    )

    df = df.iloc[:, :18]
    
    df.columns = column_names
    
    df = df[columns_to_keep]
    
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

combined.to_csv(OUT_FILE, index=False, sep=";", encoding="utf-8")