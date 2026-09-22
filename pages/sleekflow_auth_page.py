"""Shared selectors and behavior for SleekFlow authentication page objects."""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.test_data import TestDataManager


AUTH_DATA = TestDataManager.load_yaml("test_data/test_scenarios.yaml")["sleekflow_auth"]
WAIT_CONFIG = AUTH_DATA["waits"]


class SleekFlowAuthPage(BasePage):
    """Shared foundation for the SleekFlow login and signup page objects."""

    SIGNUP_URL = f"{config.base_url}/en?screen_hint=signup"
    LOGIN_URL = f"{config.base_url}/en/inbox?screen_hint=login"
    APP_URL_PATTERN = f"{config.base_url}/**"
    SSO_HOST = "sso.sleekflow.io"

    EMAIL_INPUT = "input#email, input[type='email'], input[name='username']"
    PASSWORD_INPUT = "input#password"
    TERMS_CHECKBOX = "input[name='ulp-terms-of-service']"
    CONTINUE_BUTTON = "button[type='submit'][name='action'][value='default']"
    OTP_INPUT = (
        "input[name='code'], input[autocomplete='one-time-code'], "
        "input[inputmode='numeric'], input[maxlength='1']"
    )
    GOOGLE_BUTTON = "button[data-provider='google']"
    APPLE_BUTTON = "button[data-provider='apple']"
    GOOGLE_EMAIL_INPUT = "input[name='identifier']"
    GOOGLE_NEXT_BUTTON = "#identifierNext"
    GOOGLE_PASSWORD_INPUT = "input[name='Passwd']"
    GOOGLE_PASSWORD_NEXT_BUTTON = "#passwordNext"
    SIGNUP_BUTTON = "button[type='submit'][name='action'][value='default']"
    SIGNUP_VERIFICATION_TEXT = "text=Confirm your email address"
    AUTHENTICATED_HEADING = "text=What's your company name?"

    @property
    def page_load_timeout(self) -> int:
        """Return the configured page-load timeout in milliseconds."""
        return WAIT_CONFIG["page_load_ms"]

    @property
    def navigation_timeout(self) -> int:
        """Return the configured authentication navigation timeout."""
        return WAIT_CONFIG["navigation_ms"]

    @property
    def oauth_timeout(self) -> int:
        """Return the configured OAuth timeout."""
        return WAIT_CONFIG["oauth_ms"]

    @property
    def verification_timeout(self) -> int:
        """Return the configured verification timeout."""
        return WAIT_CONFIG["verification_ms"]
