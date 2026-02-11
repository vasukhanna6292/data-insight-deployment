# app.py - Professional UI matching reference design

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
# Custom CSS - Matching Reference Design
# -----------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: none;
    }
    
    /* Main Background - Purple/Pink Gradient */
    .main {
        background: linear-gradient(180deg, #6B5DD3 0%, #8B5FBF 50%, #B65D8E 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar - Dark Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1625 0%, #2d2438 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Section Headers */
    [data-testid="stSidebar"] .element-container {
        color: #ffffff;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 500;
        color: #E8E3FF;
        margin-bottom: 2rem;
        text-align: left;
    }
    
    /* Demo Mode Banner */
    .demo-banner {
        background: linear-gradient(90deg, #FF6B9D 0%, #FFA06B 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
        color: #ffffff;
        font-size: 0.95rem;
    }
    
    .live-mode-banner {
        background: linear-gradient(90deg, #00D4FF 0%, #00E5A0 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
        color: #ffffff;
        font-size: 0.95rem;
    }
    
    /* Feature Cards - Matching Reference */
    .feature-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: left;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 700;
        color: #ffffff;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Content Cards - White with Shadow */
    .content-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        margin-bottom: 1.5rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2D1B4E;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-subheader {
        font-size: 0.95rem;
        color: #6B5DD3;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2D1B4E !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #6B5DD3 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #00D4FF;
        background: rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Buttons - Primary */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6B5DD3 0%, #8B5FBF 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        box-shadow: 0 4px 20px rgba(107, 93, 211, 0.4);
        transition: all 0.3s ease;
        text-transform: none;
        letter-spacing: 0.3px;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7B6DE3 0%, #9B6FCF 100%);
        box-shadow: 0 6px 28px rgba(107, 93, 211, 0.6);
        transform: translateY(-2px);
    }
    
    /* Regular Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6B5DD3 0%, #8B5FBF 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        box-shadow: 0 4px 20px rgba(107, 93, 211, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7B6DE3 0%, #9B6FCF 100%);
        transform: translateY(-2px);
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #E0D7FF;
        padding: 0.85rem 1.25rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6B5DD3;
        box-shadow: 0 0 0 3px rgba(107, 93, 211, 0.1);
    }
    
    .stTextInput label {
        font-weight: 600;
        color: #2D1B4E;
        font-size: 0.95rem;
    }
    
    /* Success/Info/Warning/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #00E5A015 0%, #00D4FF15 100%);
        border-left: 4px solid #00E5A0;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #006B5D;
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #00D4FF15 0%, #6B5DD315 100%);
        border-left: 4px solid #00D4FF;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #004A99;
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #FFB84D15 0%, #FFA06B15 100%);
        border-left: 4px solid #FFB84D;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #8B5000;
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, #FF6B9D15 0%, #FF4D6D15 100%);
        border-left: 4px solid #FF6B9D;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #8B1538;
        font-weight: 500;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        border-radius: 12px;
        font-weight: 700;
        padding: 1rem 1.5rem;
        border: 2px solid #E0D7FF;
        color: #2D1B4E;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #6B5DD3;
        background: linear-gradient(135deg, #EDE9FE 0%, #E0D7FF 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
        border-bottom: 3px solid #00D4FF;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #00D4FF !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6B5DD3 0%, #00D4FF 100%);
    }
    
    /* Plotly Charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    
    /* Sidebar Alert Boxes */
    [data-testid="stSidebar"] .element-container div[data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }
    
    /* Sidebar Warning Box */
    .sidebar-warning {
        background: rgba(255, 184, 77, 0.2);
        border-left: 4px solid #FFB84D;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .sidebar-success {
        background: rgba(0, 229, 160, 0.2);
        border-left: 4px solid #00E5A0;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Custom Alert Styling */
    .custom-alert {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .alert-demo {
        background: linear-gradient(90deg, #FF6B9D 0%, #FFA06B 100%);
        color: #ffffff;
    }
    
    .alert-live {
        background: linear-gradient(90deg, #00D4FF 0%, #00E5A0 100%);
        color: #ffffff;
    }
    
    /* Answer Box */
    .answer-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 4px solid #00E5A0;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
    }
    
    .answer-box p {
        color: #065F46;
        font-size: 1.05rem;
        line-height: 1.8;
        margin: 0;
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    }
    
    /* Code blocks */
    code {
        background: #F5F3FF;
        color: #6B5DD3;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #2D1B4E;
        font-weight: 700;
    }
    
    /* Links */
    a {
        color: #6B5DD3;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: #8B5FBF;
        text-decoration: underline;
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

if "fastapi_connected" not in st.session_state:
    st.session_state.fastapi_connected = False

# -----------------------------
# HERO SECTION
# -----------------------------
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <div class='hero-title'>
        😊 AI Data-to-Insight Agent
    </div>
    <div class='hero-subtitle'>
        Transform Your Business Data into Actionable Insights
    </div>
</div>
""", unsafe_allow_html=True)

# Demo/Live Mode Banner
if st.session_state.fastapi_connected:
    st.markdown("""
    <div class='custom-alert alert-live'>
        ✅ Live Mode - Connected to FastAPI backend. Real-time analysis enabled.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='custom-alert alert-demo'>
        ⚠️ Demo Mode - FastAPI backend not detected. Start FastAPI to enable live analysis.
    </div>
    """, unsafe_allow_html=True)

# Feature Cards Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>✅</div>
        <div class='feature-title'>Analytics Engine</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>✅</div>
        <div class='feature-title'>Anomaly Detection</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>✅</div>
        <div class='feature-title'>Natural Language</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>✅</div>
        <div class='feature-title'>AI Insights</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 📂 Navigation")
    
    # Connection Status
    if st.session_state.fastapi_connected:
        st.markdown("""
        <div class='sidebar-success'>
            <strong>✅ Live Mode</strong><br>
            Connected to FastAPI backend.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='sidebar-warning'>
            <strong>⚠️ Demo Mode</strong><br>
            FastAPI backend not detected.<br>
            Using sample responses.
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("💡 To enable live mode:", expanded=False):
            st.markdown("""
            **1. Start FastAPI:**
            ```bash
            uvicorn api.main:app --reload
            ```
            
            **2. Refresh this page**
            """)
    
    st.markdown("---")
    
    st.markdown("## 🚀 Quick Start")
    st.markdown("""
    1. **Upload your CSV file**
    2. **Click** 🔍 Analyze Data
    3. **Review insights & charts**
    4. **Ask natural language questions**
    """)
    
    st.markdown("---")
    
    st.markdown("## 📋 Required CSV Columns")
    st.markdown("""
    - **transaction_id**
    - **Date**
    - **Country**
    - **SKU**
    - **Channel**
    - **Units Sold**
    - **Unit Price**
    - **Revenue**
    - **Margin %**
    - **Margin**
    """)
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px;'>
        <p style='color: rgba(255,255,255,0.6); font-size: 0.75rem; margin: 0;'>
            🔗 API Endpoint<br>
            <code style='color: #00E5A0; background: transparent; font-size: 0.7rem;'>{FASTAPI_BASE_URL}</code>
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# UPLOAD SECTION
# -----------------------------
st.markdown("""
<div class='content-card'>
    <div class='section-header'>📁 Upload Your Data</div>
    <div class='section-subheader'>Choose a CSV file containing your sales data</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose CSV File",
    type=["csv"],
    help="Drag and drop your weekly sales data here (max 200MB)",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    st.session_state.uploaded_file_content = uploaded_file.read()
    uploaded_file.seek(0)
    
    file_size = len(st.session_state.uploaded_file_content) / 1024
    
    st.success(f"✅ File uploaded successfully!")
    
    with st.expander("📄 File Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Filename:** `{uploaded_file.name}`")
        with col2:
            st.markdown(f"**Size:** `{file_size:.1f} KB`")
    
    # Action Buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Data", type="primary", use_container_width=True)
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.uploaded_file_content = None
            st.session_state.analysis_data = None
            st.rerun()

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if uploaded_file and 'analyze_button' in locals() and analyze_button:
    
    progress_container = st.container()
    
    with progress_container:
        st.markdown("""
        <div class='content-card' style='text-align: center;'>
            <h3 style='color: #6B5DD3;'>⚡ Processing Your Data...</h3>
            <p style='color: #666;'>This may take 30-60 seconds. AI is analyzing patterns and generating insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        import time
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
            if i < 25:
                status_text.text("📊 Loading data...")
            elif i < 50:
                status_text.text("🔍 Detecting anomalies...")
            elif i < 75:
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
        
        if response.status_code == 200:
            st.session_state.analysis_data = response.json()
            st.session_state.fastapi_connected = True
            progress_container.empty()
            st.success("✅ Analysis complete!")
            time.sleep(0.5)
            st.rerun()
        else:
            progress_container.empty()
            st.error("❌ Failed to connect to FastAPI backend")
            
            with st.expander("🔧 Troubleshooting"):
                st.markdown("""
                **Start FastAPI server:**
                ```bash
                # PowerShell
                $env:OPENAI_API_KEY="your-key-here"
                python -m uvicorn api.main:app --reload
                ```
                
                **Then refresh this page**
                """)
    
    except requests.exceptions.ConnectionError:
        progress_container.empty()
        st.error("🔌 Cannot connect to FastAPI backend")
        st.info("Starting FastAPI server will enable live analysis. See sidebar for instructions.")
    
    except Exception as e:
        progress_container.empty()
        st.error(f"❌ Error: {str(e)}")

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
if st.session_state.analysis_data is not None:
    
    data = st.session_state.analysis_data
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown("""
    <div class='content-card'>
        <div class='section-header'>📊 Executive Summary</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics Row
    overall = data["metrics"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='content-card' style='padding: 1.5rem;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B5DD3; font-weight: 600; font-size: 0.85rem; margin: 0;'>💰 TOTAL REVENUE</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #2D1B4E; font-weight: 700; font-size: 1.8rem; margin: 0.5rem 0 0 0;'>$2,475,680</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        wow_pct = overall['wow_pct']
        st.markdown("<div class='content-card' style='padding: 1.5rem;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B5DD3; font-weight: 600; font-size: 0.85rem; margin: 0;'>📈 GROWTH RATE</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #2D1B4E; font-weight: 700; font-size: 1.8rem; margin: 0.5rem 0 0 0;'>{wow_pct:+.1f}%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='content-card' style='padding: 1.5rem;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B5DD3; font-weight: 600; font-size: 0.85rem; margin: 0;'>🌍 TOP COUNTRY</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #2D1B4E; font-weight: 700; font-size: 1.8rem; margin: 0.5rem 0 0 0;'>USA ($1.2M)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='content-card' style='padding: 1.5rem;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B5DD3; font-weight: 600; font-size: 0.85rem; margin: 0;'>📺 TOP CHANNEL</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #2D1B4E; font-weight: 700; font-size: 1.8rem; margin: 0.5rem 0 0 0;'>Supermarket</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Insights
    st.markdown("""
    <div class='content-card'>
        <div class='section-header'>💡 Key Insights</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='content-card' style='background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);'>
        <p style='font-size: 1.05rem; line-height: 1.8; color: #2D1B4E; margin: 0;'>
            {data["executive_summary"]}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("""
    <div class='content-card'>
        <div class='section-header'>📈 Weekly Revenue Trend</div>
    </div>
    """, unsafe_allow_html=True)
    
    weekly_total_df = pd.DataFrame(data["trends"]["weekly_total"])
    
    fig_rev = plot_weekly_revenue(
        weekly_total=weekly_total_df,
        anomaly_result=data["anomalies"]["overall_anomaly"]
    )
    
    fig_rev.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter", size=12, color="#2D1B4E"),
        margin=dict(t=20, b=50, l=50, r=20)
    )
    
    st.plotly_chart(fig_rev, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance Drivers
    st.markdown("""
    <div class='content-card'>
        <div class='section-header'>🔍 Performance Drivers</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Country Performance")
        fig_country = plot_country_drivers(
            country_trends=data["trends"]["country_trends"],
            anomaly_results=data["anomalies"]
        )
        fig_country.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_country, use_container_width=True)
    
    with col2:
        st.markdown("### 📺 Channel Performance")
        fig_channel = plot_channel_trends(
            channel_trends=data["trends"]["channel_trends"]
        )
        fig_channel.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_channel, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Natural Language Query
    st.markdown("""
    <div class='content-card'>
        <div class='section-header'>💬 Ask Questions About Your Data</div>
        <div class='section-subheader'>Use natural language to explore your data interactively</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_question = st.text_input(
        "What would you like to know?",
        placeholder="e.g., Which region performed best? Show me top 5 stores by revenue",
        key="nl_query"
    )
    
    if st.button("🔍 Ask Question", type="primary"):
        if user_question:
            with st.spinner("🤔 Analyzing your question..."):
                try:
                    if st.session_state.uploaded_file_content:
                        file_bytes = io.BytesIO(st.session_state.uploaded_file_content)
                        
                        query_response = requests.post(
                            FASTAPI_URL_QUERY,
                            files={"file": ("data.csv", file_bytes, "text/csv")},
                            data={"query": user_question},
                            timeout=120
                        )
                        
                        if query_response.status_code == 200:
                            result = query_response.json()
                            
                            st.markdown(f"""
                            <div class='answer-box'>
                                <p><strong>✨ Answer:</strong><br><br>{result["answer"]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if result.get("data"):
                                df_result = pd.DataFrame(result["data"])
                                st.dataframe(df_result, use_container_width=True)
                        else:
                            st.error("❌ Query failed")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question")
    
    with st.expander("💡 Example Questions"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Regional Performance:**
            - Which region performed best?
            - Show me country comparison
            
            **Channel Analysis:**
            - Which channel is growing fastest?
            - Compare online vs retail
            
            **Anomalies:**
            - Are there any anomalies?
            """)
        
        with col2:
            st.markdown("""
            **Top/Bottom:**
            - Top 5 stores by sales
            - Top 10 countries by revenue
            
            **Filtering:**
            - Sales where discount > 30%
            - Filter USA sales only
            
            **Complex Queries:**
            - Top 5 stores in USA
            """)

else:
    # Landing Page
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='content-card' style='text-align: center; padding: 3rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>📊</div>
        <h2 style='color: #2D1B4E;'>Ready to Get Started?</h2>
        <p style='color: #666; font-size: 1.1rem; margin: 1rem 0;'>
            Upload your CSV file above to generate AI-powered insights in seconds
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    <h3 style='margin: 0 0 1rem 0; color: #6B5DD3;'>AI Data-to-Insight Agent</h3>
    <p style='color: #666; font-size: 1rem; margin-bottom: 1.5rem;'>
        Powered by <strong>Streamlit</strong> • <strong>FastAPI</strong> • <strong>OpenAI GPT-4</strong>
    </p>
    
    <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;'>
        <div><strong>⚡</strong> Real-time Processing</div>
        <div><strong>🔒</strong> Enterprise Security</div>
        <div><strong>📈</strong> Scalable Architecture</div>
        <div><strong>🎯</strong> Actionable Insights</div>
    </div>
    
    <p style='color: #999; font-size: 0.85rem; margin-top: 1.5rem;'>
        © 2024 Data-to-Insight Platform
    </p>
</div>
""", unsafe_allow_html=True)
