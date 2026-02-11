import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="AI Data Insight Agent | Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bandcamp-Inspired Premium Theme CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Background - Bandcamp Gradient */
    .stApp {
        background: linear-gradient(135deg, #1a0a2e 0%, #6a1b4d 25%, #c2185b 50%, #ff6f00 75%, #ff8f00 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar Styling - Dark Like Bandcamp */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0221 0%, #1a0a2e 100%);
        border-right: 2px solid rgba(138, 43, 226, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00d9ff !important;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        background: rgba(13, 2, 33, 0.8);
        border: 2px solid #00d9ff;
        border-radius: 12px;
        padding: 20px;
    }
    
    [data-testid="stFileUploader"] label {
        color: #00d9ff !important;
        font-weight: 600;
        font-size: 16px;
    }
    
    /* Main Content Containers */
    .main-container {
        background: rgba(13, 2, 33, 0.85);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(138, 43, 226, 0.4);
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Headers - Vibrant Like Bandcamp */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 30px rgba(255, 111, 0, 0.6);
        margin-bottom: 30px !important;
        background: linear-gradient(90deg, #ff6f00, #00d9ff, #c2185b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        color: #00d9ff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 30px !important;
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.4);
    }
    
    h3 {
        color: #ff6f00 !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        text-shadow: 0 0 15px rgba(255, 111, 0, 0.4);
    }
    
    /* Metric Cards - Dark with Vibrant Accents */
    .metric-card {
        background: linear-gradient(135deg, rgba(13, 2, 33, 0.95) 0%, rgba(26, 10, 46, 0.95) 100%);
        border: 2px solid #00d9ff;
        border-radius: 16px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 217, 255, 0.5);
        border-color: #ff6f00;
    }
    
    .metric-label {
        color: #00d9ff;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }
    
    .metric-delta {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 8px;
    }
    
    /* Buttons - Teal/Cyan Like Bandcamp */
    .stButton > button {
        background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%) !important;
        color: #0d0221 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 15px 40px !important;
        border-radius: 12px !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 6px 24px rgba(0, 217, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff6f00 0%, #ff8f00 100%) !important;
        color: #ffffff !important;
        transform: translateY(-3px);
        box-shadow: 0 12px 36px rgba(255, 111, 0, 0.6) !important;
    }
    
    /* Text Input Fields */
    .stTextInput > div > div > input {
        background: rgba(13, 2, 33, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid #00d9ff !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6f00 !important;
        box-shadow: 0 0 20px rgba(255, 111, 0, 0.4) !important;
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(13, 2, 33, 0.9);
        border: 2px solid rgba(138, 43, 226, 0.5);
        border-radius: 16px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.3);
    }
    
    /* Executive Summary Box */
    .executive-summary {
        background: linear-gradient(135deg, rgba(26, 10, 46, 0.95) 0%, rgba(106, 27, 77, 0.95) 100%);
        border: 2px solid #ff6f00;
        border-radius: 16px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 8px 32px rgba(255, 111, 0, 0.4);
    }
    
    .executive-summary p {
        color: #ffffff !important;
        font-size: 1.15rem !important;
        line-height: 1.8 !important;
        font-weight: 500 !important;
    }
    
    /* Signal Cards */
    .signal-card {
        background: linear-gradient(135deg, rgba(13, 2, 33, 0.95) 0%, rgba(26, 10, 46, 0.95) 100%);
        border-left: 5px solid #00d9ff;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 217, 255, 0.2);
    }
    
    .signal-card h4 {
        color: #00d9ff !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }
    
    .signal-card p {
        color: #ffffff !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(13, 2, 33, 0.9) !important;
        border: 2px solid #00d9ff !important;
        border-radius: 12px !important;
        color: #00d9ff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(26, 10, 46, 0.95) !important;
        border-color: #ff6f00 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(13, 2, 33, 0.8);
        border-radius: 12px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 2px solid rgba(0, 217, 255, 0.3);
        color: #00d9ff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
        color: #0d0221;
        border-color: #00d9ff;
    }
    
    /* Regular Text */
    p, li, span {
        color: #ffffff !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
    }
    
    /* Success/Error/Info Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(13, 2, 33, 0.9) !important;
        border-radius: 12px !important;
        border-left: 5px solid #00d9ff !important;
        color: #ffffff !important;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(0, 217, 255, 0.3) !important;
        margin: 30px 0 !important;
    }
    
    /* Footer */
    .footer {
        background: rgba(13, 2, 33, 0.95);
        border-top: 2px solid rgba(0, 217, 255, 0.3);
        border-radius: 16px;
        padding: 25px;
        margin-top: 50px;
        text-align: center;
    }
    
    .footer p {
        color: #00d9ff !important;
        font-size: 0.95rem !important;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #00d9ff !important;
        border-right-color: #ff6f00 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'uploaded_file_data' not in st.session_state:
    st.session_state.uploaded_file_data = None

# ===========================
# SIDEBAR
# ===========================
with st.sidebar:
    st.markdown("# 📊 DATA INSIGHT")
    st.markdown("### Executive Analytics Platform")
    st.markdown("---")
    
    # File Upload
    uploaded_file = st.file_uploader(
        "Upload Sales Data (CSV)",
        type=['csv'],
        help="Upload your sales data CSV file for analysis"
    )
    
    if uploaded_file:
        st.session_state.uploaded_file_data = uploaded_file.getvalue()
        df = pd.read_csv(BytesIO(st.session_state.uploaded_file_data))
        st.success(f"✅ Loaded: {len(df):,} rows")
        
        with st.expander("📋 Data Preview"):
            st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("📁 No data uploaded")
        st.markdown("**Sample Data Available:**")
        st.markdown("- 8 weeks of sales data")
        st.markdown("- 5 countries")
        st.markdown("- 3 channels")
        st.markdown("- ~20K transactions")
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Actions")
    st.markdown("1. Upload CSV data")
    st.markdown("2. Run Executive Review")
    st.markdown("3. Ask questions")
    st.markdown("4. Explore insights")

# ===========================
# MAIN CONTENT
# ===========================

# Landing Page
if not uploaded_file:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("# 🚀 AI DATA-TO-INSIGHT AGENT")
    st.markdown("## Your Executive Intelligence Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📊 ANALYTICS</div>
            <h3 style="color: #00d9ff;">Automated Insights</h3>
            <p>Weekly performance review with AI-powered analysis and trend detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🤖 AI POWERED</div>
            <h3 style="color: #ff6f00;">Natural Language</h3>
            <p>Ask questions in plain English and get instant, intelligent answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">⚡ REAL-TIME</div>
            <h3 style="color: #c2185b;">Live Processing</h3>
            <p>Upload data and get executive-ready insights in seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Platform Capabilities")
    
    cap1, cap2 = st.columns(2)
    
    with cap1:
        st.markdown("### 📈 Automated Analysis")
        st.markdown("- Week-over-week revenue trends")
        st.markdown("- Regional performance breakdown")
        st.markdown("- Channel effectiveness analysis")
        st.markdown("- Anomaly detection & alerts")
        st.markdown("- Promotion impact assessment")
    
    with cap2:
        st.markdown("### 💬 Interactive Q&A")
        st.markdown("- Natural language queries")
        st.markdown("- Custom data exploration")
        st.markdown("- On-demand visualizations")
        st.markdown("- Drill-down analytics")
        st.markdown("- Export-ready insights")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>AI Data-to-Insight Agent</strong> | Powered by GPT-4 & FastAPI</p>
        <p>© 2026 FirstSource PoC | Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ===========================
# EXECUTIVE REVIEW SECTION
# ===========================
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown("# 📊 EXECUTIVE REVIEW")
st.markdown("## Weekly Performance Dashboard")

if st.button("🚀 RUN EXECUTIVE REVIEW", use_container_width=True):
    with st.spinner("🔄 Analyzing data... This may take 30-60 seconds..."):
        try:
            files = {'file': ('data.csv', BytesIO(st.session_state.uploaded_file_data), 'text/csv')}
            response = requests.post(
                f"{API_BASE_URL}/review/full",
                files=files,
                timeout=120
            )
            
            if response.status_code == 200:
                st.session_state.analysis_data = response.json()
                st.success("✅ Analysis complete!")
                st.rerun()
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.error(response.text)
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Backend may still be processing.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection failed. Ensure backend is running on port 8000.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# DISPLAY ANALYSIS RESULTS
# ===========================
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    
    # Executive Judgment
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🎯 Executive Judgment")
    
    executive_judgment = data.get('executive_judgment', 'No judgment available')
    st.markdown(f"""
    <div class="executive-summary">
        <p>{executive_judgment}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Business Signals
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📡 Key Business Signals")
    
    signals = data.get('key_signals', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        revenue_wow = signals.get('revenue_wow_pct', 0)
        color = "#00d9ff" if revenue_wow >= 0 else "#ff6f00"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Revenue WoW</div>
            <div class="metric-value" style="color: {color};">{revenue_wow:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        trend_dir = signals.get('trend_direction', 'stable')
        trend_emoji = "📈" if trend_dir == "up" else "📉" if trend_dir == "down" else "➡️"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Trend Direction</div>
            <div class="metric-value">{trend_emoji} {trend_dir.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        severity = signals.get('severity', 'normal')
        severity_color = {"critical": "#ff0000", "warning": "#ff6f00", "normal": "#00d9ff"}.get(severity, "#00d9ff")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Alert Severity</div>
            <div class="metric-value" style="color: {severity_color};">{severity.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weekly Revenue Trend Chart
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📈 Weekly Revenue Trend")
    
    trend_data = data.get('weekly_trend', {})
    weeks = trend_data.get('weeks', [])
    revenues = trend_data.get('revenues', [])
    
    if weeks and revenues:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weeks,
            y=revenues,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#00d9ff', width=4),
            marker=dict(size=12, color='#ff6f00', line=dict(color='#ffffff', width=2)),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.2)'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(13, 2, 33, 0.9)',
            paper_bgcolor='rgba(13, 2, 33, 0.9)',
            font=dict(color='#ffffff', size=14, family='Inter'),
            xaxis=dict(
                title="Week",
                gridcolor='rgba(138, 43, 226, 0.2)',
                showgrid=True,
                color='#ffffff'
            ),
            yaxis=dict(
                title="Revenue ($)",
                gridcolor='rgba(138, 43, 226, 0.2)',
                showgrid=True,
                color='#ffffff'
            ),
            height=450,
            hovermode='x unified',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No trend data available")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance Drivers
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🎯 Performance Drivers")
    
    col1, col2 = st.columns(2)
    
    # Regional Performance
    with col1:
        st.markdown("### 🌍 Regional Performance")
        regional_data = data.get('performance_drivers', {}).get('regional', {})
        
        if regional_data:
            countries = list(regional_data.keys())
            values = list(regional_data.values())
            
            fig = go.Figure(data=[
                go.Bar(
                    x=countries,
                    y=values,
                    marker=dict(
                        color=values,
                        colorscale=[[0, '#ff6f00'], [0.5, '#c2185b'], [1, '#00d9ff']],
                        line=dict(color='#ffffff', width=2)
                    ),
                    text=[f"${v:,.0f}" for v in values],
                    textposition='outside',
                    textfont=dict(color='#ffffff', size=12, family='Inter')
                )
            ])
            
            fig.update_layout(
                plot_bgcolor='rgba(13, 2, 33, 0.9)',
                paper_bgcolor='rgba(13, 2, 33, 0.9)',
                font=dict(color='#ffffff', size=12, family='Inter'),
                xaxis=dict(gridcolor='rgba(138, 43, 226, 0.2)', color='#ffffff'),
                yaxis=dict(gridcolor='rgba(138, 43, 226, 0.2)', color='#ffffff', title="Revenue ($)"),
                height=400,
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Channel Performance
    with col2:
        st.markdown("### 📢 Channel Performance")
        channel_data = data.get('performance_drivers', {}).get('channel', {})
        
        if channel_data:
            channels = list(channel_data.keys())
            values = list(channel_data.values())
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=channels,
                    values=values,
                    hole=0.4,
                    marker=dict(
                        colors=['#00d9ff', '#ff6f00', '#c2185b'],
                        line=dict(color='#ffffff', width=3)
                    ),
                    textfont=dict(size=14, color='#ffffff', family='Inter'),
                    textinfo='label+percent'
                )
            ])
            
            fig.update_layout(
                plot_bgcolor='rgba(13, 2, 33, 0.9)',
                paper_bgcolor='rgba(13, 2, 33, 0.9)',
                font=dict(color='#ffffff', size=12, family='Inter'),
                height=400,
                showlegend=True,
                legend=dict(font=dict(color='#ffffff')),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# NATURAL LANGUAGE Q&A
# ===========================
if st.session_state.uploaded_file_data:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 💬 Ask Questions About Your Data")
    st.markdown("### Natural Language Query Interface")
    
    user_question = st.text_input(
        "Enter your question:",
        placeholder="e.g., Which country had the highest revenue last week?",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 ASK QUESTION", use_container_width=True):
        if user_question:
            with st.spinner("🤔 Thinking..."):
                try:
                    files = {'file': ('data.csv', BytesIO(st.session_state.uploaded_file_data), 'text/csv')}
                    payload = {'question': user_question}
                    
                    response = requests.post(
                        f"{API_BASE_URL}/review/query",
                        files=files,
                        data=payload,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown("### 💡 Answer")
                        st.markdown(f"""
                        <div class="executive-summary">
                            <p>{result.get('answer', 'No answer available')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display visualizations if available
                        viz_data = result.get('visualization')
                        if viz_data and isinstance(viz_data, dict):
                            chart_type = viz_data.get('type')
                            chart_data = viz_data.get('data', {})
                            
                            if chart_type == 'bar' and chart_data:
                                st.markdown("### 📊 Visualization")
                                fig = go.Figure(data=[
                                    go.Bar(
                                        x=list(chart_data.keys()),
                                        y=list(chart_data.values()),
                                        marker=dict(
                                            color=list(chart_data.values()),
                                            colorscale=[[0, '#ff6f00'], [0.5, '#c2185b'], [1, '#00d9ff']],
                                            line=dict(color='#ffffff', width=2)
                                        ),
                                        text=[f"{v:,.0f}" for v in chart_data.values()],
                                        textposition='outside',
                                        textfont=dict(color='#ffffff', size=12)
                                    )
                                ])
                                
                                fig.update_layout(
                                    plot_bgcolor='rgba(13, 2, 33, 0.9)',
                                    paper_bgcolor='rgba(13, 2, 33, 0.9)',
                                    font=dict(color='#ffffff', size=12),
                                    xaxis=dict(gridcolor='rgba(138, 43, 226, 0.2)', color='#ffffff'),
                                    yaxis=dict(gridcolor='rgba(138, 43, 226, 0.2)', color='#ffffff'),
                                    height=400,
                                    margin=dict(l=20, r=20, t=20, b=20)
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Key insights
                        insights = result.get('insights', [])
                        if insights:
                            st.markdown("### 🔑 Key Insights")
                            for insight in insights:
                                st.markdown(f"""
                                <div class="signal-card">
                                    <p>• {insight}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Follow-up questions
                        followups = result.get('follow_up_questions', [])
                        if followups:
                            st.markdown("### ❓ Suggested Follow-Up Questions")
                            for fq in followups:
                                st.markdown(f"- {fq}")
                    
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                        st.error(response.text)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question")
    
    # Example Questions
    with st.expander("💡 Example Questions"):
        tab1, tab2 = st.tabs(["📊 Pre-Computed", "🔍 Custom Queries"])
        
        with tab1:
            st.markdown("#### Regional Performance")
            st.markdown("- Which region performed best last week?")
            st.markdown("- Show me country performance comparison")
            st.markdown("- What is the revenue breakdown by country?")
            
            st.markdown("#### Channel Performance")
            st.markdown("- Compare channel performance across regions")
            st.markdown("- Which channel is most effective?")
            st.markdown("- Show channel revenue distribution")
            
            st.markdown("#### Revenue Trends")
            st.markdown("- What is the week-over-week revenue trend?")
            st.markdown("- Show me revenue growth rate")
            st.markdown("- Which week had highest revenue?")
        
        with tab2:
            st.markdown("#### Anomaly Detection")
            st.markdown("- Were there any unusual patterns last week?")
            st.markdown("- Show me revenue anomalies")
            st.markdown("- Detect outliers in the data")
            
            st.markdown("#### Promotions")
            st.markdown("- What was the impact of promotions?")
            st.markdown("- Compare promoted vs non-promoted sales")
            st.markdown("- Show promotion effectiveness by channel")
            
            st.markdown("#### Pricing & Demand")
            st.markdown("- What is the average price per unit?")
            st.markdown("- Show quantity sold trends")
            st.markdown("- Analyze price vs demand relationship")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# ABOUT SECTION
# ===========================
with st.expander("ℹ️ About This Platform"):
    st.markdown("""
    ### 🚀 AI Data-to-Insight Agent
    
    **Version:** 1.0  
    **Platform:** Streamlit + FastAPI  
    **AI Engine:** GPT-4
    
    #### Features:
    - 📊 Automated weekly executive reviews
    - 🤖 Natural language query processing
    - 📈 Advanced trend analysis & anomaly detection
    - 🎯 Regional & channel performance breakdown
    - ⚡ Real-time data processing
    
    #### Tech Stack:
    - **Frontend:** Streamlit with custom Bandcamp-inspired theme
    - **Backend:** FastAPI with deterministic + AI engines
    - **Analytics:** Pandas, NumPy, Plotly
    - **AI:** OpenAI GPT-4
    
    **© 2026 FirstSource PoC**
    """)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>🚀 AI Data-to-Insight Agent</strong> | Powered by GPT-4 & FastAPI</p>
    <p>© 2026 FirstSource PoC | Version 1.0 | Bandcamp-Inspired Design</p>
</div>
""", unsafe_allow_html=True)
