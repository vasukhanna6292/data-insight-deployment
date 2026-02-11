# engines/trend_engine.py

import pandas as pd

# =========================================================
# Overall Revenue Trend (CONSUMES precomputed WoW)
# =========================================================
def overall_revenue_trend(weekly_total):
    """
    Expects weekly_total to already contain:
    - Revenue
    - revenue_wow_pct
    """

    latest = weekly_total.iloc[-1]
    pct = latest["revenue_wow_pct"]

    return {
        "metric": "Revenue",
        "level": "Overall",
        "wow_pct": round(pct, 1),
        "direction": "increase" if pct > 0 else "decrease",
        "severity": (
            "flat" if abs(pct) < 2
            else "moderate" if abs(pct) < 10
            else "significant"
        ),
    }


# =========================================================
# Country-level Trends (Top & Bottom Movers)
# =========================================================
def country_trends(weekly_df):
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

    latest_week = country_weekly["week"].max()

    movers = (
        country_weekly[
            (country_weekly["week"] == latest_week) &
            (country_weekly["wow_pct"].notna())
        ]
        .sort_values("wow_pct", ascending=False)
    )

    top_bottom = pd.concat([movers.head(2), movers.tail(2)])

    return top_bottom.to_dict("records")


# =========================================================
# Channel-level Trends
# =========================================================
def channel_trends(weekly_df):
    channel_weekly = (
        weekly_df
        .groupby(["week", "Channel"], as_index=False)["Revenue"]
        .sum()
        .sort_values("week")
    )

    channel_weekly["wow_pct"] = (
        channel_weekly
        .groupby("Channel")["Revenue"]
        .pct_change() * 100
    )

    latest_week = channel_weekly["week"].max()

    latest = channel_weekly[
        (channel_weekly["week"] == latest_week) &
        (channel_weekly["wow_pct"].notna())
    ]

    return latest.to_dict("records")


# =========================================================
# Promotion Trend (SEMANTICALLY MATCHES NOTEBOOK)
# =========================================================
def promotion_trend(df):
    if "Promotion" not in df.columns:
        return []

    promo_weekly = (
        df
        .assign(promo_flag=df["Promotion"].fillna("No Promotion"))
        .groupby(["week", "promo_flag"], as_index=False)["Revenue"]
        .sum()
        .sort_values("week")
    )

    promo_weekly["wow_pct"] = (
        promo_weekly
        .groupby("promo_flag")["Revenue"]
        .pct_change() * 100
    )

    latest_week = promo_weekly["week"].max()

    latest = promo_weekly[
        (promo_weekly["week"] == latest_week) &
        (promo_weekly["wow_pct"].notna())
    ]

    return latest.to_dict("records")


# =========================================================
# Unit Price & Demand Trend (WEIGHTED, NOTEBOOK-CORRECT)
# =========================================================
def unit_price_trend(weekly_df):
    weekly = (
        weekly_df
        .groupby("week", as_index=False)
        .agg({
            "Revenue": "sum",
            "Units Sold": "sum"
        })
        .sort_values("week")
    )

    weekly["avg_price"] = weekly["Revenue"] / weekly["Units Sold"]
    weekly["units_change_pct"] = weekly["Units Sold"].pct_change() * 100
    weekly["price_change_pct"] = weekly["avg_price"].pct_change() * 100

    latest = weekly.iloc[-1]

    return {
        "units_change_pct": round(latest["units_change_pct"], 1),
        "price_change_pct": round(latest["price_change_pct"], 1),
    }


# =========================================================
# Master Runner (PURE ORCHESTRATION)
# =========================================================
def run_trend_engine(df, weekly_df, weekly_total):
    """
    Returns a fully structured, notebook-equivalent trend output.
    """

    return {
        "overall_revenue_trend": overall_revenue_trend(weekly_total),
        "country_trends": country_trends(weekly_df),
        "channel_trends": channel_trends(weekly_df),
        "promotion_trend": promotion_trend(df),
        "unit_price_trend": unit_price_trend(weekly_df),
    }
