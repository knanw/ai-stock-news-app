from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def sample_response(ticker="AAPL"):
    return {
        "ticker": ticker,
        "news": [{"title": "Apple launches product", "publisher": "Example", "link": "https://example.com", "publishTime": "2026-01-01", "summary": "Product launch."}],
        "analysis": {"executiveSummary": "A short briefing.", "sentiment": "Neutral", "keyTakeaways": ["Watch demand"]},
    }


def test_summary_normalizes_ticker_and_returns_summary(monkeypatch):
    monkeypatch.setattr(main, "fetch_latest_news", lambda ticker: [{"title": "Headline", "publisher": "Example", "link": "https://example.com", "publishTime": "Today"}])
    def fake_analyze(ticker, news, api_key):
        assert ticker == "AAPL"
        assert news[0]["title"] == "Headline"
        assert api_key == "user-key"
        return sample_response(ticker)
    monkeypatch.setattr(main, "analyze_stock_news", fake_analyze)

    response = client.post("/api/summary", json={"ticker": "  aapl ", "api_key": "user-key"})
    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"
    assert response.json()["analysis"]["sentiment"] == "Neutral"


def test_summary_missing_ticker_is_validation_error():
    response = client.post("/api/summary", json={"ticker": "   "})
    # The request schema accepts whitespace, then the route rejects it.
    assert response.status_code == 400
    assert response.json()["detail"] == "Ticker symbol is required."


def test_summary_maps_missing_api_key_to_401(monkeypatch):
    monkeypatch.setattr(main, "fetch_latest_news", lambda ticker: [])
    monkeypatch.setattr(main, "analyze_stock_news", lambda *args: (_ for _ in ()).throw(ValueError("API key missing")))
    response = client.post("/api/summary", json={"ticker": "MSFT"})
    assert response.status_code == 401
    assert response.json()["detail"] == "API key missing"


def test_summary_maps_unexpected_error_to_500(monkeypatch):
    monkeypatch.setattr(main, "fetch_latest_news", lambda ticker: (_ for _ in ()).throw(RuntimeError("upstream down")))
    response = client.post("/api/summary", json={"ticker": "MSFT"})
    assert response.status_code == 500
    assert "Internal Server Error" in response.json()["detail"]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
