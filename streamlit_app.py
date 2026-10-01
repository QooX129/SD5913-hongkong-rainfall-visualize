# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "requests", "streamlit"]
# ///

"""Interactive Streamlit interface for HKO daily rainfall records."""

import calendar
from datetime import date

import matplotlib.pyplot as plt
import streamlit as st

from fetch import fetch_year
from plot import rainfall_for_month


@st.cache_data(ttl=3600, show_spinner=False)
def load_year(year):
    """Fetch and cache one yearly HKO file for this browser session."""
    return fetch_year(year)


st.set_page_config(page_title="Hong Kong Rainfall", layout="wide")
st.title("Hong Kong Observatory Rainfall")

controls, chart = st.columns([1, 3])
with controls:
    year = st.selectbox(
        "Year",
        range(date.today().year, 1883, -1),
    )
    show_year = st.checkbox("Show the whole year")
    month = None
    if not show_year:
        month = st.selectbox(
            "Month",
            range(1, 13),
            format_func=lambda number: calendar.month_name[number],
        )

try:
    with st.spinner(f"Loading rainfall records for {year}..."):
        data_path = load_year(year)

    figure, axis = plt.subplots(figsize=(10, 4.8))
    if show_year:
        months = []
        totals = []
        for month_number in range(1, 13):
            _, daily_totals = rainfall_for_month(data_path, month_number)
            if daily_totals:
                months.append(month_number)
                totals.append(sum(daily_totals))
        if not months:
            raise ValueError(f"No rainfall data are available for {year}.")
        axis.bar(months, totals, color="#247ba0", width=0.8)
        axis.set_xticks(months, [calendar.month_abbr[number] for number in months])
        axis.set_xlabel("Month")
        axis.set_ylabel("Monthly total rainfall (mm)")
        axis.set_title(f"Monthly Rainfall - {year}")
        summary = f"{len(months)} months available · {sum(totals):,.1f} mm total"
    else:
        days, totals = rainfall_for_month(data_path, month)
        if not days:
            raise ValueError(f"No rainfall data are available for {calendar.month_name[month]} {year}.")
        axis.bar(days, totals, color="#247ba0", width=0.8)
        axis.set_xticks(range(1, calendar.monthrange(year, month)[1] + 1))
        axis.set_xlabel("Day of month")
        axis.set_ylabel("Daily total rainfall (mm)")
        axis.set_title(f"Daily Rainfall - {calendar.month_name[month]} {year}")
        summary = f"{len(days)} days available · {sum(totals):,.1f} mm total"

    axis.grid(axis="y", color="#d9d9d9", linewidth=0.7)
    axis.set_axisbelow(True)
    figure.tight_layout()

    with chart:
        st.caption(summary)
        st.pyplot(figure, width="stretch")
    plt.close(figure)
except Exception as error:
    with chart:
        st.error(str(error))