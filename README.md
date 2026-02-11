# 🤖 AI Data-to-Insight Agent

> **Transform Business Data into Actionable Executive Insights using AI**

A cloud-deployed intelligent analytics platform that combines deterministic data processing with GPT-4 powered executive reasoning to deliver comprehensive weekly performance reviews automatically.

**🌐 Live Demo:** [https://data-insight-deployment.streamlit.app](https://data-insight-deployment.streamlit.app)  
**📦 Repository:** [https://github.com/vasukhanna6292/data-insight-deployment](https://github.com/vasukhanna6292/data-insight-deployment)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Live Deployment](#live-deployment)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start Guide](#quick-start-guide)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Technology Stack](#technology-stack)
- [Deployment Architecture](#deployment-architecture)
- [Demo Workflow](#demo-workflow)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

**AI Data-to-Insight Agent** is a production-ready analytics platform that automates the weekly executive review process by:

1. **Ingesting** business transaction data (CSV format)
2. **Processing** through deterministic analytics engines
3. **Detecting** anomalies and trends automatically
4. **Generating** AI-powered executive summaries
5. **Answering** natural language queries about the data

### Problem Statement

Traditional business analytics require:
- ❌ Manual data exploration (time-consuming)
- ❌ Technical SQL/Python knowledge (barrier to entry)
- ❌ Separate tools for visualization and reporting (fragmented workflow)
- ❌ Post-processing interpretation (delayed insights)

### Solution

A unified cloud platform where:
- ✅ **Upload CSV** → Instant analysis
- ✅ **Ask questions in plain English** → Get data-driven answers
- ✅ **View AI-generated insights** → No manual interpretation needed
- ✅ **Interactive visualizations** → Explore trends visually
- ✅ **Access anywhere** → Cloud-deployed, no installation required

---

## ✨ Key Features

### 1. **Automated Weekly Executive Review** 📊
- Calculates key metrics (revenue, growth, margins)
- Identifies trends across regions, channels, and time periods
- Detects anomalies automatically using z-score analysis
- Generates executive-level natural language summaries via GPT-4

### 2. **Natural Language Query Interface** 💬
- Ask questions like: *"Show me revenue by country for USA and India"*
- AI generates and executes Python code dynamically
- Returns results as tables and visualizations
- Suggests relevant follow-up questions

### 3. **Anomaly Detection Engine** 🚨
- Flags outliers in revenue, margin, and discount patterns
- Contextual impact analysis (e.g., "Unusual 40% discount spike")
- Prioritized alerts for executive attention

### 4. **Interactive Visualizations** 📈
- Weekly revenue trends (line charts)
- Regional performance drivers (bar charts)
- Channel distribution analysis (pie/donut charts)
- Built with Plotly for rich interactivity

### 5. **Premium Enterprise UI** 🎨
- **Bandcamp-inspired design** with gradient backgrounds
- Dark theme with vibrant cyan/orange accents
- Glassmorphism effects and smooth animations
- Fully responsive and mobile-friendly

### 6. **Cloud-Native Architecture** ☁️
- **Frontend:** Deployed on Streamlit Cloud
- **Backend:** Deployed on Render.com
- **Scalable:** Auto-scaling FastAPI backend
- **Secure:** HTTPS endpoints, environment variable management

---

## 🌐 Live Deployment

### **Access the Application:**

**🚀 Frontend URL:** [https://data-insight-deployment.streamlit.app](https://data-insight-deployment.streamlit.app)

**🔧 Backend API:** Deployed on Render.com (private endpoint)

**📚 API Documentation:**
- Swagger UI: `[backend-url]/docs`
- ReDoc: `[backend-url]/redoc`

### **Deployment Status:**

| Service | Platform | Status | URL |
|---------|----------|--------|-----|
| Frontend | Streamlit Cloud | ✅ Live | [streamlit.app](https://data-insight-deployment.streamlit.app) |
| Backend | Render.com | ✅ Live | Private endpoint |
| Database | N/A (CSV upload) | ✅ Active | File-based |

---

## 🏗️ Architecture

### **Cloud Deployment Architecture:**

```
┌─────────────────────────────────────────┐
│         USER BROWSER                     │
│    (Anywhere in the world)              │
└───────────────┬─────────────────────────┘
                │ HTTPS
                ↓
┌─────────────────────────────────────────┐
│    STREAMLIT CLOUD (Frontend)           │
│    • app.py (UI)                        │
│    • Premium Bandcamp-inspired theme    │
│    • File upload & visualization        │
│    • https://...streamlit.app           │
└───────────────┬─────────────────────────┘
                │ HTTPS API Calls
                ↓
┌─────────────────────────────────────────┐
│    RENDER.COM (Backend)                 │
│    • FastAPI (api/main.py)              │
│    • Uvicorn ASGI server                │
│    • Auto-scaling instances             │
│    • Environment: Python 3.11           │
└───────────────┬─────────────────────────┘
                │
                ├──→ Deterministic Engines
                │    ├─ prep_engine.py    (Data cleaning)
                │    ├─ trend_engine.py   (Trend analysis)
                │    ├─ anomaly_engine.py (Outlier detection)
                │    └─ query_engine.py   (NLQ processing)
                │
                ├──→ AI Reasoning Layer
                │    └─ ai_summary.py     (OpenAI GPT-4)
                │
                └──→ Visualization
                     └─ charts.py         (Plotly charts)
```

### **Workflow:**

1. **User uploads CSV** → Streamlit Cloud frontend
2. **POST request** → Render.com backend API
3. **Data processing** → Analytics engines + GPT-4
4. **JSON response** → Frontend displays results
5. **Interactive charts** → Plotly visualizations

---

## 📁 Project Structure

```
data-insight-deployment/
├── .streamlit/
│   └── config.toml                # Streamlit theme configuration
├── ai/
│   ├── __init__.py
│   └── ai_summary.py              # GPT-4 integration for executive summaries
├── api/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point (with CORS)
│   └── routes/
│       └── review.py              # API endpoints (/review/full, /review/query)
├── engines/
│   ├── __init__.py
│   ├── prep_engine.py             # Data cleaning & preprocessing
│   ├── trend_engine.py            # Regional/channel/weekly trend analysis
│   ├── anomaly_engine.py          # Outlier detection (z-score based)
│   └── query_engine.py            # Natural language query processor
├── viz/
│   ├── __init__.py
│   └── charts.py                  # Plotly visualization functions
├── Screenshots/                   # Reference screenshots for demo
├── .gitignore                     # Git ignore rules
├── app.py                         # Streamlit frontend (Bandcamp-inspired UI)
├── Procfile                       # Render.com process file
├── render.yaml                    # Render.com deployment config
├── runtime.txt                    # Python version specification
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

### **Key Files Explained:**

| File | Purpose | Deployment Role |
|------|---------|-----------------|
| `app.py` | Streamlit UI | **Streamlit Cloud** - Frontend |
| `api/main.py` | FastAPI server | **Render.com** - Backend API |
| `Procfile` | Process definition | Render.com startup command |
| `render.yaml` | Infrastructure config | Render.com service definition |
| `runtime.txt` | Python version | Forces Python 3.11 |
| `.streamlit/config.toml` | Theme settings | Streamlit appearance |
| `requirements.txt` | Dependencies | Both platforms |

---

## 🚀 Quick Start Guide

### **Option 1: Use Live Deployment (Recommended)**

**No installation required!**

1. Visit: [https://data-insight-deployment.streamlit.app](https://data-insight-deployment.streamlit.app)
2. Upload your CSV file (or use sample data)
3. Click **"🚀 RUN EXECUTIVE REVIEW"**
4. Explore insights and ask questions!

---

### **Option 2: Local Development Setup**

For developers who want to run locally:

#### **Prerequisites:**
- Python 3.11+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git

#### **Step 1: Clone Repository**

```bash
git clone https://github.com/vasukhanna6292/data-insight-deployment.git
cd data-insight-deployment
```

#### **Step 2: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `streamlit` - Frontend UI framework
- `fastapi` - Backend API framework
- `uvicorn` - ASGI server
- `pandas`, `numpy` - Data processing
- `plotly` - Interactive charts
- `openai` - GPT-4 API client
- `python-dotenv` - Environment variables
- `python-multipart` - File upload support

#### **Step 3: Configure Environment Variables**

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=sk-proj-YOUR-API-KEY-HERE
```

**🔒 Security Note:** Never commit `.env` to version control!

#### **Step 4: Start Services**

**Terminal 1 - Backend:**
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
streamlit run app.py
```

**Access locally:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎮 Usage Guide

### **Full Analysis Mode:**

1. **Upload CSV file** (10+ columns recommended)
   - Supported format: Date, Country, SKU, Channel, Units Sold, Unit Price, Revenue, Margin%, Margin
2. Click **"🚀 RUN EXECUTIVE REVIEW"**
3. Wait 20-40 seconds for AI processing
4. View results:
   - 🎯 **Executive Judgment** (AI-generated summary)
   - 📡 **Key Business Signals** (WoW%, trend, severity)
   - 📈 **Weekly Revenue Trend** (interactive chart)
   - 🌍 **Regional Performance** (bar chart)
   - 📢 **Channel Distribution** (pie chart)

### **Natural Language Query Mode:**

1. After uploading data, scroll to **"💬 Ask Questions"** section
2. Type your question (examples below)
3. Click **"🔍 ASK QUESTION"**
4. View:
   - 💡 **AI-generated answer**
   - 📊 **Data visualization** (if applicable)
   - 🔑 **Key insights**
   - ❓ **Follow-up suggestions**

#### **Example Questions:**

**Pre-Computed Analytics:**
- "Which region performed best last week?"
- "Show me country performance comparison"
- "What is the revenue breakdown by country?"
- "Compare channel performance across regions"

**Custom Exploration:**
- "Show me top 5 products by revenue"
- "What's the average margin by channel?"
- "Compare USA vs India revenue trends"
- "Which week had the highest revenue?"

**Advanced Queries:**
- "Show me revenue anomalies"
- "What was the impact of promotions?"
- "Analyze price vs demand relationship"

---

## 📡 API Documentation

### **Base URL (Production):** `https://[your-render-backend].onrender.com`

### **Interactive API Docs:**
- **Swagger UI:** `[backend-url]/docs`
- **ReDoc:** `[backend-url]/redoc`

---

### **Endpoint 1: Full Executive Review**

**`POST /review/full`**

Performs comprehensive weekly performance analysis.

**Request:**
```http
POST /review/full HTTP/1.1
Content-Type: multipart/form-data

file: <CSV file>
```

**Response (JSON):**
```json
{
  "executive_judgment": "Revenue declined 7.0% this week...",
  "key_signals": {
    "revenue_wow_pct": -7.0,
    "trend_direction": "down",
    "severity": "warning"
  },
  "weekly_trend": {
    "weeks": ["Week 1", "Week 2", ...],
    "revenues": [120000, 135000, ...]
  },
  "performance_drivers": {
    "regional": {"USA": 500000, "India": 320000, ...},
    "channel": {"Online": 400000, "Retail": 350000, ...}
  }
}
```

---

### **Endpoint 2: Natural Language Query**

**`POST /review/query`**

Answers natural language questions about uploaded data.

**Request:**
```http
POST /review/query HTTP/1.1
Content-Type: multipart/form-data

file: <CSV file>
question: "Show me top 3 countries by revenue"
```

**Response (JSON):**
```json
{
  "answer": "Here are the top 3 countries by total revenue...",
  "visualization": {
    "type": "bar",
    "data": {"USA": 500000, "India": 320000, "UK": 280000}
  },
  "insights": [
    "USA leads with 38% of total revenue",
    "India shows strong growth (+15% WoW)"
  ],
  "follow_up_questions": [
    "What's the growth rate for each country?",
    "Show channel breakdown for USA"
  ]
}
```

---

## 🛠️ Technology Stack

### **Frontend:**
- **Streamlit 1.x** - Rapid UI development
- **Plotly 5.x** - Interactive charts
- **Custom CSS** - Bandcamp-inspired theme

### **Backend:**
- **FastAPI 0.1x** - Modern async API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### **AI/ML:**
- **OpenAI GPT-4** - Natural language understanding & code generation
- **Python execution** - Safe code sandbox

### **Data Processing:**
- **Pandas** - DataFrame operations
- **NumPy** - Numerical analysis
- **SciPy** - Statistical functions (z-score)

### **Cloud Infrastructure:**
- **Streamlit Cloud** - Frontend hosting (free tier)
- **Render.com** - Backend API hosting (free tier)
- **GitHub** - Version control & CI/CD

### **Development:**
- **Python 3.11** - Programming language
- **Git** - Version control
- **python-dotenv** - Config management

---

## ☁️ Deployment Architecture

### **Streamlit Cloud (Frontend):**

**Configuration File:** `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#00d9ff"
backgroundColor = "#0d0221"
secondaryBackgroundColor = "#1a0a2e"
textColor = "#ffffff"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

**Deployment Process:**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set environment variables (OPENAI_API_KEY)
4. Auto-deploy on every commit

---

### **Render.com (Backend):**

**Configuration File:** `render.yaml`
```yaml
services:
  - type: web
    name: data-insight-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

**Process File:** `Procfile`
```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Deployment Process:**
1. Push code to GitHub
2. Connect repository to Render.com
3. Configure environment variables
4. Auto-deploy on every commit
5. Backend URL provided automatically

---

### **CORS Configuration:**

**File:** `api/main.py`
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎥 Demo Workflow

### **Sample Dataset:**

Use the provided sample dataset or your own CSV with these columns:

**Required Columns:**
- `Date` - Transaction date (YYYY-MM-DD)
- `Country` - Geographic region
- `Channel` - Sales channel (Online, Retail, etc.)
- `Revenue` - Total revenue
- `Margin %` - Profit margin percentage

**Optional Columns:**
- `SKU`, `Units Sold`, `Unit Price`, `Margin`, `transaction_id`

**Sample Data Stats:**
- ~20,000 rows
- 8 weeks of data
- 5 countries, 3 channels
- Multiple product SKUs

---

### **Step-by-Step Demo:**

1. **Access the app:** [https://data-insight-deployment.streamlit.app](https://data-insight-deployment.streamlit.app)
2. **Upload CSV** (use sample or your own data)
3. **Click "🚀 RUN EXECUTIVE REVIEW"**
4. **View results:**
   - Executive AI summary identifies key trends
   - Charts show regional/channel performance
   - Anomalies flagged automatically
5. **Ask questions:**
   - "Show me weekly revenue trends"
   - "Which channel has the highest margin?"
   - "Compare USA vs India performance"
6. **Explore** interactive visualizations

---

## 🚧 Challenges & Solutions

### **Challenge 1: Cloud Deployment Architecture** ✅

**Problem:**  
Streamlit Cloud cannot run FastAPI backend alongside frontend (single-container limitation).

**Solution:**
- ✅ Deployed FastAPI backend to **Render.com**
- ✅ Deployed Streamlit frontend to **Streamlit Cloud**
- ✅ Connected via HTTPS public API endpoint
- ✅ Configured CORS for cross-origin requests

**Outcome:**  
**Production-ready cloud deployment** with auto-scaling and zero infrastructure management.

---

### **Challenge 2: Environment Variable Security** ✅

**Problem:**  
Sensitive API keys (OpenAI) must not be exposed in GitHub.

**Solution:**
- ✅ `.env` added to `.gitignore`
- ✅ Environment variables configured in platform dashboards
- ✅ Secrets management via Streamlit/Render interfaces

**Outcome:**  
Zero security incidents, production-safe deployment.

---

### **Challenge 3: Natural Language to Code Reliability** ✅

**Problem:**  
GPT-4 occasionally generates code with syntax errors or invalid column references.

**Solutions Implemented:**
1. **Structured prompts** with column schema
2. **Few-shot examples** in system prompt
3. **Error handling** with retry logic
4. **Sandboxed execution** (no file system access)
5. **Result validation** before returning

**Outcome:**  
~90% query success rate with graceful error messages.

---

### **Challenge 4: Premium UI Design** ✅

**Problem:**  
Default Streamlit theme looks generic and unprofessional.

**Solution:**
- ✅ Custom CSS with **Bandcamp-inspired gradient theme**
- ✅ Glassmorphism effects and smooth animations
- ✅ Vibrant cyan/orange accent colors
- ✅ Dark containers with high-contrast text
- ✅ Professional typography (Inter font)

**Outcome:**  
Enterprise-grade UI that impresses stakeholders.

---

### **Challenge 5: Performance Optimization** ✅

**Problem:**  
20k+ row CSVs caused 30+ second processing delays.

**Optimizations:**
1. Vectorized pandas operations (no loops)
2. Cached preprocessing results
3. Async FastAPI endpoints
4. Streaming responses

**Outcome:**  
Reduced full analysis time from 45s → 25s.

---

## 🔮 Future Enhancements

### **Near-Term (Next Sprint):**

1. **Database Integration:**
   - Replace CSV uploads with PostgreSQL/MongoDB
   - Store historical analyses
   - Enable trend comparison across weeks

2. **User Authentication:**
   - Add login/signup (Auth0 or Firebase)
   - Role-based access control
   - Multi-tenant support

3. **Enhanced Visualizations:**
   - Drill-down charts (click country → see products)
   - Dashboard builder (drag-and-drop widgets)
   - Export to PDF/PowerPoint

4. **Scheduled Reports:**
   - Email weekly executive summaries
   - Slack/Teams integration
   - Custom report templates

---

### **Long-Term (Future Versions):**

5. **Advanced AI Features:**
   - Predictive forecasting (next week's revenue)
   - Recommendation engine (suggested actions)
   - Sentiment analysis on customer feedback

6. **Real-Time Data:**
   - Streaming data ingestion (Kafka/Redis)
   - Live dashboard updates (WebSocket)
   - Real-time anomaly alerts

7. **Multi-Source Integration:**
   - Connect to CRM (Salesforce), ERP (SAP)
   - API connectors for Google Analytics, Shopify
   - Automated ETL pipelines

8. **Collaboration Features:**
   - Shared reports with comments
   - Team dashboards
   - Version control for analyses

---

## 📜 License

This project is a **Proof of Concept (PoC)** developed for demonstration purposes.

**Usage:**
- ✅ Academic/research use
- ✅ Internal company demos
- ✅ Portfolio showcases
- ❌ Commercial redistribution without permission

**Dependencies:**  
All dependencies retain their original licenses (see `requirements.txt`).

---

## 🤝 Contributing

This is a PoC project, but feedback is welcome!

**To report issues or suggest features:**
1. Open an issue on GitHub
2. Describe the problem/idea clearly
3. Include screenshots if applicable

---

## 📧 Contact

**Project Maintainer:** Vasu Khanna  
**Email:** vasukhanna6292@gmail.com  
**GitHub:** [@vasukhanna6292](https://github.com/vasukhanna6292)  
**Live Demo:** [data-insight-deployment.streamlit.app](https://data-insight-deployment.streamlit.app)

---

## 🙏 Acknowledgments

- **OpenAI GPT-4** - Powering AI insights
- **Streamlit Team** - Cloud hosting & rapid UI framework
- **Render.com** - Backend API hosting
- **FastAPI Community** - Modern backend architecture
- **Plotly** - Interactive visualizations
- **FirstSource Team** - Domain expertise and requirements

---

## 📊 Project Stats

- **Total Lines of Code:** ~3,000+
- **Development Time:** 7 Days
- **Cloud Platforms:** 2 (Streamlit Cloud + Render.com)
- **Dependencies:** 12 packages
- **API Endpoints:** 2 (full analysis, query)
- **Supported Query Types:** 15+ patterns
- **Deployment Status:** ✅ **LIVE IN PRODUCTION**

---

## 🎯 Key Takeaways

✅ **Cloud-Native Design** - Fully deployed, no local setup required  
✅ **AI + Deterministic = Best Results** - Combine rule-based engines with GPT reasoning  
✅ **Natural Language Unlocks Insights** - Non-technical users can explore data  
✅ **Premium UI Matters** - Professional design increases stakeholder confidence  
✅ **Auto-Scaling Ready** - Architecture supports production workloads  

---

## 🚀 Quick Links

- **🌐 Live Demo:** [https://data-insight-deployment.streamlit.app](https://data-insight-deployment.streamlit.app)
- **📦 GitHub Repo:** [https://github.com/vasukhanna6292/data-insight-deployment](https://github.com/vasukhanna6292/data-insight-deployment)
- **📧 Support:** vasukhanna6292@gmail.com

---

**Built with ❤️ and ☕ by Vasu Khanna**

**🎨 Design Inspired by:** Bandcamp Explorer  
**⚡ Powered by:** OpenAI GPT-4 | Streamlit | FastAPI
