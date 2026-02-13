"""Shared pytest fixtures: base URL (env/CLI), page objects."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import Page

from config import BASE_URL
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.secure_page import SecurePage


def pytest_addoption(parser: pytest.Parser) -> None:
    """App base URL override so tests can run against any environment."""
    parser.addoption(
        "--app-base-url",
        action="store",
        default=None,
        help="Override base URL for the app under test (else uses APP_BASE_URL / config).",
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """Base URL: --app-base-url > env/config > default."""
    cli_url = pytestconfig.getoption("app_base_url", default=None)
    if cli_url:
        return str(cli_url).rstrip("/")
    return BASE_URL


@pytest.fixture
def main_page(page: Page, base_url: str) -> Iterator[MainPage]:
    yield MainPage(page, base_url)


@pytest.fixture
def login_page(page: Page, base_url: str) -> Iterator[LoginPage]:
    yield LoginPage(page, base_url)


@pytest.fixture
def secure_page(page: Page, base_url: str) -> Iterator[SecurePage]:
    yield SecurePage(page, base_url)

