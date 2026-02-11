# viz/charts.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# Weekly Revenue Trend (with Anomaly Highlight)
# =========================================================
def plot_weekly_revenue(weekly_total, anomaly_result):
    """
    Expects weekly_total to contain:
    - week
    - Revenue
    """

    fig = px.line(
        weekly_total,
        x="week",
        y="Revenue",
        markers=True,
        title="Weekly Revenue Trend",
    )

    # Highlight anomalous week (if detected)
    if anomaly_result and anomaly_result.get("is_anomaly", False):
        latest = weekly_total.iloc[-1]

        fig.add_trace(
            go.Scatter(
                x=[latest["week"]],
                y=[latest["Revenue"]],
                mode="markers",
                marker=dict(color="red", size=12),
                name="Statistical Anomaly",
            )
        )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Week",
        yaxis_title="Revenue",
        showlegend=True,
    )

    return fig


# =========================================================
# Country-level Drivers (WoW % with Annotations)
# =========================================================
def plot_country_drivers(country_trends, anomaly_results):
    """
    country_trends: list of dicts with Country + wow_pct
    anomaly_results: output of anomaly_engine
    """

    if not country_trends:
        return go.Figure()

    df = pd.DataFrame(country_trends)

    fig = px.bar(
        df,
        x="Country",
        y="wow_pct",
        title="Country-level Revenue Change (WoW %)",
        labels={"wow_pct": "WoW % Change"},
    )

    # Annotate anomalous countries
    for anomaly in anomaly_results.get("driver_anomalies", []):
        fig.add_annotation(
            x=anomaly["entity"],
            y=anomaly["wow_pct"],
            text="Anomaly",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            font=dict(color="red"),
        )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Country",
        yaxis_title="WoW % Change",
        showlegend=False,
    )

    return fig


# =========================================================
# Channel-level Revenue Trends (WoW %)
# =========================================================
def plot_channel_trends(channel_trends):
    """
    channel_trends: list of dicts with Channel + wow_pct
    """

    if not channel_trends:
        return go.Figure()

    df = pd.DataFrame(channel_trends)

    fig = px.bar(
        df,
        x="Channel",
        y="wow_pct",
        title="Channel-level Revenue Change (WoW %)",
        labels={"wow_pct": "WoW % Change"},
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Channel",
        yaxis_title="WoW % Change",
        showlegend=False,
    )

    return fig
