"""Base page: common navigation and URL helpers."""

from __future__ import annotations

from playwright.sync_api import Page, Response


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str | None = None, timeout: float = 60_000) -> Response | None:
        if path:
            url = f"{self.base_url}/{path.lstrip('/')}"
        else:
            url = self.base_url
        return self.page.goto(url, timeout=timeout)

    @property
    def current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()
