
from config import Settings


def test_openai_defaults(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("MODEL_NAME", raising=False)

    settings = Settings()

    assert settings.API_KEY == ""
    assert settings.BASE_URL is None
    assert settings.MODEL_NAME == "gpt-4o-mini"


def test_openai_configuration(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-openai-key")
    monkeypatch.setenv("BASE_URL", "")
    monkeypatch.setenv("MODEL_NAME", "gpt-4o-mini")

    settings = Settings()

    assert settings.API_KEY == "test-openai-key"
    assert settings.BASE_URL is None
    assert settings.MODEL_NAME == "gpt-4o-mini"


def test_groq_configuration(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-groq-key")
    monkeypatch.setenv(
        "BASE_URL",
        "https://api.groq.com/openai/v1",
    )
    monkeypatch.setenv("MODEL_NAME", "qwen/qwen3.8-27b")

    settings = Settings()

    assert settings.API_KEY == "test-groq-key"
    assert settings.BASE_URL == "https://api.groq.com/openai/v1"
    assert settings.MODEL_NAME == "qwen/qwen3.8-27b"


def test_custom_model_is_supported(monkeypatch):
    monkeypatch.setenv("MODEL_NAME", "my-custom-model")

    settings = Settings()

    assert settings.MODEL_NAME == "my-custom-model"
