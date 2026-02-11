# engines/prep_engine.py

import pandas as pd

# ============================================================
# Column Role Contract (LOCKED – mirrors notebook)
# ============================================================
COLUMN_ROLES = {
    "time": {
        "primary": "Date",
        "grain": "weekly",
    },
    "metrics": {
        "primary": "Revenue",
        "secondary": [
            "Units Sold",
            "Margin",
            "Margin %",
            "Discount",
            "Unit Price",
        ],
    },
    "dimensions": {
        "primary": [
            "Country",
            "Channel",
            "Store",
        ],
        "secondary": [
            "SKU",
            "Promotion",
        ],
    },
}

PRIMARY_KEY = "transaction_id"


# ============================================================
# Main Preparation Engine
# ============================================================
def prepare_data(df: pd.DataFrame):
    """
    Canonical data preparation layer.
    Mirrors the Jupyter notebook logic exactly.

    Returns:
        clean_df
        weekly_df
        weekly_total
        analysis_week
    """

    df = df.copy()

    # --------------------------------------------------------
    # 1. Validate Required Columns
    # --------------------------------------------------------
    required_columns = (
        [COLUMN_ROLES["time"]["primary"]]
        + [COLUMN_ROLES["metrics"]["primary"]]
        + COLUMN_ROLES["dimensions"]["primary"]
    )

    missing_cols = [c for c in required_columns if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # --------------------------------------------------------
    # 2. Parse Date
    # --------------------------------------------------------
    TIME_COL = COLUMN_ROLES["time"]["primary"]

    df[TIME_COL] = pd.to_datetime(
        df[TIME_COL],
        errors="coerce",
        dayfirst=True
    )

    df = df.dropna(subset=[TIME_COL])

    # --------------------------------------------------------
    # 3. Create WEEK column (CRITICAL)
    # --------------------------------------------------------
    df["week"] = (
        df[TIME_COL]
        .dt.to_period("W")
        .apply(lambda r: r.start_time)
    )

    # --------------------------------------------------------
    # 4. Coerce Numeric Metrics
    # --------------------------------------------------------
    numeric_cols = (
        [COLUMN_ROLES["metrics"]["primary"]]
        + COLUMN_ROLES["metrics"]["secondary"]
    )

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --------------------------------------------------------
    # 5. Handle Missing Revenue / Units / Price
    # --------------------------------------------------------
    REVENUE_COL = "Revenue"
    UNITS_COL = "Units Sold"
    PRICE_COL = "Unit Price"

    if UNITS_COL in df.columns and PRICE_COL in df.columns:
        can_compute_revenue = (
            df[REVENUE_COL].isna()
            & df[UNITS_COL].notna()
            & df[PRICE_COL].notna()
        )

        df.loc[can_compute_revenue, REVENUE_COL] = (
            df.loc[can_compute_revenue, UNITS_COL]
            * df.loc[can_compute_revenue, PRICE_COL]
        )

    df = df.dropna(subset=[REVENUE_COL])

    # --------------------------------------------------------
    # 6. Fill Dimension Nulls
    # --------------------------------------------------------
    for col in COLUMN_ROLES["dimensions"]["primary"]:
        df[col] = df[col].fillna("Unknown")

    if "Promotion" in df.columns:
        df["Promotion"] = df["Promotion"].fillna("No Promotion")

    # --------------------------------------------------------
    # 7. Weekly Aggregations
    # --------------------------------------------------------
    weekly_df = (
        df
        .groupby(
            ["week"] + COLUMN_ROLES["dimensions"]["primary"],
            as_index=False
        )
        .agg({
            "Revenue": "sum",
            "Units Sold": "sum"
        })
        .sort_values("week")
    )

    weekly_total = (
        weekly_df
        .groupby("week", as_index=False)["Revenue"]
        .sum()
        .sort_values("week")
    )

    weekly_total["revenue_wow_pct"] = (
        weekly_total["Revenue"].pct_change() * 100
    )

    # --------------------------------------------------------
    # 8. Analysis Week (LATEST WEEK ONLY)
    # --------------------------------------------------------
    analysis_week = weekly_total.iloc[-1]["week"]

    return df, weekly_df, weekly_total, analysis_week
