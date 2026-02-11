# app.py - Enhanced Professional UI/UX

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
    page_title="AI Data-to-Insight Agent | Enterprise Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for Professional Look
# -----------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #1a1a2e !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #16213e !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    /* Feature Badge Cards */
    .feature-badge {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .feature-badge:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #667eea;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    /* Content Cards */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #667eea !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #666 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px dashed rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Info/Success/Warning/Error Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        font-weight: 600;
        padding: 1rem 1.5rem;
        border: 1px solid #dee2e6;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #666;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    
    /* Caption */
    .caption {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        margin-top: 0.5rem !important;
    }
    
    /* Code blocks */
    code {
        background: #f8f9fa;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Animated gradient text */
    .gradient-text {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Pulse animation for metrics */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .metric-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Glass morphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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
# HERO SECTION
# -----------------------------
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 class='gradient-text' style='font-size: 3.5rem; margin-bottom: 0;'>
        AI Data-to-Insight Agent
    </h1>
    <p class='caption' style='font-size: 1.3rem; margin-top: 1rem;'>
        Transform Raw Data into Strategic Insights in Seconds
    </p>
</div>
""", unsafe_allow_html=True)

# Feature Badges with Icons
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='feature-badge'>
        <div class='feature-icon'>🚀</div>
        <div class='feature-title'>Analytics Engine</div>
        <div class='feature-desc'>Automated weekly reviews</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-badge'>
        <div class='feature-icon'>🔍</div>
        <div class='feature-title'>Anomaly Detection</div>
        <div class='feature-desc'>AI-powered insights</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-badge'>
        <div class='feature-icon'>💬</div>
        <div class='feature-title'>Natural Language</div>
        <div class='feature-desc'>Ask questions freely</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='feature-badge'>
        <div class='feature-icon'>📊</div>
        <div class='feature-title'>Visual Intelligence</div>
        <div class='feature-desc'>Interactive dashboards</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR - Enhanced Design
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0; margin-bottom: 2rem;'>
        <h2 style='color: white; font-size: 1.5rem; margin: 0;'>📂 Data Control Center</h2>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.5rem;'>
            Upload your data to begin
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help="Drag and drop your weekly sales data here",
        label_visibility="collapsed"
    )
    
    # Store uploaded file
    if uploaded_file is not None:
        st.session_state.uploaded_file_content = uploaded_file.read()
        uploaded_file.seek(0)
        
        st.markdown("""
        <div style='background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
            <p style='color: #4CAF50; font-weight: 600; margin: 0;'>✅ File Loaded Successfully</p>
        </div>
        """, unsafe_allow_html=True)
        
        # File info card
        file_size = len(st.session_state.uploaded_file_content) / 1024
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
            <p style='color: white; margin: 0; font-size: 0.9rem;'>
                📄 <strong>{uploaded_file.name}</strong><br>
                📊 Size: {file_size:.1f} KB
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main action button
    run_analysis = st.button(
        "🚀 Generate Executive Report",
        type="primary",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sample data guide
    if uploaded_file is None:
        with st.expander("💡 Need Sample Data?", expanded=False):
            st.markdown("""
            <div style='color: white; font-size: 0.85rem;'>
                <p><strong>Generate test data:</strong></p>
                <code style='background: rgba(255,255,255,0.1); color: #4CAF50; padding: 0.5rem; display: block; border-radius: 5px;'>
                python synthetic_data_generator.py --scenario growth
                </code>
                
                <p style='margin-top: 1rem;'><strong>Available scenarios:</strong></p>
                <ul style='padding-left: 1.5rem;'>
                    <li>growth: +12% trend</li>
                    <li>decline: -8% trend</li>
                    <li>mixed: Varied performance</li>
                    <li>promotional: Campaign data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # How to use guide
    with st.expander("📖 Quick Start Guide", expanded=False):
        st.markdown("""
        <div style='color: white; font-size: 0.85rem;'>
            <ol style='padding-left: 1.5rem; line-height: 1.8;'>
                <li><strong>Upload</strong> your CSV file above</li>
                <li><strong>Click</strong> "Generate Executive Report"</li>
                <li><strong>Review</strong> automated insights</li>
                <li><strong>Ask</strong> natural language questions</li>
            </ol>
            
            <p style='margin-top: 1rem;'><strong>Required columns:</strong></p>
            <ul style='padding-left: 1.5rem;'>
                <li>Date, Store, Country</li>
                <li>Channel, Revenue</li>
                <li>Units Sold, Discount</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # API status indicator
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px;'>
        <p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; margin: 0;'>
            🔗 API Endpoint<br>
            <code style='color: #4CAF50;'>{FASTAPI_BASE_URL}</code>
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# MAIN EXECUTION with Error Handling
# -----------------------------
if uploaded_file and run_analysis:
    
    # Progress indicator
    progress_placeholder = st.empty()
    
    with progress_placeholder.container():
        st.markdown("""
        <div class='content-card' style='text-align: center;'>
            <div class='feature-icon'>⚡</div>
            <h3>Processing Your Data...</h3>
            <p style='color: #666;'>This may take 30-60 seconds. Our AI is analyzing patterns, detecting anomalies, and generating insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress for UX
        import time
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("📊 Loading data...")
            elif i < 60:
                status_text.text("🔍 Detecting anomalies...")
            elif i < 90:
                status_text.text("🧠 Generating insights...")
            else:
                status_text.text("✨ Finalizing report...")
    
    try:
        uploaded_file.seek(0)
        
        response = requests.post(
            FASTAPI_URL_FULL,
            files={"file": uploaded_file},
            timeout=300
        )
        
        if response.status_code != 200:
            progress_placeholder.empty()
            st.error("❌ Analysis Failed")
            
            with st.expander("🔍 Error Details"):
                st.code(response.text[:1000])
            
            st.markdown("""
            <div class='content-card'>
                <h3>🔧 Troubleshooting Steps:</h3>
                <ol>
                    <li><strong>Verify FastAPI is running:</strong>
                        <code>uvicorn api.main:app --reload</code>
                    </li>
                    <li><strong>Check OpenAI API key:</strong>
                        <code>echo $env:OPENAI_API_KEY</code>
                    </li>
                    <li><strong>Restart both servers</strong></li>
                    <li><strong>Check FastAPI terminal for errors</strong></li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
    
    except requests.exceptions.Timeout:
        progress_placeholder.empty()
        st.error("⏱️ Request Timed Out")
        st.warning("This might happen with very large datasets or slow API responses.")
        
        st.markdown("""
        <div class='content-card'>
            <h3>💡 Solutions:</h3>
            <ul>
                <li>Use a smaller dataset (< 50,000 rows)</li>
                <li>Check internet connection</li>
                <li>Verify OpenAI API credits</li>
                <li>Restart FastAPI server</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    except requests.exceptions.ConnectionError:
        progress_placeholder.empty()
        st.error("🔌 Cannot Connect to Backend")
        
        st.markdown("""
        <div class='content-card'>
            <h3>🚀 Start FastAPI Server:</h3>
            <code style='display: block; background: #f8f9fa; padding: 1rem; border-radius: 8px;'>
            # PowerShell:<br>
            $env:OPENAI_API_KEY="your-key-here"<br>
            python -m uvicorn api.main:app --reload
            </code>
            <p style='margin-top: 1rem;'>Then refresh this page and try again.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    except Exception as e:
        progress_placeholder.empty()
        st.error("❌ Unexpected Error")
        
        with st.expander("🔍 Technical Details"):
            st.code(str(e))
        st.stop()
    
    # Clear progress and store data
    progress_placeholder.empty()
    st.session_state.analysis_data = response.json()
    
    st.success("✅ Analysis Complete!")
    time.sleep(0.5)
    st.rerun()

# -----------------------------
# DISPLAY ANALYSIS RESULTS
# -----------------------------
if st.session_state.analysis_data is not None:
    
    data = st.session_state.analysis_data
    
    # =============================
    # 1. EXECUTIVE SUMMARY
    # =============================
    st.markdown("""
    <div class='content-card'>
        <h2 style='margin-top: 0;'>🧠 Executive Intelligence Summary</h2>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea;'>
        <p style='font-size: 1.05rem; line-height: 1.8; color: #333; margin: 0;'>
            {data["executive_summary"]}
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =============================
    # 2. KEY BUSINESS SIGNALS
    # =============================
    st.markdown("""
    <div class='content-card'>
        <h2 style='margin-top: 0;'>📌 Key Performance Indicators</h2>
    """, unsafe_allow_html=True)
    
    overall = data["metrics"]
    wow_pct = overall['wow_pct']
    direction = overall["direction"].capitalize()
    severity = overall["severity"].capitalize()
    
    # KPI Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta_color = "normal" if wow_pct >= 0 else "inverse"
        st.metric(
            "Revenue Week-over-Week",
            f"{wow_pct:+.1f}%",
            delta=f"{abs(wow_pct):.1f}% {'Growth' if wow_pct > 0 else 'Decline'}",
            delta_color=delta_color
        )
    
    with col2:
        direction_emoji = "📈" if direction == "Increase" else "📉"
        st.metric(
            "Trend Direction",
            f"{direction_emoji} {direction}",
            delta=None
        )
    
    with col3:
        severity_emoji = {"Significant": "🔴", "Moderate": "🟡", "Minor": "🟢"}.get(severity, "🟢")
        st.metric(
            "Impact Severity",
            f"{severity_emoji} {severity}",
            delta=None
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =============================
    # 3. WEEKLY REVENUE TREND
    # =============================
    st.markdown("""
    <div class='content-card'>
        <h2 style='margin-top: 0;'>📈 Revenue Trajectory Analysis</h2>
        <p style='color: #666; margin-bottom: 1.5rem;'>
            Comprehensive view of weekly revenue performance with anomaly detection
        </p>
    """, unsafe_allow_html=True)
    
    weekly_total_df = pd.DataFrame(data["trends"]["weekly_total"])
    
    fig_rev = plot_weekly_revenue(
        weekly_total=weekly_total_df,
        anomaly_result=data["anomalies"]["overall_anomaly"]
    )
    
    # Enhance chart styling
    fig_rev.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=12, color="#333"),
        title=None,
        margin=dict(t=20, b=50, l=50, r=20),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_rev, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =============================
    # 4. PERFORMANCE DRIVERS
    # =============================
    st.markdown("""
    <div class='content-card'>
        <h2 style='margin-top: 0;'>🔍 Performance Deep Dive</h2>
        <p style='color: #666; margin-bottom: 1.5rem;'>
            Granular analysis of regional and channel-level performance drivers
        </p>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🌍 Regional Impact")
        fig_country = plot_country_drivers(
            country_trends=data["trends"]["country_trends"],
            anomaly_results=data["anomalies"]
        )
        fig_country.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=50, l=50, r=20)
        )
        st.plotly_chart(fig_country, use_container_width=True)
    
    with col_right:
        st.markdown("### 📺 Channel Performance")
        fig_channel = plot_channel_trends(
            channel_trends=data["trends"]["channel_trends"]
        )
        fig_channel.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=50, l=50, r=20)
        )
        st.plotly_chart(fig_channel, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =============================
    # 5. NATURAL LANGUAGE QUERY
    # =============================
    st.markdown("""
    <div class='content-card'>
        <h2 style='margin-top: 0;'>💬 Interactive Intelligence Assistant</h2>
        <p style='color: #666; margin-bottom: 1.5rem;'>
            Ask questions in plain English and get instant insights from your data
        </p>
    """, unsafe_allow_html=True)
    
    # Query input
    user_question = st.text_input(
        "What would you like to know?",
        placeholder="e.g., Which region performed best? Show me top 5 stores by revenue",
        key="nl_query_input",
        label_visibility="collapsed"
    )
    
    col_btn, col_space = st.columns([1, 3])
    with col_btn:
        ask_button = st.button("🔍 Analyze", key="ask_button", type="primary", use_container_width=True)
    
    if ask_button and user_question:
        with st.spinner("🤔 Processing your question..."):
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
                            st.error(f"❌ {result.get('answer', 'Query failed')}")
                        else:
                            # Answer display
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #4CAF5015 0%, #8BC34A15 100%); 
                                        padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4CAF50; margin: 1.5rem 0;'>
                                <p style='font-size: 1.05rem; line-height: 1.8; color: #333; margin: 0;'>
                                    <strong>✨ Answer:</strong><br><br>
                                    {result["answer"]}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Key insights
                            if result.get("key_insights"):
                                st.markdown("**📊 Key Findings:**")
                                for insight in result["key_insights"]:
                                    st.markdown(f"• {insight}")
                            
                            # Visualization
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
                                            color="wow_pct",
                                            color_continuous_scale="RdYlGn",
                                            template="plotly_white"
                                        )
                                        fig.update_layout(
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            paper_bgcolor='rgba(0,0,0,0)'
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.dataframe(df_viz, use_container_width=True)
                                elif chart_type == "table":
                                    st.dataframe(df_viz, use_container_width=True)
                            
                            # Follow-up suggestions
                            if result.get("follow_up_questions"):
                                st.markdown("**💡 You might also want to ask:**")
                                for fq in result["follow_up_questions"]:
                                    st.markdown(f"• {fq}")
                    else:
                        st.error(f"❌ Query failed (Status: {query_response.status_code})")
                else:
                    st.error("❌ No file data found. Please upload a file first.")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Example questions
    with st.expander("💡 Example Questions", expanded=False):
        tab1, tab2 = st.tabs(["📊 Pre-Computed Analytics", "🔍 Custom Queries"])
        
        with tab1:
            st.markdown("""
            <div style='font-size: 0.95rem; line-height: 1.8;'>
                <strong>Regional Performance:</strong>
                <ul>
                    <li>Which region performed best last week?</li>
                    <li>Show me country performance comparison</li>
                    <li>What's the top performing country?</li>
                </ul>
                
                <strong>Channel Performance:</strong>
                <ul>
                    <li>Which channel is growing fastest?</li>
                    <li>Compare online vs retail performance</li>
                </ul>
                
                <strong>Anomaly Detection:</strong>
                <ul>
                    <li>Are there any anomalies in the data?</li>
                    <li>Which regions show unusual behavior?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div style='font-size: 0.95rem; line-height: 1.8;'>
                <strong>Top/Bottom Analysis:</strong>
                <ul>
                    <li>Show me top 5 stores by total sales</li>
                    <li>Top 10 countries by revenue</li>
                    <li>Bottom 3 channels by performance</li>
                </ul>
                
                <strong>Filtering:</strong>
                <ul>
                    <li>Show me sales where discount > 30%</li>
                    <li>Filter sales from USA only</li>
                </ul>
                
                <strong>Complex Queries:</strong>
                <ul>
                    <li>Top 5 stores in USA by revenue</li>
                    <li>Average margin for Online channel only</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # =============================
    # LANDING PAGE (No Data)
    # =============================
    
    st.markdown("""
    <div class='content-card' style='text-align: center; padding: 3rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>📊</div>
        <h2>Ready to Transform Your Data?</h2>
        <p style='color: #666; font-size: 1.1rem; margin: 1rem 0 2rem 0;'>
            Upload your CSV file and click <strong>"Generate Executive Report"</strong> to unlock AI-powered insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("## 🎯 Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Automated Analytics
        - **Weekly revenue trends** with anomaly detection
        - **Regional performance** tracking across markets
        - **Channel-level insights** for omnichannel strategy
        - **Promotion impact** analysis with ROI metrics
        
        ### 🔍 Anomaly Detection
        - **Z-score based** statistical validation
        - **Automatic alerting** for significant deviations
        - **Root cause** identification
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Natural Language Queries
        - **Pre-computed insights** for instant answers
        - **Custom data exploration** with AI code generation
        - **Interactive Q&A** with follow-up suggestions
        - **Smart visualizations** based on query context
        
        ### 🧠 AI-Powered Insights
        - **Executive summaries** in plain English
        - **Business recommendations** with prioritization
        - **Action items** with impact assessment
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    <h3 style='margin: 0 0 1rem 0; color: #667eea;'>AI Data-to-Insight Agent</h3>
    <p style='color: #666; font-size: 1rem; margin-bottom: 1.5rem;'>
        Powered by <strong>Streamlit</strong> • <strong>FastAPI</strong> • <strong>OpenAI GPT-4</strong>
    </p>
    
    <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin: 1.5rem 0;'>
        <div style='text-align: center;'>
            <div style='font-size: 2rem;'>⚡</div>
            <div style='font-size: 0.9rem; color: #666;'>Real-time Processing</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 2rem;'>🔒</div>
            <div style='font-size: 0.9rem; color: #666;'>Enterprise Security</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 2rem;'>📈</div>
            <div style='font-size: 0.9rem; color: #666;'>Scalable Architecture</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 2rem;'>🎯</div>
            <div style='font-size: 0.9rem; color: #666;'>Actionable Insights</div>
        </div>
    </div>
    
    <p style='color: #999; font-size: 0.85rem; margin-top: 1.5rem;'>
        © 2024 Data-to-Insight Platform | Built for Enterprise Analytics
    </p>
</div>
""", unsafe_allow_html=True)
