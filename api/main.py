from fastapi import FastAPI
from api.routes.review import router as review_router

app = FastAPI(
    title="AI Data-to-Insight API",
    description="Deterministic analytics + executive AI reasoning",
    version="1.0"
)

app.include_router(review_router, prefix="/review")
