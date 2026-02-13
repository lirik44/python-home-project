# Zentist – UI automation

Python + Playwright + Pytest tests for the-internet.herokuapp.com (login and main page).

## Run locally

**Setup (once):**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

**Run tests:**

```bash
pytest
```

Base URL is taken from env: `APP_BASE_URL` or from `.env`. Override from CLI:

```bash
pytest --app-base-url=https://the-internet.herokuapp.com
```

Credentials: `APP_USERNAME`, `APP_PASSWORD` (defaults in `config.py`).

## Layout

- `pages/` – page objects (base, main, login, secure).
- `tests/` – pytest tests and `conftest.py` (fixtures, base URL).
- `config.py` – base URL and credentials from env.

Allure results `allure serve allure-results`.
