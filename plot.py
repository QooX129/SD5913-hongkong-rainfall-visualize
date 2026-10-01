# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "requests"]
# ///

"""
Fetch one year of HKO observations and plot one month of daily rainfall.

    uv run plot.py
"""

import calendar
import json
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt

from fetch import fetch_year

HERE = Path(__file__).parent
OUT = HERE / "out"
TRACE_RAINFALL = 0.025


def ask_for_number(label, minimum, maximum):
    """Prompt until the user enters an integer in the accepted range."""
    while True:
        try:
            value = int(input(f"{label}: "))
        except ValueError:
            print(f"Enter a whole number from {minimum} to {maximum}.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Enter a whole number from {minimum} to {maximum}.")


def rainfall_for_month(path, month):
    """Return available day numbers and daily rainfall totals for one month."""
    with path.open(encoding="utf-8") as handle:
        weather = json.load(handle)

    rainfall = next(
        (item for item in weather["stn"]["data"] if item["code"] == "RF"),
        None,
    )
    if rainfall is None:
        raise ValueError("the downloaded file has no rainfall records")

    days = []
    totals = []
    for row in rainfall["dayData"]:
        value = row[month].strip()
        if not value:
            continue
        days.append(int(row[0]))
        totals.append(TRACE_RAINFALL if value == "Trace" else float(value))
    return days, totals


def main():
    year = ask_for_number("Year", 1884, date.today().year)
    month = ask_for_number("Month", 1, 12)
    data_path = fetch_year(year)
    days, totals = rainfall_for_month(data_path, month)
    if not days:
        raise ValueError(f"no rainfall data are available for {calendar.month_name[month]} {year}")

    print(f"{len(totals)} daily totals, from {min(totals):g} to {max(totals):g} mm")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(days, totals, color="#247ba0", width=0.8)
    ax.set_xticks(range(1, calendar.monthrange(year, month)[1] + 1))
    ax.set_xlabel("Day of month")
    ax.set_ylabel("Daily total rainfall (mm)")
    ax.set_title(f"Hong Kong Observatory Rainfall - {calendar.month_name[month]} {year}")
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    picture = OUT / f"rainfall.png"
    fig.savefig(picture, dpi=150)
    print(f"saved out/{picture.name}")
    plt.show()


if __name__ == "__main__":
    main()
