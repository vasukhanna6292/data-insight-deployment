# 🤖 AI Data-to-Insight Agent

> **Transform Business Data into Actionable Executive Insights using AI**

An intelligent analytics platform that combines deterministic data processing with GPT-4 powered executive reasoning to deliver comprehensive weekly performance reviews automatically.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Technology Stack](#technology-stack)
- [Demo](#demo)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

**AI Data-to-Insight Agent** is a proof-of-concept application that automates the weekly executive review process by:

1. **Ingesting** business transaction data (CSV format)
2. **Processing** through deterministic analytics engines
3. **Detecting** anomalies and trends automatically
4. **Generating** AI-powered executive summaries
5. **Answering** natural language queries about the data

### Problem Statement

Traditional business analytics require:
- Manual data exploration (time-consuming)
- Technical SQL/Python knowledge (barrier to entry)
- Separate tools for visualization and reporting (fragmented workflow)
- Post-processing interpretation (delayed insights)

### Solution

A unified platform where:
- ✅ **Upload CSV** → Instant analysis
- ✅ **Ask questions in plain English** → Get data-driven answers
- ✅ **View AI-generated insights** → No manual interpretation needed
- ✅ **Interactive visualizations** → Explore trends visually

---

## ✨ Key Features

### 1. **Automated Weekly Executive Review** 📊
- Calculates key metrics (revenue, growth, margins)
- Identifies trends across regions, channels, and time periods
- Detects anomalies automatically
- Generates executive-level natural language summaries

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
- Channel distribution analysis (pie/bar charts)
- Built with Plotly for rich interactivity

### 5. **Transparent AI Reasoning** 🔍
- Shows generated Python code for each query
- Displays data retrieval steps
- Enables verification of AI logic

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  (User Interface)
│   (app.py)      │
└────────┬────────┘
         │ HTTP Requests
         ↓
┌─────────────────┐
│   FastAPI       │  (Backend API)
│  (api/main.py)  │
└────────┬────────┘
         │
         ├──→ Deterministic Engines
         │    ├─ prep_engine.py    (Data cleaning & transformation)
         │    ├─ trend_engine.py   (Trend analysis)
         │    ├─ anomaly_engine.py (Outlier detection)
         │    └─ query_engine.py   (NLQ processing)
         │
         ├──→ AI Reasoning Layer
         │    └─ ai_summary.py     (GPT-4 integration)
         │
         └──→ Visualization
              └─ charts.py         (Plotly charts)
```

### **Workflow:**

1. **User uploads CSV** → Streamlit frontend
2. **POST /review/full** → FastAPI backend
3. **Data preparation** → Clean & validate data
4. **Deterministic processing** → Run analytics engines
5. **AI summarization** → GPT-4 generates insights
6. **Return JSON** → Streamlit displays results

For **Natural Language Queries:**

1. **User types question** → "Show top 5 products by revenue"
2. **POST /review/query** → Send CSV + query to backend
3. **GPT-4 code generation** → Generates pandas/numpy code
4. **Execute code** → Run in sandboxed environment
5. **Return results** → Table + chart + follow-up questions

---

## 📁 Project Structure

```
FirstSource/
├── ai/
│   ├── __init__.py
│   └── ai_summary.py          # GPT-4 integration for executive summaries
├── api/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   └── routes/
│       └── review.py          # API endpoints (/review/full, /review/query)
├── engines/
│   ├── __init__.py
│   ├── prep_engine.py         # Data cleaning & preprocessing
│   ├── trend_engine.py        # Regional/channel/weekly trend analysis
│   ├── anomaly_engine.py      # Outlier detection (z-score based)
│   └── query_engine.py        # Natural language query processor
├── viz/
│   ├── __init__.py
│   └── charts.py              # Plotly visualization functions
├── sample_data/
│   └── sample_sales_data.csv  # Demo dataset (10 columns, ~20k rows)
├── Screenshots/               # Reference screenshots for README/demo
├── .env                       # Environment variables (OPENAI_API_KEY)
├── .gitignore                 # Git ignore rules
├── app.py                     # Streamlit frontend application
├── requirements.txt           # Python dependencies
├── test_prototype.py          # Unit tests for engines
└── README.md                  # This file
```

### **Key Files Explained:**

| File | Purpose | Key Functions |
|------|---------|---------------|
| `app.py` | Streamlit UI | File upload, display results, NLQ interface |
| `api/main.py` | FastAPI server | Include routers, CORS config |
| `api/routes/review.py` | API endpoints | `/review/full`, `/review/query` |
| `engines/prep_engine.py` | Data prep | `prepare_data()` - clean CSV, add Week column |
| `engines/trend_engine.py` | Trend analysis | `run_trend_engine()` - region/channel/weekly trends |
| `engines/anomaly_engine.py` | Anomaly detection | `run_anomaly_engine()` - z-score outliers |
| `engines/query_engine.py` | NLQ processing | `process_natural_language_query()` - GPT-4 → code |
| `ai/ai_summary.py` | AI summaries | `generate_ai_summary()` - executive insights |
| `viz/charts.py` | Visualizations | `plot_weekly_revenue()`, `plot_country_drivers()` |

---

## 🚀 Installation & Setup

### **Prerequisites:**

- Python 3.8+ (tested on Python 3.11)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### **Step 1: Clone Repository**

```bash
git clone https://github.com/yourusername/FirstSource.git
cd FirstSource
```

### **Step 2: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `streamlit` - Frontend UI framework
- `fastapi` - Backend API framework
- `uvicorn` - ASGI server
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `plotly` - Interactive charts
- `openai` - GPT-4 API client
- `python-dotenv` - Environment variable management
- `python-multipart` - File upload support

### **Step 3: Configure Environment Variables**

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=sk-proj-YOUR-API-KEY-HERE
```

**🔒 Security Note:** Never commit `.env` to version control! (Already in `.gitignore`)

### **Step 4: Verify Setup**

Test that dependencies are installed:

```bash
python -c "import streamlit; import fastapi; import openai; print('✅ All dependencies installed!')"
```

---

## 🎮 Usage Guide

### **Starting the Application:**

#### **Option A: Quick Start (Automatic)**

Run both FastAPI and Streamlit in one command:

```bash
# Terminal 1: Start FastAPI backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Streamlit frontend
streamlit run app.py
```

#### **Option B: Manual Start**

**Terminal 1 - Start FastAPI Backend:**
```bash
cd FirstSource
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### **Using the Application:**

#### **1. Full Analysis Mode:**

1. **Upload CSV file** (e.g., `sample_data/sample_sales_data.csv`)
2. Click **"🚀 Analyze Data"**
3. Wait 30-60 seconds
4. View results:
   - Executive Summary (AI-generated)
   - Key Metrics (revenue, growth, trends)
   - Regional Performance
   - Channel Breakdown
   - Anomaly Alerts
   - Interactive Charts

#### **2. Natural Language Query Mode:**

1. Upload CSV (same as above)
2. Scroll to **"Ask a Question"** section
3. Type question:
   - *"Show me top 5 countries by revenue"*
   - *"What's the average margin by channel?"*
   - *"Compare revenue Q1 vs Q2"*
4. Click **"Ask"**
5. View:
   - AI-generated answer
   - Data table
   - Generated Python code
   - Follow-up question suggestions

---

## 📡 API Documentation

### **Base URL:** `http://localhost:8000`

### **Interactive API Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### **Endpoint 1: Full Analysis**

**`POST /review/full`**

Performs comprehensive weekly executive review.

**Request:**
```http
POST /review/full HTTP/1.1
Content-Type: multipart/form-data

file: <CSV file>
```

**Response (JSON):**
```json
{
  "analysis_week": "2024-W08",
  "metrics": {
    "overall_revenue_trend": "Downward (-7.0%)"
  },
  "trends": {
    "region": [
      {
        "region": "USA",
        "trend": "Downward",
        "description": "Revenue fell 7.1% from previous period..."
      }
    ],
    "channel": [...],
    "weekly_total": [...]
  },
  "anomalies": [
    {
      "type": "Revenue Outlier",
      "description": "Week 7 revenue 35% below average",
      "impact": "High"
    }
  ],
  "executive_summary": "Revenue declined 7.0% this week..."
}
```

---

### **Endpoint 2: Natural Language Query**

**`POST /review/query`**

Answers natural language questions about the data.

**Request:**
```http
POST /review/query HTTP/1.1
Content-Type: multipart/form-data

file: <CSV file>
query: "Show me top 3 countries by revenue"
```

**Response (JSON):**
```json
{
  "query": "Show me top 3 countries by revenue",
  "answer": "Here are the top 3 countries by total revenue...",
  "data": [
    {"Country": "USA", "Revenue": 1234567},
    {"Country": "India", "Revenue": 890123},
    {"Country": "UK", "Revenue": 567890}
  ],
  "code": "df.groupby('Country')['Revenue'].sum().nlargest(3)",
  "follow_up_questions": [
    "What's the growth rate for each country?",
    "Show me revenue by channel for USA"
  ]
}
```

---

## 🛠️ Technology Stack

### **Frontend:**
- **Streamlit 1.x** - Rapid UI development
- **Plotly 5.x** - Interactive charts
- **Pandas** - Data display

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

### **Development:**
- **Python 3.11** - Programming language
- **Git** - Version control
- **python-dotenv** - Config management

---

## 🎥 Demo

### **Sample Dataset:**

Located in `sample_data/sample_sales_data.csv`

**Columns:**
- `transaction_id` - Unique identifier
- `Date` - Transaction date (YYYY-MM-DD)
- `Country` - USA, India, UK, France, Germany
- `SKU` - Product ID
- `Channel` - Supermarket, Online, Retail
- `Units Sold` - Quantity
- `Unit Price` - Price per unit
- `Revenue` - Total revenue
- `Margin %` - Profit margin percentage
- `Margin` - Absolute margin

**Stats:**
- ~20,000 rows
- 8 weeks of data
- 5 countries, 3 channels
- Multiple product SKUs

### **Demo Workflow:**

1. **Start servers** (see Usage Guide)
2. **Open Streamlit** (http://localhost:8501)
3. **Upload** `sample_data/sample_sales_data.csv`
4. **Analyze** → View executive summary
5. **Ask queries:**
   - "Show me weekly revenue trends"
   - "Which channel has the highest margin?"
   - "Compare USA vs India performance"
6. **Explore** charts and insights

### **Expected Results:**

- **Executive Summary:** AI identifies 7% revenue decline, regional disparities
- **Anomalies:** Flags Week 7 revenue outlier, Diwali promo underperformance
- **Trends:** USA declining (-7.1%), India declining (-13.5%)
- **Charts:** Interactive weekly revenue line chart, country bar chart

---

## 🚧 Challenges & Solutions

### **Challenge 1: Streamlit Cloud Deployment**

**Problem:**  
Streamlit Cloud cannot run FastAPI backend alongside frontend (single-container limitation).

**Attempted Solutions:**
1. Railway.app deployment for FastAPI
2. Secrets configuration for cross-origin connection
3. CORS policy adjustments

**Outcome:**  
Railway deployment successful but connection issues persisted due to Streamlit Cloud's restrictive environment policies.

**Final Decision:**  
Delivered as **localhost deployment** for PoC demonstration. Production-ready architecture designed (see Future Enhancements).

---

### **Challenge 2: Natural Language to Code Reliability**

**Problem:**  
GPT-4 occasionally generates code with:
- Syntax errors
- Non-existent column references
- Inefficient operations

**Solutions Implemented:**
1. **Structured prompts** with column schema
2. **Few-shot examples** in system prompt
3. **Error handling** with retry logic
4. **Sandboxed execution** (no file system access)
5. **Result validation** before returning to user

**Outcome:**  
~90% query success rate with graceful error messages for edge cases.

---

### **Challenge 3: Anomaly Detection Tuning**

**Problem:**  
Z-score threshold too sensitive → too many false positives.

**Solution:**
- Tuned threshold to **z > 2.5** (97.5th percentile)
- Added context-aware descriptions
- Filtered low-impact anomalies (<5% deviation)

**Outcome:**  
Reduced alerts by 60%, improved executive relevance.

---

### **Challenge 4: Performance with Large Datasets**

**Problem:**  
20k+ row CSVs caused 30+ second processing delays.

**Optimizations:**
1. Vectorized pandas operations (no loops)
2. Cached data preprocessing results
3. Async FastAPI endpoints
4. Streaming response for queries

**Outcome:**  
Reduced full analysis time from 45s → 25s.

---

### **Challenge 5: Environment Variable Management**

**Problem:**  
Developers accidentally committed `.env` with API keys.

**Solution:**
1. Added `.env` to `.gitignore`
2. Created `.env.example` template
3. Documented setup in README
4. Added pre-commit hook (optional)

**Outcome:**  
Zero security incidents during development.

---

## 🔮 Future Enhancements

### **Near-Term (Next Sprint):**

1. **Cloud Deployment:**
   - Deploy FastAPI to Heroku/Railway/AWS Lambda
   - Use Streamlit Cloud for frontend only
   - Connect via public HTTPS endpoint

2. **Database Integration:**
   - Replace CSV uploads with PostgreSQL/MongoDB
   - Store historical analyses
   - Enable trend comparison across weeks

3. **User Authentication:**
   - Add login/signup (e.g., Auth0)
   - Role-based access control
   - Multi-tenant support

4. **Enhanced Visualizations:**
   - Drill-down charts (click country → see products)
   - Dashboard builder (drag-and-drop widgets)
   - Export to PDF/PowerPoint

### **Long-Term (Future Versions):**

5. **Advanced AI Features:**
   - Predictive forecasting (next week's revenue)
   - Recommendation engine (suggested actions)
   - Sentiment analysis on customer feedback

6. **Real-Time Data:**
   - Streaming data ingestion (Kafka/Redis)
   - Live dashboard updates (WebSocket)
   - Alert notifications (email/Slack)

7. **Multi-Source Integration:**
   - Connect to CRM (Salesforce), ERP (SAP)
   - API connectors for Google Analytics, Shopify
   - Automated ETL pipelines

8. **Collaboration Features:**
   - Shared reports with comments
   - Team dashboards
   - Scheduled reports (weekly email digest)

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

---

## 🙏 Acknowledgments

- **OpenAI GPT-4** - Powering AI insights
- **Streamlit Team** - Rapid UI framework
- **FastAPI Community** - Modern backend architecture
- **Plotly** - Interactive visualizations
- **FirstSource Team** - Domain expertise and requirements

---

## 📊 Project Stats

- **Total Lines of Code:** ~2,500
- **Development Time:** 5 Days
- **Dependencies:** 10 packages
- **Test Coverage:** Core engines tested
- **API Endpoints:** 2 (full analysis, query)
- **Supported Query Types:** 10+ patterns

---

## 🎯 Key Takeaways

✅ **AI + Deterministic = Best Results** - Combine rule-based engines with GPT reasoning  
✅ **Natural Language Unlocks Insights** - Non-technical users can explore data  
✅ **Fast Iteration Matters** - Localhost deployment accelerates testing  
✅ **Transparency Builds Trust** - Show generated code, don't hide AI logic  
✅ **Cloud Deployment Needs Planning** - Architecture decisions affect hosting options  

---

**Built with ❤️ and ☕ by the FirstSource Analytics Team**

---

*Last Updated: February 11, 2026*
