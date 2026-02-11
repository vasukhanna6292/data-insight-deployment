from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import pandas as pd
import traceback
import numpy as np
import math

from engines.prep_engine import prepare_data
from engines.trend_engine import run_trend_engine
from engines.anomaly_engine import run_anomaly_engine
from engines.query_engine import process_natural_language_query
from ai.ai_summary import build_ai_prompt, generate_ai_summary

router = APIRouter()


# =====================================================
# JSON Sanitizer (CRITICAL FOR FASTAPI)
# Handles NumPy, Pandas, NaN, Inf
# =====================================================
def to_native(obj):
    """
    Recursively convert NumPy / Pandas scalars and invalid floats
    (NaN, Inf) into JSON-safe Python types.
    """
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [to_native(v) for v in obj]

    # NumPy scalar → Python scalar
    if isinstance(obj, np.generic):
        obj = obj.item()

    # JSON does NOT allow NaN / Inf
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None

    return obj


@router.post("/full")
async def run_full_review(file: UploadFile = File(...)):
    try:
        # =====================================================
        # 1. Load CSV
        # =====================================================
        df = pd.read_csv(file.file)

        print("✅ CSV loaded successfully")
        print("Columns:", df.columns.tolist())
        print(df.head(2))

        # =====================================================
        # 2. Canonical Data Prep
        # =====================================================
        clean_df, weekly_df, weekly_total, analysis_week = prepare_data(df)

        print("✅ Data preparation successful")
        print("Weeks available:", weekly_total["week"].tolist())

        analysis_week = str(weekly_total.iloc[-1]["week"])

        # =====================================================
        # 3. Deterministic Engines
        # =====================================================
        trend_results = run_trend_engine(
            df=clean_df,
            weekly_df=weekly_df,
            weekly_total=weekly_total
        )

        print("✅ Trend engine executed")

        anomaly_results = run_anomaly_engine(
            weekly_total=weekly_total,
            weekly_df=weekly_df
        )

        print("✅ Anomaly engine executed")

        # =====================================================
        # 4. AI Executive Summary (FAULT-TOLERANT)
        # =====================================================
        try:
            prompt = build_ai_prompt(
                trend_results=trend_results,
                anomaly_results=anomaly_results,
                analysis_week=analysis_week
            )

            executive_summary = generate_ai_summary(prompt)
            print("🧠 AI summary generated")

        except Exception as ai_error:
            print("⚠️ AI SUMMARY FAILED — FALLING BACK")
            print(str(ai_error))

            executive_summary = (
                "Executive summary could not be generated due to an AI service issue. "
                "All deterministic analytics and signals are valid."
            )

        # =====================================================
        # 5. LOCKED & JSON-SAFE API RESPONSE
        # =====================================================
        response = {
            "analysis_week": analysis_week,
            "metrics": trend_results["overall_revenue_trend"],
            "trends": {
                **trend_results,
                "weekly_total": weekly_total.to_dict("records")
            },
            "anomalies": anomaly_results,
            "executive_summary": executive_summary
        }

        # 🔐 FINAL SANITIZATION STEP
        return to_native(response)

    except Exception as e:
        print("❌ FATAL ERROR IN /review/full")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# NEW ENDPOINT: Natural Language Query
# =====================================================
@router.post("/query")
async def natural_language_query(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    """
    Endpoint for natural language queries.
    
    Example:
    - "Which region performed best?"
    - "Show me channel trends"
    - "Are there any anomalies?"
    """
    try:
        print(f"📝 Received query: {query}")
        
        # =====================================================
        # 1. Load and Prepare Data
        # =====================================================
        df = pd.read_csv(file.file)
        clean_df, weekly_df, weekly_total, analysis_week = prepare_data(df)
        
        print("✅ Data prepared for query")
        
        # =====================================================
        # 2. Process Natural Language Query
        # =====================================================
        result = process_natural_language_query(
            user_query=query,
            clean_df=clean_df,
            weekly_df=weekly_df,
            weekly_total=weekly_total
        )
        
        print("✅ Query processed successfully")
        
        # =====================================================
        # 3. Return Sanitized Response
        # =====================================================
        return to_native(result)
        
    except Exception as e:
        print("❌ FATAL ERROR IN /review/query")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
