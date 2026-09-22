"""Smoke coverage for the SleekFlow login flow."""
import pytest

from pages.automation_page import SleekFlowAutomationPage
from utils.config_reader import config
from utils.test_data import TestDataManager


AUTH_DATA = TestDataManager.load_yaml("test_data/test_scenarios.yaml")[
    "sleekflow_auth"
]
LOGIN_PAGE_DATA = AUTH_DATA["login_page"]


def _find_case(cases: list[dict], name: str) -> dict:
    """Return a configured test case by name."""
    for case in cases:
        if case["name"] == name:
            return case
    raise ValueError(f"Configured SleekFlow test case was not found: {name}")


SMOKE_DATA = AUTH_DATA["smoke"]
SUCCESSFUL_LOGIN = _find_case(
    AUTH_DATA["login"], SMOKE_DATA["successful_login_case"]
)
NEGATIVE_LOGIN = _find_case(
    AUTH_DATA["negative_login"], SMOKE_DATA["negative_login_case"]
)


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.critical
class TestSleekFlowLoginSmoke:
    """Critical-path login smoke tests."""

    def test_login_page_is_ready(self, page):
        """Verify the login page loads with its essential controls and text."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()

        assert auth.is_visible(auth.EMAIL_INPUT)
        assert auth.is_visible(auth.CONTINUE_BUTTON)
        assert auth.is_visible(auth.GOOGLE_BUTTON)
        assert auth.is_visible(auth.APPLE_BUTTON)
        auth.assert_login_text(
            {
                "heading": LOGIN_PAGE_DATA["expected_heading"],
                "subheading": LOGIN_PAGE_DATA["expected_subheading"],
                "account_prompt": LOGIN_PAGE_DATA["expected_account_prompt"],
                "signup_link": LOGIN_PAGE_DATA["signup_link_text"],
            }
        )

    def test_successful_login(self, page):
        """Verify a provisioned account can complete the login flow."""
        if not config.login_username or not config.login_password:
            pytest.skip("Set SLEEKFLOW_LOGIN_USERNAME and SLEEKFLOW_LOGIN_PASSWORD to run")

        auth = SleekFlowAutomationPage(page)
        auth.login_with_credentials(
            config.login_username,
            config.login_password,
        )

        assert auth.verify_logged_in()
        assert (
            auth.capture_authenticated_element()
            == SUCCESSFUL_LOGIN["expected_authenticated_heading"]
        )

    def test_login_rejects_negative_identifier(self, page):
        """Verify the login page displays the configured validation message."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()
        auth.fill_email(NEGATIVE_LOGIN["email"])
        auth.submit_identifier()
        auth.assert_login_error(NEGATIVE_LOGIN["expected_error"])
