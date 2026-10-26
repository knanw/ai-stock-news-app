from pydantic import BaseModel, Field
from typing import List, Optional

class SummaryRequest(BaseModel):
    ticker: str = Field(..., json_schema_extra={"example": "AAPL"},)
    api_key: Optional[str] = None

class NewsItem(BaseModel):
    title: str
    publisher: str
    link: str
    publishTime: str
    summary: Optional[str] = None

class AnalysisResult(BaseModel):
    executiveSummary: str
    sentiment: str
    keyTakeaways: List[str]

class SummaryResponse(BaseModel):
    ticker: str
    news: List[NewsItem]
    analysis: AnalysisResult