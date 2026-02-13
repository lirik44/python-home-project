"""Positive login flow: valid credentials, secure area, logout."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser, expect

from config import PASSWORD, USERNAME
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.secure_page import SecurePage


@pytest.fixture(scope="module")
def login_positive_scenario(
    browser: Browser, base_url: str
) -> Iterator[tuple[LoginPage, SecurePage]]:
    """One session: open main -> login -> authorize. Tests start on secure page."""
    page = browser.new_page()
    main_page = MainPage(page, base_url)
    login_page = LoginPage(page, base_url)
    secure_page = SecurePage(page, base_url)
    response = main_page.open_main()
    assert response is not None and response.status == 200
    main_page.open_login_page()
    expect(login_page.page).to_have_url(login_page.base_url + "/login")
    login_page.login(USERNAME, PASSWORD)
    yield login_page, secure_page
    page.close()


def test_successful_login_redirects_to_secure_area(
    login_positive_scenario: tuple[LoginPage, SecurePage],
) -> None:
    _, secure_page = login_positive_scenario
    assert secure_page.base_url + "/secure" in secure_page.current_url
    secure_page.is_loaded()
    assert "You logged into a secure area!" in secure_page.get_flash_message()


def test_secure_page_has_title_and_content(
    login_positive_scenario: tuple[LoginPage, SecurePage],
) -> None:
    _, secure_page = login_positive_scenario
    assert secure_page.get_title(), "Page should have a title"
    content_h2 = secure_page.page.locator("#content h2")
    expect(content_h2).to_have_text("Secure Area")
    content_h4 = secure_page.page.locator("#content h4")
    expect(content_h4).to_have_text(
        "Welcome to the Secure Area. When you are done click logout below."
    )


def test_secure_page_has_logout_button(
    login_positive_scenario: tuple[LoginPage, SecurePage],
) -> None:
    _, secure_page = login_positive_scenario
    logout_link = secure_page.page.locator("#content div a")
    expect(logout_link).to_be_visible()
    expect(logout_link).to_contain_text("Logout")


def test_logout_and_assert_user_logged_out(
    login_positive_scenario: tuple[LoginPage, SecurePage],
) -> None:
    login_page, secure_page = login_positive_scenario
    secure_page.logout()
    expect(login_page.page).to_have_url(login_page.base_url + "/login")
    assert "You logged out of the secure area!" in login_page.get_flash_message()
