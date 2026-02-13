"""Login page: form and flash message."""

from __future__ import annotations

from playwright.sync_api import expect

from .base_page import BasePage


class LoginPage(BasePage):
    _username_input = "#username"
    _password_input = "#password"
    _submit_button = "button[type='submit']"
    _flash_message = "#flash"

    def open_login(self) -> None:
        self.open("login")
        expect(self.page).to_have_url(self.base_url + "/login")

    def login(self, username: str, password: str) -> None:
        self.page.fill(self._username_input, username)
        self.page.fill(self._password_input, password)
        self.page.click(self._submit_button)

    def get_flash_message(self) -> str:
        flash = self.page.locator(self._flash_message)
        expect(flash).to_be_visible()
        text = flash.inner_text().strip()
        return " ".join(text.split())

