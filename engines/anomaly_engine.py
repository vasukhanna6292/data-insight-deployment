# engines/anomaly_engine.py

import numpy as np
import pandas as pd


# =========================================================
# Z-score Utility (safe, notebook-aligned)
# =========================================================
def compute_z_score(series):
    std = series.std()
    if std == 0 or np.isnan(std):
        return pd.Series([0] * len(series), index=series.index)
    return (series - series.mean()) / std


# =========================================================
# Overall Revenue Anomaly (CONSUMES precomputed WoW)
# =========================================================
def overall_revenue_anomaly(weekly_total, threshold=2):
    """
    Expects weekly_total to already contain:
    - revenue_wow_pct
    """

    series = weekly_total["revenue_wow_pct"].dropna()

    if len(series) < 4:
        return {
            "is_anomaly": False,
            "z_score": 0.0,
            "severity": "low",
        }

    z_scores = compute_z_score(series)
    latest_z = z_scores.iloc[-1]

    return {
        "is_anomaly": abs(latest_z) >= threshold,
        "z_score": round(latest_z, 2),
        "severity": (
            "high" if abs(latest_z) >= 3
            else "moderate" if abs(latest_z) >= threshold
            else "low"
        ),
    }


# =========================================================
# Country-level Revenue Anomalies (Rolling Window)
# =========================================================
def country_revenue_anomalies(weekly_df, window=8, threshold=2):
    anomalies = []

    country_weekly = (
        weekly_df
        .groupby(["week", "Country"], as_index=False)["Revenue"]
        .sum()
        .sort_values("week")
    )

    country_weekly["wow_pct"] = (
        country_weekly
        .groupby("Country")["Revenue"]
        .pct_change() * 100
    )

    for country, group in country_weekly.groupby("Country"):
        recent = group.dropna(subset=["wow_pct"]).tail(window)

        if len(recent) < 4:
            continue

        z_scores = compute_z_score(recent["wow_pct"])
        latest = recent.iloc[-1]
        latest_z = z_scores.iloc[-1]

        if abs(latest_z) >= threshold:
            anomalies.append(
                {
                    "dimension": "Country",
                    "entity": country,
                    "wow_pct": round(latest["wow_pct"], 1),
                    "z_score": round(latest_z, 2),
                }
            )

    return anomalies


# =========================================================
# Master Runner (PURE ORCHESTRATION)
# =========================================================
def run_anomaly_engine(weekly_total, weekly_df):
    """
    Returns anomaly signals aligned with notebook logic.
    """

    return {
        "overall_anomaly": overall_revenue_anomaly(weekly_total),
        "driver_anomalies": country_revenue_anomalies(weekly_df),
    }
