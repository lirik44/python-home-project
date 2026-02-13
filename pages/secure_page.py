"""Secure area page: header, flash message, logout."""

from __future__ import annotations

from playwright.sync_api import expect

from .base_page import BasePage


class SecurePage(BasePage):
    _header = "h2"
    _flash_message = "#flash"

    def is_loaded(self) -> None:
        expect(self.page).to_have_url(self.base_url + "/secure")
        expect(self.page.locator(self._header)).to_have_text("Secure Area")

    def get_flash_message(self) -> str:
        flash = self.page.locator(self._flash_message)
        expect(flash).to_be_visible()
        text = flash.inner_text().strip()
        return " ".join(text.split())

    def logout(self) -> None:
        logout_link = self.page.locator("#content div a")
        expect(logout_link).to_contain_text("Logout")
        logout_link.click()

