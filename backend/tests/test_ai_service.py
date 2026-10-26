import json
from types import SimpleNamespace
import pytest
from services import ai_service


class FakeCompletions:
    def __init__(self, content):
        self.content = content
        self.kwargs = None
    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))])


class FakeOpenAI:
    completions = None
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.chat = SimpleNamespace(completions=self.completions)


def setup_function():
    ai_service._cache.clear()


def test_analyze_stock_news_formats_result_and_caches(monkeypatch):
    news = [{"title": "Headline", "publisher": "Publisher", "link": "https://example.com", "publishTime": "Today"}]
    fake = FakeCompletions(json.dumps({"executiveSummary": "Overall summary", "sentiment": "Bullish", "keyTakeaways": ["Takeaway"], "itemSummaries": [{"id": 0, "summary": "Story summary"}]}))
    FakeOpenAI.completions = fake
    monkeypatch.setattr(ai_service, "OpenAI", FakeOpenAI)
    monkeypatch.setattr(ai_service.settings, "API_KEY", "configured-key")

    result = ai_service.analyze_stock_news("AAPL", news)
    assert result["ticker"] == "AAPL"
    assert result["news"][0]["summary"] == "Story summary"
    assert result["analysis"]["sentiment"] == "Bullish"
    assert FakeOpenAI.completions.kwargs["response_format"] == {"type": "json_object"}

    # A second request within TTL returns cached data without a second model call.
    result2 = ai_service.analyze_stock_news("AAPL", news)
    assert result2 == result


def test_analyze_stock_news_requires_api_key(monkeypatch):
    monkeypatch.setattr(ai_service.settings, "API_KEY", "")
    with pytest.raises(ValueError, match="API Key is missing"):
        ai_service.analyze_stock_news("MSFT", [])


def test_analyze_stock_news_uses_title_when_item_summary_missing(monkeypatch):
    news = [{"title": "Original title", "publisher": "Publisher", "link": "#", "publishTime": "Today"}]
    FakeOpenAI.completions = FakeCompletions(json.dumps({"executiveSummary": "Summary", "sentiment": "Neutral", "keyTakeaways": [], "itemSummaries": []}))
    monkeypatch.setattr(ai_service, "OpenAI", FakeOpenAI)
    monkeypatch.setattr(ai_service.settings, "API_KEY", "configured-key")
    result = ai_service.analyze_stock_news("IBM", news)
    assert result["news"][0]["summary"] == "Original title"
