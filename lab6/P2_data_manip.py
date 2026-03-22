"""
Panhathai Suporn
683040496-5
P2: Data Manip
"""

import json
import pandas as pd
import pyqtgraph as pg
import numpy as np

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """TODO 1 — Read a CSV file and return a clean DataFrame."""

    df = pd.read_csv(path)

    # ตรวจสอบว่ามี columns ครบ
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # แปลง type ให้ถูกต้อง
    df["temp_c"]      = pd.to_numeric(df["temp_c"],      errors="raise")
    df["humidity"]    = pd.to_numeric(df["humidity"],    errors="raise")
    df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="raise")

    return df


def read_json(path: str) -> pd.DataFrame:
    """TODO 2 — Read a JSON file and return a DataFrame."""

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # รองรับทั้ง list of dicts และ dict of lists
    df = pd.DataFrame(data)

    # ตรวจสอบว่ามี columns ครบ
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # แปลง type ให้ถูกต้อง
    df["temp_c"]      = pd.to_numeric(df["temp_c"],      errors="raise")
    df["humidity"]    = pd.to_numeric(df["humidity"],    errors="raise")
    df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="raise")

    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """TODO 3 — Save a DataFrame to a CSV file."""

    if df.empty:
        raise ValueError("No data to save.")

    df.to_csv(path, index=False, encoding="utf-8")


def write_json(df: pd.DataFrame, path: str) -> None:
    """TODO 4 — Save a DataFrame to a JSON file."""

    if df.empty:
        raise ValueError("No data to save.")

    # orient="records" → list of dicts, indent=2 → อ่านง่าย
    df.to_json(path, orient="records", indent=2, force_ascii=False)


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """TODO 5 — Return a QTableWidget showing per-city statistics."""

    if df.empty:
        raise ValueError("No data for statistics.")

    # คำนวณ stats แยกตาม city
    stats = df.groupby("city").agg(
        avg_temp    =("temp_c",      "mean"),
        max_temp    =("temp_c",      "max"),
        min_temp    =("temp_c",      "min"),
        total_rain  =("rainfall_mm", "sum"),
        avg_humidity=("humidity",    "mean"),
    ).round(1).T  # transpose → rows = metrics, cols = cities

    cities  = list(stats.columns)
    metrics = list(stats.index)

    table = QTableWidget(len(metrics), len(cities))
    table.setHorizontalHeaderLabels(cities)
    table.setVerticalHeaderLabels(metrics)

    for ri, metric in enumerate(metrics):
        for ci, city in enumerate(cities):
            val  = str(stats.loc[metric, city])
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(ri, ci, item)

    table.resizeColumnsToContents()
    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """TODO 6 — Draw a Rainfall Histogram using pyqtgraph, return a PlotWidget."""

    if df.empty:
        raise ValueError("No data to chart.")

    if "rainfall_mm" not in df.columns:
        raise ValueError("Column 'rainfall_mm' not found.")

    data = df["rainfall_mm"].dropna().values

    # คำนวณ histogram
    counts, bin_edges = np.histogram(data, bins=10)

    pw = pg.PlotWidget()
    pw.setBackground("w")
    pw.setTitle("Rainfall Histogram", color="k", size="12pt")
    pw.setLabel("left",   "Frequency",   color="k")
    pw.setLabel("bottom", "Rainfall (mm)", color="k")
    pw.getAxis("left").setTextPen("k")
    pw.getAxis("bottom").setTextPen("k")

    # สร้าง bar graph
    bar_width = bin_edges[1] - bin_edges[0]
    bar_item = pg.BarGraphItem(
        x    = bin_edges[:-1],
        height = counts,
        width  = bar_width * 0.9,
        brush  = pg.mkBrush(30, 144, 255, 180),  # dodger blue
        pen    = pg.mkPen("w", width=1),
    )
    pw.addItem(bar_item)

    return pw