import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.PROJECT_NAME = "Stock News Summary API"

        self.API_KEY = os.getenv("API_KEY", "").strip()

        base_url = os.getenv("BASE_URL", "").strip()
        self.BASE_URL = base_url or None

        self.MODEL_NAME = (
            os.getenv("MODEL_NAME", "").strip() or "gpt-4o-mini"
        )


settings = Settings()
