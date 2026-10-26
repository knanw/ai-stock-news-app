import requests
from services import news_service


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
    def json(self):
        return self.payload


def test_fetch_latest_news_maps_provider_payload(monkeypatch):
    monkeypatch.setattr(news_service.requests, "get", lambda *a, **kw: FakeResponse({"news": [{"title": "Headline", "publisher": "Publisher", "link": "https://example.com", "providerPublishTime": 0}]}))
    items = news_service.fetch_latest_news("AAPL")
    assert len(items) == 1
    assert items[0]["title"] == "Headline"
    assert items[0]["publisher"] == "Publisher"
    assert items[0]["link"] == "https://example.com"
    assert items[0]["publishTime"]


def test_fetch_latest_news_falls_back_when_provider_fails(monkeypatch):
    def raise_error(*args, **kwargs):
        raise requests.RequestException("offline")
    monkeypatch.setattr(news_service.requests, "get", raise_error)
    items = news_service.fetch_latest_news("TSLA")
    assert len(items) >= 1
    assert all("title" in item and "publisher" in item for item in items)
    assert all("TSLA" in item["title"] for item in items)


def test_fetch_latest_news_falls_back_when_no_news(monkeypatch):
    monkeypatch.setattr(news_service.requests, "get", lambda *a, **kw: FakeResponse({"news": []}))
    assert news_service.fetch_latest_news("NVDA")
