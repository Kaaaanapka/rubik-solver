#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os

# ======= Konfiguracja =======
INPUT_FILE = "data/solves.csv"       # CSV wyeksportowany z Django
OUTPUT_DIR = "analysis_output"       # katalog z wynikami

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======= Wczytaj dane =======
df = pd.read_csv(INPUT_FILE, sep=";")

# jeśli masz kolumnę time_ms -> zamień na sekundy
if "time_ms" in df.columns:
    df["time_s"] = df["time_ms"] / 1000.0
elif "time_min" in df.columns:  # gdybyś miał już w minutach
    df["time_s"] = df["time_min"] * 60
else:
    raise ValueError("Brak kolumny z czasem (time_ms albo time_min).")

# Policz TPS (ruchy / sekunda)
if "length_htm" in df.columns:
    df["TPS"] = df.apply(
        lambda r: (r["length_htm"] / r["time_s"]) if r["time_s"] > 0 else None,
        axis=1
    )

# ======= Przygotuj zbiory =======
# Pełny zbiór do analizy czasu
df_time = df.copy()

# Zbiór tylko z poprawnymi HTM
df_htm = df.copy()
df_htm = df_htm[df_htm["length_htm"].notna()]
df_htm = df_htm[df_htm["length_htm"] > 0]
# (opcjonalnie) odfiltruj ekstremalne outliery
# df_htm = df_htm[df_htm["length_htm"] <= 100]

print("Liczba wszystkich prób (czas):", len(df_time))
print("Liczba poprawnych prób (HTM):", len(df_htm))

# ======= Statystyki =======
print("\n=== Podstawowe statystyki czasu (wszystkie próby) ===")
stats_time = df_time.groupby("method").agg({
    "time_s": ["count", "mean", "median", "min", "max"],
    "TPS": ["mean", "median", "max"] if "TPS" in df_time.columns else "mean"
})
print(stats_time)
stats_time.to_csv(os.path.join(OUTPUT_DIR, "summary_stats_time.csv"), sep=";")

print("\n=== Podstawowe statystyki HTM (tylko poprawne) ===")
cols_htm = {"length_htm": ["count", "mean", "median", "min", "max"]}
if "length_qtm" in df_htm.columns:
    cols_htm["length_qtm"] = ["mean", "median", "min", "max"]
stats_htm = df_htm.groupby("method").agg(cols_htm)
print(stats_htm)
stats_htm.to_csv(os.path.join(OUTPUT_DIR, "summary_stats_htm.csv"), sep=";")

# ======= Wykresy =======

# Histogram czasu (pełny zbiór)
plt.figure(figsize=(8,6))
for method, group in df_time.groupby("method"):
    plt.hist(group["time_s"], bins=15, alpha=0.5, label=method)
plt.xlabel("Czas [s]")
plt.ylabel("Liczba solve’ów")
plt.title("Rozkład czasów per metoda")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "hist_times.png"))
plt.close()

# Boxplot HTM (tylko poprawne próby)
if "length_htm" in df_htm.columns and not df_htm.empty:
    plt.figure(figsize=(8,6))
    df_htm.boxplot(column="length_htm", by="method")
    plt.title("HTM per metoda (tylko poprawne wpisy)")
    plt.suptitle("")
    plt.ylabel("Liczba ruchów (HTM)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "box_htm.png"))
    plt.close()

# Scatter: czas vs HTM (tylko poprawne próby)
if "length_htm" in df_htm.columns and not df_htm.empty:
    plt.figure(figsize=(8,6))
    for method, group in df_htm.groupby("method"):
        plt.scatter(group["length_htm"], group["time_s"], alpha=0.7, label=method)
    plt.xlabel("HTM (liczba ruchów)")
    plt.ylabel("Czas [s]")
    plt.title("Czas vs liczba ruchów (HTM) — tylko poprawne wpisy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "scatter_time_htm.png"))
    plt.close()

print(f"\n✅ Analiza zakończona. Wyniki w folderze: {OUTPUT_DIR}")
