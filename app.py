# app.py - REFINED PROFESSIONAL UI - PRODUCTION READY

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import io
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Data-to-Insight Agent | FirstSource",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS - Refined Professional Design
# -----------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background - Subtle Gradient */
    .stApp {
        background: linear-gradient(135deg, #e3e8f5 0%, #d4dff7 50%, #c5d6f9 100%);
        background-attachment: fixed;
    }
    
    /* Content Container - Solid White with Shadow */
    .main .block-container {
        background: #ffffff;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        max-width: 1400px;
        margin: 2rem auto;
    }
    
    /* Header Styling */
    h1 {
        color: #1a202c;
        font-weight: 800;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: #718096;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    h2 {
        color: #2D3748;
        font-weight: 700;
        font-size: 1.75rem !important;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #667eea;
    }
    
    h3 {
        color: #4A5568;
        font-weight: 600;
        font-size: 1.25rem !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1.1rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
    }
    
    /* Feature Badges */
    .feature-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        cursor: default;
    }
    
    .feature-badge:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.45);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4A5568;
        font-size: 1.05rem;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800;
        color: #667eea;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.85rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.5);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.7);
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        padding: 0.85rem 1.15rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
        outline: none;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 10px;
        font-weight: 600;
        color: #2D3748;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
    }
    
    /* Success/Info/Warning Messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 10px;
        padding: 1rem 1.25rem;
        font-weight: 500;
    }
    
    /* Divider */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #cbd5e0, transparent);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f7fafc;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        color: #4A5568;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #edf2f7;
        border-color: #cbd5e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: transparent;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        border-left: 5px solid #667eea;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .info-box h3 {
        color: #667eea;
        margin-top: 0;
        font-weight: 700;
    }
    
    .info-box p {
        color: #4A5568;
        font-size: 1.05rem;
        line-height: 1.8;
        margin: 0;
    }
    
    /* Executive Summary Card */
    .executive-summary {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-top: 5px solid #667eea;
        margin: 1.5rem 0;
    }
    
    .executive-summary p {
        font-size: 1.15rem;
        line-height: 2;
        color: #2D3748;
        font-weight: 400;
    }
    
    /* Chart Container */
    .chart-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    /* Capability Cards */
    .capability-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border-left: 4px solid #667eea;
        height: 100%;
    }
    
    .capability-card h3 {
        color: #667eea;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1.25rem;
    }
    
    .capability-card ul {
        color: #4A5568;
        line-height: 2;
        font-size: 1rem;
        padding-left: 1.5rem;
    }
    
    .capability-card li {
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2.5rem 1rem;
        margin-top: 4rem;
        border-top: 2px solid #e2e8f0;
        color: #718096;
    }
    
    .footer h3 {
        color: #2D3748;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Project Imports
# -----------------------------
from viz.charts import (
    plot_weekly_revenue,
    plot_country_drivers,
    plot_channel_trends
)

# API Configuration
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000")
FASTAPI_URL_FULL = f"{FASTAPI_BASE_URL}/review/full"
FASTAPI_URL_QUERY = f"{FASTAPI_BASE_URL}/review/query"

# -----------------------------
# Initialize Session State
# -----------------------------
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if "uploaded_file_content" not in st.session_state:
    st.session_state.uploaded_file_content = None

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### 🎯 Control Panel")
    st.markdown("---")
    
    st.markdown("### 📂 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help="Upload your sales data in CSV format"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file_content = uploaded_file.read()
        uploaded_file.seek(0)
        
        st.success("✅ File Loaded")
        file_size = len(st.session_state.uploaded_file_content) / 1024
        st.info(f"📊 Size: {file_size:.1f} KB")
    
    st.markdown("---")
    
    run_analysis = st.button("🚀 Run Executive Review", use_container_width=True)
    
    st.markdown("---")
    
    # Help Section
    with st.expander("💡 Quick Guide"):
        st.markdown("""
        **How to Use:**
        
        1️⃣ Upload CSV file  
        2️⃣ Click 'Run Executive Review'  
        3️⃣ View AI-generated insights  
        4️⃣ Ask natural language questions
        
        **Sample Data:**  
        Use `sample_sales_data.csv` from repository
        """)
    
    # About Section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **AI Data-to-Insight Agent**
        
        Version: 1.0  
        Built with: FastAPI + Streamlit  
        Powered by: OpenAI GPT-4
        
        © 2026 FirstSource POC
        """)

# -----------------------------
# Main Header
# -----------------------------
st.markdown("<h1>📊 AI Data-to-Insight Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Transform Business Data into Actionable Executive Intelligence</p>", unsafe_allow_html=True)

# Feature Badges
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='feature-badge'>✨ Analytics Engine</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='feature-badge'>🔍 Anomaly Detection</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='feature-badge'>💬 Natural Language</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='feature-badge'>🧠 AI Insights</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Main Execution
# -----------------------------
if uploaded_file and run_analysis:
    
    with st.spinner("🔄 Analyzing your data with AI... This may take 30-60 seconds"):
        
        try:
            uploaded_file.seek(0)
            
            response = requests.post(
                FASTAPI_URL_FULL,
                files={"file": uploaded_file},
                timeout=300
            )
            
            if response.status_code != 200:
                st.error("❌ Analysis Failed")
                with st.expander("🔍 Error Details"):
                    st.code(response.text[:1000])
                st.markdown("""
                **Troubleshooting:**
                - Check OpenAI API key in deployment settings
                - Verify CSV format is correct
                - Review backend logs for errors
                """)
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Request Timeout")
            st.warning("Analysis exceeded 5 minutes. Try with a smaller dataset.")
            st.stop()
            
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot Connect to Backend")
            st.info("Backend may be starting up. Wait 2-3 minutes and try again.")
            st.stop()
            
        except Exception as e:
            st.error(f"❌ Unexpected Error")
            with st.expander("🔍 Technical Details"):
                st.code(str(e))
            st.stop()

    st.session_state.analysis_data = response.json()
    st.success("✅ Analysis Complete! Scroll down to view insights.")
    st.balloons()

# -----------------------------
# Display Results
# -----------------------------
if st.session_state.analysis_data is not None:
    
    data = st.session_state.analysis_data

    # Executive Summary
    st.markdown("<h2>🧠 Executive Judgment</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='executive-summary animate-fade-in'>
        <p>{data["executive_summary"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Key Business Signals
    st.markdown("<h2>📌 Key Business Signals</h2>", unsafe_allow_html=True)
    
    overall = data["metrics"]
    
    col1, col2, col3 = st.columns(3)
    
    wow_pct = overall['wow_pct']
    col1.metric(
        "Revenue WoW", 
        f"{wow_pct:+.1f}%",
        delta=f"{wow_pct:.1f}%",
        delta_color="normal"
    )
    
    direction = overall["direction"].capitalize()
    direction_emoji = "📈" if direction == "Increase" else "📉"
    col2.metric("Trend Direction", f"{direction_emoji} {direction}")
    
    severity = overall["severity"].capitalize()
    severity_emoji = "🔴" if severity == "Significant" else "🟡" if severity == "Moderate" else "🟢"
    col3.metric("Severity Level", f"{severity_emoji} {severity}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Weekly Revenue Trend
    st.markdown("<h2>📈 Weekly Revenue Trend</h2>", unsafe_allow_html=True)
    
    weekly_total_df = pd.DataFrame(data["trends"]["weekly_total"])
    
    fig_rev = plot_weekly_revenue(
        weekly_total=weekly_total_df,
        anomaly_result=data["anomalies"]["overall_anomaly"]
    )
    
    # Chart styling
    fig_rev.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(family="Inter, sans-serif", size=12, color="#2D3748"),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter"
        )
    )
    
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig_rev, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Performance Drivers
    st.markdown("<h2>🔍 Performance Drivers</h2>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🌍 Regional Performance")
        fig_country = plot_country_drivers(
            country_trends=data["trends"]["country_trends"],
            anomaly_results=data["anomalies"]
        )
        fig_country.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family="Inter, sans-serif", color="#2D3748")
        )
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.plotly_chart(fig_country, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### 📺 Channel Performance")
        fig_channel = plot_channel_trends(
            channel_trends=data["trends"]["channel_trends"]
        )
        fig_channel.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(family="Inter, sans-serif", color="#2D3748")
        )
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.plotly_chart(fig_channel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Natural Language Query Section
    st.markdown("<h2>💬 Ask Questions About Your Data</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #718096; margin-bottom: 1.5rem; font-size: 1.05rem;'>Use natural language to explore insights interactively</p>", unsafe_allow_html=True)

    user_question = st.text_input(
        "Your Question",
        placeholder="e.g., Which region performed best? or Show me top 5 stores by revenue",
        label_visibility="collapsed"
    )

    col_ask, col_spacer = st.columns([1, 3])
    
    with col_ask:
        ask_button = st.button("🔍 Ask Question", use_container_width=True)

    if ask_button and user_question:
        with st.spinner("🤔 Analyzing your question..."):
            
            try:
                if st.session_state.uploaded_file_content is not None:
                    
                    file_bytes = io.BytesIO(st.session_state.uploaded_file_content)
                    
                    query_response = requests.post(
                        FASTAPI_URL_QUERY,
                        files={"file": ("data.csv", file_bytes, "text/csv")},
                        data={"query": user_question},
                        timeout=120
                    )
                    
                    if query_response.status_code == 200:
                        result = query_response.json()
                        
                        if not result.get("success", True):
                            st.error(f"❌ Query failed: {result.get('answer', 'Unknown error')}")
                        else:
                            st.markdown("""
                            <div class='executive-summary animate-fade-in'>
                                <h3 style='color: #667eea; margin-bottom: 1rem; font-weight: 700;'>✨ Answer</h3>
                            """, unsafe_allow_html=True)
                            st.markdown(f"<p style='font-size: 1.05rem; line-height: 1.9; color: #2D3748;'>{result['answer']}</p>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            if result.get("key_insights"):
                                st.markdown("**📊 Key Findings:**")
                                for insight in result["key_insights"]:
                                    st.markdown(f"- {insight}")
                            
                            chart_type = result.get("chart_suggestion")
                            data_result = result.get("data")
                            
                            if data_result and isinstance(data_result, list) and len(data_result) > 0:
                                df_viz = pd.DataFrame(data_result)
                                
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
                                        fig.update_layout(
                                            plot_bgcolor='#ffffff',
                                            paper_bgcolor='#ffffff',
                                            font=dict(family="Inter")
                                        )
                                        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.markdown("</div>", unsafe_allow_html=True)
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
                                        fig.update_layout(
                                            plot_bgcolor='#ffffff',
                                            paper_bgcolor='#ffffff',
                                            font=dict(family="Inter")
                                        )
                                        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                                        st.plotly_chart(fig, use_container_width=True)
                                        st.markdown("</div>", unsafe_allow_html=True)
                                    else:
                                        st.dataframe(df_viz, use_container_width=True)
                                
                                elif chart_type == "table":
                                    st.dataframe(df_viz, use_container_width=True)
                                
                                elif data_result and not isinstance(data_result, list):
                                    st.metric("Result", f"{data_result:,.2f}" if isinstance(data_result, (int, float)) else data_result)
                            
                            if result.get("follow_up_questions"):
                                st.markdown("**💡 Related Questions:**")
                                for fq in result["follow_up_questions"]:
                                    st.markdown(f"- {fq}")
                    else:
                        st.error(f"❌ Failed to process query")
                        with st.expander("Error details"):
                            st.code(query_response.text[:500])
                else:
                    st.error("❌ No file uploaded")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Query timed out")
                
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API")
                
            except Exception as e:
                st.error(f"❌ Query error: {str(e)}")

    # Example Questions
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
    # Landing Page
    st.markdown("""
    <div class='info-box animate-fade-in'>
        <h3>👋 Welcome to AI Data-to-Insight Agent</h3>
        <p>
            Upload your CSV file and click <strong>"Run Executive Review"</strong> to generate AI-powered insights.
            This tool automatically analyzes your data, detects anomalies, and provides actionable recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2>🎯 Platform Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='capability-card'>
            <h3>📊 Automated Analytics</h3>
            <ul>
                <li>Weekly revenue trends</li>
                <li>Regional performance tracking</li>
                <li>Channel-level insights</li>
                <li>Promotion impact analysis</li>
            </ul>
            
            <h3>🔍 Anomaly Detection</h3>
            <ul>
                <li>Z-score based detection</li>
                <li>Statistical validation</li>
                <li>Automatic alerting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='capability-card'>
            <h3>💬 Natural Language Queries</h3>
            <ul>
                <li>Pre-computed insights</li>
                <li>Custom data exploration</li>
                <li>AI-powered code generation</li>
                <li>Interactive Q&A</li>
            </ul>
            
            <h3>🧠 AI-Powered Insights</h3>
            <ul>
                <li>Executive summaries</li>
                <li>Business recommendations</li>
                <li>Action prioritization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <h3>AI Data-to-Insight Agent</h3>
    <p style='color: #4A5568; font-weight: 500;'>
        Built with FastAPI, Streamlit & OpenAI GPT-4 | Production-Ready Architecture
    </p>
    <p style='color: #718096; font-size: 0.95rem; margin-top: 0.75rem;'>
        🚀 Cloud Deployed • 📊 Enterprise-Grade • 🔒 Secure by Design
    </p>
    <p style='color: #A0AEC0; font-size: 0.9rem; margin-top: 1rem;'>
        © 2026 FirstSource POC | Version 1.0
    </p>
</div>
""", unsafe_allow_html=True)
