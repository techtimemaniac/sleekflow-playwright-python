"""SleekFlow login flow and login-page regression tests."""
import pytest

from pages.automation_page import SleekFlowAutomationPage
from utils.config_reader import config
from utils.test_data import TestDataManager


AUTH_DATA = TestDataManager.load_yaml("test_data/test_scenarios.yaml")["sleekflow_auth"]
LOGIN_CASES = [
    pytest.param(case, id=case["name"])
    for case in AUTH_DATA["login"]
]
NEGATIVE_LOGIN_CASES = [
    pytest.param(case, id=case["name"])
    for case in AUTH_DATA["negative_login"]
]
LOGIN_PAGE_DATA = AUTH_DATA["login_page"]


@pytest.mark.ui
@pytest.mark.critical
class TestSleekFlowLogin:
    """Tests for logging in with a provisioned SleekFlow account."""

    @pytest.mark.parametrize("login_case", LOGIN_CASES)
    def test_login_with_signup_account(self, page, login_case):
        """Log in with each configured account and verify authenticated content."""
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
            == login_case["expected_authenticated_heading"]
        )

    @pytest.mark.skipif(
        not config.google_login_enabled,
        reason="Set SLEEKFLOW_GOOGLE_LOGIN_ENABLED=true to open Google OAuth",
    )
    def test_login_with_google(self, page):
        """Open Google OAuth without submitting external account credentials."""
        auth = SleekFlowAutomationPage(page)
        auth.login_with_google()
        page.wait_for_url(
            "https://accounts.google.com/**", timeout=auth.oauth_timeout
        )
        assert LOGIN_PAGE_DATA["oauth_hosts"]["google"] in page.url

    @pytest.mark.skipif(
        not config.apple_login_enabled,
        reason="Set SLEEKFLOW_APPLE_LOGIN_ENABLED=true to open Apple OAuth",
    )
    def test_login_with_apple(self, page):
        """Open Apple OAuth without submitting external account credentials."""
        auth = SleekFlowAutomationPage(page)
        auth.login_with_apple()
        page.wait_for_url(
            "https://appleid.apple.com/**", timeout=auth.oauth_timeout
        )
        assert LOGIN_PAGE_DATA["oauth_hosts"]["apple"] in page.url


@pytest.mark.regression
@pytest.mark.ui
class TestSleekFlowLoginRegression:
    """Regression coverage for login navigation and controls."""

    def test_login_to_signup_navigation(self, page):
        """Navigate from login to signup using the visible auth link."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()
        auth.open_signup_from_login()

        assert LOGIN_PAGE_DATA["navigation_paths"]["signup"] in page.url

    @pytest.mark.parametrize("negative_case", NEGATIVE_LOGIN_CASES)
    def test_negative_login_scenarios(self, page, negative_case):
        """Verify validation and authentication errors for invalid login data."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()
        auth.fill_email(negative_case["email"])

        if negative_case["expected_stage"] == "password":
            auth.submit_identifier()
            assert auth.is_visible(auth.PASSWORD_INPUT)
            return

        if negative_case["expected_stage"] == "error":
            auth.submit_identifier()
            auth.assert_login_error(negative_case["expected_error"])
            return

        auth.submit_identifier()
        auth.wait_for_element(auth.PASSWORD_INPUT, timeout=auth.navigation_timeout)
        auth.page.locator(auth.PASSWORD_INPUT).fill(negative_case["password"])
        auth.page.get_by_role("button", name="Sign in", exact=True).click()
        auth.assert_login_error(negative_case["expected_error"])

    def test_login_elements_are_visible(self, page):
        """Verify login inputs and social login controls are available."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()

        assert auth.is_visible(auth.EMAIL_INPUT)
        assert auth.is_visible(auth.GOOGLE_BUTTON)
        assert auth.is_visible(auth.APPLE_BUTTON)
        auth.fill_email(AUTH_DATA["login"][0]["email"])
        auth.continue_login()
        assert auth.page.get_by_text("Edit", exact=True).is_visible()
        assert auth.page.get_by_role(
            "switch", name="Show password", exact=True
        ).is_visible()

    def test_login_edit_button_returns_to_identifier_step(self, page):
        """Verify Edit returns to the identifier screen with the email preserved."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()
        auth.fill_email(AUTH_DATA["login"][0]["email"])
        auth.continue_login()
        auth.edit_login_identifier()

        assert auth.page.locator(auth.EMAIL_INPUT).input_value() == AUTH_DATA["login"][0][
            "email"
        ]
        assert auth.is_visible(auth.CONTINUE_BUTTON)

    def test_login_eye_icon_toggles_password_visibility(self, page):
        """Verify the password eye control toggles between hidden and visible text."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()
        auth.fill_email(AUTH_DATA["login"][0]["email"])
        auth.continue_login()
        auth.fill(auth.PASSWORD_INPUT, "Password123!")

        assert auth.page.locator(auth.PASSWORD_INPUT).get_attribute("type") == "password"
        auth.toggle_password_visibility()
        assert auth.page.locator(auth.PASSWORD_INPUT).get_attribute("type") == "text"
        assert auth.is_visible(auth.HIDE_PASSWORD_BUTTON)

    def test_login_buttons_are_visible_and_enabled(self, page):
        """Verify configured login buttons are visible, enabled, and labeled."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()

        auth.assert_login_buttons(LOGIN_PAGE_DATA["buttons"])

    def test_login_text_elements_are_visible(self, page):
        """Verify the main login-page text elements are displayed."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()

        auth.assert_login_text(
            {
                "heading": LOGIN_PAGE_DATA["expected_heading"],
                "subheading": LOGIN_PAGE_DATA["expected_subheading"],
                "account_prompt": LOGIN_PAGE_DATA["expected_account_prompt"],
                "signup_link": LOGIN_PAGE_DATA["signup_link_text"],
            }
        )
        assert auth.is_visible(auth.CONTINUE_BUTTON)

    def test_login_language_dropdown_is_interactive(self, page):
        """Verify the language selector opens and exposes English."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()

        assert auth.is_visible(auth.LANGUAGE_SELECT)
        auth.open_language_dropdown()
        language = LOGIN_PAGE_DATA["language"]
        option = auth.page.locator(f"{auth.LANGUAGE_OPTION} #{language['option_id']}")
        assert option.is_visible()
        assert option.get_by_text(language["label"], exact=True).is_visible()
        auth.select_language(language["option_id"])

    def test_login_images_are_visible(self, page):
        """Verify the login branding and feature images are loaded."""
        auth = SleekFlowAutomationPage(page)
        auth.open_login()

        assert auth.is_visible(auth.LOGO_IMAGE)
        visible_images = auth.page.locator("img:visible")
        assert visible_images.count() >= 2
