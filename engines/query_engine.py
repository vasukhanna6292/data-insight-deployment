# engines/query_engine.py

import json
import pandas as pd
import numpy as np
from openai import OpenAI
import os

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


from engines.trend_engine import (
    overall_revenue_trend,
    country_trends,
    channel_trends,
    promotion_trend,
    unit_price_trend
)
from engines.anomaly_engine import run_anomaly_engine

# ============================================================
# OpenAI Client
# ============================================================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# JSON Sanitizer Helper (for Timestamp handling)
# ============================================================
def sanitize_for_json(obj):
    """
    Convert pandas/numpy objects to JSON-serializable types.
    Handles Timestamps, numpy types, DataFrames, Series, etc.
    """
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        result = {}
        for k, v in obj.items():
            key_str = k.isoformat() if isinstance(k, pd.Timestamp) else str(k)
            result[key_str] = sanitize_for_json(v)
        return result
    elif isinstance(obj, pd.DataFrame):
        return json.loads(obj.to_json(orient='records', date_format='iso'))
    elif isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif pd.isna(obj):
        return None
    else:
        return obj


# ============================================================
# Query Capabilities Definition
# ============================================================
QUERY_CAPABILITIES = {
    "regional_performance": {
        "examples": [
            "Which region performed best?",
            "Show me country performance",
            "What's the top performing country?"
        ],
        "function": "country_trends",
        "data_source": "weekly_df"
    },
    "channel_performance": {
        "examples": [
            "Which channel is growing fastest?",
            "Compare online vs retail performance",
            "Show channel breakdown"
        ],
        "function": "channel_trends",
        "data_source": "weekly_df"
    },
    "revenue_trend": {
        "examples": [
            "What's the revenue trend?",
            "Is revenue growing or declining?",
            "Show me week over week change"
        ],
        "function": "overall_revenue_trend",
        "data_source": "weekly_total"
    },
    "anomaly_detection": {
        "examples": [
            "Are there any anomalies?",
            "Which regions show unusual behavior?",
            "Detect outliers"
        ],
        "function": "run_anomaly_engine",
        "data_source": "weekly_df"
    },
    "promotion_impact": {
        "examples": [
            "How are promotions performing?",
            "Show me promo effectiveness",
            "Compare promoted vs non-promoted sales"
        ],
        "function": "promotion_trend",
        "data_source": "clean_df"
    },
    "price_demand": {
        "examples": [
            "What's happening with pricing?",
            "Show unit price trends",
            "Is demand increasing?"
        ],
        "function": "unit_price_trend",
        "data_source": "weekly_df"
    },
    "custom_exploration": {
        "examples": [
            "Average revenue by store",
            "Top 5 SKUs by margin",
            "Sales where discount > 20%",
            "Total revenue from Walmart stores"
        ],
        "function": "execute_custom_query",
        "data_source": "clean_df"
    }
}


# ============================================================
# Intent Classifier (ENHANCED)
# ============================================================
def classify_query_intent(user_query: str) -> dict:
    """
    Uses GPT-4o-mini to classify user intent and extract parameters.
    NOW SUPPORTS CUSTOM EXPLORATION QUERIES.
    
    Returns:
        {
            "query_type": "regional_performance" or "custom_exploration",
            "filters": {...},
            "confidence": 0.95,
            "requires_calculation": false
        }
    """
    
    capabilities_summary = "\n".join([
        f"- {key}: {', '.join(val['examples'][:2])}"
        for key, val in QUERY_CAPABILITIES.items()
    ])
    
    prompt = f"""You are a query intent classifier for a retail sales analytics system.

Available query types:
{capabilities_summary}

IMPORTANT: Choose "custom_exploration" when the query asks for:
- Custom aggregations (average, sum, count by specific dimension)
- Filtering by specific values (discount > X, specific store, specific SKU)
- Top N queries (top 5, bottom 10, etc.)
- Custom calculations not covered by pre-built analytics
- Specific data inspection or drill-downs

User query: "{user_query}"

Analyze the query and return a JSON object with:
1. "query_type": The most relevant capability (use exact keys from above)
2. "filters": Any specific filters mentioned (time_period, entity name, threshold values)
3. "confidence": Your confidence level (0.0 to 1.0)
4. "requires_calculation": true if custom calculation needed (true for custom_exploration)

Examples:
- "Which region performed best?" → regional_performance
- "Average revenue by country" → custom_exploration
- "Show me sales where discount > 30%" → custom_exploration
- "Top 5 stores by revenue" → custom_exploration

Respond ONLY with valid JSON, no other text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)


# ============================================================
# Custom Query Execution (NEW!)
# ============================================================
def generate_pandas_query(user_query: str, df_info: dict) -> str:
    """
    Generate safe Pandas code for custom data exploration.
    
    Args:
        user_query: Natural language query
        df_info: Schema information (columns, dtypes, sample data)
    
    Returns:
        Safe pandas code as string
    """
    
    prompt = f"""You are a data analyst generating Pandas code for retail sales analysis.

Dataset Information:
Columns: {df_info['columns']}
Data Types: {json.dumps(df_info['dtypes'], indent=2)}

User Query: "{user_query}"

Generate SAFE Python code that:
1. Uses ONLY the DataFrame variable 'df' (already defined)
2. Uses ONLY pandas (pd) and numpy (np) operations
3. Returns a result (DataFrame, Series, or scalar) - DO NOT use print()
4. ALLOWED operations: filter [], query(), groupby(), agg(), mean(), sum(), count(), min(), max(), sort_values(), head(), tail(), describe(), value_counts(), unique(), nunique()
5. FORBIDDEN: import, exec, eval, open, file, os, sys, subprocess, __builtins__, compile

Return ONLY the Python code (one line or multiple lines), no explanations, no markdown.

Examples:
Query: "Average revenue by country"
Code: df.groupby('Country')['Revenue'].mean().sort_values(ascending=False)

Query: "Top 5 stores by total revenue"
Code: df.groupby('Store')['Revenue'].sum().sort_values(ascending=False).head(5)

Query: "Sales where discount greater than 30%"
Code: df[df['Discount'] > 0.3][['Store', 'Country', 'Revenue', 'Discount']].sort_values('Revenue', ascending=False)

Query: "Total revenue from Walmart stores"
Code: df[df['Store'] == 'Walmart']['Revenue'].sum()

Your code:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    code = response.choices[0].message.content.strip()
    
    # Clean markdown formatting if present
    code = code.replace("```python", "").replace("```", "").strip()
    
    return code


def execute_custom_query(user_query: str, clean_df, weekly_df) -> dict:
    """
    Execute custom data exploration queries using AI-generated Pandas code.
    FIXED: Properly handles Timestamp serialization.
    
    Returns:
        {
            "success": True/False,
            "query_type": "custom_exploration",
            "data": [...],
            "code_generated": "df.groupby(...)...",
            "metadata": {...}
        }
    """
    
    # Provide dataset schema info to AI
    df_info = {
        "columns": clean_df.columns.tolist(),
        "dtypes": {col: str(dtype) for col, dtype in clean_df.dtypes.items()},
        "row_count": len(clean_df)
    }
    
    try:
        print(f"🔍 Generating pandas code for: {user_query}")
        
        # Step 1: Generate pandas code
        pandas_code = generate_pandas_query(user_query, df_info)
        
        print(f"📝 Generated code: {pandas_code}")
        
        # Step 2: Security validation
        dangerous_patterns = [
            'import ', 'exec(', 'eval(', '__', 'open(', 'file(',
            'os.', 'sys.', 'subprocess', 'requests.', 'urllib',
            'compile(', 'globals(', 'locals(', 'vars(', 'dir(',
            '__builtins__', 'getattr', 'setattr', 'delattr'
        ]
        
        code_lower = pandas_code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return {
                    "success": False,
                    "query_type": "custom_exploration",
                    "error": f"Security: Query contains forbidden operation '{pattern}'",
                    "code_generated": pandas_code
                }
        
        # Step 3: Execute in restricted namespace
        namespace = {
            'df': clean_df,
            'pd': pd,
            'np': np
        }
        
        # Execute the code
        result = eval(pandas_code, {"__builtins__": {}}, namespace)
        
        print(f"✅ Code executed successfully. Result type: {type(result)}")
        
        # Step 4: Convert result to JSON-serializable format using sanitizer
        if isinstance(result, pd.DataFrame):
            # Limit to top 50 rows for performance
            result_limited = result.head(50)
            result_data = sanitize_for_json(result_limited)
            result_type = "dataframe"
            result_shape = f"{len(result)} rows × {len(result.columns)} columns"
            
        elif isinstance(result, pd.Series):
            # Limit to top 50 entries
            result_limited = result.head(50)
            result_data = sanitize_for_json(result_limited)
            result_type = "series"
            result_shape = f"{len(result)} entries"
            
        elif isinstance(result, (int, float, np.integer, np.floating)):
            result_data = float(result)
            result_type = "scalar"
            result_shape = "single value"
            
        elif isinstance(result, pd.Timestamp):
            result_data = result.isoformat()
            result_type = "timestamp"
            result_shape = "date/time"
            
        elif isinstance(result, str):
            result_data = result
            result_type = "string"
            result_shape = "text"
            
        else:
            result_data = sanitize_for_json(result)
            result_type = "other"
            result_shape = "converted"
        
        return {
            "success": True,
            "query_type": "custom_exploration",
            "data": result_data,
            "code_generated": pandas_code,
            "metadata": {
                "result_type": result_type,
                "result_shape": result_shape,
                "calculation_performed": True
            }
        }
        
    except Exception as e:
        print(f"❌ Custom query execution failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        return {
            "success": False,
            "query_type": "custom_exploration",
            "error": f"Execution error: {str(e)}",
            "code_generated": pandas_code if 'pandas_code' in locals() else None,
            "metadata": {
                "error_type": type(e).__name__
            }
        }


# ============================================================
# Query Router (ENHANCED)
# ============================================================
def execute_query(intent: dict, clean_df, weekly_df, weekly_total) -> dict:
    """
    Routes the query to appropriate analytics function.
    NOW SUPPORTS CUSTOM EXPLORATION.
    
    Returns:
        {
            "query_type": "...",
            "data": [...],
            "metadata": {...}
        }
    """
    
    query_type = intent["query_type"]
    filters = intent.get("filters", {})
    user_query = intent.get("original_query", "")
    
    # Route to pre-computed analytics
    if query_type == "regional_performance":
        data = country_trends(weekly_df)
        
        # Apply filters if specific country mentioned
        if filters.get("entity"):
            entity = filters["entity"].lower()
            data = [d for d in data if entity in d["Country"].lower()]
        
        return {
            "success": True,
            "query_type": query_type,
            "data": data,
            "metadata": {
                "total_regions": len(data),
                "metric": "Revenue WoW%"
            }
        }
    
    elif query_type == "channel_performance":
        data = channel_trends(weekly_df)
        return {
            "success": True,
            "query_type": query_type,
            "data": data,
            "metadata": {
                "total_channels": len(data),
                "metric": "Revenue WoW%"
            }
        }
    
    elif query_type == "revenue_trend":
        data = overall_revenue_trend(weekly_total)
        return {
            "success": True,
            "query_type": query_type,
            "data": data,
            "metadata": {
                "trend_direction": data["direction"],
                "severity": data["severity"]
            }
        }
    
    elif query_type == "anomaly_detection":
        data = run_anomaly_engine(weekly_total, weekly_df)
        return {
            "success": True,
            "query_type": query_type,
            "data": data,
            "metadata": {
                "overall_anomaly": data["overall_anomaly"]["is_anomaly"],
                "driver_anomalies_count": len(data["driver_anomalies"])
            }
        }
    
    elif query_type == "promotion_impact":
        data = promotion_trend(clean_df)
        return {
            "success": True,
            "query_type": query_type,
            "data": data,
            "metadata": {
                "promotions_analyzed": len(data)
            }
        }
    
    elif query_type == "price_demand":
        data = unit_price_trend(weekly_df)
        return {
            "success": True,
            "query_type": query_type,
            "data": data,
            "metadata": {
                "units_trend": data["units_change_pct"],
                "price_trend": data["price_change_pct"]
            }
        }
    
    # NEW: Handle custom exploration queries
    elif query_type == "custom_exploration":
        return execute_custom_query(
            user_query=user_query,
            clean_df=clean_df,
            weekly_df=weekly_df
        )
    
    else:
        return {
            "success": False,
            "query_type": "unknown",
            "data": None,
            "metadata": {"error": "Query type not supported"}
        }


# ============================================================
# Response Generator (ENHANCED)
# ============================================================
def generate_natural_response(user_query: str, query_result: dict) -> dict:
    """
    Generates natural language response with visualization suggestion.
    NOW HANDLES CUSTOM QUERY RESULTS.
    
    Returns:
        {
            "answer": "...",
            "chart_suggestion": "bar",
            "key_insights": ["..."],
            "follow_up_questions": ["..."]
        }
    """
    
    # Handle failed queries
    if not query_result.get("success", True):
        return {
            "answer": f"I couldn't process that query. {query_result.get('error', 'Unknown error')}",
            "key_insights": ["Query execution failed"],
            "chart_suggestion": "none",
            "follow_up_questions": [
                "Try asking about regional performance",
                "Or ask about channel trends"
            ]
        }
    
    prompt = f"""You are a senior business analyst presenting data insights.

User asked: "{user_query}"

Query type: {query_result.get('query_type')}

Analysis results:
{json.dumps(query_result, indent=2, default=str)[:3000]}

Generate a response with:
1. A clear, concise answer (2-3 sentences max) that directly addresses the user's question
2. Key numbers and entities mentioned (3-5 bullet points)
3. Business context (why this matters to the business)
4. Suggested chart type: 
   - "bar" for comparisons between categories
   - "line" for trends over time
   - "table" for detailed data lists
   - "metric_card" for single values
   - "none" if no visualization needed
5. 2-3 relevant follow-up questions the user might ask

For custom exploration queries, focus on the calculated results and their business implications.

Respond in JSON format:
{{
    "answer": "Based on the analysis, ...",
    "key_insights": ["Insight 1 with specific numbers", "Insight 2", "Insight 3"],
    "chart_suggestion": "bar",
    "follow_up_questions": ["Related question 1?", "Related question 2?", "Related question 3?"]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)


# ============================================================
# Master Query Handler (ENHANCED)
# ============================================================
def process_natural_language_query(
    user_query: str,
    clean_df,
    weekly_df,
    weekly_total
) -> dict:
    """
    Main orchestrator for natural language queries.
    NOW SUPPORTS BOTH PRE-COMPUTED AND CUSTOM QUERIES.
    
    Returns complete response with data and formatted answer.
    """
    
    print(f"\n{'='*60}")
    print(f"Processing query: {user_query}")
    print(f"{'='*60}")
    
    # Step 1: Classify intent
    intent = classify_query_intent(user_query)
    intent["original_query"] = user_query  # Store for custom queries
    
    print(f"✅ Intent classified: {intent['query_type']} (confidence: {intent.get('confidence', 'N/A')})")
    
    # Step 2: Execute query
    query_result = execute_query(intent, clean_df, weekly_df, weekly_total)
    
    if query_result.get("success", True):
        print(f"✅ Query executed successfully")
    else:
        print(f"❌ Query execution failed: {query_result.get('error')}")
    
    # Step 3: Generate natural response
    nl_response = generate_natural_response(user_query, query_result)
    
    print(f"✅ Natural language response generated")
    print(f"{'='*60}\n")
    
    # Step 4: Combine everything
    return {
        "user_query": user_query,
        "intent": intent,
        "answer": nl_response["answer"],
        "key_insights": nl_response["key_insights"],
        "data": query_result.get("data"),
        "chart_suggestion": nl_response["chart_suggestion"],
        "follow_up_questions": nl_response.get("follow_up_questions", []),
        "metadata": query_result.get("metadata", {}),
        "code_generated": query_result.get("code_generated"),  # Show generated code for transparency
        "success": query_result.get("success", True)
    }
