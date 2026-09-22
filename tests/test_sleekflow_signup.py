"""SleekFlow signup flow and signup-page regression tests."""
from uuid import uuid4

import pytest

from pages.automation_page import SleekFlowAutomationPage
from utils.mock_otp_api import MockOtpApi
from utils.config_reader import config
from utils.test_data import TestDataManager


AUTH_DATA = TestDataManager.load_yaml("test_data/test_scenarios.yaml")["sleekflow_auth"]
SIGNUP_CASES = [
    pytest.param(case, id=case["name"])
    for case in AUTH_DATA["signup"]
]
INVALID_EMAIL_CASES = [
    pytest.param(case, id=case["name"])
    for case in AUTH_DATA["signup_validation"]["invalid_emails"]
]
INVALID_PASSWORD_CASES = [
    pytest.param(case, id=case["name"])
    for case in AUTH_DATA["signup_validation"]["invalid_passwords"]
]


@pytest.mark.ui
@pytest.mark.slow
class TestSleekFlowSignup:
    """Tests for the SleekFlow signup flow."""

    @pytest.mark.parametrize("signup_case", SIGNUP_CASES)
    def test_signup_reaches_verification_and_enters_otp(self, page, signup_case):
        """Reach verification and enter the locally supplied OTP without claiming provider success."""
        if not config.signup_enabled:
            pytest.skip(
                "Set SLEEKFLOW_SIGNUP_ENABLED=true to opt in to account creation"
            )
        signup_username = config.signup_username
        signup_password = config.signup_password
        if not signup_username or not signup_password:
            pytest.skip(
                "Set SLEEKFLOW_SIGNUP_USERNAME and SLEEKFLOW_SIGNUP_PASSWORD to run"
            )

        local_part, domain = signup_username.rsplit("@", 1)
        signup_email = f"{local_part}{uuid4().int % 1_000_000}@{domain}"
        auth = SleekFlowAutomationPage(page)
        otp_api = MockOtpApi()
        otp_api.start()
        try:
            otp = auth.signup_and_enter_dummy_otp(signup_email, signup_password, otp_api.url)
        finally:
            otp_api.stop()

        assert otp == {
            "email": signup_email,
            "otp": signup_case["dummy_otp"],
            "source": "test",
        }
        assert all(
            auth.page.locator(auth.OTP_INPUT).nth(index).input_value() == digit
            for index, digit in enumerate(otp["otp"])
        )


@pytest.mark.regression
@pytest.mark.ui
class TestSleekFlowSignupRegression:
    """Regression coverage for signup navigation and controls."""

    def test_signup_to_login_navigation(self, page):
        """Navigate from signup to login using the visible auth link."""
        auth = SleekFlowAutomationPage(page)
        auth.open_signup()
        auth.open_login_from_signup()

        assert "/u/login/" in page.url

    def test_signup_elements_are_visible_and_interactive(self, page):
        """Fill signup data and accept terms without creating an account."""
        auth = SleekFlowAutomationPage(page)
        auth.open_signup()
        signup_case = AUTH_DATA["signup"][0]
        email = f"{signup_case['email_local_part']}@{signup_case['email_domain']}"

        assert auth.is_visible(auth.EMAIL_INPUT)
        assert auth.is_visible(auth.TERMS_CHECKBOX)
        assert auth.is_visible(auth.SIGNUP_BUTTON)

        auth.fill_email(email)
        auth.accept_terms()

        assert auth.page.locator(auth.EMAIL_INPUT).input_value() == email
        assert auth.page.locator(auth.TERMS_CHECKBOX).is_checked()

    @pytest.mark.parametrize("invalid_case", INVALID_EMAIL_CASES)
    def test_signup_rejects_invalid_email_formats(self, page, invalid_case):
        """Verify malformed email addresses are rejected on the signup screen."""
        auth = SleekFlowAutomationPage(page)
        auth.open_signup()
        auth.fill_email(invalid_case["email"])
        auth.accept_terms()
        auth.submit_signup()
        auth.assert_signup_error(invalid_case["expected_error"])

    @pytest.mark.parametrize("invalid_case", INVALID_PASSWORD_CASES)
    def test_signup_rejects_invalid_password_formats(self, page, invalid_case):
        """Verify weak password formats are rejected by the password step."""
        signup_username = config.signup_username
        if not signup_username:
            pytest.skip("Set SLEEKFLOW_SIGNUP_USERNAME to run")

        auth = SleekFlowAutomationPage(page)
        auth.open_signup()
        local_part, domain = signup_username.split("@", 1)
        unique_email = f"{local_part}+password-{uuid4().hex[:8]}@{domain}"
        auth.fill_email(unique_email)
        auth.accept_terms()
        auth.submit_signup()
        auth.complete_password_step(invalid_case["password"])
        auth.assert_signup_error(invalid_case["expected_error"])
