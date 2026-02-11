# app.py

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import io

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Data-to-Insight Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Project Imports (UI ONLY)
# -----------------------------
from viz.charts import (
    plot_weekly_revenue,
    plot_country_drivers,
    plot_channel_trends
)

FASTAPI_URL_FULL = "http://127.0.0.1:8000/review/full"
FASTAPI_URL_QUERY = "http://127.0.0.1:8000/review/query"

# -----------------------------
# Initialize Session State
# -----------------------------
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if "uploaded_file_content" not in st.session_state:
    st.session_state.uploaded_file_content = None

# -----------------------------
# Header with Feature Badges
# -----------------------------
st.title("📊 AI Data-to-Insight Agent")
st.caption("Weekly Executive Performance Review (Automated)")

# Feature badges
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("✅ **Analytics Engine**")
with col2:
    st.markdown("✅ **Anomaly Detection**")
with col3:
    st.markdown("✅ **Natural Language**")
with col4:
    st.markdown("✅ **AI Insights**")

st.markdown("---")

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("📂 Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload weekly sales data (CSV)",
    type=["csv"],
    help="Upload CSV file with transaction data"
)

# Store uploaded file in session state
if uploaded_file is not None:
    # Read file content and store in session state
    st.session_state.uploaded_file_content = uploaded_file.read()
    uploaded_file.seek(0)  # Reset file pointer
    
    # Show file info
    st.sidebar.success(f"✅ File loaded: {uploaded_file.name}")
    st.sidebar.info(f"📊 Size: {len(st.session_state.uploaded_file_content) / 1024:.1f} KB")

# Sample data info
if uploaded_file is None:
    st.sidebar.info("💡 **Need test data?**")
    st.sidebar.markdown("""
    Use the synthetic data generator:
    ```bash
    python synthetic_data_generator.py \\
      --scenario growth --weeks 4 \\
      --output test_data.csv
    ```
    
    **Available scenarios:**
    - `growth`: +12% growth
    - `decline`: -8% decline  
    - `mixed`: Mixed performance
    - `promotional`: Heavy promos
    - `normal`: Baseline data
    """)

st.sidebar.markdown("---")

run_analysis = st.sidebar.button("🚀 Run Executive Review", type="primary", use_container_width=True)

# Add help section
with st.sidebar.expander("ℹ️ How to Use"):
    st.markdown("""
    **Step 1:** Upload your CSV file
    
    **Step 2:** Click "Run Executive Review"
    
    **Step 3:** View insights and charts
    
    **Step 4:** Ask natural language questions
    
    **Required CSV columns:**
    - Date, Store, Country, Channel
    - Revenue, Units Sold, etc.
    """)

# -----------------------------
# Main Execution with Enhanced Error Handling
# -----------------------------
if uploaded_file and run_analysis:

    with st.spinner("🔄 Running executive review... This may take 30-60 seconds."):
        
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            response = requests.post(
                FASTAPI_URL_FULL,
                files={"file": uploaded_file},
                timeout=300  # 2 minute timeout
            )
            
            # Check response status
            if response.status_code != 200:
                st.error("❌ Failed to process data via FastAPI.")
                
                # Show detailed error
                with st.expander("🔍 Error Details"):
                    st.code(response.text[:1000])
                
                # Troubleshooting tips
                st.error("**Troubleshooting Tips:**")
                st.markdown("""
                1. **Check if FastAPI is running:**
                   ```bash
                   uvicorn api.main:app --reload
                   ```
                
                2. **Verify your API key is set:**
                   ```bash
                   echo $env:OPENAI_API_KEY  # PowerShell
                   ```
                
                3. **Check the FastAPI terminal for error messages**
                
                4. **Try restarting both servers**
                """)
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out (exceeded 2 minutes)")
            st.warning("This might happen with very large datasets or slow API responses.")
            st.info("**Try these solutions:**")
            st.markdown("""
            - Use a smaller dataset (< 50,000 rows)
            - Check your internet connection (for OpenAI API calls)
            - Verify OpenAI API credits are available
            - Restart the FastAPI server
            """)
            st.stop()
            
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to FastAPI backend")
            st.error("**FastAPI is not running or not accessible**")
            
            st.info("**To start FastAPI:**")
            st.code("""
# In a new terminal:
cd C:\\Users\\vasuk\\OneDrive\\Desktop\\FirstSource

# Set API key (PowerShell):
$env:OPENAI_API_KEY="your-key-here"

# Start server:
python -m uvicorn api.main:app --reload
            """, language="bash")
            
            st.info("Then refresh this page and try again.")
            st.stop()
            
        except Exception as e:
            st.error(f"❌ Unexpected error occurred")
            
            with st.expander("🔍 Technical Details"):
                st.code(str(e))
            
            st.warning("**Possible causes:**")
            st.markdown("""
            - Invalid CSV format
            - Missing required columns
            - Data type issues
            - OpenAI API errors
            """)
            st.stop()

    # Store analysis data in session state
    st.session_state.analysis_data = response.json()
    st.success("✅ Analysis complete!")

# Display analysis if available in session state
if st.session_state.analysis_data is not None:
    
    data = st.session_state.analysis_data

    # =============================
    # 1. Executive Summary
    # =============================
    st.subheader("🧠 Executive Judgment")
    st.write(data["executive_summary"])

    st.markdown("---")

    # =============================
    # 2. Key Business Signals
    # =============================
    st.subheader("📌 Key Business Signals")

    overall = data["metrics"]

    col1, col2, col3 = st.columns(3)
    
    # Revenue WoW with color
    wow_pct = overall['wow_pct']
    col1.metric(
        "Revenue WoW %", 
        f"{wow_pct:+.1f}%",
        delta=f"{wow_pct:.1f}%",
        delta_color="normal"
    )
    
    # Trend direction with emoji
    direction = overall["direction"].capitalize()
    direction_emoji = "📈" if direction == "Increase" else "📉"
    col2.metric("Trend Direction", f"{direction_emoji} {direction}")
    
    # Severity with color
    severity = overall["severity"].capitalize()
    severity_emoji = "🔴" if severity == "Significant" else "🟡" if severity == "Moderate" else "🟢"
    col3.metric("Severity", f"{severity_emoji} {severity}")

    st.markdown("---")

    # =============================
    # 3. Weekly Revenue Trend
    # =============================
    st.subheader("📈 Weekly Revenue Trend")

    weekly_total_df = pd.DataFrame(
        data["trends"]["weekly_total"]
    )

    fig_rev = plot_weekly_revenue(
        weekly_total=weekly_total_df,
        anomaly_result=data["anomalies"]["overall_anomaly"]
    )

    st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("---")

    # =============================
    # 4. Performance Drivers
    # =============================
    st.subheader("🔍 Performance Drivers")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**🌍 Country-Level Impact**")
        fig_country = plot_country_drivers(
            country_trends=data["trends"]["country_trends"],
            anomaly_results=data["anomalies"]
        )
        st.plotly_chart(fig_country, use_container_width=True)

    with col_right:
        st.markdown("**📺 Channel-Level Impact**")
        fig_channel = plot_channel_trends(
            channel_trends=data["trends"]["channel_trends"]
        )
        st.plotly_chart(fig_channel, use_container_width=True)

    st.markdown("---")

    # =============================
    # 5. NATURAL LANGUAGE QUERY SECTION
    # =============================
    st.subheader("💬 Ask Questions About Your Data")
    st.caption("Try natural language queries to explore insights interactively")

    # Query input
    user_question = st.text_input(
        "Ask me anything:",
        placeholder="e.g., Which region performed best? or Show me top 5 stores by total sales",
        key="nl_query_input"
    )

    # Ask button
    col_ask, col_example = st.columns([1, 4])
    
    with col_ask:
        ask_button = st.button("🔍 Ask", key="ask_button", type="primary")

    if ask_button and user_question:
        with st.spinner("🤔 Analyzing your question..."):
            
            try:
                # Use stored file content from session state
                if st.session_state.uploaded_file_content is not None:
                    
                    # Create file-like object from stored content
                    file_bytes = io.BytesIO(st.session_state.uploaded_file_content)
                    
                    # Call query endpoint
                    query_response = requests.post(
                        FASTAPI_URL_QUERY,
                        files={"file": ("data.csv", file_bytes, "text/csv")},
                        data={"query": user_question},
                        timeout=120
                    )
                    
                    if query_response.status_code == 200:
                        result = query_response.json()
                        
                        # Check if query was successful
                        if not result.get("success", True):
                            st.error(f"❌ Query failed: {result.get('answer', 'Unknown error')}")
                        else:
                            # Display answer in a nice box
                            st.success("✨ **Answer:**")
                            st.markdown(result["answer"])
                            
                            # Show generated code if available (for custom queries)
                            if result.get("code_generated"):
                                with st.expander("🔧 Generated Code (for transparency)"):
                                    st.code(result["code_generated"], language="python")
                            
                            # Show key insights
                            if result.get("key_insights"):
                                st.markdown("**📊 Key Findings:**")
                                for insight in result["key_insights"]:
                                    st.markdown(f"- {insight}")
                            
                            # Render suggested visualization
                            chart_type = result.get("chart_suggestion")
                            data_result = result.get("data")
                            
                            if data_result and isinstance(data_result, list) and len(data_result) > 0:
                                df_viz = pd.DataFrame(data_result)
                                
                                # Smart chart rendering based on data structure
                                if chart_type == "bar":
                                    if "Country" in df_viz.columns and "wow_pct" in df_viz.columns:
                                        fig = px.bar(
                                            df_viz, 
                                            x="Country", 
                                            y="wow_pct",
                                            title="Regional Performance",
                                            labels={"wow_pct": "WoW % Change"},
                                            color="wow_pct",
                                            color_continuous_scale="RdYlGn"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                    elif "Channel" in df_viz.columns and "wow_pct" in df_viz.columns:
                                        fig = px.bar(
                                            df_viz, 
                                            x="Channel", 
                                            y="wow_pct",
                                            title="Channel Performance",
                                            labels={"wow_pct": "WoW % Change"},
                                            color="wow_pct",
                                            color_continuous_scale="RdYlGn"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        # Generic bar chart
                                        st.dataframe(df_viz, use_container_width=True)
                                
                                elif chart_type == "table":
                                    st.dataframe(df_viz, use_container_width=True)
                                
                                elif data_result and not isinstance(data_result, list):
                                    # Scalar result
                                    st.metric("Result", f"{data_result:,.2f}" if isinstance(data_result, (int, float)) else data_result)
                            
                            # Show follow-up questions as clickable suggestions
                            if result.get("follow_up_questions"):
                                st.markdown("**💡 You might also want to ask:**")
                                for fq in result["follow_up_questions"]:
                                    st.markdown(f"- {fq}")
                    else:
                        st.error(f"❌ Failed to process query (Status: {query_response.status_code})")
                        with st.expander("Error details"):
                            st.code(query_response.text[:500])
                else:
                    st.error("❌ No file data found. Please upload a file first.")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Query timed out")
                st.info("Try a simpler query or check your API connection.")
                
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to FastAPI")
                st.info("Make sure FastAPI is running: `uvicorn api.main:app --reload`")
                
            except Exception as e:
                st.error(f"❌ Query error: {str(e)}")

    # Show example queries in an expander
    with st.expander("💡 Example Questions You Can Ask"):
        
        tab1, tab2 = st.tabs(["📊 Pre-Computed Analytics", "🔍 Custom Exploration"])
        
        with tab1:
            st.markdown("""
            **Regional Performance:**
            - Which region performed best last week?
            - Show me country performance comparison
            - What's the top performing country?
            
            **Channel Performance:**
            - Which channel is growing fastest?
            - Compare online vs retail performance
            - Show channel breakdown
            
            **Revenue Trends:**
            - What's the overall revenue trend?
            - Is revenue growing or declining?
            - Show me week over week change
            
            **Anomaly Detection:**
            - Are there any anomalies in the data?
            - Which regions show unusual behavior?
            - Detect any outliers
            
            **Promotions:**
            - How are promotions performing?
            - Show me promo effectiveness
            - Compare promoted vs non-promoted sales
            
            **Pricing & Demand:**
            - What's happening with pricing?
            - Show unit price trends
            - Is demand increasing or decreasing?
            """)
        
        with tab2:
            st.markdown("""
            **Aggregations:**
            - What's the average revenue by country?
            - Calculate total revenue by channel
            - Show me average margin by store
            - What's the sum of units sold by SKU?
            
            **Top/Bottom Queries:**
            - Show me top 5 stores by total sales
            - Top 10 countries by revenue
            - Bottom 3 channels by performance
            - Which are the top 5 SKUs by margin?
            
            **Filtering:**
            - Show me sales where discount > 30%
            - Filter sales from USA only
            - Sales with margin greater than 35%
            - Show me Walmart store performance only
            
            **Specific Calculations:**
            - Total revenue from Walmart stores
            - Average discount by channel
            - How many unique stores are there?
            - What's the total revenue from Diwali Promo?
            
            **Complex Queries:**
            - Top 5 stores in USA by revenue
            - Average margin for Online channel only
            - Revenue by SKU sorted by units sold
            """)

else:
    # =============================
    # Landing Page (No Data Uploaded)
    # =============================
    
    st.info("👆 Upload a CSV file and click **Run Executive Review** to generate insights.")
    
    # Feature showcase
    st.markdown("---")
    st.subheader("🎯 What This Agent Can Do")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 **Automated Analytics**
        - Weekly revenue trends
        - Regional performance tracking
        - Channel-level insights
        - Promotion impact analysis
        
        ### 🔍 **Anomaly Detection**
        - Z-score based detection
        - Statistical validation
        - Automatic alerting
        """)
    
    with col2:
        st.markdown("""
        ### 💬 **Natural Language Queries**
        - Pre-computed insights
        - Custom data exploration
        - AI-powered code generation
        - Interactive Q&A
        
        ### 🧠 **AI-Powered Insights**
        - Executive summaries
        - Business recommendations
        - Action prioritization
        """)
    
    # Sample query showcase
    st.markdown("---")
    st.subheader("💬 Natural Language Query Feature")
    st.caption("After uploading data, you'll be able to ask questions like:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Pre-Computed Analytics:**")
        st.code("""
• Which region performed best?
• Show me channel trends
• Are there any anomalies?
• How are promotions performing?
        """)
    
    with col2:
        st.markdown("**🔍 Custom Data Exploration:**")
        st.code("""
• Top 5 stores by total sales
• Average revenue by country
• Sales where discount > 30%
• Total revenue from Walmart
        """)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>AI Data-to-Insight Agent</strong> | Built with Streamlit, FastAPI & OpenAI GPT-4</p>
    <p style='font-size: 0.9em;'>
        Features: Pre-computed Analytics • Custom Data Exploration • Anomaly Detection • Natural Language Queries
    </p>
    <p style='font-size: 0.8em; margin-top: 10px;'>
        💡 Powered by AI • 📊 Production-Ready Architecture • 🔒 Secure by Design
    </p>
</div>
""", unsafe_allow_html=True)
