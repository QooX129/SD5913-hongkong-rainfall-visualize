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

PRIMARY_COLOR = "#247BA0"
COMPARISON_COLORS = ["#D1495B", "#EDA839", "#3A7D44", "#725AC1"]


@st.cache_data(ttl=3600, show_spinner=False)
def load_year(year):
    """Fetch and cache one yearly HKO file for this browser session."""
    return fetch_year(year)


def monthly_totals(path):
    """Return available monthly rainfall totals keyed by month number."""
    totals = {}
    for month_number in range(1, 13):
        _, daily_totals = rainfall_for_month(path, month_number)
        if daily_totals:
            totals[month_number] = sum(daily_totals)
    return totals


st.set_page_config(page_title="Hong Kong Rainfall", layout="wide")
st.title("Hong Kong Rainfall Visualizer")

controls, chart = st.columns([1, 3])
with controls:
    year_options = list(range(date.today().year, 1883, -1))
    year = st.selectbox(
        "Year",
        year_options,
    )
    show_year = st.checkbox("Show the whole year")
    month = None
    primary_color = PRIMARY_COLOR
    comparison_years = []
    comparison_opacity = 0.4
    comparison_colors = {}
    if show_year:
        primary_color = st.color_picker(
            f"{year} color",
            PRIMARY_COLOR,
            key=f"primary-color-{year}",
        )
        comparison_years = st.multiselect(
            "Compare with",
            [option for option in year_options if option != year],
            max_selections=4,
        )
        if comparison_years:
            comparison_opacity = st.slider(
                "Comparison opacity",
                min_value=0.1,
                max_value=1.0,
                value=0.4,
                step=0.05,
            )
            for index, comparison_year in enumerate(comparison_years):
                comparison_colors[comparison_year] = st.color_picker(
                    f"{comparison_year} color",
                    COMPARISON_COLORS[index],
                    key=f"comparison-color-{comparison_year}",
                )
    else:
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
        primary_totals = monthly_totals(data_path)
        if not primary_totals:
            raise ValueError(f"No rainfall data are available for {year}.")

        series = [(year, primary_totals, primary_color, 1.0)]
        for comparison_year in comparison_years:
            with st.spinner(f"Loading rainfall records for {comparison_year}..."):
                comparison_path = load_year(comparison_year)
            series.append(
                (
                    comparison_year,
                    monthly_totals(comparison_path),
                    comparison_colors[comparison_year],
                    comparison_opacity,
                )
            )

        bar_width = 0.8 / len(series)
        for index, (series_year, totals_by_month, color, opacity) in enumerate(series):
            offset = (index - (len(series) - 1) / 2) * bar_width
            months = list(totals_by_month)
            axis.bar(
                [month_number + offset for month_number in months],
                [totals_by_month[month_number] for month_number in months],
                color=color,
                alpha=opacity,
                width=bar_width,
                label=str(series_year),
            )

        axis.set_xticks(range(1, 13), [calendar.month_abbr[number] for number in range(1, 13)])
        axis.set_xlabel("Month")
        axis.set_ylabel("Monthly total rainfall (mm)")
        axis.set_title("Monthly Rainfall Comparison" if comparison_years else f"Monthly Rainfall - {year}")
        if comparison_years:
            axis.legend(title="Year")
        summary = " | ".join(
            f"{series_year}: {len(totals_by_month)} months, {sum(totals_by_month.values()):,.1f} mm"
            for series_year, totals_by_month, _, _ in series
        )
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