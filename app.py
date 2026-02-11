# app.py - PREMIUM ENTERPRISE UI

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import io
import os
from datetime import datetime

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
# Custom CSS - Premium Enterprise Design
# -----------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Content Container with Glassmorphism */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Header Styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    h2 {
        color: #2D3748;
        font-weight: 600;
        font-size: 1.8rem !important;
        margin-top: 2rem;
        border-left: 5px solid #667eea;
        padding-left: 1rem;
    }
    
    h3 {
        color: #4A5568;
        font-weight: 600;
        font-size: 1.3rem !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Feature Badges */
    .feature-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-badge:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4A5568;
        font-size: 1rem;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #667eea;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #E2E8F0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
        border-radius: 12px;
        font-weight: 600;
        color: #2D3748;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Success/Info/Warning Messages */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 2px solid #E2E8F0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Caption/Small Text */
    .stCaption {
        color: #718096;
        font-size: 0.95rem;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Executive Summary Card */
    .executive-summary {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #667eea;
        margin: 1.5rem 0;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 2px solid #E2E8F0;
        color: #718096;
    }
    
    /* Animation for elements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Pulse animation for important elements */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
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
    
    # API Status Indicator
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <small>🔗 API Endpoint</small><br>
        <code style='color: #10b981; font-size: 0.75rem;'>{FASTAPI_BASE_URL}</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📂 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help="Upload your sales data in CSV format"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file_content = uploaded_file.read()
        uploaded_file.seek(0)
        
        st.success("✅ File Loaded Successfully")
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
        Use `sample_sales_data.csv` from the repository
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
st.markdown("<p style='text-align: center; color: #718096; font-size: 1.2rem; margin-bottom: 2rem;'>Transform Business Data into Actionable Executive Intelligence</p>", unsafe_allow_html=True)

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
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Request Timeout")
            st.warning("Try with a smaller dataset or check your connection.")
            st.stop()
            
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot Connect to Backend")
            st.info(f"**API URL:** {FASTAPI_BASE_URL}")
            st.stop()
            
        except Exception as e:
            st.error(f"❌ Unexpected Error")
            with st.expander("🔍 Details"):
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
        <p style='font-size: 1.1rem; line-height: 1.8; color: #2D3748;'>
            {data["executive_summary"]}
        </p>
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
    
    # Update chart styling for premium look
    fig_rev.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
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
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
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
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="#2D3748")
        )
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.plotly_chart(fig_channel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Natural Language Query Section
    st.markdown("<h2>💬 Ask Questions About Your Data</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #718096; margin-bottom: 1.5rem;'>Use natural language to explore insights interactively</p>", unsafe_allow_html=True)

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
                                <h3 style='color: #667eea; margin-bottom: 1rem;'>✨ Answer</h3>
                            """, unsafe_allow_html=True)
                            st.markdown(result["answer"])
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            if result.get("code_generated"):
                                with st.expander("🔧 Generated Code"):
                                    st.code(result["code_generated"], language="python")
                            
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
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            font=dict(family="Inter")
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.dataframe(df_viz, use_container_width=True)
                                
                                elif chart_type == "table":
                                    st.dataframe(df_viz, use_container_width=True)
                            
                            if result.get("follow_up_questions"):
                                st.markdown("**💡 Related Questions:**")
                                for fq in result["follow_up_questions"]:
                                    st.markdown(f"- {fq}")
                    else:
                        st.error(f"❌ Failed to process query")
                else:
                    st.error("❌ No file uploaded")
                    
            except Exception as e:
                st.error(f"❌ Query error: {str(e)}")

    # Example Questions
    with st.expander("💡 Example Questions"):
        tab1, tab2 = st.tabs(["📊 Pre-Computed", "🔍 Custom Queries"])
        
        with tab1:
            st.markdown("""
            - Which region performed best last week?
            - Show me country performance comparison
            - Which channel is growing fastest?
            - What's the overall revenue trend?
            - Are there any anomalies in the data?
            - How are promotions performing?
            """)
        
        with tab2:
            st.markdown("""
            - Show me top 5 stores by total sales
            - What's the average revenue by country?
            - Filter sales where discount > 30%
            - Total revenue from Walmart stores
            - Average margin for Online channel only
            """)

else:
    # Landing Page
    st.markdown("""
    <div class='info-box animate-fade-in'>
        <h3 style='color: #667eea; margin-top: 0;'>👋 Welcome to AI Data-to-Insight Agent</h3>
        <p style='color: #4A5568; font-size: 1.1rem; line-height: 1.8;'>
            Upload your CSV file and click <strong>"Run Executive Review"</strong> to generate AI-powered insights.
            This tool automatically analyzes your data, detects anomalies, and provides actionable recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2>🎯 Platform Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='chart-container'>
            <h3 style='color: #667eea;'>📊 Automated Analytics</h3>
            <ul style='color: #4A5568; line-height: 2;'>
                <li>Weekly revenue trends</li>
                <li>Regional performance tracking</li>
                <li>Channel-level insights</li>
                <li>Promotion impact analysis</li>
            </ul>
            
            <h3 style='color: #667eea; margin-top: 1.5rem;'>🔍 Anomaly Detection</h3>
            <ul style='color: #4A5568; line-height: 2;'>
                <li>Z-score based detection</li>
                <li>Statistical validation</li>
                <li>Automatic alerting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='chart-container'>
            <h3 style='color: #667eea;'>💬 Natural Language Queries</h3>
            <ul style='color: #4A5568; line-height: 2;'>
                <li>Pre-computed insights</li>
                <li>Custom data exploration</li>
                <li>AI-powered code generation</li>
                <li>Interactive Q&A</li>
            </ul>
            
            <h3 style='color: #667eea; margin-top: 1.5rem;'>🧠 AI-Powered Insights</h3>
            <ul style='color: #4A5568; line-height: 2;'>
                <li>Executive summaries</li>
                <li>Business recommendations</li>
                <li>Action prioritization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <h3 style='color: #667eea; margin-bottom: 1rem;'>AI Data-to-Insight Agent</h3>
    <p style='color: #718096;'>
        Built with FastAPI, Streamlit & OpenAI GPT-4 | 
        <strong>Production-Ready Architecture</strong> | 
        Zero Infrastructure Cost
    </p>
    <p style='color: #A0AEC0; font-size: 0.9rem; margin-top: 0.5rem;'>
        🚀 Deployed on Cloud • 📊 Enterprise-Grade • 🔒 Secure by Design
    </p>
    <p style='color: #CBD5E0; font-size: 0.85rem; margin-top: 1rem;'>
        © 2026 FirstSource POC | Version 1.0
    </p>
</div>
""", unsafe_allow_html=True)
