"""Main page: load, title, GitHub ribbon, examples link count."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser

from pages.main_page import MainPage

# Expected number of example links on the-internet herokuapp main page (stable for this app)
EXPECTED_EXAMPLES_LINKS = 44


@pytest.fixture(scope="module")
def main_page_scenario(browser: Browser, base_url: str) -> Iterator[MainPage]:
    """One session: open main page once. All tests use same tab."""
    page = browser.new_page()
    main_page = MainPage(page, base_url)
    response = main_page.open_main()
    assert response is not None and response.status == 200
    yield main_page
    page.close()


def test_main_page_is_opened(main_page_scenario: MainPage) -> None:
    assert main_page_scenario.current_url.startswith(main_page_scenario.base_url)


def test_main_page_has_title(main_page_scenario: MainPage) -> None:
    assert main_page_scenario.get_title(), "Page should have a title"


def test_main_page_has_github_ribbon(main_page_scenario: MainPage) -> None:
    assert main_page_scenario.get_github_ribbon().is_visible(), "GitHub ribbon should be visible"


def test_main_page_has_expected_links_count(main_page_scenario: MainPage) -> None:
    assert main_page_scenario.get_examples_links_quantity() == EXPECTED_EXAMPLES_LINKS
    