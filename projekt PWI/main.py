import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "imgw_2001_2023_temp.csv"

df = pd.read_csv(CSV_FILE, sep=";")

# Zad 1

stations_record_count = (
    df.groupby("Nazwa_stacji")
      .size()
      .reset_index(name="liczba_rekordow")
)

stations_8400_records = stations_record_count[
    stations_record_count["liczba_rekordow"] == 8400
]

station_8400_names = stations_8400_records[["Nazwa_stacji"]]

station_8400_names.to_csv(
    "stacje_mające_8400_rekordow.csv",
    index=False,
    sep=";",
    encoding="utf-8"
)

# Zad 2

station_without_8400 = stations_record_count[
    stations_record_count["liczba_rekordow"] != 8400
].iloc[0]["Nazwa_stacji"]

station_without_8400_df = df[df["Nazwa_stacji"] == station_without_8400]

monthly_count = (
    station_without_8400_df
    .groupby(["Rok", "Miesiac"])
    .size()
    .reset_index(name="Liczba_pomiarow")
)

monthly_count["Rok_Miesiac"] = (
    monthly_count["Rok"].astype(int).astype(str)
    + "-"
    + monthly_count["Miesiac"].astype(int).astype(str).str.zfill(2)
)

monthly_count = monthly_count.sort_values(["Rok", "Miesiac"])

plt.figure(figsize=(20, 6))
plt.bar(
    monthly_count["Rok_Miesiac"],
    monthly_count["Liczba_pomiarow"],
    width=0.6
)

plt.xticks(rotation=90)
plt.ylim(25, 32)
plt.xlabel("Rok–miesiąc")
plt.ylabel("Liczba pomiarów")
plt.title(f"Liczba pomiarów w miesiącach – {station_without_8400}")
plt.show()

# Zad 3

station_with_8400 = station_8400_names.iloc[0]["Nazwa_stacji"]

station_with_8400_df = df[df["Nazwa_stacji"] == station_with_8400]

# Uproszczenie 31 dni w miesiącu
station_with_8400_df["Dni_od_startu"] = (
    (station_with_8400_df["Rok"] - 2001) * 12 * 31
    + (station_with_8400_df["Miesiac"] - 1) * 31
    + (station_with_8400_df["Dzien"] - 1)
)

station_with_8400_df = station_with_8400_df.sort_values("Dni_od_startu")

plt.figure(figsize=(20, 6))
plt.plot(
    station_with_8400_df["Dni_od_startu"],
    station_with_8400_df["STD"]
)

plt.xlabel("Liczba dni od 01.01.2001")
plt.ylabel("Średnia temperatura dobowa [°C]")
plt.title(f"Średnia temperatura dobowa – {station_with_8400}")
plt.show()

# Zad 4

df4 = df.copy()
df4["TMIN"] = pd.to_numeric(df["TMIN"], errors="coerce")
df4["TMAX"] = pd.to_numeric(df["TMAX"], errors="coerce")

df4_temp = df4.dropna(subset=["TMIN", "TMAX"])

min_temp_row = df4_temp.loc[df4_temp["TMIN"].idxmin()]
max_temp_row = df4_temp.loc[df4_temp["TMAX"].idxmax()]

print(f"Temperatura min: {min_temp_row['TMIN']} °C")
print(
    f"Data: {int(min_temp_row['Rok'])}-"
    f"{int(min_temp_row['Miesiac']):02d}-"
    f"{int(min_temp_row['Dzien']):02d}"
)
print(f"Stacja: {min_temp_row['Nazwa_stacji']}")
print()

print(f"Temperatura max: {max_temp_row['TMAX']} °C")
print(
    f"Data: {int(max_temp_row['Rok'])}-"
    f"{int(max_temp_row['Miesiac']):02d}-"
    f"{int(max_temp_row['Dzien']):02d}"
)
print(f"Stacja: {max_temp_row['Nazwa_stacji']}")

# Zad 5

station_with_8400_df = df[df["Nazwa_stacji"] == station_with_8400]

station_with_8400_df = station_with_8400_df.dropna(subset=["STD"])

monthly_avg = (
    station_with_8400_df.groupby(["Rok", "Miesiac"])["STD"]
    .mean()
    .reset_index()
)
months = range(1, 13)
month_names = [
    "Styczeń", "Luty", "Marzec", "Kwiecień",
    "Maj", "Czerwiec", "Lipiec", "Sierpień",
    "Wrzesień", "Październik", "Listopad", "Grudzień"
]

for month in months:
    month_df = monthly_avg[monthly_avg["Miesiac"] == month]
    
    plt.figure(figsize=(10, 4))
    plt.bar(month_df["Rok"], month_df["STD"], color="skyblue", width=0.6)
    
    plt.xlabel("Rok")
    plt.ylabel("Średnia temperatura [°C]")
    plt.title(f"Średnia temperatura – {month_names[month-1]} – {station_with_8400}")
    plt.show()