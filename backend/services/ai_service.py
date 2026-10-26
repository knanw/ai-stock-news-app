import json
import time
from openai import OpenAI
from config import settings

# Simple In-Memory TTL Cache: { "AAPL": {"timestamp": 12345678, "data": {...}} }
_cache = {}
CACHE_TTL = 600  # 10 minutes TTL cache

def analyze_stock_news(ticker: str, news_items: list, user_api_key: str = None) -> dict:
    now = time.time()

    print(news_items)

    if ticker in _cache:
        cached_entry = _cache[ticker]
        if now - cached_entry["timestamp"] < CACHE_TTL:
            print(f"⚡ Cache hit for {ticker}")
            return cached_entry["data"]

    api_key = user_api_key or settings.API_KEY
    if not api_key:
        raise ValueError("API Key is missing. Provide it in the UI or set API_KEY env variable.")

    # prepare new structure for prompting the AI model
    formatted_news = json.dumps([
        {"id": i, "title": item['title'], "publisher": item['publisher']}
        for i, item in enumerate(news_items)
    ], indent=2)
    
    prompt = f"""
    You are a professional financial market analyst.
    Analyze the following headlines for ticker symbol '{ticker}':

    {formatted_news}

    IMPORTANT CONSTRAINTS & GUARDRAILS:
    - Do NOT provide explicit investment advice, buy/sell recommendations, or financial guarantees.
    - Keep language natural, concise, and professional. Avoid cluttering with raw technical IDs like WKN or ISIN.
    - Summarize each individual news story in 1-2 sentences explaining its market implication.

    Return a JSON response strictly matching this structure:
    {{
      "executiveSummary": "A concise 2-sentence overall market briefing.",
      "sentiment": "Bullish" | "Bearish" | "Neutral",
      "keyTakeaways": ["Key point 1", "Key point 2", "Key point 3"],
      "itemSummaries": [
        {{"id": 0, "summary": "Concise summary for news item 0..."}}
      ]
    }}
    """

    client = OpenAI(api_key=api_key, base_url=settings.BASE_URL)
    completion = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    ai_raw = json.loads(completion.choices[0].message.content)
    
    # Map the individual summaries back to the news_items
    summaries_map = {item["id"]: item["summary"] for item in ai_raw.get("itemSummaries", [])}
    
    enriched_news = []
    for i, item in enumerate(news_items):
        item_copy = dict(item)
        item_copy["summary"] = summaries_map.get(i, item["title"])
        enriched_news.append(item_copy)

    # The exact format for SummaryResponse:
    # ticker, news, analysis (with executiveSummary, sentiment, keyTakeaways)
    result = {
        "ticker": ticker,
        "news": enriched_news,
        "analysis": {
            "executiveSummary": ai_raw.get("executiveSummary", ""),
            "sentiment": ai_raw.get("sentiment", "Neutral"),
            "keyTakeaways": ai_raw.get("keyTakeaways", [])
        }
    }

    _cache[ticker] = {
        "timestamp": now,
        "data": result
    }
    
    return result