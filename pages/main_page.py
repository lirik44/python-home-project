"""Main landing page: examples list, link to login form."""

from __future__ import annotations

from playwright.sync_api import Locator, Response, expect

from .base_page import BasePage


class MainPage(BasePage):
    def open_main(self) -> Response | None:
        response = self.open()
        expect(self.page).to_have_url(self.base_url + "/")
        return response

    def open_login_page(self) -> None:
        self.page.get_by_text("Form Authentication").click()

    def get_github_ribbon(self) -> Locator:
        return self.page.get_by_alt_text("Fork me on GitHub")

    def get_examples_links_quantity(self) -> int:
        return self.page.locator("#content a").count()


