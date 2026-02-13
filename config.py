"""App under test: base URL and test credentials (env / .env)."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://the-internet.herokuapp.com"
BASE_URL: str = os.getenv("APP_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
USERNAME: str = os.getenv("APP_USERNAME", "tomsmith")
PASSWORD: str = os.getenv("APP_PASSWORD", "SuperSecretPassword!")

