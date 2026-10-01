# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""
Fetch one year of daily Hong Kong Observatory weather data.

    uv run fetch.py

The yearly file includes daily rainfall. Each fetch replaces the file for that
year in data/ so that incomplete current-year data can be refreshed.
"""

from datetime import date
from pathlib import Path

import requests

URL = "https://www.hko.gov.hk/cis/individual_day/daily_{year}.xml"
HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(url, path):
    """Download a raw file, replacing any existing copy."""
    DATA.mkdir(exist_ok=True)
    print(f"asking {url}")
    reply = requests.get(url, timeout=60)
    reply.raise_for_status()
    path.write_bytes(reply.content)
    print(f"saved data/{path.name} ({path.stat().st_size // 1024} KB), replacing any older copy")
    return path


def fetch_year(year):
    """Fetch all available daily observations for one year."""
    if not 1884 <= year <= date.today().year:
        raise ValueError(f"year must be between 1884 and {date.today().year}")
    return fetch(URL.format(year=year), DATA / f"hko-daily-weather-{year}.xml")


if __name__ == "__main__":
    fetch_year(int(input("Year: ")))
