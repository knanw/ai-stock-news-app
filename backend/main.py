from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from models import SummaryRequest, SummaryResponse
from services.news_service import fetch_latest_news
from services.ai_service import analyze_stock_news

app = FastAPI(title=settings.PROJECT_NAME, version="2.0.0")

@app.get("/health")
def health_check():
    """Lightweight health endpoint used by Docker and local checks."""
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/summary", response_model=SummaryResponse)
async def get_stock_summary(req: SummaryRequest):
    ticker = req.ticker.strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker symbol is required.")

    try:
        # 1. Fetch data (service layer)
        news_items = fetch_latest_news(ticker)

        # 2. Perform AI Analysis (Service Layer)
        analysis_result = analyze_stock_news(ticker, news_items, req.api_key)
        return analysis_result

    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")