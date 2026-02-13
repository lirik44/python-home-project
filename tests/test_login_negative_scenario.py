"""Negative login: invalid/empty credentials, wrong case, injection-like input."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from faker import Faker
from playwright.sync_api import Browser, expect

from config import PASSWORD, USERNAME
from pages.login_page import LoginPage
from pages.main_page import MainPage


@pytest.fixture(scope="module")
def login_page_scenario(browser: Browser, base_url: str) -> Iterator[LoginPage]:
    """One session: open main -> login page. Tests start on login page."""
    page = browser.new_page()
    main_page = MainPage(page, base_url)
    login_page = LoginPage(page, base_url)
    response = main_page.open_main()
    assert response is not None and response.status == 200
    main_page.open_login_page()
    yield login_page
    page.close()


@pytest.fixture(autouse=True)
def ensure_on_login_page(login_page_scenario: LoginPage) -> Iterator[None]:
    """Bring browser back to login page before each test (shared session)."""
    login_page_scenario.open_login()
    yield


def test_login_page_is_opened(login_page_scenario: LoginPage) -> None:
    assert login_page_scenario.current_url.startswith(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_empty_credentials_shows_error(login_page_scenario: LoginPage) -> None:
    login_page_scenario.login("", "")
    assert "Your username is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_valid_username_and_empty_password_shows_error(
    login_page_scenario: LoginPage,
) -> None:
    login_page_scenario.login(USERNAME, "")
    assert "Your password is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_empty_username_and_valid_password_shows_error(
    login_page_scenario: LoginPage,
) -> None:
    login_page_scenario.login("", PASSWORD)
    assert "Your username is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_valid_username_and_random_password_shows_error(
    login_page_scenario: LoginPage,
) -> None:
    login_page_scenario.login(USERNAME, Faker().password())
    assert "Your password is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_random_username_and_valid_password_shows_error(
    login_page_scenario: LoginPage,
) -> None:
    login_page_scenario.login(Faker().user_name(), PASSWORD)
    assert "Your username is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_username_wrong_case_shows_error(login_page_scenario: LoginPage) -> None:
    login_page_scenario.login(USERNAME.upper(), PASSWORD)
    assert "Your username is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )


def test_login_with_injection_like_input_shows_error(login_page_scenario: LoginPage) -> None:
    login_page_scenario.login("' OR '1'='1", PASSWORD)
    assert "Your username is invalid!" in login_page_scenario.get_flash_message()
    expect(login_page_scenario.page).to_have_url(
        login_page_scenario.base_url + "/login"
    )
