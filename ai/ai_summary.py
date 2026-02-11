# ai/ai_summary.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# =========================================================
# Prompt Builder (Executive, Deterministic)
# =========================================================
def build_ai_prompt(trend_results, anomaly_results, analysis_week):
    """
    Builds a senior, decision-oriented AI prompt for an executive weekly performance review.
    No calculations. No assumptions. Strictly narrative and judgment-based.
    """

    # -------------------- Trend Inputs --------------------
    overall = trend_results["overall_revenue_trend"]
    country_trends = trend_results.get("country_trends", [])
    channel_trends = trend_results.get("channel_trends", [])
    unit_price = trend_results["unit_price_trend"]
    promotion_trends = trend_results.get("promotion_trend", [])

    # -------------------- Anomaly Inputs --------------------
    overall_anomaly = anomaly_results["overall_anomaly"]
    driver_anomalies = anomaly_results.get("driver_anomalies", [])

    # -------------------- Regional Summary (SAFE) --------------------
    if country_trends:
        sorted_countries = sorted(
            country_trends, key=lambda x: x["wow_pct"], reverse=True
        )
        top_country_pos = sorted_countries[0]
        top_country_neg = sorted_countries[-1]

        regional_summary = (
            f"- Best performing region: {top_country_pos['Country']} "
            f"({round(top_country_pos['wow_pct'], 1)}%).\n"
            f"- Worst performing region: {top_country_neg['Country']} "
            f"({round(top_country_neg['wow_pct'], 1)}%)."
        )
    else:
        regional_summary = "- Regional performance data not available."

    # -------------------- Channel Summary (ORDERED) --------------------
    if channel_trends:
        channel_summary = ", ".join(
            sorted(
                [
                    f"{c['Channel']} ({round(c['wow_pct'], 1)}%)"
                    for c in channel_trends
                    if c.get("wow_pct") is not None
                ]
            )
        )
    else:
        channel_summary = "Channel performance data not available."

    # -------------------- Promotion Impact (SEMANTICALLY CORRECT) --------------------
    if promotion_trends:
        promo_summary = ", ".join(
            [
                f"{p['promo_flag']} ({round(p['wow_pct'], 1)}%)"
                for p in promotion_trends
                if p.get("wow_pct") is not None
            ]
        )
    else:
        promo_summary = "Promotion impact data not available."

    # -------------------- Anomaly Context --------------------
    if overall_anomaly["is_anomaly"]:
        anomaly_text = (
            f"An overall revenue anomaly was detected this week "
            f"(Z-score: {round(overall_anomaly['z_score'], 2)}), "
            "indicating a statistically significant deviation from historical performance."
        )
    else:
        anomaly_text = "No statistically significant revenue anomaly was detected this week."

    if driver_anomalies:
        anomalous_drivers = ", ".join(
            [
                f"{a['entity']} (Z-score: {round(a['z_score'], 2)})"
                for a in driver_anomalies
            ]
        )
    else:
        anomalous_drivers = "None"

    # -------------------- FINAL PROMPT --------------------
    prompt = f"""
You are a Business Development and Commercial Strategy leader with 30+ years of experience
in retail and consumer goods. You have owned P&Ls, led market turnarounds, managed channel
restructuring, and made capital allocation decisions under pressure.

You think like a decision-maker, not an analyst.
You prioritize actions based on commercial impact, urgency, and feasibility.

Rules:
- Do NOT restate data unless it supports a decision.
- Do NOT invent data or assumptions.
- Avoid generic advice (e.g., "analyze further", "monitor closely").
- Avoid recommending blanket discounting unless promotion data supports it.
- Tie recommendations to revenue recovery, demand stabilization, cost control, or risk mitigation.
- Be concise, direct, and pragmatic.
- Base all judgments strictly on the data provided.

Context:
- Industry: Retail
- Review cadence: Weekly performance review
- Audience: Business leadership
- Analysis week: {analysis_week}

Performance Snapshot:
- Overall revenue changed by {round(overall['wow_pct'], 1)}% week-over-week.
- Trend direction: {overall['direction']} ({overall['severity']}).

Regional Performance:
- Best performing region: {top_country_pos['Country']} ({round(top_country_pos['wow_pct'], 1)}%).
- Worst performing region: {top_country_neg['Country']} ({round(top_country_neg['wow_pct'], 1)}%).

Channel Performance:
- {channel_summary}

Demand & Pricing Signals:
- Units sold change: {round(unit_price['units_change_pct'], 1)}%.
- Average price change: {round(unit_price['price_change_pct'], 1)}%.

Promotion Impact:
- {promo_summary}

Anomaly Assessment (Statistical Validation):
- Z-score explanation: A Z-score shows how unusual this week’s change is compared to normal history — values beyond ±2 indicate movement that is unlikely to be normal fluctuation.
- {anomaly_text}
- Statistically significant drivers: {anomalous_drivers}

Decision Lens:
- Leadership can act on only TWO initiatives in the next two weeks.
- Capital and execution bandwidth are constrained.
- The primary objective is to stabilize revenue decline before pursuing growth.

Your task:
1. Write a 2–3 sentence executive judgment summarizing the business situation.
2. Provide 3–4 sharply prioritized insights explaining WHY performance deteriorated.
3. Provide EXACTLY two business actions:
   - One immediate stabilization action (next 1–2 weeks)
   - One medium-term corrective action (next 4–8 weeks)
4. Explicitly state ONE material risk if no action is taken.
5. Keep tone decisive, commercial, and leadership-oriented.

CEO Question (answer explicitly):
"If I approve only ONE action this week, what should it be and why?"
"""

    return prompt


# =========================================================
# AI Summary Generator
# =========================================================
def generate_ai_summary(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
