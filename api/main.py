from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="AI Data-to-Insight Agent API",
    description="Deterministic analytics + executive AI reasoning",
    version="1.0"
)

# UPDATED: More permissive CORS for cloud deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from api.routes import review
app.include_router(review.router, prefix="/review", tags=["Review"])

# Health check endpoint (root)
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "AI Data-to-Insight Agent API",
        "version": "1.0",
        "endpoints": {
            "full_analysis": "/review/full",
            "query": "/review/query",
            "docs": "/docs"
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI server started successfully")
    print(f"📊 OpenAI API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("👋 FastAPI server shutting down")
